from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from apps.accounts.decorators import admin_required
from apps.core.multi_company import filter_by_company, get_active_company
from .models import CRMStage
from .forms import CRMStageForm
import json
import random


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
        fold_by_default = data.get('fold_by_default', False)
        
        # Validar que só pode haver um estágio de vitória
        company = request.session.get('active_company_id')
        if is_won_stage:
            existing_won = CRMStage.objects.filter(
                is_won_stage=True,
                is_active=True
            )
            # Filter by company
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
        
        # Obter owner_company
        owner_company = get_active_company(request)
        
        # Criar o estágio
        stage = CRMStage.objects.create(
            name=name,
            sequence=sequence,
            color=color,
            routing_in_days=routing_in_days,
            is_won_stage=is_won_stage,
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
    
    IMPORTANTE: Estágios com is_won_stage=True não podem ser duplicados.
    Só pode existir um estágio de vitória por empresa.
    """
    try:
        data = json.loads(request.body)
        stage_ids = data.get('stage_ids', [])
        
        if not stage_ids:
            return JsonResponse({
                'success': False,
                'error': 'Nenhum estágio selecionado'
            }, status=400)
        
        # Verificar se algum dos estágios selecionados é um estágio de vitória
        won_stages = CRMStage.objects.filter(
            id__in=stage_ids,
            is_won_stage=True,
            is_active=True
        )
        
        if won_stages.exists():
            return JsonResponse({
                'success': False,
                'error': 'Não é possível duplicar estágios de vitória. Só pode existir um estágio com "Vitória" ativo por empresa.'
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