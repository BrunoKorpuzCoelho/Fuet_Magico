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
from django.contrib.contenttypes.models import ContentType
from apps.accounts.decorators import admin_required
from apps.core.multi_company import filter_by_company, get_active_company
from apps.core.models import ActivityType, ScheduledActivity
from apps.core.forms import ScheduledActivityForm
from apps.contacts.models import Contact
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
            
            messages.success(request, f'Oportunidade "{lead.title}" criada com sucesso!')
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
        'page_title': 'Nova Oportunidade',
        'stages': stages,
        'won_stage': won_stage,
        'lost_stage': lost_stage,
        'new_stage': new_stage,
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
    
    # Get leads based on stage filter
    if stage_filter == 'won':
        # Only Won stages
        leads = Lead.objects.filter(
            is_active=True,
            stage__is_won_stage=True
        ).select_related(
            'contact', 
            'assigned_to', 
            'stage',
            'owner_company'
        ).prefetch_related('tags')
    elif stage_filter == 'lost':
        # Only Lost stages
        leads = Lead.objects.filter(
            is_active=True,
            stage__is_lost_stage=True
        ).select_related(
            'contact', 
            'assigned_to', 
            'stage',
            'owner_company'
        ).prefetch_related('tags')
    elif stage_filter == 'all':
        # All stages (including Won and Lost)
        leads = Lead.objects.filter(
            is_active=True
        ).select_related(
            'contact', 
            'assigned_to', 
            'stage',
            'owner_company'
        ).prefetch_related('tags')
    else:
        # Default: Active (EXCLUDE Won and Lost stages)
        leads = Lead.objects.filter(
            is_active=True
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
        'filtered_contact': filtered_contact,  # Para exibir "Leads de [Nome do Contacto]"
    }
    
    return render(request, 'crm/lead_list.html', context)


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
        
        # Update leads to Won stage
        updated_count = leads.update(stage=won_stage)
        
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
        updated_count = leads.update(stage=lost_stage)
        
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
