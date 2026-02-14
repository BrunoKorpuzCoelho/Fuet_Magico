from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q, F, Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from apps.accounts.decorators import admin_required
from apps.core.multi_company import filter_by_company, get_active_company
from .models import CRMTag, CRMStage, Lead
from .forms import CRMStageForm, CRMTagForm
import json
import random

User = get_user_model()


def generate_random_color():
    """Gera uma cor hexadecimal aleatória bonita para estágios"""
    colors = [
        '#6c757d',  # Gray
        '#17a2b8',  # Cyan
        '#ffc107',  # Yellow
        '#28a745',  # Green
        '#dc3545',  # Red
        '#007bff',  # Blue
        '#6610f2',  # Purple
        '#e83e8c',  # Pink
        '#fd7e14',  # Orange
        '#20c997',  # Teal
        '#343a40',  # Dark
    ]
    return random.choice(colors)


@ensure_csrf_cookie
@admin_required
def stage_list_view(request):
    """
    Lista de estágios CRM com funcionalidade de drag & drop para reordenar.
    """
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)
    
    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50
    
    # Buscar stages ativos ordenados por sequence
    stages = CRMStage.objects.filter(is_active=True).order_by('sequence', 'name')
    
    # Filter by active company (global + active company records)
    stages = filter_by_company(stages, request)
    
    # Busca
    if search_query:
        stages = stages.filter(
            Q(name__icontains=search_query)
        )
    
    total_count = stages.count()
    
    # Paginação
    paginator = Paginator(stages, page_size)
    stages_page = paginator.get_page(page_number)
    
    context = {
        'stages': stages_page,
        'total_count': total_count,
        'search_query': search_query,
        'page_size': page_size,
    }
    
    return render(request, 'crm/stage_list.html', context)


@require_http_methods(["POST"])
@admin_required
def stage_create(request):
    """
    Cria um novo estágio CRM.
    """
    try:
        data = json.loads(request.body)
        
        name = data.get('name', '').strip()
        if not name:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'MISSING_NAME',
                    'message': 'Nome do estágio é obrigatório'
                }
            }, status=400)
        
        sequence = data.get('sequence', 1)
        color = data.get('color', '#6c757d')
        routing_in_days = data.get('routing_in_days', 0)
        is_won_stage = data.get('is_won_stage', False)
        is_lost_stage = data.get('is_lost_stage', False)
        fold_by_default = data.get('fold_by_default', False)
        
        # Validar que só pode haver um estágio de vitória
        company = request.session.get('active_company_id')
        if is_won_stage:
            existing_won = CRMStage.objects.filter(
                is_won_stage=True,
                is_active=True
            )
            if company:
                existing_won = existing_won.filter(
                    Q(owner_company_id=company) | Q(owner_company__isnull=True)
                )
            else:
                existing_won = existing_won.filter(owner_company__isnull=True)
            
            if existing_won.exists():
                return JsonResponse({
                    'success': False,
                    'error': {
                        'code': 'WON_STAGE_EXISTS',
                        'message': 'Já existe um estágio de vitória. Só pode existir um estágio com "Vitória" ativo por empresa.'
                    }
                }, status=400)
        
        # Validar que só pode haver um estágio de perda
        if is_lost_stage:
            existing_lost = CRMStage.objects.filter(
                is_lost_stage=True,
                is_active=True
            )
            if company:
                existing_lost = existing_lost.filter(
                    Q(owner_company_id=company) | Q(owner_company__isnull=True)
                )
            else:
                existing_lost = existing_lost.filter(owner_company__isnull=True)
            
            if existing_lost.exists():
                return JsonResponse({
                    'success': False,
                    'error': {
                        'code': 'LOST_STAGE_EXISTS',
                        'message': 'Já existe um estágio de perda. Só pode existir um estágio com "Perda" ativo por empresa.'
                    }
                }, status=400)
        
        # Obter owner_company
        owner_company = get_active_company(request)
        
        # Criar o estágio
        stage = CRMStage.objects.create(
            name=name,
            sequence=sequence,
            color=color,
            routing_in_days=routing_in_days,
            is_won_stage=is_won_stage,
            is_lost_stage=is_lost_stage,
            fold_by_default=fold_by_default,
            owner_company=owner_company
        )
        
        return JsonResponse({
            'success': True,
            'message': f'Estágio "{stage.name}" criado com sucesso',
            'data': {
                'id': str(stage.id),
                'name': stage.name,
                'sequence': stage.sequence,
                'color': stage.color
            }
        }, status=201)
        
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
                'message': str(e)
            }
        }, status=500)


