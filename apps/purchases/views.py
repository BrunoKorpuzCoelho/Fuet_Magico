import json
import re

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_http_methods

from apps.core.models import ChatterMessage, ChatterActivity, ChatterFollower

User = get_user_model()

from apps.core.multi_company import filter_by_company, get_active_company
from .models import PurchaseOrder, PurchaseOrderLine
from .forms import PurchaseOrderForm, PurchaseOrderLineForm


_FIELD_LABELS = {
    'supplier':                'Fornecedor',
    'order_date':              'Data Encomenda',
    'expected_delivery_date':  'Entrega Prevista',
    'payment_terms':           'Condições de Pagamento',
    'origin':                  'Origem',
    'notes':                   'Notas',
}


def _log(order, user, activity_type, description, details=None):
    """Create a ChatterActivity log entry for a PurchaseOrder."""
    ct = ContentType.objects.get_for_model(PurchaseOrder)
    ChatterActivity.objects.create(
        content_type=ct,
        object_id=order.pk,
        user=user,
        activity_type=activity_type,
        description=description,
        details=details or {},
    )


def _build_lines_json(order):
    """Serialize PurchaseOrderLine queryset to JSON string for Alpine.js."""
    lines_data = []
    for line in order.lines.select_related('product', 'uom').all():
        lines_data.append({
            'id':           str(line.pk),
            'product_id':   str(line.product.pk),
            'product_name': line.product.name,
            'product_ref':  line.product.internal_reference or '',
            'quantity':     float(line.quantity),
            'uom_id':       str(line.uom.pk) if line.uom else '',
            'uom_symbol':   line.uom.symbol if line.uom else '',
            'unit_price':   float(line.unit_price),
            'tax_rate':     float(line.tax_rate),
            'discount_pct': float(line.discount_pct),
            'line_total':   float(line.line_total),
        })
    return json.dumps(lines_data)


# ────────────────────────────────────────────────────────────────────
# Purchase Order — Index
# ────────────────────────────────────────────────────────────────────

_STATUS_FILTER_OPTIONS = [
    ('all',       'Todas (Activas)',   'bg-gray-400'),
    ('draft',     'Rascunho',          'bg-gray-500'),
    ('confirmed', 'Confirmado',        'bg-yellow-500'),
    ('received',  'Recebido',          'bg-green-500'),
    ('cancelled', 'Cancelado',         'bg-red-500'),
    ('archived',  'Arquivados',        'bg-orange-400'),
]


@login_required
def purchase_order_index(request):
    """List purchase orders for the active company with search, status filter and pagination."""
    search_query = request.GET.get('search', '').strip()
    search_field = request.GET.get('field', 'order_number')
    status_filter = request.GET.get('status', 'all')
    page_number = request.GET.get('page', 1)

    try:
        page_size = int(request.GET.get('page_size', 50))
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    qs = filter_by_company(
        PurchaseOrder.objects.select_related('supplier', 'owner_company'),
        request,
    )

    # is_active / status filtering
    if status_filter == 'archived':
        qs = qs.filter(is_active=False)
    elif status_filter in ('draft', 'confirmed', 'received', 'cancelled'):
        qs = qs.filter(is_active=True, status=status_filter)
    else:
        qs = qs.filter(is_active=True)

    # Search
    if search_query:
        field_map = {
            'order_number': Q(order_number__icontains=search_query),
            'supplier':     Q(supplier__name__icontains=search_query),
            'notes':        Q(notes__icontains=search_query),
        }
        q_filter = field_map.get(search_field)
        if q_filter:
            qs = qs.filter(q_filter)
        else:
            qs = qs.filter(
                Q(order_number__icontains=search_query) |
                Q(supplier__name__icontains=search_query) |
                Q(notes__icontains=search_query)
            )

    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page_number)

    return render(request, 'purchases/order_list.html', {
        'orders': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'status_filter': status_filter,
        'status_filter_options': _STATUS_FILTER_OPTIONS,
        'total_count': paginator.count,
        'page_size': page_size,
    })


# ────────────────────────────────────────────────────────────────────
# Purchase Order — Create
# ────────────────────────────────────────────────────────────────────

