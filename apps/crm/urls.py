from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # Pipeline / Kanban (Default View)
    path('', views.lead_pipeline_view, name='crm_home'),  # /crm/ → Pipeline (DEFAULT)
    path('pipeline/', views.lead_pipeline_view, name='lead_pipeline'),  # Alias
    path('list/', views.lead_list_view, name='lead_list'),  # List View
    
    # Lead CRUD
    path('leads/new/', views.lead_create_view, name='lead_create'),
    path('leads/<uuid:lead_id>/', views.lead_detail_view, name='lead_detail'),
    path('leads/bulk-delete/', views.bulk_delete_leads, name='bulk_delete_leads'),
    path('leads/bulk-mark-won/', views.bulk_mark_won, name='bulk_mark_won'),
    path('leads/bulk-mark-lost/', views.bulk_mark_lost, name='bulk_mark_lost'),
    
    # Lead Actions (API)
    path('leads/<uuid:lead_id>/change-stage/', views.lead_change_stage, name='lead_change_stage'),
    
    # Configuração
    path('lost-reasons/', views.lost_reasons_list_view, name='lost_reasons_list'),
    
    # Tipos de Atividade (Configuração)
    path('activity-types/', views.activity_type_list_view, name='activity_type_list'),
    path('activity-types/new/', views.activity_type_create_view, name='activity_type_create'),
    path('activity-types/<uuid:type_id>/edit/', views.activity_type_edit_view, name='activity_type_edit'),
    path('activity-types/bulk-archive/', views.bulk_archive_activity_types, name='bulk_archive_activity_types'),
    path('activity-types/bulk-unarchive/', views.bulk_unarchive_activity_types, name='bulk_unarchive_activity_types'),
    path('activity-types/bulk-delete/', views.bulk_delete_activity_types, name='bulk_delete_activity_types'),
    
    # Activity Chains (Cadeias de Atividade)
    path('activity-chains/', views.activity_chain_list_view, name='activity_chain_list'),
    path('activity-chains/new/', views.activity_chain_create_view, name='activity_chain_create'),
    path('activity-chains/<uuid:chain_id>/edit/', views.activity_chain_edit_view, name='activity_chain_edit'),
    path('activity-chains/bulk-archive/', views.bulk_archive_chains, name='bulk_archive_chains'),
    path('activity-chains/bulk-unarchive/', views.bulk_unarchive_chains, name='bulk_unarchive_chains'),
    path('activity-chains/bulk-delete/', views.bulk_delete_chains, name='bulk_delete_chains'),

    # Activities (Atividades)
    path('activities/', views.activities_list_view, name='activities_list'),
    path('activities/new/', views.activity_create_view, name='activity_create'),
    path('activities/<uuid:activity_id>/edit/', views.activity_edit_view, name='activity_edit'),
    path('activities/bulk-archive/', views.bulk_archive_activities, name='bulk_archive_activities'),
    path('activities/bulk-unarchive/', views.bulk_unarchive_activities, name='bulk_unarchive_activities'),
    path('activities/bulk-delete/', views.bulk_delete_activities, name='bulk_delete_activities'),
    path('activities/bulk-duplicate/', views.bulk_duplicate_activities, name='bulk_duplicate_activities'),
    
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

    # Lead Activities (atividades de uma lead específica)
    path('leads/<uuid:lead_id>/activities/create/', views.lead_activity_create, name='lead_activity_create'),
    path('leads/<uuid:lead_id>/activities/<uuid:activity_id>/done/', views.lead_activity_mark_done, name='lead_activity_mark_done'),
    path('leads/<uuid:lead_id>/activities/<uuid:activity_id>/delete/', views.lead_activity_delete, name='lead_activity_delete'),
    path('leads/<uuid:lead_id>/activities/<uuid:activity_id>/update/', views.lead_activity_update, name='lead_activity_update'),

    # Lead Chain Start
    path('leads/<uuid:lead_id>/chains/start/', views.lead_chain_start, name='lead_chain_start'),
]