@require_http_methods(["POST"])
@admin_required
def stage_reorder(request, pk):
    """
    Endpoint para reordenar estágios via drag & drop.
    Recebe new_sequence e atualiza todos os stages afetados.
    """
    try:
        data = json.loads(request.body)
        new_sequence = int(data.get('new_sequence'))
        
        stage = get_object_or_404(CRMStage, pk=pk, is_active=True)
        old_sequence = stage.sequence
        
        if old_sequence == new_sequence:
            return JsonResponse({'success': True, 'message': 'Sem alterações'})
        
        # Atualizar sequences dos stages afetados
        if new_sequence > old_sequence:
            # Moveu para baixo: decrementar stages entre old e new
            CRMStage.objects.filter(
                sequence__gt=old_sequence,
                sequence__lte=new_sequence,
                is_active=True
            ).update(sequence=F('sequence') - 1)
        else:
            # Moveu para cima: incrementar stages entre new and old
            CRMStage.objects.filter(
                sequence__gte=new_sequence,
                sequence__lt=old_sequence,
                is_active=True
            ).update(sequence=F('sequence') + 1)
        
        # Atualizar sequence do stage movido
        stage.sequence = new_sequence
        stage.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Estágio reordenado com sucesso',
            'stage_id': str(stage.pk),
            'new_sequence': new_sequence
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@require_http_methods(["POST"])
@login_required
@admin_required
def stage_reorder_all(request):
    """
    Endpoint para reordenar todos os estágios de uma vez.
    Recebe uma lista de IDs na nova ordem e recalcula as sequências (1, 2, 3...).
    """
    try:
        data = json.loads(request.body)
        ordered_ids = data.get('ordered_ids', [])
        
        if not ordered_ids:
            return JsonResponse({
                'success': False,
                'error': 'Lista de IDs vazia'
            }, status=400)
        
        # Update sequence for each stage based on position in list
        for index, stage_id in enumerate(ordered_ids):
            new_sequence = index + 1
            CRMStage.objects.filter(pk=stage_id, is_active=True).update(sequence=new_sequence)
        
        return JsonResponse({
            'success': True,
            'message': f'{len(ordered_ids)} estágios reordenados com sucesso'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@require_http_methods(["POST"])
@admin_required
def stage_delete(request, pk):
    """
    Soft delete de estágio CRM.
    """
    try:
        stage = get_object_or_404(CRMStage, pk=pk)
        stage.is_active = False
        stage.save()
        
        messages.success(request, f'Estágio "{stage.name}" arquivado com sucesso.')
        return JsonResponse({
            'success': True,
            'message': f'Estágio "{stage.name}" arquivado'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@require_http_methods(["POST"])
@admin_required
def stage_duplicate(request):
    """
    Duplica estágios selecionados.
    Cria cópias exatas com sequence = original.sequence + 1
    
    IMPORTANTE: Estágios com is_won_stage=True ou is_lost_stage=True não podem ser duplicados.
    Só pode existir um estágio de vitória e um de perda por empresa.
    """
    try:
        data = json.loads(request.body)
        stage_ids = data.get('stage_ids', [])
        
        if not stage_ids:
            return JsonResponse({
                'success': False,
                'error': 'Nenhum estágio selecionado'
            }, status=400)
        
        # Verificar se algum dos estágios selecionados é um estágio de vitória ou perda
        special_stages = CRMStage.objects.filter(
            id__in=stage_ids,
            is_active=True
        ).filter(Q(is_won_stage=True) | Q(is_lost_stage=True))
        
        if special_stages.exists():
            return JsonResponse({
                'success': False,
                'error': 'Não é possível duplicar estágios de vitória ou perda. Só pode existir um de cada por empresa.'
            }, status=400)
        
        duplicated_count = 0
        
        for stage_id in stage_ids:
            original_stage = get_object_or_404(CRMStage, pk=stage_id, is_active=True)
            
            # Incrementar sequences dos stages que vêm depois
            CRMStage.objects.filter(
                sequence__gt=original_stage.sequence,
                is_active=True
            ).update(sequence=F('sequence') + 1)
            
            # Criar duplicata
            duplicated_stage = CRMStage.objects.create(
                name=f"{original_stage.name} (cópia)",
                sequence=original_stage.sequence + 1,
                is_won_stage=original_stage.is_won_stage,
                is_lost_stage=original_stage.is_lost_stage,
                fold_by_default=original_stage.fold_by_default,
                routing_in_days=original_stage.routing_in_days,
                color=original_stage.color,
                owner_company=original_stage.owner_company
            )
            
            duplicated_count += 1
        
        messages.success(request, f'{duplicated_count} estágio(s) duplicado(s) com sucesso.')
        return JsonResponse({
            'success': True,
            'message': f'{duplicated_count} estágio(s) duplicado(s)',
            'count': duplicated_count
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@require_http_methods(["POST"])
@admin_required
def stage_bulk_delete(request):
    """
    Permanently delete CRM stages (ADMIN ONLY)
    Checks for related data (future: leads, opportunities)
    """
    try:
        data = json.loads(request.body)
        stage_ids = data.get('stage_ids', [])
        
        if not stage_ids:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'NO_STAGES',
                    'message': 'Nenhum estágio selecionado'
                }
            }, status=400)
        
        # Get stages to delete
        stages = CRMStage.objects.filter(id__in=stage_ids, is_active=True)
        count = stages.count()
        
        if count == 0:
            return JsonResponse({
                'success': False,
                'error': {
                    'code': 'NOT_FOUND',
                    'message': 'Estágios não encontrados'
                }
            }, status=404)
        
        # TODO: Check for related data when leads/opportunities are implemented
        # For now, we'll just check if any is a won stage
        related_warnings = []
        for stage in stages:
            if stage.is_won_stage:
                related_warnings.append({
                    'stage': stage.name,
                    'warning': 'Este é um estágio de vitória'
                })
            if stage.is_lost_stage:
                related_warnings.append({
                    'stage': stage.name,
                    'warning': 'Este é um estágio de perda'
                })
        
        # Delete stages (hard delete)
        deleted_names = [stage.name for stage in stages]
        stages.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'{count} estágio(s) eliminado(s) permanentemente',
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

@login_required
@admin_required
def stage_create_view(request):
    """View para criar novo estágio CRM"""
    if request.method == 'POST':
        form = CRMStageForm(request.POST)
        if form.is_valid():
            stage = form.save(commit=False)
            # Auto-fill owner_company with active company from session
            if not stage.owner_company:
                stage.owner_company = get_active_company(request)
            
            # Auto-increment sequences if needed
            new_sequence = stage.sequence
            existing_stages = CRMStage.objects.filter(
                is_active=True,
                sequence__gte=new_sequence
            ).order_by('-sequence')
            
            # Increment sequences for all stages >= new sequence
            for existing_stage in existing_stages:
                existing_stage.sequence = F('sequence') + 1
                existing_stage.save(update_fields=['sequence'])
            
            # Refresh to get actual sequence values
            for existing_stage in existing_stages:
                existing_stage.refresh_from_db()
            
            stage.save()
            messages.success(request, f'Estágio "{stage.name}" criado com sucesso!')
            return redirect('crm:stage_list')
    else:
        # Get next sequence number
        last_stage = CRMStage.objects.filter(is_active=True).order_by('-sequence').first()
        next_sequence = (last_stage.sequence + 1) if last_stage else 1
        
        form = CRMStageForm(initial={'sequence': next_sequence, 'color': generate_random_color()})
    
    context = {
        'form': form,
        'is_edit': False,
    }
    
    return render(request, 'crm/stage_form.html', context)


@login_required
@admin_required
def stage_edit_view(request, stage_id):
    """View para editar estágio CRM existente"""
    stage = get_object_or_404(CRMStage, id=stage_id, is_active=True)
    original_sequence = stage.sequence
    
    if request.method == 'POST':
        form = CRMStageForm(request.POST, instance=stage)
        if form.is_valid():
            stage = form.save(commit=False)
            # Auto-fill owner_company if not set
            if not stage.owner_company:
                stage.owner_company = get_active_company(request)
            
            # Auto-increment sequences if sequence changed
            new_sequence = stage.sequence
            if new_sequence != original_sequence:
                if new_sequence < original_sequence:
                    # Moving up - increment stages between new and old position
                    CRMStage.objects.filter(
                        is_active=True,
                        sequence__gte=new_sequence,
                        sequence__lt=original_sequence
                    ).exclude(pk=stage.pk).update(sequence=F('sequence') + 1)
                else:
                    # Moving down - decrement stages between old and new position
                    CRMStage.objects.filter(
                        is_active=True,
                        sequence__gt=original_sequence,
                        sequence__lte=new_sequence
                    ).exclude(pk=stage.pk).update(sequence=F('sequence') - 1)
            
            stage.save()
            messages.success(request, f'Estágio "{stage.name}" atualizado com sucesso!')
            return redirect('crm:stage_list')
    else:
        form = CRMStageForm(instance=stage)
    
    context = {
        'form': form,
        'stage': stage,
        'is_edit': True,
    }
    
    return render(request, 'crm/stage_form.html', context)


# =============================================
# PIPELINE / KANBAN VIEW (Default CRM View)
# =============================================

@login_required
def lead_pipeline_view(request):
    """
    Vista Kanban do Pipeline CRM (Odoo-style).
    Esta é a vista DEFAULT ao aceder /crm/
    
    Mostra leads organizadas por estágio com drag & drop,
    totais por coluna, progress bars e filtros.
    """
    # Load all active stages (filtered by company)
    stages = CRMStage.objects.filter(is_active=True)
    stages = filter_by_company(stages, request)
    stages = stages.order_by('sequence', 'name')
    
    # Handle search
    search_query = request.GET.get('search', '').strip()
    search_field = request.GET.get('field', 'title')
    
    # For each stage, get leads and calculate totals
    pipeline_data = []
    grand_total_value = 0
    grand_total_count = 0
    
    for stage in stages:
        # Get leads for this stage
        leads = Lead.objects.filter(stage=stage, is_active=True)
        leads = filter_by_company(leads, request)
        
        # Apply search filter
        if search_query:
            search_filters = {
                'title': Q(title__icontains=search_query),
                'contact': Q(contact__name__icontains=search_query),
                'source': Q(source__icontains=search_query),
                'assigned_to': Q(assigned_to__username__icontains=search_query),
                'priority': Q(priority__icontains=search_query),
                'description': Q(description__icontains=search_query),
            }
            leads = leads.filter(search_filters.get(search_field, Q(title__icontains=search_query)))
        
        leads = leads.select_related('contact', 'assigned_to', 'stage')
        leads = leads.order_by('-created_at')
        
        # Annotate overdue status (routing_in_days > 0 and lead stuck too long)
        leads_list = list(leads)
        now = timezone.now()
        for lead in leads_list:
            if stage.routing_in_days > 0:
                days_in_stage = (now - lead.stage_updated_at).days
                if days_in_stage > stage.routing_in_days:
                    lead.is_overdue = True
                    lead.is_warning = False
                elif days_in_stage == stage.routing_in_days:
                    lead.is_overdue = False
                    lead.is_warning = True
                else:
                    lead.is_overdue = False
                    lead.is_warning = False
            else:
                lead.is_overdue = False
                lead.is_warning = False
        
        # Calculate totals for this column
        stage_stats = leads.aggregate(
            total_value=Sum('estimated_value'),
            count=Count('id')
        )
        
        stage_total = stage_stats['total_value'] or 0
        stage_count = stage_stats['count'] or 0
        
        pipeline_data.append({
            'stage': stage,
            'leads': leads_list,
            'total_value': stage_total,
            'count': stage_count,
            'is_folded': stage.fold_by_default,
        })
        
        grand_total_value += stage_total
        grand_total_count += stage_count
    
    context = {
        'pipeline_data': pipeline_data,
        'grand_total_value': grand_total_value,
        'grand_total_count': grand_total_count,
        'search_query': search_query,
        'search_field': search_field,
    }
    
    return render(request, 'crm/lead_pipeline.html', context)


@login_required
@require_http_methods(["POST"])
def lead_change_stage(request, lead_id):
    """
    API endpoint to change a lead's stage via drag & drop.
    POST /crm/leads/<uuid:lead_id>/change-stage/
    Payload: {"new_stage_id": "stage-uuid"}
    """
    try:
        # Parse JSON body
        data = json.loads(request.body)
        new_stage_id = data.get('new_stage_id')
        
        if not new_stage_id:
            return JsonResponse({'success': False, 'error': 'new_stage_id is required'}, status=400)
        
        # Get active company
        active_company = get_active_company(request)
        
        # Debug: Check if stage exists
        try:
            new_stage = CRMStage.objects.get(id=new_stage_id)
        except CRMStage.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': f'Stage with id {new_stage_id} does not exist'
            }, status=404)
        
        # Check if stage belongs to user's company OR is global (owner_company=None)
        if new_stage.owner_company is not None and new_stage.owner_company != active_company:
            return JsonResponse({
                'success': False, 
                'error': f'Stage belongs to different company. Stage company: {new_stage.owner_company}, Active company: {active_company}'
            }, status=403)
        
        # Get lead (must belong to user's company)
        try:
            lead = Lead.objects.get(id=lead_id, owner_company=active_company)
        except Lead.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': f'Lead with id {lead_id} not found or belongs to different company'
            }, status=404)
        
        # Store old stage for totals calculation
        old_stage = lead.stage
        
        # Update lead
        lead.stage = new_stage
        lead.stage_updated_at = timezone.now()
        lead.save()
        
        # Calculate new totals for both columns
        old_column_leads = Lead.objects.filter(stage=old_stage, owner_company=active_company)
        old_column_total = old_column_leads.aggregate(Sum('estimated_value'))['estimated_value__sum'] or 0
        
        new_column_leads = Lead.objects.filter(stage=new_stage, owner_company=active_company)
        new_column_total = new_column_leads.aggregate(Sum('estimated_value'))['estimated_value__sum'] or 0
        
        return JsonResponse({
            'success': True,
            'new_stage_name': new_stage.name,
            'new_stage_color': new_stage.color,
            'old_stage_id': str(old_stage.id),
            'new_stage_id': str(new_stage.id),
            'old_column_total': float(old_column_total),
            'new_column_total': float(new_column_total),
            'old_column_count': old_column_leads.count(),
            'new_column_count': new_column_leads.count(),
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False, 
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)


@login_required
def lead_create_view(request):
    """
    Criar nova lead (oportunidade de venda).
    """
    from .forms import LeadForm
    from apps.contacts.models import Contact
    
    active_company = get_active_company(request)
    
    if request.method == 'POST':
        form = LeadForm(request.POST)
        
        if form.is_valid():
            lead = form.save(commit=False)
            lead.owner_company = active_company
            lead.save()
            
            # Handle M2M tags
            tag_ids = request.POST.getlist('tags')
            if tag_ids:
                tags = CRMTag.objects.filter(id__in=tag_ids, is_active=True)
                lead.tags.set(tags)
            
            messages.success(request, f'Oportunidade "{lead.title}" criada com sucesso!')
            return redirect('crm:crm_home')
    else:
        # Get first stage as default
        default_stage = CRMStage.objects.filter(
            is_active=True
        ).filter(
            Q(owner_company__isnull=True) | Q(owner_company=active_company)
        ).order_by('sequence').first()
        
        form = LeadForm(initial={
            'stage': default_stage,
            'assigned_to': request.user,
            'probability': 10,
        })
    
    # Filtrar contactos e stages da empresa
    form.fields['contact'].queryset = Contact.objects.filter(
        is_active=True,
        owner_company=active_company
    ).order_by('name')
    
    form.fields['stage'].queryset = CRMStage.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).order_by('sequence')
    
    form.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('username')
    
    stages = CRMStage.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).exclude(is_lost_stage=True).order_by('sequence')

    context = {
        'form': form,
        'page_title': 'Nova Oportunidade',
        'stages': stages,
    }
    
    return render(request, 'crm/lead_create.html', context)