@login_required
def purchase_order_create(request):
    """Create a new purchase order."""
    from .models import PaymentTerm
    from django.db.models import Q as _Q
    company = get_active_company(request)
    payment_terms_qs = PaymentTerm.objects.filter(
        _Q(owner_company=company) | _Q(owner_company__isnull=True), is_active=True
    ).order_by('days', 'name')

    form = PurchaseOrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.owner_company = company
            order.save()
            _log(order, request.user, 'CREATE', f'Encomenda {order.order_number} criada.')
        messages.success(request, f'Encomenda {order.order_number} criada.')
        return redirect('purchases:order_edit', pk=order.pk)

    default_pt = payment_terms_qs.filter(is_default=True).first()
    # On POST errors: keep what the user selected; on GET: pre-select default
    if request.method == 'POST':
        selected_pt_id = request.POST.get('payment_terms', '')
    else:
        selected_pt_id = str(default_pt.pk) if default_pt else ''
    return render(request, 'purchases/order_form.html', {
        'form': form,
        'order': None,
        'title': 'Nova Encomenda de Compra',
        'is_create': True,
        'lines_json': '[]',
        'next_ref_preview': PurchaseOrder.generate_order_number(),
        'payment_terms_qs': payment_terms_qs,
        'selected_payment_term_id': selected_pt_id,
    })


# ────────────────────────────────────────────────────────────────────
# Purchase Order — Edit
# ────────────────────────────────────────────────────────────────────

@login_required
def purchase_order_edit(request, pk):
    """Edit (or view) a purchase order."""
    order = get_object_or_404(
        filter_by_company(
            PurchaseOrder.objects.select_related('supplier', 'owner_company')
                          .prefetch_related('lines__product', 'lines__uom'),
            request,
        ),
        pk=pk,
    )

    if order.is_editable:
        form = PurchaseOrderForm(request.POST or None, instance=order)
        if request.method == 'POST' and form.is_valid():
            with transaction.atomic():
                # Capture human-readable before-values
                old_supplier = order.supplier.name if order.supplier else ''
                old_vals = {
                    'supplier':               old_supplier,
                    'order_date':             str(order.order_date or ''),
                    'expected_delivery_date': str(order.expected_delivery_date or ''),
                    'payment_terms':          str(order.payment_terms.name if order.payment_terms else ''),
                    'origin':                 str(order.origin or ''),
                    'notes':                  str(order.notes or ''),
                }
                form.save()
                order.refresh_from_db()
                new_supplier = order.supplier.name if order.supplier else ''
                new_vals = {
                    'supplier':               new_supplier,
                    'order_date':             str(order.order_date or ''),
                    'expected_delivery_date': str(order.expected_delivery_date or ''),
                    'payment_terms':          str(order.payment_terms.name if order.payment_terms else ''),
                    'origin':                 str(order.origin or ''),
                    'notes':                  str(order.notes or ''),
                }
                changes = {
                    _FIELD_LABELS[f]: {'old': old_vals[f], 'new': new_vals[f]}
                    for f in old_vals if old_vals[f] != new_vals[f]
                }
                if changes:
                    _log(order, request.user, 'UPDATE', 'Encomenda actualizada.', {'changes': changes})
            messages.success(request, 'Encomenda guardada.')
            return redirect('purchases:order_edit', pk=order.pk)
    else:
        form = PurchaseOrderForm(instance=order)  # read-only display

    # Chatter context
    _ct = ContentType.objects.get_for_model(PurchaseOrder)
    chatter_activities = ChatterActivity.objects.filter(
        content_type=_ct, object_id=order.id
    ).select_related('user').order_by('-created_at')[:100]

    # Smart button counts
    from apps.inventory.models import StockMovement
    receipt_count = StockMovement.objects.filter(
        origin=order.order_number,
        movement_type='receipt',
    ).count()

    # Payment terms for select field
    from .models import PaymentTerm
    payment_terms_qs = PaymentTerm.objects.filter(
        Q(owner_company=order.owner_company) | Q(owner_company__isnull=True), is_active=True
    ).order_by('days', 'name')

    return render(request, 'purchases/order_form.html', {
        'form': form,
        'order': order,
        'title': order.order_number,
        'is_create': False,
        'lines_json': _build_lines_json(order),
        'next_ref_preview': None,
        'activities': chatter_activities,
        'receipt_count': receipt_count,
        'payment_terms_qs': payment_terms_qs,
        'selected_payment_term_id': request.POST.get('payment_terms', str(order.payment_terms_id) if order.payment_terms_id else '') if request.method == 'POST' else str(order.payment_terms_id) if order.payment_terms_id else '',
        'has_smtp':                getattr(getattr(request.user, 'email_config', None), 'has_smtp_configured', False),
        'chatter_contact_email':   order.supplier.email if order.supplier else '',
    })


