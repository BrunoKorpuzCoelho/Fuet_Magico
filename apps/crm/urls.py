from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # Pipeline / Kanban (Default View)
    path('', views.lead_pipeline_view, name='crm_home'),  # /crm/ → Pipeline (DEFAULT)
    path('pipeline/', views.lead_pipeline_view, name='lead_pipeline'),  # Alias
    
    # Lead CRUD
    path('leads/new/', views.lead_create_view, name='lead_create'),
    path('leads/<uuid:lead_id>/', views.lead_detail_view, name='lead_detail'),
    
    # Lead Actions (API)
    path('leads/<uuid:lead_id>/change-stage/', views.lead_change_stage, name='lead_change_stage'),
    
    # Stages (Configuração)
    path('stages/', views.stage_list_view, name='stage_list'),
    path('stages/new/', views.stage_create_view, name='stage_create'),
    path('stages/<uuid:stage_id>/edit/', views.stage_edit_view, name='stage_edit'),
    path('stages/create/', views.stage_create, name='stage_create_api'),
    path('stages/<uuid:pk>/reorder/', views.stage_reorder, name='stage_reorder'),
    path('stages/reorder-all/', views.stage_reorder_all, name='stage_reorder_all'),
    path('stages/<uuid:pk>/delete/', views.stage_delete, name='stage_delete'),
    path('stages/duplicate/', views.stage_duplicate, name='stage_duplicate'),
    path('stages/bulk-delete/', views.stage_bulk_delete, name='stage_bulk_delete'),
    
    # CRM Tags
    path('tags/', views.crm_tag_list_view, name='crm_tag_list'),
    path('tags/new/', views.crm_tag_create_view, name='crm_tag_create'),
    path('tags/<uuid:tag_id>/edit/', views.crm_tag_edit_view, name='crm_tag_edit'),
    path('tags/bulk-archive/', views.crm_bulk_archive_tags, name='crm_bulk_archive_tags'),
    path('tags/bulk-unarchive/', views.crm_bulk_unarchive_tags, name='crm_bulk_unarchive_tags'),
    path('tags/bulk-delete/', views.crm_bulk_delete_tags, name='crm_bulk_delete_tags'),
    
    # CRM Tags API
    path('api/tags/check-leads/', views.crm_check_tags_leads, name='crm_check_tags_leads'),
    path('api/tags/search/', views.crm_search_tags_api, name='crm_search_tags_api'),
    path('api/tags/quick-create/', views.crm_quick_create_tag_api, name='crm_quick_create_tag_api'),
    
    # Contact Search API (for lead form)
    path('api/contacts/search/', views.search_contacts_for_lead_api, name='search_contacts_for_lead'),
]
