from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserEmailConfig

admin.site.site_header = 'Fuet Mágico Admin'
admin.site.site_title = 'Fuet Mágico'
admin.site.index_title = 'Gestão'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'avatar', 'role')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone', 'avatar', 'role')}),
    )


@admin.register(UserEmailConfig)
class UserEmailConfigAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_address', 'provider', 'is_active', 'has_smtp_configured']
    list_filter = ['provider', 'is_active']
    search_fields = ['user__username', 'user__email', 'email_address']
    readonly_fields = ['has_smtp_configured']
    fields = ['user', 'email_address', 'app_password', 'provider', 'is_active', 'has_smtp_configured']

    def has_smtp_configured(self, obj):
        return obj.has_smtp_configured
    has_smtp_configured.boolean = True
    has_smtp_configured.short_description = 'SMTP configurado'
