from django.urls import path
from . import views

app_name = 'bom'

urlpatterns = [
    path('', views.bom_dashboard, name='bom_dashboard'),
    path('receitas/', views.bom_list, name='bom_list'),
    path('novo/', views.bom_create, name='bom_create'),
    path('<uuid:bom_id>/editar/', views.bom_edit, name='bom_edit'),
    # Lines API
    path('<uuid:bom_id>/lines/', views.bom_lines_api, name='bom_lines_api'),
    path('<uuid:bom_id>/lines/<uuid:line_id>/', views.bom_line_detail_api, name='bom_line_detail_api'),
    # Bulk actions
    path('bulk-archive/', views.bom_bulk_archive, name='bulk_archive'),
    path('bulk-unarchive/', views.bom_bulk_unarchive, name='bulk_unarchive'),
    path('bulk-delete/', views.bom_bulk_delete, name='bulk_delete'),
    # Relatórios
    path('relatorios/', views.bom_reports, name='bom_reports'),
    path('relatorios/custo/', views.report_bom_cost_analysis, name='report_cost_analysis'),
    path('relatorios/margem/', views.report_bom_margin, name='report_margin'),
    path('relatorios/custo-vs-venda/', views.report_bom_cost_vs_sale, name='report_cost_vs_sale'),
    path('relatorios/materiais/', views.report_bom_materials_needed, name='report_materials_needed'),
    path('relatorios/stock-vs-necessidade/', views.report_bom_stock_vs_need, name='report_stock_vs_need'),
]
