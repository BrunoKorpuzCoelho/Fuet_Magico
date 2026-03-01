import json
import re
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from django.contrib.contenttypes.models import ContentType
from apps.core.multi_company import filter_by_company, get_active_company
from apps.core.models import ChatterMessage, ChatterActivity, ChatterFollower

User = get_user_model()
from .forms import CategoryForm, UoMForm, UoMCategoryForm, ProductForm, WarehouseForm, StockMovementForm
from .models import Category, UoM, UoMCategory, Product, Warehouse, StockMovement, StockMovementLine, StockQuant, ProductSupplierInfo


def _weekly_placeholder_bars():
    """Generate 7-day placeholder bar data for CSS mini-charts."""
    today = timezone.now().date()
    days = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        days.append({
            'label': d.strftime('%a'),
            'count': 0,
            'pct': 6,   # min visible height
        })
    return days


@login_required
def inventory_dashboard(request):
    """Inventory dashboard with KPI overview and operation cards."""
    company = get_active_company(request)
    today = timezone.now().date()

    # ── Base querysets filtered by company ────────────────────────────────
    movements_qs = StockMovement.objects.all()
    if company:
        movements_qs = movements_qs.filter(owner_company=company)

    receipts_qs    = movements_qs.filter(movement_type='receipt')
    deliveries_qs  = movements_qs.filter(movement_type='delivery')
    adjustments_qs = movements_qs.filter(movement_type='adjustment')

    # ── Receções card ─────────────────────────────────────────────────────
    receipts_draft   = receipts_qs.filter(state='draft')
    receipts_to_proc = receipts_draft.count()
    receipts_late    = receipts_draft.filter(date__date__lt=today).count()
    receipts_waiting = receipts_draft.filter(date__date__gte=today).count()
    receipts_today   = receipts_qs.filter(state='done', date__date=today).count()

    # ── Entregas card ─────────────────────────────────────────────────────
    deliveries_draft   = deliveries_qs.filter(state='draft')
    deliveries_to_proc = deliveries_draft.count()
    deliveries_late    = deliveries_draft.filter(date__date__lt=today).count()
    deliveries_waiting = deliveries_draft.filter(date__date__gte=today).count()
    deliveries_today   = deliveries_qs.filter(state='done', date__date=today).count()

    # ── Operações Hoje card ───────────────────────────────────────────────
    ops_today_receipts     = receipts_today
    ops_today_deliveries   = deliveries_today
    ops_today_adjustments  = adjustments_qs.filter(state='done', date__date=today).count()
    ops_today_total        = ops_today_receipts + ops_today_deliveries + ops_today_adjustments

    # ── Pendentes card ────────────────────────────────────────────────────
    pending_receipts   = receipts_to_proc
    pending_deliveries = deliveries_to_proc
    pending_other      = adjustments_qs.filter(state='draft').count()
    total_pending      = pending_receipts + pending_deliveries + pending_other

    # ── Weekly bar charts (last 7 days, done movements) ───────────────────
    def _weekly_bars(qs):
        """Count done movements per day for the last 7 days."""
        days = []
        counts = []
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            n = qs.filter(state='done', date__date=d).count()
            counts.append(n)
            days.append({'label': d.strftime('%a'), 'count': n, 'date': str(d)})
        max_val = max(counts) if counts else 0
        for day in days:
            day['pct'] = max(6, int(day['count'] / max_val * 100)) if max_val else 6
        return days

    receipts_weekly    = _weekly_bars(receipts_qs)
    deliveries_weekly  = _weekly_bars(deliveries_qs)
    ops_today_weekly   = _weekly_bars(movements_qs)
    pending_weekly     = _weekly_bars(movements_qs)

    context = {
        # Receções card
        'receipts_to_process':  receipts_to_proc,
        'receipts_waiting':     receipts_waiting,
        'receipts_late':        receipts_late,
        'receipts_done_today':  receipts_today,
        'receipts_weekly':      receipts_weekly,

        # Entregas card
        'deliveries_to_process': deliveries_to_proc,
        'deliveries_waiting':    deliveries_waiting,
        'deliveries_late':       deliveries_late,
        'deliveries_done_today': deliveries_today,
        'deliveries_weekly':     deliveries_weekly,

        # Erros card (placeholder — a implementar quando houver lógica de erros)
        'errors_to_resolve':      0,
        'errors_missing_products': 0,
        'errors_documents':       0,
        'errors_resolved_today':  0,
        'errors_weekly':          _weekly_placeholder_bars(),

        # Operações Hoje card
        'ops_today':             ops_today_total,
        'ops_today_receipts':    ops_today_receipts,
        'ops_today_deliveries':  ops_today_deliveries,
        'ops_today_adjustments': ops_today_adjustments,
        'ops_today_weekly':      ops_today_weekly,

        # Pendentes card
        'total_pending':      total_pending,
        'pending_receipts':   pending_receipts,
        'pending_deliveries': pending_deliveries,
        'pending_other':      pending_other,
        'pending_weekly':     pending_weekly,
    }
    return render(request, 'inventory/inventory_dashboard.html', context)


@login_required
def category_list(request):
    """List view for product categories with search, pagination & bulk select."""
    search_query = request.GET.get('search', '')
    search_field = request.GET.get('field', 'name')
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)
    status_filter = request.GET.get('status', 'active')

    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    if status_filter == 'archived':
        qs = Category.objects.filter(is_active=False)
    else:
        qs = Category.objects.filter(is_active=True)

    qs = filter_by_company(qs, request)
    qs = qs.select_related('parent', 'owner_company').annotate(
        children_count=Count('children', distinct=True),
    )

    if search_query:
        field_mapping = {
            'name': Q(name__icontains=search_query),
            'description': Q(description__icontains=search_query),
            'parent': Q(parent__name__icontains=search_query),
        }
        if search_field in field_mapping:
            qs = qs.filter(field_mapping[search_field])

    qs = qs.order_by('name')
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
    }
    return render(request, 'inventory/category_list.html', context)


# ── Category create / edit ───────────────────────────────────────────

@login_required
def category_create(request):
    """Create a new product category."""
    company = get_active_company(request)

    if request.method == 'POST':
        form = CategoryForm(request.POST, company=company)
        if form.is_valid():
            category = form.save(commit=False)
            if not category.owner_company:
                category.owner_company = company
            category.save()
            messages.success(request, f'Categoria "{category.name}" criada com sucesso!')
            return redirect('inventory:category_edit', pk=category.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CategoryForm(company=company)

    context = {
        'form': form,
    }
    return render(request, 'inventory/category_form.html', context)


@login_required
def category_edit(request, pk):
    """Edit an existing product category."""
    category = get_object_or_404(Category, pk=pk)
    company = get_active_company(request)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category, company=company)
        if form.is_valid():
            cat = form.save(commit=False)
            if not cat.owner_company:
                cat.owner_company = company
            cat.save()
            messages.success(request, f'Categoria "{cat.name}" atualizada com sucesso!')
            return redirect('inventory:category_edit', pk=cat.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CategoryForm(instance=category, company=company)

    subcategories_count = Category.objects.filter(parent=category, is_active=True).count()

    # ── Products in this category (paginated, 50/page) ───────────
    products_qs = Product.objects.filter(
        category=category, is_active=True,
    ).select_related('uom').order_by('name')
    products_count = products_qs.count()

    page_number = request.GET.get('page', 1)
    paginator = Paginator(products_qs, 50)
    products_page = paginator.get_page(page_number)

    # Serialize page products for Alpine
    products_json = json.dumps([
        {
            'id': str(p.pk),
            'name': p.name,
            'internal_reference': p.internal_reference or '',
            'reference': p.reference or '',
            'type_label': p.get_product_type_display(),
            'sale_price': str(p.sale_price),
            'edit_url': f'/inventory/products/{p.pk}/edit/',
        }
        for p in products_page
    ])

    context = {
        'form': form,
        'category': category,
        'subcategories_count': subcategories_count,
        'products_count': products_count,
        'products_page': products_page,
        'products_json': products_json,
    }
    return render(request, 'inventory/category_form.html', context)


# ── Category products API ────────────────────────────────────────────

@login_required
def category_products_search(request, pk):
    """Search products NOT in this category to add them."""
    category = get_object_or_404(Category, pk=pk)
    q = request.GET.get('q', '').strip()
    if len(q) < 1:
        return JsonResponse({'results': []})

    results = Product.objects.filter(
        is_active=True,
    ).filter(
        Q(name__icontains=q) | Q(internal_reference__icontains=q) | Q(reference__icontains=q)
    ).exclude(
        category=category,
    ).order_by('name')[:10]

    return JsonResponse({'results': [
        {
            'id': str(p.pk),
            'name': p.name,
            'reference': p.internal_reference or p.reference or '',
        }
        for p in results
    ]})


@require_http_methods(["POST"])
@login_required
def category_products_add(request, pk):
    """Add a product to this category."""
    category = get_object_or_404(Category, pk=pk)
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        product.category = category
        product.save(update_fields=['category', 'updated_at'])
        return JsonResponse({
            'success': True,
            'product': {
                'id': str(product.pk),
                'name': product.name,
                'internal_reference': product.internal_reference or '',
                'reference': product.reference or '',
                'type_label': product.get_product_type_display(),
                'sale_price': str(product.sale_price),
                'edit_url': f'/inventory/products/{product.pk}/edit/',
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["POST"])
@login_required
def category_products_remove(request, pk, product_pk):
    """Remove a product from this category (sets category=NULL)."""
    category = get_object_or_404(Category, pk=pk)
    product = get_object_or_404(Product, pk=product_pk, category=category)
    product.category = None
    product.save(update_fields=['category', 'updated_at'])
    return JsonResponse({'success': True})


# ── Bulk actions ─────────────────────────────────────────────────────

@require_http_methods(["POST"])
@login_required
def bulk_archive_categories(request):
    """Archive selected categories (set is_active=False)."""
    try:
        data = json.loads(request.body)
        ids = data.get('category_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma categoria selecionada para arquivar'}
            }, status=400)

        categories = Category.objects.filter(id__in=ids)
        if not categories.exists():
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma categoria válida encontrada'}
            }, status=404)

        already = [c.name for c in categories if not c.is_active]
        to_archive = [c for c in categories if c.is_active]

        if already and not to_archive:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'ALREADY_ARCHIVED',
                    'message': 'As categorias selecionadas já estão arquivadas. Use a opção desarquivar se pretende restaurá-las.',
                    'categories': already,
                }
            }, status=409)

        with transaction.atomic():
            count = 0
            for cat in to_archive:
                cat.is_active = False
                cat.save(update_fields=['is_active', 'updated_at'])
                count += 1

        result = {'success': True, 'archived_count': count, 'message': f'{count} categoria(s) arquivada(s) com sucesso'}
        if already:
            result['warning'] = f'{len(already)} categoria(s) já estavam arquivadas'
        return JsonResponse(result)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_categories(request):
    """Unarchive selected categories (set is_active=True)."""
    try:
        data = json.loads(request.body)
        ids = data.get('category_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma categoria selecionada para desarquivar'}
            }, status=400)

        categories = Category.objects.filter(id__in=ids)
        if not categories.exists():
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma categoria válida encontrada'}
            }, status=404)

        already_active = [c.name for c in categories if c.is_active]
        to_unarchive = [c for c in categories if not c.is_active]

        if already_active and not to_unarchive:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'ALREADY_ACTIVE',
                    'message': 'As categorias selecionadas já estão ativas.',
                    'categories': already_active,
                }
            }, status=409)

        with transaction.atomic():
            count = 0
            for cat in to_unarchive:
                cat.is_active = True
                cat.save(update_fields=['is_active', 'updated_at'])
                count += 1

        result = {'success': True, 'unarchived_count': count, 'message': f'{count} categoria(s) desarquivada(s) com sucesso'}
        if already_active:
            result['warning'] = f'{len(already_active)} categoria(s) já estavam ativas'
        return JsonResponse(result)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_delete_categories(request):
    """Permanently delete selected categories."""
    try:
        data = json.loads(request.body)
        ids = data.get('category_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma categoria selecionada'}
            }, status=400)

        categories = Category.objects.filter(id__in=ids)
        count = categories.count()

        if count == 0:
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Categorias não encontradas'}
            }, status=404)

        # Check for children that will also be deleted (CASCADE)
        children_count = Category.objects.filter(parent__in=categories).exclude(id__in=ids).count()

        with transaction.atomic():
            categories.delete()

        msg = f'{count} categoria(s) eliminada(s) permanentemente'
        if children_count:
            msg += f' (+ {children_count} subcategoria(s) associadas)'

        return JsonResponse({'success': True, 'deleted_count': count, 'message': msg})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


