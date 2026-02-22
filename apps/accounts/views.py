import json
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.core.models import Company
from apps.core.email_utils import encrypt_password
from .forms import LoginForm
from .models import CustomUser, UserEmailConfig, AppRole, APP_REGISTRY, APP_MODELS_REGISTRY


# ──────────────────────────────────────────────────────────────────────────────
# Helper: apply default AppRole levels based on system role
# ──────────────────────────────────────────────────────────────────────────────
_ROLE_TO_APP_LEVEL = {
    CustomUser.ADMIN:    AppRole.ADMIN,    # 'ADMIN'   → 'admin'
    CustomUser.MANAGER:  AppRole.MANAGER,  # 'MANAGER' → 'manager'
    CustomUser.EMPLOYEE: AppRole.USER,     # 'EMPLOYEE'→ 'user'
}


def apply_default_app_roles(user):
    """Set AppRole for every (company, app) pair based on the user's system role.
    Existing records are overwritten; apps/companies without an AppRole get one created.
    """
    app_level = _ROLE_TO_APP_LEVEL.get(user.role)
    if app_level is None:
        return  # unknown role — do nothing
    for company in user.companies.all():
        for app_slug, _ in APP_REGISTRY:
            AppRole.objects.update_or_create(
                user=user, app=app_slug, company=company,
                defaults={'level': app_level},
            )


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        # Set default company in session on login
        if self.request.user.default_company:
            self.request.session['active_company_id'] = str(self.request.user.default_company.id)
        return reverse_lazy('dashboard:index')


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('accounts:login')


@login_required
def switch_company(request, company_id):
    """
    Switch active company for the current user session.
    Only allows switching to companies the user has access to.
    """
    try:
        company = Company.objects.get(id=company_id)
        
        # Verify user has access to this company
        if request.user.companies.filter(id=company_id).exists() or request.user.is_superuser:
            request.session['active_company_id'] = str(company_id)
            messages.success(request, f'Empresa alterada para: {company.name}')
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'company_id': str(company_id),
                    'company_name': company.name
                })
        else:
            messages.error(request, 'Não tem permissão para aceder a esta empresa.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
                
    except Company.DoesNotExist:
        messages.error(request, 'Empresa não encontrada.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Company not found'}, status=404)
    
    # Redirect back to the previous page
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:index'))


@login_required
def profile_settings(request):
    """Página de configurações do perfil — inclui configuração SMTP de email."""
    user = request.user
    config, _ = UserEmailConfig.objects.get_or_create(user=user)

    if request.method == 'POST':
        smtp_address = request.POST.get('email_address', '').strip()
        app_password_raw = request.POST.get('app_password', '').strip()
        provider = request.POST.get('provider', 'gmail').strip()

        if provider not in dict(UserEmailConfig.PROVIDER_CHOICES):
            messages.error(request, 'Provedor SMTP inválido.')
            return redirect('accounts:profile_settings')

        config.email_address = smtp_address
        config.provider = provider

        if app_password_raw:
            # Nova password introduzida — encriptar e guardar
            try:
                config.app_password = encrypt_password(app_password_raw)
            except ValueError as e:
                messages.error(request, f'Erro de configuração de encriptação: {e}')
                return redirect('accounts:profile_settings')
        elif not smtp_address:
            # Campo de email limpo — limpar também a password
            config.app_password = ''

        config.save()
        messages.success(request, 'Configuração de email guardada com sucesso.')
        return redirect('accounts:profile_settings')

    context = {
        'email_config': config,
        'smtp_providers': UserEmailConfig.PROVIDER_CHOICES,
        'page_title': 'Definições do Perfil',
    }
    return render(request, 'accounts/profile_settings.html', context)


