from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    {'slug': 'inventory', 'name': 'Inventário',    'icon': '📦', 'url_name': 'inventory:inventory_dashboard'},
    {'slug': 'purchases', 'name': 'Compras',       'icon': '🛒', 'url_name': None, 'url': '#'},
    {'slug': 'sales',     'name': 'Vendas',        'icon': '💰', 'url_name': None, 'url': '#'},
    {'slug': 'website',   'name': 'Website',       'icon': '🌐', 'url_name': None, 'url': '/'},
    {'slug': 'financial', 'name': 'Financeiro',    'icon': '💳', 'url_name': None, 'url': '#'},
    {'slug': 'bom',       'name': 'BOM',           'icon': '🎂', 'url_name': None, 'url': '#'},
    {'slug': 'documents', 'name': 'Documentos',    'icon': '📄', 'url_name': None, 'url': '#'},
    {'slug': 'marketing', 'name': 'Marketing',     'icon': '📱', 'url_name': None, 'url': '#'},
    {'slug': 'reports',       'name': 'Relatórios',       'icon': '📊', 'url_name': None, 'url': '#'},
    {'slug': 'whatsapp',      'name': 'WhatsApp',         'icon': '',   'url_name': 'whatsapp:template_list'},
    {'slug': 'purchase_list', 'name': 'Lista de Compras', 'icon': '🛍️', 'url_name': 'inventory:purchase_list_index'},
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
        'active_tab': request.GET.get('tab', 'geral'),
        'crm_config': crm_config,
        'user_count': User.objects.filter(is_active=True).count(),
        'company_count': Company.objects.count(),
    })


@admin_required
@require_http_methods(['GET', 'POST'])
def email_layout_view(request):
    """Vista de edição do Email Layout (envelope global)."""
    from apps.core.models import EmailLayout

    layout = EmailLayout.get_layout()
    if not layout:
        # Auto-seed if missing
        layout = EmailLayout.reset_to_default(user=request.user)

    if request.method == 'POST':
        html_content = request.POST.get('html_content', '').strip()
        if html_content:
            layout.html_content = html_content
            layout.updated_by = request.user
            layout.save()
            messages.success(request, 'Email Layout atualizado com sucesso.')
        else:
            messages.error(request, 'O conteúdo HTML não pode estar vazio.')
        return redirect('dashboard:email_layout')

    # Build preview context with real company/user data
    company = None
    active_company_id = request.session.get('active_company_id')
    if active_company_id:
        company = Company.objects.filter(pk=active_company_id).first()
    if not company:
        company = getattr(request.user, 'default_company', None)
    if not company:
        company = Company.objects.order_by('name').first()

    sender_name = request.user.get_full_name() or request.user.username
    sender_initials = ''.join([p[0] for p in sender_name.split()[:2]]).upper() if sender_name else '?'
    sender_email = ''
    try:
        sender_email = request.user.email_config.email_address
    except Exception:
        sender_email = request.user.email or ''

    from django.utils import timezone

    preview_context = {
        'company_name': company.name if company else 'Empresa',
        'company_initial': company.name[0].upper() if company and company.name else 'E',
        'company_logo_url': request.build_absolute_uri(company.logo.url) if company and company.logo else '',
        'company_address': '',
        'company_full_address': '',
        'company_email': company.email if company else '',
        'company_phone': company.phone if company else '',
        'company_website': company.website if company else '',
        'company_website_display': (company.website or '').replace('https://', '').replace('http://', '').rstrip('/') if company else '',
        'sender_name': sender_name,
        'sender_initials': sender_initials,
        'sender_email': sender_email,
        'sender_phone': getattr(request.user, 'phone', '') or '',
        'sender_role': request.user.get_role_display() if hasattr(request.user, 'get_role_display') else '',
        'date_sent': timezone.now().strftime('%d/%m/%Y'),
    }

    # Build company address
    if company:
        parts = []
        if company.address:
            parts.append(company.address.split('\n')[0].strip())
        loc = ' '.join(filter(None, [company.postal_code, company.city]))
        if loc:
            parts.append(loc)
        if company.country:
            parts.append(company.country)
        preview_context['company_address'] = ' · '.join(parts)
        preview_context['company_full_address'] = ' · '.join(parts)

    return render(request, 'dashboard/email_layout.html', {
        'layout': layout,
        'preview_context': json.dumps(preview_context),
    })


