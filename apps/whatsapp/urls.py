from django.urls import path
from . import views

app_name = 'whatsapp'

urlpatterns = [
    path('', views.template_list_view, name='template_list'),
    path('novo/', views.template_create_view, name='template_create'),
    path('<uuid:pk>/editar/', views.template_edit_view, name='template_edit'),
    path('<uuid:pk>/submeter/', views.template_submit_view, name='template_submit'),
    path('<uuid:pk>/arquivar/', views.template_archive_view, name='template_archive'),
    path('<uuid:pk>/desarquivar/', views.template_unarchive_view, name='template_unarchive'),
    path('<uuid:pk>/eliminar/', views.template_delete_view, name='template_delete'),
    path('bulk/', views.bulk_action_view, name='bulk_action'),
    # Notes (chatter)
    path('<uuid:template_id>/notas/', views.template_notes_list, name='template_notes_list'),
    path('<uuid:template_id>/notas/criar/', views.template_note_create, name='template_note_create'),
    # Followers (chatter)
    path('<uuid:template_id>/seguidores/', views.template_followers_api, name='template_followers_api'),
    path('<uuid:template_id>/seguidores/<uuid:user_id>/remover/', views.template_follower_remove_api, name='template_follower_remove_api'),
    # Activities
    path('<uuid:template_id>/atividades/criar/', views.template_activity_create, name='template_activity_create'),
    path('<uuid:template_id>/atividades/<uuid:activity_id>/concluir/', views.template_activity_done, name='template_activity_done'),
    path('<uuid:template_id>/atividades/<uuid:activity_id>/eliminar/', views.template_activity_delete, name='template_activity_delete'),
]
