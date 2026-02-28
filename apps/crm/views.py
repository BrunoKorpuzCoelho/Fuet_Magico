import json
import logging
import random
import re
from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q, F, Sum, Count, Avg, Prefetch
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.contenttypes.models import ContentType
from apps.accounts.decorators import admin_required
from apps.core.multi_company import filter_by_company, get_active_company
from apps.core.models import ActivityType, ScheduledActivity, ActivityChain, ActivityChainStep, ActivityChainInstance, ChatterFollower, notify_followers
from apps.core.forms import ScheduledActivityForm
from apps.contacts.models import Contact
from .models import CRMTag, CRMStage, Lead, Activity, LeadNote
from .forms import CRMStageForm, CRMTagForm, ActivityForm

logger = logging.getLogger(__name__)

User = get_user_model()


def _get_crm_config(request):
    """Helper: retorna CRMConfig da empresa ativa (ou None)."""
    from .models import CRMConfig
    company = get_active_company(request)
    if company:
        return CRMConfig.for_company(company)
    return None


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

    # Handle age filter (default: 1 year)
    age_filter = request.GET.get('age', '1')
    now = timezone.now()

    age_days_map = {'1': 365, '2': 730, '3': 1095, '5': 1825, 'all': None}
    age_days = age_days_map.get(age_filter, 365)
    cutoff_date = now - timedelta(days=age_days) if age_days is not None else None

    # For each stage, get leads and calculate totals
    pipeline_data = []
    grand_total_value = 0
    grand_total_count = 0
    
    for stage in stages:
        # Get leads for this stage (exclude prospects)
        leads = Lead.objects.filter(stage=stage, is_active=True, is_prospect=False)
        leads = filter_by_company(leads, request)

        # Apply age filter
        if cutoff_date:
            leads = leads.filter(created_at__gte=cutoff_date)

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
        leads = leads.prefetch_related(
            Prefetch(
                'activities',
                queryset=Activity.objects.filter(is_done=False).select_related('scheduled_activity').order_by('due_date'),
                to_attr='pending_activities',
            )
        )
        leads = leads.order_by('-created_at')
        
        # Annotate overdue status
        # Priority: 1) expected_close_date past due  2) routing_in_days exceeded
        leads_list = list(leads)
        today = now.date()
        for lead in leads_list:
            lead.is_overdue = False
            lead.is_warning = False

            # Check expected_close_date first (takes priority)
            if lead.expected_close_date:
                days_past = (today - lead.expected_close_date).days
                if days_past > 0:
                    lead.is_overdue = True
                    continue
                elif days_past == 0:
                    lead.is_warning = True
                    continue

            # Fallback to routing_in_days (stage-based timer)
            if stage.routing_in_days > 0:
                days_in_stage = (now - lead.stage_updated_at).days
                if days_in_stage > stage.routing_in_days:
                    lead.is_overdue = True
                elif days_in_stage == stage.routing_in_days:
                    lead.is_warning = True
        
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
        'age_filter': age_filter,
        'crm_config': _get_crm_config(request),
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
def lost_reasons_list_view(request):
    """
    Lista de leads perdidas com motivos de perda preenchidos.
    Mostra apenas: Oportunidade | Motivo de Perda
    Com pesquisa por título da oportunidade e paginação.
    """
    active_company = get_active_company(request)
    
    # Get search parameters
    search_query = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)
    
    # Validate page_size
    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50
    
    # Filtrar leads:
    # 1. Que estão em stage Lost (is_lost_stage=True)
    # 2. Que têm lost_reason preenchido (não vazio)
    lost_leads = Lead.objects.filter(
        owner_company=active_company,
        stage__is_lost_stage=True,
        lost_reason__isnull=False
    ).exclude(
        lost_reason=''
    ).select_related(
        'stage', 'assigned_to', 'contact'
    )
    
    # Apply search filter (por título da oportunidade)
    if search_query:
        lost_leads = lost_leads.filter(title__icontains=search_query)
    
    # Order by most recent first
    lost_leads = lost_leads.order_by('-updated_at')
    
    # Paginate
    paginator = Paginator(lost_leads, page_size)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': paginator.count,
        'page_size': page_size,
    }
    
    return render(request, 'crm/lost_reasons_list.html', context)


@login_required
def activities_list_view(request):
    """
    Lista de blueprints de atividades (ScheduledActivity).
    
    Mostra todos os blueprints reutilizáveis da empresa ativa.
    Com pesquisa, filtro por status (ativos/arquivados) e bulk actions.
    """
    search_query = request.GET.get('search', '').strip()
    search_field = request.GET.get('field', 'summary')
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)
    status_filter = request.GET.get('status', 'active')
    
    # Validate page_size
    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50
    
    # Get active company
    active_company = get_active_company(request)
    
    # Filter blueprints: company-specific OR global (owner_company=None)
    company_filter = Q(owner_company=active_company) | Q(owner_company__isnull=True)
    if status_filter == 'archived':
        activities = ScheduledActivity.objects.filter(
            company_filter,
            is_active=False
        )
    else:
        activities = ScheduledActivity.objects.filter(
            company_filter,
            is_active=True
        )
    
    # Apply search filter
    if search_query:
        field_mapping = {
            'summary': Q(summary__icontains=search_query),
            'name': Q(name__icontains=search_query),
            'description': Q(description__icontains=search_query),
            'activity_type': Q(activity_type__name__icontains=search_query),
        }
        
        if search_field in field_mapping:
            activities = activities.filter(field_mapping[search_field])
        else:
            # Search all text fields
            activities = activities.filter(
                Q(name__icontains=search_query) |
                Q(summary__icontains=search_query) |
                Q(description__icontains=search_query)
            )
    
    # Order by type then name
    activities = activities.order_by('activity_type__name', 'name')
    
    # Paginate
    paginator = Paginator(activities, page_size)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'activities': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
    }
    
    return render(request, 'crm/activities_list.html', context)


@login_required
def activity_create_view(request):
    """Criar novo blueprint de atividade"""
    active_company = get_active_company(request)

    if request.method == 'POST':
        form = ScheduledActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.owner_company = active_company
            # Normaliza o SVG para usar currentColor
            if activity.icon_svg:
                activity.icon_svg = _normalize_svg_colors(activity.icon_svg)
            if not activity.icon_color:
                activity.icon_color = '#6B7280'
            activity.save()
            messages.success(request, f'Atividade "{activity.name}" criada com sucesso!')
            return redirect('crm:activities_list')
    else:
        form = ScheduledActivityForm()

    return render(request, 'crm/activity_form.html', {
        'form': form,
        'is_edit': False,
    })


@login_required
def activity_edit_view(request, activity_id):
    """Editar blueprint de atividade existente"""
    activity = get_object_or_404(ScheduledActivity, id=activity_id)

    if request.method == 'POST':
        form = ScheduledActivityForm(request.POST, instance=activity)
        if form.is_valid():
            activity = form.save(commit=False)
            if activity.icon_svg:
                activity.icon_svg = _normalize_svg_colors(activity.icon_svg)
            if not activity.icon_color:
                activity.icon_color = '#6B7280'
            activity.save()
            messages.success(request, f'Atividade "{activity.name}" atualizada com sucesso!')
            return redirect('crm:activity_edit', activity_id=activity.id)
    else:
        form = ScheduledActivityForm(instance=activity)

    return render(request, 'crm/activity_form.html', {
        'form': form,
        'activity': activity,
        'is_edit': True,
    })


def _normalize_svg_colors(svg_code):
    """
    Remove atributos de cor do SVG e substitui por currentColor.
    Garante que o ícone usa sempre a cor definida via icon_color.
    """
    import re
    # Remove fill="#..." e fill="rgb(...)" exceto fill="none"
    svg_code = re.sub(r'fill="(?!none)[^"]+"', 'fill="currentColor"', svg_code)
    # Remove stroke="#..." exceto stroke="none" e stroke="currentColor"
    svg_code = re.sub(r'stroke="(?!none|currentColor)[^"]+"', 'stroke="currentColor"', svg_code)
    # Remove fill em style inline
    svg_code = re.sub(r'(?i)(fill\s*:\s*)(?!none|currentColor)(#[0-9a-fA-F]{3,8}|rgb\([^)]+\)|[a-zA-Z]+)', r'\1currentColor', svg_code)
    # Remove stroke em style inline
    svg_code = re.sub(r'(?i)(stroke\s*:\s*)(?!none|currentColor)(#[0-9a-fA-F]{3,8}|rgb\([^)]+\)|[a-zA-Z]+)', r'\1currentColor', svg_code)
    # Se a tag <svg> não tiver fill, adiciona fill="currentColor" para que
    # todos os elementos filhos sem fill explícito herdem a cor
    if not re.search(r'<svg[^>]+fill=', svg_code, re.IGNORECASE):
        svg_code = re.sub(r'(<svg\b)', r'\1 fill="currentColor"', svg_code, count=1)
    return svg_code.strip()


def _resolve_summary(summary, lead):
    """
    Substitui variáveis de template no resumo da atividade pelos valores reais da lead.

    Variáveis suportadas:
      {{contact_name}}  → nome do contacto da lead
      {{company_name}}  → nome da empresa do contacto; fallback para nome do contacto
    """
    if not summary or ('{{' not in summary):
        return summary

    # Resolve contact name
    if lead.contact:
        contact_name = lead.contact.name
        # company: contact.company is a FK to another Contact of type COMPANY
        company_name = lead.contact.company.name if lead.contact.company_id else contact_name
    else:
        contact_name = lead.contact_name or ''
        company_name = contact_name

    summary = summary.replace('{{contact_name}}', contact_name)
    summary = summary.replace('{{company_name}}', company_name)
    return summary