@admin_required
@require_http_methods(['POST'])
def email_layout_reset_view(request):
    """Restaura o Email Layout para o ficheiro default."""
    from apps.core.models import EmailLayout
    EmailLayout.reset_to_default(user=request.user)
    messages.success(request, 'Email Layout restaurado para o default.')
    return redirect('dashboard:email_layout')


@admin_required
@require_http_methods(['GET'])
def email_template_list_view(request):
    """Lista de Email Templates com pesquisa, filtros e paginação."""
    from apps.core.models import EmailTemplate
    from apps.core.multi_company import filter_by_company
    from django.core.paginator import Paginator
    from django.db.models import Q

    search_query = request.GET.get('search', '')
    search_field = request.GET.get('field', 'name')
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)
    status_filter = request.GET.get('status', 'active')
    module_filter = request.GET.get('module', '')

    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    if status_filter == 'archived':
        templates = EmailTemplate.objects.filter(is_active=False)
    else:
        templates = EmailTemplate.objects.filter(is_active=True)

    templates = filter_by_company(templates, request)

    # Module filter
    if module_filter:
        templates = templates.filter(module=module_filter)

    # Search
    if search_query:
        field_mapping = {
            'name': Q(name__icontains=search_query),
            'module': Q(module__icontains=search_query),
            'subject': Q(subject__icontains=search_query),
            'language': Q(language__icontains=search_query),
        }
        if search_field in field_mapping:
            templates = templates.filter(field_mapping[search_field])

    templates = templates.order_by('module', 'name')

    paginator = Paginator(templates, page_size)
    page_obj = paginator.get_page(page_number)

    context = {
        'templates': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
        'module_filter': module_filter,
        'module_choices': EmailTemplate.MODULE_CHOICES,
    }

    return render(request, 'dashboard/email_template_list.html', context)


@admin_required
@require_http_methods(['POST'])
def email_template_bulk_archive(request):
    """Arquivar (is_active=False) templates selecionados (apenas CUSTOM)."""
    from apps.core.models import EmailTemplate
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        if not ids:
            return JsonResponse({'success': False, 'error': {'code': 'NO_SELECTION', 'message': 'Nenhum template selecionado.'}}, status=400)

        templates = EmailTemplate.objects.filter(id__in=ids)
        base_templates = [t for t in templates if t.template_type == 'BASE']
        already_archived = [t for t in templates if t.template_type == 'CUSTOM' and not t.is_active]
        to_archive = [t for t in templates if t.template_type == 'CUSTOM' and t.is_active]

        # All selected are already archived (or BASE)
        if not to_archive:
            if already_archived:
                return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ARCHIVED', 'message': 'Os templates selecionados já estão arquivados.'}})
            if base_templates:
                return JsonResponse({'success': False, 'error': {'code': 'BASE_PROTECTED', 'message': 'Templates base do sistema não podem ser arquivados.'}})

        count = EmailTemplate.objects.filter(id__in=[t.id for t in to_archive]).update(is_active=False)
        msg = f'{count} template(s) arquivado(s) com sucesso.'
        warning = None
        if already_archived:
            warning = f'{len(already_archived)} template(s) já estava(m) arquivado(s).'
        if base_templates:
            base_msg = f'{len(base_templates)} template(s) base ignorado(s).'
            warning = f'{warning} {base_msg}' if warning else base_msg
        result = {'success': True, 'message': msg}
        if warning:
            result['warning'] = warning
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'error': {'code': 'SERVER_ERROR', 'message': str(e)}}, status=500)


