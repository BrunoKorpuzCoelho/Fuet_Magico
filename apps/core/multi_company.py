"""
Multi-company utilities for filtering queries by active company.
"""
from django.db.models import Q


def get_active_company(request):
    """
    Get the active company from request session.
    
    Args:
        request: Django request object with session
        
    Returns:
        Company object or None
    """
    from apps.core.models import Company
    
    active_company_id = request.session.get('active_company_id')
    
    if not active_company_id:
        return None
        
    try:
        return Company.objects.get(id=active_company_id)
    except Company.DoesNotExist:
        return None


def filter_by_company(queryset, request, company_field='owner_company'):
    """
    Filter queryset by active company with multi-company logic:
    - Include records where company_field is NULL (global records, all companies can see)
    - Include records where company_field matches active_company (private records)
    
    Args:
        queryset: Django queryset to filter
        request: Django request object with session
        company_field: Name of the FK field to Company (default: 'owner_company')
        
    Returns:
        Filtered queryset
        
    Example:
        contacts = Contact.objects.all()
        contacts = filter_by_company(contacts, request)
        # Returns: contacts with owner_company=NULL OR owner_company=active_company
    """
    active_company = get_active_company(request)
    
    if not active_company:
        # No active company, show only global records (NULL)
        return queryset.filter(**{f'{company_field}__isnull': True})
    
    # Show global records (NULL) + records from active company
    return queryset.filter(
        Q(**{f'{company_field}__isnull': True}) | 
        Q(**{company_field: active_company})
    )


def set_owner_company(instance, request):
    """
    Set owner_company on instance if not already set.
    Uses active company from session.
    
    Args:
        instance: Model instance with owner_company field
        request: Django request object with session
        
    Returns:
        Modified instance (not saved)
        
    Example:
        contact = Contact(name="New Contact")
        contact = set_owner_company(contact, request)
        contact.save()
    """
    if hasattr(instance, 'owner_company') and not instance.owner_company:
        instance.owner_company = get_active_company(request)
    
    return instance
