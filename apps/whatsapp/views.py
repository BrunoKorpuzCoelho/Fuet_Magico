import json as _json
from datetime import date as _date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import WhatsAppTemplate
from .forms import WhatsAppTemplateForm
from .api import submit_template_to_meta
from apps.core.multi_company import filter_by_company
from apps.core.models import ChatterFollower


@login_required
def template_list_view(request):
    search_query = request.GET.get('search', '')
    search_field = request.GET.get('field', 'display_name')
    page_number = request.GET.get('page', 1)
    page_size = 50
    status_filter = request.GET.get('status', 'active')   # active / archived
    wa_status_filter = request.GET.get('wa_status', '')    # DRAFT / PENDING / APPROVED / REJECTED / PAUSED / DISABLED
    category_filter = request.GET.get('category', '')

    qs = WhatsAppTemplate.objects.select_related('owner_company', 'created_by')

    # Filter by active company
    qs = filter_by_company(qs, request)

    # Filter active / archived
    if status_filter == 'archived':
        qs = qs.filter(is_active=False)
    else:
        qs = qs.filter(is_active=True)

    # Filter by wa_status (DRAFT, PENDING, APPROVED…)
    if wa_status_filter:
        qs = qs.filter(status=wa_status_filter)

    # Category filter
    if category_filter:
        qs = qs.filter(category=category_filter)

    # Search
    if search_query:
        field_map = {
            'display_name': Q(display_name__icontains=search_query),
            'name': Q(name__icontains=search_query),
            'body': Q(body__icontains=search_query),
            'category': Q(category__icontains=search_query),
            'language': Q(language__icontains=search_query),
            'footer': Q(footer__icontains=search_query),
        }
        if search_field in field_map:
            qs = qs.filter(field_map[search_field])
        else:
            qs = qs.filter(
                Q(display_name__icontains=search_query) |
                Q(name__icontains=search_query) |
                Q(body__icontains=search_query)
            )

    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page_number)

    context = {
        'templates': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'search_field': search_field,
        'status_filter': status_filter,
        'wa_status_filter': wa_status_filter,
        'category_filter': category_filter,
        'total_count': paginator.count,
        'page_size': page_size,
        'wa_status_choices': WhatsAppTemplate.STATUS_CHOICES,
        'category_choices': WhatsAppTemplate.CATEGORY_CHOICES,
    }
    return render(request, 'whatsapp/template_list.html', context)


@login_required
def template_create_view(request):
    if request.method == 'POST':
        form = WhatsAppTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by = request.user
            template._current_user = request.user
            template.save()
            messages.success(request, f'Template "{template.display_name}" criado com sucesso.')
            return redirect('whatsapp:template_edit', pk=template.pk)
    else:
        form = WhatsAppTemplateForm()

    return render(request, 'whatsapp/template_form.html', {'form': form, 'is_edit': False})


