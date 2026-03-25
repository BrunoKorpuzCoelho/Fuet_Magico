import json
import re
import secrets
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from apps.core.models import ChatterMessage, ChatterActivity, ChatterFollower

User = get_user_model()

from apps.core.multi_company import filter_by_company, get_active_company
from .models import SaleOrder, SaleOrderLine, PaymentTerm
from .forms import SaleOrderForm, SaleOrderLineForm, PaymentTermForm


_FIELD_LABELS = {
    'client':         'Cliente',
    'order_date':     'Data',
    'delivery_date':  'Data de Entrega',
    'notes':          'Notas',
    'payment_terms':  'Condição de Pagamento',
}


def _log(order, user, activity_type, description, details=None):
    """Create a ChatterActivity log entry for a SaleOrder."""
    ct = ContentType.objects.get_for_model(SaleOrder)
    ChatterActivity.objects.create(
        content_type=ct,
        object_id=order.pk,
        user=user,
        activity_type=activity_type,
        description=description,
        details=details or {},
    )


def _build_lines_json(order):
    """Serialize SaleOrderLine queryset to JSON string for Alpine.js."""
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


_STATUS_FILTER_OPTIONS = [
    ('all',       'Todas (Activas)',   'bg-gray-400'),
    ('draft',     'Rascunho',          'bg-gray-500'),
    ('confirmed', 'Confirmado',        'bg-yellow-500'),
    ('delivered', 'Entregue',          'bg-blue-500'),
    ('invoiced',  'Faturado',          'bg-green-500'),
    ('cancelled', 'Cancelado',         'bg-red-500'),
    ('archived',  'Arquivados',        'bg-orange-400'),
]


def _parse_order_ids(request):
    try:
        body = json.loads(request.body)
        ids = body.get('order_ids', [])
        if not ids:
            return None, 'Nenhum registo selecionado.'
        return ids, None
    except (json.JSONDecodeError, KeyError):
        return None, 'Pedido inválido.'


# ────────────────────────────────────────────────────────────────────
# Sale Order — Index
# ────────────────────────────────────────────────────────────────────

@login_required
def sale_order_index(request):
    """List sale orders for the active company with search, status filter and pagination."""
    search_query  = request.GET.get('search', '').strip()
    search_field  = request.GET.get('field', 'order_number')
    status_filter = request.GET.get('status', 'all')
    page_number   = request.GET.get('page', 1)

    try:
        page_size = int(request.GET.get('page_size', 50))
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    qs = filter_by_company(
        SaleOrder.objects.select_related('client', 'owner_company'),
        request,
    )

    if status_filter == 'archived':
        qs = qs.filter(is_active=False)
    elif status_filter in ('draft', 'confirmed', 'delivered', 'invoiced', 'cancelled'):
        qs = qs.filter(is_active=True, status=status_filter)
    else:
        qs = qs.filter(is_active=True)

    if search_query:
        field_map = {
            'order_number':  Q(order_number__icontains=search_query),
            'client':        Q(client__name__icontains=search_query),
            'document_type': Q(document_type__icontains=search_query),
            'notes':         Q(notes__icontains=search_query),
        }
        q_filter = field_map.get(search_field)
        if q_filter:
            qs = qs.filter(q_filter)
        else:
            qs = qs.filter(
                Q(order_number__icontains=search_query) |
                Q(client__name__icontains=search_query) |
                Q(notes__icontains=search_query)
            )

    paginator = Paginator(qs, page_size)
    page_obj  = paginator.get_page(page_number)

    return render(request, 'sales/order_list.html', {
        'orders':                page_obj,
        'search_query':          search_query,
        'search_field':          search_field,
        'status_filter':         status_filter,
        'status_filter_options': _STATUS_FILTER_OPTIONS,
        'total_count':           paginator.count,
        'page_size':             page_size,
    })


# ────────────────────────────────────────────────────────────────────
# Sale Order — Create
# ────────────────────────────────────────────────────────────────────

@login_required
def sale_order_create(request):
    """Create a new sale order."""
    company = get_active_company(request)

    # Build payment terms queryset for this company + global
    payment_terms_qs = PaymentTerm.objects.filter(
        Q(owner_company=company) | Q(owner_company__isnull=True),
        is_active=True,
    )

    form = SaleOrderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            order = form.save(commit=False)
            order.owner_company = company
            order.document_type = SaleOrder.DocumentType.QUOTATION  # DRAFT → Orçamento
            order.save()
            _log(order, request.user, 'CREATE', f'Venda {order.order_number} criada.')
        messages.success(request, f'Venda {order.order_number} criada.')
        return redirect('sales:order_edit', pk=order.pk)

    # Pre-select default payment term on GET
    default_pt = payment_terms_qs.filter(is_default=True).first()
    selected_payment_term_id = (
        str(request.POST.get('payment_terms', '')) if request.method == 'POST'
        else (str(default_pt.pk) if default_pt else '')
    )

    return render(request, 'sales/order_form.html', {
        'form':                    form,
        'order':                   None,
        'title':                   'Nova Venda',
        'is_create':               True,
        'lines_json':              '[]',
        'next_ref_preview':        SaleOrder.generate_order_number(),
        'payment_terms_qs':        payment_terms_qs,
        'selected_payment_term_id': selected_payment_term_id,
    })


# ────────────────────────────────────────────────────────────────────
# Sale Order — Edit
# ────────────────────────────────────────────────────────────────────

@login_required
def sale_order_edit(request, pk):
    """Edit (or view) a sale order."""
    order = get_object_or_404(
        filter_by_company(
            SaleOrder.objects.select_related('client', 'owner_company', 'payment_terms')
                      .prefetch_related('lines__product', 'lines__uom'),
            request,
        ),
        pk=pk,
    )

    company = get_active_company(request)
    payment_terms_qs = PaymentTerm.objects.filter(
        Q(owner_company=company) | Q(owner_company__isnull=True),
        is_active=True,
    )

    if order.is_editable:
        form = SaleOrderForm(request.POST or None, instance=order)
        if request.method == 'POST' and form.is_valid():
            with transaction.atomic():
                old_client = order.client.name if order.client else ''
                old_pt     = order.payment_terms.name if order.payment_terms else ''
                old_vals = {
                    'client':        old_client,
                    'order_date':    str(order.order_date or ''),
                    'delivery_date': str(order.delivery_date or ''),
                    'notes':         str(order.notes or ''),
                    'payment_terms': old_pt,
                }
                form.save()
                order.refresh_from_db()
                new_client = order.client.name if order.client else ''
                new_pt     = order.payment_terms.name if order.payment_terms else ''
                new_vals = {
                    'client':        new_client,
                    'order_date':    str(order.order_date or ''),
                    'delivery_date': str(order.delivery_date or ''),
                    'notes':         str(order.notes or ''),
                    'payment_terms': new_pt,
                }
                changes = {
                    _FIELD_LABELS[f]: {'old': old_vals[f], 'new': new_vals[f]}
                    for f in old_vals if old_vals[f] != new_vals[f]
                }
                if changes:
                    _log(order, request.user, 'UPDATE', 'Venda actualizada.', {'changes': changes})
            messages.success(request, 'Venda guardada.')
            return redirect('sales:order_edit', pk=order.pk)
    else:
        form = SaleOrderForm(instance=order)

    selected_payment_term_id = str(order.payment_terms.pk) if order.payment_terms else ''

    # Chatter context
    _ct = ContentType.objects.get_for_model(SaleOrder)
    chatter_activities = ChatterActivity.objects.filter(
        content_type=_ct, object_id=order.id
    ).select_related('user').order_by('-created_at')[:100]

    # Smart button counts
    from apps.inventory.models import StockMovement
    delivery_count = StockMovement.objects.filter(
        origin=order.order_number,
        movement_type='delivery',
    ).count()

    return render(request, 'sales/order_form.html', {
        'form':                    form,
        'order':                   order,
        'title':                   order.order_number,
        'is_create':               False,
        'lines_json':              _build_lines_json(order),
        'next_ref_preview':        None,
        'activities':              chatter_activities,
        'delivery_count':          delivery_count,
        'payment_terms_qs':        payment_terms_qs,
        'amount_paid_raw':         str(order.amount_paid),  # dot-decimal, safe for <input type="number">
        'selected_payment_term_id': selected_payment_term_id,
        'has_smtp':                getattr(getattr(request.user, 'email_config', None), 'has_smtp_configured', False),
        'chatter_contact_email':   order.client.email if order.client else '',
    })


