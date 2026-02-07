from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.contact_list_view, name='contact_list'),
    path('bulk-archive/', views.bulk_archive_contacts, name='bulk_archive'),
]
