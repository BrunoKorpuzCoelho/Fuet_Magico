from django.urls import path
from .views import LoginView, LogoutView, switch_company, profile_settings, test_smtp

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('switch-company/<uuid:company_id>/', switch_company, name='switch_company'),
    path('perfil/', profile_settings, name='profile_settings'),
    path('perfil/testar-smtp/', test_smtp, name='test_smtp'),
]