# ────────────────────────────────────────────────────────────────────
# Purchase Order — Detail (read-only)
# ────────────────────────────────────────────────────────────────────

@login_required
def purchase_order_detail(request, pk):
    """Redirect to edit view (which handles all states)."""
    return redirect('purchases:order_edit', pk=pk)


# ────────────────────────────────────────────────────────────────────
# Purchase Order — State transitions
# ────────────────────────────────────────────────────────────────────

@login_required
@require_POST
def purchase_order_confirm(request, pk):
    """Confirm a DRAFT order → CONFIRMED and create a draft receipt StockMovement."""
    from apps.inventory.models import StockMovement, StockMovementLine, Warehouse

    order = get_object_or_404(
        filter_by_company(
            PurchaseOrder.objects.prefetch_related('lines__product', 'lines__uom'),
            request,
        ),
        pk=pk,
    )
    if order.status != PurchaseOrder.Status.DRAFT:
        messages.error(request, 'Apenas encomendas em rascunho podem ser confirmadas.')
        return redirect('purchases:order_detail', pk=order.pk)

    po_lines = list(order.lines.select_related('product', 'uom').all())
    if not po_lines:
        messages.error(request, 'Não é possível confirmar uma encomenda sem linhas.')
        return redirect('purchases:order_edit', pk=order.pk)

    # Resolve default warehouse for this company
    warehouse = (
        Warehouse.objects.filter(owner_company=order.owner_company, is_default=True).first()
        or Warehouse.objects.filter(owner_company=order.owner_company).first()
        or Warehouse.objects.filter(owner_company__isnull=True).first()
    )
    if not warehouse:
        messages.error(request, 'Não existe nenhum armazém configurado. Cria um armazém antes de confirmar.')
        return redirect('purchases:order_edit', pk=order.pk)

    with transaction.atomic():
        # 1. Confirm the purchase order
        order.status = PurchaseOrder.Status.CONFIRMED
        order.save(update_fields=['status'])

        # 2. Create a draft receipt movement linked via origin
        movement = StockMovement.objects.create(
            movement_type='receipt',
            state='draft',
            warehouse=warehouse,
            partner=order.supplier,
            origin=order.order_number,
            notes=f'Gerado automaticamente a partir da encomenda {order.order_number}.',
            responsible=request.user,
            owner_company=order.owner_company,
        )

        # 3. Copy every PO line into the movement
        StockMovementLine.objects.bulk_create([
            StockMovementLine(
                stock_movement=movement,
                product=line.product,
                quantity=line.quantity,
                unit_price=line.unit_price,
                uom=line.uom,
                tax_rate=line.tax_rate,
                discount_pct=line.discount_pct,
            )
            for line in po_lines
        ])

        _log(
            order, request.user, 'STATUS_CHANGE',
            f'Estado alterado: Rascunho → Confirmado. Receção {movement.reference} criada.',
            {
                'field':       'status',
                'old':         'draft',
                'new':         'confirmed',
                'receipt_ref': movement.reference,
                'receipt_pk':  str(movement.pk),
            },
        )

    messages.success(
        request,
        f'Encomenda {order.order_number} confirmada. Receção {movement.reference} criada em rascunho.',
    )
    return redirect('purchases:order_edit', pk=order.pk)


@login_required
@require_POST
def purchase_order_receive(request, pk):
    """Mark a CONFIRMED order as RECEIVED and create stock movements."""
    order = get_object_or_404(
        filter_by_company(PurchaseOrder.objects.prefetch_related('lines__product'), request),
        pk=pk,
    )
    if order.status != PurchaseOrder.Status.CONFIRMED:
        messages.error(request, 'Apenas encomendas confirmadas podem ser recebidas.')
        return redirect('purchases:order_detail', pk=order.pk)

    # TODO (7.8): create StockMovements / StockMovementLines for each line
    order.status = PurchaseOrder.Status.RECEIVED
    order.save(update_fields=['status'])
    _log(order, request.user, 'STATUS_CHANGE', 'Estado alterado: Confirmado → Recebido.', {'field': 'status', 'old': 'confirmed', 'new': 'received'})
    messages.success(request, f'Encomenda {order.order_number} recebida. Stock actualizado.')
    return redirect('purchases:order_edit', pk=order.pk)


