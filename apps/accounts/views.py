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
from .models import UserEmailConfig


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