@admin_required
@require_http_methods(['POST'])
def email_template_bulk_unarchive(request):
    """Desarquivar (is_active=True) templates selecionados (apenas CUSTOM)."""
    from apps.core.models import EmailTemplate
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        if not ids:
            return JsonResponse({'success': False, 'error': {'code': 'NO_SELECTION', 'message': 'Nenhum template selecionado.'}}, status=400)

        templates = EmailTemplate.objects.filter(id__in=ids)
        base_templates = [t for t in templates if t.template_type == 'BASE']
        already_active = [t for t in templates if t.template_type == 'CUSTOM' and t.is_active]
        to_unarchive = [t for t in templates if t.template_type == 'CUSTOM' and not t.is_active]

        # All selected are already active (or BASE)
        if not to_unarchive:
            if already_active:
                return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ACTIVE', 'message': 'Os templates selecionados já estão ativos.'}})
            if base_templates:
                return JsonResponse({'success': False, 'error': {'code': 'BASE_PROTECTED', 'message': 'Templates base do sistema não podem ser desarquivados.'}})

        count = EmailTemplate.objects.filter(id__in=[t.id for t in to_unarchive]).update(is_active=True)
        msg = f'{count} template(s) desarquivado(s) com sucesso.'
        warning = None
        if already_active:
            warning = f'{len(already_active)} template(s) já estava(m) ativo(s).'
        if base_templates:
            base_msg = f'{len(base_templates)} template(s) base ignorado(s).'
            warning = f'{warning} {base_msg}' if warning else base_msg
        result = {'success': True, 'message': msg}
        if warning:
            result['warning'] = warning
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'error': {'code': 'SERVER_ERROR', 'message': str(e)}}, status=500)


@admin_required
@require_http_methods(['POST'])
def email_template_bulk_delete(request):
    """Eliminar permanentemente templates CUSTOM selecionados."""
    from apps.core.models import EmailTemplate
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        if not ids:
            return JsonResponse({'success': False, 'error': {'code': 'NO_SELECTION', 'message': 'Nenhum template selecionado.'}}, status=400)

        base_count = EmailTemplate.objects.filter(id__in=ids, template_type='BASE').count()
        if base_count == len(ids):
            return JsonResponse({'success': False, 'error': {'code': 'BASE_PROTECTED', 'message': 'Templates base do sistema não podem ser eliminados.'}}, status=403)

        count, _ = EmailTemplate.objects.filter(id__in=ids, template_type='CUSTOM').delete()
        msg = f'{count} template(s) eliminado(s) com sucesso.'
        warning = None
        if base_count:
            warning = f'{base_count} template(s) base ignorado(s) (não podem ser eliminados).'
        result = {'success': True, 'message': msg}
        if warning:
            result['warning'] = warning
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'success': False, 'error': {'code': 'SERVER_ERROR', 'message': str(e)}}, status=500)


# ══════════════════════════════════════════════════════════════════════
# Email Template — Create / Edit / Reset Body
# ══════════════════════════════════════════════════════════════════════