@login_required
def template_edit_view(request, pk):
    from apps.core.models import AuditLog
    template = get_object_or_404(WhatsAppTemplate, pk=pk)

    LOCKED_STATUSES = (WhatsAppTemplate.STATUS_PENDING, WhatsAppTemplate.STATUS_APPROVED)
    form_readonly = template.status in LOCKED_STATUSES

    if request.method == 'POST':
        if form_readonly:
            messages.warning(request, 'Não é possível editar um template em estado Pendente ou Aprovado.')
            return redirect('whatsapp:template_edit', pk=pk)
        form = WhatsAppTemplateForm(request.POST, instance=template)
        if form.is_valid():
            template._current_user = request.user
            form.save()
            messages.success(request, f'Template "{template.display_name}" atualizado.')
            # Notificar seguidores da atualização
            try:
                from apps.core.models import notify_followers
                from django.urls import reverse
                notify_followers(
                    template,
                    'MENTION',
                    f'Template "{template.display_name}" foi atualizado por {request.user.get_full_name() or request.user.username}',
                    exclude_user=request.user,
                )
            except Exception:
                pass
            return redirect('whatsapp:template_edit', pk=pk)
    else:
        form = WhatsAppTemplateForm(instance=template)

    audit_logs = AuditLog.objects.filter(
        model_name='WhatsAppTemplate',
        object_id=str(template.id)
    ).select_related('user').order_by('-timestamp')[:50]

    # Activities context
    from apps.core.models import GenericActivity, ScheduledActivity
    import json as _j
    ct = ContentType.objects.get_for_model(WhatsAppTemplate)
    activities_qs = (
        GenericActivity.objects
        .filter(content_type=ct, object_id=str(template.id))
        .select_related('assigned_to', 'scheduled_activity', 'scheduled_activity__activity_type')
        .order_by('is_done', 'due_date')
    )
    today = _date.today()
    def _activity_dict(a):
        return {
            'id': str(a.id),
            'activity_type': a.activity_type,
            'activity_type_display': a.get_activity_type_display(),
            'scheduled_activity_id': str(a.scheduled_activity.id) if a.scheduled_activity else '',
            'icon_svg': a.scheduled_activity.icon_svg if a.scheduled_activity else '',
            'icon_color': a.scheduled_activity.icon_color if a.scheduled_activity else '#6366F1',
            'summary': a.summary,
            'due_date': a.due_date.strftime('%Y-%m-%d'),
            'due_date_display': a.due_date.strftime('%d/%m/%Y'),
            'assigned_to': (a.assigned_to.get_full_name() or a.assigned_to.username) if a.assigned_to else None,
            'assigned_to_id': str(a.assigned_to.id) if a.assigned_to else '',
            'is_done': a.is_done,
            'is_overdue': a.is_overdue,
            'is_today': a.is_today,
            'feedback': a.feedback or '',
        }
    template_activities_json = _j.dumps([_activity_dict(a) for a in activities_qs])

    from apps.core.multi_company import get_active_company
    sa_qs = ScheduledActivity.objects.filter(
        is_active=True
    ).filter(
        Q(applicable_models=[]) | Q(applicable_models__contains=['WHATSAPP'])
    ).select_related('activity_type').order_by('activity_type__name', 'name', 'summary')
    scheduled_activities_json = _j.dumps([
        {
            'id': str(sa.id),
            'name': sa.name or sa.summary,
            'summary': sa.summary,
            'type_code': sa.activity_type.code if sa.activity_type else '',
            'icon_svg': sa.icon_svg or '',
            'icon_color': sa.icon_color or '#6366F1',
        }
        for sa in sa_qs
    ])

    from apps.core.models import GenericActivity as _GA
    current_user_id = str(request.user.id)
    User = get_user_model()
    users_for_activity = User.objects.filter(is_active=True).order_by('first_name', 'last_name')

    return render(request, 'whatsapp/template_form.html', {
        'form': form,
        'is_edit': True,
        'template': template,
        'audit_logs': audit_logs,
        'form_readonly': form_readonly,
        'template_activities_json': template_activities_json,
        'scheduled_activities_json': scheduled_activities_json,
        'activity_type_choices': _GA.ACTIVITY_TYPE_CHOICES,
        'current_user_id': current_user_id,
        'users_for_activity': users_for_activity,
    })


@login_required
@require_http_methods(['POST'])
def template_submit_view(request, pk):
    """Submit a WhatsApp template to Meta for approval via the Graph API."""
    template = get_object_or_404(WhatsAppTemplate, pk=pk)

    # Guard: only submit DRAFT or REJECTED templates
    if template.status in (WhatsAppTemplate.STATUS_PENDING, WhatsAppTemplate.STATUS_APPROVED):
        return JsonResponse({
            'ok': False,
            'message': f'Template já está em estado "{template.get_status_display()}" — não é possível submeter novamente.'
        }, status=400)

    # Ensure owner_company is set — assign from active session if missing
    if template.owner_company is None:
        from apps.core.multi_company import get_active_company
        active_company = get_active_company(request)
        if active_company:
            template.owner_company = active_company
            template.save(update_fields=['owner_company'])

    success, data = submit_template_to_meta(template)

    if success:
        template.wa_template_uid = data.get('id', '')
        template.status = WhatsAppTemplate.STATUS_PENDING
        template._current_user = request.user
        template.save(update_fields=['wa_template_uid', 'status'])
        return JsonResponse({
            'ok': True,
            'message': f'Template submetido com sucesso. A Meta está a rever o template — estado atualizado para Pendente.',
            'wa_template_uid': template.wa_template_uid,
        })
    else:
        return JsonResponse({
            'ok': False,
            'message': data.get('error', 'Erro desconhecido da Meta API.'),
        }, status=400)


@login_required
@require_http_methods(['POST'])
def template_archive_view(request, pk):
    template = get_object_or_404(WhatsAppTemplate, pk=pk)
    template.is_active = False
    template._current_user = request.user
    template.save(update_fields=['is_active', 'updated_at'])
    return JsonResponse({'success': True})


