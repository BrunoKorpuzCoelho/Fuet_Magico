import json
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.core.multi_company import get_active_company
from apps.accounts.decorators import admin_required
from apps.inventory.models import Product, UoM
from apps.core.models import Company
from .models import ProductBOM, ProductBOMLine
from .forms import ProductBOMForm


@login_required
def bom_dashboard(request):
    company = get_active_company(request)
    search_query = request.GET.get('search', '').strip()
    search_field = request.GET.get('field', '')
    status_filter = request.GET.get('status', 'active')
    page = request.GET.get('page', 1)
    page_size = int(request.GET.get('page_size', 100))

    boms = ProductBOM.objects.filter(
        Q(owner_company=company) | Q(owner_company__isnull=True)
    ).select_related('product', 'uom')

    if status_filter == 'archived':
        boms = boms.filter(is_active=False)
    else:
        boms = boms.filter(is_active=True)

    if search_query:
        if search_field == 'reference':
            boms = boms.filter(product__internal_reference__icontains=search_query)
        elif search_field == 'uom':
            boms = boms.filter(uom__name__icontains=search_query)
        else:
            boms = boms.filter(product__name__icontains=search_query)

    boms = boms.annotate(lines_count=Count('lines')).order_by('product__name')
    total_count = boms.count()

    paginator = Paginator(boms, page_size)
    boms_page = paginator.get_page(page)

    return render(request, 'bom/bom_dashboard.html', {
        'boms': boms_page,
        'search_query': search_query,
        'search_field': search_field,
        'status_filter': status_filter,
        'page_size': page_size,
        'total_count': total_count,
    })

@login_required
def bom_list(request):
    company = get_active_company(request)
    q = request.GET.get('q', '').strip()
    boms = ProductBOM.objects.filter(
        Q(owner_company=company) | Q(owner_company__isnull=True)
    ).select_related('product', 'uom')

    if q:
        boms = boms.filter(product__name__icontains=q)

    boms = boms.order_by('product__name')
    return render(request, 'bom/bom_list.html', {
        'boms': boms,
        'q': q,
    })


