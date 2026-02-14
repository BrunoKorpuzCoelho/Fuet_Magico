from django.contrib import admin
from .models import AuditLog, ErrorLog, Company, ChatterMessage, ChatterActivity


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