@login_required
@require_http_methods(['POST'])
def template_unarchive_view(request, pk):
    template = get_object_or_404(WhatsAppTemplate, pk=pk)
    template.is_active = True
    template._current_user = request.user
    template.save(update_fields=['is_active', 'updated_at'])
    return JsonResponse({'success': True})


@login_required
@require_http_methods(['POST'])
def template_delete_view(request, pk):
    template = get_object_or_404(WhatsAppTemplate, pk=pk)
    from .api import delete_template_from_meta
    ok, err = delete_template_from_meta(template)
    if not ok:
        return JsonResponse({'success': False, 'error': f'Erro ao eliminar na Meta: {err}'})
    template.delete()
    return JsonResponse({'success': True})


@login_required
@require_http_methods(['POST'])
def bulk_action_view(request):
    import json
    data = json.loads(request.body)
    action = data.get('action')
    ids = data.get('ids', [])

    qs = WhatsAppTemplate.objects.filter(pk__in=ids)

    n = len(ids)
    if action == 'archive':
        qs.update(is_active=False)
        msg = f'{n} template(s) arquivado(s) com sucesso.'
    elif action == 'unarchive':
        qs.update(is_active=True)
        msg = f'{n} template(s) desarquivado(s) com sucesso.'
    elif action == 'delete':
        from .api import delete_template_from_meta
        errors = []
        deleted = 0
        for tmpl in qs:
            ok, err = delete_template_from_meta(tmpl)
            if ok:
                tmpl.delete()
                deleted += 1
            else:
                errors.append(f'"{tmpl.name}": {err}')
        if errors:
            return JsonResponse({
                'success': False,
                'count': deleted,
                'message': f'{deleted} eliminado(s). Erros Meta: {" | ".join(errors)}',
            })
        msg = f'{deleted} template(s) eliminado(s) permanentemente.'
    else:
        return JsonResponse({'success': False, 'error': 'Ação inválida'}, status=400)

    return JsonResponse({'success': True, 'count': n, 'message': msg})


# ============================================================
# Template Notes (Chatter)
# ============================================================

@login_required
@require_http_methods(['GET'])
def template_notes_list(request, template_id):
    """GET /whatsapp/<id>/notas/  →  lista notas internas do template."""
    from apps.core.models import ChatterMessage
    from django.contrib.contenttypes.models import ContentType as CT
    template = get_object_or_404(WhatsAppTemplate, id=template_id)
    ct = CT.objects.get_for_model(WhatsAppTemplate)
    notes = (
        ChatterMessage.objects
        .filter(content_type=ct, object_id=template.id, message_type='NOTE')
        .select_related('author')
        .order_by('-created_at')[:100]
    )
    def author_display(n):
        if n.author:
            return n.author.get_full_name() or n.author.username
        return 'Sistema'
    def author_initials(n):
        d = author_display(n)
        return ''.join(p[0].upper() for p in d.split()[:2])
    return JsonResponse({
        'notes': [
            {
                'id': str(n.id),
                'author': author_display(n),
                'author_initials': author_initials(n),
                'content': n.body,
                'created_at': n.created_at.strftime('%d/%m/%Y %H:%M'),
            }
            for n in notes
        ]
    })


@login_required
@require_http_methods(['POST'])
def template_note_create(request, template_id):
    """POST /whatsapp/<id>/notas/criar/  →  cria nota + notif @menções + notify_followers."""
    import re
    from apps.core.models import ChatterMessage, notify_followers
    from apps.core.models import Notification as _N
    from django.contrib.contenttypes.models import ContentType as CT
    from django.contrib.auth import get_user_model as _get_user_model
    User = _get_user_model()
    template = get_object_or_404(WhatsAppTemplate, id=template_id)
    try:
        data = _json.loads(request.body or '{}')
    except _json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
    content = data.get('content', '').strip()
    urgent  = bool(data.get('urgent', False))
    if not content:
        return JsonResponse({'success': False, 'error': 'Conteúdo obrigatório.'}, status=400)
    ct = CT.objects.get_for_model(WhatsAppTemplate)
    note = ChatterMessage.objects.create(
        content_type=ct,
        object_id=template.id,
        author=request.user,
        message_type='NOTE',
        is_internal=True,
        body=content,
    )
    # @menções → notificação MENTION
    author_display = request.user.get_full_name() or request.user.username
    for username in set(re.findall(r'@(\w+)', content)):
        try:
            mu = User.objects.get(username=username, is_active=True)
            _N.objects.create(
                user=mu,
                notification_type='MENTION',
                title=f'{author_display} mencionou-te numa nota',
                message=f'Template: {template.display_name}',
                link=f'/whatsapp/{str(template.id)}/edit/',
                related_object_id=note.id,
                is_urgent=urgent,
            )
        except Exception:
            pass
    # Notificar seguidores
    try:
        notify_followers(
            template, 'MENTION',
            f'Nova nota em template "{template.display_name}" por {author_display}',
            message=content[:200],
            exclude_user=request.user,
        )
    except Exception:
        pass
    def _d(n):
        if n.author:
            return n.author.get_full_name() or n.author.username
        return 'Sistema'
    return JsonResponse({
        'success': True,
        'note': {
            'id': str(note.id),
            'author': _d(note),
            'author_initials': ''.join(p[0].upper() for p in _d(note).split()[:2]),
            'content': note.body,
            'created_at': note.created_at.strftime('%d/%m/%Y %H:%M'),
        }
    }, status=201)