# ── UoM list ─────────────────────────────────────────────────────────

@login_required
def uom_list(request):
    """List view for units of measure with search, pagination & bulk select."""
    search_query = request.GET.get('search', '')
    search_field = request.GET.get('field', 'name')
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)
    status_filter = request.GET.get('status', 'active')

    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    if status_filter == 'archived':
        qs = UoM.objects.filter(is_active=False)
    else:
        qs = UoM.objects.filter(is_active=True)

    qs = filter_by_company(qs, request)
    qs = qs.select_related('category', 'owner_company')

    if search_query:
        field_mapping = {
            'name': Q(name__icontains=search_query),
            'symbol': Q(symbol__icontains=search_query),
            'category': Q(category__name__icontains=search_query),
        }
        if search_field in field_mapping:
            qs = qs.filter(field_mapping[search_field])

    qs = qs.order_by('category__name', 'uom_type', 'name')
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page_number)

    context = {
        'uoms': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
    }
    return render(request, 'inventory/uom_list.html', context)


# ── UoM create / edit ────────────────────────────────────────────────

@login_required
def uom_create(request):
    """Create a new unit of measure."""
    company = get_active_company(request)

    if request.method == 'POST':
        form = UoMForm(request.POST, company=company)
        if form.is_valid():
            uom = form.save(commit=False)
            if not uom.owner_company:
                uom.owner_company = company
            uom.save()
            messages.success(request, f'Unidade "{uom.name}" criada com sucesso!')
            return redirect('inventory:uom_edit', pk=uom.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UoMForm(company=company)

    context = {
        'form': form,
    }
    return render(request, 'inventory/uom_form.html', context)


@login_required
def uom_edit(request, pk):
    """Edit an existing unit of measure."""
    uom = get_object_or_404(UoM, pk=pk)
    company = get_active_company(request)

    if request.method == 'POST':
        form = UoMForm(request.POST, instance=uom, company=company)
        if form.is_valid():
            u = form.save(commit=False)
            if not u.owner_company:
                u.owner_company = company
            u.save()
            messages.success(request, f'Unidade "{u.name}" atualizada com sucesso!')
            return redirect('inventory:uom_edit', pk=u.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UoMForm(instance=uom, company=company)

    context = {
        'form': form,
        'uom': uom,
    }
    return render(request, 'inventory/uom_form.html', context)


# ── UoM bulk actions ─────────────────────────────────────────────────

@require_http_methods(["POST"])
@login_required
def bulk_archive_uoms(request):
    """Archive selected UoMs (set is_active=False)."""
    try:
        data = json.loads(request.body)
        ids = data.get('uom_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma unidade selecionada para arquivar'}
            }, status=400)

        uoms = UoM.objects.filter(id__in=ids)
        if not uoms.exists():
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma unidade válida encontrada'}
            }, status=404)

        already = [u.name for u in uoms if not u.is_active]
        to_archive = [u for u in uoms if u.is_active]

        if already and not to_archive:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'ALREADY_ARCHIVED',
                    'message': 'As unidades selecionadas já estão arquivadas. Use a opção desarquivar se pretende restaurá-las.',
                    'uoms': already,
                }
            }, status=409)

        with transaction.atomic():
            count = 0
            for uom in to_archive:
                uom.is_active = False
                uom.save(update_fields=['is_active', 'updated_at'])
                count += 1

        result = {'success': True, 'archived_count': count, 'message': f'{count} unidade(s) arquivada(s) com sucesso'}
        if already:
            result['warning'] = f'{len(already)} unidade(s) já estavam arquivadas'
        return JsonResponse(result)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_uoms(request):
    """Unarchive selected UoMs (set is_active=True)."""
    try:
        data = json.loads(request.body)
        ids = data.get('uom_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma unidade selecionada para desarquivar'}
            }, status=400)

        uoms = UoM.objects.filter(id__in=ids)
        if not uoms.exists():
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma unidade válida encontrada'}
            }, status=404)

        already_active = [u.name for u in uoms if u.is_active]
        to_unarchive = [u for u in uoms if not u.is_active]

        if already_active and not to_unarchive:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'ALREADY_ACTIVE',
                    'message': 'As unidades selecionadas já estão ativas.',
                    'uoms': already_active,
                }
            }, status=409)

        with transaction.atomic():
            count = 0
            for uom in to_unarchive:
                uom.is_active = True
                uom.save(update_fields=['is_active', 'updated_at'])
                count += 1

        result = {'success': True, 'unarchived_count': count, 'message': f'{count} unidade(s) desarquivada(s) com sucesso'}
        if already_active:
            result['warning'] = f'{len(already_active)} unidade(s) já estavam ativas'
        return JsonResponse(result)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_delete_uoms(request):
    """Permanently delete selected UoMs."""
    try:
        data = json.loads(request.body)
        ids = data.get('uom_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma unidade selecionada'}
            }, status=400)

        uoms = UoM.objects.filter(id__in=ids)
        count = uoms.count()

        if count == 0:
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Unidades não encontradas'}
            }, status=404)

        with transaction.atomic():
            uoms.delete()

        msg = f'{count} unidade(s) eliminada(s) permanentemente'
        return JsonResponse({'success': True, 'deleted_count': count, 'message': msg})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


# ── UoM Category list ────────────────────────────────────────────────

@login_required
def uom_category_list(request):
    """List view for UoM categories with search, pagination & bulk select."""
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)
    status_filter = request.GET.get('status', 'active')

    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    if status_filter == 'archived':
        qs = UoMCategory.objects.filter(is_active=False)
    else:
        qs = UoMCategory.objects.filter(is_active=True)

    qs = filter_by_company(qs, request)
    qs = qs.select_related('owner_company').annotate(
        uom_count=Count('uoms', distinct=True),
    )

    if search_query:
        qs = qs.filter(name__icontains=search_query)

    qs = qs.order_by('name')
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': page_obj,
        'search_query': search_query,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
    }
    return render(request, 'inventory/uom_category_list.html', context)


# ── UoM Category create / edit ───────────────────────────────────────