@login_required
@require_http_methods(['POST'])
def test_smtp(request):
    """Envia um email de teste para o próprio utilizador para verificar a configuração SMTP."""
    from apps.core.email_utils import send_email_for_record
    user = request.user

    try:
        config = user.email_config
    except UserEmailConfig.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'SMTP não configurado.'})

    if not config.has_smtp_configured:
        return JsonResponse({'success': False, 'error': 'SMTP não configurado.'})

    # Para o teste, não ligamos a nenhum registo — enviamos diretamente via baixo nível
    from apps.core.email_utils import _send_via_smtp
    success, error, msg_id = _send_via_smtp(
        config=config,
        to_email=config.email_address,
        to_name=user.get_full_name(),
        subject='Teste de email — Fuet Mágico CRM',
        body=(
            f'Olá {user.get_full_name()},\n\n'
            'Este é um email de teste enviado pelo Fuet Mágico CRM para confirmar '
            'que a tua configuração SMTP está correta.\n\nBom trabalho!'
        ),
        body_html=None,
        sender_name=user.get_full_name() or user.username,
    )
    if success:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': error})


# ─────────────────────────────────────────────────────────────────────────────
# USER MANAGEMENT (ADMIN only)
# ─────────────────────────────────────────────────────────────────────────────
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.http import require_POST
from .forms import UserCreateForm, UserEditForm, SetNewPasswordForm
from .decorators import admin_required


@admin_required
def user_list_view(request):
    """Lista todos os utilizadores visíveis para o admin."""
    from django.core.paginator import Paginator
    from django.db.models import Q as Qobj

    qs = CustomUser.objects.all().order_by('username')

    search_query = request.GET.get('search', '').strip()
    search_field = request.GET.get('field', '')
    role_filter  = request.GET.get('role', '')
    status_filter = request.GET.get('status', 'active')  # default: ativos

    if search_query:
        if search_field == 'name':
            qs = qs.filter(Qobj(first_name__icontains=search_query) | Qobj(last_name__icontains=search_query))
        elif search_field == 'email':
            qs = qs.filter(email__icontains=search_query)
        elif search_field == 'username':
            qs = qs.filter(username__icontains=search_query)
        elif search_field == 'phone':
            qs = qs.filter(phone__icontains=search_query)
        elif search_field == 'role':
            qs = qs.filter(role__icontains=search_query)
        else:
            qs = qs.filter(
                Qobj(first_name__icontains=search_query) |
                Qobj(last_name__icontains=search_query) |
                Qobj(username__icontains=search_query) |
                Qobj(email__icontains=search_query) |
                Qobj(phone__icontains=search_query)
            )

    if role_filter:
        qs = qs.filter(role=role_filter)

    if status_filter == 'archived':
        qs = qs.filter(is_active=False)
    else:
        qs = qs.filter(is_active=True)

    total_count = qs.count()

    try:
        page_size = int(request.GET.get('page_size', 25))
        page_size = max(5, min(page_size, 200))
    except (ValueError, TypeError):
        page_size = 25

    paginator = Paginator(qs, page_size)
    page_number = request.GET.get('page', 1)
    users_page = paginator.get_page(page_number)

    return render(request, 'accounts/user_list.html', {
        'users': users_page,
        'total_count': total_count,
        'page_size': page_size,
        'search_query': search_query,
        'search_field': search_field,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'role_choices': CustomUser.ROLE_CHOICES,
        'page_title': 'Utilizadores',
    })


@admin_required
@require_POST
def user_bulk_archive(request):
    """Arquivar utilizadores selecionados (AJAX / JSON)."""
    import json
    try:
        data = json.loads(request.body)
        user_ids = [int(x) for x in data.get('user_ids', [])]
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID', 'message': 'Pedido inválido.'}}, status=400)

    if not user_ids:
        return JsonResponse({'success': False, 'error': {'code': 'NO_SELECTION', 'message': 'Nenhum utilizador selecionado.'}}, status=400)

    # Exclude own user and ADMIN-role users (they may never be archived)
    qs = CustomUser.objects.filter(pk__in=user_ids).exclude(pk=request.user.pk).exclude(role='ADMIN')

    if not qs.exists():
        return JsonResponse({'success': False, 'error': {'code': 'ALL_BLOCKED', 'message': 'Não é possível arquivar os utilizadores selecionados (admins ou próprio utilizador).'}}, status=409)

    active_qs = qs.filter(is_active=True)
    if not active_qs.exists():
        return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ARCHIVED', 'message': 'Os utilizadores selecionados já estão arquivados.'}}, status=409)

    count = active_qs.update(is_active=False)
    return JsonResponse({'success': True, 'message': f'{count} utilizador(es) arquivado(s).'})


