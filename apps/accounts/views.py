from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from apps.core.models import Company
from .forms import LoginForm


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