@login_required
def uom_category_create(request):
    """Create a new UoM category."""
    company = get_active_company(request)

    if request.method == 'POST':
        form = UoMCategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            if not cat.owner_company:
                cat.owner_company = company
            cat.save()
            messages.success(request, f'Categoria "{cat.name}" criada com sucesso!')
            return redirect('inventory:uom_category_edit', pk=cat.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UoMCategoryForm()

    context = {'form': form}
    return render(request, 'inventory/uom_category_form.html', context)


@login_required
def uom_category_edit(request, pk):
    """Edit an existing UoM category."""
    cat = get_object_or_404(UoMCategory, pk=pk)
    company = get_active_company(request)

    if request.method == 'POST':
        form = UoMCategoryForm(request.POST, instance=cat)
        if form.is_valid():
            c = form.save(commit=False)
            if not c.owner_company:
                c.owner_company = company
            c.save()
            messages.success(request, f'Categoria "{c.name}" atualizada com sucesso!')
            return redirect('inventory:uom_category_edit', pk=c.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UoMCategoryForm(instance=cat)

    uoms = UoM.objects.filter(category=cat).order_by('-is_active', 'name')
    uom_count = uoms.filter(is_active=True).count()

    context = {
        'form': form,
        'category': cat,
        'uoms': uoms,
        'uom_count': uom_count,
    }
    return render(request, 'inventory/uom_category_form.html', context)


# ── UoM Category bulk actions ────────────────────────────────────────

@require_http_methods(["POST"])
@login_required
def bulk_archive_uom_categories(request):
    """Archive selected UoM categories."""
    try:
        data = json.loads(request.body)
        ids = data.get('category_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma categoria selecionada para arquivar'}
            }, status=400)

        cats = UoMCategory.objects.filter(id__in=ids)
        if not cats.exists():
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma categoria válida encontrada'}
            }, status=404)

        already = [c.name for c in cats if not c.is_active]
        to_archive = [c for c in cats if c.is_active]

        if already and not to_archive:
            return JsonResponse({
                'success': False,
                'error': {'code': 'ALREADY_ARCHIVED', 'message': 'As categorias selecionadas já estão arquivadas.'}
            }, status=409)

        with transaction.atomic():
            count = 0
            for c in to_archive:
                c.is_active = False
                c.save(update_fields=['is_active', 'updated_at'])
                count += 1

        result = {'success': True, 'archived_count': count, 'message': f'{count} categoria(s) arquivada(s) com sucesso'}
        if already:
            result['warning'] = f'{len(already)} categoria(s) já estavam arquivadas'
        return JsonResponse(result)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_uom_categories(request):
    """Unarchive selected UoM categories."""
    try:
        data = json.loads(request.body)
        ids = data.get('category_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma categoria selecionada para desarquivar'}
            }, status=400)

        cats = UoMCategory.objects.filter(id__in=ids)
        if not cats.exists():
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma categoria válida encontrada'}
            }, status=404)

        already_active = [c.name for c in cats if c.is_active]
        to_unarchive = [c for c in cats if not c.is_active]

        if already_active and not to_unarchive:
            return JsonResponse({
                'success': False,
                'error': {'code': 'ALREADY_ACTIVE', 'message': 'As categorias selecionadas já estão ativas.'}
            }, status=409)

        with transaction.atomic():
            count = 0
            for c in to_unarchive:
                c.is_active = True
                c.save(update_fields=['is_active', 'updated_at'])
                count += 1

        result = {'success': True, 'unarchived_count': count, 'message': f'{count} categoria(s) desarquivada(s) com sucesso'}
        if already_active:
            result['warning'] = f'{len(already_active)} categoria(s) já estavam ativas'
        return JsonResponse(result)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_delete_uom_categories(request):
    """Permanently delete selected UoM categories."""
    try:
        data = json.loads(request.body)
        ids = data.get('category_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma categoria selecionada'}
            }, status=400)

        cats = UoMCategory.objects.filter(id__in=ids)
        count = cats.count()

        if count == 0:
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Categorias não encontradas'}
            }, status=404)

        # Count UoMs that will also be deleted (CASCADE)
        uom_count = UoM.objects.filter(category__in=cats).exclude(category__id__in=[]).count()

        with transaction.atomic():
            cats.delete()

        msg = f'{count} categoria(s) eliminada(s) permanentemente'
        if uom_count:
            msg += f' (+ {uom_count} unidade(s) associadas)'

        return JsonResponse({'success': True, 'deleted_count': count, 'message': msg})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


# ═══════════════════════════════════════════════════════════════════════
# PRODUCTS
# ═══════════════════════════════════════════════════════════════════════

@login_required
def product_list(request):
    """List view for products with search, pagination & bulk select."""
    from django.db.models import OuterRef, Subquery, DecimalField, F, Value
    from django.db.models.functions import Coalesce

    search_query = request.GET.get('search', '')
    search_field = request.GET.get('field', 'name')
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)
    status_filter = request.GET.get('status', 'active')
    stock_filter = request.GET.get('stock_filter', '')

    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    if status_filter == 'archived':
        qs = Product.objects.filter(is_active=False)
    else:
        qs = Product.objects.filter(is_active=True)

    qs = filter_by_company(qs, request)
    qs = qs.select_related('category', 'uom', 'supplier', 'owner_company')

    if search_query:
        field_mapping = {
            'name': Q(name__icontains=search_query),
            'reference': Q(internal_reference__icontains=search_query) | Q(reference__icontains=search_query),
            'barcode': Q(barcode__icontains=search_query),
            'category': Q(category__name__icontains=search_query),
            'supplier': Q(supplier__name__icontains=search_query),
        }
        if search_field in field_mapping:
            qs = qs.filter(field_mapping[search_field])
        else:
            qs = qs.filter(Q(name__icontains=search_query))

    # Annotate each product with its current on-hand quantity (sum of StockQuant)
    _dec = DecimalField(max_digits=14, decimal_places=4)
    on_hand_sq = (
        StockQuant.objects
        .filter(product_id=OuterRef('pk'))
        .values('product_id')
        .annotate(t=Sum('quantity'))
        .values('t')[:1]
    )
    qs = qs.annotate(
        on_hand_ann=Coalesce(Subquery(on_hand_sq, output_field=_dec), Value(0, output_field=_dec))
    )

    if stock_filter == 'below_min':
        qs = qs.filter(min_stock__gt=0, on_hand_ann__lt=F('min_stock'))

    qs = qs.order_by('name')
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page_number)

    # Set of PKs on the current page that are below min stock (for row highlight)
    below_min_pks = {
        p.pk for p in page_obj
        if p.min_stock and p.min_stock > 0 and p.on_hand_ann < p.min_stock
    }

    context = {
        'products': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
        'stock_filter': stock_filter,
        'below_min_pks': below_min_pks,
    }
    return render(request, 'inventory/product_list.html', context)


# ── Product create / edit ─────────────────────────────────────────────