@admin_required
@require_POST
def user_bulk_unarchive(request):
    """Desarquivar utilizadores selecionados (AJAX / JSON)."""
    import json
    try:
        data = json.loads(request.body)
        user_ids = [int(x) for x in data.get('user_ids', [])]
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID', 'message': 'Pedido inválido.'}}, status=400)

    if not user_ids:
        return JsonResponse({'success': False, 'error': {'code': 'NO_SELECTION', 'message': 'Nenhum utilizador selecionado.'}}, status=400)

    qs = CustomUser.objects.filter(pk__in=user_ids).exclude(pk=request.user.pk).exclude(role='ADMIN')

    if not qs.exists():
        return JsonResponse({'success': False, 'error': {'code': 'ALL_BLOCKED', 'message': 'Não é possível desarquivar os utilizadores selecionados (admins ou próprio utilizador).'}}, status=409)

    inactive_qs = qs.filter(is_active=False)
    if not inactive_qs.exists():
        return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ACTIVE', 'message': 'Os utilizadores selecionados já estão ativos.'}}, status=409)

    count = inactive_qs.update(is_active=True)
    return JsonResponse({'success': True, 'message': f'{count} utilizador(es) reativado(s).'})


@admin_required
@require_POST
def user_bulk_delete(request):
    """Eliminar permanentemente utilizadores selecionados (AJAX / JSON)."""
    import json
    try:
        data = json.loads(request.body)
        user_ids = [int(x) for x in data.get('user_ids', [])]
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID', 'message': 'Pedido inválido.'}}, status=400)

    if not user_ids:
        return JsonResponse({'success': False, 'error': {'code': 'NO_SELECTION', 'message': 'Nenhum utilizador selecionado.'}}, status=400)

    # Exclude own user and ADMIN-role users (they may never be deleted)
    qs = CustomUser.objects.filter(pk__in=user_ids).exclude(pk=request.user.pk).exclude(role='ADMIN')

    if not qs.exists():
        return JsonResponse({'success': False, 'error': {'code': 'ALL_BLOCKED', 'message': 'Não é possível eliminar os utilizadores selecionados (admins ou próprio utilizador).'}}, status=409)

    count = qs.count()
    qs.delete()
    return JsonResponse({'success': True, 'message': f'{count} utilizador(es) eliminado(s) permanentemente.'})


@admin_required
@require_POST
def user_delete_single(request, user_id):
    """Eliminar um único utilizador (AJAX / JSON). Bloqueia admins e o próprio utilizador."""
    from django.shortcuts import get_object_or_404
    target = get_object_or_404(CustomUser, id=user_id)

    if target.pk == request.user.pk:
        return JsonResponse({'success': False, 'error': {'code': 'SELF', 'message': 'Não podes eliminar a tua própria conta.'}}, status=409)
    if target.role == 'ADMIN':
        return JsonResponse({'success': False, 'error': {'code': 'ADMIN', 'message': 'Não é possível eliminar utilizadores com role ADMIN.'}}, status=409)

    name = target.get_full_name() or target.username
    target.delete()
    return JsonResponse({'success': True, 'message': f'Utilizador «{name}» eliminado permanentemente.'})