@admin_required
@require_http_methods(['GET', 'POST'])
def email_template_create_view(request):
    """Criar novo Email Template."""
    from apps.core.models import EmailTemplate

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        module = request.POST.get('module', 'GENERAL')
        language = request.POST.get('language', 'pt_PT')
        subject = request.POST.get('subject', '').strip()
        body_html = request.POST.get('body_html', '').strip()
        placeholders_raw = request.POST.get('available_placeholders', '{}').strip()

        if not name:
            messages.error(request, 'O nome do template é obrigatório.')
            return redirect('dashboard:email_template_create')
        if not subject:
            messages.error(request, 'O assunto é obrigatório.')
            return redirect('dashboard:email_template_create')

        import json as _json
        try:
            available_placeholders = _json.loads(placeholders_raw) if placeholders_raw else {}
        except _json.JSONDecodeError:
            available_placeholders = {}

        # Determine owner_company
        active_company_id = request.session.get('active_company_id')
        owner_company = None
        if active_company_id:
            owner_company = Company.objects.filter(pk=active_company_id).first()

        try:
            tmpl = EmailTemplate.objects.create(
                name=name,
                module=module,
                language=language,
                subject=subject,
                body_html=body_html,
                available_placeholders=available_placeholders,
                owner_company=owner_company,
                template_type='CUSTOM',
                created_by=request.user,
                updated_by=request.user,
            )
            messages.success(request, f'Template "{name}" criado com sucesso.')
            return redirect('dashboard:email_template_edit', template_id=tmpl.pk)
        except Exception as e:
            messages.error(request, f'Erro ao criar template: {e}')
            return redirect('dashboard:email_template_create')

    # GET — empty form (CUSTOM templates start blank)
    from apps.core.models import EmailLayout
    preview_context = _build_email_preview_context(request)
    layout = EmailLayout.get_layout()
    layout_html = layout.html_content if layout else '{{ body_content }}'

    return render(request, 'dashboard/email_template_form.html', {
        'template': None,
        'preview_context': json.dumps(preview_context),
        'layout_html': layout_html,
        'placeholders_json': '{}',
        'module_choices': EmailTemplate.MODULE_CHOICES,
        'language_choices': EmailTemplate.LANGUAGE_CHOICES,
    })


