from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # Pipeline / Kanban (Default View)
    path('', views.lead_pipeline_view, name='crm_home'),  # /crm/ → Pipeline (DEFAULT)
    path('pipeline/', views.lead_pipeline_view, name='lead_pipeline'),  # Alias
    
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
]
