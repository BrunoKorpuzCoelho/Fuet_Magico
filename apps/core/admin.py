from django.contrib import admin
from django.utils.html import format_html
from .models import (
    AuditLog, ErrorLog, Company, ChatterMessage, ChatterActivity,
    ActivityType, ScheduledActivity, ActivityWorkflow,
    ActivityChain, ActivityChainStep, ActivityChainInstance, ActivityLog,
    Notification, ChatterFollower,
)


@admin.register(ActivityType)
class ActivityTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'blueprint_count', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['name']

    def blueprint_count(self, obj):
        return obj.blueprints.count()
    blueprint_count.short_description = 'Blueprints'


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'vat', 'city', 'country', 'currency', 'language', 'is_active', 'created_at']
    list_filter = ['is_active', 'country', 'currency', 'created_at']
    search_fields = ['name', 'legal_name', 'vat', 'email', 'city']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'legal_name', 'vat', 'company_registry', 'is_active']
        }),
        ('Contact Information', {
            'fields': ['email', 'phone', 'website']
        }),
        ('Address', {
            'fields': ['address', 'city', 'postal_code', 'country']
        }),
        ('Regional Settings', {
            'fields': ['currency', 'language']
        }),
        ('Branding', {
            'fields': ['logo'],
            'classes': ['collapse']
        }),
        ('Hierarchy', {
            'fields': ['parent_company'],
            'classes': ['collapse']
        }),
        ('System', {
            'fields': ['id', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'model_name', 'object_id']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'model_name', 'object_id']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'timestamp', 'details']
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'level', 'message_preview', 'request_path', 'user']
    list_filter = ['level', 'timestamp']
    search_fields = ['message', 'request_path', 'user__username']
    readonly_fields = ['level', 'message', 'traceback', 'request_path', 'user', 'timestamp']
    ordering = ['-timestamp']
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(ChatterMessage)
class ChatterMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_object', 'author', 'message_type', 'subject', 'is_internal', 'created_at']
    list_filter = ['message_type', 'is_internal', 'created_at']
    search_fields = ['subject', 'body', 'to_email', 'author__username', 'author__first_name', 'author__last_name']
    readonly_fields = ['content_type', 'object_id', 'sent_at', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Related Object', {
            'fields': ('content_type', 'object_id')
        }),
        ('Message', {
            'fields': ('author', 'message_type', 'subject', 'body')
        }),
        ('Email Details', {
            'fields': ('to_email', 'cc_emails', 'sent_at'),
            'classes': ['collapse']
        }),
        ('Attachments & Status', {
            'fields': ('attachments', 'is_internal')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse']
        }),
    )
    
    def content_object(self, obj):
        """Display the related object"""
        if obj.content_object:
            return f"{obj.content_type.model.title()} #{str(obj.object_id)[:8]}..."
        return "-"
    content_object.short_description = 'Related Object'


@admin.register(ChatterActivity)
class ChatterActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_object', 'user', 'activity_type', 'description', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['description', 'user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['content_type', 'object_id', 'created_at']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Related Object', {
            'fields': ('content_type', 'object_id')
        }),
        ('Activity', {
            'fields': ('user', 'activity_type', 'description', 'details')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def content_object(self, obj):
        """Display the related object"""
        if obj.content_object:
            return f"{obj.content_type.model.title()} #{str(obj.object_id)[:8]}..."
        return "-"
    content_object.short_description = 'Related Object'
    
    def has_add_permission(self, request):
        """Prevent manual creation (activities are auto-generated)"""
        return False


# ============================================================================
# ACTIVITIES SYSTEM ADMIN
# ============================================================================


@admin.register(ActivityChain)
class ActivityChainAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_steps', 'owner_company', 'is_active', 'created_at']
    list_filter = ['is_active', 'owner_company']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Chain Info', {
            'fields': ('name', 'description')
        }),
        ('Company', {
            'fields': ('owner_company',),
            'classes': ['collapse']
        }),
        ('System', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ['collapse']
        }),
    )


@admin.register(ActivityChainStep)
class ActivityChainStepAdmin(admin.ModelAdmin):
    list_display = ['chain', 'order', 'activity', 'delay_days', 'default_assigned_to']
    list_filter = ['chain', 'delay_days']
    search_fields = ['chain__name', 'activity__summary']
    ordering = ['chain', 'order']


@admin.register(ActivityChainInstance)
class ActivityChainInstanceAdmin(admin.ModelAdmin):
    list_display = ['chain', 'status', 'assigned_to', 'owner_company', 'started_at', 'completed_at']
    list_filter = ['status', 'chain', 'owner_company']
    search_fields = ['chain__name']
    readonly_fields = ['started_at', 'completed_at', 'created_at', 'updated_at']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['step', 'chain_instance', 'result', 'is_done', 'due_date', 'executed_at', 'logged_by']
    list_filter = ['result', 'is_done', 'due_date']
    search_fields = ['notes', 'chain_instance__chain__name']
    readonly_fields = ['executed_at', 'done_at', 'created_at', 'updated_at']
    date_hierarchy = 'due_date'


