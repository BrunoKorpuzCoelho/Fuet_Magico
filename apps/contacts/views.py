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
from .forms import ContactForm, ContactTagForm


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
        contacts = Contact.objects.filter(is_active=False).select_related('company', 'owner_company').prefetch_related('tags').order_by('name')
    else:
        contacts = Contact.objects.filter(is_active=True).select_related('company', 'owner_company').prefetch_related('tags').order_by('name')
    
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
            associated_count = contact.associated_contacts.count()
            if associated_count > 0:
                related_warnings.append({
                    'contact': contact.name,
                    'warning': f'{associated_count} contacto(s) associado(s) perderão a associação'
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
            
            # Fase 4: Processar tags selecionadas
            tag_ids = request.POST.getlist('tags')
            if tag_ids:
                contact.tags.set(tag_ids)  # Define as tags do contacto
            
            messages.success(request, f'Contacto "{contact.name}" criado com sucesso!')
            return redirect('contacts:contact_list')
        else:
            # Debug: mostrar erros de validação
            print("ERROS DO FORMULÁRIO:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
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
            
            # Fase 4: Processar tags selecionadas
            tag_ids = request.POST.getlist('tags')
            if tag_ids:
                contact.tags.set(tag_ids)  # Define as tags do contacto
            else:
                contact.tags.clear()  # Remove todas as tags se nenhuma foi selecionada
            
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
    """Criar novo contacto e associar a outro contacto via M2M"""
    from apps.core.multi_company import get_active_company
    from django.shortcuts import get_object_or_404
    
    parent_id = request.POST.get('company_id')
    if not parent_id:
        messages.error(request, 'ID do contacto não fornecido.')
        return redirect('contacts:contact_list')
    
    parent_contact = get_object_or_404(Contact, id=parent_id)
    
    # Criar novo contacto
    contact = Contact(
        name=request.POST.get('name', ''),
        contact_category=request.POST.get('contact_category', 'PERSON'),
        email=request.POST.get('email') or None,
        phone=request.POST.get('phone', ''),
        owner_company=get_active_company(request)
    )
    contact.save()
    
    # Associar via ManyToMany
    parent_contact.associated_contacts.add(contact)
    
    messages.success(request, f'Contacto "{contact.name}" criado e associado com sucesso!')
    return redirect('contacts:contact_edit', contact_id=parent_contact.id)


@require_http_methods(["POST"])
def associate_existing_contact(request):
    """Associar contacto existente a outro contacto via M2M"""
    from django.shortcuts import get_object_or_404
    
    parent_id = request.POST.get('company_id')
    contact_id = request.POST.get('contact_id')
    
    if not parent_id or not contact_id:
        messages.error(request, 'IDs não fornecidos.')
        return redirect('contacts:contact_list')
    
    parent_contact = get_object_or_404(Contact, id=parent_id)
    contact = get_object_or_404(Contact, id=contact_id)
    
    # Associar via ManyToMany
    parent_contact.associated_contacts.add(contact)
    
    messages.success(request, f'Contacto "{contact.name}" associado com sucesso!')
    return redirect('contacts:contact_edit', contact_id=parent_contact.id)


def search_contacts_api(request):
    """API para pesquisar contactos (para o modal de associação) - com paginação"""
    query = request.GET.get('q', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    
    exclude_id = request.GET.get('exclude', '')
    
    # Buscar todos os contactos ativos
    contacts = Contact.objects.filter(
        is_active=True,
    )
    
    # Excluir o próprio contacto e os já associados
    if exclude_id:
        contacts = contacts.exclude(id=exclude_id)
        try:
            parent = Contact.objects.get(id=exclude_id)
            already_associated = parent.associated_contacts.values_list('id', flat=True)
            contacts = contacts.exclude(id__in=already_associated)
        except Contact.DoesNotExist:
            pass
    
    # Filter by active company
    contacts = filter_by_company(contacts, request)
    
    # Filtrar por nome se houver query
    if query:
        contacts = contacts.filter(name__icontains=query)
    
    contacts = contacts.order_by('name')
    
    # Paginação
    total_count = contacts.count()
    total_pages = max(1, (total_count + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))
    offset = (page - 1) * page_size
    contacts_page = contacts[offset:offset + page_size]
    
    results = [{
        'id': str(contact.id),
        'name': contact.name,
        'email': contact.email or '',
        'phone': contact.phone or '',
        'avatar_url': contact.get_avatar_url(),
        'category_display': contact.get_contact_category_display()
    } for contact in contacts_page]
    
    return JsonResponse({
        'contacts': results,
        'current_page': page,
        'total_pages': total_pages,
        'total_count': total_count,
    })


@require_http_methods(["POST"])
def remove_association(request, company_id, employee_id):
    """Remover associação M2M entre dois contactos"""
    from django.shortcuts import get_object_or_404
    
    parent_contact = get_object_or_404(Contact, id=company_id)
    associated = get_object_or_404(Contact, id=employee_id)
    
    # Remover associação M2M
    parent_contact.associated_contacts.remove(associated)
    
    return JsonResponse({'success': True, 'message': 'Associação removida com sucesso!'})


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
    from django.db import transaction
    
    try:
        data = json.loads(request.body)
        tag_ids = data.get('tag_ids', [])
        
        if not isinstance(tag_ids, list):
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'INVALID_FORMAT',
                    'message': 'tag_ids deve ser uma lista'
                }
            }, status=400)
        
        if not tag_ids:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'EMPTY_SELECTION',
                    'message': 'Nenhuma tag selecionada para arquivar'
                }
            }, status=400)
        
        tags = ContactTag.objects.filter(id__in=tag_ids)
        
        if not tags.exists():
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'TAGS_NOT_FOUND',
                    'message': 'Nenhuma tag válida encontrada'
                }
            }, status=404)
        
        already_archived = []
        to_archive = []
        
        for tag in tags:
            if not tag.is_active:
                already_archived.append(tag.name)
            else:
                to_archive.append(tag)
        
        # Se TODAS já estiverem arquivadas, retorna erro
        if already_archived and not to_archive:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'ALREADY_ARCHIVED',
                    'message': 'As tags selecionadas já estão arquivadas. Use a opção desarquivar se pretende restaurá-las.',
                    'tags': already_archived
                }
            }, status=409)
        
        # Arquivar apenas as que estão ativas
        with transaction.atomic():
            archived_count = 0
            for tag in to_archive:
                tag.is_active = False
                tag.save(update_fields=['is_active'])
                archived_count += 1
        
        result = {
            'success': True,
            'archived_count': archived_count,
            'message': f'{archived_count} tag(s) arquivada(s) com sucesso'
        }
        
        if already_archived:
            result['already_archived'] = already_archived
            result['warning'] = f'{len(already_archived)} tag(s) já estavam arquivadas'
        
        return JsonResponse(result, status=200)
            
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
def bulk_unarchive_tags(request):
    """Desarquivar múltiplas tags em massa"""
    from .models import ContactTag
    from django.db import transaction
    
    try:
        data = json.loads(request.body)
        tag_ids = data.get('tag_ids', [])
        
        if not isinstance(tag_ids, list):
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'INVALID_FORMAT',
                    'message': 'tag_ids deve ser uma lista'
                }
            }, status=400)
        
        if not tag_ids:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'EMPTY_SELECTION',
                    'message': 'Nenhuma tag selecionada para desarquivar'
                }
            }, status=400)
        
        tags = ContactTag.objects.filter(id__in=tag_ids)
        
        if not tags.exists():
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'TAGS_NOT_FOUND',
                    'message': 'Nenhuma tag válida encontrada'
                }
            }, status=404)
        
        already_active = []
        to_unarchive = []
        
        for tag in tags:
            if tag.is_active:
                already_active.append(tag.name)
            else:
                to_unarchive.append(tag)
        
        # Se TODAS já estiverem ativas, retorna erro
        if already_active and not to_unarchive:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'ALREADY_ACTIVE',
                    'message': 'As tags selecionadas já estão ativas.',
                    'tags': already_active
                }
            }, status=409)
        
        # Desarquivar apenas as que estão arquivadas
        with transaction.atomic():
            unarchived_count = 0
            for tag in to_unarchive:
                tag.is_active = True
                tag.save(update_fields=['is_active'])
                unarchived_count += 1
        
        result = {
            'success': True,
            'unarchived_count': unarchived_count,
            'message': f'{unarchived_count} tag(s) desarquivada(s) com sucesso'
        }
        
        if already_active:
            result['already_active'] = already_active
            result['warning'] = f'{len(already_active)} tag(s) já estavam ativas'
        
        return JsonResponse(result, status=200)
            
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
def check_tags_contacts(request):
    """Verificar quantos contactos estão associados às tags selecionadas"""
    from .models import ContactTag
    
    try:
        data = json.loads(request.body)
        tag_ids = data.get('tag_ids', [])
        
        if not isinstance(tag_ids, list) or not tag_ids:
            return JsonResponse({'success': False}, status=400)
        
        tags = ContactTag.objects.filter(id__in=tag_ids)
        tags_with_contacts = []
        total_affected = 0
        
        for tag in tags:
            count = tag.contacts.count()
            if count > 0:
                tags_with_contacts.append({
                    'name': tag.name,
                    'contacts_count': count
                })
                total_affected += count
        
        return JsonResponse({
            'success': True,
            'tags_with_contacts': tags_with_contacts,
            'total_affected': total_affected
        })
    except (json.JSONDecodeError, Exception):
        return JsonResponse({'success': False}, status=400)


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
                'error': {
                    'code': 'INVALID_FORMAT',
                    'message': 'tag_ids deve ser uma lista'
                }
            }, status=400)
        
        if not tag_ids:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'NO_TAGS',
                    'message': 'Nenhuma tag selecionada'
                }
            }, status=400)
        
        # Get tags to delete
        tags = ContactTag.objects.filter(id__in=tag_ids)
        count = tags.count()
        
        if count == 0:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'NOT_FOUND',
                    'message': 'Tags não encontradas'
                }
            }, status=404)
        
        # Check how many contacts are using these tags
        related_warnings = []
        for tag in tags:
            contacts_count = tag.contacts.count()
            if contacts_count > 0:
                related_warnings.append({
                    'tag': tag.name,
                    'warning': f'{contacts_count} contacto(s) associado(s)'
                })
        
        # Delete tags (hard delete)
        deleted_names = [tag.name for tag in tags]
        tags.delete()
        
        result = {
            'success': True,
            'message': f'{count} tag(s) eliminada(s) permanentemente',
            'deleted_count': count,
            'deleted_names': deleted_names
        }
        
        if related_warnings:
            result['warnings'] = related_warnings
        
        return JsonResponse(result, status=200)
            
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
def tag_create_view(request):
    """View para criar nova tag"""
    from apps.core.multi_company import get_active_company
    from .models import ContactTag
    
    if request.method == 'POST':
        form = ContactTagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            # Auto-fill owner_company with active company from session
            if not tag.owner_company:
                tag.owner_company = get_active_company(request)
            tag.save()
            messages.success(request, f'Tag "{tag.name}" criada com sucesso!')
            return redirect('contacts:tag_list')
    else:
        form = ContactTagForm()
    
    context = {
        'form': form,
        'is_edit': False,
    }
    
    return render(request, 'contacts/tag_form.html', context)