@login_required
def lead_detail_view(request, lead_id):
    """
    Detail/Edit view para uma lead (estilo Odoo).
    Layout: Form 70% | Chatter 30%
    """
    from .forms import LeadForm
    
    active_company = get_active_company(request)
    
    # Get lead
    lead = get_object_or_404(Lead, id=lead_id, owner_company=active_company)
    
    # Handle POST (save changes)
    if request.method == 'POST':
        form = LeadForm(request.POST, instance=lead)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Oportunidade "{lead.title}" atualizada com sucesso!')
            return redirect('crm:lead_detail', lead_id=lead.id)
    else:
        form = LeadForm(instance=lead)
    
    # Filtrar contactos e stages da empresa
    form.fields['contact'].queryset = Contact.objects.filter(
        is_active=True,
        owner_company=active_company
    ).order_by('name')
    
    form.fields['stage'].queryset = CRMStage.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).order_by('sequence')
    
    form.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('username')
    
    # Get all stages for status bar
    all_stages = CRMStage.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).order_by('sequence')
    
    # Smart buttons counts (TODO: implement when models exist)
    quotations_count = 0  # TODO: lead.quotations.count()
    revenue_total = 0  # TODO: lead.quotations.filter(state='won').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Serialize stages for JavaScript
    all_stages_json = json.dumps([{
        'id': str(stage.id),
        'name': stage.name,
        'is_won_stage': stage.is_won_stage,
        'is_lost_stage': stage.is_lost_stage
    } for stage in all_stages])
    
    context = {
        'lead': lead,
        'form': form,
        'all_stages': all_stages,
        'all_stages_json': all_stages_json,
        'quotations_count': quotations_count,
        'revenue_total': revenue_total,
        'page_title': lead.title,
    }
    
    return render(request, 'crm/lead_detail.html', context)


