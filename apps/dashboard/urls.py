from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='index'),
    path('toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),
    path('toggle-developer-mode/', views.toggle_developer_mode, name='toggle_developer_mode'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/email-layout/', views.email_layout_view, name='email_layout'),
    path('settings/email-layout/reset/', views.email_layout_reset_view, name='email_layout_reset'),
    path('settings/email-templates/', views.email_template_list_view, name='email_template_list'),
    path('settings/email-templates/new/', views.email_template_create_view, name='email_template_create'),
    path('settings/email-templates/<uuid:template_id>/edit/', views.email_template_edit_view, name='email_template_edit'),
    path('settings/email-templates/<uuid:template_id>/reset-body/', views.email_template_reset_body_view, name='email_template_reset_body'),
    path('settings/email-templates/bulk-archive/', views.email_template_bulk_archive, name='email_template_bulk_archive'),
    path('settings/email-templates/bulk-unarchive/', views.email_template_bulk_unarchive, name='email_template_bulk_unarchive'),
    path('settings/email-templates/bulk-delete/', views.email_template_bulk_delete, name='email_template_bulk_delete'),
    path('settings/document-layout/', views.document_layout_view, name='document_layout'),
    path('settings/document-sequences/', views.document_sequence_list_view, name='document_sequences'),
    path('settings/document-sequences/<uuid:seq_id>/save/', views.document_sequence_save_view, name='document_sequence_save'),
    path('settings/document-sequences/create/', views.document_sequence_create_view, name='document_sequence_create'),
    path('settings/document-sequences/generate/', views.document_sequence_generate_view, name='document_sequence_generate'),
    path('settings/document-sequences/<uuid:seq_id>/edit/', views.document_sequence_edit_view, name='document_sequence_edit'),
    path('settings/document-sequences/bulk-archive/', views.document_sequence_bulk_archive_view, name='document_sequence_bulk_archive'),
    path('settings/document-sequences/bulk-unarchive/', views.document_sequence_bulk_unarchive_view, name='document_sequence_bulk_unarchive'),
    path('settings/document-sequences/bulk-delete/', views.document_sequence_bulk_delete_view, name='document_sequence_bulk_delete'),
]
