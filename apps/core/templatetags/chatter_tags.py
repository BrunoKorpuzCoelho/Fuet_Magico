"""
Template tags for Chatter component.

Usage in templates:
    {% load chatter_tags %}
    
    <div x-data="chatterComponent('{{ object|content_type }}', '{{ object.id }}')">
    
Example output:
    {{ lead|content_type }} → "crm.lead"
    {{ contact|content_type }} → "contacts.contact"
    {{ sale|content_type }} → "sales.saleorder"
"""
from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter
def content_type(obj):
    """
    Returns 'app_label.model' string for any Django model instance.
    Used to identify the object type in JavaScript/Alpine.js components.
    
    Args:
        obj: Any Django model instance (Lead, Contact, Sale, etc.)
        
    Returns:
        str: "app_label.model" format (e.g., "crm.lead", "contacts.contact")
        
    Usage:
        Template:
            {{ lead|content_type }}
            
        Output:
            "crm.lead"
            
        In Alpine.js:
            <div x-data="chatterComponent('{{ object|content_type }}', '{{ object.id }}')">
            
        Result:
            <div x-data="chatterComponent('crm.lead', '123e4567-...')">
    """
    if obj is None:
        return ''
    
    try:
        ct = ContentType.objects.get_for_model(obj)
        return f"{ct.app_label}.{ct.model}"
    except Exception:
        return ''