@admin_required
@require_POST
def user_bulk_reset(request):
    """Enviar email de reset de password em massa (AJAX / JSON)."""
    import json
    from apps.core.email_utils import _send_via_smtp

    try:
        data = json.loads(request.body)
        user_ids = [int(x) for x in data.get('user_ids', [])]
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID', 'message': 'Pedido inválido.'}}, status=400)

    if not user_ids:
        return JsonResponse({'success': False, 'error': {'code': 'NO_SELECTION', 'message': 'Nenhum utilizador selecionado.'}}, status=400)

    # Verify admin has SMTP configured
    try:
        smtp_config = request.user.email_config
    except Exception:
        smtp_config = None

    if not smtp_config or not smtp_config.has_smtp_configured:
        return JsonResponse({'success': False, 'error': {'code': 'NO_SMTP', 'message': 'Configura primeiro o teu SMTP em Meu Perfil antes de enviar emails.'}}, status=400)

    targets = CustomUser.objects.filter(pk__in=user_ids, email__isnull=False).exclude(email='')
    if not targets.exists():
        return JsonResponse({'success': False, 'error': {'code': 'NO_EMAIL', 'message': 'Nenhum dos utilizadores selecionados tem email configurado.'}}, status=400)

    sent = 0
    failed = 0
    for target in targets:
        uid   = urlsafe_base64_encode(force_bytes(target.pk))
        token = default_token_generator.make_token(target)
        reset_url = request.build_absolute_uri(f'/accounts/reset/{uid}/{token}/')

        subject = 'Redefinição de Password — Fuet Mágico CRM'
        body = (
            f'Olá {target.get_full_name() or target.username},\n\n'
            f'O administrador do sistema solicitou a redefinição da tua password.\n\n'
            f'Clica no link abaixo para definir uma nova password:\n\n'
            f'{reset_url}\n\n'
            f'Este link é válido por 3 dias e só pode ser utilizado uma vez.\n\n'
            f'Se não solicitaste esta alteração, ignora este email.\n\n'
            f'— Fuet Mágico CRM'
        )
        body_html = f'''
        <div style="font-family:sans-serif;max-width:520px;margin:0 auto">
          <h2 style="color:#dbc693">Redefinição de Password</h2>
          <p>Olá <strong>{target.get_full_name() or target.username}</strong>,</p>
          <p>O administrador do sistema solicitou a redefinição da tua password.</p>
          <p style="margin:24px 0">
            <a href="{reset_url}"
               style="background:#dbc693;color:#1a1a1a;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:bold">
              Definir Nova Password
            </a>
          </p>
          <p style="color:#888;font-size:13px">Este link é válido por 3 dias e só pode ser utilizado uma vez.<br>
          Se não solicitaste esta alteração, ignora este email.</p>
        </div>
        '''

        ok, _err, _ = _send_via_smtp(
            config=smtp_config,
            to_email=target.email,
            to_name=target.get_full_name() or target.username,
            subject=subject,
            body=body,
            body_html=body_html,
            sender_name=request.user.get_full_name() or 'Fuet Mágico CRM',
        )
        if ok:
            sent += 1
        else:
            failed += 1

    if sent == 0:
        return JsonResponse({'success': False, 'error': {'code': 'SEND_FAILED', 'message': f'Falha ao enviar emails ({failed} erro(s)).'}}, status=500)

    msg = f'Email de reset enviado para {sent} utilizador(es).'
    if failed:
        msg += f' ({failed} falhou.)'
    return JsonResponse({'success': True, 'message': msg})


@admin_required
def user_create_view(request):
    """Criar novo utilizador."""
    form = UserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        avatar_b64 = request.POST.get('avatar_base64', '').strip()
        if avatar_b64 and avatar_b64.startswith('data:image'):
            user.avatar = avatar_b64
            user.save(update_fields=['avatar'])
        # Pre-fill AppRole levels from system role (admin/manager/employee)
        apply_default_app_roles(user)
        messages.success(request, f'Utilizador «{user.get_full_name() or user.username}» criado com sucesso.')
        return redirect('accounts:user_list')
    return render(request, 'accounts/user_create.html', {
        'form': form,
        'page_title': 'Novo Utilizador',
    })