@login_required
def product_create(request):
    """Create a new product."""
    company   = get_active_company(request)
    return_to = request.GET.get('return_to') or request.POST.get('return_to', '')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, company=company)
        if form.is_valid():
            product = form.save(commit=False)
            if not product.owner_company:
                product.owner_company = company
            product.save()
            messages.success(request, f'Produto "{product.name}" criado com sucesso!')
            if return_to:
                return redirect('inventory:movement_edit', pk=return_to)
            return redirect('inventory:product_edit', pk=product.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm(company=company)

    context = {'form': form, 'return_to': return_to}
    return render(request, 'inventory/product_form.html', context)


@login_required
def product_edit(request, pk):
    """Edit an existing product."""
    product   = get_object_or_404(Product, pk=pk)
    company   = get_active_company(request)
    return_to = request.GET.get('return_to') or request.POST.get('return_to', '')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, company=company)
        if form.is_valid():
            p = form.save(commit=False)
            if not p.owner_company:
                p.owner_company = company
            p.save()
            messages.success(request, f'Produto "{p.name}" atualizado com sucesso!')
            if return_to:
                return redirect('inventory:movement_edit', pk=return_to)
            return redirect('inventory:product_edit', pk=p.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm(instance=product, company=company)

    # Smart button counts
    bom_count = 0        # Bill of Materials
    sold_count = 0       # Unidades vendidas
    on_hand_count = (
        StockQuant.objects
        .filter(product=product)
        .aggregate(total=Sum('quantity'))['total']
        or 0
    )
    incoming_pending = (
        StockMovementLine.objects
        .filter(product=product, stock_movement__movement_type='receipt', stock_movement__state='draft')
        .aggregate(total=Sum('quantity'))['total'] or 0
    )
    outgoing_pending = (
        StockMovementLine.objects
        .filter(product=product, stock_movement__movement_type='delivery', stock_movement__state='draft')
        .aggregate(total=Sum('quantity'))['total'] or 0
    )
    forecast_count = float(on_hand_count) + float(incoming_pending) - float(outgoing_pending)

    stock_value = float(on_hand_count) * float(product.cost_price)
    profit_margin_pct = product.get_profit_margin_pct()
    markup_pct = (
        round(float((product.sale_price - product.cost_price) / product.cost_price * 100), 1)
        if product.cost_price else None
    )

    context = {
        'form': form,
        'product': product,
        'bom_count': bom_count,
        'forecast_count': forecast_count,
        'sold_count': sold_count,
        'on_hand_count': on_hand_count,
        'incoming_pending': incoming_pending,
        'outgoing_pending': outgoing_pending,
        'stock_value': stock_value,
        'profit_margin_pct': profit_margin_pct,
        'markup_pct': markup_pct,
        'return_to': return_to,
        'supplier_infos_json': json.dumps([
            {
                'id': str(si.pk),
                'supplier_id': str(si.supplier_id),
                'supplier_name': si.supplier.name,
                'sequence': si.sequence,
                'supplier_product_code': si.supplier_product_code or '',
                'price': float(si.price),
                'min_quantity': float(si.min_quantity),
                'lead_time': si.lead_time,
                'is_preferred': si.is_preferred,
            }
            for si in ProductSupplierInfo.objects.filter(product=product, is_active=True)
            .select_related('supplier')
            .order_by('sequence', '-is_preferred')
        ]),
    }
    return render(request, 'inventory/product_form.html', context)


@login_required
def product_forecast(request, pk):
    """Forecast view for a product: historical stock + pending movements projected forward."""
    import json as _json
    from decimal import Decimal
    from datetime import timedelta
    from django.utils import timezone as tz
    from django.core.serializers.json import DjangoJSONEncoder

    product = get_object_or_404(Product, pk=pk)

    # ── Current on-hand ──────────────────────────────────────────────
    on_hand = float(
        StockQuant.objects.filter(product=product)
        .aggregate(total=Sum('quantity'))['total'] or 0
    )

    # ── Pending incoming / outgoing ──────────────────────────────────
    incoming = float(
        StockMovementLine.objects
        .filter(product=product, stock_movement__movement_type='receipt', stock_movement__state='draft')
        .aggregate(total=Sum('quantity'))['total'] or 0
    )
    outgoing = float(
        StockMovementLine.objects
        .filter(product=product, stock_movement__movement_type='delivery', stock_movement__state='draft')
        .aggregate(total=Sum('quantity'))['total'] or 0
    )
    forecast_qty = on_hand + incoming - outgoing

    now = tz.now()

    # ── Historical timeline (last 20 validated movements) ────────────
    done_lines = list(
        StockMovementLine.objects
        .filter(product=product, stock_movement__state='done')
        .select_related('stock_movement', 'stock_movement__partner')
        .order_by('-stock_movement__date')[:20]
    )
    # Reconstruct backwards from current on_hand
    running = on_hand
    history_events = []
    for line in done_lines:
        mv = line.stock_movement
        qty = float(line.quantity)
        # This point is BEFORE the movement was applied → reverse it
        if mv.movement_type == 'receipt':
            running -= qty
        elif mv.movement_type == 'delivery':
            running += qty
        history_events.append({
            'date': mv.date.strftime('%Y-%m-%dT%H:%M:%S'),
            'label': mv.date.strftime('%d/%m/%Y'),
            'balance': round(running, 3),
            'document': mv.reference,
            'pk': str(mv.pk),
            'movement_type': mv.movement_type,
            'type_label': mv.get_movement_type_display(),
            'partner': str(mv.partner) if mv.partner else '—',
            'quantity': qty,
            'delta': -qty if mv.movement_type == 'receipt' else qty,  # sign when going backwards
        })
    history_events.reverse()  # chronological

    # ── Future timeline (draft movements sorted by planned date) ─────
    pending_lines = list(
        StockMovementLine.objects
        .filter(product=product, stock_movement__state='draft')
        .select_related('stock_movement', 'stock_movement__partner')
        .order_by('stock_movement__date')
    )
    running_f = on_hand
    future_events = []
    for line in pending_lines:
        mv = line.stock_movement
        qty = float(line.quantity)
        delta = qty if mv.movement_type == 'receipt' else -qty
        running_f += delta
        future_events.append({
            'date': mv.date.strftime('%Y-%m-%dT%H:%M:%S'),
            'label': mv.date.strftime('%d/%m/%Y'),
            'balance': round(running_f, 3),
            'document': mv.reference,
            'pk': str(mv.pk),
            'movement_type': mv.movement_type,
            'type_label': mv.get_movement_type_display(),
            'partner': str(mv.partner) if mv.partner else '—',
            'quantity': qty,
            'delta': delta,
        })

    # ── Chart data ───────────────────────────────────────────────────
    today_label = now.strftime('%d/%m/%Y')

    # Historical line: history_events + today point.
    # If there's no history, add a synthetic "start" point 30 days ago so the
    # line is visible (Chart.js needs at least 2 points to draw a line).
    if history_events:
        chart_hist_labels = [e['label'] for e in history_events] + [today_label]
        chart_hist_values = [round(e['balance'], 3) for e in history_events] + [round(on_hand, 3)]
    else:
        past_label = (now - timedelta(days=30)).strftime('%d/%m/%Y')
        chart_hist_labels = [past_label, today_label]
        chart_hist_values = [round(on_hand, 3), round(on_hand, 3)]

    # Forecast line: today point + future events
    chart_fore_values = [round(on_hand, 3)] + [round(e['balance'], 3) for e in future_events]

    # Merged label set (history labels + future-only labels)
    future_labels_only = [e['label'] for e in future_events]
    all_labels = chart_hist_labels + future_labels_only

    # Pad both datasets to the same length for Chart.js
    hist_data = chart_hist_values + [None] * len(future_labels_only)
    fore_data = [None] * (len(chart_hist_labels) - 1) + chart_fore_values

    def jdumps(v):
        return _json.dumps(v, cls=DjangoJSONEncoder)

    context = {
        'product': product,
        'on_hand': on_hand,
        'incoming': incoming,
        'outgoing': outgoing,
        'forecast_qty': forecast_qty,
        'history_events': history_events,
        'future_events': future_events,
        # JSON for Chart.js — all serialised with DjangoJSONEncoder (handles Decimal)
        'chart_labels_json':  jdumps(all_labels),
        'chart_hist_json':    jdumps(hist_data),
        'chart_fore_json':    jdumps(fore_data),
        'on_hand_line_json':  jdumps([round(on_hand, 3)] * len(all_labels)),
        'on_hand_json':       jdumps(round(on_hand, 3)),
        'uom_name': product.uom.name if product.uom else '',
    }
    return render(request, 'inventory/product_forecast.html', context)


# ── Product bulk actions ──────────────────────────────────────────────

@require_http_methods(["POST"])
@login_required
def bulk_archive_products(request):
    """Archive selected products."""
    try:
        data = json.loads(request.body)
        ids = data.get('product_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum produto selecionado para arquivar'}
            }, status=400)

        products = Product.objects.filter(id__in=ids)
        if not products.exists():
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Produtos não encontrados'}
            }, status=404)

        count = products.update(is_active=False)
        return JsonResponse({'success': True, 'archived_count': count, 'message': f'{count} produto(s) arquivado(s) com sucesso'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_products(request):
    """Unarchive selected products."""
    try:
        data = json.loads(request.body)
        ids = data.get('product_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum produto selecionado para desarquivar'}
            }, status=400)

        products = Product.objects.filter(id__in=ids)
        if not products.exists():
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Produtos não encontrados'}
            }, status=404)

        count = products.update(is_active=True)
        return JsonResponse({'success': True, 'unarchived_count': count, 'message': f'{count} produto(s) desarquivado(s) com sucesso'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_delete_products(request):
    """Permanently delete selected products."""
    try:
        data = json.loads(request.body)
        ids = data.get('product_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum produto selecionado para eliminar'}
            }, status=400)

        products = Product.objects.filter(id__in=ids)
        count = products.count()

        if count == 0:
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Produtos não encontrados'}
            }, status=404)

        with transaction.atomic():
            products.delete()

        return JsonResponse({'success': True, 'deleted_count': count, 'message': f'{count} produto(s) eliminado(s) permanentemente'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


# ══════════════════════════════════════════════════════════════════════
#  WAREHOUSE
# ══════════════════════════════════════════════════════════════════════

# ── Warehouse list ────────────────────────────────────────────────────

@login_required
def warehouse_list(request):
    """List view for warehouses with search, pagination & bulk select."""
    search_query = request.GET.get('search', '')
    search_field = request.GET.get('field', 'name')
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)
    status_filter = request.GET.get('status', 'active')

    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    if status_filter == 'archived':
        qs = Warehouse.objects.filter(is_active=False)
    else:
        qs = Warehouse.objects.filter(is_active=True)

    qs = filter_by_company(qs, request)
    qs = qs.select_related('owner_company')

    if search_query:
        field_mapping = {
            'name': Q(name__icontains=search_query),
            'code': Q(code__icontains=search_query),
            'address': Q(address__icontains=search_query),
            'company': Q(owner_company__name__icontains=search_query),
        }
        if search_field in field_mapping:
            qs = qs.filter(field_mapping[search_field])
        else:
            qs = qs.filter(Q(name__icontains=search_query))

    qs = qs.order_by('-is_default', 'name')
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page_number)

    context = {
        'warehouses': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
    }
    return render(request, 'inventory/warehouse_list.html', context)


# ── Warehouse create / edit ───────────────────────────────────────────