@login_required
@require_POST
def purchase_order_cancel(request, pk):
    """Cancel an order (not allowed if already RECEIVED)."""
    order = get_object_or_404(
        filter_by_company(PurchaseOrder.objects, request), pk=pk
    )
    if order.status == PurchaseOrder.Status.RECEIVED:
        messages.error(request, 'Não é possível cancelar uma encomenda já recebida.')
        return redirect('purchases:order_detail', pk=order.pk)
    old_status = order.status
    order.status = PurchaseOrder.Status.CANCELLED
    order.save(update_fields=['status'])
    _log(order, request.user, 'STATUS_CHANGE', f'Estado alterado: {old_status} → Cancelado.', {'field': 'status', 'old': old_status, 'new': 'cancelled'})
    messages.success(request, f'Encomenda {order.order_number} cancelada.')
    return redirect('purchases:order_edit', pk=order.pk)


# ────────────────────────────────────────────────────────────────────
# Purchase Order Line — Add / Remove (AJAX)
# ────────────────────────────────────────────────────────────────────

@login_required
@require_POST
def purchase_order_line_add(request, pk):
    """Add a line to a DRAFT purchase order (JSON body)."""
    order = get_object_or_404(
        filter_by_company(PurchaseOrder.objects, request), pk=pk
    )
    if not order.is_editable:
        return JsonResponse({'error': 'Encomenda não editável.'}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido.'}, status=400)

    product_id = data.get('product_id')
    if not product_id:
        return JsonResponse({'error': 'product_id é obrigatório.'}, status=400)

    from apps.inventory.models import Product, UoM
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado.'}, status=404)

    uom_id = data.get('uom_id')
    uom = None
    if uom_id:
        try:
            uom = UoM.objects.get(pk=uom_id)
        except UoM.DoesNotExist:
            pass
    if not uom:
        uom = product.uom

    quantity   = data.get('quantity', 1)
    unit_price = data.get('unit_price', float(product.cost_price or 0))
    tax_rate   = data.get('tax_rate', 0)
    discount_pct = data.get('discount_pct', 0)

    with transaction.atomic():
        line = PurchaseOrderLine.objects.create(
            purchase_order=order,
            product=product,
            uom=uom,
            quantity=quantity,
            unit_price=unit_price,
            tax_rate=tax_rate,
            discount_pct=discount_pct,
        )
        order.recalculate_totals()
        _log(order, request.user, 'UPDATE', f'Linha adicionada: {product.name}', {
            'changes': {
                'Produto':    {'old': '', 'new': product.name},
                'Quantidade': {'old': '', 'new': str(quantity)},
                'Preço Unit.': {'old': '', 'new': str(unit_price)},
            }
        })

    return JsonResponse({
        'success': True,
        'line_id': str(line.id),
        'product_name': line.product.name,
        'quantity': float(line.quantity),
        'unit_price': float(line.unit_price),
        'tax_rate': float(line.tax_rate),
        'line_total': float(line.line_total),
        'order_subtotal': float(order.subtotal),
        'order_tax': float(order.tax),
        'order_total': float(order.total),
    })


@login_required
@require_POST
def purchase_order_line_remove(request, pk, line_pk):
    """Remove a line from a DRAFT purchase order."""
    order = get_object_or_404(
        filter_by_company(PurchaseOrder.objects, request), pk=pk
    )
    if not order.is_editable:
        return JsonResponse({'error': 'Encomenda não editável.'}, status=400)
    line = get_object_or_404(PurchaseOrderLine, pk=line_pk, purchase_order=order)
    product_name = line.product.name if line.product else ''
    with transaction.atomic():
        line.delete()
        order.recalculate_totals()
        _log(order, request.user, 'UPDATE', f'Linha removida: {product_name}', {
            'changes': {'Produto': {'old': product_name, 'new': ''}}
        })
    return JsonResponse({'success': True, 'order_total': float(order.total)})


@login_required
@require_POST
def purchase_order_line_update(request, pk, line_pk):
    """Update qty/price/tax of an existing DRAFT line (JSON body)."""
    order = get_object_or_404(
        filter_by_company(PurchaseOrder.objects, request), pk=pk
    )
    if not order.is_editable:
        return JsonResponse({'error': 'Encomenda não editável.'}, status=400)
    line = get_object_or_404(PurchaseOrderLine, pk=line_pk, purchase_order=order)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido.'}, status=400)
    old_qty   = float(line.quantity)
    old_price = float(line.unit_price)
    old_tax   = float(line.tax_rate)
    old_discount = float(line.discount_pct)
    if 'quantity' in data:
        line.quantity = data['quantity']
    if 'unit_price' in data:
        line.unit_price = data['unit_price']
    if 'uom_id' in data and data['uom_id']:
        line.uom_id = data['uom_id']
    if 'tax_rate' in data:
        line.tax_rate = data['tax_rate']
    if 'discount_pct' in data:
        line.discount_pct = data['discount_pct']
    with transaction.atomic():
        line.save()
        order.recalculate_totals()
        line_changes = {}
        if old_qty != float(line.quantity):
            line_changes['Quantidade'] = {'old': str(old_qty), 'new': str(float(line.quantity))}
        if old_price != float(line.unit_price):
            line_changes['Preço Unit.'] = {'old': str(old_price), 'new': str(float(line.unit_price))}
        if old_tax != float(line.tax_rate):
            line_changes['IVA %'] = {'old': str(old_tax), 'new': str(float(line.tax_rate))}
        if old_discount != float(line.discount_pct):
            line_changes['Desconto %'] = {'old': str(old_discount), 'new': str(float(line.discount_pct))}
        if line_changes:
            product_name = line.product.name if line.product else ''
            _log(order, request.user, 'UPDATE', f'Linha actualizada: {product_name}', {'changes': line_changes})
    return JsonResponse({
        'success': True,
        'line': {
            'id': str(line.pk),
            'line_total': float(line.line_total),
        },
        'order_subtotal': float(order.subtotal),
        'order_tax': float(order.tax),
        'order_total': float(order.total),
    })


# ────────────────────────────────────────────────────────────────────
# Bulk actions (AJAX — used by list view)
# ────────────────────────────────────────────────────────────────────

def _parse_order_ids(request):
    """Extract and validate order_ids list from JSON body."""
    try:
        data = json.loads(request.body)
        ids = data.get('order_ids', [])
        if not isinstance(ids, list):
            return None, 'order_ids deve ser uma lista'
        return ids, None
    except json.JSONDecodeError:
        return None, 'JSON inválido'


@login_required
@require_POST
def purchase_order_bulk_archive(request):
    """Bulk archive (is_active=False) purchase orders."""
    ids, err = _parse_order_ids(request)
    if err:
        return JsonResponse({'success': False, 'error': err}, status=400)
    qs = filter_by_company(PurchaseOrder.objects, request).filter(pk__in=ids, is_active=True)
    updated = qs.update(is_active=False)
    return JsonResponse({'success': True, 'message': f'{updated} encomenda(s) arquivada(s).', 'updated': updated})


@login_required
@require_POST
def purchase_order_bulk_unarchive(request):
    """Bulk unarchive (is_active=True) purchase orders."""
    ids, err = _parse_order_ids(request)
    if err:
        return JsonResponse({'success': False, 'error': err}, status=400)
    qs = filter_by_company(PurchaseOrder.objects, request).filter(pk__in=ids, is_active=False)
    updated = qs.update(is_active=True)
    return JsonResponse({'success': True, 'message': f'{updated} encomenda(s) desarquivada(s).', 'updated': updated})


@login_required
@require_POST
def purchase_order_bulk_delete(request):
    """Permanently delete purchase orders (admin only)."""
    if getattr(request.user, 'role', None) != 'ADMIN':
        return JsonResponse({'success': False, 'error': 'Apenas administradores podem eliminar encomendas.'}, status=403)
    ids, err = _parse_order_ids(request)
    if err:
        return JsonResponse({'success': False, 'error': err}, status=400)
    qs = filter_by_company(PurchaseOrder.objects, request).filter(pk__in=ids)
    count = qs.count()
    qs.delete()
    return JsonResponse({'success': True, 'message': f'{count} encomenda(s) eliminada(s) permanentemente.', 'deleted': count})


# ── Chatter — Notes & Followers ─────────────────────────────────────────────

def _po_note_to_dict(n):
    author = n.author
    name = author.get_full_name() or author.username if author else 'Sistema'
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
def purchase_order_notes_list(request, pk):
    """GET /purchases/<pk>/notes/"""
    order = get_object_or_404(PurchaseOrder, pk=pk)
    ct = ContentType.objects.get_for_model(PurchaseOrder)
    notes = (
        ChatterMessage.objects
        .filter(content_type=ct, object_id=order.id, message_type='NOTE')
        .select_related('author')
        .order_by('-created_at')[:100]
    )
    return JsonResponse({'notes': [_po_note_to_dict(n) for n in notes]})


@login_required
@require_http_methods(['POST'])
def purchase_order_note_create(request, pk):
    """POST /purchases/<pk>/notes/create/"""
    order = get_object_or_404(PurchaseOrder, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    content = data.get('content', '').strip()
    if not content:
        return JsonResponse({'success': False, 'error': 'Conteúdo não pode estar vazio.'}, status=400)

    urgent = bool(data.get('urgent', False))
    ct = ContentType.objects.get_for_model(PurchaseOrder)
    note = ChatterMessage.objects.create(
        content_type=ct,
        object_id=order.id,
        author=request.user,
        message_type='NOTE',
        body=content,
    )

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
                    message=f'Encomenda: {order.order_number}',
                    link=f'/purchases/{str(order.id)}/edit/',
                    related_object_id=note.id,
                    is_urgent=urgent,
                )
        except Exception:
            pass

    return JsonResponse({'success': True, 'note': _po_note_to_dict(note)}, status=201)


@login_required
@require_http_methods(['GET', 'POST'])
def purchase_order_followers_api(request, pk):
    """GET/POST /purchases/<pk>/followers/"""
    order = get_object_or_404(PurchaseOrder, pk=pk)
    ct = ContentType.objects.get_for_model(PurchaseOrder)

    if request.method == 'GET':
        ChatterFollower.objects.get_or_create(
            content_type=ct, object_id=order.id, user=request.user,
            defaults={'added_by': None},
        )
        followers = (
            ChatterFollower.objects
            .filter(content_type=ct, object_id=order.id)
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
        content_type=ct, object_id=order.id, user=target_user,
        defaults={'added_by': request.user},
    )
    display  = target_user.get_full_name() or target_user.username
    initials = ''.join(p[0].upper() for p in display.split()[:2])
    return JsonResponse({'success': True, 'user_id': str(target_user.id), 'display': display, 'initials': initials})


@login_required
@require_http_methods(['DELETE'])
def purchase_order_follower_remove(request, pk, user_id):
    """DELETE /purchases/<pk>/followers/<user_id>/remove/"""
    order = get_object_or_404(PurchaseOrder, pk=pk)
    ct = ContentType.objects.get_for_model(PurchaseOrder)
    ChatterFollower.objects.filter(
        content_type=ct, object_id=order.id, user_id=user_id,
    ).delete()
    return JsonResponse({'success': True})


# ──────────────────────────────────────────────────────────────────
# Payment Terms — CRUD
# ──────────────────────────────────────────────────────────────────

@login_required
def payment_term_list(request):
    """List payment terms with search and pagination."""
    from .models import PaymentTerm
    from django.core.paginator import Paginator

    company = get_active_company(request)
    search_query = request.GET.get('search', '').strip()
    search_field = request.GET.get('field', '')
    active_filter = request.GET.get('active', '')
    page_size = max(1, int(request.GET.get('page_size', 50) or 50))

    qs = PaymentTerm.objects.filter(
        Q(owner_company=company) | Q(owner_company__isnull=True)
    ).order_by('days', 'name')

    # Active filter
    if active_filter == 'active':
        qs = qs.filter(is_active=True)
    elif active_filter == 'inactive':
        qs = qs.filter(is_active=False)

    # Search filter
    if search_query:
        if search_field == 'name':
            qs = qs.filter(name__icontains=search_query)
        elif search_field == 'description':
            qs = qs.filter(description__icontains=search_query)
        else:
            qs = qs.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    total_count = qs.count()
    paginator = Paginator(qs, page_size)
    page_number = request.GET.get('page', 1)
    payment_terms_page = paginator.get_page(page_number)

    return render(request, 'purchases/payment_term_list.html', {
        'payment_terms': payment_terms_page,
        'search_query':  search_query,
        'search_field':  search_field,
        'active_filter': active_filter,
        'total_count':   total_count,
        'page_size':     page_size,
    })


@login_required
def payment_term_create(request):
    """Create a new payment term."""
    from .models import PaymentTerm
    from .forms import PaymentTermForm

    company = get_active_company(request)
    form = PaymentTermForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        pt = form.save(commit=False)
        pt.owner_company = company
        pt.save()
        messages.success(request, f'Condição de pagamento "{pt.name}" criada.')
        return redirect('purchases:payment_term_list')

    return render(request, 'purchases/payment_term_form.html', {
        'form':    form,
        'editing': None,
    })


@login_required
def payment_term_edit(request, pk):
    """Edit an existing payment term."""
    from .models import PaymentTerm
    from .forms import PaymentTermForm

    company = get_active_company(request)
    pt = get_object_or_404(PaymentTerm, pk=pk)
    form = PaymentTermForm(request.POST or None, instance=pt)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Condição de pagamento "{pt.name}" actualizada.')
        return redirect('purchases:payment_term_list')

    return render(request, 'purchases/payment_term_form.html', {
        'form':    form,
        'editing': pt,
    })


@login_required
@require_POST
def payment_term_toggle(request, pk):
    """Toggle active/inactive on a payment term."""
    from .models import PaymentTerm
    pt = get_object_or_404(PaymentTerm, pk=pk)
    pt.is_active = not pt.is_active
    pt.save(update_fields=['is_active'])
    state = 'activada' if pt.is_active else 'desactivada'
    messages.success(request, f'"{pt.name}" {state}.')
    return redirect('purchases:payment_term_list')


@login_required
@require_POST
def payment_term_delete(request, pk):
    """Delete a payment term only if no purchase orders reference it."""
    from .models import PaymentTerm
    pt = get_object_or_404(PaymentTerm, pk=pk)
    if pt.purchase_orders.exists():
        messages.error(request, f'Não é possível eliminar "{pt.name}" — está associada a encomendas.')
    else:
        name = pt.name
        pt.delete()
        messages.success(request, f'"{name}" eliminada.')
    return redirect('purchases:payment_term_list')


@login_required
@require_POST
def payment_term_bulk_activate(request):
    """Bulk-activate (desarquivar) payment terms."""
    import json
    from .models import PaymentTerm
    try:
        data = json.loads(request.body)
        ids = data.get('term_ids', [])
        count = PaymentTerm.objects.filter(pk__in=ids).update(is_active=True)
        return JsonResponse({'success': True, 'message': f'{count} condição(oes) activada(s).'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def payment_term_bulk_deactivate(request):
    """Bulk-deactivate (arquivar) payment terms."""
    import json
    from .models import PaymentTerm
    try:
        data = json.loads(request.body)
        ids = data.get('term_ids', [])
        count = PaymentTerm.objects.filter(pk__in=ids).update(is_active=False)
        return JsonResponse({'success': True, 'message': f'{count} condição(oes) desactivada(s).'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def payment_term_bulk_delete(request):
    """Bulk-delete payment terms that have no associated purchase orders."""
    import json
    from .models import PaymentTerm
    try:
        data = json.loads(request.body)
        ids = data.get('term_ids', [])
        qs = PaymentTerm.objects.filter(pk__in=ids)
        blocked = [pt.name for pt in qs if pt.purchase_orders.exists()]
        deletable = qs.exclude(pk__in=[
            pt.pk for pt in qs if pt.purchase_orders.exists()
        ])
        count = deletable.count()
        deletable.delete()
        if blocked:
            return JsonResponse({
                'success': True,
                'message': f'{count} eliminada(s).',
                'warning': f'Não foi possível eliminar: {", ".join(blocked)} (têm encomendas associadas).',
            })
        return JsonResponse({'success': True, 'message': f'{count} condição(oes) eliminada(s).'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