@admin_required
@require_http_methods(['GET', 'POST'])
def email_template_edit_view(request, template_id):
    """Editar Email Template existente."""
    from apps.core.models import EmailTemplate
    from django.shortcuts import get_object_or_404

    tmpl = get_object_or_404(EmailTemplate, pk=template_id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        module = request.POST.get('module', tmpl.module)
        language = request.POST.get('language', tmpl.language)
        subject = request.POST.get('subject', '').strip()
        body_html = request.POST.get('body_html', '').strip()
        placeholders_raw = request.POST.get('available_placeholders', '{}').strip()

        if not name:
            messages.error(request, 'O nome do template é obrigatório.')
            return redirect('dashboard:email_template_edit', template_id=tmpl.pk)
        if not subject:
            messages.error(request, 'O assunto é obrigatório.')
            return redirect('dashboard:email_template_edit', template_id=tmpl.pk)

        import json as _json
        try:
            available_placeholders = _json.loads(placeholders_raw) if placeholders_raw else {}
        except _json.JSONDecodeError:
            available_placeholders = tmpl.available_placeholders

        tmpl.name = name
        tmpl.module = module
        tmpl.language = language
        tmpl.subject = subject
        tmpl.body_html = body_html
        tmpl.available_placeholders = available_placeholders
        tmpl.updated_by = request.user
        try:
            tmpl.save()
            messages.success(request, f'Template "{name}" atualizado com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao guardar: {e}')
        return redirect('dashboard:email_template_edit', template_id=tmpl.pk)

    # GET
    from apps.core.models import EmailLayout
    preview_context = _build_email_preview_context(request)
    layout = EmailLayout.get_layout()
    layout_html = layout.html_content if layout else '{{ body_content }}'

    return render(request, 'dashboard/email_template_form.html', {
        'template': tmpl,
        'preview_context': json.dumps(preview_context),
        'layout_html': layout_html,
        'placeholders_json': json.dumps(tmpl.available_placeholders or {}, indent=4, ensure_ascii=False),
        'module_choices': EmailTemplate.MODULE_CHOICES,
        'language_choices': EmailTemplate.LANGUAGE_CHOICES,
    })


@admin_required
@require_http_methods(['POST'])
def email_template_reset_body_view(request, template_id):
    """Restaura o body_html de um template para o default."""
    from apps.core.models import EmailTemplate
    from django.shortcuts import get_object_or_404

    tmpl = get_object_or_404(EmailTemplate, pk=template_id)
    tmpl.reset_body_to_default(user=request.user)
    messages.success(request, 'Corpo do template restaurado para o default.')
    return redirect('dashboard:email_template_edit', template_id=tmpl.pk)


def _build_email_preview_context(request):
    """Constrói o contexto de preview para templates de email (reutilizado por create/edit)."""
    from django.utils import timezone

    company = None
    active_company_id = request.session.get('active_company_id')
    if active_company_id:
        company = Company.objects.filter(pk=active_company_id).first()
    if not company:
        company = getattr(request.user, 'default_company', None)
    if not company:
        company = Company.objects.order_by('name').first()

    sender_name = request.user.get_full_name() or request.user.username
    sender_initials = ''.join([p[0] for p in sender_name.split()[:2]]).upper() if sender_name else '?'
    sender_email = ''
    try:
        sender_email = request.user.email_config.email_address
    except Exception:
        sender_email = request.user.email or ''

    ctx = {
        'contact_name': 'João Silva',
        'lead_title': 'Proposta Website Redesign',
        'company_name': company.name if company else 'Empresa',
        'company_initial': company.name[0].upper() if company and company.name else 'E',
        'company_logo_url': request.build_absolute_uri(company.logo.url) if company and company.logo else '',
        'company_address': '',
        'company_full_address': '',
        'company_email': company.email if company else '',
        'company_phone': company.phone if company else '',
        'company_website': company.website if company else '',
        'company_website_display': (company.website or '').replace('https://', '').replace('http://', '').rstrip('/') if company else '',
        'sender_name': sender_name,
        'sender_initials': sender_initials,
        'sender_email': sender_email,
        'sender_phone': getattr(request.user, 'phone', '') or '',
        'sender_role': request.user.get_role_display() if hasattr(request.user, 'get_role_display') else '',
        'date_sent': timezone.now().strftime('%d/%m/%Y'),
    }

    if company:
        parts = []
        if company.address:
            parts.append(company.address.split('\n')[0].strip())
        loc = ' '.join(filter(None, [company.postal_code, company.city]))
        if loc:
            parts.append(loc)
        if company.country:
            parts.append(company.country)
        ctx['company_address'] = ' · '.join(parts)
        ctx['company_full_address'] = ' · '.join(parts)

    return ctx


# ─── Document Layout ─────────────────────────────────────────────────────────

FONT_CHOICES = [
    ('Lato', 'Lato'),
    ('Inter', 'Inter'),
    ('Roboto', 'Roboto'),
    ('Open Sans', 'Open Sans'),
    ('Montserrat', 'Montserrat'),
    ('Poppins', 'Poppins'),
    ('Merriweather', 'Merriweather'),
    ('Playfair Display', 'Playfair Display'),
    ('Source Sans Pro', 'Source Sans Pro'),
    ('Nunito', 'Nunito'),
]


@admin_required
@require_http_methods(['GET', 'POST'])
def document_layout_view(request):
    """Vista de configuração do Document Layout por empresa."""
    from apps.documents.models import LayoutStyle, TableStyle, DocumentLayout

    # Resolve active company
    company = None
    active_company_id = request.session.get('active_company_id')
    if active_company_id:
        company = Company.objects.filter(pk=active_company_id).first()
    if not company:
        company = getattr(request.user, 'default_company', None)
    if not company:
        company = Company.objects.order_by('name').first()

    if not company:
        messages.error(request, 'Nenhuma empresa encontrada. Crie uma empresa primeiro.')
        return redirect('dashboard:settings')

    # Get or create DocumentLayout for this company
    layout_styles = LayoutStyle.objects.filter(is_active=True)
    table_styles = TableStyle.objects.filter(is_active=True)

    try:
        doc_layout = DocumentLayout.objects.select_related(
            'layout_style', 'table_style'
        ).get(company=company)
    except DocumentLayout.DoesNotExist:
        # Auto-create with defaults
        default_ls = layout_styles.first()
        default_ts = table_styles.first()
        if default_ls and default_ts:
            doc_layout = DocumentLayout.objects.create(
                company=company,
                layout_style=default_ls,
                table_style=default_ts,
                created_by=request.user,
                updated_by=request.user,
            )
        else:
            messages.error(request, 'Execute o seed de estilos primeiro: scripts/seed_document_styles.py')
            return redirect('dashboard:settings')

    if request.method == 'POST':
        layout_style_id = request.POST.get('layout_style')
        table_style_id = request.POST.get('table_style')
        font = request.POST.get('font', 'Lato')
        primary_color = request.POST.get('primary_color', '#dbc693')
        secondary_color = request.POST.get('secondary_color', '#1f2937')
        tagline = request.POST.get('tagline', '').strip()
        footer_text = request.POST.get('footer_text', '').strip()
        paper_format = request.POST.get('paper_format', 'A4')
        tax_id = request.POST.get('tax_id', '').strip()

        try:
            doc_layout.layout_style = LayoutStyle.objects.get(pk=layout_style_id)
            doc_layout.table_style = TableStyle.objects.get(pk=table_style_id)
        except (LayoutStyle.DoesNotExist, TableStyle.DoesNotExist):
            messages.error(request, 'Estilo inválido.')
            return redirect('dashboard:document_layout')

        doc_layout.font = font
        doc_layout.primary_color = primary_color
        doc_layout.secondary_color = secondary_color
        doc_layout.tagline = tagline
        doc_layout.footer_text = footer_text
        doc_layout.paper_format = paper_format
        doc_layout.tax_id = tax_id
        doc_layout.updated_by = request.user
        doc_layout.save()

        messages.success(request, 'Layout de documentos atualizado com sucesso.')
        return redirect('dashboard:document_layout')

    # Build company preview context
    company_initials = ''.join([p[0] for p in company.name.split()[:2]]).upper() if company.name else 'E'
    address_parts = []
    if company.address:
        address_parts.append(company.address.split('\n')[0].strip())
    loc = ' '.join(filter(None, [company.postal_code, company.city]))
    if loc:
        address_parts.append(loc)
    if company.country:
        address_parts.append(company.country)

    preview_context = {
        'company_name': company.name,
        'company_initials': company_initials,
        'company_logo': request.build_absolute_uri(company.logo.url) if company.logo else '',
        'company_address': ' · '.join(address_parts) if address_parts else '',
        'company_phone': company.phone or '',
        'company_email': company.email or '',
        'company_website': company.website or '',
        'primary_color': doc_layout.primary_color,
        'secondary_color': doc_layout.secondary_color,
        'font': doc_layout.font,
        'tagline': doc_layout.tagline,
        'footer_text': doc_layout.footer_text,
        'tax_id': doc_layout.tax_id or company.vat or '',
    }

    return render(request, 'dashboard/document_layout.html', {
        'company': company,
        'doc_layout': doc_layout,
        'layout_styles': layout_styles,
        'table_styles': table_styles,
        'font_choices': FONT_CHOICES,
        'paper_choices': DocumentLayout.PAPER_CHOICES,
        'preview_context': json.dumps(preview_context),
    })


# ── Document Sequences ────────────────────────────────────────────────

@admin_required
@require_http_methods(['GET'])
def document_sequence_list_view(request):
    """List DocumentSequence records for the active company — searchable + paginated."""
    from apps.core.models import DocumentSequence
    from apps.core.multi_company import get_active_company
    from django.core.paginator import Paginator

    company      = get_active_company(request)
    search_query = request.GET.get('search', '')
    search_field = request.GET.get('field', 'name')
    status_filter = request.GET.get('status', 'active')
    page_number  = request.GET.get('page', 1)
    try:
        page_size = int(request.GET.get('page_size', 50))
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50

    from django.db.models import Q
    if status_filter == 'archived':
        qs = DocumentSequence.objects.filter(owner_company=company, is_active=False)
    elif status_filter == 'all':
        qs = DocumentSequence.objects.filter(owner_company=company)
    else:
        qs = DocumentSequence.objects.filter(owner_company=company, is_active=True)

    if search_query:
        field_map = {
            'code':   Q(code__icontains=search_query),
            'name':   Q(name__icontains=search_query),
            'prefix': Q(prefix__icontains=search_query),
        }
        qs = qs.filter(field_map.get(search_field, Q(name__icontains=search_query)))

    qs = qs.order_by('code')
    paginator = Paginator(qs, page_size)
    page_obj  = paginator.get_page(page_number)

    statuses = [
        ('active',   'Ativos'),
        ('archived', 'Arquivados'),
        ('all',      'Todos'),
    ]

    return render(request, 'dashboard/document_sequences.html', {
        'sequences':     page_obj,
        'company':       company,
        'search_query':  search_query,
        'search_field':  search_field,
        'status_filter': status_filter,
        'total_count':   paginator.count,
        'page_size':     page_size,
        'statuses':      statuses,
    })


@admin_required
@require_http_methods(['POST'])
def document_sequence_save_view(request, seq_id):
    """Inline-save a DocumentSequence (name, prefix, suffix, padding, next_number)."""
    from apps.core.models import DocumentSequence
    from apps.core.multi_company import get_active_company

    company = get_active_company(request)
    try:
        seq = DocumentSequence.objects.get(pk=seq_id, owner_company=company)
    except DocumentSequence.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Sequência não encontrada.'}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido.'}, status=400)

    seq.name        = data.get('name', seq.name).strip() or seq.name
    seq.prefix      = data.get('prefix', seq.prefix)
    seq.suffix      = data.get('suffix', seq.suffix)
    seq.is_active   = bool(data.get('is_active', seq.is_active))

    try:
        padding = int(data.get('padding', seq.padding))
        if 1 <= padding <= 10:
            seq.padding = padding
    except (ValueError, TypeError):
        pass

    try:
        next_number = int(data.get('next_number', seq.next_number))
        if next_number >= 1:
            seq.next_number = next_number
    except (ValueError, TypeError):
        pass

    seq.save()
    return JsonResponse({
        'success': True,
        'preview': f'{seq.prefix}{str(seq.next_number).zfill(seq.padding)}{seq.suffix}',
    })


