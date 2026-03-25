import json
from datetime import date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q, F, ExpressionWrapper, DecimalField
from django.shortcuts import render
from django.utils import timezone

from apps.core.multi_company import get_active_company
from apps.sales.models import SaleOrder, SaleOrderLine
from apps.purchases.models import PurchaseOrder
from apps.inventory.models import StockMovement, StockMovementLine, Product


# ── Helpers ───────────────────────────────────────────────────────────────────

REVENUE_STATUSES = ['confirmed', 'delivered', 'invoiced']
COST_STATUSES = ['confirmed', 'received']

MONTH_NAMES = [
    'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez',
]


def _sales_qs(company):
    qs = SaleOrder.objects.filter(status__in=REVENUE_STATUSES)
    if company:
        qs = qs.filter(owner_company=company)
    return qs


def _purchases_qs(company):
    qs = PurchaseOrder.objects.filter(status__in=COST_STATUSES)
    if company:
        qs = qs.filter(owner_company=company)
    return qs


def _dec(value):
    """Convert value to Decimal, handling None."""
    return Decimal(str(value)) if value is not None else Decimal('0.00')


def _cogs(company, year, month=None):
    """Cost of Goods Sold: sum of qty × product.cost_price for confirmed sale lines."""
    order_filter = Q(
        sale_order__status__in=REVENUE_STATUSES,
        sale_order__order_date__year=year,
    )
    if company:
        order_filter &= Q(sale_order__owner_company=company)
    if month:
        order_filter &= Q(sale_order__order_date__month=month)
    result = (
        SaleOrderLine.objects
        .filter(order_filter)
        .annotate(
            line_cost=ExpressionWrapper(
                F('quantity') * F('product__cost_price'),
                output_field=DecimalField(max_digits=14, decimal_places=4),
            )
        )
        .aggregate(total=Sum('line_cost'))['total']
    )
    return _dec(result)


# ── Dashboard ─────────────────────────────────────────────────────────────────

@login_required
def financial_index(request):
    company = get_active_company(request)
    today = timezone.now().date()
    year = today.year
    month = today.month

    # Current month KPIs
    month_sales = _sales_qs(company).filter(
        order_date__year=year,
        order_date__month=month,
    ).aggregate(total=Sum('subtotal'))['total'] or Decimal('0.00')

    month_costs = _cogs(company, year, month)

    month_profit = _dec(month_sales) - _dec(month_costs)
    month_margin = (
        round(float(month_profit) / float(month_sales) * 100, 1)
        if month_sales else 0
    )

    # Year-to-date KPIs
    ytd_sales = _sales_qs(company).filter(
        order_date__year=year,
    ).aggregate(total=Sum('subtotal'))['total'] or Decimal('0.00')

    ytd_costs = _cogs(company, year)

    ytd_profit = _dec(ytd_sales) - _dec(ytd_costs)

    # Last 6 months mini chart data
    labels = []
    rev_data = []
    cost_data = []
    for i in range(5, -1, -1):
        m = month - i
        y = year
        while m <= 0:
            m += 12
            y -= 1
        s = _sales_qs(company).filter(order_date__year=y, order_date__month=m).aggregate(
            t=Sum('subtotal'))['t'] or 0
        c = _cogs(company, y, m)
        labels.append(MONTH_NAMES[m - 1])
        rev_data.append(float(s))
        cost_data.append(float(c))

    return render(request, 'financial/reports_index.html', {
        'month_sales': month_sales,
        'month_costs': month_costs,
        'month_profit': month_profit,
        'month_margin': month_margin,
        'ytd_sales': ytd_sales,
        'ytd_costs': ytd_costs,
        'ytd_profit': ytd_profit,
        'current_month': MONTH_NAMES[month - 1],
        'current_year': year,
        'chart_labels_json': json.dumps(labels),
        'chart_rev_json': json.dumps(rev_data),
        'chart_cost_json': json.dumps(cost_data),
    })


# ── P&L Mensal ────────────────────────────────────────────────────────────────

