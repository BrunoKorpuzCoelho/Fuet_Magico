import json
from datetime import timedelta

from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from apps.core.multi_company import filter_by_company, get_active_company
from .forms import CategoryForm, UoMForm, UoMCategoryForm, ProductForm, WarehouseForm
from .models import Category, UoM, UoMCategory, Product, Warehouse


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
    categories = filter_by_company(Category.objects.filter(is_active=True), request)

    # Placeholder weekly bars (will be real data once models exist)
    weekly_bars = _weekly_placeholder_bars()

    context = {
        # Recepções card
        'receipts_to_process': 0,
        'receipts_waiting': 0,
        'receipts_late': 0,
        'receipts_done_today': 0,
        'receipts_weekly': weekly_bars,

        # Entregas card
        'deliveries_to_process': 0,
        'deliveries_waiting': 0,
        'deliveries_late': 0,
        'deliveries_done_today': 0,
        'deliveries_weekly': weekly_bars,

        # Erros card
        'errors_to_resolve': 0,
        'errors_missing_products': 0,
        'errors_documents': 0,
        'errors_resolved_today': 0,
        'errors_weekly': weekly_bars,

        # Operações Hoje card
        'ops_today': 0,
        'ops_today_receipts': 0,
        'ops_today_deliveries': 0,
        'ops_today_adjustments': 0,
        'ops_today_weekly': weekly_bars,

        # Pendentes card
        'total_pending': 0,
        'pending_receipts': 0,
        'pending_deliveries': 0,
        'pending_other': 0,
        'pending_weekly': weekly_bars,
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

    qs = qs.order_by('name')
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
    }
    return render(request, 'inventory/product_list.html', context)


# ── Product create / edit ─────────────────────────────────────────────

@login_required
def product_create(request):
    """Create a new product."""
    company = get_active_company(request)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, company=company)
        if form.is_valid():
            product = form.save(commit=False)
            if not product.owner_company:
                product.owner_company = company
            product.save()
            messages.success(request, f'Produto "{product.name}" criado com sucesso!')
            return redirect('inventory:product_edit', pk=product.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm(company=company)

    context = {'form': form}
    return render(request, 'inventory/product_form.html', context)


@login_required
def product_edit(request, pk):
    """Edit an existing product."""
    product = get_object_or_404(Product, pk=pk)
    company = get_active_company(request)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, company=company)
        if form.is_valid():
            p = form.save(commit=False)
            if not p.owner_company:
                p.owner_company = company
            p.save()
            messages.success(request, f'Produto "{p.name}" atualizado com sucesso!')
            return redirect('inventory:product_edit', pk=p.pk)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm(instance=product, company=company)

    # Smart button counts (placeholder zeros until modules exist)
    bom_count = 0        # Bill of Materials
    forecast_count = 0   # Previsão
    sold_count = 0       # Unidades vendidas
    on_hand_count = 0    # Em stock

    context = {
        'form': form,
        'product': product,
        'bom_count': bom_count,
        'forecast_count': forecast_count,
        'sold_count': sold_count,
        'on_hand_count': on_hand_count,
    }
    return render(request, 'inventory/product_form.html', context)


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