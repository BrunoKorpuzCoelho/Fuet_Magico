from django.contrib import admin
from .models import CRMStage


@admin.register(CRMStage)
class CRMStageAdmin(admin.ModelAdmin):
    list_display = ['name', 'sequence', 'is_won_stage', 'routing_in_days', 'color', 'fold_by_default', 'owner_company']
    list_editable = ['sequence', 'fold_by_default']
    list_filter = ['is_won_stage', 'fold_by_default', 'owner_company']
    search_fields = ['name']
    ordering = ['sequence', 'name']
    
    fieldsets = (
        ('Informação Básica', {
            'fields': ('name', 'sequence', 'color')
        }),
        ('Configurações', {
            'fields': ('is_won_stage', 'fold_by_default', 'routing_in_days')
        }),
        ('Multi-Company', {
            'fields': ('owner_company',),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )

