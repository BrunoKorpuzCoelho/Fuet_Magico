from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from .models import UserSettings, Notification


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from .models import UserSettings, Notification
from apps.accounts.models import AppRole

# Mapa slug -> definição visual da app no dashboard
_APP_TILES = [
    {'slug': 'crm',       'name': 'CRM',          'icon': '🤝', 'url_name': 'crm:crm_home'},
    {'slug': 'contacts',  'name': 'Contactos',     'icon': '👥', 'url_name': None, 'url': '/contacts/'},
    {'slug': 'inventory', 'name': 'Inventário',    'icon': '📦', 'url_name': None, 'url': '#'},
    {'slug': 'purchases', 'name': 'Compras',       'icon': '🛒', 'url_name': None, 'url': '#'},
    {'slug': 'sales',     'name': 'Vendas',        'icon': '💰', 'url_name': None, 'url': '#'},
    {'slug': 'website',   'name': 'Website',       'icon': '🌐', 'url_name': None, 'url': '/'},
    {'slug': 'financial', 'name': 'Financeiro',    'icon': '💳', 'url_name': None, 'url': '#'},
    {'slug': 'bom',       'name': 'BOM',           'icon': '🎂', 'url_name': None, 'url': '#'},
    {'slug': 'documents', 'name': 'Documentos',    'icon': '📄', 'url_name': None, 'url': '#'},
    {'slug': 'marketing', 'name': 'Marketing',     'icon': '📱', 'url_name': None, 'url': '#'},
    {'slug': 'reports',   'name': 'Relatórios',    'icon': '📊', 'url_name': None, 'url': '#'},
]


@login_required
def dashboard_view(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    unread_count = Notification.get_unread_count(request.user)

    # --- Filtrar apps por AppRole na empresa ativa ---
    # Global ADMIN vê sempre tudo; os restantes só vêem apps onde têm acesso
    is_global_admin = (request.user.role == 'ADMIN')
    active_company_id = request.session.get('active_company_id')

    if is_global_admin:
        allowed_slugs = {tile['slug'] for tile in _APP_TILES}
    elif active_company_id:
        allowed_slugs = set(
            AppRole.objects.filter(
                user=request.user,
                company_id=active_company_id,
            ).values_list('app', flat=True)
        )
    else:
        allowed_slugs = set()

    apps = []
    for tile in _APP_TILES:
        if tile['slug'] not in allowed_slugs:
            continue
        url = tile.get('url') or ''
        if tile.get('url_name'):
            try:
                url = reverse(tile['url_name'])
            except Exception:
                url = '#'
        apps.append({'name': tile['name'], 'icon': tile['icon'], 'url': url})

    # Tile de Configurações do sistema — só para ADMIN global
    if is_global_admin:
        apps.append({'name': 'Configurações', 'icon': '⚙️', 'url': reverse('dashboard:settings')})

    context = {
        'apps': apps,
        'user_settings': user_settings,
        'unread_count': unread_count,
    }

    return render(request, 'dashboard/index.html', context)


@login_required
@csrf_exempt
def toggle_dark_mode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)
        user_settings.dark_mode = data.get('dark_mode', False)
        user_settings.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
@csrf_exempt
def toggle_developer_mode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)
        user_settings.developer_mode = data.get('developer_mode', False)
        user_settings.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


from apps.accounts.decorators import admin_required
from apps.core.models import Company
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