@require_http_methods(["POST"])
@login_required
def bom_bulk_archive(request):
    try:
        data = json.loads(request.body)
        bom_ids = data.get('bom_ids', [])
        if not bom_ids:
            return JsonResponse({'success': False, 'error': {'code': 'NO_ITEMS', 'message': 'Nenhuma receita selecionada'}}, status=400)
        count = ProductBOM.objects.filter(id__in=bom_ids).update(is_active=False)
        return JsonResponse({'success': True, 'message': f'{count} receita(s) arquivada(s) com sucesso.'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bom_bulk_unarchive(request):
    try:
        data = json.loads(request.body)
        bom_ids = data.get('bom_ids', [])
        if not bom_ids:
            return JsonResponse({'success': False, 'error': {'code': 'NO_ITEMS', 'message': 'Nenhuma receita selecionada'}}, status=400)
        count = ProductBOM.objects.filter(id__in=bom_ids).update(is_active=True)
        return JsonResponse({'success': True, 'message': f'{count} receita(s) desarquivada(s) com sucesso.'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
@admin_required
def bom_bulk_delete(request):
    try:
        data = json.loads(request.body)
        bom_ids = data.get('bom_ids', [])
        if not bom_ids:
            return JsonResponse({'success': False, 'error': {'code': 'NO_ITEMS', 'message': 'Nenhuma receita selecionada'}}, status=400)
        deleted, _ = ProductBOM.objects.filter(id__in=bom_ids).delete()
        return JsonResponse({'success': True, 'message': f'{deleted} receita(s) eliminada(s) permanentemente.'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Erro inesperado'}}, status=500)


# ── Formulário de criação / edição ───────────────────────────────────────────

def _bom_form_context(request, form, bom=None):
    """Context partilhado entre create e edit."""
    import json as _json
    uoms = UoM.objects.filter(is_active=True).select_related('category').order_by('name')
    companies = Company.objects.filter(is_active=True).order_by('name')

    # Pre-populate product autocomplete when editing
    selected_product = None
    if bom and bom.product_id:
        selected_product = {
            'id': str(bom.product.pk),
            'name': bom.product.name,
            'internal_reference': bom.product.internal_reference or '',
        }
    elif form.data.get('product'):
        try:
            p = Product.objects.get(pk=form.data['product'])
            selected_product = {
                'id': str(p.pk),
                'name': p.name,
                'internal_reference': p.internal_reference or '',
            }
        except Product.DoesNotExist:
            pass

    # Initial lines JSON (only when editing a saved BOM)
    initial_lines = []
    if bom and bom.pk:
        for line in bom.lines.select_related('component', 'uom').order_by('sequence', 'component__name'):
            initial_lines.append(_line_to_dict(line))

    return {
        'form': form,
        'bom': bom,
        'uoms': uoms,
        'companies': companies,
        'selected_product': selected_product,
        'initial_lines_json': _json.dumps(initial_lines),
    }


@login_required
def bom_create(request):
    """Criar nova receita BOM."""
    if request.method == 'POST':
        form = ProductBOMForm(request.POST)
        if form.is_valid():
            bom = form.save(commit=False)
            if not bom.owner_company:
                bom.owner_company = get_active_company(request)
            bom.save()
            # Marcar produto como manufaturado ao associar uma receita
            if not bom.product.is_manufactured:
                bom.product.is_manufactured = True
                bom.product.save(update_fields=['is_manufactured', 'updated_at'])
            if bom.product.is_manufactured:
                bom.sync_to_product()
            messages.success(request, f'Receita "{bom.product.name}" criada com sucesso!')
            return redirect('bom:bom_edit', bom_id=bom.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductBOMForm()

    return render(request, 'bom/bom_form.html', _bom_form_context(request, form))


@login_required
def bom_edit(request, bom_id):
    """Editar receita BOM existente."""
    bom = get_object_or_404(ProductBOM, pk=bom_id)

    if request.method == 'POST':
        form = ProductBOMForm(request.POST, instance=bom)
        if form.is_valid():
            bom = form.save(commit=False)
            if not bom.owner_company:
                bom.owner_company = get_active_company(request)
            bom.save()
            if bom.product.is_manufactured:
                bom.sync_to_product()
            messages.success(request, f'Receita "{bom.product.name}" guardada com sucesso!')
            return redirect('bom:bom_edit', bom_id=bom.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductBOMForm(instance=bom)

    return render(request, 'bom/bom_form.html', _bom_form_context(request, form, bom=bom))


# ── BOM Lines API ─────────────────────────────────────────────────────────────

@require_http_methods(["GET", "POST"])
@login_required
def bom_lines_api(request, bom_id):
    bom = get_object_or_404(ProductBOM, pk=bom_id)

    if request.method == 'GET':
        lines = bom.lines.select_related('component', 'uom').order_by('sequence', 'component__name')
        data = [_line_to_dict(line) for line in lines]
        return JsonResponse({'lines': data})

    # POST — create a new line
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    err, line = _save_line(bom, None, payload)
    if err:
        return JsonResponse({'error': err}, status=400)
    if bom.product.is_manufactured:
        bom.sync_to_product()
    return JsonResponse(_line_to_dict(line), status=201)


@require_http_methods(["PUT", "DELETE"])
@login_required
def bom_line_detail_api(request, bom_id, line_id):
    bom  = get_object_or_404(ProductBOM, pk=bom_id)
    line = get_object_or_404(ProductBOMLine, pk=line_id, bom=bom)

    if request.method == 'DELETE':
        line.delete()
        if bom.product.is_manufactured:
            bom.sync_to_product()
        return JsonResponse({'ok': True})

    # PUT
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    err, line = _save_line(bom, line, payload)
    if err:
        return JsonResponse({'error': err}, status=400)
    if bom.product.is_manufactured:
        bom.sync_to_product()
    return JsonResponse(_line_to_dict(line))


def _line_to_dict(line):
    comp = line.component
    return {
        'id':            str(line.pk),
        'sequence':      line.sequence,
        'component_id':  str(line.component_id),
        'component_name': comp.name,
        'component_ref':  comp.internal_reference or '',
        'quantity':      str(line.quantity),
        'uom_id':        str(line.uom_id),
        'uom_name':      line.uom.name,
        'uom_symbol':    line.uom.symbol,
        'notes':         line.notes,
        'cost_price':    float(comp.cost_price or 0),
        'sale_price':    float(comp.sale_price or 0),
    }


def _save_line(bom, line, payload):
    from apps.inventory.models import Product, UoM
    from decimal import Decimal, InvalidOperation

    component_id = payload.get('component_id', '')
    uom_id       = payload.get('uom_id', '')
    try:
        quantity = Decimal(str(payload.get('quantity', '1')))
        if quantity <= 0:
            raise ValueError
    except (InvalidOperation, ValueError):
        return 'Quantidade inválida.', None

    try:
        component = Product.objects.get(pk=component_id, is_active=True)
    except Product.DoesNotExist:
        return 'Componente não encontrado.', None

    try:
        uom = UoM.objects.get(pk=uom_id) if uom_id else component.uom
    except UoM.DoesNotExist:
        return 'Unidade de medida não encontrada.', None

    if line is None:
        line = ProductBOMLine(bom=bom)

    line.component = component
    line.uom       = uom
    line.quantity  = quantity
    line.sequence  = int(payload.get('sequence', 10))
    line.notes     = payload.get('notes', '')[:255]
    line.save()
    return None, line


# ══════════════════════════════════════════════════════════════════════════════
# RELATÓRIOS BOM
# ══════════════════════════════════════════════════════════════════════════════

@login_required
def bom_reports(request):
    """Hub de relatórios BOM."""
    company = get_active_company(request)

    boms_qs = ProductBOM.objects.filter(is_active=True).select_related('product')
    if company:
        boms_qs = boms_qs.filter(Q(owner_company=company) | Q(owner_company__isnull=True))

    total_boms = boms_qs.count()

    from apps.inventory.models import Product as Prod
    mfg_qs = Prod.objects.filter(is_active=True, is_manufactured=True)
    if company:
        mfg_qs = mfg_qs.filter(Q(owner_company=company) | Q(owner_company__isnull=True))
    total_manufactured = mfg_qs.count()
    boms_without_bom = mfg_qs.filter(bom__isnull=True).count()

    # Margem média
    margins = []
    for bom in boms_qs.prefetch_related('lines__component'):
        cost = bom.calculate_unit_cost()
        sale = bom.product.sale_price or Decimal('0')
        if sale > 0:
            margins.append(float((sale - cost) / sale * 100))
    avg_margin_pct = round(sum(margins) / len(margins), 1) if margins else 0

    return render(request, 'bom/reports_index.html', {
        'total_boms':        total_boms,
        'total_manufactured': total_manufactured,
        'avg_margin_pct':    avg_margin_pct,
        'boms_without_bom':  boms_without_bom,
    })


@login_required
def report_bom_cost_analysis(request):
    """Análise de custo por receita — breakdown de componentes."""
    company = get_active_company(request)

    boms_qs = ProductBOM.objects.filter(is_active=True).select_related(
        'product', 'uom'
    ).prefetch_related('lines__component', 'lines__uom')
    if company:
        boms_qs = boms_qs.filter(Q(owner_company=company) | Q(owner_company__isnull=True))
    boms_qs = boms_qs.order_by('product__name')

    rows = []
    total_boms = 0
    cost_sum = Decimal('0')
    highest = None

    for bom in boms_qs:
        total_boms += 1
        unit_cost  = bom.calculate_unit_cost()
        total_cost = bom.calculate_total_cost()
        cost_sum  += unit_cost
        if highest is None or unit_cost > highest['unit_cost']:
            highest = {'name': bom.product.name, 'unit_cost': unit_cost}

        components = []
        for line in bom.lines.all():
            comp_cost = (line.component.cost_price or Decimal('0')) * line.quantity
            pct = float(comp_cost / total_cost * 100) if total_cost > 0 else 0
            components.append({
                'name':      line.component.name,
                'reference': line.component.internal_reference or '',
                'quantity':  line.quantity,
                'uom':       line.uom.symbol,
                'unit_cost': line.component.cost_price or Decimal('0'),
                'subtotal':  comp_cost,
                'pct':       round(pct, 1),
            })

        rows.append({
            'bom':         bom,
            'unit_cost':   unit_cost,
            'total_cost':  total_cost,
            'components':  components,
        })

    avg_unit_cost = (cost_sum / total_boms).quantize(Decimal('0.01')) if total_boms else Decimal('0')

    chart_labels = json.dumps([r['bom'].product.name for r in rows])
    chart_values = json.dumps([float(r['unit_cost']) for r in rows])

    return render(request, 'bom/report_cost_analysis.html', {
        'rows':          rows,
        'total_boms':    total_boms,
        'avg_unit_cost': avg_unit_cost,
        'highest':       highest,
        'chart_labels':  chart_labels,
        'chart_values':  chart_values,
    })


@login_required
def report_bom_margin(request):
    """Relatório de margem de lucro por receita."""
    company = get_active_company(request)

    boms_qs = ProductBOM.objects.filter(is_active=True).select_related(
        'product', 'uom'
    ).prefetch_related('lines__component')
    if company:
        boms_qs = boms_qs.filter(Q(owner_company=company) | Q(owner_company__isnull=True))
    boms_qs = boms_qs.order_by('product__name')

    rows = []
    best = worst = None

    for bom in boms_qs:
        unit_cost  = bom.calculate_unit_cost()
        sale_price = bom.product.sale_price or Decimal('0')
        margin_eur = sale_price - unit_cost
        margin_pct = float(margin_eur / sale_price * 100) if sale_price > 0 else 0

        row = {
            'bom':        bom,
            'unit_cost':  unit_cost,
            'sale_price': sale_price,
            'margin_eur': margin_eur,
            'margin_pct': round(margin_pct, 1),
        }
        rows.append(row)

        if sale_price > 0:
            if best is None or margin_pct > best['margin_pct']:
                best = {'name': bom.product.name, 'margin_pct': round(margin_pct, 1)}
            if worst is None or margin_pct < worst['margin_pct']:
                worst = {'name': bom.product.name, 'margin_pct': round(margin_pct, 1)}

    all_pcts = [r['margin_pct'] for r in rows if r['sale_price'] > 0]
    avg_margin = round(sum(all_pcts) / len(all_pcts), 1) if all_pcts else 0

    chart_labels = json.dumps([r['bom'].product.name for r in rows])
    chart_values = json.dumps([r['margin_pct'] for r in rows])

    return render(request, 'bom/report_margin.html', {
        'rows':       rows,
        'avg_margin': avg_margin,
        'best':       best,
        'worst':      worst,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
    })


@login_required
def report_bom_cost_vs_sale(request):
    """Comparação custo de produção vs. preço de venda."""
    company = get_active_company(request)

    boms_qs = ProductBOM.objects.filter(is_active=True).select_related(
        'product', 'uom'
    ).prefetch_related('lines__component')
    if company:
        boms_qs = boms_qs.filter(Q(owner_company=company) | Q(owner_company__isnull=True))
    boms_qs = boms_qs.order_by('product__name')

    rows = []
    for bom in boms_qs:
        unit_cost  = bom.calculate_unit_cost()
        sale_price = bom.product.sale_price or Decimal('0')
        margin_eur = sale_price - unit_cost
        margin_pct = float(margin_eur / sale_price * 100) if sale_price > 0 else 0
        rows.append({
            'bom':        bom,
            'unit_cost':  unit_cost,
            'sale_price': sale_price,
            'margin_eur': margin_eur,
            'margin_pct': round(margin_pct, 1),
            'ok':         sale_price > unit_cost,
        })

    chart_labels    = json.dumps([r['bom'].product.name for r in rows])
    chart_costs     = json.dumps([float(r['unit_cost'])  for r in rows])
    chart_sales     = json.dumps([float(r['sale_price']) for r in rows])
    total_ok        = sum(1 for r in rows if r['ok'])
    total_negative  = len(rows) - total_ok

    return render(request, 'bom/report_cost_vs_sale.html', {
        'rows':           rows,
        'total_ok':       total_ok,
        'total_negative': total_negative,
        'total_boms':     len(rows),
        'chart_labels':   chart_labels,
        'chart_costs':    chart_costs,
        'chart_sales':    chart_sales,
    })


@login_required
def report_bom_materials_needed(request):
    """Lista de materiais necessários para produzir N unidades de uma receita."""
    from apps.inventory.models import Product as Prod

    company = get_active_company(request)

    boms_qs = ProductBOM.objects.filter(is_active=True).select_related('product', 'uom')
    if company:
        boms_qs = boms_qs.filter(Q(owner_company=company) | Q(owner_company__isnull=True))
    all_boms = boms_qs.order_by('product__name')

    bom_id  = request.GET.get('bom', '')
    try:
        qty_req = Decimal(str(request.GET.get('qty', '1') or '1'))
        if qty_req <= 0:
            qty_req = Decimal('1')
    except Exception:
        qty_req = Decimal('1')

    selected_bom = None
    materials    = []

    if bom_id:
        try:
            selected_bom = boms_qs.prefetch_related('lines__component', 'lines__uom').get(pk=bom_id)
        except ProductBOM.DoesNotExist:
            pass

    if selected_bom:
        multiplier = qty_req / (selected_bom.qty_produced or Decimal('1'))
        total_cost = Decimal('0')
        for line in selected_bom.lines.all():
            qty_needed = (line.quantity * multiplier).quantize(Decimal('0.0001'))
            subtotal   = qty_needed * (line.component.cost_price or Decimal('0'))
            total_cost += subtotal
            materials.append({
                'component': line.component,
                'uom':       line.uom,
                'qty_needed': qty_needed,
                'unit_cost': line.component.cost_price or Decimal('0'),
                'subtotal':  subtotal,
            })
        # Add labor pro-rata
        labor_runs   = multiplier
        labor_total  = (selected_bom.labor_cost * labor_runs).quantize(Decimal('0.01'))
        total_cost  += labor_total
    else:
        total_cost  = Decimal('0')
        labor_total = Decimal('0')

    return render(request, 'bom/report_materials_needed.html', {
        'all_boms':     all_boms,
        'selected_bom': selected_bom,
        'qty_req':      qty_req,
        'materials':    materials,
        'total_cost':   total_cost,
        'labor_total':  labor_total if selected_bom else Decimal('0'),
        'bom_id':       bom_id,
    })


@login_required
def report_bom_stock_vs_need(request):
    """Stock actual vs. necessidade para produzir N unidades."""
    from apps.inventory.models import StockQuant

    company = get_active_company(request)

    boms_qs = ProductBOM.objects.filter(is_active=True).select_related('product', 'uom')
    if company:
        boms_qs = boms_qs.filter(Q(owner_company=company) | Q(owner_company__isnull=True))
    all_boms = boms_qs.order_by('product__name')

    bom_id  = request.GET.get('bom', '')
    try:
        qty_req = Decimal(str(request.GET.get('qty', '1') or '1'))
        if qty_req <= 0:
            qty_req = Decimal('1')
    except Exception:
        qty_req = Decimal('1')

    selected_bom = None
    rows         = []

    if bom_id:
        try:
            selected_bom = boms_qs.prefetch_related('lines__component', 'lines__uom').get(pk=bom_id)
        except ProductBOM.DoesNotExist:
            pass

    if selected_bom:
        multiplier = qty_req / (selected_bom.qty_produced or Decimal('1'))
        for line in selected_bom.lines.all():
            qty_needed = (line.quantity * multiplier).quantize(Decimal('0.0001'))
            # Stock actual (soma de todos os quants do produto)
            quant_qs = StockQuant.objects.filter(product=line.component)
            if company:
                quant_qs = quant_qs.filter(
                    Q(product__owner_company=company) | Q(product__owner_company__isnull=True)
                )
            current_stock = sum(q.quantity for q in quant_qs) or Decimal('0')
            diff      = Decimal(str(current_stock)) - qty_needed
            ok        = diff >= 0
            rows.append({
                'component':     line.component,
                'uom':           line.uom,
                'qty_needed':    qty_needed,
                'current_stock': Decimal(str(current_stock)),
                'diff':          diff,
                'ok':            ok,
            })

    total_ok       = sum(1 for r in rows if r['ok'])
    total_shortage = len(rows) - total_ok

    return render(request, 'bom/report_stock_vs_need.html', {
        'all_boms':      all_boms,
        'selected_bom':  selected_bom,
        'qty_req':       qty_req,
        'rows':          rows,
        'total_ok':      total_ok,
        'total_shortage': total_shortage,
        'bom_id':        bom_id,
    })

