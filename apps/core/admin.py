from django.contrib import admin
from .models import AuditLog, ErrorLog, Company


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
