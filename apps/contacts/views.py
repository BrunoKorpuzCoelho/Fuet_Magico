from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from .models import Contact
from .services import ContactService
from apps.accounts.decorators import admin_required
from apps.core.multi_company import filter_by_company
from .forms import ContactForm


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
        contacts = Contact.objects.filter(is_active=False).select_related('company', 'owner_company').order_by('name')
    else:
        contacts = Contact.objects.filter(is_active=True).select_related('company', 'owner_company').order_by('name')
    
    # Filter by active company (global + active company records)
    contacts = filter_by_company(contacts, request)
    
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


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_contacts(request):
    try:
        data = json.loads(request.body)
        contact_ids = data.get('contact_ids', [])
        
        result = ContactService.bulk_unarchive(contact_ids)
        
        if result['success']:
            return JsonResponse(result, status=200)
        else:
            status_code = 400
            if result['error']['code'] == 'ALREADY_ACTIVE':
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


@require_http_methods(["POST"])
@login_required
@admin_required
def bulk_delete_contacts(request):
    """
    Permanently delete contacts (ADMIN ONLY)
    Checks for related data (future: sales, purchases)
    """
    try:
        data = json.loads(request.body)
        contact_ids = data.get('contact_ids', [])
        
        if not contact_ids:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'NO_CONTACTS',
                    'message': 'Nenhum contacto selecionado'
                }
            }, status=400)
        
        # Get contacts to delete
        contacts = Contact.objects.filter(id__in=contact_ids)
        count = contacts.count()
        
        if count == 0:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'NOT_FOUND',
                    'message': 'Contactos não encontrados'
                }
            }, status=404)
        
        # TODO: Check for related data when sales/purchases are implemented
        # For now, we'll check for company relationships
        related_warnings = []
        for contact in contacts:
            if contact.contact_category == 'COMPANY':
                employees_count = contact.employees.count()
                if employees_count > 0:
                    related_warnings.append({
                        'contact': contact.name,
                        'warning': f'{employees_count} colaborador(es) associado(s) ficarão sem empresa'
                    })
        
        # Delete contacts (hard delete)
        deleted_names = [contact.name for contact in contacts]
        contacts.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'{count} contacto(s) eliminado(s) permanentemente',
            'data': {
                'count': count,
                'deleted_names': deleted_names,
                'warnings': related_warnings
            }
        }, status=200)
        
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


@require_http_methods(["POST"])
@login_required
def find_duplicates(request):
    try:
        data = json.loads(request.body)
        contact_id = data.get('contact_id')
        
        if not contact_id:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'MISSING_CONTACT_ID',
                    'message': 'ID do contacto é obrigatório'
                }
            }, status=400)
        
        result = ContactService.find_potential_duplicates(contact_id)
        
        if result['success']:
            return JsonResponse(result, status=200)
        else:
            return JsonResponse(result, status=404)
            
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


@login_required
@ensure_csrf_cookie
def contact_create_view(request):
    """View para criar novo contacto"""
    from apps.core.multi_company import get_active_company
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            # Auto-fill owner_company with active company from session
            if not contact.owner_company:
                contact.owner_company = get_active_company(request)
            contact.save()
            messages.success(request, f'Contacto "{contact.name}" criado com sucesso!')
            return redirect('contacts:contact_list')
    else:
        form = ContactForm()
    
    # Get companies for the dropdown (filter by owner_company too)
    companies = Contact.objects.filter(contact_category='COMPANY', is_active=True).order_by('name')
    companies = filter_by_company(companies, request)
    
    # Contadores para smart buttons (todos a 0 para novo contacto)
    context = {
        'form': form,
        'companies': companies,
        'crm_count': 0,
        'sales_count': 0,
        'purchases_count': 0,
        'invoices_total': 0,
        'documents_count': 0,
        'campaigns_count': 0,
    }
    
    return render(request, 'contacts/create.html', context)


def contact_edit_view(request, contact_id):
    """View para editar contacto existente"""
    from apps.core.multi_company import get_active_company
    from django.shortcuts import get_object_or_404
    
    contact = get_object_or_404(Contact, id=contact_id)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            # Auto-fill owner_company if not set
            if not contact.owner_company:
                contact.owner_company = get_active_company(request)
            contact.save()
            messages.success(request, f'Contacto "{contact.name}" atualizado com sucesso!')
            return redirect('contacts:contact_edit', contact_id=contact.id)
    else:
        form = ContactForm(instance=contact)
    
    # Get companies for the dropdown
    companies = Contact.objects.filter(contact_category='COMPANY', is_active=True).order_by('name')
    companies = filter_by_company(companies, request)
    
    # TODO: Calcular contadores reais quando os módulos estiverem implementados
    context = {
        'form': form,
        'contact': contact,  # Passa o contacto para o template
        'companies': companies,
        'crm_count': 0,
        'sales_count': 0,
        'purchases_count': 0,
        'invoices_total': 0,
        'documents_count': 0,
        'campaigns_count': 0,
    }
    
    return render(request, 'contacts/create.html', context)


@require_http_methods(["POST"])
def create_associated_contact(request):
    """Criar novo contacto e associar a uma empresa"""
    from apps.core.multi_company import get_active_company
    from django.shortcuts import get_object_or_404
    
    company_id = request.POST.get('company_id')
    if not company_id:
        messages.error(request, 'ID da empresa não fornecido.')
        return redirect('contacts:contact_list')
    
    company = get_object_or_404(Contact, id=company_id, contact_category='COMPANY')
    
    # Criar novo contacto
    contact = Contact(
        name=request.POST.get('name', ''),
        contact_category=request.POST.get('contact_category', 'PERSON'),
        email=request.POST.get('email') or None,  # None if empty to avoid unique constraint issues
        phone=request.POST.get('phone', ''),
        position=request.POST.get('job_title', ''),
        company=company,  # Associar à empresa
        owner=request.user,
        owner_company=get_active_company(request)
    )
    contact.save()
    
    messages.success(request, f'Contacto "{contact.name}" criado e associado com sucesso!')
    return redirect('contacts:contact_edit', contact_id=company.id)


