from django.contrib import admin
from .models import SaleOrder, SaleOrderLine, PaymentTerm


class SaleOrderLineInline(admin.TabularInline):
    model = SaleOrderLine
    extra = 0
    fields = ('product', 'uom', 'quantity', 'unit_price', 'tax_rate')


@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'client', 'document_type', 'order_date', 'status', 'payment_status', 'total', 'owner_company')
    list_filter = ('status', 'document_type', 'payment_status')
    search_fields = ('order_number', 'client__name')
    inlines = [SaleOrderLineInline]


@admin.register(SaleOrderLine)
class SaleOrderLineAdmin(admin.ModelAdmin):
    list_display = ('sale_order', 'product', 'quantity', 'unit_price', 'tax_rate')


@admin.register(PaymentTerm)
class PaymentTermAdmin(admin.ModelAdmin):
    list_display = ('name', 'days', 'is_default', 'is_active', 'owner_company')
    list_filter = ('is_active', 'is_default')
    search_fields = ('name',)
