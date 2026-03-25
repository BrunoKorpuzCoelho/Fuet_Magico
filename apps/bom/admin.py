from django.contrib import admin
from .models import ProductBOM, ProductBOMLine


class ProductBOMLineInline(admin.TabularInline):
    model = ProductBOMLine
    extra = 1
    fields = ('sequence', 'component', 'quantity', 'uom', 'notes')
    ordering = ('sequence',)
    autocomplete_fields = ('component',)


@admin.register(ProductBOM)
class ProductBOMAdmin(admin.ModelAdmin):
    list_display = ('product', 'qty_produced', 'uom', 'labor_cost', 'calculated_unit_cost', 'owner_company')
    list_filter = ('owner_company',)
    search_fields = ('product__name',)
    autocomplete_fields = ('product', 'uom', 'owner_company')
    inlines = [ProductBOMLineInline]

    @admin.display(description='Custo unitário (€)')
    def calculated_unit_cost(self, obj):
        return f'{obj.calculate_unit_cost():.4f} €'