# ────────────────────────────────────────────────────────────────────
# Sale Order — Detail (read-only → redirect to edit)
# ────────────────────────────────────────────────────────────────────

@login_required
def sale_order_detail(request, pk):
    return redirect('sales:order_edit', pk=pk)


# ────────────────────────────────────────────────────────────────────
# Sale Order — Quotation Report (HTML)
# ────────────────────────────────────────────────────────────────────

_PT_MONTHS = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
}


def _html_to_pdf(html_string: str, request=None, header_html: str = '') -> bytes | None:
    """Convert an HTML string to PDF bytes using wkhtmltopdf (via pdfkit).

    Requires wkhtmltopdf to be installed on the system:
      - Windows: https://wkhtmltopdf.org/downloads.html
      - Linux:   sudo apt install wkhtmltopdf

    Args:
        header_html: Complete HTML for the repeating page header (--header-html).

    Returns the PDF bytes on success, or None if conversion fails.
    """
    import sys
    import pdfkit
    from django.conf import settings

    # ── Resolve /static/ URLs to absolute file:// paths ──────────
    # wkhtmltopdf cannot fetch relative URLs like /static/...
    # Use STATICFILES_DIRS[0] in dev, STATIC_ROOT in production.
    static_dir = (
        settings.STATICFILES_DIRS[0]
        if settings.DEBUG and settings.STATICFILES_DIRS
        else settings.STATIC_ROOT
    )
    static_file_base = 'file:///' + str(static_dir).replace('\\', '/')
    # Replace both quoted and unquoted occurrences
    html_string = html_string.replace('/static/', static_file_base + '/')

    # ── Footer HTML for pagination ──────────────────────────────
    footer_html = '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
body { margin: 0; padding: 0 18mm; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; }
</style></head><body>
<table style="width:100%; border-collapse:collapse;">
<tr>
  <td style="border-top:2px solid #dbc693; padding-top:6px; font-size:10px; font-style:italic; color:#7a6e64; letter-spacing:0.3px;">
    Obrigada pela confiança. Com carinho, Fuet Mágico by Daisy
  </td>
  <td style="border-top:2px solid #dbc693; padding-top:6px; font-size:10px; color:#7a6e64; letter-spacing:0.5px; text-align:right; white-space:nowrap;">
    Página <span class="page"></span> de <span class="topage"></span>
  </td>
</tr>
</table>
</body></html>'''

    import tempfile
    import os

    # Write footer HTML to temp file
    footer_tmp = tempfile.NamedTemporaryFile(
        mode='w', suffix='.html', encoding='utf-8', delete=False
    )
    footer_tmp.write(footer_html)
    footer_tmp.close()
    footer_path = footer_tmp.name

    # Write header HTML to temp file (if provided)
    header_path = None
    if header_html:
        header_tmp = tempfile.NamedTemporaryFile(
            mode='w', suffix='.html', encoding='utf-8', delete=False
        )
        header_tmp.write(header_html)
        header_tmp.close()
        header_path = header_tmp.name

    options = {
        'enable-local-file-access': '',
        'print-media-type': '',
        'no-outline': '',
        'quiet': '',
        'page-size': 'A4',
        'margin-top': '32mm' if header_path else '0',
        'margin-bottom': '18mm',
        'margin-left': '0',
        'margin-right': '0',
        'footer-html': footer_path,
        'footer-spacing': '0',
    }
    if header_path:
        options['header-html'] = header_path
        options['header-spacing'] = '0'

    # On Windows the installer doesn't add the binary to PATH automatically.
    # Use explicit path; on Linux wkhtmltopdf is expected to be in PATH.
    config = None
    if sys.platform == 'win32':
        config = pdfkit.configuration(
            wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        )

    # pdfkit.from_string() writes to a temp file using the system default encoding
    # (Windows-1252 on Windows), which garbles UTF-8 characters.
    # Write the temp file ourselves in explicit UTF-8 and use from_file() instead.
    try:
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.html', encoding='utf-8', delete=False
        ) as tmp:
            tmp.write(html_string)
            tmp_path = tmp.name
        try:
            return pdfkit.from_file(tmp_path, False, options=options, configuration=config)
        finally:
            os.unlink(tmp_path)
            os.unlink(footer_path)
            if header_path:
                os.unlink(header_path)
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning('wkhtmltopdf conversion error: %s', exc)
        for p in [footer_path, header_path]:
            if p:
                try:
                    os.unlink(p)
                except OSError:
                    pass
        return None


def _get_logo_base64() -> str:
    """Return the brand logo as a base64 data URI so PDFs have no external dependencies."""
    import base64
    import os
    from django.conf import settings
    static_dir = (
        settings.STATICFILES_DIRS[0]
        if settings.DEBUG and settings.STATICFILES_DIRS
        else settings.STATIC_ROOT
    )
    logo_path = os.path.join(
        str(static_dir), 'brand', 'watermarks', 'black', 'watermark-logo-secondary.png'
    )
    try:
        with open(logo_path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        return f'data:image/png;base64,{data}'
    except Exception:
        return ''


def _fmt_date_pt(d):
    if not d:
        return ''
    return f"{d.day:02d} de {_PT_MONTHS[d.month]} de {d.year}"


@login_required
def sale_order_quotation_report(request, pk):
    order = get_object_or_404(
        filter_by_company(
            SaleOrder.objects.select_related('client', 'owner_company')
                      .prefetch_related('lines__product', 'lines__uom'),
            request,
        ),
        pk=pk,
    )
    from django.templatetags.static import static
    return render(request, 'sales/quotation_report.html', {
        'order':                  order,
        'company':                order.owner_company,
        'lines':                  order.lines.select_related('product', 'uom').order_by('created_at'),
        'order_date_formatted':   _fmt_date_pt(order.order_date),
        'delivery_date_formatted': _fmt_date_pt(order.delivery_date),
        'logo_src':               request.build_absolute_uri(static('brand/watermarks/black/watermark-logo-secondary.png')),
        'pdf_mode':               False,
    })


@login_required
@require_POST
def sale_order_send_quotation(request, pk):
    """Send the quotation by email with the report attached as an HTML file.

    Accepts both multipart/form-data (rich compose modal) and application/json (legacy).
    FormData fields: to_email, subject, body, body_html, cc, bcc, extra_attachments (files).
    """
    import html as _html
    import mimetypes
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile
    from django.template.loader import render_to_string
    from apps.core.email_utils import send_email_for_record

    order = get_object_or_404(
        filter_by_company(
            SaleOrder.objects.select_related('client', 'owner_company')
                     .prefetch_related('lines__product', 'lines__uom'),
            request,
        ),
        pk=pk,
    )

    # ── Generate / refresh signature token ─────────────────────────────
    from django.utils import timezone as tz
    if not order.signature_token:
        order.signature_token = secrets.token_urlsafe(32)
    order.token_expires_at   = tz.now() + timedelta(days=30)
    order.signature_status   = SaleOrder.SignatureStatus.PENDING
    order.save(update_fields=['signature_token', 'token_expires_at', 'signature_status'])

    # ── Parse request (FormData or JSON) ──────────────────────────
    if 'application/json' in (request.content_type or ''):
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'success': False, 'error': 'Pedido inválido.'}, status=400)
        to_email  = (data.get('to_email')  or '').strip()
        subject   = (data.get('subject')   or f'Orçamento {order.order_number}').strip()
        body      = (data.get('body')      or '').strip()
        body_html = (data.get('body_html') or '').strip()
        cc        = (data.get('cc')        or '').strip()
        bcc       = (data.get('bcc')       or '').strip()
        extra_files = []
    else:
        to_email  = (request.POST.get('to_email')  or '').strip()
        subject   = (request.POST.get('subject')   or f'Orçamento {order.order_number}').strip()
        body      = (request.POST.get('body')      or '').strip()
        body_html = (request.POST.get('body_html') or '').strip()
        cc        = (request.POST.get('cc')        or '').strip()
        bcc       = (request.POST.get('bcc')       or '').strip()
        extra_files = request.FILES.getlist('extra_attachments')

    if not to_email:
        return JsonResponse({'success': False, 'error': 'O email do destinatário é obrigatório.'})

    # ── Normalise body / body_html ────────────────────────────────
    if not body_html and body:
        body_html = ''.join(
            f'<p style="margin: 0 0 16px 0;">{_html.escape(para)}</p>'
            for para in body.split('\n') if para.strip()
        )
    if body_html and not body:
        body = re.sub(r'<[^>]+>', '', body_html).strip()

    # ── Auto-attach the quotation as PDF ───────────────────────────
    logo_b64 = _get_logo_base64()
    report_html = render_to_string('sales/quotation_report.html', {
        'order':                   order,
        'company':                 order.owner_company,
        'lines':                   order.lines.select_related('product', 'uom').order_by('created_at'),
        'order_date_formatted':    _fmt_date_pt(order.order_date),
        'delivery_date_formatted': _fmt_date_pt(order.delivery_date),
        'logo_src':                logo_b64,
        'pdf_mode':                True,
    }, request=request)

    # Header HTML for wkhtmltopdf --header-html (repeats on every page)
    header_html = f'''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><style>