@admin_required
@require_http_methods(['GET', 'POST'])
def settings_view(request):
    """Página de configurações gerais do sistema (ADMIN only)."""
    # Usa a empresa ativa da sessão ou a primeira disponível
    active_company_id = request.session.get('active_company_id')
    if active_company_id:
        company = Company.objects.filter(pk=active_company_id).first()
    else:
        company = Company.objects.order_by('name').first()

    # ── Preview AJAX ─────────────────────────────────────────────────────────
    if request.method == 'GET' and request.GET.get('action') == 'crm_leads_preview':
        from apps.crm.services import get_eligible_contacts
        from apps.crm.models import CRMConfig
        if not company:
            return JsonResponse({'eligible': 0, 'windows': []})
        try:
            years = max(1, min(10, int(request.GET.get('years', 3))))
        except (ValueError, TypeError):
            years = 3
        eligible = get_eligible_contacts(company, years)
        # Calcular janelas para mostrar no modal
        from apps.crm.services import _seasonal_windows
        windows = [
            {'year': i + 1, 'start': str(s), 'end': str(e)}
            for i, (s, e) in enumerate(_seasonal_windows(years))
        ]
        return JsonResponse({'eligible': len(eligible), 'years': years, 'windows': windows})
    # ─────────────────────────────────────────────────────────────────────────

    if request.method == 'POST':
        section = request.POST.get('section', 'geral')
        if section == 'geral' and company:
            import base64, uuid
            from django.core.files.base import ContentFile
            company.name        = request.POST.get('name', company.name).strip() or company.name
            company.legal_name  = request.POST.get('legal_name', company.legal_name)
            company.vat         = request.POST.get('vat', company.vat)
            company.email       = request.POST.get('email', company.email)
            company.phone       = request.POST.get('phone', company.phone)
            website = request.POST.get('website', company.website)
            if website and not website.startswith(('http://', 'https://')):
                website = 'https://' + website
            company.website     = website
            company.address     = request.POST.get('address', company.address)
            company.city        = request.POST.get('city', company.city)
            company.postal_code = request.POST.get('postal_code', company.postal_code)
            company.country     = request.POST.get('country', company.country)
            company.currency    = request.POST.get('currency', company.currency)
            logo_b64 = request.POST.get('logo_base64', '').strip()
            if logo_b64 and ',' in logo_b64:
                try:
                    header, data_b64 = logo_b64.split(',', 1)
                    img_bytes = base64.b64decode(data_b64)
                    ext = 'png' if 'png' in header else 'jpg'
                    company.logo.save(f'{uuid.uuid4()}.{ext}', ContentFile(img_bytes), save=False)
                except Exception:
                    pass
            company.save()
            messages.success(request, 'Configurações guardadas com sucesso.')

        elif section == 'crm' and company:
            from apps.crm.models import CRMConfig
            config = CRMConfig.for_company(company)
            config.predictive_scoring  = request.POST.get('predictive_scoring') == '1'
            config.prospects_enabled   = request.POST.get('prospects_enabled') == '1'
            years = request.POST.get('lead_generation_years', '3')
            try:
                config.lead_generation_years = max(1, min(10, int(years)))
            except (ValueError, TypeError):
                pass
            config.save()
            messages.success(request, 'Configurações de CRM guardadas.')

        elif section == 'crm_recalculate' and company:
            from apps.crm.services import recalculate_stage_probabilities
            results = recalculate_stage_probabilities(company=company)
            messages.success(request, f'Probabilidades recalculadas para {len(results)} estágios.')

        elif section == 'crm_generate_leads' and company:
            from apps.crm.services import generate_leads_from_history
            from apps.crm.models import CRMConfig
            crm_cfg = CRMConfig.for_company(company)
            raw_limit = request.POST.get('lead_count', '')
            limit = None
            if raw_limit:
                try:
                    limit = max(1, int(raw_limit))
                except (ValueError, TypeError):
                    pass
            count = generate_leads_from_history(
                company=company,
                years=crm_cfg.lead_generation_years,
                user=request.user,
                limit=limit,
            )
            if count > 0:
                messages.success(request, f'{count} lead{"s geradas" if count != 1 else " gerada"} a partir do histórico de vendas.')
            else:
                messages.info(request, 'Nenhuma lead nova gerada — todos os clientes elegíveis já têm prospectos ou oportunidades abertas.')

        else:
            messages.success(request, 'Configurações guardadas.')

        # Redireciona de volta para a mesma secção
        from django.shortcuts import redirect
        crm_subsections = {'crm_recalculate': 'crm', 'crm_generate_leads': 'crm'}
        redirect_section = crm_subsections.get(section, section) if section in ('geral', 'crm', 'contactos', 'marketing', 'utilizadores', 'crm_recalculate', 'crm_generate_leads') else 'geral'
        return redirect(f"{reverse('dashboard:settings')}?s={redirect_section}")

    from django.contrib.auth import get_user_model
    from apps.crm.models import CRMConfig
    User = get_user_model()
    crm_config = CRMConfig.for_company(company) if company else None
    return render(request, 'dashboard/settings.html', {
        'company': company,
        'active_section': request.GET.get('s', 'geral'),
        'crm_config': crm_config,
        'user_count': User.objects.filter(is_active=True).count(),
        'company_count': Company.objects.count(),
    })