@admin_required
@require_http_methods(['GET', 'POST'])
def document_sequence_create_view(request):
    """Create a new DocumentSequence — full form page."""
    from apps.core.models import DocumentSequence
    from apps.core.multi_company import get_active_company

    company = get_active_company(request)

    if request.method == 'GET':
        return render(request, 'dashboard/document_sequence_form.html', {'seq': None, 'company': company})

    code = request.POST.get('code', '').strip().upper()
    name = request.POST.get('name', '').strip()
    prefix = request.POST.get('prefix', '')
    suffix = request.POST.get('suffix', '')

    if not code or not name:
        messages.error(request, 'Código e Nome são obrigatórios.')
        return render(request, 'dashboard/document_sequence_form.html', {'seq': None, 'company': company})

    try:
        padding = int(request.POST.get('padding', 5))
        padding = max(1, min(10, padding))
    except (ValueError, TypeError):
        padding = 5

    try:
        next_number = int(request.POST.get('next_number', 1))
        next_number = max(1, next_number)
    except (ValueError, TypeError):
        next_number = 1

    _, created = DocumentSequence.objects.get_or_create(
        code=code,
        owner_company=company,
        defaults={
            'name': name,
            'prefix': prefix,
            'suffix': suffix,
            'padding': padding,
            'next_number': next_number,
            'is_active': 'is_active' in request.POST,
        },
    )

    if created:
        messages.success(request, f'Sequência «{code}» criada com sucesso.')
        return redirect('dashboard:document_sequences')
    else:
        messages.warning(request, f'Já existe uma sequência com o código «{code}».'
                         ' Escolha um código diferente.')
        return render(request, 'dashboard/document_sequence_form.html', {'seq': None, 'company': company})