@login_required
def report_pnl(request):
    company = get_active_company(request)
    today = timezone.now().date()

    year = int(request.GET.get('year', today.year))

    rows = []
    for m in range(1, 13):
        sales = _dec(_sales_qs(company).filter(order_date__year=year, order_date__month=m).aggregate(
            t=Sum('subtotal'))['t'])
        costs = _cogs(company, year, m)
        profit = _dec(sales) - _dec(costs)
        margin = round(float(profit) / float(sales) * 100, 1) if sales else 0
        rows.append({
            'month': MONTH_NAMES[m - 1],
            'month_num': m,
            'sales': sales,
            'costs': costs,
            'profit': profit,
            'margin': margin,
        })

    total_sales = sum(_dec(r['sales']) for r in rows)
    total_costs = sum(_dec(r['costs']) for r in rows)
    total_profit = total_sales - total_costs
    total_margin = round(float(total_profit) / float(total_sales) * 100, 1) if total_sales else 0

    # Chart data
    chart_labels = json.dumps(MONTH_NAMES)
    chart_rev = json.dumps([float(r['sales']) for r in rows])
    chart_cost = json.dumps([float(r['costs']) for r in rows])
    chart_profit = json.dumps([float(r['profit']) for r in rows])

    years = list(range(today.year, today.year - 5, -1))

    return render(request, 'financial/report_pnl.html', {
        'rows': rows,
        'year': year,
        'years': years,
        'total_sales': total_sales,
        'total_costs': total_costs,
        'total_profit': total_profit,
        'total_margin': total_margin,
        'chart_labels': chart_labels,
        'chart_rev': chart_rev,
        'chart_cost': chart_cost,
        'chart_profit': chart_profit,
    })


# ── Vendas por Período ────────────────────────────────────────────────────────

@login_required
def report_sales_period(request):
    company = get_active_company(request)
    today = timezone.now().date()

    year = int(request.GET.get('year', today.year))
    month = request.GET.get('month', '')

    qs = _sales_qs(company).filter(order_date__year=year)
    if month:
        qs = qs.filter(order_date__month=int(month))

    orders = qs.select_related('client').order_by('-order_date')

    total_revenue = qs.aggregate(t=Sum('subtotal'))['t'] or Decimal('0.00')
    total_orders = qs.count()

    years = list(range(today.year, today.year - 5, -1))
    months = [(i, MONTH_NAMES[i - 1]) for i in range(1, 13)]

    return render(request, 'financial/report_sales_period.html', {
        'orders': orders,
        'year': year,
        'month': int(month) if month else '',
        'years': years,
        'months': months,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
    })


# ── Vendas por Produto ────────────────────────────────────────────────────────

@login_required
def report_sales_products(request):
    company = get_active_company(request)
    today = timezone.now().date()

    year = int(request.GET.get('year', today.year))
    month = request.GET.get('month', '')

    # Filter sale orders first
    order_filter = Q(
        sale_order__status__in=REVENUE_STATUSES,
        sale_order__order_date__year=year,
    )
    if company:
        order_filter &= Q(sale_order__owner_company=company)
    if month:
        order_filter &= Q(sale_order__order_date__month=int(month))

    lines = (
        SaleOrderLine.objects
        .filter(order_filter)
        .annotate(
            line_val=ExpressionWrapper(
                F('quantity') * F('unit_price') * (1 - F('discount_pct') / Decimal('100')),
                output_field=DecimalField(max_digits=14, decimal_places=4),
            )
        )
        .values('product__id', 'product__name', 'product__internal_reference')
        .annotate(
            total_qty=Sum('quantity'),
            total_revenue=Sum('line_val'),
            order_count=Count('sale_order', distinct=True),
        )
        .order_by('-total_revenue')
    )

    grand_total = sum(r['total_revenue'] or 0 for r in lines)

    years = list(range(today.year, today.year - 5, -1))
    months = [(i, MONTH_NAMES[i - 1]) for i in range(1, 13)]

    return render(request, 'financial/report_sales_products.html', {
        'lines': lines,
        'year': year,
        'month': int(month) if month else '',
        'years': years,
        'months': months,
        'grand_total': grand_total,
    })


# ── Vendas por Cliente ────────────────────────────────────────────────────────

@login_required
def report_sales_clients(request):
    company = get_active_company(request)
    today = timezone.now().date()

    year = int(request.GET.get('year', today.year))
    month = request.GET.get('month', '')

    qs = _sales_qs(company).filter(order_date__year=year)
    if month:
        qs = qs.filter(order_date__month=int(month))

    rows = (
        qs
        .values('client__id', 'client__name')
        .annotate(
            total=Sum('subtotal'),
            order_count=Count('id'),
        )
        .order_by('-total')
    )

    grand_total = qs.aggregate(t=Sum('subtotal'))['t'] or Decimal('0.00')

    years = list(range(today.year, today.year - 5, -1))
    months = [(i, MONTH_NAMES[i - 1]) for i in range(1, 13)]

    return render(request, 'financial/report_sales_clients.html', {
        'rows': rows,
        'year': year,
        'month': int(month) if month else '',
        'years': years,
        'months': months,
        'grand_total': grand_total,
    })


# ── Evolução da Receita ───────────────────────────────────────────────────────

