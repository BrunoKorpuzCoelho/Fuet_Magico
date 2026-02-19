from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Logs APIs
    path('api/audit-logs/', views.audit_logs_api, name='audit_logs_api'),
    path('api/error-logs/', views.error_logs_api, name='error_logs_api'),
    path('api/application-logs/', views.application_logs_api, name='application_logs_api'),
    
    # Logs Views (DevTools)
    path('devtools/logs/application/', views.application_logs_view, name='application_logs_view'),
    path('devtools/logs/error/', views.error_logs_view, name='error_logs_view'),
    path('devtools/logs/audit/', views.audit_logs_view, name='audit_logs_view'),
    
    # Chatter APIs
    path('api/chatter/message/', views.chatter_create_message, name='chatter_create_message'),
    path('api/chatter/whatsapp/', views.chatter_send_whatsapp, name='chatter_send_whatsapp'),
    path('api/users/search/', views.users_search_api, name='users_search_api'),

    # Planned Activities API
    path('api/chatter/planned-activity/create/', views.planned_activity_create, name='planned_activity_create'),
    path('api/chatter/planned-activity/<uuid:pk>/done/', views.planned_activity_done, name='planned_activity_done'),
    path('api/chatter/planned-activity/<uuid:pk>/cancel/', views.planned_activity_cancel, name='planned_activity_cancel'),
    path('api/chatter/planned-activity/<uuid:pk>/edit/', views.planned_activity_edit, name='planned_activity_edit'),
]
