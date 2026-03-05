from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderLine, PaymentTerm


class PurchaseOrderLineInline(admin.TabularInline):
    model = PurchaseOrderLine
    extra = 0
    fields = ('product', 'uom', 'quantity', 'unit_price', 'tax_rate')
    autocomplete_fields = ['product']
    readonly_fields = []


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'supplier', 'order_date', 'status', 'total', 'owner_company')
    list_filter = ('status', 'order_date', 'owner_company')
    search_fields = ('order_number', 'supplier__name')
    readonly_fields = ('order_number', 'subtotal', 'tax', 'total', 'created_at', 'updated_at')
    inlines = [PurchaseOrderLineInline]

    fieldsets = (
        ('Identificação', {'fields': ('order_number', 'status', 'owner_company')}),
        ('Fornecedor & Datas', {'fields': ('supplier', 'order_date', 'expected_delivery_date', 'payment_terms')}),
        ('Totais', {'fields': ('subtotal', 'tax', 'total')}),
        ('Notas', {'fields': ('notes',)}),
    )


@admin.register(PaymentTerm)
class PaymentTermAdmin(admin.ModelAdmin):
    list_display = ('name', 'days', 'is_default', 'is_active', 'owner_company')
    list_filter = ('is_default', 'is_active', 'owner_company')
    search_fields = ('name',)
