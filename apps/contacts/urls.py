from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.contact_list_view, name='contact_list'),
    path('new/', views.contact_create_view, name='contact_create'),
    path('<uuid:contact_id>/edit/', views.contact_edit_view, name='contact_edit'),
    path('create-associated/', views.create_associated_contact, name='create_associated'),
    path('associate-existing/', views.associate_existing_contact, name='associate_existing'),
    path('api/search/', views.search_contacts_api, name='search_api'),
    path('<uuid:company_id>/remove-association/<uuid:employee_id>/', views.remove_association, name='remove_association'),
    path('bulk-archive/', views.bulk_archive_contacts, name='bulk_archive'),
    path('bulk-unarchive/', views.bulk_unarchive_contacts, name='bulk_unarchive'),
    path('bulk-delete/', views.bulk_delete_contacts, name='bulk_delete'),
    path('find-duplicates/', views.find_duplicates, name='find_duplicates'),
    
    # Tags URLs
    path('tags/', views.tag_list_view, name='tag_list'),
    path('tags/bulk-archive/', views.bulk_archive_tags, name='bulk_archive_tags'),
    path('tags/bulk-unarchive/', views.bulk_unarchive_tags, name='bulk_unarchive_tags'),
    path('tags/bulk-delete/', views.bulk_delete_tags, name='bulk_delete_tags'),
]