body {{ margin: 0; padding: 0 18mm; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; }}
</style></head><body>
<table style="width:100%; border-collapse:collapse;">
<tr>
  <td style="width:110px; vertical-align:middle; padding-bottom:14px; border-bottom:2.5px solid #dbc693;">
    <img src="{logo_b64}" alt="Fuet Mágico" style="height:90px; width:auto; display:block;">
  </td>
  <td style="vertical-align:middle; text-align:center; padding:0 20px 14px; border-bottom:2.5px solid #dbc693;">
    <div style="font-size:11px; color:#7a6e64; font-style:italic; letter-spacing:1px; margin-bottom:5px;">Criações refinadas &amp; irresistíveis</div>
    <div style="font-size:20px; font-weight:600; color:#b89a5a; text-transform:uppercase; letter-spacing:3.5px;">Orçamento de Encomenda</div>
  </td>
  <td style="width:90px; padding-bottom:14px; border-bottom:2.5px solid #dbc693;"></td>
</tr>
</table>
</body></html>'''

    pdf_bytes = _html_to_pdf(report_html, request, header_html=header_html)
    if pdf_bytes:
        attachments = [{
            'filename':  f'orcamento_{order.order_number}.pdf',
            'content':   pdf_bytes,
            'mime_type': 'application/pdf',
        }]
    else:
        # Fallback to HTML if PDF conversion fails
        attachments = [{
            'filename':  f'orcamento_{order.order_number}.html',
            'content':   report_html.encode('utf-8'),
            'mime_type': 'text/html',
        }]

    # ── Save & attach extra uploaded files ────────────────────────
    for f in extra_files:
        rel_path = f'chatter/{order.pk}/{f.name}'
        saved_path = default_storage.save(rel_path, ContentFile(f.read()))
        url = default_storage.url(saved_path)
        mime = mimetypes.guess_type(f.name)[0] or 'application/octet-stream'
        with default_storage.open(saved_path, 'rb') as fp:
            content = fp.read()
        attachments.append({
            'filename':  f.name,
            'url':       url,
            'size':      f.size,
            'mime_type': mime,
            'content':   content,
        })

    result = send_email_for_record(
        user=request.user,
        record=order,
        to_email=to_email,
        subject=subject,
        body=body,
        body_html=body_html or None,
        to_name=order.client.name if order.client else '',
        attachments=attachments,
        cc=cc,
        bcc=bcc,
    )
    return JsonResponse(result)


@login_required
@require_http_methods(['GET'])
def sale_order_quotation_email_compose(request, pk):
    """Return compose data (pre-filled fields + preview HTML) for the email modal."""
    from apps.core.models import EmailTemplate
    from apps.core.email_utils import wrap_email_with_layout
    from django.urls import reverse

    order = get_object_or_404(
        filter_by_company(
            SaleOrder.objects.select_related('client', 'owner_company'),
            request,
        ),
        pk=pk,
    )

    # ── Generate signature token for preview (save if new) ──────────────────
    if not order.signature_token:
        order.signature_token = secrets.token_urlsafe(32)
        order.save(update_fields=['signature_token'])
    sign_url = request.build_absolute_uri(f'/sales/orcamento/{order.signature_token}/')

    client_name  = order.client.name  if order.client else 'Cliente'
    order_number = order.order_number or ''
    subject      = f'Orçamento {order_number}'
    to_email     = order.client.email if order.client else ''

    # Resolve body from the "Envio de Orçamento" email template
    body_html = ''
    tmpl = EmailTemplate.objects.filter(
        module='SALES',
        default_body_path='defaults/sales_quotation.html',
    ).first()
    if tmpl and tmpl.body_html:
        body_html = (
            tmpl.body_html
            .replace('{{1}}', client_name)
            .replace('{{2}}', order_number)
        )

    # ── Append sign CTA to body ──────────────────────────────────────────
    sign_button_html = (
        '<div style="margin: 28px 0; text-align: center;">'
        f'<a href="{sign_url}" target="_blank" '
        'style="display:inline-block; padding: 12px 32px; '
        'background-color:#b89a5a; color:#ffffff; '
        'text-decoration:none; border-radius:6px; '
        'font-size:15px; font-weight:600; letter-spacing:0.5px;">'
        '&#9997;&#65039; Ver e Assinar Or&ccedil;amento'
        '</a></div>'
        f'<p style="margin:8px 0 0 0; text-align:center; font-size:12px; color:#9ca3af;">'
        f'Link v&aacute;lido por 30 dias: <a href="{sign_url}" style="color:#b89a5a;">{sign_url}</a></p>'
    )
    body_html_with_sign = (body_html + sign_button_html) if body_html else sign_button_html

    # Build preview from final body (with sign button) wrapped in email layout
    preview_html = body_html_with_sign
    try:
        preview_html, _ = wrap_email_with_layout(
            body_html=body_html_with_sign,
            user=request.user,
            record=order,
            subject=subject,
        )
    except Exception:
        pass  # fall back to body_html_with_sign

    return JsonResponse({
        'to_email':          to_email,
        'to_name':           client_name,
        'subject':           subject,
        'body_html':         body_html_with_sign,
        'preview_html':      preview_html,
        'sign_url':          sign_url,
        'quotation_url':     request.build_absolute_uri(
            reverse('sales:order_quotation_report', args=[str(pk)])
        ),
        'quotation_filename': f'orcamento_{order_number}.pdf',
    })


# ────────────────────────────────────────────────────────────────────
# Sale Order — State transitions
# ────────────────────────────────────────────────────────────────────

def _auto_confirm_order(order, user=None):
    """
    Confirm a DRAFT SaleOrder programmatically (no request needed).
    Returns (True, movement) on success, (False, reason_str) on failure.
    Called both from sale_order_confirm view and from the signature portal.
    """
    from apps.inventory.models import StockMovement, StockMovementLine, Warehouse

    if order.status != SaleOrder.Status.DRAFT:
        return False, 'not_draft'

    if not order.lines.exists():
        return False, 'no_lines'

    warehouse = (
        Warehouse.objects.filter(owner_company=order.owner_company, is_default=True).first()
        or Warehouse.objects.filter(owner_company=order.owner_company).first()
        or Warehouse.objects.filter(owner_company__isnull=True).first()
    )
    if not warehouse:
        return False, 'no_warehouse'

    so_lines = list(order.lines.select_related('product', 'uom').all())

    with transaction.atomic():
        order.status = SaleOrder.Status.CONFIRMED
        order.document_type = SaleOrder.DocumentType.ORDER
        order.save(update_fields=['status', 'document_type'])

        movement = StockMovement.objects.create(
            movement_type='delivery',
            state='draft',
            warehouse=warehouse,
            partner=order.client,
            origin=order.order_number,
            notes=f'Gerado automaticamente a partir da venda {order.order_number}.',
            responsible=user,
            owner_company=order.owner_company,
        )

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
            for line in so_lines
        ])

        _log(
            order, user, 'STATUS_CHANGE',
            f'Estado alterado: Rascunho → Confirmado (Encomenda). Entrega {movement.reference} criada.',
            {
                'field':        'status',
                'old':          'draft',
                'new':          'confirmed',
                'delivery_ref': movement.reference,
                'delivery_pk':  str(movement.pk),
            },
        )

    return True, movement


@login_required
@require_POST
def sale_order_confirm(request, pk):
    """Confirm a DRAFT sale order → CONFIRMED."""
    order = get_object_or_404(
        filter_by_company(SaleOrder.objects, request), pk=pk
    )

    ok, result = _auto_confirm_order(order, user=request.user)

    if not ok:
        if result == 'not_draft':
            messages.error(request, 'Apenas vendas em rascunho podem ser confirmadas.')
            return redirect('sales:order_detail', pk=order.pk)
        elif result == 'no_lines':
            messages.error(request, 'Não é possível confirmar uma venda sem linhas.')
            return redirect('sales:order_edit', pk=order.pk)
        elif result == 'no_warehouse':
            messages.error(request, 'Não existe nenhum armazém configurado. Cria um armazém antes de confirmar.')
            return redirect('sales:order_edit', pk=order.pk)

    movement = result
    messages.success(
        request,
        f'Venda {order.order_number} confirmada. Entrega {movement.reference} criada em rascunho.',
    )
    return redirect('sales:order_edit', pk=order.pk)


@login_required
@require_POST
def sale_order_deliver(request, pk):
    """Mark a CONFIRMED sale order as DELIVERED."""
    order = get_object_or_404(
        filter_by_company(SaleOrder.objects, request), pk=pk
    )
    if order.status != SaleOrder.Status.CONFIRMED:
        messages.error(request, 'Apenas vendas confirmadas podem ser marcadas como entregues.')
        return redirect('sales:order_detail', pk=order.pk)

    with transaction.atomic():
        order.status = SaleOrder.Status.DELIVERED
        order.save(update_fields=['status'])
        _log(order, request.user, 'STATUS_CHANGE',
             'Estado alterado: Confirmado → Entregue.',
             {'field': 'status', 'old': 'confirmed', 'new': 'delivered'})

    messages.success(request, f'Venda {order.order_number} marcada como entregue.')
    return redirect('sales:order_edit', pk=order.pk)


@login_required
@require_POST
def sale_order_cancel(request, pk):
    """Cancel a sale order (not allowed if already INVOICED)."""
    order = get_object_or_404(
        filter_by_company(SaleOrder.objects, request), pk=pk
    )
    if order.status == SaleOrder.Status.INVOICED:
        messages.error(request, 'Não é possível cancelar uma venda já faturada.')
        return redirect('sales:order_detail', pk=order.pk)
    old_status = order.status
    with transaction.atomic():
        order.status = SaleOrder.Status.CANCELLED
        order.save(update_fields=['status'])
        _log(order, request.user, 'STATUS_CHANGE',
             f'Estado alterado: {old_status} → Cancelado.',
             {'field': 'status', 'old': old_status, 'new': 'cancelled'})

    messages.success(request, f'Venda {order.order_number} cancelada.')
    return redirect('sales:order_edit', pk=order.pk)


# ────────────────────────────────────────────────────────────────────
# Sale Order Line — Add / Remove / Update (AJAX)
# ────────────────────────────────────────────────────────────────────

@login_required
def sale_order_margins(request, pk):
    """Return margin analysis for a sale order as JSON."""
    order = get_object_or_404(
        filter_by_company(SaleOrder.objects, request), pk=pk
    )
    lines = order.lines.select_related('product').all()

    line_data = []
    total_cost = 0
    total_sale = float(order.subtotal or 0)

    for line in lines:
        sale_value = float(line.line_total)
        cost_unit = float(line.product.cost_price or 0) if line.product else 0
        cost_value = cost_unit * float(line.quantity or 0)
        profit = sale_value - cost_value
        margin_pct = (profit / sale_value * 100) if sale_value else 0
        total_cost += cost_value
        line_data.append({
            'product': line.product.name if line.product else '—',
            'quantity': str(line.quantity),
            'unit_price': str(line.unit_price),
            'sale_value': round(sale_value, 2),
            'cost_unit': round(cost_unit, 4),
            'cost_value': round(cost_value, 2),
            'profit': round(profit, 2),
            'margin_pct': round(margin_pct, 1),
        })

    total_profit = total_sale - total_cost
    total_margin_pct = (total_profit / total_sale * 100) if total_sale else 0

    return JsonResponse({
        'order_number': order.order_number,
        'lines': line_data,
        'totals': {
            'sale': round(total_sale, 2),
            'cost': round(total_cost, 2),
            'profit': round(total_profit, 2),
            'margin_pct': round(total_margin_pct, 1),
        },
    })


@login_required
@require_POST
def sale_order_line_add(request, pk):
    """Add a line to a DRAFT sale order (JSON body)."""
    order = get_object_or_404(
        filter_by_company(SaleOrder.objects, request), pk=pk
    )
    if not order.is_editable:
        return JsonResponse({'error': 'Venda não editável.'}, status=400)

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
    unit_price = data.get('unit_price', float(product.sale_price or product.cost_price or 0))
    tax_rate   = data.get('tax_rate', 0)
    discount_pct = data.get('discount_pct', 0)

    with transaction.atomic():
        line = SaleOrderLine.objects.create(
            sale_order=order,
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
                'Produto':     {'old': '', 'new': product.name},
                'Quantidade':  {'old': '', 'new': str(quantity)},
                'Preço Unit.': {'old': '', 'new': str(unit_price)},
            }
        })

    return JsonResponse({
        'success':        True,
        'line_id':        str(line.id),
        'product_name':   line.product.name,
        'quantity':       float(line.quantity),
        'unit_price':     float(line.unit_price),
        'tax_rate':       float(line.tax_rate),
        'line_total':     float(line.line_total),
        'order_subtotal': float(order.subtotal),
        'order_tax':      float(order.tax),
        'order_total':    float(order.total),
    })


@login_required
@require_POST
def sale_order_line_remove(request, pk, line_pk):
    """Remove a line from a DRAFT sale order."""
    order = get_object_or_404(
        filter_by_company(SaleOrder.objects, request), pk=pk
    )
    if not order.is_editable:
        return JsonResponse({'error': 'Venda não editável.'}, status=400)

    line = get_object_or_404(SaleOrderLine, pk=line_pk, sale_order=order)
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
def sale_order_line_update(request, pk, line_pk):
    """Update qty/price/tax of an existing DRAFT line (JSON body)."""
    order = get_object_or_404(
        filter_by_company(SaleOrder.objects, request), pk=pk
    )
    if not order.is_editable:
        return JsonResponse({'error': 'Venda não editável.'}, status=400)

    line = get_object_or_404(SaleOrderLine, pk=line_pk, sale_order=order)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido.'}, status=400)

    old_qty   = float(line.quantity)
    old_price = float(line.unit_price)
    old_tax   = float(line.tax_rate)
    old_discount = float(line.discount_pct)

    if 'quantity'    in data: line.quantity    = data['quantity']
    if 'unit_price'  in data: line.unit_price  = data['unit_price']
    if 'tax_rate'    in data: line.tax_rate    = data['tax_rate']
    if 'discount_pct' in data: line.discount_pct = data['discount_pct']
    if 'uom_id'      in data and data['uom_id']: line.uom_id = data['uom_id']

    with transaction.atomic():
        line.save()
        order.recalculate_totals()
        line_changes = {}
        if old_qty   != float(line.quantity):   line_changes['Quantidade']  = {'old': str(old_qty),   'new': str(float(line.quantity))}
        if old_price != float(line.unit_price): line_changes['Preço Unit.'] = {'old': str(old_price), 'new': str(float(line.unit_price))}
        if old_tax   != float(line.tax_rate):   line_changes['IVA %']       = {'old': str(old_tax),   'new': str(float(line.tax_rate))}
        if old_discount != float(line.discount_pct): line_changes['Desconto %'] = {'old': str(old_discount), 'new': str(float(line.discount_pct))}
        if line_changes:
            product_name = line.product.name if line.product else ''
            _log(order, request.user, 'UPDATE', f'Linha actualizada: {product_name}', {'changes': line_changes})

    return JsonResponse({
        'success': True,
        'line': {'id': str(line.pk), 'line_total': float(line.line_total)},
        'order_subtotal': float(order.subtotal),
        'order_tax':      float(order.tax),
        'order_total':    float(order.total),
    })


# ────────────────────────────────────────────────────────────────────
# Sale Order — Bulk Actions
# ────────────────────────────────────────────────────────────────────

@login_required
@require_POST
def sale_order_bulk_archive(request):
    ids, err = _parse_order_ids(request)
    if err:
        return JsonResponse({'success': False, 'error': err}, status=400)
    qs = filter_by_company(SaleOrder.objects, request).filter(pk__in=ids, is_active=True)
    updated = qs.update(is_active=False)
    return JsonResponse({'success': True, 'message': f'{updated} venda(s) arquivada(s).', 'updated': updated})


@login_required
@require_POST
def sale_order_bulk_unarchive(request):
    ids, err = _parse_order_ids(request)
    if err:
        return JsonResponse({'success': False, 'error': err}, status=400)
    qs = filter_by_company(SaleOrder.objects, request).filter(pk__in=ids, is_active=False)
    updated = qs.update(is_active=True)
    return JsonResponse({'success': True, 'message': f'{updated} venda(s) desarquivada(s).', 'updated': updated})


@login_required
@require_POST
def sale_order_bulk_delete(request):
    if getattr(request.user, 'role', None) != 'ADMIN':
        return JsonResponse({'success': False, 'error': 'Apenas administradores podem eliminar vendas.'}, status=403)
    ids, err = _parse_order_ids(request)
    if err:
        return JsonResponse({'success': False, 'error': err}, status=400)
    qs = filter_by_company(SaleOrder.objects, request).filter(pk__in=ids)
    count = qs.count()
    qs.delete()
    return JsonResponse({'success': True, 'message': f'{count} venda(s) eliminada(s) permanentemente.', 'deleted': count})


# ────────────────────────────────────────────────────────────────────
# Chatter — Notes & Followers
# ────────────────────────────────────────────────────────────────────

def _so_note_to_dict(n):
    author = n.author
    name = author.get_full_name() or author.username if author else 'Sistema'
    initials = ''.join(p[0].upper() for p in name.split()[:2])
    return {
        'id':           str(n.id),
        'author':       name,
        'author_initials': initials,
        'content':      n.body,
        'created_at':   n.created_at.strftime('%d/%m/%Y %H:%M'),
    }


@login_required
@require_http_methods(['GET'])
def sale_order_notes_list(request, pk):
    """GET /vendas/<pk>/notes/"""
    order = get_object_or_404(SaleOrder, pk=pk)
    ct = ContentType.objects.get_for_model(SaleOrder)
    notes = (
        ChatterMessage.objects
        .filter(content_type=ct, object_id=order.id, message_type='NOTE')
        .select_related('author')
        .order_by('-created_at')[:100]
    )
    return JsonResponse({'notes': [_so_note_to_dict(n) for n in notes]})


@login_required
@require_http_methods(['POST'])
def sale_order_note_create(request, pk):
    """POST /vendas/<pk>/notes/create/"""
    order = get_object_or_404(SaleOrder, pk=pk)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    content = data.get('content', '').strip()
    if not content:
        return JsonResponse({'success': False, 'error': 'Conteúdo não pode estar vazio.'}, status=400)

    urgent = bool(data.get('urgent', False))
    ct = ContentType.objects.get_for_model(SaleOrder)
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
                    message=f'Venda: {order.order_number}',
                    link=f'/sales/{str(order.id)}/edit/',
                    related_object_id=note.id,
                    is_urgent=urgent,
                )
        except Exception:
            pass

    return JsonResponse({'success': True, 'note': _so_note_to_dict(note)}, status=201)


@login_required
@require_http_methods(['GET', 'POST'])
def sale_order_followers_api(request, pk):
    """GET/POST /vendas/<pk>/followers/"""
    order = get_object_or_404(SaleOrder, pk=pk)
    ct = ContentType.objects.get_for_model(SaleOrder)

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
                    'user_id':  str(f.user.id),
                    'display':  f.user.get_full_name() or f.user.username,
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
def sale_order_follower_remove(request, pk, user_id):
    """DELETE /vendas/<pk>/followers/<user_id>/remove/"""
    order = get_object_or_404(SaleOrder, pk=pk)
    ct = ContentType.objects.get_for_model(SaleOrder)
    ChatterFollower.objects.filter(
        content_type=ct, object_id=order.id, user_id=user_id,
    ).delete()
    return JsonResponse({'success': True})


# ────────────────────────────────────────────────────────────────────
# Signature Portal — public views (no @login_required)
# ────────────────────────────────────────────────────────────────────

def quotation_sign(request, token):
    """Public GET: render the quotation signature page for the client."""
    from django.utils import timezone as tz

    try:
        order = (
            SaleOrder.objects
            .select_related('client', 'owner_company')
            .prefetch_related('lines__product', 'lines__uom')
            .get(signature_token=token)
        )
    except SaleOrder.DoesNotExist:
        return render(request, 'sales/quotation_sign_expired.html', {
            'reason': 'not_found',
        }, status=404)

    # Token expired?
    if order.token_expires_at and tz.now() > order.token_expires_at:
        return render(request, 'sales/quotation_sign_expired.html', {
            'reason': 'expired',
            'order':  order,
        }, status=410)

    # Already signed or refused?
    already_done = order.signature_status in (
        SaleOrder.SignatureStatus.SIGNED,
        SaleOrder.SignatureStatus.REFUSED,
    )

    lines = order.lines.select_related('product', 'uom').order_by('created_at')
    return render(request, 'sales/quotation_sign.html', {
        'order':        order,
        'company':      order.owner_company,
        'lines':        lines,
        'token':        token,
        'already_done': already_done,
    })


@csrf_exempt
@require_POST
def quotation_sign_submit(request, token):
    """Public POST: save the client signature (sign or refuse)."""
    from django.utils import timezone as tz
    from django.contrib.contenttypes.models import ContentType

    try:
        order = SaleOrder.objects.select_related('client', 'owner_company').get(
            signature_token=token
        )
    except SaleOrder.DoesNotExist:
        return render(request, 'sales/quotation_sign_expired.html', {
            'reason': 'not_found',
        }, status=404)

    # Token expired?
    if order.token_expires_at and tz.now() > order.token_expires_at:
        return render(request, 'sales/quotation_sign_expired.html', {
            'reason': 'expired',
            'order':  order,
        }, status=410)

    # Already actioned — idempotent, just redirect to done
    if order.signature_status in (
        SaleOrder.SignatureStatus.SIGNED,
        SaleOrder.SignatureStatus.REFUSED,
    ):
        return redirect('sales:quotation_sign_done', token=token)

    action       = request.POST.get('action', '').strip()       # 'sign' | 'refuse'
    signer_name  = request.POST.get('signer_name', '').strip()
    signature_data = request.POST.get('signature_data', '').strip()  # base64 PNG

    if action not in ('sign', 'refuse'):
        return redirect('sales:quotation_sign', token=token)

    now = tz.now()
    ct  = ContentType.objects.get_for_model(SaleOrder)

    if action == 'sign':
        if not signer_name:
            return redirect('sales:quotation_sign', token=token)

        order.signature_status = SaleOrder.SignatureStatus.SIGNED
        order.signed_at        = now
        order.signed_by_name   = signer_name
        order.signature_image  = signature_data
        order.save(update_fields=[
            'signature_status', 'signed_at', 'signed_by_name', 'signature_image',
        ])

        sig_html = ''
        if signature_data:
            sig_html = (
                f'<br><img src="{signature_data}" alt="Assinatura" '
                'style="max-height:80px; border:1px solid #dbc693; border-radius:4px; '
                'margin-top:8px; display:block;">'
            )
        chatter_body_html = (
            f'<p style="margin:0;">&#9989; <strong>Or&ccedil;amento aceite e assinado</strong> '
            f'por <em>{signer_name}</em> em {now.strftime("%d/%m/%Y %H:%M")}.</p>'
            f'{sig_html}'
        )
        ChatterMessage.objects.create(
            content_type=ct,
            object_id=order.pk,
            author=None,
            message_type='EMAIL',
            subject=f'Assinatura — {order.order_number}',
            body=f'Orçamento aceite e assinado por {signer_name} em {now.strftime("%d/%m/%Y %H:%M")}.',
            body_html=chatter_body_html,
            from_email=order.client.email if order.client else '',
            to_email='',
            direction=ChatterMessage.DIRECTION_INBOUND,
            sent_at=now,
            is_internal=False,
        )

        # Auto-confirm: trigger the same flow as the "Confirmar" button
        ok, result = _auto_confirm_order(order, user=None)
        if ok:
            movement = result
            ChatterMessage.objects.create(
                content_type=ct,
                object_id=order.pk,
                author=None,
                message_type='NOTE',
                subject=f'Encomenda confirmada — {order.order_number}',
                body=f'Encomenda confirmada automaticamente após assinatura do cliente. Entrega {movement.reference} criada.',
                body_html=(
                    f'<p style="margin:0;">&#128230; <strong>Encomenda confirmada automaticamente</strong> '
                    f'após assinatura do cliente. Entrega <strong>{movement.reference}</strong> criada em rascunho.</p>'
                ),
                from_email='',
                to_email='',
                direction=ChatterMessage.DIRECTION_INBOUND,
                sent_at=now,
                is_internal=True,
            )

    else:  # refuse
        order.signature_status = SaleOrder.SignatureStatus.REFUSED
        order.signed_at        = now
        order.signed_by_name   = signer_name
        order.save(update_fields=['signature_status', 'signed_at', 'signed_by_name'])

        ChatterMessage.objects.create(
            content_type=ct,
            object_id=order.pk,
            author=None,
            message_type='EMAIL',
            subject=f'Or\u00e7amento recusado — {order.order_number}',
            body=f'Orçamento recusado por {signer_name or "o cliente"} em {now.strftime("%d/%m/%Y %H:%M")}.',
            body_html=(
                f'<p style="margin:0;">&#10060; <strong>Or&ccedil;amento recusado</strong> '
                f'por <em>{signer_name or "o cliente"}</em> em {now.strftime("%d/%m/%Y %H:%M")}.</p>'
            ),
            from_email=order.client.email if order.client else '',
            to_email='',
            direction=ChatterMessage.DIRECTION_INBOUND,
            sent_at=now,
            is_internal=False,
        )

    return redirect('sales:quotation_sign_done', token=token)


def quotation_sign_done(request, token):
    """Public GET: confirmation page after signing or refusing."""
    try:
        order = SaleOrder.objects.select_related('client', 'owner_company').get(
            signature_token=token
        )
    except SaleOrder.DoesNotExist:
        return render(request, 'sales/quotation_sign_expired.html', {
            'reason': 'not_found',
        }, status=404)

    return render(request, 'sales/quotation_sign_done.html', {
        'order':   order,
        'company': order.owner_company,
    })


def quotation_terms(request):
    """Public GET: terms and conditions for digital signature."""
    return render(request, 'sales/quotation_terms.html')


_STATUS_FILTER_OPTIONS = [
    ('all',       'Todas (Activas)',   'bg-gray-400'),
    ('draft',     'Rascunho',          'bg-gray-500'),
    ('confirmed', 'Confirmado',        'bg-yellow-500'),
    ('delivered', 'Entregue',          'bg-blue-500'),
    ('invoiced',  'Faturado',          'bg-green-500'),
    ('cancelled', 'Cancelado',         'bg-red-500'),
    ('archived',  'Arquivados',        'bg-orange-400'),
]


def _parse_order_ids(request):
    try:
        body = json.loads(request.body)
        ids = body.get('order_ids', [])
        if not ids:
            return None, 'Nenhum registo selecionado.'
        return ids, None
    except (json.JSONDecodeError, KeyError):
        return None, 'Pedido inválido.'


# ────────────────────────────────────────────────────────────────────
# Sale Order — Index
# ────────────────────────────────────────────────────────────────────

@login_required
def sale_order_index(request):
    """List sale orders for the active company with search, status filter and pagination."""
    search_query  = request.GET.get('search', '').strip()
    search_field  = request.GET.get('field', 'order_number')
    status_filter = request.GET.get('status', 'all')
    page_number   = request.GET.get('page', 1)

    try:
        page_size = int(request.GET.get('page_size', 50))
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    qs = filter_by_company(
        SaleOrder.objects.select_related('client', 'owner_company'),
        request,
    )

    # is_active / status filtering
    if status_filter == 'archived':
        qs = qs.filter(is_active=False)
    elif status_filter in ('draft', 'confirmed', 'delivered', 'invoiced', 'cancelled'):
        qs = qs.filter(is_active=True, status=status_filter)
    else:
        qs = qs.filter(is_active=True)

    # Search
    if search_query:
        field_map = {
            'order_number': Q(order_number__icontains=search_query),
            'client':       Q(client__name__icontains=search_query),
            'document_type': Q(document_type__icontains=search_query),
            'notes':        Q(notes__icontains=search_query),
        }
        q_filter = field_map.get(search_field)
        if q_filter:
            qs = qs.filter(q_filter)
        else:
            qs = qs.filter(
                Q(order_number__icontains=search_query) |
                Q(client__name__icontains=search_query) |
                Q(notes__icontains=search_query)
            )

    paginator = Paginator(qs, page_size)
    page_obj  = paginator.get_page(page_number)

    return render(request, 'sales/order_list.html', {
        'orders':               page_obj,
        'search_query':         search_query,
        'search_field':         search_field,
        'status_filter':        status_filter,
        'status_filter_options': _STATUS_FILTER_OPTIONS,
        'total_count':          paginator.count,
        'page_size':            page_size,
    })


# ────────────────────────────────────────────────────────────────────
# Sale Order — Bulk Actions
# ────────────────────────────────────────────────────────────────────

@login_required
@require_POST
def sale_order_bulk_archive(request):
    ids, err = _parse_order_ids(request)
    if err:
        return JsonResponse({'success': False, 'error': err}, status=400)
    qs = filter_by_company(SaleOrder.objects, request).filter(pk__in=ids, is_active=True)
    updated = qs.update(is_active=False)
    return JsonResponse({'success': True, 'message': f'{updated} venda(s) arquivada(s).', 'updated': updated})


@login_required
@require_POST
def sale_order_bulk_unarchive(request):
    ids, err = _parse_order_ids(request)
    if err:
        return JsonResponse({'success': False, 'error': err}, status=400)
    qs = filter_by_company(SaleOrder.objects, request).filter(pk__in=ids, is_active=False)
    updated = qs.update(is_active=True)
    return JsonResponse({'success': True, 'message': f'{updated} venda(s) desarquivada(s).', 'updated': updated})


@login_required
@require_POST
def sale_order_bulk_delete(request):
    if getattr(request.user, 'role', None) != 'ADMIN':
        return JsonResponse({'success': False, 'error': 'Apenas administradores podem eliminar vendas.'}, status=403)
    ids, err = _parse_order_ids(request)
    if err:
        return JsonResponse({'success': False, 'error': err}, status=400)
    qs = filter_by_company(SaleOrder.objects, request).filter(pk__in=ids)
    count = qs.count()
    qs.delete()
    return JsonResponse({'success': True, 'message': f'{count} venda(s) eliminada(s) permanentemente.', 'deleted': count})


# ──────────────────────────────────────────────────────────────────
# Payment Terms — CRUD
# ──────────────────────────────────────────────────────────────────


@login_required
def sale_reports(request):
    """
    Página de Relatórios de Vendas — 6 gráficos profissionais com Chart.js.
    Funil de Vendas | Vendas Mensais | Top Clientes | Previsão | Tipo Documento | Estado Pagamento
    """
    from dateutil.relativedelta import relativedelta
    from django.db.models import Count, Sum, Avg, Q
    from django.utils import timezone

    active_company = get_active_company(request)
    now = timezone.now()

    def base_qs():
        qs = SaleOrder.objects.all()
        if active_company:
            qs = qs.filter(owner_company=active_company)
        return qs

    # ── KPI Cards ──────────────────────────────────────────────────
    kpi_in_progress = base_qs().filter(
        status__in=[SaleOrder.Status.CONFIRMED, SaleOrder.Status.DELIVERED]
    ).count()

    kpi_invoiced_month = base_qs().filter(
        status=SaleOrder.Status.INVOICED,
        order_date__year=now.year, order_date__month=now.month,
    ).count()

    kpi_revenue_month = base_qs().filter(
        status__in=[SaleOrder.Status.CONFIRMED, SaleOrder.Status.DELIVERED, SaleOrder.Status.INVOICED],
        order_date__year=now.year, order_date__month=now.month,
    ).aggregate(v=Sum('total'))['v'] or 0

    ticket_medio_raw = base_qs().filter(
        status__in=[SaleOrder.Status.CONFIRMED, SaleOrder.Status.DELIVERED, SaleOrder.Status.INVOICED]
    ).aggregate(v=Avg('total'))['v'] or 0
    kpi_ticket_medio = round(float(ticket_medio_raw), 2)

    # ── 1. Funil de Vendas (por estado) ────────────────────────────
    funnel_statuses = ['draft', 'confirmed', 'delivered', 'invoiced']
    funnel_display  = ['Rascunho', 'Confirmada', 'Entregue', 'Faturada']
    funnel_counts = []
    funnel_values = []
    for s in funnel_statuses:
        agg = base_qs().filter(status=s).aggregate(cnt=Count('id'), val=Sum('total'))
        funnel_counts.append(agg['cnt'] or 0)
        funnel_values.append(float(agg['val'] or 0))

    # ── 2. Vendas Mensais (últimos 12 meses) ───────────────────────
    monthly_labels    = []
    monthly_active    = []   # confirmed + delivered + invoiced
    monthly_cancelled = []
    monthly_revenue   = []
    for i in range(11, -1, -1):
        d = now - relativedelta(months=i)
        monthly_labels.append(d.strftime('%b %Y'))
        active_cnt = base_qs().filter(
            status__in=['confirmed', 'delivered', 'invoiced'],
            order_date__year=d.year, order_date__month=d.month,
        ).count()
        cancelled_cnt = base_qs().filter(
            status='cancelled',
            order_date__year=d.year, order_date__month=d.month,
        ).count()
        rev = base_qs().filter(
            status__in=['confirmed', 'delivered', 'invoiced'],
            order_date__year=d.year, order_date__month=d.month,
        ).aggregate(v=Sum('total'))['v'] or 0
        monthly_active.append(active_cnt)
        monthly_cancelled.append(cancelled_cnt)
        monthly_revenue.append(float(rev))

    # ── 3. Top Clientes (top 8 por receita) ────────────────────────
    top_clients_qs = (
        base_qs()
        .filter(client__isnull=False, status__in=['confirmed', 'delivered', 'invoiced'])
        .values('client__name')
        .annotate(
            total_orders=Count('id'),
            total_revenue=Sum('total'),
            invoiced_cnt=Count('id', filter=Q(status='invoiced')),
        )
        .order_by('-total_revenue')[:8]
    )
    client_labels   = [r['client__name'] or 'Sem nome' for r in top_clients_qs]
    client_orders   = [r['total_orders'] for r in top_clients_qs]
    client_revenue  = [float(r['total_revenue'] or 0) for r in top_clients_qs]
    client_invoiced = [r['invoiced_cnt'] for r in top_clients_qs]

    # ── 4. Previsão de Receita (próximos 6 meses) ──────────────────
    forecast_labels    = []
    forecast_expected  = []
    forecast_confirmed = []
    for i in range(0, 6):
        d = now + relativedelta(months=i)
        forecast_labels.append(d.strftime('%b %Y'))
        agg_all = base_qs().filter(
            status__in=['confirmed', 'delivered', 'invoiced'],
            delivery_date__year=d.year, delivery_date__month=d.month,
        ).aggregate(v=Sum('total'))
        agg_conf = base_qs().filter(
            status='confirmed',
            delivery_date__year=d.year, delivery_date__month=d.month,
        ).aggregate(v=Sum('total'))
        forecast_expected.append(float(agg_all['v'] or 0))
        forecast_confirmed.append(float(agg_conf['v'] or 0))

    # ── 5. Análise por Tipo de Documento ───────────────────────────
    DOC_LABELS = {'quotation': 'Orçamento', 'order': 'Encomenda', 'invoice': 'Fatura'}
    doc_data = (
        base_qs()
        .values('document_type')
        .annotate(cnt=Count('id'), revenue=Sum('total'))
        .order_by('-cnt')
    )
    doc_labels  = [DOC_LABELS.get(r['document_type'], r['document_type']) for r in doc_data]
    doc_counts  = [r['cnt'] for r in doc_data]
    doc_revenue = [float(r['revenue'] or 0) for r in doc_data]

    # ── 6. Estado de Pagamento ─────────────────────────────────────
    PAY_LABELS = {'unpaid': 'Não Pago', 'partial': 'Parcial', 'paid': 'Pago'}
    pay_data = (
        base_qs()
        .filter(status__in=['confirmed', 'delivered', 'invoiced'])
        .values('payment_status')
        .annotate(cnt=Count('id'), val=Sum('total'))
        .order_by('-val')
    )
    pay_labels = [PAY_LABELS.get(r['payment_status'], r['payment_status']) for r in pay_data]
    pay_counts = [r['cnt'] for r in pay_data]
    pay_values = [float(r['val'] or 0) for r in pay_data]

    context = {
        # KPIs
        'kpi_in_progress':   kpi_in_progress,
        'kpi_invoiced_month': kpi_invoiced_month,
        'kpi_revenue_month': kpi_revenue_month,
        'kpi_ticket_medio':  kpi_ticket_medio,
        # Chart JSON
        'funnel_labels_json':     json.dumps(funnel_display),
        'funnel_counts_json':     json.dumps(funnel_counts),
        'funnel_values_json':     json.dumps(funnel_values),
        'monthly_labels_json':    json.dumps(monthly_labels),
        'monthly_active_json':    json.dumps(monthly_active),
        'monthly_cancelled_json': json.dumps(monthly_cancelled),
        'monthly_revenue_json':   json.dumps(monthly_revenue),
        'client_labels_json':     json.dumps(client_labels),
        'client_orders_json':     json.dumps(client_orders),
        'client_revenue_json':    json.dumps(client_revenue),
        'client_invoiced_json':   json.dumps(client_invoiced),
        'forecast_labels_json':   json.dumps(forecast_labels),
        'forecast_expected_json': json.dumps(forecast_expected),
        'forecast_confirmed_json':json.dumps(forecast_confirmed),
        'doc_labels_json':        json.dumps(doc_labels),
        'doc_counts_json':        json.dumps(doc_counts),
        'doc_revenue_json':       json.dumps(doc_revenue),
        'pay_labels_json':        json.dumps(pay_labels),
        'pay_counts_json':        json.dumps(pay_counts),
        'pay_values_json':        json.dumps(pay_values),
    }

    return render(request, 'sales/reports.html', context)


# ──────────────────────────────────────────────────────────────────

@login_required
def payment_term_list(request):
    """List payment terms with search and pagination."""
    company = get_active_company(request)
    search_query = request.GET.get('search', '').strip()
    active_filter = request.GET.get('active', '')
    page_size = max(1, int(request.GET.get('page_size', 50) or 50))

    qs = PaymentTerm.objects.filter(
        Q(owner_company=company) | Q(owner_company__isnull=True)
    )

    if active_filter == '1':
        qs = qs.filter(is_active=True)
    elif active_filter == '0':
        qs = qs.filter(is_active=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    total_count = qs.count()
    from django.core.paginator import Paginator
    paginator = Paginator(qs, page_size)
    page_number = request.GET.get('page', 1)
    payment_terms_page = paginator.get_page(page_number)

    return render(request, 'sales/payment_term_list.html', {
        'payment_terms': payment_terms_page,
        'search_query':  search_query,
        'active_filter': active_filter,
        'total_count':   total_count,
        'page_size':     page_size,
    })


@login_required
def payment_term_create(request):
    """Create a new payment term."""
    company = get_active_company(request)
    form = PaymentTermForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        pt = form.save(commit=False)
        pt.owner_company = company
        pt.save()
        messages.success(request, f'Condicao de pagamento "{pt.name}" criada.')
        return redirect('sales:payment_term_list')

    return render(request, 'sales/payment_term_form.html', {
        'form':    form,
        'editing': None,
    })


@login_required
def payment_term_edit(request, pk):
    """Edit an existing payment term."""
    pt = get_object_or_404(PaymentTerm, pk=pk)
    form = PaymentTermForm(request.POST or None, instance=pt)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Condicao de pagamento "{pt.name}" actualizada.')
        return redirect('sales:payment_term_list')

    return render(request, 'sales/payment_term_form.html', {
        'form':    form,
        'editing': pt,
    })


@login_required
@require_POST
def payment_term_toggle(request, pk):
    """Toggle active/inactive on a payment term."""
    pt = get_object_or_404(PaymentTerm, pk=pk)
    pt.is_active = not pt.is_active
    pt.save(update_fields=['is_active'])
    state = 'activada' if pt.is_active else 'desactivada'
    messages.success(request, f'"{pt.name}" {state}.')
    return redirect('sales:payment_term_list')


@login_required
@require_POST
def payment_term_delete(request, pk):
    """Delete a payment term only if no sale orders reference it."""
    pt = get_object_or_404(PaymentTerm, pk=pk)
    if pt.sale_orders.exists():
        messages.error(request, f'Nao e possivel eliminar "{pt.name}" - esta associada a vendas.')
    else:
        name = pt.name
        pt.delete()
        messages.success(request, f'"{name}" eliminada.')
    return redirect('sales:payment_term_list')


@login_required
@require_POST
def payment_term_bulk_activate(request):
    try:
        data = json.loads(request.body)
        ids = data.get('term_ids', [])
        count = PaymentTerm.objects.filter(pk__in=ids).update(is_active=True)
        return JsonResponse({'success': True, 'message': f'{count} condicao(oes) activada(s).'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def payment_term_bulk_deactivate(request):
    try:
        data = json.loads(request.body)
        ids = data.get('term_ids', [])
        count = PaymentTerm.objects.filter(pk__in=ids).update(is_active=False)
        return JsonResponse({'success': True, 'message': f'{count} condicao(oes) desactivada(s).'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def payment_term_bulk_delete(request):
    try:
        data = json.loads(request.body)
        ids = data.get('term_ids', [])
        qs = PaymentTerm.objects.filter(pk__in=ids)
        blocked = [pt.name for pt in qs if pt.sale_orders.exists()]
        deletable = qs.exclude(pk__in=[pt.pk for pt in qs if pt.sale_orders.exists()])
        count = deletable.count()
        deletable.delete()
        if blocked:
            return JsonResponse({
                'success': True,
                'message': f'{count} eliminada(s).',
                'warning': f'Nao foi possivel eliminar: {", ".join(blocked)} (tem vendas associadas).',
            })
        return JsonResponse({'success': True, 'message': f'{count} condicao(oes) eliminada(s).'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