@require_http_methods(["POST"])
@login_required
def bulk_archive_activities(request):
    """Arquivar múltiplos blueprints de atividade em massa"""
    from django.db import transaction
    try:
        data = json.loads(request.body)
        activity_ids = data.get('activity_ids', [])

        if not isinstance(activity_ids, list):
            return JsonResponse({'success': False, 'error': {'code': 'INVALID_FORMAT', 'message': 'activity_ids deve ser uma lista'}}, status=400)
        if not activity_ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma atividade selecionada'}}, status=400)

        activities = ScheduledActivity.objects.filter(id__in=activity_ids)
        if not activities.exists():
            return JsonResponse({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma atividade válida encontrada'}}, status=404)

        already_archived = list(activities.filter(is_active=False).values_list('name', flat=True))
        to_archive = list(activities.filter(is_active=True))

        if already_archived and not to_archive:
            return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ARCHIVED', 'message': 'As atividades selecionadas já estão arquivadas. Use a opção desarquivar se pretende restaurá-las.', 'activities': already_archived}}, status=409)

        with transaction.atomic():
            archived_count = 0
            for a in to_archive:
                a.is_active = False
                a.save(update_fields=['is_active'])
                archived_count += 1

        result = {'success': True, 'archived_count': archived_count, 'message': f'{archived_count} atividade(s) arquivada(s) com sucesso'}
        if already_archived:
            result['warning'] = f'{len(already_archived)} atividade(s) já estavam arquivadas'
        return JsonResponse(result, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_activities(request):
    """Desarquivar múltiplos blueprints de atividade em massa"""
    from django.db import transaction
    try:
        data = json.loads(request.body)
        activity_ids = data.get('activity_ids', [])

        if not isinstance(activity_ids, list):
            return JsonResponse({'success': False, 'error': {'code': 'INVALID_FORMAT', 'message': 'activity_ids deve ser uma lista'}}, status=400)
        if not activity_ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma atividade selecionada'}}, status=400)

        activities = ScheduledActivity.objects.filter(id__in=activity_ids)
        if not activities.exists():
            return JsonResponse({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma atividade válida encontrada'}}, status=404)

        already_active = list(activities.filter(is_active=True).values_list('name', flat=True))
        to_unarchive = list(activities.filter(is_active=False))

        if already_active and not to_unarchive:
            return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ACTIVE', 'message': 'As atividades selecionadas já estão ativas. Use a opção arquivar se pretende arquivá-las.', 'activities': already_active}}, status=409)

        with transaction.atomic():
            unarchived_count = 0
            for a in to_unarchive:
                a.is_active = True
                a.save(update_fields=['is_active'])
                unarchived_count += 1

        result = {'success': True, 'unarchived_count': unarchived_count, 'message': f'{unarchived_count} atividade(s) restaurada(s) com sucesso'}
        if already_active:
            result['warning'] = f'{len(already_active)} atividade(s) já estavam ativas'
        return JsonResponse(result, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_duplicate_activities(request):
    """Duplicar blueprints de atividade selecionados, adicionando '(Cópia)' ao nome"""
    from django.db import transaction
    try:
        data = json.loads(request.body)
        activity_ids = data.get('activity_ids', [])

        if not isinstance(activity_ids, list):
            return JsonResponse({'success': False, 'error': {'code': 'INVALID_FORMAT', 'message': 'activity_ids deve ser uma lista'}}, status=400)
        if not activity_ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma atividade selecionada'}}, status=400)

        activities = ScheduledActivity.objects.filter(id__in=activity_ids)
        if not activities.exists():
            return JsonResponse({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma atividade válida encontrada'}}, status=404)

        with transaction.atomic():
            duplicated_count = 0
            for activity in activities:
                activity.pk = None  # força criação de novo registo
                activity.name = f'{activity.name} (Cópia)'
                activity.is_active = True
                activity.save()
                duplicated_count += 1

        return JsonResponse({'success': True, 'duplicated_count': duplicated_count, 'message': f'{duplicated_count} atividade(s) duplicada(s) com sucesso'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@require_http_methods(["POST"])
@login_required
@admin_required
def bulk_delete_activities(request):
    """Eliminar permanentemente blueprints de atividade (ADMIN ONLY)"""
    from django.db import transaction
    try:
        data = json.loads(request.body)
        activity_ids = data.get('activity_ids', [])

        if not isinstance(activity_ids, list):
            return JsonResponse({'success': False, 'error': {'code': 'INVALID_FORMAT', 'message': 'activity_ids deve ser uma lista'}}, status=400)
        if not activity_ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma atividade selecionada'}}, status=400)

        activities = ScheduledActivity.objects.filter(id__in=activity_ids)
        count = activities.count()
        if count == 0:
            return JsonResponse({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma atividade encontrada'}}, status=404)

        with transaction.atomic():
            activities.delete()

        return JsonResponse({'success': True, 'message': f'{count} atividade(s) eliminada(s) permanentemente', 'count': count})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'Formato JSON inválido'}}, status=400)
    except Exception:
        return JsonResponse({'success': False, 'error': {'code': 'INTERNAL_ERROR', 'message': 'Ocorreu um erro inesperado'}}, status=500)


@login_required
def lead_create_view(request):
    """
    Criar nova lead (oportunidade de venda).
    """
    from .forms import LeadForm
    
    active_company = get_active_company(request)
    is_prospect_mode = request.GET.get('prospect', '') == '1'
    
    if request.method == 'POST':
        form = LeadForm(request.POST, request.FILES)
        
        if form.is_valid():
            lead = form.save(commit=False)
            lead.owner_company = active_company
            lead._current_user = request.user  # Set user for audit logging
            lead.save()
            
            # Handle M2M tags
            tag_ids = request.POST.getlist('tags')
            if tag_ids:
                tags = CRMTag.objects.filter(id__in=tag_ids, is_active=True)
                lead.tags.set(tags)
            
            messages.success(request, f'{"Prospecto" if lead.is_prospect else "Oportunidade"} "{lead.title}" criada com sucesso!')
            if lead.is_prospect:
                return redirect('crm:prospects_list')
            return redirect('crm:crm_home')
    else:
        # Check if a stage parameter was provided (from pipeline + button)
        stage_param = request.GET.get('stage', '').strip()
        default_stage = None
        
        if stage_param:
            # Try to get the specified stage
            try:
                default_stage = CRMStage.objects.filter(
                    id=stage_param,
                    is_active=True
                ).filter(
                    Q(owner_company__isnull=True) | Q(owner_company=active_company)
                ).first()
            except:
                pass  # Invalid UUID, fallback to first stage
        
        # If no stage param or invalid, get first stage as default
        if not default_stage:
            default_stage = CRMStage.objects.filter(
                is_active=True
            ).filter(
                Q(owner_company__isnull=True) | Q(owner_company=active_company)
            ).order_by('sequence').first()
        
        form = LeadForm(initial={
            'stage': default_stage,
            'assigned_to': request.user,
            'probability': 10,
            'is_prospect': is_prospect_mode,
        })
    
    # Filtrar contactos e stages da empresa
    # Contactos sem empresa (NULL) aparecem para todas as empresas
    form.fields['contact'].queryset = Contact.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
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
    
    # Get Won and Lost stages for button logic
    won_stage = CRMStage.objects.filter(
        is_active=True, is_won_stage=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).first()
    
    lost_stage = CRMStage.objects.filter(
        is_active=True, is_lost_stage=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).first()
    
    new_stage = CRMStage.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).order_by('sequence').first()

    context = {
        'form': form,
        'page_title': 'Novo Prospecto' if is_prospect_mode else 'Nova Oportunidade',
        'stages': stages,
        'won_stage': won_stage,
        'lost_stage': lost_stage,
        'new_stage': new_stage,
        'is_prospect_mode': is_prospect_mode,
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
    
    # Get lead (select_related so contact.company is available without extra queries)
    try:
        lead = Lead.objects.select_related('contact', 'contact__company').get(
            id=lead_id, owner_company=active_company
        )
    except Lead.DoesNotExist:
        from django.http import Http404
        raise Http404
    
    # Handle POST (save changes)
    if request.method == 'POST':
        form = LeadForm(request.POST, request.FILES, instance=lead)
        
        if form.is_valid():
            lead = form.save(commit=False)
            lead._current_user = request.user  # Set user for audit logging
            lead.save()
            
            # Handle M2M tags
            tag_ids = request.POST.getlist('tags')
            if tag_ids:
                tags = CRMTag.objects.filter(id__in=tag_ids, is_active=True)
                lead.tags.set(tags)
            else:
                lead.tags.clear()  # Remove all tags if none selected
            
            # Se for request AJAX (stage auto-save), retornar JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Stage atualizado com sucesso',
                    'stage': lead.stage.name if lead.stage else None
                })
            
            messages.success(request, f'Oportunidade "{lead.title}" atualizada com sucesso!')
            return redirect('crm:lead_detail', lead_id=lead.id)
        else:
            # Se for AJAX e houver erro
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
            
            # Log form errors for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f'Lead form validation errors: {form.errors}')
            messages.error(request, 'Erro ao salvar. Verifique os campos.')
    else:
        form = LeadForm(instance=lead)
    
    # Filtrar contactos e stages da empresa
    # Contactos sem empresa (NULL) aparecem para todas as empresas
    form.fields['contact'].queryset = Contact.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).order_by('name')
    
    form.fields['stage'].queryset = CRMStage.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).order_by('sequence')
    
    form.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('username')
    
    # Get all stages for status bar (exclude Lost stage from status bar)
    all_stages = CRMStage.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).exclude(is_lost_stage=True).order_by('sequence')
    
    # Get Won and Lost stages for button logic
    won_stage = CRMStage.objects.filter(
        is_active=True, is_won_stage=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).first()
    
    lost_stage = CRMStage.objects.filter(
        is_active=True, is_lost_stage=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).first()
    
    new_stage = CRMStage.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).order_by('sequence').first()  # First stage is usually "New"
    
    # Smart buttons counts (TODO: implement when models exist)
    quotations_count = 0  # TODO: lead.quotations.count()
    revenue_total = 0  # TODO: lead.quotations.filter(state='won').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get audit logs for this lead
    from apps.core.models import AuditLog
    audit_logs = AuditLog.objects.filter(
        model_name='Lead',
        object_id=str(lead.id)
    ).select_related('user').order_by('-timestamp')[:50]  # Last 50 activities
    
    # Serialize stages for JavaScript
    all_stages_json = json.dumps([{
        'id': str(stage.id),
        'name': stage.name,
        'is_won_stage': stage.is_won_stage,
        'is_lost_stage': stage.is_lost_stage
    } for stage in all_stages])

    # Load activities linked to this lead, ordered by due_date
    lead_activities = Activity.objects.filter(
        lead=lead
    ).select_related(
        'assigned_to', 'scheduled_activity', 'scheduled_activity__activity_type'
    ).order_by('is_done', 'due_date', '-created_at')

    # Users list for "assign activity" dropdown
    users_for_activity = User.objects.filter(is_active=True).order_by('username')

    # Activity chains applicable to leads (filter by company)
    activity_chains = ActivityChain.objects.filter(
        is_active=True, applicable_model='lead'
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).order_by('name')
    activity_chains_json = json.dumps([{
        'id': str(c.id),
        'name': c.name,
        'description': c.description,
        'total_steps': c.total_steps,
    } for c in activity_chains])

    # ScheduledActivity blueprints available for this company (for activity picker)
    # Only CRM-applicable blueprints (or global ones with no specific module set)
    scheduled_activities = ScheduledActivity.objects.filter(
        is_active=True
    ).select_related('activity_type').filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).filter(
        Q(applicable_models=[]) | Q(applicable_models__contains=['CRM'])
    ).order_by('activity_type__code', 'name')
    scheduled_activities_json = json.dumps([{
        'id': str(sa.id),
        'name': sa.name or sa.summary,
        'summary': sa.summary,
        'type_code': sa.activity_type.code if sa.activity_type else '',
        'type_name': sa.activity_type.name if sa.activity_type else '',
        'icon_svg': sa.icon_svg if sa.icon_svg else '',
        'icon_color': sa.icon_color or '#6366F1',
    } for sa in scheduled_activities])

    # Pre-serialize activities to JSON for Alpine.js initialization
    from datetime import date as date_type
    lead_activities_json = json.dumps([{
        'id': str(a.id),
        'activity_type': a.activity_type,
        'activity_type_display': a.get_activity_type_display(),
        'scheduled_activity_id': str(a.scheduled_activity.id) if a.scheduled_activity else '',
        'icon_svg': a.scheduled_activity.icon_svg if a.scheduled_activity and a.scheduled_activity.icon_svg else '',
        'icon_color': a.scheduled_activity.icon_color if a.scheduled_activity and a.scheduled_activity.icon_color else '#6366F1',
        'summary': _resolve_summary(a.summary, lead),
        'due_date': a.due_date.strftime('%Y-%m-%d'),
        'due_date_display': a.due_date.strftime('%d/%m/%Y'),
        'assigned_to': a.assigned_to.get_full_name() or a.assigned_to.username if a.assigned_to else '',
        'assigned_to_id': str(a.assigned_to.id) if a.assigned_to else '',
        'is_done': a.is_done,
        'feedback': a.feedback or '',
        'is_overdue': (not a.is_done) and (a.due_date < date_type.today()),
        'is_today': (not a.is_done) and (a.due_date == date_type.today()),
    } for a in lead_activities])

    context = {
        'lead': lead,
        'form': form,
        'all_stages': all_stages,
        'all_stages_json': all_stages_json,
        'quotations_count': quotations_count,
        'revenue_total': revenue_total,
        'page_title': lead.title,
        'is_edit': True,  # Flag para indicar modo edição
        'stages': all_stages,  # Para compatibilidade com lead_create.html
        'audit_logs': audit_logs,  # Activity logs for the Log tab
        'won_stage': won_stage,
        'lost_stage': lost_stage,
        'new_stage': new_stage,
        'crm_config': _get_crm_config(request),
        'lead_activities': lead_activities,
        'users_for_activity': users_for_activity,
        'activity_type_choices': Activity.ACTIVITY_TYPE_CHOICES,
        'lead_activities_json': lead_activities_json,
        'activity_chains_json': activity_chains_json,
        'scheduled_activities_json': scheduled_activities_json,
        'current_user_id': str(request.user.id),
        'current_user_display': request.user.get_full_name() or request.user.username,
        'has_smtp': getattr(getattr(request.user, 'email_config', None), 'has_smtp_configured', False),
        'has_whatsapp': getattr(getattr(active_company, 'whatsapp_config', None), 'has_whatsapp_configured', False),
        'lead_phone': lead.phone or '',
    }
    
    return render(request, 'crm/lead_create.html', context)


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
@login_required
def search_contacts_for_lead_api(request):
    """API para pesquisar contactos (autocomplete no campo contacto do lead)"""
    active_company = get_active_company(request)
    query = request.GET.get('q', '').strip()
    limit = int(request.GET.get('limit', 7))
    
    # Contactos sem empresa (NULL) aparecem para todas as empresas
    # Contactos com empresa aparecem só para essa empresa
    contacts = Contact.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
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
            'website': c.website or '',
        }
        for c in contacts
    ]
    
    return JsonResponse({
        'success': True,
        'results': results,
        'count': len(results),
    })


# ===================================================
# LEAD LIST VIEW
# ===================================================

