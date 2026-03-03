from django.contrib import admin
from .models import Category, UoMCategory, UoM, Product, Warehouse, StockMovement, StockMovementLine, StockQuant, ProductSupplierInfo


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_default', 'owner_company', 'is_active']
    list_filter = ['is_active', 'is_default', 'owner_company']
    search_fields = ['name', 'code']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = [
        ('Informação', {
            'fields': ['name', 'code', 'address', 'is_default']
        }),
        ('Multi-Company', {
            'fields': ['owner_company'],
            'classes': ['collapse']
        }),
        ('Sistema', {
            'fields': ['id', 'is_active', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(UoMCategory)
class UoMCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner_company', 'is_active', 'created_at']
    list_filter = ['is_active', 'owner_company']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = [
        ('Informação', {
            'fields': ['name']
        }),
        ('Multi-Company', {
            'fields': ['owner_company'],
            'classes': ['collapse']
        }),
        ('Sistema', {
            'fields': ['id', 'is_active', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(UoM)
class UoMAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'category', 'uom_type', 'factor', 'rounding', 'is_active']
    list_filter = ['is_active', 'category', 'uom_type', 'owner_company']
    search_fields = ['name', 'symbol']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = [
        ('Informação', {
            'fields': ['name', 'symbol', 'category', 'uom_type', 'factor', 'rounding']
        }),
        ('Multi-Company', {
            'fields': ['owner_company'],
            'classes': ['collapse']
        }),
        ('Sistema', {
            'fields': ['id', 'is_active', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'owner_company', 'is_active', 'created_at']
    list_filter = ['is_active', 'owner_company', 'parent']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = [
        ('Informação', {
            'fields': ['name', 'description', 'parent']
        }),
        ('Multi-Company', {
            'fields': ['owner_company'],
            'classes': ['collapse']
        }),
        ('Sistema', {
            'fields': ['id', 'is_active', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'internal_reference', 'category', 'product_type', 'uom', 'sale_price', 'cost_price', 'is_active']
    list_filter = ['is_active', 'product_type', 'category', 'owner_company']
    search_fields = ['name', 'internal_reference', 'reference', 'barcode', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = [
        ('Identificação', {
            'fields': ['name', 'internal_reference', 'reference', 'barcode', 'description', 'image']
        }),
        ('Classificação', {
            'fields': ['product_type', 'category']
        }),
        ('Unidades de Medida', {
            'fields': ['uom', 'uom_purchase']
        }),
        ('Preços', {
            'fields': ['sale_price', 'cost_price', 'tax_rate']
        }),
        ('Compras', {
            'fields': ['supplier'],
            'classes': ['collapse']
        }),
        ('Multi-Company', {
            'fields': ['owner_company'],
            'classes': ['collapse']
        }),
        ('Sistema', {
            'fields': ['id', 'is_active', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(StockQuant)
class StockQuantAdmin(admin.ModelAdmin):
    list_display = ['product', 'warehouse', 'quantity', 'is_active']
    list_filter = ['warehouse', 'is_active']
    search_fields = ['product__name', 'product__internal_reference']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = [
        ('Stock', {
            'fields': ['product', 'warehouse', 'quantity']
        }),
        ('Sistema', {
            'fields': ['id', 'is_active', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


class StockMovementLineInline(admin.TabularInline):
    model = StockMovementLine
    extra = 1
    fields = ['product', 'quantity', 'uom', 'unit_price']
    readonly_fields = ['id']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    inlines = [StockMovementLineInline]
    list_display = ['reference', 'movement_type', 'partner', 'state', 'date', 'warehouse', 'responsible']
    list_filter = ['state', 'movement_type', 'warehouse', 'owner_company']
    search_fields = ['reference', 'origin', 'notes']
    readonly_fields = ['id', 'reference', 'created_at', 'updated_at']
    date_hierarchy = 'date'

    fieldsets = [
        ('Movimento', {
            'fields': ['reference', 'movement_type', 'warehouse', 'state', 'date']
        }),
        ('Parceiro', {
            'fields': ['partner', 'origin'],
        }),
        ('Detalhes', {
            'fields': ['notes', 'responsible'],
        }),
        ('Multi-Company', {
            'fields': ['owner_company'],
            'classes': ['collapse']
        }),
        ('Sistema', {
            'fields': ['id', 'is_active', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(ProductSupplierInfo)
class ProductSupplierInfoAdmin(admin.ModelAdmin):
    list_display  = ['product', 'supplier', 'sequence', 'supplier_product_code', 'price', 'min_quantity', 'lead_time', 'is_preferred', 'is_active']
    list_filter   = ['is_preferred', 'is_active', 'owner_company']
    search_fields = ['product__name', 'product__internal_reference', 'supplier__name', 'supplier_product_code']
    ordering      = ['product__name', 'sequence']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = [
        ('Relação', {
            'fields': ['product', 'supplier', 'sequence', 'is_preferred']
        }),
        ('Dados de Compra', {
            'fields': ['supplier_product_code', 'price', 'min_quantity', 'lead_time']
        }),
        ('Multi-Company', {
            'fields': ['owner_company'],
            'classes': ['collapse']
        }),
        ('Sistema', {
            'fields': ['id', 'is_active', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


# ---------------------------------------------------------------------------
# Purchase List admin
# ---------------------------------------------------------------------------

from .models import PurchaseList, PurchaseListLine


class PurchaseListLineInline(admin.TabularInline):
    model = PurchaseListLine
    extra = 0
    fields = ['product', 'uom', 'qty_on_hand', 'qty_needed', 'qty_to_buy', 'purchase_price', 'vat_rate', 'notes']
    readonly_fields = ['qty_on_hand', 'qty_needed']
    autocomplete_fields = ['product']


@admin.register(PurchaseList)
class PurchaseListAdmin(admin.ModelAdmin):
    list_display  = ['name', 'state', 'date', 'supplier', 'warehouse', 'owner_company']
    list_filter   = ['state', 'owner_company']
    search_fields = ['name', 'reference', 'supplier__name']
    ordering      = ['-date', '-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines       = [PurchaseListLineInline]

    fieldsets = [
        ('Cabeçalho', {
            'fields': ['name', 'state', 'date', 'supplier', 'warehouse', 'reference', 'notes']
        }),
        ('Multi-Company', {
            'fields': ['owner_company'],
            'classes': ['collapse']
        }),
        ('Sistema', {
            'fields': ['id', 'is_active', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