@admin.register(ScheduledActivity)
class ScheduledActivityAdmin(admin.ModelAdmin):
    list_display = ['name_or_summary', 'activity_type', 'icon_preview', 'owner_company', 'is_active', 'created_at']
    list_filter = ['activity_type', 'is_active', 'owner_company', 'decoration_type']
    search_fields = ['name', 'summary', 'description']
    readonly_fields = ['created_at', 'updated_at', 'icon_rendered_preview']
    ordering = ['activity_type__name', 'name', 'summary']

    fieldsets = (
        ('Blueprint Info', {
            'fields': ('activity_type', 'name', 'summary', 'description')
        }),
        ('Visual (Icon & Colors)', {
            'fields': ('icon', 'icon_svg', 'icon_color', 'icon_rendered_preview', 'decoration_type'),
            'description': 'Escolha UMA opção: Emoji (campo icon) OU SVG customizado (icon_svg + icon_color)'
        }),
        ('Company', {
            'fields': ('owner_company',),
            'classes': ['collapse']
        }),
        ('System', {
            'fields': ('is_active', 'created_at', 'updated_at'),
            'classes': ['collapse']
        }),
    )

    def name_or_summary(self, obj):
        return obj.name or obj.summary
    name_or_summary.short_description = 'Name / Summary'

    def icon_preview(self, obj):
        if obj.icon_svg:
            return format_html(
                '<span style="display: inline-block; width: 20px; height: 20px; color: {};">{}</span>',
                obj.icon_color or '#6366F1', obj.icon_svg
            )
        if obj.icon:
            if obj.icon.startswith('fa-'):
                return format_html(
                    '<i class="{}" style="font-size: 18px; color: {};"></i>',
                    obj.icon, obj.icon_color or '#6366F1'
                )
            return format_html('<span style="font-size: 18px;">{}</span>', obj.icon)
        return format_html('<span style="font-size: 18px;">{}</span>', obj.default_icon_emoji)
    icon_preview.short_description = 'Icon'

    def icon_rendered_preview(self, obj):
        if not obj.pk:
            return '-'
        return format_html(
            '<div style="padding: 20px; background: #f5f5f5; border-radius: 8px; display: inline-block;">{}</div>'
            '<p style="color: #666; margin-top: 10px;">Preview at 48px</p>',
            obj.get_rendered_icon(size='48px')
        )
    icon_rendered_preview.short_description = 'Icon Preview'


@admin.register(ActivityWorkflow)
class ActivityWorkflowAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'trigger_info', 'next_template_info', 
        'chaining_mode', 'delay_days', 'is_active', 'sequence'
    ]
    list_filter = [
        'is_active', 'trigger_activity_type', 'trigger_result', 
        'chaining_mode', 'base_date_type', 'model', 'owner_company'
    ]
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['sequence', 'name']
    
    fieldsets = (
        ('Workflow Info', {
            'fields': ('name', 'description', 'is_active', 'sequence')
        }),
        ('Trigger Conditions', {
            'fields': (
                'model',
                'trigger_activity_type', 
                'trigger_result',
                'trigger_condition'
            ),
            'description': 'When should this workflow execute?'
        }),
        ('Action (What to Create)', {
            'fields': (
                'next_activity_template',
                'delay_days',
                'base_date_type',
                'chaining_mode'
            ),
            'description': 'What activity to create and how'
        }),
        ('Company', {
            'fields': ('owner_company',),
            'classes': ['collapse']
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ['collapse']
        }),
    )
    
    def trigger_info(self, obj):
        """Display trigger conditions"""
        result_text = f" ({obj.get_trigger_result_display()})" if obj.trigger_result else " (any result)"
        return format_html(
            '<span title="Trigger: {} on {}">{}{}</span>',
            obj.get_trigger_activity_type_display(),
            obj.model,
            obj.get_trigger_activity_type_display(),
            result_text
        )
    trigger_info.short_description = 'Trigger'
    
    def next_template_info(self, obj):
        """Display next activity template"""
        return format_html(
            '<span title="{}">{}</span>',
            obj.next_activity_template.default_summary,
            obj.next_activity_template.name
        )
    next_template_info.short_description = 'Next Activity'
    
    def chaining_mode(self, obj):
        """Display chaining mode with icon"""
        if obj.chaining_mode == 'SUGGEST':
            icon = '💡'
            color = '#F59E0B'
        else:  # TRIGGER
            icon = '⚡'
            color = '#10B981'
        
        return format_html(
            '<span style="color: {};">{} {}</span>',
            color,
            icon,
            obj.get_chaining_mode_display()
        )
    chaining_mode.short_description = 'Mode'


# ─────────────────────────────────────────────────────────────────────────────
# NOTIFICATIONS
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notification_type', 'title', 'priority', 'is_read', 'created_at']
    list_filter  = ['notification_type', 'is_read', 'priority', 'created_at']
    search_fields = ['title', 'message', 'user__first_name', 'user__last_name', 'user__username']
    readonly_fields = ['id', 'priority', 'related_content_type', 'related_object_id', 'read_at', 'created_at', 'updated_at']
    ordering = ['priority', '-created_at']

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        count = 0
        for n in queryset:
            n.mark_as_read()
            count += 1
        self.message_user(request, f'{count} notificação(ões) marcada(s) como lida(s).')
    mark_as_read.short_description = 'Marcar como lida'

    def mark_as_unread(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_read=False, read_at=None)
        self.message_user(request, f'{queryset.count()} notificação(ões) marcada(s) como não lida(s).')
    mark_as_unread.short_description = 'Marcar como não lida'


@admin.register(ChatterFollower)
class ChatterFollowerAdmin(admin.ModelAdmin):
    list_display  = ['user', 'content_type', 'object_id', 'added_by', 'created_at']
    list_filter   = ['content_type']
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    readonly_fields = ['created_at']