@admin_required
@require_http_methods(['POST'])
def document_sequence_generate_view(request):
    """Generate all default DocumentSequences (inventory) for the active company."""
    from apps.core.models import DocumentSequence
    from apps.core.multi_company import get_active_company

    company = get_active_company(request)
    created_count = 0
    skipped_count = 0

    for code, defaults in DocumentSequence.SEQUENCE_DEFAULTS.items():
        _, created = DocumentSequence.objects.get_or_create(
            code=code,
            owner_company=company,
            defaults={
                'name':       defaults.get('name', code),
                'prefix':     defaults.get('prefix', ''),
                'suffix':     defaults.get('suffix', ''),
                'padding':    defaults.get('padding', 5),
                'next_number': 1,
            },
        )
        if created:
            created_count += 1
        else:
            skipped_count += 1

    if created_count and skipped_count:
        messages.success(request, f'{created_count} sequência(s) criada(s). {skipped_count} já existia(m) e não foram alteradas.')
    elif created_count:
        messages.success(request, f'{created_count} sequência(s) de inventário criada(s) com sucesso.')
    else:
        messages.info(request, 'Todas as sequências de inventário já existiam.')

    return redirect('dashboard:document_sequences')


@admin_required
@require_http_methods(['GET', 'POST'])
def document_sequence_edit_view(request, seq_id):
    """Edit an existing DocumentSequence — full form page."""
    from apps.core.models import DocumentSequence
    from apps.core.multi_company import get_active_company

    company = get_active_company(request)
    seq = get_object_or_404(DocumentSequence, pk=seq_id, owner_company=company)

    if request.method == 'POST':
        seq.name = request.POST.get('name', seq.name).strip() or seq.name
        seq.prefix = request.POST.get('prefix', seq.prefix)
        seq.suffix = request.POST.get('suffix', seq.suffix)
        try:
            padding = int(request.POST.get('padding', seq.padding))
            seq.padding = max(1, min(10, padding))
        except (ValueError, TypeError):
            pass
        try:
            next_number = int(request.POST.get('next_number', seq.next_number))
            seq.next_number = max(1, next_number)
        except (ValueError, TypeError):
            pass
        seq.is_active = 'is_active' in request.POST
        seq.save()
        messages.success(request, f'Sequência «{seq.code}» gravada com sucesso.')
        return redirect('dashboard:document_sequences')

    return render(request, 'dashboard/document_sequence_form.html', {
        'seq': seq,
        'company': company,
    })