# ============================================================
# Template Followers (Chatter)
# ============================================================

@login_required
@require_http_methods(['GET', 'POST'])
def template_followers_api(request, template_id):
    """
    GET  /whatsapp/<id>/seguidores/   → lista seguidores
    POST /whatsapp/<id>/seguidores/   → adiciona seguidor  { user_id }
    """
    User = get_user_model()
    template = get_object_or_404(WhatsAppTemplate, id=template_id)
    ct = ContentType.objects.get_for_model(WhatsAppTemplate)

    if request.method == 'GET':
        # Auto-follow: utilizador actual
        ChatterFollower.objects.get_or_create(
            content_type=ct,
            object_id=template.id,
            user=request.user,
            defaults={'added_by': None},
        )
        followers = (
            ChatterFollower.objects
            .filter(content_type=ct, object_id=template.id)
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

    # POST — adicionar seguidor
    try:
        data = _json.loads(request.body or '{}')
    except _json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    user_id = data.get('user_id', '').strip()
    if not user_id:
        return JsonResponse({'success': False, 'error': 'user_id obrigatório'}, status=400)

    User = get_user_model()
    try:
        target_user = User.objects.get(id=user_id, is_active=True)
    except Exception:
        return JsonResponse({'success': False, 'error': 'Utilizador não encontrado'}, status=404)

    ChatterFollower.objects.get_or_create(
        content_type=ct,
        object_id=template.id,
        user=target_user,
        defaults={'added_by': request.user},
    )
    display  = target_user.get_full_name() or target_user.username
    initials = ''.join(p[0].upper() for p in display.split()[:2])
    return JsonResponse({'success': True, 'user_id': str(target_user.id), 'display': display, 'initials': initials})


@login_required
@require_http_methods(['DELETE'])
def template_follower_remove_api(request, template_id, user_id):
    """
    DELETE /whatsapp/<template_id>/seguidores/<user_id>/remover/
    """
    template = get_object_or_404(WhatsAppTemplate, id=template_id)
    ct = ContentType.objects.get_for_model(WhatsAppTemplate)
    ChatterFollower.objects.filter(
        content_type=ct, object_id=template.id, user_id=user_id,
    ).delete()
    return JsonResponse({'success': True})


# ============================================================
# Template Activities (GenericActivity)
# ============================================================

@login_required
@require_http_methods(['POST'])
def template_activity_create(request, template_id):
    """POST /whatsapp/<id>/atividades/criar/"""
    from apps.core.models import GenericActivity, ScheduledActivity
    from apps.core.multi_company import get_active_company
    template = get_object_or_404(WhatsAppTemplate, id=template_id)
    try:
        data = _json.loads(request.body or '{}')
    except _json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)

    activity_type       = data.get('activity_type', '').strip()
    summary             = data.get('summary', '').strip()
    due_date_str        = data.get('due_date', '').strip()
    assigned_to_id      = data.get('assigned_to_id', '').strip()
    scheduled_activity_id = data.get('scheduled_activity_id', '').strip()

    sa_obj = None
    if scheduled_activity_id:
        try:
            sa_obj = ScheduledActivity.objects.select_related('activity_type').get(id=scheduled_activity_id)
            if not activity_type and sa_obj.activity_type:
                activity_type = sa_obj.activity_type.code
        except ScheduledActivity.DoesNotExist:
            pass

    errors = {}
    valid_types = dict(GenericActivity.ACTIVITY_TYPE_CHOICES)
    if not activity_type:
        errors['activity_type'] = 'Tipo de atividade é obrigatório.'
    elif activity_type not in valid_types:
        errors['activity_type'] = 'Tipo inválido.'
    if not summary:
        errors['summary'] = 'Resumo é obrigatório.'
    if not due_date_str:
        errors['due_date'] = 'Data limite é obrigatória.'
    else:
        try:
            from datetime import datetime
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            errors['due_date'] = 'Formato de data inválido (use YYYY-MM-DD).'
    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    User = get_user_model()
    assigned_to = request.user
    if assigned_to_id:
        try:
            assigned_to = User.objects.get(id=assigned_to_id, is_active=True)
        except User.DoesNotExist:
            pass

    ct = ContentType.objects.get_for_model(WhatsAppTemplate)
    activity = GenericActivity.objects.create(
        content_type=ct,
        object_id=str(template.id),
        scheduled_activity=sa_obj,
        activity_type=activity_type,
        summary=summary,
        due_date=due_date,
        assigned_to=assigned_to,
        owner_company=get_active_company(request),
    )

    # ── Criar notificação para o utilizador atribuído ─────────────────────
    try:
        from apps.core.models import Notification as _Notification
        _today_n = _date.today()
        if activity.due_date < _today_n:
            _notif_type = 'ACTIVITY_OVERDUE'
        elif activity.due_date == _today_n:
            _notif_type = 'ACTIVITY_TODAY'
        else:
            _notif_type = 'ACTIVITY_UPCOMING'
        _Notification.objects.create(
            user=activity.assigned_to,
            notification_type=_notif_type,
            title=activity.summary,
            message=f'Template: {template.display_name}',
            link=f'/whatsapp/{str(template.id)}/edit/',
            related_object_id=activity.id,
        )
    except Exception as _e:
        import logging as _nlog
        _nlog.getLogger('apps.whatsapp.notifications').error(
            'Notification creation failed for activity %s: %s', activity.id, _e
        )

    today = _date.today()
    return JsonResponse({
        'success': True,
        'activity': {
            'id': str(activity.id),
            'activity_type': activity.activity_type,
            'activity_type_display': activity.get_activity_type_display(),
            'scheduled_activity_id': str(sa_obj.id) if sa_obj else '',
            'icon_svg': sa_obj.icon_svg if sa_obj else '',
            'icon_color': sa_obj.icon_color if sa_obj else '#6366F1',
            'summary': activity.summary,
            'due_date': activity.due_date.strftime('%Y-%m-%d'),
            'due_date_display': activity.due_date.strftime('%d/%m/%Y'),
            'assigned_to': (assigned_to.get_full_name() or assigned_to.username) if assigned_to else None,
            'assigned_to_id': str(assigned_to.id) if assigned_to else '',
            'is_done': False,
            'is_overdue': activity.is_overdue,
            'is_today': activity.is_today,
            'feedback': '',
        }
    }, status=201)


