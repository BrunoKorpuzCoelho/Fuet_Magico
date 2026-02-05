from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Contact


def contact_list_view(request):
    search_query = request.GET.get('search', '')
    search_field = request.GET.get('field', 'name')
    page_number = request.GET.get('page', 1)
    
    contacts = Contact.objects.filter(is_active=True).select_related('company').order_by('name')
    
    if search_query:
        field_mapping = {
            'name': Q(name__icontains=search_query),
            'email': Q(email__icontains=search_query),
            'phone': Q(phone__icontains=search_query),
            'whatsapp': Q(whatsapp__icontains=search_query),
            'nif': Q(nif__icontains=search_query),
            'address': Q(address__icontains=search_query),
            'city': Q(city__icontains=search_query),
            'postal_code': Q(postal_code__icontains=search_query),
            'contact_type': Q(contact_type__icontains=search_query),
            'contact_category': Q(contact_category__icontains=search_query),
            'company': Q(company__name__icontains=search_query),
            'position': Q(position__icontains=search_query),
            'notes': Q(notes__icontains=search_query),
        }
        
        if search_field in field_mapping:
            contacts = contacts.filter(field_mapping[search_field])
    
    paginator = Paginator(contacts, 50)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'contacts': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
    }
    
    return render(request, 'contacts/list.html', context)