@admin_required
def user_edit_view(request, user_id):
    """Editar utilizador existente."""
    from django.shortcuts import get_object_or_404
    target = get_object_or_404(CustomUser, id=user_id)

    # ADMIN não pode rebaixar o próprio role
    is_self = (request.user.pk == target.pk)

    form = UserEditForm(request.POST or None, instance=target)
    if is_self:
        form.fields['role'].disabled = True
        form.fields['is_active'].disabled = True

    if request.method == 'POST' and form.is_valid():
        old_role = target.role  # capture before form.save() overwrites it
        form.save()
        avatar_b64 = request.POST.get('avatar_base64', '').strip()
        if avatar_b64 and avatar_b64.startswith('data:image'):
            target.avatar = avatar_b64
            target.save(update_fields=['avatar'])
        # 1) App-level roles (AppRole)
        # If the system role changed, reset all AppRoles to the new role's defaults
        # and skip the per-field POST processing (admin can fine-tune on the next edit).
        role_changed = (not is_self) and (target.role != old_role)
        if role_changed:
            apply_default_app_roles(target)
        else:
            valid_levels = {key for key, _ in AppRole.LEVEL_CHOICES}
            AppRole.objects.filter(user=target).exclude(company__in=target.companies.all()).delete()
            # Global permissions: same level written to every company the user belongs to
            for app_slug, _ in APP_REGISTRY:
                level = request.POST.get(f'app_role_{app_slug}', '').strip()
                for company in target.companies.all():
                    if level in valid_levels:
                        AppRole.objects.update_or_create(
                            user=target, app=app_slug, company=company,
                            defaults={'level': level},
                        )
                    else:
                        AppRole.objects.filter(user=target, app=app_slug, company=company).delete()
        # 2) Model-level CRUD permissions (Django auth.Permission)
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        for app_slug, models in APP_MODELS_REGISTRY.items():
            for app_label, model_name, _ in models:
                try:
                    ct = ContentType.objects.get(app_label=app_label, model=model_name)
                except ContentType.DoesNotExist:
                    continue
                for action in ['view', 'add', 'change', 'delete']:
                    try:
                        perm = Permission.objects.get(content_type=ct, codename=f'{action}_{model_name}')
                    except Permission.DoesNotExist:
                        continue
                    if request.POST.get(f'perm_{app_label}_{model_name}_{action}'):
                        target.user_permissions.add(perm)
                    else:
                        target.user_permissions.remove(perm)
        messages.success(request, f'Utilizador «{target.get_full_name() or target.username}» atualizado.')
        return redirect('accounts:user_list')
    # Build flat global app_roles list (same level across all companies)
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType
    target_companies = list(target.companies.all())
    # Use the first company to read existing levels (all companies share the same level)
    first_company_id = str(target_companies[0].id) if target_companies else None
    existing_app_roles = {
        (str(r.company_id), r.app): r.level
        for r in AppRole.objects.filter(user=target).select_related('company')
    }
    user_perm_set = set(
        f"{p.content_type.app_label}.{p.codename}"
        for p in target.user_permissions.select_related('content_type').all()
    )

    def build_models(app_slug):
        models_data = []
        for model_app_label, model_name, display_name in APP_MODELS_REGISTRY.get(app_slug, []):
            models_data.append({
                'display_name': display_name,
                'app_label':    model_app_label,
                'model_name':   model_name,
                'perm_view':    f'{model_app_label}.view_{model_name}'   in user_perm_set,
                'perm_add':     f'{model_app_label}.add_{model_name}'    in user_perm_set,
                'perm_change':  f'{model_app_label}.change_{model_name}' in user_perm_set,
                'perm_delete':  f'{model_app_label}.delete_{model_name}' in user_perm_set,
            })
        return models_data

    app_roles = [
        {
            'app':    app_slug,
            'label':  app_label,
            'level':  existing_app_roles.get((first_company_id, app_slug), '') if first_company_id else '',
            'models': build_models(app_slug),
        }
        for app_slug, app_label in APP_REGISTRY
    ]
    # Email/SMTP config for this user
    try:
        target_email_config = target.email_config
    except UserEmailConfig.DoesNotExist:
        target_email_config = None

    return render(request, 'accounts/user_edit.html', {
        'form': form,
        'target_user': target,
        'is_self': is_self,
        'page_title': f'Editar — {target.get_full_name() or target.username}',
        'existing_companies': [{'id': str(c.id), 'name': c.name} for c in target_companies],
        'app_roles': app_roles,
        'app_role_levels': AppRole.LEVEL_CHOICES,
        'target_email_config': target_email_config,
    })


