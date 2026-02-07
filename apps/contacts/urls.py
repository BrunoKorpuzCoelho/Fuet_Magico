from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.contact_list_view, name='contact_list'),
    path('bulk-archive/', views.bulk_archive_contacts, name='bulk_archive'),
    path('bulk-unarchive/', views.bulk_unarchive_contacts, name='bulk_unarchive'),
    path('bulk-delete/', views.bulk_delete_contacts, name='bulk_delete'),
    path('find-duplicates/', views.find_duplicates, name='find_duplicates'),
]