@login_required
def report_sales_evolution(request):
    company = get_active_company(request)
    today = timezone.now().date()

    period = int(request.GET.get('period', 12))  # 12 or 24

    labels = []
    rev_data = []
    cost_data = []
    profit_data = []

    for i in range(period - 1, -1, -1):
        m = today.month - i
        y = today.year
        while m <= 0:
            m += 12
            y -= 1
        label = f"{MONTH_NAMES[m - 1]}/{str(y)[-2:]}"
        s = _dec(
            _sales_qs(company).filter(order_date__year=y, order_date__month=m).aggregate(
                t=Sum('subtotal'))['t']
        )
        c = _cogs(company, y, m)
        labels.append(label)
        rev_data.append(float(s))
        cost_data.append(float(c))
        profit_data.append(float(s - c))

    return render(request, 'financial/report_sales_evolution.html', {
        'period': period,
        'chart_labels_json': json.dumps(labels),
        'chart_rev_json': json.dumps(rev_data),
        'chart_cost_json': json.dumps(cost_data),
        'chart_profit_json': json.dumps(profit_data),
        'total_revenue': sum(rev_data),
        'total_cost': sum(cost_data),
        'total_profit': sum(profit_data),
    })


# ── Compras por Período ───────────────────────────────────────────────────────

@login_required
def report_purchases_period(request):
    company = get_active_company(request)
    today = timezone.now().date()

    year = int(request.GET.get('year', today.year))
    month = request.GET.get('month', '')

    qs = _purchases_qs(company).filter(order_date__year=year)
    if month:
        qs = qs.filter(order_date__month=int(month))

    orders = qs.select_related('supplier').order_by('-order_date')

    total_cost = qs.aggregate(t=Sum('subtotal'))['t'] or Decimal('0.00')
    total_orders = qs.count()

    years = list(range(today.year, today.year - 5, -1))
    months = [(i, MONTH_NAMES[i - 1]) for i in range(1, 13)]

    return render(request, 'financial/report_purchases_period.html', {
        'orders': orders,
        'year': year,
        'month': int(month) if month else '',
        'years': years,
        'months': months,
        'total_cost': total_cost,
        'total_orders': total_orders,
    })


# ── Compras por Fornecedor ────────────────────────────────────────────────────

@login_required
def report_purchases_suppliers(request):
    company = get_active_company(request)
    today = timezone.now().date()

    year = int(request.GET.get('year', today.year))
    month = request.GET.get('month', '')

    qs = _purchases_qs(company).filter(order_date__year=year)
    if month:
        qs = qs.filter(order_date__month=int(month))

    rows = (
        qs
        .values('supplier__id', 'supplier__name')
        .annotate(
            total=Sum('subtotal'),
            order_count=Count('id'),
        )
        .order_by('-total')
    )

    grand_total = qs.aggregate(t=Sum('subtotal'))['t'] or Decimal('0.00')

    years = list(range(today.year, today.year - 5, -1))
    months = [(i, MONTH_NAMES[i - 1]) for i in range(1, 13)]

    return render(request, 'financial/report_purchases_suppliers.html', {
        'rows': rows,
        'year': year,
        'month': int(month) if month else '',
        'years': years,
        'months': months,
        'grand_total': grand_total,
    })


# ── Perdas de Stock ───────────────────────────────────────────────────────────

@login_required
def report_stock_losses(request):
    company = get_active_company(request)
    today = timezone.now().date()

    year = int(request.GET.get('year', today.year))
    month = request.GET.get('month', '')

    qs = StockMovement.objects.filter(
        movement_type='scrap',
        state='done',
    )
    if company:
        qs = qs.filter(owner_company=company)
    qs = qs.filter(date__year=year)
    if month:
        qs = qs.filter(date__month=int(month))

    movements = qs.select_related('partner', 'warehouse', 'responsible').order_by('-date')

    # Compute losses: each scrap line qty × product cost_price
    scrap_lines = (
        StockMovementLine.objects
        .filter(stock_movement__in=qs)
        .select_related('product', 'stock_movement')
    )

    total_qty = sum(float(l.quantity) for l in scrap_lines)
    total_value = sum(float(l.quantity) * float(l.product.cost_price or 0) for l in scrap_lines)

    years = list(range(today.year, today.year - 5, -1))
    months = [(i, MONTH_NAMES[i - 1]) for i in range(1, 13)]

    return render(request, 'financial/report_stock_losses.html', {
        'movements': movements,
        'scrap_lines': scrap_lines,
        'year': year,
        'month': int(month) if month else '',
        'years': years,
        'months': months,
        'total_qty': total_qty,
        'total_value': total_value,
        'movement_count': movements.count(),
    })


# ── Margem por Produto ─────────────────────────────────────────────────────────