@require_http_methods(["POST"])
def associate_existing_contact(request):
    """Associar contacto existente a uma empresa"""
    from django.shortcuts import get_object_or_404
    
    company_id = request.POST.get('company_id')
    contact_id = request.POST.get('contact_id')
    
    if not company_id or not contact_id:
        messages.error(request, 'IDs não fornecidos.')
        return redirect('contacts:contact_list')
    
    company = get_object_or_404(Contact, id=company_id, contact_category='COMPANY')
    contact = get_object_or_404(Contact, id=contact_id)
    
    # Associar contacto à empresa
    contact.company = company
    contact.save()
    
    messages.success(request, f'Contacto "{contact.name}" associado com sucesso!')
    return redirect('contacts:contact_edit', contact_id=company.id)


def search_contacts_api(request):
    """API para pesquisar contactos (para o modal de associação)"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'contacts': []})
    
    # Buscar contactos (excluindo empresas)
    contacts = Contact.objects.filter(
        Q(name__icontains=query) | 
        Q(email__icontains=query) | 
        Q(phone__icontains=query),
        is_active=True,
        contact_category__in=['PERSON', 'BILLING', 'SHIPPING', 'OTHER']
    ).exclude(
        company__isnull=False  # Excluir contactos já associados
    )[:10]
    
    # Filter by active company
    contacts = filter_by_company(contacts, request)
    
    results = [{
        'id': str(contact.id),
        'name': contact.name,
        'email': contact.email or '',
        'phone': contact.phone or '',
        'avatar_url': contact.get_avatar_url(),
        'category_display': contact.get_contact_category_display()
    } for contact in contacts]
    
    return JsonResponse({'contacts': results})


@require_http_methods(["POST"])
def remove_association(request, company_id, employee_id):
    """Remover associação de um contacto a uma empresa"""
    from django.shortcuts import get_object_or_404
    
    company = get_object_or_404(Contact, id=company_id)
    employee = get_object_or_404(Contact, id=employee_id, company=company)
    
    # Remover associação
    employee.company = None
    employee.save()
    
    return JsonResponse({'success': True, 'message': f'Associação removida com sucesso!'})


# ============================================================
# CONTACT TAGS VIEWS
# ============================================================

@ensure_csrf_cookie
def tag_list_view(request):
    """View para listar Contact Tags com paginação, busca e filtros"""
    from .models import ContactTag
    from django.db.models import Count
    
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
    
    # Filtrar por status (ativo/arquivado)
    if status_filter == 'archived':
        tags = ContactTag.objects.filter(is_active=False).annotate(contact_count=Count('contacts')).order_by('name')
    else:
        tags = ContactTag.objects.filter(is_active=True).annotate(contact_count=Count('contacts')).order_by('name')
    
    # Filter by active company (global + active company records)
    tags = filter_by_company(tags, request)
    
    # Aplicar busca por campo
    if search_query:
        field_mapping = {
            'name': Q(name__icontains=search_query),
            'color': Q(color__icontains=search_query),
        }
        
        if search_field in field_mapping:
            tags = tags.filter(field_mapping[search_field])
    
    # Paginação
    paginator = Paginator(tags, page_size)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tags': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
    }
    
    return render(request, 'contacts/tag_list.html', context)


@require_http_methods(["POST"])
@login_required
def bulk_archive_tags(request):
    """Arquivar múltiplas tags em massa"""
    from .models import ContactTag
    
    try:
        data = json.loads(request.body)
        tag_ids = data.get('tag_ids', [])
        
        if not isinstance(tag_ids, list):
            return JsonResponse({
                'success': False,
                'error': 'tag_ids deve ser uma lista'
            }, status=400)
        
        # Arquivar tags
        updated_count = ContactTag.objects.filter(id__in=tag_ids, is_active=True).update(is_active=False)
        
        return JsonResponse({
            'success': True,
            'message': f'{updated_count} tag(s) arquivada(s) com sucesso!',
            'count': updated_count
        }, status=200)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_tags(request):
    """Desarquivar múltiplas tags em massa"""
    from .models import ContactTag
    
    try:
        data = json.loads(request.body)
        tag_ids = data.get('tag_ids', [])
        
        if not isinstance(tag_ids, list):
            return JsonResponse({
                'success': False,
                'error': 'tag_ids deve ser uma lista'
            }, status=400)
        
        # Desarquivar tags
        updated_count = ContactTag.objects.filter(id__in=tag_ids, is_active=False).update(is_active=True)
        
        return JsonResponse({
            'success': True,
            'message': f'{updated_count} tag(s) desarquivada(s) com sucesso!',
            'count': updated_count
        }, status=200)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["POST"])
@login_required
@admin_required
def bulk_delete_tags(request):
    """Eliminar múltiplas tags em massa (apenas ADMIN)"""
    from .models import ContactTag
    
    try:
        data = json.loads(request.body)
        tag_ids = data.get('tag_ids', [])
        
        if not isinstance(tag_ids, list):
            return JsonResponse({
                'success': False,
                'error': 'tag_ids deve ser uma lista'
            }, status=400)
        
        # Eliminar tags permanentemente
        deleted_count, _ = ContactTag.objects.filter(id__in=tag_ids).delete()
        
        return JsonResponse({
            'success': True,
            'message': f'{deleted_count} tag(s) eliminada(s) permanentemente!',
            'count': deleted_count
        }, status=200)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