@login_required
def tag_edit_view(request, tag_id):
    """View para editar tag existente"""
    from apps.core.multi_company import get_active_company
    from .models import ContactTag
    from django.shortcuts import get_object_or_404
    
    tag = get_object_or_404(ContactTag, id=tag_id)
    
    if request.method == 'POST':
        form = ContactTagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save(commit=False)
            # Auto-fill owner_company if not set
            if not tag.owner_company:
                tag.owner_company = get_active_company(request)
            tag.save()
            messages.success(request, f'Tag "{tag.name}" atualizada com sucesso!')
            return redirect('contacts:tag_list')
    else:
        form = ContactTagForm(instance=tag)
    
    context = {
        'form': form,
        'tag': tag,
        'is_edit': True,
    }
    
    return render(request, 'contacts/tag_form.html', context)


@require_http_methods(["GET"])
@login_required
def search_tags_api(request):
    """API para pesquisar tags (usado no autocomplete do formulário de contactos)"""
    from .models import ContactTag
    from apps.core.multi_company import get_active_company
    
    query = request.GET.get('q', '').strip()
    limit = int(request.GET.get('limit', 7))
    
    if not query:
        # Se não houver query, retorna as tags mais usadas
        tags = ContactTag.objects.filter(
            owner_company=get_active_company(request),
            is_active=True
        ).order_by('-created_at')[:limit]
    else:
        # Pesquisa por nome (case-insensitive)
        tags = ContactTag.objects.filter(
            owner_company=get_active_company(request),
            is_active=True,
            name__icontains=query
        ).order_by('name')[:limit]
    
    # Serializar tags
    results = [
        {
            'id': str(tag.id),
            'name': tag.name,
            'color': tag.color,
            'contact_count': tag.contacts.count()
        }
        for tag in tags
    ]
    
    return JsonResponse({
        'success': True,
        'results': results,
        'count': len(results),
        'has_more': ContactTag.objects.filter(
            owner_company=get_active_company(request),
            is_active=True,
            name__icontains=query
        ).count() > limit
    })


