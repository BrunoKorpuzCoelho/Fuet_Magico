from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from .models import Contact
from .services import ContactService


@ensure_csrf_cookie
def contact_list_view(request):
    search_query = request.GET.get('search', '')
    search_field = request.GET.get('field', 'name')
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)
    status_filter = request.GET.get('status', 'active')
    
    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50
    
    if status_filter == 'archived':
        contacts = Contact.objects.filter(is_active=False).select_related('company').order_by('name')
    else:
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
    
    paginator = Paginator(contacts, page_size)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'contacts': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
    }
    
    return render(request, 'contacts/list.html', context)


@require_http_methods(["POST"])
@login_required
def bulk_archive_contacts(request):
    try:
        data = json.loads(request.body)
        contact_ids = data.get('contact_ids', [])
        
        if not isinstance(contact_ids, list):
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'INVALID_FORMAT',
                    'message': 'contact_ids deve ser uma lista'
                }
            }, status=400)
        
        result = ContactService.bulk_archive(contact_ids)
        
        if result['success']:
            return JsonResponse(result, status=200)
        else:
            status_code = 400
            if result['error']['code'] == 'ALREADY_ARCHIVED':
                status_code = 409
            return JsonResponse(result, status=status_code)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': {
                'code': 'INVALID_JSON',
                'message': 'Formato JSON inválido'
            }
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'Ocorreu um erro inesperado'
            }
        }, status=500)