@login_required
def warehouse_create(request):
    """Create a new warehouse."""
    company = get_active_company(request)

    if request.method == 'POST':
        form = WarehouseForm(request.POST, company=company)
        if form.is_valid():
            warehouse = form.save(commit=False)
            if not warehouse.owner_company:
                warehouse.owner_company = company
            warehouse.save()
            messages.success(request, f'Armazém "{warehouse.name}" criado com sucesso!')
            return redirect('inventory:warehouse_edit', pk=warehouse.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = WarehouseForm(company=company)

    context = {'form': form}
    return render(request, 'inventory/warehouse_form.html', context)


@login_required
def warehouse_edit(request, pk):
    """Edit an existing warehouse."""
    warehouse = get_object_or_404(Warehouse, pk=pk)
    company = get_active_company(request)

    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse, company=company)
        if form.is_valid():
            w = form.save(commit=False)
            if not w.owner_company:
                w.owner_company = company
            w.save()
            messages.success(request, f'Armazém "{w.name}" atualizado com sucesso!')
            return redirect('inventory:warehouse_edit', pk=w.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = WarehouseForm(instance=warehouse, company=company)

    context = {
        'form': form,
        'warehouse': warehouse,
    }
    return render(request, 'inventory/warehouse_form.html', context)


# ── Warehouse bulk actions ────────────────────────────────────────────

@require_http_methods(["POST"])
@login_required
def bulk_archive_warehouses(request):
    """Archive selected warehouses."""
    try:
        data = json.loads(request.body)
        ids = data.get('warehouse_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum armazém selecionado para arquivar'}
            }, status=400)

        warehouses = Warehouse.objects.filter(id__in=ids)
        if not warehouses.exists():
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Armazéns não encontrados'}
            }, status=404)

        count = warehouses.update(is_active=False)
        return JsonResponse({'success': True, 'archived_count': count, 'message': f'{count} armazém(ns) arquivado(s) com sucesso'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_warehouses(request):
    """Unarchive selected warehouses."""
    try:
        data = json.loads(request.body)
        ids = data.get('warehouse_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum armazém selecionado para desarquivar'}
            }, status=400)

        warehouses = Warehouse.objects.filter(id__in=ids)
        if not warehouses.exists():
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Armazéns não encontrados'}
            }, status=404)

        count = warehouses.update(is_active=True)
        return JsonResponse({'success': True, 'unarchived_count': count, 'message': f'{count} armazém(ns) desarquivado(s) com sucesso'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_delete_warehouses(request):
    """Permanently delete selected warehouses."""
    try:
        data = json.loads(request.body)
        ids = data.get('warehouse_ids', [])

        if not ids:
            return JsonResponse({
                'success': False,
                'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum armazém selecionado para eliminar'}
            }, status=400)

        warehouses = Warehouse.objects.filter(id__in=ids)
        count = warehouses.count()

        if count == 0:
            return JsonResponse({
                'success': False,
                'error': {'code': 'NOT_FOUND', 'message': 'Armazéns não encontrados'}
            }, status=404)

        with transaction.atomic():
            warehouses.delete()

        return JsonResponse({'success': True, 'deleted_count': count, 'message': f'{count} armazém(ns) eliminado(s) permanentemente'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


# ─────────────────────────────────────────────────────────────────────
# Operations — Receipts & Deliveries
# ─────────────────────────────────────────────────────────────────────

_MOVEMENT_TYPE_META = {
    'receipt': {
        'label': 'Receções',
        'label_singular': 'Receção',
        'list_url_name': 'inventory:receipt_list',
        'create_url_name': 'inventory:receipt_create',
    },
    'delivery': {
        'label': 'Entregas',
        'label_singular': 'Entrega',
        'list_url_name': 'inventory:delivery_list',
        'create_url_name': 'inventory:delivery_create',
    },
    'adjustment': {
        'label': 'Ajustes',
        'label_singular': 'Ajuste',
        'list_url_name': 'inventory:adjustment_list',
        'create_url_name': 'inventory:adjustment_create',
    },
}


@login_required
def movement_list(request, movement_type):
    """List view for stock movements (receipt or delivery).

    Searchable by: reference, partner (name), origin.
    Filterable by state: all / draft / done / cancelled / archived.
    Paginated at 50 per page.
    """
    if movement_type not in _MOVEMENT_TYPE_META:
        from django.http import Http404
        raise Http404

    meta = _MOVEMENT_TYPE_META[movement_type]
    search_query = request.GET.get('search', '')
    search_field = request.GET.get('field', 'reference')
    page_number  = request.GET.get('page', 1)
    state_filter = request.GET.get('state', 'all')

    try:
        page_size = int(request.GET.get('page_size', 50))
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    # ── Base queryset ─────────────────────────────────────────────
    if state_filter == 'archived':
        qs = StockMovement.objects.filter(movement_type=movement_type, is_active=False)
    elif state_filter in ('draft', 'done', 'cancelled'):
        qs = StockMovement.objects.filter(movement_type=movement_type, is_active=True, state=state_filter)
    else:
        qs = StockMovement.objects.filter(movement_type=movement_type, is_active=True)

    qs = filter_by_company(qs, request)
    qs = qs.select_related('partner', 'warehouse', 'responsible', 'owner_company')

    # ── Search ────────────────────────────────────────────────────
    if search_query:
        field_mapping = {
            'reference': Q(reference__icontains=search_query),
            'partner':   Q(partner__name__icontains=search_query),
            'origin':    Q(origin__icontains=search_query),
        }
        qs = qs.filter(field_mapping.get(search_field, Q(reference__icontains=search_query)))

    qs = qs.order_by('-date', '-created_at')
    paginator = Paginator(qs, page_size)
    page_obj  = paginator.get_page(page_number)

    from django.urls import reverse
    context = {
        'movements':      page_obj,
        'movement_type':  movement_type,
        'type_label':     meta['label'],
        'type_label_singular': meta['label_singular'],
        'list_url':       reverse(meta['list_url_name']),
        'create_url':     reverse(meta['create_url_name']),
        'search_query':   search_query,
        'search_field':   search_field,
        'state_filter':   state_filter,
        'total_count':    paginator.count,
        'page_size':      page_size,
        'states': [
            ('all',       'Todos'),
            ('draft',     'Rascunho'),
            ('done',      'Validado'),
            ('cancelled', 'Cancelado'),
            ('archived',  'Arquivados'),
        ],
    }
    return render(request, 'inventory/movement_list.html', context)


# ── Operations bulk actions ───────────────────────────────────────────

@require_http_methods(["POST"])
@login_required
def bulk_archive_movements(request):
    """Archive selected movements. Errors if all are already archived."""
    try:
        data = json.loads(request.body)
        ids  = data.get('movement_ids', [])

        if not ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum movimento selecionado.'}}, status=400)

        qs = StockMovement.objects.filter(id__in=ids)
        if not qs.exists():
            return JsonResponse({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Movimentos não encontrados.'}}, status=404)

        already_archived = qs.filter(is_active=False).count()
        if already_archived == qs.count():
            return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ARCHIVED', 'message': 'Os movimentos selecionados já estão arquivados.'}}, status=400)

        count = qs.filter(is_active=True).update(is_active=False)
        return JsonResponse({'success': True, 'archived_count': count, 'message': f'{count} movimento(s) arquivado(s) com sucesso.'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido.'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado.'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_movements(request):
    """Unarchive selected movements. Errors if all are already active."""
    try:
        data = json.loads(request.body)
        ids  = data.get('movement_ids', [])

        if not ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum movimento selecionado.'}}, status=400)

        qs = StockMovement.objects.filter(id__in=ids)
        if not qs.exists():
            return JsonResponse({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Movimentos não encontrados.'}}, status=404)

        already_active = qs.filter(is_active=True).count()
        if already_active == qs.count():
            return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ACTIVE', 'message': 'Os movimentos selecionados já estão ativos (não arquivados).'}}, status=400)

        count = qs.filter(is_active=False).update(is_active=True)
        return JsonResponse({'success': True, 'unarchived_count': count, 'message': f'{count} movimento(s) desarquivado(s) com sucesso.'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido.'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado.'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_delete_movements(request):
    """Permanently delete movements. Only draft or cancelled state is allowed."""
    try:
        data = json.loads(request.body)
        ids  = data.get('movement_ids', [])

        if not ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum movimento selecionado.'}}, status=400)

        qs = StockMovement.objects.filter(id__in=ids)
        if not qs.exists():
            return JsonResponse({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Movimentos não encontrados.'}}, status=404)

        blocked = qs.filter(state='done').count()
        if blocked > 0:
            return JsonResponse({'success': False, 'error': {
                'code': 'CANNOT_DELETE_DONE',
                'message': f'{blocked} movimento(s) não podem ser eliminados porque estão no estado "Validado". Cancele-os primeiro.'
            }}, status=400)

        count = qs.count()
        with transaction.atomic():
            qs.delete()

        return JsonResponse({'success': True, 'deleted_count': count, 'message': f'{count} movimento(s) eliminado(s) permanentemente.'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido.'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado.'}}, status=500)


# ── Product search (AJAX) ─────────────────────────────────────────────

@login_required
def product_search(request):
    """Return up to 7 products matching ?q=... as JSON.

    Used by the stock movement form lines dropdown.
    Returns cost_price for receipts and sale_price for deliveries via
    the ?movement_type= param so the front-end can pre-fill unit_price.
    """
    q             = request.GET.get('q', '').strip()
    movement_type = request.GET.get('movement_type', 'receipt')
    company       = get_active_company(request)

    if not q:
        return JsonResponse({'results': []})

    qs = filter_by_company(
        Product.objects.filter(is_active=True).select_related('uom', 'uom_purchase'),
        request,
    ).filter(
        Q(name__icontains=q)
        | Q(internal_reference__icontains=q)
        | Q(reference__icontains=q)
    )[:7]

    results = []
    for p in qs:
        price = float(p.cost_price) if movement_type == 'receipt' else float(p.sale_price)
        # For receipts, suggest the purchase UoM (if defined); otherwise fall back to base UoM
        if movement_type == 'receipt' and p.uom_purchase_id:
            line_uom_id     = str(p.uom_purchase.pk)
            line_uom_symbol = p.uom_purchase.symbol
        else:
            line_uom_id     = str(p.uom.pk) if p.uom else None
            line_uom_symbol = p.uom.symbol if p.uom else ''
        results.append({
            'id':                   str(p.pk),
            'name':                 p.name,
            'internal_reference':   p.internal_reference or '',
            'cost_price':           float(p.cost_price),
            'sale_price':           float(p.sale_price),
            'default_price':        price,
            'uom_id':               str(p.uom.pk) if p.uom else None,
            'uom_name':             p.uom.name if p.uom else '',
            'uom_symbol':           p.uom.symbol if p.uom else '',
            'uom_purchase_id':      str(p.uom_purchase.pk) if p.uom_purchase else None,
            'uom_purchase_symbol':  p.uom_purchase.symbol if p.uom_purchase else '',
            'line_uom_id':          line_uom_id,
            'line_uom_symbol':      line_uom_symbol,
            'tax_rate':             float(p.tax_rate),
        })
    return JsonResponse({'results': results})


# ── Movement create / edit ─────────────────────────────────────────────

@login_required
def movement_create(request, movement_type):
    """Create a new StockMovement (receipt or delivery).

    GET  → blank form with movement_type pre-selected.
    POST → saves the header draft, then redirects to movement_edit.
    """
    if movement_type not in ('receipt', 'delivery', 'adjustment'):
        from django.http import Http404
        raise Http404

    company  = get_active_company(request)
    meta     = _MOVEMENT_TYPE_META[movement_type]

    if request.method == 'POST':
        form = StockMovementForm(request.POST, company=company)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.movement_type = movement_type
            movement.owner_company = company
            movement.responsible   = request.user
            movement.save()
            # Log CREATE
            ChatterActivity.objects.create(
                content_object=movement,
                user=request.user,
                activity_type='CREATE',
                description=f'criou o movimento {movement.reference}',
            )
            messages.success(request, f'{meta["label_singular"]} criada com sucesso.')
            return redirect('inventory:movement_edit', pk=movement.pk)
        # If invalid, fall through and re-render the form
    else:
        # Pre-select default warehouse
        from django.utils import timezone as tz
        default_wh = Warehouse.objects.filter(
            is_active=True, is_default=True,
        ).filter(
            Q(owner_company=company) | Q(owner_company__isnull=True)
        ).first()
        initial = {
            'movement_type': movement_type,
            'date':          tz.now(),
            'warehouse':     default_wh,
        }
        form = StockMovementForm(company=company, initial=initial)

    # Compute next reference preview (does not consume the sequence)
    from apps.core.models import DocumentSequence
    seq_code         = StockMovement.SEQUENCE_CODES[movement_type]
    seq              = DocumentSequence.get_for(seq_code, company)
    next_ref_preview = seq.preview

    return render(request, 'inventory/stock_movement_form.html', {
        'form':              form,
        'movement':          None,
        'movement_type':     movement_type,
        'type_label':        meta['label'],
        'type_label_singular': meta['label_singular'],
        'list_url_name':     meta['list_url_name'],
        'lines_json':        '[]',
        'next_ref_preview':  next_ref_preview,
    })


@login_required
def movement_edit(request, pk):
    """View / edit a StockMovement.

    GET  → renders the form (read-only if state != draft).
    POST → updates the header; redirects to self.
    Lines are managed separately via AJAX endpoints.
    """
    movement = get_object_or_404(StockMovement, pk=pk)
    company  = get_active_company(request)
    meta     = _MOVEMENT_TYPE_META[movement.movement_type]
    is_draft = movement.state == 'draft'

    if request.method == 'POST' and is_draft:
        form = StockMovementForm(request.POST, instance=movement, company=company)
        if form.is_valid():
            # Capture old values BEFORE save for audit diff
            _field_labels = {
                'partner':    'Fornecedor',
                'warehouse':  'Armaz\u00e9m',
                'date':       'Data',
                'origin':     'Origem',
                'notes':      'Notas Internas',
            }
            _old = {
                'partner':   str(movement.partner)   if movement.partner   else '',
                'warehouse': str(movement.warehouse) if movement.warehouse else '',
                'date':      movement.date.strftime('%d/%m/%Y %H:%M') if movement.date else '',
                'origin':    movement.origin  or '',
                'notes':     movement.notes   or '',
            }
            form.save()
            movement.refresh_from_db()
            _new = {
                'partner':   str(movement.partner)   if movement.partner   else '',
                'warehouse': str(movement.warehouse) if movement.warehouse else '',
                'date':      movement.date.strftime('%d/%m/%Y %H:%M') if movement.date else '',
                'origin':    movement.origin  or '',
                'notes':     movement.notes   or '',
            }
            _changes = {
                _field_labels[k]: {'old': _old[k], 'new': _new[k]}
                for k in _field_labels
                if _old[k] != _new[k]
            }
            ChatterActivity.objects.create(
                content_object=movement,
                user=request.user,
                activity_type='UPDATE',
                description='atualizou o movimento',
                details={'changes': _changes},
            )
            messages.success(request, 'Movimento atualizado.')
        else:
            for field, errs in form.errors.items():
                for e in errs:
                    messages.error(request, f'{field}: {e}')
        return redirect('inventory:movement_edit', pk=movement.pk)

    form = StockMovementForm(instance=movement, company=company)

    # Build lines JSON for Alpine.js initial state and compute totals for template
    import json as _json
    from decimal import Decimal as _D
    lines_data  = []
    _subtotal   = _D('0.00')
    _tax_total  = _D('0.00')
    for line in movement.lines.select_related('product', 'uom').order_by('created_at'):
        lt = _D(str(line.quantity)) * _D(str(line.unit_price))
        ta = lt * _D(str(line.tax_rate)) / _D('100')
        _subtotal  += lt
        _tax_total += ta
        lines_data.append({
            'id':           str(line.pk),
            'product_id':   str(line.product.pk),
            'product_name': line.product.name,
            'product_ref':  line.product.internal_reference or '',
            'quantity':     float(line.quantity),
            'unit_price':   float(line.unit_price),
            'uom_id':       str(line.uom.pk) if line.uom else None,
            'uom_symbol':   line.uom.symbol if line.uom else '',
            'tax_rate':     float(line.tax_rate),
            'line_total':   float(lt),
        })

    # Chatter context
    _ct = ContentType.objects.get_for_model(movement)
    chatter_notes = ChatterMessage.objects.filter(
        content_type=_ct, object_id=movement.id, message_type='NOTE'
    ).select_related('author').order_by('-created_at')
    chatter_activities = ChatterActivity.objects.filter(
        content_type=_ct, object_id=movement.id
    ).select_related('user').order_by('-created_at')[:100]

    return render(request, 'inventory/stock_movement_form.html', {
        'form':          form,
        'movement':      movement,
        'movement_type': movement.movement_type,
        'type_label':    meta['label'],
        'type_label_singular': meta['label_singular'],
        'list_url_name': meta['list_url_name'],
        'lines_json':    _json.dumps(lines_data),
        'is_draft':      is_draft,
        'next_ref_preview': None,
        'ctx_subtotal':  _subtotal,
        'ctx_tax':       _tax_total,
        'ctx_total':     _subtotal + _tax_total,
        # chatter
        'chatter_notes':      chatter_notes,
        'activities':         chatter_activities,
    })


@require_http_methods(['POST'])
@login_required
def movement_validate(request, pk):
    """Validate a draft movement → state becomes 'done' and stock is updated."""
    movement = get_object_or_404(StockMovement, pk=pk)
    if movement.state != 'draft':
        messages.error(request, 'Apenas movimentos em rascunho podem ser validados.')
        return redirect('inventory:movement_edit', pk=movement.pk)
    if not movement.lines.exists():
        messages.error(request, 'Não é possível validar um movimento sem linhas.')
        return redirect('inventory:movement_edit', pk=movement.pk)
    try:
        movement.action_validate()
        # Log STATUS_CHANGE
        ChatterActivity.objects.create(
            content_object=movement,
            user=request.user,
            activity_type='STATUS_CHANGE',
            description='validou o movimento — stock atualizado',
        )
        messages.success(request, f'Movimento {movement.reference} validado com sucesso.')
    except Exception as exc:
        messages.error(request, str(exc))
    return redirect('inventory:movement_edit', pk=movement.pk)


@require_http_methods(['POST'])
@login_required
def movement_cancel(request, pk):
    """Cancel a draft movement."""
    movement = get_object_or_404(StockMovement, pk=pk)
    meta     = _MOVEMENT_TYPE_META[movement.movement_type]
    try:
        movement.action_cancel()
        # Log STATUS_CHANGE
        ChatterActivity.objects.create(
            content_object=movement,
            user=request.user,
            activity_type='STATUS_CHANGE',
            description='cancelou o movimento',
        )
        messages.success(request, f'Movimento {movement.reference} cancelado.')
    except Exception as exc:
        messages.error(request, str(exc))
    from django.urls import reverse
    return redirect(reverse(meta['list_url_name']))


# ── Movement line AJAX endpoints ──────────────────────────────────────

@require_http_methods(['POST'])
@login_required
def movement_line_add(request, pk):
    """Add a new line to a draft movement. Expects JSON body."""
    movement = get_object_or_404(StockMovement, pk=pk)
    if movement.state != 'draft':
        return JsonResponse({'success': False, 'error': 'Movimento já validado ou cancelado.'}, status=400)

    try:
        data       = json.loads(request.body)
        product_id = data.get('product_id')
        quantity   = data.get('quantity', 1)
        unit_price = data.get('unit_price', 0)
        uom_id     = data.get('uom_id')
        tax_rate   = data.get('tax_rate', None)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'success': False, 'error': 'JSON inválido.'}, status=400)

    product = get_object_or_404(Product, pk=product_id)
    uom     = None
    if uom_id:
        uom = UoM.objects.filter(pk=uom_id).first()
    if not uom:
        # For receipts prefer the purchase UoM; for everything else use the base UoM
        if movement.movement_type == 'receipt' and product.uom_purchase_id:
            uom = product.uom_purchase
        else:
            uom = product.uom

    # Determine tax_rate: use provided value, else fall back to product
    if tax_rate is None:
        tax_rate = float(product.tax_rate)

    with transaction.atomic():
        line = StockMovementLine.objects.create(
            stock_movement=movement,
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            uom=uom,
            tax_rate=tax_rate,
        )

    return JsonResponse({
        'success': True,
        'line': {
            'id':           str(line.pk),
            'product_id':   str(product.pk),
            'product_name': product.name,
            'product_ref':  product.internal_reference or '',
            'quantity':     float(line.quantity),
            'unit_price':   float(line.unit_price),
            'uom_id':       str(line.uom.pk) if line.uom else None,
            'uom_symbol':   line.uom.symbol if line.uom else '',
            'tax_rate':     float(line.tax_rate),
            'line_total':   float(line.quantity * line.unit_price),
        },
        'movement_total': float(movement.total_value),
    })


@require_http_methods(['POST'])
@login_required
def movement_line_update(request, movement_pk, line_pk):
    """Update quantity/unit_price of an existing line. Expects JSON body."""
    movement = get_object_or_404(StockMovement, pk=movement_pk)
    line     = get_object_or_404(StockMovementLine, pk=line_pk, stock_movement=movement)

    if movement.state != 'draft':
        return JsonResponse({'success': False, 'error': 'Movimento já validado ou cancelado.'}, status=400)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'success': False, 'error': 'JSON inválido.'}, status=400)

    if 'quantity' in data:
        line.quantity = data['quantity']
    if 'unit_price' in data:
        line.unit_price = data['unit_price']
    if 'uom_id' in data and data['uom_id']:
        uom = UoM.objects.filter(pk=data['uom_id']).first()
        if uom:
            line.uom = uom
    if 'tax_rate' in data:
        line.tax_rate = data['tax_rate']
    line.save()

    return JsonResponse({
        'success': True,
        'line': {
            'id':         str(line.pk),
            'quantity':   float(line.quantity),
            'unit_price': float(line.unit_price),
            'uom_id':     str(line.uom.pk) if line.uom else None,
            'uom_symbol': line.uom.symbol if line.uom else '',
            'tax_rate':   float(line.tax_rate),
            'line_total': float(line.quantity * line.unit_price),
        },
        'movement_total': float(movement.total_value),
    })


@require_http_methods(['POST'])
@login_required
def movement_line_delete(request, movement_pk, line_pk):
    """Delete a line from a draft movement."""
    movement = get_object_or_404(StockMovement, pk=movement_pk)
    line     = get_object_or_404(StockMovementLine, pk=line_pk, stock_movement=movement)

    if movement.state != 'draft':
        return JsonResponse({'success': False, 'error': 'Movimento já validado ou cancelado.'}, status=400)

    line.delete()
    return JsonResponse({
        'success': True,
        'movement_total': float(movement.total_value),
    })


# ── Named entry points (for clean URL names) ──────────────────────────

@login_required
def receipt_list(request):
    return movement_list(request, 'receipt')


@login_required
def receipt_create(request):
    return movement_create(request, 'receipt')


@login_required
def delivery_list(request):
    return movement_list(request, 'delivery')


@login_required
def delivery_create(request):
    return movement_create(request, 'delivery')


@login_required
def adjustment_list(request):
    return movement_list(request, 'adjustment')


@login_required
def adjustment_create(request):
    return movement_create(request, 'adjustment')


# ══════════════════════════════════════════════════════════════════════════════
# CHATTER API — Movement Notes & Followers
# ══════════════════════════════════════════════════════════════════════════════


def _note_to_dict(n):
    author = n.author
    if author:
        name = author.get_full_name() or author.username
    else:
        name = 'Sistema'
    initials = ''.join(p[0].upper() for p in name.split()[:2])
    return {
        'id': str(n.id),
        'author': name,
        'author_initials': initials,
        'content': n.body,
        'created_at': n.created_at.strftime('%d/%m/%Y %H:%M'),
    }


@login_required
@require_http_methods(['GET'])
def movement_notes_list(request, pk):
    """
    GET /inventory/operations/movements/<pk>/notes/
    Returns all internal notes for a StockMovement.
    """
    movement = get_object_or_404(StockMovement, pk=pk)
    ct = ContentType.objects.get_for_model(StockMovement)
    notes = (
        ChatterMessage.objects
        .filter(content_type=ct, object_id=movement.id, message_type='NOTE')
        .select_related('author')
        .order_by('-created_at')[:100]
    )
    return JsonResponse({'notes': [_note_to_dict(n) for n in notes]})


@login_required
@require_http_methods(['POST'])
def movement_note_create(request, pk):
    """
    POST /inventory/operations/movements/<pk>/notes/create/
    Creates an internal note for a StockMovement.
    """
    movement = get_object_or_404(StockMovement, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    content = data.get('content', '').strip()
    if not content:
        return JsonResponse({'success': False, 'error': 'Conteúdo não pode estar vazio.'}, status=400)

    urgent = bool(data.get('urgent', False))
    ct = ContentType.objects.get_for_model(StockMovement)
    note = ChatterMessage.objects.create(
        content_type=ct,
        object_id=movement.id,
        author=request.user,
        message_type='NOTE',
        body=content,
    )

    # Parse @mentions and create notifications
    mentioned_usernames = list(set(re.findall(r'@(\w+)', content)))
    if mentioned_usernames:
        try:
            from apps.core.models import Notification as _N
            mentioned_users = User.objects.filter(username__in=mentioned_usernames, is_active=True)
            author_display = request.user.get_full_name() or request.user.username
            for mu in mentioned_users:
                _N.objects.create(
                    user=mu,
                    notification_type='MENTION',
                    title=f'{author_display} mencionou-te numa nota',
                    message=f'Movimento: {movement.reference}',
                    link=f'/inventory/operations/movements/{str(movement.id)}/edit/',
                    related_object_id=note.id,
                    is_urgent=urgent,
                )
        except Exception:
            pass

    return JsonResponse({'success': True, 'note': _note_to_dict(note)}, status=201)


@login_required
@require_http_methods(['GET', 'POST'])
def movement_followers_api(request, pk):
    """
    GET  /inventory/operations/movements/<pk>/followers/   — list followers
    POST /inventory/operations/movements/<pk>/followers/   — add follower { user_id }
    """
    movement = get_object_or_404(StockMovement, pk=pk)
    ct = ContentType.objects.get_for_model(StockMovement)

    if request.method == 'GET':
        # Auto-follow the current user
        ChatterFollower.objects.get_or_create(
            content_type=ct,
            object_id=movement.id,
            user=request.user,
            defaults={'added_by': None},
        )
        followers = (
            ChatterFollower.objects
            .filter(content_type=ct, object_id=movement.id)
            .select_related('user')
            .order_by('created_at')
        )
        return JsonResponse({
            'followers': [
                {
                    'user_id': str(f.user.id),
                    'display': f.user.get_full_name() or f.user.username,
                    'initials': ''.join(
                        p[0].upper()
                        for p in (f.user.get_full_name() or f.user.username).split()[:2]
                    ),
                }
                for f in followers
            ]
        })

    # POST — add follower
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    user_id = data.get('user_id', '').strip()
    if not user_id:
        return JsonResponse({'success': False, 'error': 'user_id obrigatório'}, status=400)

    try:
        target_user = User.objects.get(id=user_id, is_active=True)
    except (User.DoesNotExist, Exception):
        return JsonResponse({'success': False, 'error': 'Utilizador não encontrado'}, status=404)

    ChatterFollower.objects.get_or_create(
        content_type=ct,
        object_id=movement.id,
        user=target_user,
        defaults={'added_by': request.user},
    )
    display  = target_user.get_full_name() or target_user.username
    initials = ''.join(p[0].upper() for p in display.split()[:2])
    return JsonResponse({'success': True, 'user_id': str(target_user.id), 'display': display, 'initials': initials})


@login_required
@require_http_methods(['DELETE'])
def movement_follower_remove_api(request, pk, user_id):
    """
    DELETE /inventory/operations/movements/<pk>/followers/<user_id>/remove/
    """
    movement = get_object_or_404(StockMovement, pk=pk)
    ct = ContentType.objects.get_for_model(StockMovement)
    ChatterFollower.objects.filter(
        content_type=ct, object_id=movement.id, user_id=user_id,
    ).delete()
    return JsonResponse({'success': True})


# ── Inventário Físico (Physical Inventory) ───────────────────────────────────

@login_required
def physical_inventory_list(request):
    """List current on-hand stock (StockQuant) with search, pagination and inline editing."""
    from decimal import Decimal, InvalidOperation
    from django.db.models import F, Sum, DecimalField, ExpressionWrapper

    # ── POST: save adjustments ───────────────────────────────────────
    if request.method == 'POST':
        # 1. Update existing StockQuant rows where Ajuste was filled
        for key, value in request.POST.items():
            if key.startswith('ajuste_') and value.strip():
                quant_id = key[len('ajuste_'):]
                try:
                    new_qty = Decimal(value.strip().replace(',', '.'))
                    quant = StockQuant.objects.get(pk=quant_id)
                    quant.quantity = new_qty
                    quant.save()
                except (StockQuant.DoesNotExist, ValueError, InvalidOperation):
                    pass

        # 2. Create / update new rows
        new_product_ids  = request.POST.getlist('new_product_id')
        new_quantities    = request.POST.getlist('new_quantity')
        new_warehouse_ids = request.POST.getlist('new_warehouse_id')
        default_warehouse = Warehouse.objects.filter(is_active=True).order_by('name').first()

        for prod_id, qty_str, wh_id in zip(new_product_ids, new_quantities, new_warehouse_ids):
            if not prod_id or not qty_str.strip():
                continue
            try:
                product   = Product.objects.get(pk=prod_id)
                new_qty   = Decimal(qty_str.strip().replace(',', '.'))
                warehouse = Warehouse.objects.get(pk=wh_id) if wh_id else default_warehouse
                if warehouse:
                    StockQuant.objects.update_or_create(
                        product=product,
                        warehouse=warehouse,
                        defaults={'quantity': new_qty},
                    )
            except (Product.DoesNotExist, Warehouse.DoesNotExist, ValueError, InvalidOperation):
                pass

        messages.success(request, 'Inventário actualizado com sucesso.')
        # Preserve active filters on redirect
        qs_string = request.POST.get('_qs', '')
        return redirect(
            request.path + ('?' + qs_string if qs_string else '')
        )

    search_query = request.GET.get('search', '').strip()
    search_field = request.GET.get('field', 'auto')
    warehouse_filter = request.GET.get('warehouse', '')
    page_size = max(1, int(request.GET.get('page_size', 50)))

    qs = (
        StockQuant.objects
        .select_related('product', 'product__category', 'product__uom', 'warehouse')
        .filter(product__is_active=True)
    )

    # Search
    if search_query:
        if search_field == 'produto':
            qs = qs.filter(
                Q(product__name__icontains=search_query)
                | Q(product__internal_reference__icontains=search_query)
            )
        elif search_field == 'armazem':
            qs = qs.filter(warehouse__name__icontains=search_query)
        elif search_field == 'categoria':
            qs = qs.filter(product__category__name__icontains=search_query)
        else:  # auto
            qs = qs.filter(
                Q(product__name__icontains=search_query)
                | Q(product__internal_reference__icontains=search_query)
                | Q(warehouse__name__icontains=search_query)
                | Q(product__category__name__icontains=search_query)
            )

    if warehouse_filter:
        qs = qs.filter(warehouse__id=warehouse_filter)

    qs = qs.order_by('product__name', 'warehouse__name')

    # Annotate each row with stock_value = quantity * cost_price
    qs = qs.annotate(
        stock_value=ExpressionWrapper(
            F('quantity') * F('product__cost_price'),
            output_field=DecimalField(),
        )
    )

    total_count = qs.count()

    # Footer total: sum(stock_value) — reuses the annotation above
    total_value = qs.aggregate(total=Sum('stock_value'))['total'] or Decimal('0.00')

    paginator = Paginator(qs, page_size)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Warehouses for filter dropdown
    warehouses = Warehouse.objects.filter(is_active=True).order_by('name')
    default_warehouse = warehouses.first()

    return render(request, 'inventory/physical_inventory_list.html', {
        'quants': page_obj,
        'total_count': total_count,
        'total_value': total_value,
        'search_query': search_query,
        'search_field': search_field,
        'warehouse_filter': warehouse_filter,
        'warehouses': warehouses,
        'default_warehouse': default_warehouse,
        'page_size': page_size,
        # Inventory navbar form-action buttons
        'show_form_actions': True,
        'form_id': 'physical-inventory-form',
        'action_discard_url': request.get_full_path(),
    })


# ─── Product Supplier Info API ────────────────────────────────────────────────

@login_required
@require_http_methods(['GET', 'POST'])
def product_suppliers_api(request, pk):
    """List or create ProductSupplierInfo for a product."""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        rows = (
            ProductSupplierInfo.objects
            .filter(product=product, is_active=True)
            .select_related('supplier')
            .order_by('sequence', '-is_preferred')
        )
        return JsonResponse({'suppliers': [
            {
                'id': str(si.pk),
                'supplier_id': str(si.supplier_id),
                'supplier_name': si.supplier.name,
                'sequence': si.sequence,
                'supplier_product_code': si.supplier_product_code or '',
                'price': float(si.price),
                'min_quantity': float(si.min_quantity),
                'lead_time': si.lead_time,
                'is_preferred': si.is_preferred,
            }
            for si in rows
        ]})

    # POST — create
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    supplier_id = data.get('supplier_id')
    if not supplier_id:
        return JsonResponse({'error': 'supplier_id obrigatório'}, status=400)

    from apps.contacts.models import Contact
    supplier = get_object_or_404(Contact, pk=supplier_id)

    if ProductSupplierInfo.objects.filter(product=product, supplier=supplier).exists():
        return JsonResponse({'error': 'Este fornecedor já existe neste produto.'}, status=400)

    company = get_active_company(request)
    si = ProductSupplierInfo.objects.create(
        product=product,
        supplier=supplier,
        sequence=int(data.get('sequence', 10)),
        supplier_product_code=data.get('supplier_product_code', '').strip(),
        price=data.get('price', 0),
        min_quantity=data.get('min_quantity', 1),
        lead_time=int(data.get('lead_time', 0)),
        is_preferred=bool(data.get('is_preferred', False)),
        owner_company=company,
    )
    return JsonResponse({
        'id': str(si.pk),
        'supplier_id': str(si.supplier_id),
        'supplier_name': si.supplier.name,
        'sequence': si.sequence,
        'supplier_product_code': si.supplier_product_code,
        'price': float(si.price),
        'min_quantity': float(si.min_quantity),
        'lead_time': si.lead_time,
        'is_preferred': si.is_preferred,
    }, status=201)


@login_required
@require_http_methods(['PUT', 'DELETE'])
def product_supplier_detail_api(request, pk, si_pk):
    """Update or delete a single ProductSupplierInfo."""
    si = get_object_or_404(ProductSupplierInfo, pk=si_pk, product__pk=pk)

    if request.method == 'DELETE':
        si.delete()
        return JsonResponse({'ok': True})

    # PUT — update
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    si.sequence = int(data.get('sequence', si.sequence))
    si.supplier_product_code = data.get('supplier_product_code', si.supplier_product_code).strip()
    si.price = data.get('price', si.price)
    si.min_quantity = data.get('min_quantity', si.min_quantity)
    si.lead_time = int(data.get('lead_time', si.lead_time))
    si.is_preferred = bool(data.get('is_preferred', si.is_preferred))
    si.save()
    return JsonResponse({
        'id': str(si.pk),
        'supplier_id': str(si.supplier_id),
        'supplier_name': si.supplier.name,
        'sequence': si.sequence,
        'supplier_product_code': si.supplier_product_code,
        'price': float(si.price),
        'min_quantity': float(si.min_quantity),
        'lead_time': si.lead_time,
        'is_preferred': si.is_preferred,
    })


# ---------------------------------------------------------------------------
# All Movements List — Global view across every movement type
# ---------------------------------------------------------------------------

@login_required
def all_movements_list(request):
    """Global list of all StockMovements regardless of type.

    Filterable by movement_type (receipt/delivery/adjustment/all)
    and by state (all/draft/done/cancelled/archived).
    Searchable by reference, partner, origin.
    """
    from django.urls import reverse

    search_query = request.GET.get('search', '')
    search_field = request.GET.get('field', 'reference')
    page_number  = request.GET.get('page', 1)
    state_filter = request.GET.get('state', 'all')
    type_filter  = request.GET.get('type', 'all')

    try:
        page_size = int(request.GET.get('page_size', 50))
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    # ── Base queryset ─────────────────────────────────────────────
    if state_filter == 'archived':
        qs = StockMovement.objects.filter(is_active=False)
    elif state_filter in ('draft', 'done', 'cancelled'):
        qs = StockMovement.objects.filter(is_active=True, state=state_filter)
    else:
        qs = StockMovement.objects.filter(is_active=True)

    if type_filter in ('receipt', 'delivery', 'adjustment'):
        qs = qs.filter(movement_type=type_filter)

    qs = filter_by_company(qs, request)
    qs = qs.select_related('partner', 'warehouse', 'responsible', 'owner_company')

    # ── Search ────────────────────────────────────────────────────
    if search_query:
        field_mapping = {
            'reference': Q(reference__icontains=search_query),
            'partner':   Q(partner__name__icontains=search_query),
            'origin':    Q(origin__icontains=search_query),
        }
        qs = qs.filter(field_mapping.get(search_field, Q(reference__icontains=search_query)))

    qs = qs.order_by('-date', '-created_at')
    paginator = Paginator(qs, page_size)
    page_obj  = paginator.get_page(page_number)

    list_url = reverse('inventory:all_movements_list')

    context = {
        'movements':    page_obj,
        'list_url':     list_url,
        'search_query': search_query,
        'search_field': search_field,
        'state_filter': state_filter,
        'type_filter':  type_filter,
        'total_count':  paginator.count,
        'page_size':    page_size,
        'states': [
            ('all',       'Todos'),
            ('draft',     'Rascunho'),
            ('done',      'Validado'),
            ('cancelled', 'Cancelado'),
            ('archived',  'Arquivados'),
        ],
        'types': [
            ('all',        'Todos os tipos'),
            ('receipt',    'Receções'),
            ('delivery',   'Entregas'),
            ('adjustment', 'Ajustes'),
        ],
        'type_labels': {
            'receipt':    'Receção',
            'delivery':   'Entrega',
            'adjustment': 'Ajuste',
        },
    }
    return render(request, 'inventory/all_movements_list.html', context)


# ---------------------------------------------------------------------------
# Low-Stock Check — Manual Trigger
# ---------------------------------------------------------------------------

@login_required
@require_http_methods(["POST"])
def run_low_stock_check(request):
    """Run the low-stock check synchronously and redirect back with a result message."""
    from config.tasks import check_low_stock_periodic
    try:
        count = check_low_stock_periodic()
        if count:
            messages.success(
                request,
                f'Verificação concluída — {count} notificação(ões) de stock mínimo criada(s).',
            )
        else:
            messages.info(request, 'Verificação concluída — nenhum produto abaixo do stock mínimo.')
    except Exception as exc:
        messages.error(request, f'Erro durante a verificação: {exc}')
    return redirect(request.META.get('HTTP_REFERER', 'inventory:product_list'))
