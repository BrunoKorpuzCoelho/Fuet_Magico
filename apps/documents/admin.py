from django.contrib import admin
from .models import LayoutStyle, TableStyle, DocumentLayout


@admin.register(LayoutStyle)
class LayoutStyleAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'sort_order', 'updated_at']
    list_editable = ['is_active', 'sort_order']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'is_active', 'sort_order'),
        }),
        ('HTML', {
            'fields': ('header_html', 'footer_html'),
            'classes': ('collapse',),
        }),
        ('Preview', {
            'fields': ('preview_image',),
        }),
        ('Auditoria', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TableStyle)
class TableStyleAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'sort_order', 'updated_at']
    list_editable = ['is_active', 'sort_order']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'is_active', 'sort_order'),
        }),
        ('CSS & HTML', {
            'fields': ('css_styles', 'header_row_html', 'data_row_html', 'totals_row_html'),
            'classes': ('collapse',),
        }),
        ('Preview', {
            'fields': ('preview_image',),
        }),
        ('Auditoria', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(DocumentLayout)
class DocumentLayoutAdmin(admin.ModelAdmin):
    list_display = ['company', 'layout_style', 'table_style', 'font', 'paper_format', 'updated_at']
    list_filter = ['paper_format', 'layout_style', 'table_style']
    list_select_related = ['company', 'layout_style', 'table_style']
    search_fields = ['company__name']
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    fieldsets = (
        (None, {
            'fields': ('company', 'layout_style', 'table_style'),
        }),
        ('Aparência', {
            'fields': ('font', 'primary_color', 'secondary_color'),
        }),
        ('Textos', {
            'fields': ('tagline', 'footer_text', 'tax_id'),
        }),
        ('Formato', {
            'fields': ('paper_format',),
        }),
        ('Auditoria', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