@login_required
@require_http_methods(['POST'])
def template_activity_done(request, template_id, activity_id):
    """POST /whatsapp/<template_id>/atividades/<activity_id>/concluir/"""
    from apps.core.models import GenericActivity
    from django.utils import timezone
    template = get_object_or_404(WhatsAppTemplate, id=template_id)
    ct = ContentType.objects.get_for_model(WhatsAppTemplate)
    activity = get_object_or_404(GenericActivity, id=activity_id, content_type=ct, object_id=str(template.id))
    try:
        data = _json.loads(request.body or '{}')
    except _json.JSONDecodeError:
        data = {}
    feedback = data.get('feedback', '').strip()
    activity.is_done = True
    activity.done_date = timezone.now()
    activity.feedback = feedback
    activity.save(update_fields=['is_done', 'done_date', 'feedback'])
    # Remover notificação pendente desta atividade
    try:
        from apps.core.models import Notification as _Notification
        _Notification.objects.filter(related_object_id=activity.id).delete()
    except Exception:
        pass
    return JsonResponse({'success': True})


@login_required
@require_http_methods(['DELETE'])
def template_activity_delete(request, template_id, activity_id):
    """DELETE /whatsapp/<template_id>/atividades/<activity_id>/eliminar/"""
    from apps.core.models import GenericActivity
    template = get_object_or_404(WhatsAppTemplate, id=template_id)
    ct = ContentType.objects.get_for_model(WhatsAppTemplate)
    activity_qs = GenericActivity.objects.filter(id=activity_id, content_type=ct, object_id=str(template.id))
    # Remover notificação antes de apagar
    try:
        from apps.core.models import Notification as _Notification
        _Notification.objects.filter(related_object_id=activity_id).delete()
    except Exception:
        pass
    activity_qs.delete()
    return JsonResponse({'success': True})
