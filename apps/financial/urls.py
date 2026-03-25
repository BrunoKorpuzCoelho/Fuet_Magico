from django.urls import path
from . import views

app_name = 'financial'

urlpatterns = [
    path('', views.financial_index, name='index'),
    path('reports/pnl/', views.report_pnl, name='report_pnl'),
    path('reports/sales/period/', views.report_sales_period, name='report_sales_period'),
    path('reports/sales/products/', views.report_sales_products, name='report_sales_products'),
    path('reports/sales/clients/', views.report_sales_clients, name='report_sales_clients'),
    path('reports/sales/evolution/', views.report_sales_evolution, name='report_sales_evolution'),
    path('reports/purchases/period/', views.report_purchases_period, name='report_purchases_period'),
    path('reports/purchases/suppliers/', views.report_purchases_suppliers, name='report_purchases_suppliers'),
    path('reports/losses/', views.report_stock_losses, name='report_stock_losses'),
    path('reports/margins/', views.report_margins, name='report_margins'),
    path('reports/annual/', views.report_annual_comparison, name='report_annual_comparison'),
]