@login_required
def report_margins(request):
    company = get_active_company(request)
    today = timezone.now().date()

    year = int(request.GET.get('year', today.year))
    month = request.GET.get('month', '')

    order_filter = Q(
        sale_order__status__in=REVENUE_STATUSES,
        sale_order__order_date__year=year,
    )
    if company:
        order_filter &= Q(sale_order__owner_company=company)
    if month:
        order_filter &= Q(sale_order__order_date__month=int(month))

    lines = (
        SaleOrderLine.objects
        .filter(order_filter)
        .select_related('product')
        .annotate(
            line_val=ExpressionWrapper(
                F('quantity') * F('unit_price') * (1 - F('discount_pct') / Decimal('100')),
                output_field=DecimalField(max_digits=14, decimal_places=4),
            ),
            line_cost=ExpressionWrapper(
                F('quantity') * F('product__cost_price'),
                output_field=DecimalField(max_digits=14, decimal_places=4),
            ),
        )
        .values('product__id', 'product__name', 'product__internal_reference', 'product__cost_price')
        .annotate(
            total_qty=Sum('quantity'),
            total_revenue=Sum('line_val'),
            total_cost=Sum('line_cost'),
        )
        .order_by('-total_revenue')
    )

    result = []
    for r in lines:
        rev = _dec(r['total_revenue'])
        cost = _dec(r['total_cost'])
        profit = rev - cost
        margin = round(float(profit) / float(rev) * 100, 1) if rev else 0
        result.append({
            'product_name': r['product__name'],
            'product_ref': r['product__internal_reference'] or '',
            'cost_price': r['product__cost_price'],
            'total_qty': r['total_qty'],
            'total_revenue': rev,
            'total_cost': cost,
            'profit': profit,
            'margin': margin,
        })

    grand_revenue = sum(_dec(r['total_revenue']) for r in result)
    grand_cost = sum(_dec(r['total_cost']) for r in result)
    grand_profit = grand_revenue - grand_cost
    grand_margin = round(float(grand_profit) / float(grand_revenue) * 100, 1) if grand_revenue else 0

    years = list(range(today.year, today.year - 5, -1))
    months = [(i, MONTH_NAMES[i - 1]) for i in range(1, 13)]

    return render(request, 'financial/report_margins.html', {
        'rows': result,
        'year': year,
        'month': int(month) if month else '',
        'years': years,
        'months': months,
        'grand_revenue': grand_revenue,
        'grand_cost': grand_cost,
        'grand_profit': grand_profit,
        'grand_margin': grand_margin,
    })


# ── Comparativo Anual ─────────────────────────────────────────────────────────

@login_required
def report_annual_comparison(request):
    company = get_active_company(request)
    today = timezone.now().date()

    year_a = int(request.GET.get('year_a', today.year))
    year_b = int(request.GET.get('year_b', today.year - 1))

    rows = []
    for m in range(1, 13):
        sa = _dec(_sales_qs(company).filter(order_date__year=year_a, order_date__month=m).aggregate(t=Sum('subtotal'))['t'])
        ca = _cogs(company, year_a, m)
        sb = _dec(_sales_qs(company).filter(order_date__year=year_b, order_date__month=m).aggregate(t=Sum('subtotal'))['t'])
        cb = _cogs(company, year_b, m)
        pa = sa - ca
        pb = sb - cb
        delta = float(sa - sb)
        delta_pct = round(float(sa - sb) / float(sb) * 100, 1) if sb else None
        rows.append({
            'month': MONTH_NAMES[m - 1],
            'sales_a': sa, 'costs_a': ca, 'profit_a': pa,
            'sales_b': sb, 'costs_b': cb, 'profit_b': pb,
            'delta': delta,
            'delta_pct': delta_pct,
        })

    totals_a_sales = sum(_dec(r['sales_a']) for r in rows)
    totals_b_sales = sum(_dec(r['sales_b']) for r in rows)
    totals_a_profit = sum(_dec(r['profit_a']) for r in rows)
    totals_b_profit = sum(_dec(r['profit_b']) for r in rows)

    chart_labels = json.dumps(MONTH_NAMES)
    chart_a = json.dumps([float(r['sales_a']) for r in rows])
    chart_b = json.dumps([float(r['sales_b']) for r in rows])

    years = list(range(today.year, today.year - 6, -1))

    return render(request, 'financial/report_annual_comparison.html', {
        'rows': rows,
        'year_a': year_a,
        'year_b': year_b,
        'years': years,
        'totals_a_sales': totals_a_sales,
        'totals_b_sales': totals_b_sales,
        'totals_a_profit': totals_a_profit,
        'totals_b_profit': totals_b_profit,
        'chart_labels': chart_labels,
        'chart_a': chart_a,
        'chart_b': chart_b,
    })