@admin_required
@require_http_methods(['POST'])
def document_sequence_bulk_archive_view(request):
    """Bulk-archive (deactivate) selected DocumentSequences."""
    from apps.core.models import DocumentSequence
    from apps.core.multi_company import get_active_company

    company = get_active_company(request)
    ids = request.POST.getlist('ids[]')
    count = DocumentSequence.objects.filter(pk__in=ids, owner_company=company).update(is_active=False)
    return JsonResponse({'success': True, 'message': f'{count} sequência(s) arquivada(s).'})


@admin_required
@require_http_methods(['POST'])
def document_sequence_bulk_unarchive_view(request):
    """Bulk-unarchive (reactivate) selected DocumentSequences."""
    from apps.core.models import DocumentSequence
    from apps.core.multi_company import get_active_company

    company = get_active_company(request)
    ids = request.POST.getlist('ids[]')
    count = DocumentSequence.objects.filter(pk__in=ids, owner_company=company).update(is_active=True)
    return JsonResponse({'success': True, 'message': f'{count} sequência(s) reativada(s).'})


@admin_required
@require_http_methods(['POST'])
def document_sequence_bulk_delete_view(request):
    """Permanently delete selected DocumentSequences."""
    from apps.core.models import DocumentSequence
    from apps.core.multi_company import get_active_company

    company = get_active_company(request)
    ids = request.POST.getlist('ids[]')
    qs = DocumentSequence.objects.filter(pk__in=ids, owner_company=company)
    count = qs.count()
    qs.delete()
    return JsonResponse({'success': True, 'message': f'{count} sequência(s) eliminada(s).'})

