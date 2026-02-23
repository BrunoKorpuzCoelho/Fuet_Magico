from django.contrib import admin
from .models import WhatsAppTemplate


@admin.register(WhatsAppTemplate)
class WhatsAppTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'display_name', 'name', 'category', 'language',
        'status', 'header_type', 'owner_company', 'created_at',
    ]
    list_filter = ['category', 'language', 'status', 'header_type', 'owner_company']
    search_fields = ['name', 'display_name', 'body']
    readonly_fields = ['id', 'created_at', 'updated_at', 'wa_template_uid']
    ordering = ['display_name']

    fieldsets = (
        ('Identificação', {
            'fields': ('id', 'name', 'display_name', 'owner_company', 'created_by'),
        }),
        ('Classificação', {
            'fields': ('category', 'language', 'status', 'allow_category_change'),
        }),
        ('Conteúdo', {
            'fields': ('header_type', 'header_text', 'body', 'footer', 'buttons'),
        }),
        ('Variáveis', {
            'fields': ('model_name', 'variables'),
        }),
        ('Meta API', {
            'fields': ('wa_template_uid',),
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