@require_http_methods(["POST"])
@login_required
def quick_create_tag_api(request):
    """API para criar tag rapidamente (usado no autocomplete do formulário de contactos)"""
    from .models import ContactTag
    from apps.core.multi_company import get_active_company
    import random
    
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        color = data.get('color', '').strip()
        
        if not name:
            return JsonResponse({
                'success': False,
                'error': 'Nome da tag é obrigatório'
            }, status=400)
        
        # Verificar se já existe
        if ContactTag.objects.filter(
            owner_company=get_active_company(request),
            name__iexact=name
        ).exists():
            return JsonResponse({
                'success': False,
                'error': 'Já existe uma tag com este nome'
            }, status=400)
        
        # Se não foi fornecida cor, gerar aleatória
        if not color:
            colors = [
                '#dc2626', '#ea580c', '#d97706', '#ca8a04', '#65a30d',
                '#16a34a', '#059669', '#0891b2', '#0284c7', '#2563eb',
                '#4f46e5', '#7c3aed', '#9333ea', '#c026d3', '#db2777',
                '#dbc693'
            ]
            color = random.choice(colors)
        
        # Criar tag
        tag = ContactTag.objects.create(
            name=name,
            color=color,
            owner_company=get_active_company(request)
        )
        
        return JsonResponse({
            'success': True,
            'tag': {
                'id': str(tag.id),
                'name': tag.name,
                'color': tag.color,
                'contact_count': 0
            },
            'message': f'Tag "{tag.name}" criada com sucesso!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Formato JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
