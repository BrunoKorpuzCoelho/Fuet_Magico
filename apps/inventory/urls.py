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
    path('products/<uuid:pk>/forecast/', views.product_forecast, name='product_forecast'),
    path('products/<uuid:pk>/suppliers/', views.product_suppliers_api, name='product_suppliers_api'),
    path('products/<uuid:pk>/suppliers/<uuid:si_pk>/', views.product_supplier_detail_api, name='product_supplier_detail_api'),
    path('products/search/', views.product_search, name='product_search'),
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

    # Operations — Receipts & Deliveries
    path('operations/receipts/', views.receipt_list, name='receipt_list'),
    path('operations/receipts/new/', views.receipt_create, name='receipt_create'),
    path('operations/deliveries/', views.delivery_list, name='delivery_list'),
    path('operations/deliveries/new/', views.delivery_create, name='delivery_create'),
    path('operations/adjustments/', views.adjustment_list, name='adjustment_list'),
    path('operations/adjustments/new/', views.adjustment_create, name='adjustment_create'),
    path('operations/scrap/', views.scrap_list, name='scrap_list'),
    path('operations/scrap/new/', views.scrap_create, name='scrap_create'),
    path('operations/movements/<uuid:pk>/edit/', views.movement_edit, name='movement_edit'),
    path('operations/movements/<uuid:pk>/validate/', views.movement_validate, name='movement_validate'),
    path('operations/movements/<uuid:pk>/cancel/', views.movement_cancel, name='movement_cancel'),
    path('operations/movements/<uuid:pk>/lines/add/', views.movement_line_add, name='movement_line_add'),
    path('operations/movements/<uuid:movement_pk>/lines/<uuid:line_pk>/update/', views.movement_line_update, name='movement_line_update'),
    path('operations/movements/<uuid:movement_pk>/lines/<uuid:line_pk>/delete/', views.movement_line_delete, name='movement_line_delete'),
    # Chatter — Notes & Followers
    path('operations/movements/<uuid:pk>/notes/', views.movement_notes_list, name='movement_notes_list'),
    path('operations/movements/<uuid:pk>/notes/create/', views.movement_note_create, name='movement_note_create'),
    path('operations/movements/<uuid:pk>/followers/', views.movement_followers_api, name='movement_followers_api'),
    path('operations/movements/<uuid:pk>/followers/<uuid:user_id>/remove/', views.movement_follower_remove_api, name='movement_follower_remove_api'),
    # Physical Inventory
    path('operations/physical-inventory/', views.physical_inventory_list, name='physical_inventory_list'),
    path('operations/bulk-archive/', views.bulk_archive_movements, name='bulk_archive_movements'),
    path('operations/bulk-unarchive/', views.bulk_unarchive_movements, name='bulk_unarchive_movements'),
    path('operations/bulk-delete/', views.bulk_delete_movements, name='bulk_delete_movements'),

    # All movements (global list)
    path('operations/movements/', views.all_movements_list, name='all_movements_list'),

    # Tools
    path('tools/run-low-stock-check/', views.run_low_stock_check, name='run_low_stock_check'),

    # Reports
    path('reports/', views.inventory_reports, name='inventory_reports'),
    path('reports/valuation/', views.report_valuation, name='report_valuation'),
    path('reports/balance/', views.report_balance, name='report_balance'),
    path('reports/purchase-prices/', views.report_purchase_prices, name='report_purchase_prices'),
    path('reports/scrap/', views.report_scrap, name='report_scrap'),

    # Lista de Compras
    path('listas-de-compras/', views.purchase_list_index, name='purchase_list_index'),
    path('listas-de-compras/nova/', views.purchase_list_create, name='purchase_list_create'),
    path('listas-de-compras/auto-generate/', views.purchase_list_auto_generate, name='purchase_list_auto_generate'),
    path('listas-de-compras/<uuid:pk>/editar/', views.purchase_list_edit, name='purchase_list_edit'),
    path('listas-de-compras/<uuid:pk>/confirmar/', views.purchase_list_confirm, name='purchase_list_confirm'),
    path('listas-de-compras/<uuid:pk>/concluir/', views.purchase_list_done, name='purchase_list_done'),
    path('listas-de-compras/<uuid:pk>/mobile/', views.purchase_list_mobile, name='purchase_list_mobile'),
    path('listas-de-compras/<uuid:pk>/lines/<uuid:line_pk>/update-qty/', views.purchase_list_line_update_qty, name='purchase_list_line_update_qty'),
    path('listas-de-compras/<uuid:pk>/mobile/add-line/', views.purchase_list_mobile_add_line, name='purchase_list_mobile_add_line'),
    path('listas-de-compras/<uuid:pk>/cancelar/', views.purchase_list_cancel, name='purchase_list_cancel'),
    # Chatter — Notes & Followers
    path('listas-de-compras/<uuid:pk>/notes/', views.purchase_list_notes_list, name='purchase_list_notes_list'),
    path('listas-de-compras/<uuid:pk>/notes/create/', views.purchase_list_note_create, name='purchase_list_note_create'),
    path('listas-de-compras/<uuid:pk>/followers/', views.purchase_list_followers_api, name='purchase_list_followers_api'),
    path('listas-de-compras/<uuid:pk>/followers/<uuid:user_id>/remove/', views.purchase_list_follower_remove, name='purchase_list_follower_remove'),
    path('listas-de-compras/bulk-archive/', views.bulk_archive_purchase_lists, name='purchase_list_bulk_archive'),
    path('listas-de-compras/bulk-unarchive/', views.bulk_unarchive_purchase_lists, name='purchase_list_bulk_unarchive'),
    path('listas-de-compras/bulk-delete/', views.bulk_delete_purchase_lists, name='purchase_list_bulk_delete'),
]
