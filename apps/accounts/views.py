from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from .forms import LoginForm


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard:index')


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('accounts:login')
