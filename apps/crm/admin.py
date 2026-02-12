from django.contrib import admin
from .models import CRMStage, Lead, Activity


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


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['title', 'contact', 'stage', 'estimated_value', 'probability', 'priority', 'assigned_to', 'created_at']
    list_filter = ['stage', 'source', 'priority', 'assigned_to', 'created_at']
    search_fields = ['title', 'description', 'contact__name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informação Básica', {
            'fields': ('contact', 'title', 'description')
        }),
        ('Valores', {
            'fields': ('estimated_value', 'probability', 'priority')
        }),
        ('Tracking', {
            'fields': ('stage', 'source', 'expected_close_date', 'assigned_to', 'lost_reason')
        }),
        ('Tags', {
            'fields': ('tags',),
            'classes': ('collapse',)
        }),
        ('Multi-Company', {
            'fields': ('owner_company',),
            'classes': ('collapse',)
        }),
        ('Sistema', {
            'fields': ('is_active', 'stage_updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['stage_updated_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['summary', 'lead', 'activity_type', 'due_date', 'assigned_to', 'is_done', 'created_at']
    list_filter = ['activity_type', 'is_done', 'due_date', 'assigned_to', 'created_at']
    search_fields = ['summary', 'feedback', 'lead__title']
    ordering = ['due_date', '-created_at']
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Informação Básica', {
            'fields': ('lead', 'activity_type', 'summary')
        }),
        ('Datas e Responsável', {
            'fields': ('due_date', 'assigned_to')
        }),
        ('Status', {
            'fields': ('is_done', 'done_date', 'feedback')
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
    readonly_fields = ['done_date']
