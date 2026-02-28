from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_dashboard, name='inventory_dashboard'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<uuid:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<uuid:pk>/products/search/', views.category_products_search, name='category_products_search'),
    path('categories/<uuid:pk>/products/add/', views.category_products_add, name='category_products_add'),
    path('categories/<uuid:pk>/products/<uuid:product_pk>/remove/', views.category_products_remove, name='category_products_remove'),
    path('categories/bulk-archive/', views.bulk_archive_categories, name='bulk_archive_categories'),
    path('categories/bulk-unarchive/', views.bulk_unarchive_categories, name='bulk_unarchive_categories'),
    path('categories/bulk-delete/', views.bulk_delete_categories, name='bulk_delete_categories'),

    # UoM
    path('uom/', views.uom_list, name='uom_list'),
    path('uom/create/', views.uom_create, name='uom_create'),
    path('uom/<uuid:pk>/edit/', views.uom_edit, name='uom_edit'),
    path('uom/bulk-archive/', views.bulk_archive_uoms, name='bulk_archive_uoms'),
    path('uom/bulk-unarchive/', views.bulk_unarchive_uoms, name='bulk_unarchive_uoms'),
    path('uom/bulk-delete/', views.bulk_delete_uoms, name='bulk_delete_uoms'),

    # UoM Categories
    path('uom-categories/', views.uom_category_list, name='uom_category_list'),
    path('uom-categories/create/', views.uom_category_create, name='uom_category_create'),
    path('uom-categories/<uuid:pk>/edit/', views.uom_category_edit, name='uom_category_edit'),
    path('uom-categories/bulk-archive/', views.bulk_archive_uom_categories, name='bulk_archive_uom_categories'),
    path('uom-categories/bulk-unarchive/', views.bulk_unarchive_uom_categories, name='bulk_unarchive_uom_categories'),
    path('uom-categories/bulk-delete/', views.bulk_delete_uom_categories, name='bulk_delete_uom_categories'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<uuid:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/bulk-archive/', views.bulk_archive_products, name='bulk_archive_products'),
    path('products/bulk-unarchive/', views.bulk_unarchive_products, name='bulk_unarchive_products'),
    path('products/bulk-delete/', views.bulk_delete_products, name='bulk_delete_products'),

    # Warehouses
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouses/create/', views.warehouse_create, name='warehouse_create'),
    path('warehouses/<uuid:pk>/edit/', views.warehouse_edit, name='warehouse_edit'),
    path('warehouses/bulk-archive/', views.bulk_archive_warehouses, name='bulk_archive_warehouses'),
    path('warehouses/bulk-unarchive/', views.bulk_unarchive_warehouses, name='bulk_unarchive_warehouses'),
    path('warehouses/bulk-delete/', views.bulk_delete_warehouses, name='bulk_delete_warehouses'),
]
