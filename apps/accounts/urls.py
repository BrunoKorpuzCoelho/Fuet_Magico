from django.urls import path
from .views import (
    LoginView, LogoutView, switch_company, profile_settings, test_smtp,
    user_list_view, user_create_view, user_edit_view,
    user_toggle_active, user_send_reset_email, password_reset_confirm,
    user_bulk_archive, user_bulk_unarchive, user_bulk_delete, user_bulk_reset,
    user_delete_single, company_search_api,
    totp_setup_view, totp_verify_view, totp_disable_view,
    user_smtp_save, user_smtp_test,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('switch-company/<uuid:company_id>/', switch_company, name='switch_company'),
    path('perfil/', profile_settings, name='profile_settings'),
    path('perfil/testar-smtp/', test_smtp, name='test_smtp'),

    # ── User Management (ADMIN only) ──────────────────────────────────────
    path('users/', user_list_view, name='user_list'),
    path('users/new/', user_create_view, name='user_create'),
    path('users/<int:user_id>/edit/', user_edit_view, name='user_edit'),
    path('users/<int:user_id>/toggle-active/', user_toggle_active, name='user_toggle_active'),
    path('users/<int:user_id>/send-reset/', user_send_reset_email, name='user_send_reset'),
    path('users/<int:user_id>/delete/', user_delete_single, name='user_delete'),
    path('users/bulk-archive/', user_bulk_archive, name='user_bulk_archive'),
    path('users/bulk-unarchive/', user_bulk_unarchive, name='user_bulk_unarchive'),
    path('users/bulk-delete/', user_bulk_delete, name='user_bulk_delete'),
    path('users/bulk-reset/', user_bulk_reset, name='user_bulk_reset'),

    # ── API ────────────────────────────────────────────────────────────────
    path('api/companies/', company_search_api, name='company_search'),

    # ── TOTP / 2FA ────────────────────────────────────────────────────────
    path('users/<int:user_id>/2fa/setup/',   totp_setup_view,   name='totp_setup'),
    path('users/<int:user_id>/2fa/verify/',  totp_verify_view,  name='totp_verify'),
    path('users/<int:user_id>/2fa/disable/', totp_disable_view, name='totp_disable'),

    # ── SMTP ────────────────────────────────────────────────────────────────────────
    path('users/<int:user_id>/smtp/save/', user_smtp_save, name='user_smtp_save'),
    path('users/<int:user_id>/smtp/test/', user_smtp_test, name='user_smtp_test'),

    # ── Password Reset (public, token-based) ─────────────────────────────
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]