@admin_required
@require_POST
def user_toggle_active(request, user_id):
    """Ativar ou desativar utilizador (AJAX)."""
    from django.shortcuts import get_object_or_404
    target = get_object_or_404(CustomUser, id=user_id)
    if target.pk == request.user.pk:
        return JsonResponse({'success': False, 'error': 'Não podes desativar a tua própria conta.'}, status=400)
    target.is_active = not target.is_active
    target.save(update_fields=['is_active'])
    state = 'ativado' if target.is_active else 'desativado'
    messages.success(request, f'Utilizador «{target.get_full_name() or target.username}» {state}.')
    return JsonResponse({'success': True, 'is_active': target.is_active})


@admin_required
@require_POST
def user_send_reset_email(request, user_id):
    """
    Gera um token de reset de password e envia email ao utilizador.
    O link gerado é válido uma única vez e expira em 3 dias (padrão Django).
    """
    from django.shortcuts import get_object_or_404
    from apps.core.email_utils import _send_via_smtp

    target = get_object_or_404(CustomUser, id=user_id)

    # Verificar que o admin tem SMTP configurado
    try:
        smtp_config = request.user.email_config
    except Exception:
        smtp_config = None

    if not smtp_config or not smtp_config.has_smtp_configured:
        messages.error(request, 'Configura primeiro o teu SMTP em Meu Perfil antes de enviar emails.')
        return redirect('accounts:user_edit', user_id=user_id)

    if not target.email:
        messages.error(request, 'Este utilizador não tem email configurado.')
        return redirect('accounts:user_edit', user_id=user_id)

    # Gerar token + UID seguros
    uid   = urlsafe_base64_encode(force_bytes(target.pk))
    token = default_token_generator.make_token(target)
    reset_url = request.build_absolute_uri(
        f'/accounts/reset/{uid}/{token}/'
    )

    subject = 'Redefinição de Password — Fuet Mágico CRM'
    body = (
        f'Olá {target.get_full_name() or target.username},\n\n'
        f'O administrador do sistema solicitou a redefinição da tua password.\n\n'
        f'Clica no link abaixo para definir uma nova password:\n\n'
        f'{reset_url}\n\n'
        f'Este link é válido por 3 dias e só pode ser utilizado uma vez.\n\n'
        f'Se não solicitaste esta alteração, ignora este email.\n\n'
        f'— Fuet Mágico CRM'
    )
    body_html = f'''
    <div style="font-family:sans-serif;max-width:520px;margin:0 auto">
      <h2 style="color:#dbc693">Redefinição de Password</h2>
      <p>Olá <strong>{target.get_full_name() or target.username}</strong>,</p>
      <p>O administrador do sistema solicitou a redefinição da tua password.</p>
      <p style="margin:24px 0">
        <a href="{reset_url}"
           style="background:#dbc693;color:#1a1a1a;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:bold">
          Definir Nova Password
        </a>
      </p>
      <p style="color:#888;font-size:13px">Este link é válido por 3 dias e só pode ser utilizado uma vez.<br>
      Se não solicitaste esta alteração, ignora este email.</p>
    </div>
    '''

    success, error, _ = _send_via_smtp(
        config=smtp_config,
        to_email=target.email,
        to_name=target.get_full_name() or target.username,
        subject=subject,
        body=body,
        body_html=body_html,
        sender_name=request.user.get_full_name() or 'Fuet Mágico CRM',
    )

    if success:
        messages.success(request, f'Email de reset enviado para {target.email}.')
    else:
        messages.error(request, f'Erro ao enviar email: {error}')
    return redirect('accounts:user_edit', user_id=user_id)