# ============================================================
# CRM TAGS VIEWS
# ============================================================

@login_required
def crm_tag_list_view(request):
    """View para listar CRM Tags com paginação, busca e filtros"""
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
    
    if status_filter == 'archived':
        tags = CRMTag.objects.filter(is_active=False).annotate(lead_count=Count('leads')).order_by('name')
    else:
        tags = CRMTag.objects.filter(is_active=True).annotate(lead_count=Count('leads')).order_by('name')
    
    tags = filter_by_company(tags, request)
    
    if search_query:
        field_mapping = {
            'name': Q(name__icontains=search_query),
            'color': Q(color__icontains=search_query),
        }
        if search_field in field_mapping:
            tags = tags.filter(field_mapping[search_field])
    
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
    
    return render(request, 'crm/crm_tag_list.html', context)


@login_required
def crm_tag_create_view(request):
    """View para criar nova CRM tag"""
    active_company = get_active_company(request)
    
    if request.method == 'POST':
        form = CRMTagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            if not tag.owner_company:
                tag.owner_company = active_company
            tag.save()
            messages.success(request, f'Tag "{tag.name}" criada com sucesso!')
            return redirect('crm:crm_tag_list')
    else:
        form = CRMTagForm()
    
    context = {
        'form': form,
        'is_edit': False,
    }
    
    return render(request, 'crm/crm_tag_form.html', context)