@login_required
def lead_list_view(request):
    """
    Vista de lista de leads (formato tabela).
    Filtra por etapas (ativas, ganhas, perdidas).
    Pode filtrar por contacto específico via parâmetro GET 'contact'.
    """
    search_query = request.GET.get('search', '').strip()
    search_field = request.GET.get('field', 'title')
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 50)
    stage_filter = request.GET.get('stage', 'active')
    contact_filter = request.GET.get('contact', '')  # UUID do contacto
    
    try:
        page_size = int(page_size)
        if page_size < 1:
            page_size = 50
    except (ValueError, TypeError):
        page_size = 50
    
    # Get active company
    active_company = get_active_company(request)
    
    # Get leads based on stage filter (always exclude prospects)
    if stage_filter == 'won':
        leads = Lead.objects.filter(
            is_active=True, is_prospect=False,
            stage__is_won_stage=True
        ).select_related(
            'contact', 'assigned_to', 'stage', 'owner_company'
        ).prefetch_related('tags')
    elif stage_filter == 'lost':
        leads = Lead.objects.filter(
            is_active=True, is_prospect=False,
            stage__is_lost_stage=True
        ).select_related(
            'contact', 'assigned_to', 'stage', 'owner_company'
        ).prefetch_related('tags')
    elif stage_filter == 'all':
        leads = Lead.objects.filter(
            is_active=True, is_prospect=False
        ).select_related(
            'contact', 'assigned_to', 'stage', 'owner_company'
        ).prefetch_related('tags')
    else:
        # Default: Active (EXCLUDE Won, Lost, and Prospects)
        leads = Lead.objects.filter(
            is_active=True, is_prospect=False
        ).exclude(
            Q(stage__is_won_stage=True) | Q(stage__is_lost_stage=True)
        ).select_related(
            'contact',
            'assigned_to', 
            'stage',
            'owner_company'
        ).prefetch_related('tags')
    
    # Filter by company
    leads = filter_by_company(leads, request)
    
    # Filter by specific contact (if provided)
    filtered_contact = None
    if contact_filter:
        try:
            from apps.contacts.models import Contact
            filtered_contact = Contact.objects.get(id=contact_filter)
            leads = leads.filter(contact=filtered_contact)
        except Contact.DoesNotExist:
            pass  # Ignore invalid contact UUID
    
    # Apply search filter
    if search_query:
        search_filters = {
            'title': Q(title__icontains=search_query),
            'contact': Q(contact__name__icontains=search_query),
            'email': Q(email_from__icontains=search_query),
            'phone': Q(phone__icontains=search_query),
            'source': Q(source__icontains=search_query),
            'assigned_to': Q(assigned_to__username__icontains=search_query) | Q(assigned_to__first_name__icontains=search_query) | Q(assigned_to__last_name__icontains=search_query),
            'priority': Q(priority__icontains=search_query),
            'stage': Q(stage__name__icontains=search_query),
            'description': Q(description__icontains=search_query),
        }
        
        if search_field in search_filters:
            leads = leads.filter(search_filters[search_field])
    
    # Order by most recent first
    leads = leads.order_by('-created_at')
    
    # Paginate
    paginator = Paginator(leads, page_size)
    page_obj = paginator.get_page(page_number)
    
    # Get Won and Lost stage names for bulk actions
    won_stage = CRMStage.objects.filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company),
        is_won_stage=True
    ).first()
    
    lost_stage = CRMStage.objects.filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company),
        is_lost_stage=True
    ).first()
    
    context = {
        'leads': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'stage_filter': stage_filter,
        'total_count': paginator.count,
        'page_size': page_size,
        'won_stage_name': won_stage.name if won_stage else 'Won',
        'lost_stage_name': lost_stage.name if lost_stage else 'Lost',
        'filtered_contact': filtered_contact,
        'crm_config': _get_crm_config(request),
    }
    
    return render(request, 'crm/lead_list.html', context)


@login_required
def prospects_list_view(request):
    """
    Vista de Prospectos — leads marcadas como is_prospect=True.
    Só acessível se prospects_enabled na CRMConfig da empresa.
    """
    crm_config = _get_crm_config(request)

    search_query = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)

    active_company = get_active_company(request)

    prospects = Lead.objects.filter(
        is_active=True,
        is_prospect=True,
    ).select_related('contact', 'assigned_to', 'stage', 'owner_company').prefetch_related('tags')

    prospects = filter_by_company(prospects, request)

    if search_query:
        prospects = prospects.filter(
            Q(title__icontains=search_query) |
            Q(contact__name__icontains=search_query) |
            Q(contact_name__icontains=search_query) |
            Q(email_from__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(source__icontains=search_query) |
            Q(assigned_to__first_name__icontains=search_query) |
            Q(assigned_to__last_name__icontains=search_query) |
            Q(assigned_to__username__icontains=search_query)
        )

    prospects = prospects.order_by('-created_at')

    paginator = Paginator(prospects, 50)
    page_obj = paginator.get_page(page_number)

    context = {
        'prospects': page_obj,
        'search_query': search_query,
        'total_count': paginator.count,
        'crm_config': crm_config,
    }
    return render(request, 'crm/prospects_list.html', context)


@require_http_methods(["POST"])
@login_required
def convert_prospect_to_lead(request, lead_id):
    """
    Converte um prospecto em oportunidade (is_prospect=False).
    """
    lead = get_object_or_404(Lead, pk=lead_id, is_active=True, is_prospect=True)
    lead.is_prospect = False
    lead.save(update_fields=['is_prospect'])
    messages.success(request, f'"{lead.title}" movido para o pipeline.')
    return redirect('crm:lead_pipeline')


@login_required
def prospect_detail_view(request, lead_id):
    """
    Vista de detalhe / edição de um Prospecto.
    Idêntica a lead_detail_view mas sem barra de stages, sem botões Ganho/Perdido/Orçamento.
    Mostra botão "Qualificar" que abre modal de confirmação.
    """
    from .forms import LeadForm

    active_company = get_active_company(request)

    try:
        lead = Lead.objects.select_related('contact', 'contact__company').get(
            id=lead_id, owner_company=active_company, is_prospect=True
        )
    except Lead.DoesNotExist:
        from django.http import Http404
        raise Http404

    if request.method == 'POST':
        form = LeadForm(request.POST, request.FILES, instance=lead)
        if form.is_valid():
            lead = form.save(commit=False)
            lead._current_user = request.user
            lead.save()
            tag_ids = request.POST.getlist('tags')
            if tag_ids:
                tags = CRMTag.objects.filter(id__in=tag_ids, is_active=True)
                lead.tags.set(tags)
            else:
                lead.tags.clear()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Prospecto actualizado'})
            messages.success(request, f'Prospecto "{lead.title}" actualizado com sucesso!')
            return redirect('crm:prospect_detail', lead_id=lead.id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            messages.error(request, 'Erro ao guardar. Verifique os campos.')
    else:
        form = LeadForm(instance=lead)

    form.fields['contact'].queryset = Contact.objects.filter(
        is_active=True
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).order_by('name')
    form.fields['stage'].queryset = CRMStage.objects.filter(is_active=True).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).order_by('sequence')
    form.fields['assigned_to'].queryset = User.objects.filter(is_active=True).order_by('username')

    from apps.core.models import AuditLog
    audit_logs = AuditLog.objects.filter(
        model_name='Lead', object_id=str(lead.id)
    ).select_related('user').order_by('-timestamp')[:50]

    lead_activities = Activity.objects.filter(lead=lead).select_related(
        'assigned_to', 'scheduled_activity', 'scheduled_activity__activity_type'
    ).order_by('is_done', 'due_date', '-created_at')

    users_for_activity = User.objects.filter(is_active=True).order_by('username')

    activity_chains = ActivityChain.objects.filter(
        is_active=True, applicable_model='lead'
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).order_by('name')
    activity_chains_json = json.dumps([{
        'id': str(c.id), 'name': c.name,
        'description': c.description, 'total_steps': c.total_steps,
    } for c in activity_chains])

    scheduled_activities = ScheduledActivity.objects.filter(is_active=True).select_related(
        'activity_type'
    ).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).filter(
        Q(applicable_models=[]) | Q(applicable_models__contains=['CRM'])
    ).order_by('activity_type__code', 'name')
    scheduled_activities_json = json.dumps([{
        'id': str(sa.id),
        'name': sa.name or sa.summary,
        'summary': sa.summary,
        'type_code': sa.activity_type.code if sa.activity_type else '',
        'type_name': sa.activity_type.name if sa.activity_type else '',
        'icon_svg': sa.icon_svg if sa.icon_svg else '',
        'icon_color': sa.icon_color or '#6366F1',
    } for sa in scheduled_activities])

    from datetime import date as date_type
    lead_activities_json = json.dumps([{
        'id': str(a.id),
        'activity_type': a.activity_type,
        'activity_type_display': a.get_activity_type_display(),
        'scheduled_activity_id': str(a.scheduled_activity.id) if a.scheduled_activity else '',
        'icon_svg': a.scheduled_activity.icon_svg if a.scheduled_activity and a.scheduled_activity.icon_svg else '',
        'icon_color': a.scheduled_activity.icon_color if a.scheduled_activity and a.scheduled_activity.icon_color else '#6366F1',
        'summary': _resolve_summary(a.summary, lead),
        'due_date': a.due_date.strftime('%Y-%m-%d'),
        'due_date_display': a.due_date.strftime('%d/%m/%Y'),
        'assigned_to': a.assigned_to.get_full_name() or a.assigned_to.username if a.assigned_to else '',
        'assigned_to_id': str(a.assigned_to.id) if a.assigned_to else '',
        'is_done': a.is_done,
        'feedback': a.feedback or '',
        'is_overdue': (not a.is_done) and (a.due_date < date_type.today()),
        'is_today': (not a.is_done) and (a.due_date == date_type.today()),
    } for a in lead_activities])

    all_stages = CRMStage.objects.filter(is_active=True).filter(
        Q(owner_company__isnull=True) | Q(owner_company=active_company)
    ).exclude(is_lost_stage=True).order_by('sequence')
    all_stages_json = json.dumps([{
        'id': str(s.id), 'name': s.name,
        'is_won_stage': s.is_won_stage, 'is_lost_stage': s.is_lost_stage,
    } for s in all_stages])

    context = {
        'lead': lead,
        'form': form,
        'all_stages': all_stages,
        'all_stages_json': all_stages_json,
        'stages': all_stages,
        'quotations_count': 0,
        'revenue_total': 0,
        'page_title': lead.title,
        'is_edit': True,
        'is_prospect_detail': True,  # ← flag used in template
        'audit_logs': audit_logs,
        'won_stage': None,
        'lost_stage': None,
        'new_stage': None,
        'crm_config': _get_crm_config(request),
        'lead_activities': lead_activities,
        'users_for_activity': users_for_activity,
        'activity_type_choices': Activity.ACTIVITY_TYPE_CHOICES,
        'lead_activities_json': lead_activities_json,
        'activity_chains_json': activity_chains_json,
        'scheduled_activities_json': scheduled_activities_json,
        'current_user_id': str(request.user.id),
        'current_user_display': request.user.get_full_name() or request.user.username,
        'has_smtp': getattr(getattr(request.user, 'email_config', None), 'has_smtp_configured', False),
        'has_whatsapp': getattr(getattr(active_company, 'whatsapp_config', None), 'has_whatsapp_configured', False),
        'lead_phone': lead.phone or '',
    }
    return render(request, 'crm/lead_create.html', context)