def password_reset_confirm(request, uidb64, token):
    """
    Página pública (sem login) onde o utilizador define a nova password.
    O token é validado pelo Django — uso único, expira em 3 dias.
    """
    invalid = False
    target  = None

    try:
        uid    = force_str(urlsafe_base64_decode(uidb64))
        target = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        invalid = True

    if not invalid and not default_token_generator.check_token(target, token):
        invalid = True

    if invalid:
        return render(request, 'accounts/password_reset_invalid.html', status=400)

    form = SetNewPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        target.set_password(form.cleaned_data['new_password1'])
        target.save(update_fields=['password'])
        messages.success(request, 'Password alterada com sucesso. Faz login com a tua nova password.')
        return redirect('accounts:login')

    return render(request, 'accounts/password_reset_confirm.html', {
        'form': form,
        'target_user': target,
    })


@login_required
@admin_required
def company_search_api(request):
    """Pesquisa empresas activas para o selector de empresas do utilizador."""
    q = request.GET.get('q', '').strip()
    companies = Company.objects.filter(is_active=True)
    if q:
        companies = companies.filter(name__icontains=q)
    companies = companies.order_by('name')[:12]
    return JsonResponse({
        'results': [{'id': str(c.id), 'name': c.name} for c in companies]
    })


# ─────────────────────────────────────────────────────────────────────────────
# TOTP / 2FA views
# ─────────────────────────────────────────────────────────────────────────────

@login_required
@require_http_methods(['POST'])
def totp_setup_view(request, user_id):
    """Generate a new TOTP secret and return QR code as base64 JSON.
    The secret is stored in the session until verified.
    Only the user themselves or an admin may call this.
    """
    from django.shortcuts import get_object_or_404
    import pyotp, qrcode, io, base64

    target = get_object_or_404(CustomUser, id=user_id)
    is_self = (request.user.pk == target.pk)
    if not is_self and request.user.role != CustomUser.ADMIN:
        return JsonResponse({'error': 'Sem permissão.'}, status=403)

    secret = pyotp.random_base32()
    request.session[f'totp_pending_{target.pk}'] = secret

    app_name = 'Fuet Mágico'
    display_name = target.get_full_name() or target.username
    uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=display_name,
        issuer_name=app_name,
    )

    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    qr_b64 = 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

    return JsonResponse({'qr': qr_b64, 'secret': secret})


@login_required
@require_http_methods(['POST'])
def totp_verify_view(request, user_id):
    """Verify a TOTP code and, if valid, activate 2FA for the user."""
    from django.shortcuts import get_object_or_404
    import pyotp

    target = get_object_or_404(CustomUser, id=user_id)
    is_self = (request.user.pk == target.pk)
    if not is_self and request.user.role != CustomUser.ADMIN:
        return JsonResponse({'error': 'Sem permissão.'}, status=403)

    code = (request.POST.get('code') or '').strip()
    secret = request.session.get(f'totp_pending_{target.pk}', '')
    if not secret:
        return JsonResponse({'error': 'Sessão expirada. Reinicia o processo.'}, status=400)

    totp = pyotp.TOTP(secret)
    if not totp.verify(code, valid_window=1):
        return JsonResponse({'error': 'Código inválido. Tenta novamente.'}, status=400)

    target.totp_secret = secret
    target.totp_enabled = True
    target.save(update_fields=['totp_secret', 'totp_enabled'])
    request.session.pop(f'totp_pending_{target.pk}', None)
    return JsonResponse({'ok': True})