@login_required
def crm_tag_edit_view(request, tag_id):
    """View para editar CRM tag existente"""
    active_company = get_active_company(request)
    tag = get_object_or_404(CRMTag, id=tag_id)
    
    if request.method == 'POST':
        form = CRMTagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save(commit=False)
            if not tag.owner_company:
                tag.owner_company = active_company
            tag.save()
            messages.success(request, f'Tag "{tag.name}" atualizada com sucesso!')
            return redirect('crm:crm_tag_list')
    else:
        form = CRMTagForm(instance=tag)
    
    context = {
        'form': form,
        'tag': tag,
        'is_edit': True,
    }
    
    return render(request, 'crm/crm_tag_form.html', context)


@require_http_methods(["POST"])
@login_required
def crm_bulk_archive_tags(request):
    """Arquivar múltiplas CRM tags em massa"""
    from django.db import transaction
    
    try:
        data = json.loads(request.body)
        tag_ids = data.get('tag_ids', [])
        
        if not isinstance(tag_ids, list):
            return JsonResponse({'success': False, 'error': {'code': 'INVALID_FORMAT', 'message': 'tag_ids deve ser uma lista'}}, status=400)
        
        if not tag_ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma tag selecionada para arquivar'}}, status=400)
        
        tags = CRMTag.objects.filter(id__in=tag_ids)
        
        if not tags.exists():
            return JsonResponse({'success': False, 'error': {'code': 'TAGS_NOT_FOUND', 'message': 'Nenhuma tag válida encontrada'}}, status=404)
        
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
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def crm_bulk_unarchive_tags(request):
    """Desarquivar múltiplas CRM tags em massa"""
    from django.db import transaction
    
    try:
        data = json.loads(request.body)
        tag_ids = data.get('tag_ids', [])
        
        if not isinstance(tag_ids, list):
            return JsonResponse({'success': False, 'error': {'code': 'INVALID_FORMAT', 'message': 'tag_ids deve ser uma lista'}}, status=400)
        
        if not tag_ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma tag selecionada para desarquivar'}}, status=400)
        
        tags = CRMTag.objects.filter(id__in=tag_ids)
        
        if not tags.exists():
            return JsonResponse({'success': False, 'error': {'code': 'TAGS_NOT_FOUND', 'message': 'Nenhuma tag válida encontrada'}}, status=404)
        
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
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def crm_bulk_delete_tags(request):
    """Eliminar múltiplas CRM tags em massa"""
    try:
        data = json.loads(request.body)
        tag_ids = data.get('tag_ids', [])
        
        if not tag_ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma tag selecionada'}}, status=400)
        
        tags = CRMTag.objects.filter(id__in=tag_ids)
        count = tags.count()
        tags.delete()
        
        return JsonResponse({'success': True, 'message': f'{count} tag(s) eliminada(s) com sucesso!'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': {'message': str(e)}}, status=500)


@require_http_methods(["POST"])
@login_required
def crm_check_tags_leads(request):
    """Verificar se tags CRM têm leads associados antes de apagar"""
    try:
        data = json.loads(request.body)
        tag_ids = data.get('tag_ids', [])
        
        tags = CRMTag.objects.filter(id__in=tag_ids).annotate(lead_count=Count('leads'))
        total_affected = sum(t.lead_count for t in tags)
        
        tags_info = [{'id': str(t.id), 'name': t.name, 'lead_count': t.lead_count} for t in tags if t.lead_count > 0]
        
        return JsonResponse({
            'success': True,
            'total_affected': total_affected,
            'tags': tags_info
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["GET"])
@login_required
def crm_search_tags_api(request):
    """API para pesquisar CRM tags (autocomplete no formulário de leads)"""
    active_company = get_active_company(request)
    query = request.GET.get('q', '').strip()
    limit = int(request.GET.get('limit', 7))
    
    if not query:
        tags = CRMTag.objects.filter(
            owner_company=active_company,
            is_active=True
        ).order_by('-created_at')[:limit]
    else:
        tags = CRMTag.objects.filter(
            owner_company=active_company,
            is_active=True,
            name__icontains=query
        ).order_by('name')[:limit]
    
    results = [
        {
            'id': str(tag.id),
            'name': tag.name,
            'color': tag.color,
            'lead_count': tag.leads.count()
        }
        for tag in tags
    ]
    
    return JsonResponse({
        'success': True,
        'results': results,
        'count': len(results),
        'has_more': CRMTag.objects.filter(
            owner_company=active_company,
            is_active=True,
            name__icontains=query
        ).count() > limit if query else False
    })


@require_http_methods(["POST"])
@login_required
def crm_quick_create_tag_api(request):
    """API para criar CRM tag rapidamente (autocomplete no formulário de leads)"""
    active_company = get_active_company(request)
    
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        color = data.get('color', '').strip()
        
        if not name:
            return JsonResponse({'success': False, 'error': 'Nome da tag é obrigatório'}, status=400)
        
        if CRMTag.objects.filter(owner_company=active_company, name__iexact=name).exists():
            return JsonResponse({'success': False, 'error': 'Já existe uma tag CRM com este nome'}, status=400)
        
        if not color:
            colors = [
                '#dc2626', '#ea580c', '#d97706', '#ca8a04', '#65a30d',
                '#16a34a', '#059669', '#0891b2', '#0284c7', '#2563eb',
                '#4f46e5', '#7c3aed', '#9333ea', '#c026d3', '#db2777',
                '#dbc693'
            ]
            color = random.choice(colors)
        
        tag = CRMTag.objects.create(
            name=name,
            color=color,
            owner_company=active_company
        )
        
        return JsonResponse({
            'success': True,
            'tag': {
                'id': str(tag.id),
                'name': tag.name,
                'color': tag.color,
                'lead_count': 0
            },
            'message': f'Tag "{tag.name}" criada com sucesso!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Formato JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ============================================================
# CONTACT SEARCH API (for lead form autocomplete)
# ============================================================

@require_http_methods(["GET"])
@login_required
def search_contacts_for_lead_api(request):
    """API para pesquisar contactos (autocomplete no campo contacto do lead)"""
    from apps.contacts.models import Contact
    
    active_company = get_active_company(request)
    query = request.GET.get('q', '').strip()
    limit = int(request.GET.get('limit', 7))
    
    contacts = Contact.objects.filter(
        is_active=True,
        owner_company=active_company
    )
    
    if query:
        contacts = contacts.filter(
            Q(name__icontains=query) | 
            Q(email__icontains=query) | 
            Q(phone__icontains=query)
        )
    
    contacts = contacts.order_by('name')[:limit]
    
    results = [
        {
            'id': str(c.id),
            'name': c.name,
            'email': c.email or '',
            'phone': c.phone or '',
        }
        for c in contacts
    ]
    
    return JsonResponse({
        'success': True,
        'results': results,
        'count': len(results),
    })
