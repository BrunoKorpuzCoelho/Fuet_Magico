from django.contrib import admin
from .models import Category, UoMCategory, UoM, Product, Warehouse


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
