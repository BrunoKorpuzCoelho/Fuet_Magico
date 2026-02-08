from django.contrib import admin
from .models import Contact, ContactTag


@admin.register(ContactTag)
class ContactTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'contact_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Tag Information', {
            'fields': ['name', 'color', 'is_active']
        }),
        ('System', {
            'fields': ['id', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def contact_count(self, obj):
        """Display number of contacts using this tag"""
        return obj.contacts.count()
    contact_count.short_description = 'Contacts'


class EmployeeInline(admin.TabularInline):
    model = Contact
    fk_name = 'company'
    extra = 0
    fields = ['name', 'email', 'phone', 'position', 'contact_type']
    verbose_name = 'Employee'
    verbose_name_plural = 'Employees'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_category', 'company', 'contact_type', 'email', 'phone', 'is_active']
    list_filter = ['contact_category', 'contact_type', 'is_active', 'company']
    search_fields = ['name', 'email', 'phone', 'nif', 'city']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'contact_category', 'contact_type', 'is_active']
        }),
        ('Contact Details', {
            'fields': ['email', 'phone', 'whatsapp']
        }),
        ('Address', {
            'fields': ['address', 'city', 'district', 'postal_code', 'country'],
            'classes': ['collapse']
        }),
        ('Company Information', {
            'fields': ['nif', 'company', 'position', 'website', 'language'],
        }),
        ('Additional', {
            'fields': ['tags', 'notes'],
            'classes': ['collapse']
        }),
        ('System', {
            'fields': ['id', 'created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    inlines = [EmployeeInline]
    
    def get_inlines(self, request, obj=None):
        if obj and obj.is_company:
            return [EmployeeInline]
        return []