@require_http_methods(["POST"])
@login_required
def bulk_archive_prospects(request):
    """Arquiva prospectos seleccionados (is_active=False)."""
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        if not ids:
            return JsonResponse({'success': False, 'error': 'Nenhum prospecto seleccionado'}, status=400)
        count = Lead.objects.filter(id__in=ids, is_prospect=True).update(is_active=False)
        return JsonResponse({'success': True, 'count': count, 'message': f'{count} prospecto(s) arquivado(s)'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_prospects(request):
    """Desarquiva prospectos seleccionados (is_active=True)."""
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        if not ids:
            return JsonResponse({'success': False, 'error': 'Nenhum prospecto seleccionado'}, status=400)
        count = Lead.objects.filter(id__in=ids, is_prospect=True).update(is_active=True)
        return JsonResponse({'success': True, 'count': count, 'message': f'{count} prospecto(s) desarquivado(s)'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_qualify_prospects(request):
    """Qualifica prospectos seleccionados: is_prospect=False → entram no pipeline."""
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        if not ids:
            return JsonResponse({'success': False, 'error': 'Nenhum prospecto seleccionado'}, status=400)
        count = Lead.objects.filter(id__in=ids, is_prospect=True, is_active=True).update(is_prospect=False)
        return JsonResponse({'success': True, 'count': count, 'message': f'{count} prospecto(s) qualificado(s) e adicionado(s) ao pipeline'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_delete_prospects(request):
    """Elimina permanentemente prospectos seleccionados."""
    try:
        data = json.loads(request.body)
        ids = data.get('ids', [])
        if not ids:
            return JsonResponse({'success': False, 'error': 'Nenhum prospecto seleccionado'}, status=400)
        qs = Lead.objects.filter(id__in=ids, is_prospect=True)
        count = qs.count()
        qs.delete()
        return JsonResponse({'success': True, 'count': count, 'message': f'{count} prospecto(s) eliminado(s) permanentemente'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def generate_leads_action(request):
    """
    Endpoint dedicado para geração de leads de seguimento a partir do CRM pipeline.

    GET  ?action=preview&years=N  → JSON com número de elegíveis + janelas
    POST                          → gera leads e redireciona para o pipeline
    """
    active_company = get_active_company(request)
    crm_config = _get_crm_config(request)
    years = crm_config.lead_generation_years if crm_config else 3

    if request.method == 'GET' and request.GET.get('action') == 'preview':
        from .services import get_eligible_contacts, _seasonal_windows
        try:
            years = max(1, min(10, int(request.GET.get('years', years))))
        except (ValueError, TypeError):
            pass
        eligible = get_eligible_contacts(active_company, years) if active_company else []
        windows = [
            {'year': i + 1, 'start': str(s), 'end': str(e)}
            for i, (s, e) in enumerate(_seasonal_windows(years))
        ]
        return JsonResponse({'eligible': len(eligible), 'years': years, 'windows': windows})

    if request.method == 'POST' and active_company:
        from .services import generate_leads_from_history
        raw_limit = request.POST.get('lead_count', '')
        limit = None
        if raw_limit:
            try:
                limit = max(1, int(raw_limit))
            except (ValueError, TypeError):
                pass
        count = generate_leads_from_history(
            company=active_company,
            years=years,
            user=request.user,
            limit=limit,
        )
        if count > 0:
            messages.success(request, f'{count} lead{"s geradas" if count != 1 else " gerada"} e adicionadas aos Prospectos.')
        else:
            messages.info(request, 'Nenhuma lead nova gerada — todos os clientes elegíveis já têm prospectos ou oportunidades abertas.')
        return redirect('crm:crm_home')

    return redirect('crm:crm_home')


@require_http_methods(["POST"])
@login_required
def bulk_delete_leads(request):
    """Delete multiple leads"""
    try:
        data = json.loads(request.body)
        lead_ids = data.get('lead_ids', [])
        
        if not isinstance(lead_ids, list):
            return JsonResponse({
                'success': False,
                'error': 'lead_ids deve ser uma lista'
            }, status=400)
        
        # Filter by company before deleting
        active_company = get_active_company(request)
        leads = Lead.objects.filter(id__in=lead_ids)
        leads = filter_by_company(leads, request)
        
        deleted_count = leads.count()
        leads.delete()
        
        return JsonResponse({
            'success': True,
            'deleted_count': deleted_count
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


@require_http_methods(["POST"])
@login_required
def bulk_mark_won(request):
    """Mark multiple leads as Won"""
    try:
        data = json.loads(request.body)
        lead_ids = data.get('lead_ids', [])
        
        if not isinstance(lead_ids, list):
            return JsonResponse({
                'success': False,
                'error': 'lead_ids deve ser uma lista'
            }, status=400)
        
        # Get active company
        active_company = get_active_company(request)
        
        # Get Won stage
        won_stage = CRMStage.objects.filter(
            Q(owner_company__isnull=True) | Q(owner_company=active_company),
            is_won_stage=True
        ).first()
        
        if not won_stage:
            return JsonResponse({
                'success': False,
                'error': 'Etapa Won não encontrada'
            }, status=404)
        
        # Filter leads by company
        leads = Lead.objects.filter(id__in=lead_ids)
        leads = filter_by_company(leads, request)
        
        # Update leads to Won stage (set closed_at now)
        updated_count = leads.update(stage=won_stage, closed_at=timezone.now(), stage_updated_at=timezone.now())
        
        return JsonResponse({
            'success': True,
            'updated_count': updated_count
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


@require_http_methods(["POST"])
@login_required
def bulk_mark_lost(request):
    """Mark multiple leads as Lost"""
    try:
        data = json.loads(request.body)
        lead_ids = data.get('lead_ids', [])
        
        if not isinstance(lead_ids, list):
            return JsonResponse({
                'success': False,
                'error': 'lead_ids deve ser uma lista'
            }, status=400)
        
        # Get active company
        active_company = get_active_company(request)
        
        # Get Lost stage
        lost_stage = CRMStage.objects.filter(
            Q(owner_company__isnull=True) | Q(owner_company=active_company),
            is_lost_stage=True
        ).first()
        
        if not lost_stage:
            return JsonResponse({
                'success': False,
                'error': 'Etapa Lost não encontrada'
            }, status=404)
        
        # Filter leads by company
        leads = Lead.objects.filter(id__in=lead_ids)
        leads = filter_by_company(leads, request)
        
        # Update leads to Lost stage (no lost_reason required for bulk action)
        updated_count = leads.update(stage=lost_stage, closed_at=timezone.now(), stage_updated_at=timezone.now())
        
        return JsonResponse({
            'success': True,
            'updated_count': updated_count
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


# ─────────────────────────────────────────────────────────
# ActivityType CRUD
# ─────────────────────────────────────────────────────────

@login_required
def activity_type_list_view(request):
    """Lista os Tipos de Atividade com paginação, busca e filtros"""
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
        qs = ActivityType.objects.filter(is_active=False)
    else:
        qs = ActivityType.objects.filter(is_active=True)

    qs = qs.annotate(blueprint_count=Count('blueprints')).order_by('name')

    if search_query:
        field_mapping = {
            'name': Q(name__icontains=search_query),
            'code': Q(code__icontains=search_query),
        }
        if search_field in field_mapping:
            qs = qs.filter(field_mapping[search_field])
        else:
            qs = qs.filter(Q(name__icontains=search_query) | Q(code__icontains=search_query))

    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page_number)

    context = {
        'activity_types': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
    }
    return render(request, 'crm/activity_type_list.html', context)


@login_required
def activity_type_create_view(request):
    """Cria um novo Tipo de Atividade"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip().upper()
        errors = {}
        if not name:
            errors['name'] = 'O nome é obrigatório.'
        if not code:
            errors['code'] = 'O código é obrigatório.'
        elif ActivityType.objects.filter(code=code).exists():
            errors['code'] = f'Já existe um tipo com o código "{code}".'
        if not errors:
            obj = ActivityType.objects.create(name=name, code=code, is_active=True)
            messages.success(request, f'Tipo de Atividade "{obj.name}" criado com sucesso!')
            return redirect('crm:activity_type_list')
        context = {'name': name, 'code': code, 'errors': errors, 'is_edit': False}
        return render(request, 'crm/activity_type_form.html', context)

    return render(request, 'crm/activity_type_form.html', {'is_edit': False})


@login_required
def activity_type_edit_view(request, type_id):
    """Edita um Tipo de Atividade existente"""
    obj = get_object_or_404(ActivityType, id=type_id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip().upper()
        errors = {}
        if not name:
            errors['name'] = 'O nome é obrigatório.'
        if not code:
            errors['code'] = 'O código é obrigatório.'
        elif ActivityType.objects.filter(code=code).exclude(id=obj.id).exists():
            errors['code'] = f'Já existe outro tipo com o código "{code}".'
        if not errors:
            obj.name = name
            obj.code = code
            obj.save(update_fields=['name', 'code'])
            messages.success(request, f'Tipo de Atividade "{obj.name}" atualizado com sucesso!')
            return redirect('crm:activity_type_list')
        context = {'name': name, 'code': code, 'errors': errors, 'is_edit': True, 'object': obj}
        return render(request, 'crm/activity_type_form.html', context)

    context = {'name': obj.name, 'code': obj.code, 'is_edit': True, 'object': obj}
    return render(request, 'crm/activity_type_form.html', context)


@require_http_methods(["POST"])
@login_required
def bulk_archive_activity_types(request):
    """Arquiva múltiplos Tipos de Atividade sem confirmação"""
    from django.db import transaction
    try:
        data = json.loads(request.body)
        ids = data.get('type_ids', [])
        if not isinstance(ids, list) or not ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum tipo selecionado'}}, status=400)
        qs = ActivityType.objects.filter(id__in=ids)
        if not qs.exists():
            return JsonResponse({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Nenhum tipo encontrado'}}, status=404)
        already = list(qs.filter(is_active=False).values_list('name', flat=True))
        to_archive = list(qs.filter(is_active=True))
        if already and not to_archive:
            return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ARCHIVED', 'message': 'Os tipos selecionados já estão arquivados.', 'types': already}}, status=409)
        with transaction.atomic():
            for obj in to_archive:
                obj.is_active = False
                obj.save(update_fields=['is_active'])
        msg = f'{len(to_archive)} tipo(s) arquivado(s) com sucesso.'
        warning = f'{len(already)} já estava(m) arquivado(s).' if already else None
        return JsonResponse({'success': True, 'message': msg, 'warning': warning, 'archived_count': len(to_archive)})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_activity_types(request):
    """Desarquiva múltiplos Tipos de Atividade sem confirmação"""
    from django.db import transaction
    try:
        data = json.loads(request.body)
        ids = data.get('type_ids', [])
        if not isinstance(ids, list) or not ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum tipo selecionado'}}, status=400)
        qs = ActivityType.objects.filter(id__in=ids)
        if not qs.exists():
            return JsonResponse({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Nenhum tipo encontrado'}}, status=404)
        already = list(qs.filter(is_active=True).values_list('name', flat=True))
        to_unarchive = list(qs.filter(is_active=False))
        if already and not to_unarchive:
            return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ACTIVE', 'message': 'Os tipos selecionados já estão ativos.', 'types': already}}, status=409)
        with transaction.atomic():
            for obj in to_unarchive:
                obj.is_active = True
                obj.save(update_fields=['is_active'])
        msg = f'{len(to_unarchive)} tipo(s) reativado(s) com sucesso.'
        warning = f'{len(already)} já estava(m) ativo(s).' if already else None
        return JsonResponse({'success': True, 'message': msg, 'warning': warning, 'unarchived_count': len(to_unarchive)})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_delete_activity_types(request):
    """Elimina múltiplos Tipos de Atividade em massa"""
    from django.db import transaction
    from django.db.models.deletion import ProtectedError

    try:
        data = json.loads(request.body)
        ids = data.get('type_ids', [])

        if not isinstance(ids, list) or not ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhum tipo selecionado'}}, status=400)

        with transaction.atomic():
            deleted_count, _ = ActivityType.objects.filter(id__in=ids).delete()

        return JsonResponse({'success': True, 'deleted_count': deleted_count, 'message': f'{deleted_count} tipo(s) de atividade eliminado(s) com sucesso!'})

    except ProtectedError as e:
        blocking_blueprints = []
        for obj in e.protected_objects:
            if isinstance(obj, ScheduledActivity):
                blocking_blueprints.append({
                    'id': str(obj.id),
                    'label': obj.name or obj.summary,
                    'summary': obj.summary,
                    'activity_type_name': obj.activity_type.name if obj.activity_type else '–',
                })
        return JsonResponse({
            'success': False,
            'error': {
                'code': 'PROTECTED_BY_BLUEPRINTS',
                'message': f'Não é possível eliminar: {len(blocking_blueprints)} blueprint(s) utiliza(m) este tipo de atividade.',
                'blocking_blueprints': blocking_blueprints,
                'count': len(blocking_blueprints),
            }
        }, status=409)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'JSON inválido'}}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': {'code': 'UNKNOWN_ERROR', 'message': str(e)}}, status=500)


# ─────────────────────────────────────────────
# Activity Chains (Cadeias de Atividade)
# ─────────────────────────────────────────────

@login_required
def activity_chain_list_view(request):
    """Lista as Cadeias de Atividade com paginação, busca e filtros"""
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
        qs = ActivityChain.objects.filter(is_active=False)
    else:
        qs = ActivityChain.objects.filter(is_active=True)

    qs = qs.annotate(step_count=Count('steps')).order_by('name')

    if search_query:
        field_mapping = {
            'name': Q(name__icontains=search_query),
            'description': Q(description__icontains=search_query),
        }
        if search_field in field_mapping:
            qs = qs.filter(field_mapping[search_field])
        else:
            qs = qs.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page_number)

    context = {
        'chains': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'total_count': paginator.count,
        'page_size': page_size,
        'status_filter': status_filter,
    }
    return render(request, 'crm/activity_chain_list.html', context)


@login_required
def activity_chain_create_view(request):
    """Cria uma nova Cadeia de Atividade com passos embutidos"""
    from django.db import transaction
    from apps.core.models import Company

    def _to_minutes(value, unit):
        if unit == 'horas': return int(value) * 60
        if unit == 'dias':  return int(value) * 1440
        return int(value)  # minutos

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        applicable_model = request.POST.get('applicable_model', 'lead')
        owner_company_id = request.POST.get('owner_company_id') or None
        steps_json_raw = request.POST.get('steps_json', '[]')

        if not name:
            messages.error(request, 'O nome da cadeia é obrigatório.')
        else:
            try:
                steps_data = json.loads(steps_json_raw)
                owner_company = Company.objects.filter(id=owner_company_id).first() if owner_company_id else None
                with transaction.atomic():
                    chain = ActivityChain.objects.create(
                        name=name,
                        description=description,
                        applicable_model=applicable_model,
                        owner_company=owner_company,
                    )
                    for idx, step in enumerate(steps_data, start=1):
                        activity_id = step.get('activity_id')
                        if not activity_id:
                            continue
                        ActivityChainStep.objects.create(
                            chain=chain,
                            activity_id=activity_id,
                            order=idx,
                            delay_days=_to_minutes(step.get('delay_days', 0), step.get('delay_unit', 'dias')),
                            on_failure_activity_id=step.get('on_failure_activity_id') or None,
                            on_failure_delay_days=_to_minutes(step.get('on_failure_delay_days', 0), step.get('on_failure_delay_unit', 'dias')),
                        )
                messages.success(request, f'Cadeia "{chain.name}" criada com sucesso!')
                return redirect('crm:activity_chain_edit', chain_id=chain.id)
            except Exception as e:
                messages.error(request, f'Erro ao criar cadeia: {e}')

    blueprints = ScheduledActivity.objects.filter(is_active=True).filter(
        Q(applicable_models=[]) | Q(applicable_models__contains=['CRM'])
    ).select_related('activity_type').order_by('activity_type__name', 'name', 'summary')
    companies = Company.objects.filter(is_active=True).order_by('name')

    context = {
        'is_edit': False,
        'chain': None,
        'steps_json': '[]',
        'blueprints': blueprints,
        'companies': companies,
    }
    return render(request, 'crm/activity_chain_form.html', context)


@login_required
def activity_chain_edit_view(request, chain_id):
    """Edita uma Cadeia de Atividade existente com passos embutidos"""
    from django.db import transaction
    from apps.core.models import Company

    def _to_minutes(value, unit):
        if unit == 'horas': return int(value) * 60
        if unit == 'dias':  return int(value) * 1440
        return int(value)

    def _from_minutes(total):
        """Devolve (valor, unidade) para exibir no frontend."""
        if total and total % 1440 == 0:
            return total // 1440, 'dias'
        if total and total % 60 == 0:
            return total // 60, 'horas'
        return total or 0, 'minutos'

    chain = get_object_or_404(ActivityChain, id=chain_id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        applicable_model = request.POST.get('applicable_model', 'lead')
        owner_company_id = request.POST.get('owner_company_id') or None
        steps_json_raw = request.POST.get('steps_json', '[]')

        if not name:
            messages.error(request, 'O nome da cadeia é obrigatório.')
        else:
            try:
                steps_data = json.loads(steps_json_raw)
                owner_company = Company.objects.filter(id=owner_company_id).first() if owner_company_id else None
                with transaction.atomic():
                    chain.name = name
                    chain.description = description
                    chain.applicable_model = applicable_model
                    chain.owner_company = owner_company
                    chain.save(update_fields=['name', 'description', 'applicable_model', 'owner_company'])
                    chain.steps.all().delete()
                    for idx, step in enumerate(steps_data, start=1):
                        activity_id = step.get('activity_id')
                        if not activity_id:
                            continue
                        ActivityChainStep.objects.create(
                            chain=chain,
                            activity_id=activity_id,
                            order=idx,
                            delay_days=_to_minutes(step.get('delay_days', 0), step.get('delay_unit', 'dias')),
                            on_failure_activity_id=step.get('on_failure_activity_id') or None,
                            on_failure_delay_days=_to_minutes(step.get('on_failure_delay_days', 0), step.get('on_failure_delay_unit', 'dias')),
                        )
                messages.success(request, f'Cadeia "{chain.name}" guardada com sucesso!')
                return redirect('crm:activity_chain_edit', chain_id=chain.id)
            except Exception as e:
                messages.error(request, f'Erro ao guardar cadeia: {e}')

    existing_steps = list(
        chain.steps
        .select_related('activity', 'activity__activity_type', 'on_failure_activity')
        .order_by('order')
        .values(
            'activity_id', 'delay_days',
            'on_failure_activity_id', 'on_failure_delay_days',
        )
    )
    steps_for_js = []
    for s in existing_steps:
        delay_val, delay_unit = _from_minutes(s['delay_days'])
        fail_val, fail_unit = _from_minutes(s['on_failure_delay_days'])
        steps_for_js.append({
            'activity_id': str(s['activity_id']),
            'delay_days': delay_val,
            'delay_unit': delay_unit,
            'on_failure_activity_id': str(s['on_failure_activity_id']) if s['on_failure_activity_id'] else '',
            'on_failure_delay_days': fail_val,
            'on_failure_delay_unit': fail_unit,
        })

    blueprints = ScheduledActivity.objects.filter(is_active=True).filter(
        Q(applicable_models=[]) | Q(applicable_models__contains=['CRM'])
    ).select_related('activity_type').order_by('activity_type__name', 'name', 'summary')
    companies = Company.objects.filter(is_active=True).order_by('name')

    context = {
        'is_edit': True,
        'chain': chain,
        'steps_json': json.dumps(steps_for_js),
        'blueprints': blueprints,
        'companies': companies,
    }
    return render(request, 'crm/activity_chain_form.html', context)


@require_http_methods(["POST"])
@login_required
def bulk_archive_chains(request):
    """Arquiva múltiplas Cadeias de Atividade sem confirmação"""
    from django.db import transaction
    try:
        data = json.loads(request.body)
        ids = data.get('chain_ids', [])
        if not isinstance(ids, list) or not ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma cadeia selecionada'}}, status=400)
        qs = ActivityChain.objects.filter(id__in=ids)
        if not qs.exists():
            return JsonResponse({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma cadeia encontrada'}}, status=404)
        already = list(qs.filter(is_active=False).values_list('name', flat=True))
        to_archive = list(qs.filter(is_active=True))
        if already and not to_archive:
            return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ARCHIVED', 'message': 'As cadeias selecionadas já estão arquivadas.', 'items': already}}, status=409)
        with transaction.atomic():
            for obj in to_archive:
                obj.is_active = False
                obj.save(update_fields=['is_active'])
        msg = f'{len(to_archive)} cadeia(s) arquivada(s) com sucesso.'
        warning = f'{len(already)} já estava(m) arquivada(s).' if already else None
        return JsonResponse({'success': True, 'message': msg, 'warning': warning})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_unarchive_chains(request):
    """Desarquiva múltiplas Cadeias de Atividade"""
    from django.db import transaction
    try:
        data = json.loads(request.body)
        ids = data.get('chain_ids', [])
        if not isinstance(ids, list) or not ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma cadeia selecionada'}}, status=400)
        qs = ActivityChain.objects.filter(id__in=ids)
        if not qs.exists():
            return JsonResponse({'success': False, 'error': {'code': 'NOT_FOUND', 'message': 'Nenhuma cadeia encontrada'}}, status=404)
        already = list(qs.filter(is_active=True).values_list('name', flat=True))
        to_unarchive = list(qs.filter(is_active=False))
        if already and not to_unarchive:
            return JsonResponse({'success': False, 'error': {'code': 'ALREADY_ACTIVE', 'message': 'As cadeias selecionadas já estão ativas.', 'items': already}}, status=409)
        with transaction.atomic():
            for obj in to_unarchive:
                obj.is_active = True
                obj.save(update_fields=['is_active'])
        msg = f'{len(to_unarchive)} cadeia(s) reativada(s) com sucesso.'
        warning = f'{len(already)} já estava(m) ativa(s).' if already else None
        return JsonResponse({'success': True, 'message': msg, 'warning': warning})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def bulk_delete_chains(request):
    """Elimina múltiplas Cadeias de Atividade em massa"""
    from django.db import transaction
    try:
        data = json.loads(request.body)
        ids = data.get('chain_ids', [])
        if not isinstance(ids, list) or not ids:
            return JsonResponse({'success': False, 'error': {'code': 'EMPTY_SELECTION', 'message': 'Nenhuma cadeia selecionada'}}, status=400)
        with transaction.atomic():
            deleted_count, _ = ActivityChain.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True, 'deleted_count': deleted_count, 'message': f'{deleted_count} cadeia(s) eliminada(s) com sucesso!'})
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': {'code': 'INVALID_JSON', 'message': 'JSON inválido'}}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': {'code': 'UNKNOWN_ERROR', 'message': str(e)}}, status=500)


# ============================================================
# LEAD ACTIVITIES (Atividades de uma Lead específica)
# ============================================================

@require_http_methods(["POST"])
@login_required
def lead_activity_create(request, lead_id):
    """
    Cria uma nova atividade vinculada a uma lead específica.
    Endpoint AJAX: POST /crm/leads/<lead_id>/activities/create/
    """
    active_company = get_active_company(request)
    lead = get_object_or_404(Lead, id=lead_id, owner_company=active_company)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    activity_type = data.get('activity_type', '').strip()
    summary = data.get('summary', '').strip()
    due_date_str = data.get('due_date', '').strip()
    assigned_to_id = data.get('assigned_to_id')
    scheduled_activity_id = data.get('scheduled_activity_id', '').strip()

    # Resolve ScheduledActivity blueprint (optional)
    sa_obj = None
    if scheduled_activity_id:
        try:
            sa_obj = ScheduledActivity.objects.select_related('activity_type').get(id=scheduled_activity_id)
            # Derive activity_type from blueprint if not explicitly provided
            if not activity_type and sa_obj.activity_type:
                activity_type = sa_obj.activity_type.code
        except ScheduledActivity.DoesNotExist:
            pass

    errors = {}
    if not activity_type:
        errors['activity_type'] = 'Tipo de atividade é obrigatório.'
    elif activity_type not in dict(Activity.ACTIVITY_TYPE_CHOICES):
        errors['activity_type'] = 'Tipo de atividade inválido.'
    if not summary:
        errors['summary'] = 'Resumo é obrigatório.'
    if not due_date_str:
        errors['due_date'] = 'Data limite é obrigatória.'
    else:
        from datetime import date as date_type
        try:
            from datetime import datetime
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            if due_date < date_type.today():
                errors['due_date'] = 'Data limite não pode ser no passado.'
        except ValueError:
            errors['due_date'] = 'Formato de data inválido (use YYYY-MM-DD).'

    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    assigned_to = None
    if assigned_to_id:
        try:
            assigned_to = User.objects.get(id=assigned_to_id, is_active=True)
        except User.DoesNotExist:
            pass

    activity = Activity.objects.create(
        lead=lead,
        activity_type=activity_type,
        scheduled_activity=sa_obj,
        summary=summary,
        due_date=due_date,
        assigned_to=assigned_to or request.user,
        owner_company=active_company,
    )

    # ── Criar notificação para o utilizador atribuído ─────────────────────
    try:
        from apps.core.models import Notification as _Notification
        import logging as _logging
        _nlog = _logging.getLogger('apps.crm.notifications')
        _today = date_type.today()
        if activity.due_date < _today:
            _notif_type = 'ACTIVITY_OVERDUE'
        elif activity.due_date == _today:
            _notif_type = 'ACTIVITY_TODAY'
        else:
            _notif_type = 'ACTIVITY_UPCOMING'
        _lead_name = lead.title or (str(lead.contact) if lead.contact else 'Lead')
        _Notification.objects.create(
            user=activity.assigned_to,
            notification_type=_notif_type,
            title=activity.summary,
            message=f'Lead: {_lead_name}',
            link=f'/crm/leads/{str(lead.id)}/',
            related_object_id=activity.id,  # para apagar quando a actividade for concluída
        )
    except Exception as _e:
        import traceback as _tb
        import logging as _logging
        _logging.getLogger('apps.crm.notifications').error(
            'Notification creation failed for activity %s: %s\n%s',
            activity.id, _e, _tb.format_exc()
        )

    today = date_type.today()
    return JsonResponse({
        'success': True,
        'message': f'Atividade "{activity.summary}" criada com sucesso!',
        'activity': {
            'id': str(activity.id),
            'activity_type': activity.activity_type,
            'activity_type_display': activity.get_activity_type_display(),
            'scheduled_activity_id': str(activity.scheduled_activity.id) if activity.scheduled_activity else '',
            'icon_svg': activity.scheduled_activity.icon_svg if activity.scheduled_activity and activity.scheduled_activity.icon_svg else '',
            'icon_color': activity.scheduled_activity.icon_color if activity.scheduled_activity and activity.scheduled_activity.icon_color else '#6366F1',
            'summary': activity.summary,
            'due_date': activity.due_date.strftime('%Y-%m-%d'),
            'due_date_display': activity.due_date.strftime('%d/%m/%Y'),
            'assigned_to': activity.assigned_to.get_full_name() or activity.assigned_to.username if activity.assigned_to else None,
            'assigned_to_id': str(activity.assigned_to.id) if activity.assigned_to else '',
            'is_done': activity.is_done,
            'is_overdue': activity.is_overdue,
            'is_today': activity.due_date == today,
            'feedback': '',
        }
    }, status=201)


@require_http_methods(["POST"])
@login_required
def lead_activity_mark_done(request, lead_id, activity_id):
    """
    Marca uma atividade como concluída com feedback.
    Endpoint AJAX: POST /crm/leads/<lead_id>/activities/<activity_id>/done/
    """
    active_company = get_active_company(request)
    lead = get_object_or_404(Lead, id=lead_id, owner_company=active_company)
    activity = get_object_or_404(Activity, id=activity_id, lead=lead)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    feedback = data.get('feedback', '').strip()

    activity.is_done = True
    activity.feedback = feedback
    activity.done_date = timezone.now()
    activity.save(update_fields=['is_done', 'feedback', 'done_date'])

    # Remover notificação da actividade (está concluída — não deve continuar no sino)
    try:
        from apps.core.models import Notification as _N
        _N.objects.filter(
            related_object_id=activity.id,
            notification_type__in=['ACTIVITY_OVERDUE', 'ACTIVITY_TODAY', 'ACTIVITY_UPCOMING'],
        ).delete()
    except Exception:
        pass

    return JsonResponse({
        'success': True,
        'message': f'Atividade "{activity.summary}" marcada como concluída!',
        'activity': {
            'id': str(activity.id),
            'is_done': activity.is_done,
            'done_date': activity.done_date.strftime('%d/%m/%Y %H:%M'),
            'feedback': activity.feedback,
        }
    })


@require_http_methods(["POST"])
@login_required
def lead_activity_delete(request, lead_id, activity_id):
    """
    Elimina uma atividade de uma lead.
    Endpoint AJAX: POST /crm/leads/<lead_id>/activities/<activity_id>/delete/
    """
    active_company = get_active_company(request)
    lead = get_object_or_404(Lead, id=lead_id, owner_company=active_company)
    activity = get_object_or_404(Activity, id=activity_id, lead=lead)

    summary = activity.summary
    activity_id = activity.id

    # Remover notificação antes de apagar a actividade
    try:
        from apps.core.models import Notification as _N
        _N.objects.filter(
            related_object_id=activity_id,
            notification_type__in=['ACTIVITY_OVERDUE', 'ACTIVITY_TODAY', 'ACTIVITY_UPCOMING'],
        ).delete()
    except Exception:
        pass

    activity.delete()

    return JsonResponse({
        'success': True,
        'message': f'Atividade "{summary}" eliminada com sucesso!',
    })


@require_http_methods(["POST"])
@login_required
def lead_activity_update(request, lead_id, activity_id):
    """
    Atualiza uma atividade existente de uma lead (apenas atividades pendentes).
    Endpoint AJAX: POST /crm/leads/<lead_id>/activities/<activity_id>/update/
    """
    from datetime import date as date_type, datetime

    active_company = get_active_company(request)
    lead = get_object_or_404(Lead, id=lead_id, owner_company=active_company)
    activity = get_object_or_404(Activity, id=activity_id, lead=lead, is_done=False)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    activity_type = data.get('activity_type', '').strip()
    summary = data.get('summary', '').strip()
    due_date_str = data.get('due_date', '').strip()
    assigned_to_id = data.get('assigned_to_id')
    scheduled_activity_id = data.get('scheduled_activity_id', '').strip()

    # Resolve ScheduledActivity blueprint (optional)
    sa_obj = None
    if scheduled_activity_id:
        try:
            sa_obj = ScheduledActivity.objects.select_related('activity_type').get(id=scheduled_activity_id)
            if not activity_type and sa_obj.activity_type:
                activity_type = sa_obj.activity_type.code
        except ScheduledActivity.DoesNotExist:
            pass

    errors = {}
    if not activity_type:
        errors['activity_type'] = 'Tipo de atividade é obrigatório.'
    elif activity_type not in dict(Activity.ACTIVITY_TYPE_CHOICES):
        errors['activity_type'] = 'Tipo de atividade inválido.'
    if not summary:
        errors['summary'] = 'Resumo é obrigatório.'
    due_date = None
    if not due_date_str:
        errors['due_date'] = 'Data limite é obrigatória.'
    else:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            errors['due_date'] = 'Formato de data inválido (use YYYY-MM-DD).'

    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    assigned_to = None
    if assigned_to_id:
        try:
            assigned_to = User.objects.get(id=assigned_to_id, is_active=True)
        except User.DoesNotExist:
            pass

    activity.activity_type = activity_type
    activity.scheduled_activity = sa_obj
    activity.summary = summary
    activity.due_date = due_date
    activity.assigned_to = assigned_to or request.user
    activity.save(update_fields=['activity_type', 'scheduled_activity', 'summary', 'due_date', 'assigned_to'])

    today = date_type.today()
    return JsonResponse({
        'success': True,
        'message': f'Atividade "{activity.summary}" atualizada com sucesso!',
        'activity': {
            'id': str(activity.id),
            'activity_type': activity.activity_type,
            'activity_type_display': activity.get_activity_type_display(),
            'scheduled_activity_id': str(activity.scheduled_activity.id) if activity.scheduled_activity else '',
            'icon_svg': activity.scheduled_activity.icon_svg if activity.scheduled_activity and activity.scheduled_activity.icon_svg else '',
            'icon_color': activity.scheduled_activity.icon_color if activity.scheduled_activity and activity.scheduled_activity.icon_color else '#6366F1',
            'summary': activity.summary,
            'due_date': activity.due_date.strftime('%Y-%m-%d'),
            'due_date_display': activity.due_date.strftime('%d/%m/%Y'),
            'assigned_to': activity.assigned_to.get_full_name() or activity.assigned_to.username if activity.assigned_to else None,
            'assigned_to_id': str(activity.assigned_to.id) if activity.assigned_to else '',
            'is_done': False,
            'is_overdue': activity.due_date < today,
            'is_today': activity.due_date == today,
            'feedback': '',
        }
    })


@require_http_methods(["POST"])
@login_required
def lead_chain_start(request, lead_id):
    """
    Inicia uma cadeia de atividades para uma lead.
    Cria ActivityChainInstance + Activity records para cada step.
    Endpoint AJAX: POST /crm/leads/<lead_id>/chains/start/
    """
    from datetime import date as date_type, timedelta as td
    from django.contrib.contenttypes.models import ContentType

    active_company = get_active_company(request)
    try:
        lead = Lead.objects.select_related('contact', 'contact__company').get(
            id=lead_id, owner_company=active_company
        )
    except Lead.DoesNotExist:
        from django.http import Http404
        raise Http404

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    chain_id = data.get('chain_id', '').strip()
    assigned_to_id = data.get('assigned_to_id')

    if not chain_id:
        return JsonResponse({'success': False, 'errors': {'chain_id': 'Cadeia é obrigatória.'}}, status=400)

    chain = get_object_or_404(ActivityChain, id=chain_id, is_active=True)

    # Validate chain belongs to company
    if chain.owner_company and chain.owner_company != active_company:
        return JsonResponse({'success': False, 'error': 'Acesso negado à cadeia selecionada.'}, status=403)

    assigned_user = request.user
    if assigned_to_id:
        try:
            assigned_user = User.objects.get(id=assigned_to_id, is_active=True)
        except User.DoesNotExist:
            pass

    # Create ActivityChainInstance
    lead_ct = ContentType.objects.get_for_model(Lead)
    instance = ActivityChainInstance.objects.create(
        chain=chain,
        content_type=lead_ct,
        object_id=lead.id,
        assigned_to=assigned_user,
        owner_company=active_company,
        status='IN_PROGRESS',
    )

    # Create Activity records for each step in the chain
    created_activities = []
    today = date_type.today()
    cumulative_delay = 0  # accumulated in minutes (delay_days field stores minutes)

    for step in chain.steps.select_related('activity', 'activity__activity_type', 'default_assigned_to').order_by('order'):
        cumulative_delay += step.delay_days
        due = today + td(minutes=cumulative_delay)
        step_assigned = step.default_assigned_to or assigned_user

        # Use ActivityType.code from the blueprint's activity type
        bp = step.activity
        if bp.activity_type:
            act_type = bp.activity_type.code
            # Ensure the code is a valid ACTIVITY_TYPE_CHOICES key
            valid_types = dict(Activity.ACTIVITY_TYPE_CHOICES)
            if act_type not in valid_types:
                act_type = 'TODO'
        else:
            act_type = 'TODO'

        summary_text = bp.summary if bp.summary else (bp.name or 'Atividade')

        activity = Activity.objects.create(
            lead=lead,
            activity_type=act_type,
            scheduled_activity=bp,
            summary=f"[{chain.name}] {summary_text}",
            due_date=due,
            assigned_to=step_assigned,
            owner_company=active_company,
        )

        # ── Criar notificação por passo da cadeia ─────────────────────────
        try:
            from apps.core.models import Notification as _Notification
            if due < today:
                _notif_type = 'ACTIVITY_OVERDUE'
            elif due == today:
                _notif_type = 'ACTIVITY_TODAY'
            else:
                _notif_type = 'ACTIVITY_UPCOMING'
            _lead_name = lead.title or (str(lead.contact) if lead.contact else 'Lead')
            _Notification.objects.create(
                user=step_assigned,
                notification_type=_notif_type,
                title=f'[{chain.name}] {summary_text}',
                message=f'Lead: {_lead_name}',
                link=f'/crm/leads/{str(lead.id)}/',
                related_object_id=activity.id,  # para apagar quando a actividade for concluída
            )
        except Exception as _ce:
            import traceback as _tb
            import logging as _logging
            _logging.getLogger('apps.crm.notifications').error(
                'Notification creation failed for chain step: %s\n%s',
                _ce, _tb.format_exc()
            )

        created_activities.append({
            'id': str(activity.id),
            'activity_type': activity.activity_type,
            'activity_type_display': activity.get_activity_type_display(),
            'scheduled_activity_id': str(bp.id),
            'icon_svg': bp.icon_svg if bp.icon_svg else '',
            'icon_color': bp.icon_color or '#6366F1',
            'summary': _resolve_summary(activity.summary, lead),
            'due_date': activity.due_date.strftime('%Y-%m-%d'),
            'due_date_display': activity.due_date.strftime('%d/%m/%Y'),
            'assigned_to': activity.assigned_to.get_full_name() or activity.assigned_to.username if activity.assigned_to else '',
            'assigned_to_id': str(activity.assigned_to.id) if activity.assigned_to else '',
            'is_done': False,
            'feedback': '',
            'is_overdue': False,
            'is_today': activity.due_date == today,
        })

    return JsonResponse({
        'success': True,
        'message': f'Cadeia "{chain.name}" iniciada com {len(created_activities)} atividade(s)!',
        'activities': created_activities,
        'chain_instance_id': str(instance.id),
    }, status=201)


# ============================================================
# LEAD NOTES (Notas internas do Chatter)
# ============================================================

@login_required
@require_http_methods(['GET'])
def lead_notes_list(request, lead_id):
    """
    GET /crm/leads/<lead_id>/notes/
    Retorna as notas internas do chatter de um lead.
    """
    active_company = get_active_company(request)
    lead = get_object_or_404(Lead, id=lead_id, owner_company=active_company)
    notes = lead.chatter_notes.select_related('author').order_by('-created_at')[:100]
    return JsonResponse({
        'notes': [
            {
                'id': str(n.id),
                'author': n.author.get_full_name() or n.author.username if n.author else 'Sistema',
                'author_initials': ''.join(p[0].upper() for p in (n.author.get_full_name() or n.author.username).split()[:2]) if n.author else 'S',
                'content': n.content,
                'created_at': n.created_at.strftime('%d/%m/%Y %H:%M'),
            }
            for n in notes
        ]
    })


@login_required
@require_http_methods(['POST'])
def lead_note_create(request, lead_id):
    """
    POST /crm/leads/<lead_id>/notes/create/
    Cria nota interna e gera notificações MENTION para @utilizadores mencionados.
    """
    active_company = get_active_company(request)
    lead = get_object_or_404(Lead, id=lead_id, owner_company=active_company)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    content = data.get('content', '').strip()
    if not content:
        return JsonResponse({'success': False, 'error': 'Conteúdo não pode estar vazio.'}, status=400)

    urgent = bool(data.get('urgent', False))

    note = LeadNote.objects.create(lead=lead, author=request.user, content=content)

    # Parsear @menções e criar notificações
    import re
    mentioned_usernames = list(set(re.findall(r'@(\w+)', content)))
    if mentioned_usernames:
        try:
            from apps.core.models import Notification as _N
            mentioned_users = User.objects.filter(username__in=mentioned_usernames, is_active=True)
            author_display = request.user.get_full_name() or request.user.username
            for mu in mentioned_users:
                _N.objects.create(
                    user=mu,
                    notification_type='MENTION',
                    title=f'{author_display} mencionou-te numa nota',
                    message=f'Lead: {lead.title}',
                    link=f'/crm/leads/{str(lead.id)}/',
                    related_object_id=note.id,
                    is_urgent=urgent,
                )
        except Exception:
            pass

    return JsonResponse({
        'success': True,
        'note': {
            'id': str(note.id),
            'author': note.author.get_full_name() or note.author.username if note.author else 'Sistema',
            'author_initials': ''.join(p[0].upper() for p in (note.author.get_full_name() or note.author.username).split()[:2]) if note.author else 'S',
            'content': note.content,
            'created_at': note.created_at.strftime('%d/%m/%Y %H:%M'),
        }
    }, status=201)


@login_required
@require_http_methods(['GET'])
def users_search_api(request):
    """
    GET /crm/api/users/search/?q=<query>
    Devolve utilizadores activos para o @mention dropdown (máx. 10).
    """
    q = request.GET.get('q', '').strip()
    qs = User.objects.filter(is_active=True)
    if q:
        qs = qs.filter(
            Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)
        )
    qs = qs.order_by('first_name', 'username')[:10]
    return JsonResponse({
        'users': [
            {
                'id': str(u.id),
                'username': u.username,
                'display': u.get_full_name() or u.username,
                'initials': ''.join(p[0].upper() for p in (u.get_full_name() or u.username).split()[:2]),
            }
            for u in qs
        ]
    })


# ---------------------------------------------------------------------------
# Lead Email (chatter — aba "Enviar Mensagem")
# ---------------------------------------------------------------------------

@login_required
@require_http_methods(['POST'])
def lead_send_email(request, lead_id):
    """
    Envia um email ao contacto da lead e regista-o no chatter via ChatterMessage.

    Aceita multipart/form-data:
      - body       (str)   texto da mensagem
      - to_email   (str)   destinatário (opcional — fallback: lead.email_from)
      - attachments (files) um ou mais ficheiros

    Resposta: { "success": true, "email": {...} } ou { "success": false, "error": "..." }
    """
    import os, mimetypes
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile
    from apps.core.email_utils import send_email_for_record

    lead = get_object_or_404(Lead, id=lead_id)

    to_email = (request.POST.get('to_email') or '').strip() or (lead.email_from or '')
    body     = (request.POST.get('body') or '').strip()
    body_html = (request.POST.get('body_html') or '').strip()
    cc       = (request.POST.get('cc') or '').strip()
    bcc      = (request.POST.get('bcc') or '').strip()

    if not to_email:
        return JsonResponse({'success': False, 'error': 'A lead não tem email. Preenche o campo Email na lead.'})
    if not body and not request.FILES.getlist('attachments'):
        return JsonResponse({'success': False, 'error': 'Escreve uma mensagem ou adiciona um ficheiro antes de enviar.'})

    subject = lead.title or 'Mensagem'

    # Gravar ficheiros em media/chatter/<lead_id>/
    attachments = []
    for f in request.FILES.getlist('attachments'):
        ext  = os.path.splitext(f.name)[1]
        rel  = f'chatter/{lead_id}/{f.name}'
        path = default_storage.save(rel, ContentFile(f.read()))
        url  = default_storage.url(path)
        mime = mimetypes.guess_type(f.name)[0] or 'application/octet-stream'
        # Relê o conteúdo do disco para o envio SMTP
        with default_storage.open(path, 'rb') as fp:
            content = fp.read()
        attachments.append({
            'filename' : f.name,
            'url'      : url,
            'size'     : f.size,
            'mime_type': mime,
            'content'  : content,
        })

    to_name = lead.contact_name or (
        lead.contact.get_full_name() if lead.contact and hasattr(lead.contact, 'get_full_name') else ''
    )

    # --- Threading: ligar ao fio de conversa existente desta lead ---
    # Busca todos os emails (outbound + inbound) ordenados por data
    from apps.core.models import ChatterMessage as _CM
    _ct = ContentType.objects.get_for_model(Lead)
    thread_msgs = (
        _CM.objects
        .filter(content_type=_ct, object_id=lead.id, message_type='EMAIL')
        .exclude(message_id='')
        .order_by('created_at')
        .values_list('message_id', flat=True)
    )
    thread_ids = list(thread_msgs)  # ex: ['<id1>', '<id2>', '<id3>']

    # In-Reply-To = o último message_id do fio
    # References  = todos os message_ids do fio, separados por espaço
    in_reply_to = thread_ids[-1] if thread_ids else ''
    references  = ' '.join(thread_ids) if thread_ids else ''

    # Se houver resposta anterior, prefixar o assunto com "Re:" se ainda não tiver
    if thread_ids and not subject.startswith('Re:'):
        subject = f'Re: {subject}'
    # ------------------------------------------------------------------

    result = send_email_for_record(
        user=request.user,
        record=lead,
        to_email=to_email,
        subject=subject,
        body=body,
        body_html=body_html or None,
        to_name=to_name,
        attachments=attachments,
        cc=cc,
        bcc=bcc,
        in_reply_to=in_reply_to,
        references=references,
    )

    if not result['success']:
        return JsonResponse(result)

    # Devolver o email recém-criado para atualizar o chat no frontend
    from apps.core.models import ChatterMessage
    ct = ContentType.objects.get_for_model(Lead)
    em = ChatterMessage.objects.filter(
        content_type=ct, object_id=lead.id, message_type='EMAIL',
        message_id=result['message_id'],
    ).select_related('author').first()

    email_data = None
    if em:
        author = em.author
        email_data = {
            'id'          : str(em.id),
            'direction'   : em.direction,
            'from_email'  : em.from_email,
            'to_email'    : em.to_email,
            'cc_emails'   : em.cc_emails or '',
            'bcc_emails'  : em.bcc_emails or '',
            'subject'     : em.subject,
            'body'        : em.body,
            'body_html'   : em.body_html or '',
            'attachments' : em.attachments or [],
            'sent_by'     : author.get_full_name() or author.username if author else None,
            'sent_by_initials': ''.join(
                p[0].upper() for p in ((author.get_full_name() or author.username).split()[:2])
            ) if author else '?',
            'sent_at'     : em.sent_at.isoformat() if em.sent_at else em.created_at.isoformat(),
        }

    return JsonResponse({'success': True, 'email': email_data})


@login_required
@require_http_methods(['GET'])
def lead_emails_list(request, lead_id):
    """
    Lista os emails (ChatterMessage type=EMAIL) de uma lead.

    Resposta JSON:
      { "emails": [ { id, direction, from_email, to_email, subject, body,
                      sent_by, sent_at, created_at } ] }
    """
    from django.contrib.contenttypes.models import ContentType
    from apps.core.models import ChatterMessage

    lead = get_object_or_404(Lead, id=lead_id)
    ct = ContentType.objects.get_for_model(Lead)

    qs = ChatterMessage.objects.filter(
        content_type=ct,
        object_id=lead.id,
        message_type='EMAIL',
    ).select_related('author').order_by('created_at')

    emails = []
    for em in qs:
        author = em.author
        emails.append({
            'id': str(em.id),
            'direction': em.direction,
            'from_email': em.from_email,
            'to_email': em.to_email,
            'cc_emails': em.cc_emails or '',
            'bcc_emails': em.bcc_emails or '',
            'subject': em.subject,
            'body': em.body,
            'body_html': em.body_html or '',
            'attachments': em.attachments or [],
            'sent_by': author.get_full_name() or author.username if author else None,
            'sent_by_initials': ''.join(
                p[0].upper() for p in ((author.get_full_name() or author.username).split()[:2])
            ) if author else '?',
            'sent_at': em.sent_at.isoformat() if em.sent_at else em.created_at.isoformat(),
            'created_at': em.created_at.isoformat(),
        })

    return JsonResponse({'emails': emails})


# ---------------------------------------------------------------------------
# Lead Email — polling IMAP (manual "Verificar respostas")
# ---------------------------------------------------------------------------

@login_required
@require_http_methods(['POST'])
def lead_poll_inbox(request, lead_id):
    """
    Endpoint manual: verifica agora o IMAP do utilizador em sessão e guarda
    quaisquer respostas inbound encontradas para esta lead.

    Resposta: { "success": true, "new_emails": [...], "count": N }
    """
    from apps.core.models import ChatterMessage
    from apps.core.email_utils import poll_imap_replies_for_user

    lead = get_object_or_404(Lead, id=lead_id)

    # Validar configuração SMTP/IMAP do utilizador
    try:
        config = request.user.email_config
    except Exception:
        return JsonResponse({
            'success': False,
            'error'  : 'Sem configuração de email. Configura o SMTP no teu perfil.',
        })

    if not config.is_active or not config.has_smtp_configured:
        return JsonResponse({
            'success': False,
            'error'  : 'Configuração de email inativa ou incompleta.',
        })

    ct = ContentType.objects.get_for_model(Lead)

    # Message-IDs dos emails outbound já enviados para esta lead
    known_ids = set(
        ChatterMessage.objects
        .filter(
            content_type=ct,
            object_id=lead.id,
            message_type='EMAIL',
            direction=ChatterMessage.DIRECTION_OUTBOUND,
        )
        .exclude(message_id='')
        .values_list('message_id', flat=True)
    )

    if not known_ids:
        return JsonResponse({
            'success'   : True,
            'new_emails': [],
            'count'     : 0,
            'message'   : 'Ainda não enviaste nenhum email para esta lead.',
        })

    # Polling IMAP
    try:
        inbound = poll_imap_replies_for_user(config, known_message_ids=known_ids)
    except Exception as e:
        logger.error('lead_poll_inbox: erro IMAP para lead %s: %s', lead_id, e)
        return JsonResponse({
            'success': False,
            'error'  : f'Erro ao ligar ao servidor IMAP: {e}',
        })

    # Auto-follow: garante que o vendedor da lead está sempre subscrito
    if lead.assigned_to:
        ChatterFollower.objects.get_or_create(
            content_type=ct,
            object_id=lead.id,
            user=lead.assigned_to,
            defaults={'added_by': None},
        )

    new_emails = []
    for em in inbound:
        imap_mid = em['imap_message_id']

        # Evitar duplicados
        if imap_mid and ChatterMessage.objects.filter(
            message_id=imap_mid,
            direction=ChatterMessage.DIRECTION_INBOUND,
        ).exists():
            continue

        # Confirmar que a resposta é mesmo para esta lead
        reply_ids = set(re.findall(r'<[^>]+>', em['in_reply_to']))
        reply_ids.update(re.findall(r'<[^>]+>', em['references']))
        if not reply_ids.intersection(known_ids):
            continue

        try:
            msg = ChatterMessage.objects.create(
                content_type=ct,
                object_id=lead.id,
                author=None,                        # inbound — sem autor interno
                message_type='EMAIL',
                direction=ChatterMessage.DIRECTION_INBOUND,
                from_email=em['from_email'],
                to_email=config.email_address,      # nós recebemos
                subject=em['subject'],
                body=em['body'],
                body_html=em.get('body_html', ''),
                message_id=imap_mid,
                in_reply_to=em['in_reply_to'],
                sent_at=em['date'],
                is_internal=False,
            )
            new_emails.append({
                'id'              : str(msg.id),
                'direction'       : msg.direction,
                'from_email'      : msg.from_email,
                'to_email'        : msg.to_email or '',
                'cc_emails'       : msg.cc_emails or '',
                'bcc_emails'      : msg.bcc_emails or '',
                'subject'         : msg.subject,
                'body'            : msg.body,
                'body_html'       : msg.body_html or '',
                'attachments'     : msg.attachments or [],
                'sent_by'         : None,
                'sent_by_initials': '?',
                'sent_at'         : msg.sent_at.isoformat() if msg.sent_at else msg.created_at.isoformat(),
            })
            # Notificar todos os seguidores desta lead
            preview = (msg.body or '')[:120].rstrip()
            if len(msg.body or '') > 120:
                preview += '…'
            notify_followers(
                lead,
                'EMAIL',
                f'{lead.title} — Novo email de {msg.from_email}',
                message=preview,
                link=f'/crm/leads/{lead.id}/',
            )
        except Exception as e:
            logger.error('lead_poll_inbox: erro ao guardar inbound: %s', e)

    logger.info(
        'lead_poll_inbox: lead=%s encontrou %d novos emails inbound', lead_id, len(new_emails)
    )
    return JsonResponse({'success': True, 'new_emails': new_emails, 'count': len(new_emails)})


# ---------------------------------------------------------------------------
# Lead Email Templates (chatter — botão "Email Template")
# ---------------------------------------------------------------------------

@login_required
@require_http_methods(['GET'])
def lead_email_templates(request, lead_id):
    """
    Devolve templates de email filtrados para o módulo CRM.
    Inclui templates globais (owner_company=NULL) e da empresa do utilizador.

    GET /crm/leads/<id>/email-templates/

    Query params opcionais:
        ?q=texto   — filtrar por nome

    Resposta: { "templates": [ { id, name, subject, body_html, placeholders }, ... ] }
    """
    from apps.core.models import EmailTemplate

    lead = get_object_or_404(Lead, id=lead_id)

    # Templates disponíveis: globais + da empresa do utilizador
    qs = EmailTemplate.objects.filter(module='CRM')

    user_company = getattr(request.user, 'company', None)
    if user_company:
        qs = qs.filter(Q(owner_company__isnull=True) | Q(owner_company=user_company))
    else:
        qs = qs.filter(owner_company__isnull=True)

    # Filtro por nome (opcional)
    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(name__icontains=q)

    qs = qs.order_by('name')

    # Resolver placeholders com dados reais da lead
    def resolve_placeholders(text, placeholders):
        """Substitui {{1}}, {{2}}, etc. pelos valores reais da lead."""
        if not text or not placeholders:
            return text
        result = text
        for key, cfg in placeholders.items():
            placeholder = '{{' + key + '}}'
            if placeholder not in result:
                continue
            # Navegar pelo field path (ex: "lead.contact.name")
            field_path = cfg.get('field', '')
            fallback = cfg.get('fallback', '')
            value = fallback
            if field_path.startswith('lead.'):
                parts = field_path[5:].split('.')  # remove "lead." prefix
                obj = lead
                try:
                    for part in parts:
                        obj = getattr(obj, part, None)
                        if obj is None:
                            break
                    if obj is not None:
                        value = str(obj)
                except Exception:
                    pass
            result = result.replace(placeholder, value)
        return result

    templates = []
    for tmpl in qs:
        placeholders = tmpl.available_placeholders or {}
        templates.append({
            'id':           str(tmpl.id),
            'name':         tmpl.name,
            'subject':      resolve_placeholders(tmpl.subject, placeholders),
            'body_html':    resolve_placeholders(tmpl.body_html, placeholders),
            'placeholders': placeholders,
        })

    return JsonResponse({'templates': templates})


# ---------------------------------------------------------------------------
# Lead Followers (Chatter)
# ---------------------------------------------------------------------------

@login_required
@require_http_methods(['GET', 'POST'])
def lead_followers_api(request, lead_id):
    """
    GET  /crm/leads/<id>/followers/        → lista seguidores
    POST /crm/leads/<id>/followers/        → adiciona seguidor  { user_id }
    """
    lead = get_object_or_404(Lead, id=lead_id)
    ct   = ContentType.objects.get_for_model(Lead)

    if request.method == 'GET':
        # Auto-follow: vendedor da lead + utilizador atual são sempre subscritos
        auto_users = [u for u in [lead.assigned_to, request.user] if u]
        for u in auto_users:
            ChatterFollower.objects.get_or_create(
                content_type=ct,
                object_id=lead.id,
                user=u,
                defaults={'added_by': None},
            )

        followers = (
            ChatterFollower.objects
            .filter(content_type=ct, object_id=lead.id)
            .select_related('user')
            .order_by('created_at')
        )
        return JsonResponse({
            'followers': [
                {
                    'user_id' : str(f.user.id),
                    'display' : f.user.get_full_name() or f.user.username,
                    'initials': ''.join(
                        p[0].upper()
                        for p in (f.user.get_full_name() or f.user.username).split()[:2]
                    ),
                }
                for f in followers
            ]
        })

    # POST — adicionar
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    user_id = data.get('user_id', '').strip()
    if not user_id:
        return JsonResponse({'success': False, 'error': 'user_id obrigatório'}, status=400)

    try:
        target_user = User.objects.get(id=user_id, is_active=True)
    except (User.DoesNotExist, Exception):
        return JsonResponse({'success': False, 'error': 'Utilizador não encontrado'}, status=404)

    ChatterFollower.objects.get_or_create(
        content_type=ct,
        object_id=lead.id,
        user=target_user,
        defaults={'added_by': request.user},
    )
    display  = target_user.get_full_name() or target_user.username
    initials = ''.join(p[0].upper() for p in display.split()[:2])
    return JsonResponse({'success': True, 'user_id': str(target_user.id), 'display': display, 'initials': initials})


@login_required
@require_http_methods(['DELETE'])
def lead_follower_remove_api(request, lead_id, user_id):
    """
    DELETE /crm/leads/<lead_id>/followers/<user_id>/remove/
    """
    lead = get_object_or_404(Lead, id=lead_id)
    ct   = ContentType.objects.get_for_model(Lead)
    ChatterFollower.objects.filter(
        content_type=ct, object_id=lead.id, user_id=user_id,
    ).delete()
    return JsonResponse({'success': True})


# ============================================================
# WHATSAPP CHATTER VIEWS
# ============================================================

@login_required
@require_http_methods(['GET'])
def lead_whatsapp_list(request, lead_id):
    """
    GET /crm/leads/<lead_id>/whatsapp/
    Returns all WhatsApp messages for a Lead as JSON.
    """
    from apps.core.models import ChatterMessage
    from django.contrib.contenttypes.models import ContentType

    lead = get_object_or_404(Lead, id=lead_id)
    ct   = ContentType.objects.get_for_model(Lead)

    msgs = ChatterMessage.objects.filter(
        content_type=ct,
        object_id=lead.id,
        message_type='WHATSAPP',
    ).order_by('sent_at')

    data = []
    for m in msgs:
        data.append({
            'id':         str(m.id),
            'direction':  m.direction,
            'from_phone': m.from_email,
            'to_phone':   m.to_email,
            'body':       m.body,
            'wamid':      m.message_id or '',
            'sent_at':    m.sent_at.isoformat() if m.sent_at else None,
            'sent_by':    (m.author.get_full_name() or m.author.username) if m.author_id else '',
        })

    return JsonResponse({'success': True, 'messages': data})


@login_required
@require_POST
def lead_send_whatsapp(request, lead_id):
    """
    POST /crm/leads/<lead_id>/whatsapp/send/
    Body JSON:
    {
        "message": "text here",
        "to_phone": "+351912345678",       // optional override; defaults to lead.phone
        "reply_to_wamid": "wamid.xxx"      // optional
    }
    """
    from apps.core.models import ChatterMessage, CompanyWhatsAppConfig
    from apps.core.whatsapp_utils import send_whatsapp_message
    from django.contrib.contenttypes.models import ContentType
    import json as _json

    lead = get_object_or_404(Lead, id=lead_id)
    active_company = get_active_company(request)

    config = getattr(active_company, 'whatsapp_config', None)
    if not config or not config.has_whatsapp_configured:
        return JsonResponse({'success': False, 'error': 'WhatsApp n\u00e3o configurado para esta empresa'}, status=400)

    try:
        body_data   = _json.loads(request.body)
    except ValueError:
        return JsonResponse({'success': False, 'error': 'JSON inv\u00e1lido'}, status=400)

    message_text = body_data.get('message', '').strip()
    to_phone     = body_data.get('to_phone', '').strip() or (lead.phone or '').strip()
    reply_to     = body_data.get('reply_to_wamid', '') or None

    if not message_text:
        return JsonResponse({'success': False, 'error': 'Mensagem n\u00e3o pode estar vazia'}, status=400)
    if not to_phone:
        return JsonResponse({'success': False, 'error': 'Número de telefone não encontrado na oportunidade'}, status=400)

    result = send_whatsapp_message(config, to_phone, message_text, reply_to)

    if not result['success']:
        return JsonResponse({'success': False, 'error': result['error']}, status=500)

    # Persist as ChatterMessage
    ct = ContentType.objects.get_for_model(Lead)
    from django.utils import timezone as tz
    msg = ChatterMessage.objects.create(
        content_type=ct,
        object_id=lead.pk,
        message_type='WHATSAPP',
        direction='outbound',
        from_email='',
        to_email='',
        subject='',
        body=message_text,
        body_html='',
        message_id=result['wamid'],
        author=request.user,
        sent_at=tz.now(),
    )

    return JsonResponse({
        'success': True,
        'wamid': result['wamid'],
        'message': {
            'id':        str(msg.id),
            'direction': 'outbound',
            'body':      message_text,
            'to_phone':  to_phone,
            'sent_at':   msg.sent_at.isoformat() if msg.sent_at else None,
            'sent_by':   request.user.get_full_name() or request.user.username,
        },
    })


# =============================================
# CRM REPORTS VIEW
# =============================================

@login_required
def crm_reports_view(request):
    """
    Página de Relatórios CRM — 6 gráficos profissionais com Chart.js.
    Funil | Ganhas vs Perdidas | Responsável | Previsão | Fonte | Motivos de Perda
    """
    from dateutil.relativedelta import relativedelta
    import calendar as cal_module

    active_company = get_active_company(request)

    def base_qs():
        qs = Lead.objects.filter(is_prospect=False)
        if active_company:
            qs = qs.filter(owner_company=active_company)
        return qs

    now = timezone.now()

    # ── KPI Cards ──────────────────────────────────────────────
    total_in_pipeline = base_qs().filter(is_active=True, stage__is_won_stage=False, stage__is_lost_stage=False).count()
    total_won_month = base_qs().filter(
        stage__is_won_stage=True,
        closed_at__year=now.year, closed_at__month=now.month
    ).count()
    revenue_won_month = base_qs().filter(
        stage__is_won_stage=True,
        closed_at__year=now.year, closed_at__month=now.month
    ).aggregate(v=Sum('estimated_value'))['v'] or 0
    avg_probability = base_qs().filter(is_active=True, stage__is_won_stage=False, stage__is_lost_stage=False
    ).aggregate(v=Avg('probability'))['v'] or 0

    # ── 1. Funil de Conversão ───────────────────────────────────
    stages = CRMStage.objects.filter(is_active=True)
    if active_company:
        stages = stages.filter(Q(owner_company__isnull=True) | Q(owner_company=active_company))
    stages = stages.exclude(is_lost_stage=True).order_by('sequence')

    funnel_labels = []
    funnel_counts = []
    funnel_values = []
    for st in stages:
        agg = base_qs().filter(stage=st).aggregate(cnt=Count('id'), val=Sum('estimated_value'))
        funnel_labels.append(st.name)
        funnel_counts.append(agg['cnt'] or 0)
        funnel_values.append(float(agg['val'] or 0))

    # ── 2. Ganhas vs. Perdidas (últimos 12 meses) ───────────────
    monthly_labels = []
    monthly_won = []
    monthly_lost = []
    monthly_revenue = []
    for i in range(11, -1, -1):
        d = now - relativedelta(months=i)
        label = d.strftime('%b %Y')
        monthly_labels.append(label)
        won_cnt = base_qs().filter(
            stage__is_won_stage=True,
            closed_at__year=d.year, closed_at__month=d.month
        ).count()
        lost_cnt = base_qs().filter(
            stage__is_lost_stage=True,
            closed_at__year=d.year, closed_at__month=d.month
        ).count()
        won_rev = base_qs().filter(
            stage__is_won_stage=True,
            closed_at__year=d.year, closed_at__month=d.month
        ).aggregate(v=Sum('estimated_value'))['v'] or 0
        monthly_won.append(won_cnt)
        monthly_lost.append(lost_cnt)
        monthly_revenue.append(float(won_rev))

    # ── 3. Performance por Responsável (top 8) ──────────────────
    resp_data = (
        base_qs()
        .filter(assigned_to__isnull=False)
        .values('assigned_to__username', 'assigned_to__first_name', 'assigned_to__last_name')
        .annotate(
            total=Count('id'),
            won=Count('id', filter=Q(stage__is_won_stage=True)),
            lost=Count('id', filter=Q(stage__is_lost_stage=True)),
            revenue=Sum('estimated_value', filter=Q(stage__is_won_stage=True)),
        )
        .order_by('-won')[:8]
    )
    resp_labels = []
    resp_total = []
    resp_won = []
    resp_lost = []
    resp_revenue = []
    for r in resp_data:
        name = (f"{r['assigned_to__first_name']} {r['assigned_to__last_name']}".strip()
                or r['assigned_to__username'])
        resp_labels.append(name)
        resp_total.append(r['total'])
        resp_won.append(r['won'])
        resp_lost.append(r['lost'])
        resp_revenue.append(float(r['revenue'] or 0))

    # ── 4. Previsão de Receita (Forecast) — próximos 6 meses ───
    forecast_labels = []
    forecast_expected = []
    forecast_weighted = []
    for i in range(0, 6):
        d = now + relativedelta(months=i)
        label = d.strftime('%b %Y')
        forecast_labels.append(label)
        agg = base_qs().filter(
            is_active=True,
            stage__is_won_stage=False,
            stage__is_lost_stage=False,
            expected_close_date__year=d.year,
            expected_close_date__month=d.month,
        ).aggregate(
            expected=Sum('estimated_value'),
            cnt=Count('id'),
        )
        # weighted = estimated_value * probability / 100  (Python-side because it's a computed field)
        leads_month = base_qs().filter(
            is_active=True,
            stage__is_won_stage=False,
            stage__is_lost_stage=False,
            expected_close_date__year=d.year,
            expected_close_date__month=d.month,
        ).values_list('estimated_value', 'probability')
        weighted = sum(float(v) * p / 100 for v, p in leads_month if v)
        forecast_expected.append(float(agg['expected'] or 0))
        forecast_weighted.append(round(weighted, 2))

    # ── 5. Análise por Fonte ────────────────────────────────────
    SOURCE_LABELS = dict(Lead.SOURCE_CHOICES)
    source_data = (
        base_qs()
        .values('source')
        .annotate(cnt=Count('id'), revenue=Sum('estimated_value', filter=Q(stage__is_won_stage=True)))
        .order_by('-cnt')
    )
    source_labels = [SOURCE_LABELS.get(r['source'], r['source']) for r in source_data]
    source_counts = [r['cnt'] for r in source_data]
    source_revenue = [float(r['revenue'] or 0) for r in source_data]

    # ── 6. Motivos de Perda ─────────────────────────────────────
    LOST_CAT_LABELS = dict(Lead.LOST_REASON_CATEGORY_CHOICES)
    lost_cat_data = (
        base_qs()
        .filter(stage__is_lost_stage=True)
        .exclude(lost_reason_category='')
        .values('lost_reason_category')
        .annotate(cnt=Count('id'))
        .order_by('-cnt')
    )
    # Also count uncategorised
    uncategorised = base_qs().filter(stage__is_lost_stage=True, lost_reason_category='').count()
    lost_cat_labels = [LOST_CAT_LABELS.get(r['lost_reason_category'], r['lost_reason_category'])
                       for r in lost_cat_data]
    lost_cat_counts = [r['cnt'] for r in lost_cat_data]
    if uncategorised:
        lost_cat_labels.append('Sem categoria')
        lost_cat_counts.append(uncategorised)

    context = {
        'crm_config': _get_crm_config(request),
        # KPIs
        'kpi_pipeline': total_in_pipeline,
        'kpi_won_month': total_won_month,
        'kpi_revenue_month': revenue_won_month,
        'kpi_avg_prob': round(avg_probability, 1),
        # Chart data (JSON)
        'funnel_labels_json': json.dumps(funnel_labels),
        'funnel_counts_json': json.dumps(funnel_counts),
        'funnel_values_json': json.dumps(funnel_values),
        'monthly_labels_json': json.dumps(monthly_labels),
        'monthly_won_json': json.dumps(monthly_won),
        'monthly_lost_json': json.dumps(monthly_lost),
        'monthly_revenue_json': json.dumps(monthly_revenue),
        'resp_labels_json': json.dumps(resp_labels),
        'resp_total_json': json.dumps(resp_total),
        'resp_won_json': json.dumps(resp_won),
        'resp_lost_json': json.dumps(resp_lost),
        'resp_revenue_json': json.dumps(resp_revenue),
        'forecast_labels_json': json.dumps(forecast_labels),
        'forecast_expected_json': json.dumps(forecast_expected),
        'forecast_weighted_json': json.dumps(forecast_weighted),
        'source_labels_json': json.dumps(source_labels),
        'source_counts_json': json.dumps(source_counts),
        'source_revenue_json': json.dumps(source_revenue),
        'lost_cat_labels_json': json.dumps(lost_cat_labels),
        'lost_cat_counts_json': json.dumps(lost_cat_counts),
    }

    return render(request, 'crm/reports.html', context)