@login_required
@require_http_methods(['POST'])
def totp_disable_view(request, user_id):
    """Disable 2FA for a user.
    Self requires their current TOTP code; admins can disable without code.
    """
    from django.shortcuts import get_object_or_404
    import pyotp

    target = get_object_or_404(CustomUser, id=user_id)
    is_self = (request.user.pk == target.pk)
    is_admin = (request.user.role == CustomUser.ADMIN)

    if not is_self and not is_admin:
        return JsonResponse({'error': 'Sem permissão.'}, status=403)

    if is_self and not is_admin:
        code = (request.POST.get('code') or '').strip()
        if not target.totp_secret:
            return JsonResponse({'error': '2FA não está ativo.'}, status=400)
        totp = pyotp.TOTP(target.totp_secret)
        if not totp.verify(code, valid_window=1):
            return JsonResponse({'error': 'Código inválido.'}, status=400)

    target.totp_secret = ''
    target.totp_enabled = False
    target.save(update_fields=['totp_secret', 'totp_enabled'])
    return JsonResponse({'ok': True})


# ───────────────────────────────────────────────────────────────────────────────
# SMTP Config (admin editing another user)
# ───────────────────────────────────────────────────────────────────────────────
@login_required
@require_http_methods(['POST'])
def user_smtp_save(request, user_id):
    """Save SMTP config for a user (admin can configure for any user; self for own)."""
    from django.shortcuts import get_object_or_404
    target = get_object_or_404(CustomUser, id=user_id)
    is_self = (request.user.pk == target.pk)
    is_admin = (request.user.role == CustomUser.ADMIN)

    if not is_self and not is_admin:
        return JsonResponse({'success': False, 'error': 'Sem permissão.'}, status=403)

    email_address = request.POST.get('email_address', '').strip()
    app_password_raw = request.POST.get('app_password', '').strip()
    provider = request.POST.get('provider', '').strip()

    if provider not in dict(UserEmailConfig.PROVIDER_CHOICES):
        return JsonResponse({'success': False, 'error': 'Provedor inválido.'}, status=400)

    config, _ = UserEmailConfig.objects.get_or_create(user=target)
    config.email_address = email_address
    config.provider = provider

    if app_password_raw:
        try:
            config.app_password = encrypt_password(app_password_raw)
        except ValueError as e:
            return JsonResponse({'success': False, 'error': f'Erro de encriptação: {e}'}, status=500)
    elif not email_address:
        config.app_password = ''

    config.save()
    return JsonResponse({'success': True, 'has_smtp': config.has_smtp_configured})


@login_required
@require_http_methods(['POST'])
def user_smtp_test(request, user_id):
    """Send a test email using the target user's SMTP config."""
    from django.shortcuts import get_object_or_404
    from apps.core.email_utils import _send_via_smtp
    target = get_object_or_404(CustomUser, id=user_id)
    is_self = (request.user.pk == target.pk)
    is_admin = (request.user.role == CustomUser.ADMIN)

    if not is_self and not is_admin:
        return JsonResponse({'success': False, 'error': 'Sem permissão.'}, status=403)

    try:
        config = target.email_config
    except UserEmailConfig.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'SMTP não configurado.'})

    if not config.has_smtp_configured:
        return JsonResponse({'success': False, 'error': 'SMTP não configurado.'})

    success, error, _ = _send_via_smtp(
        config=config,
        to_email=config.email_address,
        to_name=target.get_full_name(),
        subject='Teste SMTP — Fuet Mágico CRM',
        body=(
            f'Olá {target.get_full_name() or target.username},\n\n'
            'Este é um email de teste para confirmar que o SMTP está corretamente configurado no Fuet Mágico CRM.\n\nBom trabalho!'
        ),
        body_html=None,
        sender_name=target.get_full_name() or target.username,
    )
    if success:
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': error})

