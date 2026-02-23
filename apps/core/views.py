from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.db import models
from django.utils import timezone
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from apps.accounts.decorators import role_required
from .models import AuditLog, ErrorLog, Notification, CompanyWhatsAppConfig
from .whatsapp_utils import parse_webhook_payload, phones_match
from datetime import datetime

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
@role_required('ADMIN')
def application_logs_view(request):
    return render(request, 'devtools/application_logs.html')


@require_http_methods(["GET"])
@role_required('ADMIN')
def error_logs_view(request):
    return render(request, 'devtools/error_logs.html')


@require_http_methods(["GET"])
@role_required('ADMIN')
def audit_logs_view(request):
    return render(request, 'devtools/audit_logs.html')


@require_http_methods(["GET"])
@role_required('ADMIN')
def audit_logs_api(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 300))
    
    user_filter = request.GET.get('user')
    action_filter = request.GET.get('action')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    queryset = AuditLog.objects.all()
    
    if user_filter:
        queryset = queryset.filter(user__username__icontains=user_filter)
    if action_filter:
        queryset = queryset.filter(action=action_filter)
    if date_from:
        queryset = queryset.filter(timestamp__gte=datetime.fromisoformat(date_from))
    if date_to:
        queryset = queryset.filter(timestamp__lte=datetime.fromisoformat(date_to))
    
    paginator = Paginator(queryset, limit)
    page_obj = paginator.get_page(page)
    
    logs = [{
        'id': str(log.id),
        'timestamp': log.timestamp.isoformat(),
        'user': log.user.username if log.user else None,
        'action': log.action,
        'model_name': log.model_name,
        'object_id': log.object_id,
        'details': log.details
    } for log in page_obj]
    
    return JsonResponse({
        'logs': logs,
        'page': page,
        'total_pages': paginator.num_pages,
        'total_count': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous()
    })


@require_http_methods(["GET"])
@role_required('ADMIN')
def error_logs_api(request):
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 300))
    
    level_filter = request.GET.get('level')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    queryset = ErrorLog.objects.all()
    
    if level_filter:
        queryset = queryset.filter(level=level_filter)
    if date_from:
        queryset = queryset.filter(timestamp__gte=datetime.fromisoformat(date_from))
    if date_to:
        queryset = queryset.filter(timestamp__lte=datetime.fromisoformat(date_to))
    
    paginator = Paginator(queryset, limit)
    page_obj = paginator.get_page(page)
    
    logs = [{
        'id': log.id,
        'timestamp': log.timestamp.isoformat(),
        'level': log.level,
        'message': log.message,
        'traceback': log.traceback,
        'request_path': log.request_path,
        'user': log.user.username if log.user else None
    } for log in page_obj]
    
    return JsonResponse({
        'logs': logs,
        'page': page,
        'total_pages': paginator.num_pages,
        'total_count': paginator.count,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous()
    })


@require_http_methods(["GET"])
@role_required('ADMIN')
def application_logs_api(request):
    import os
    from datetime import datetime as dt
    from django.conf import settings
    
    limit = int(request.GET.get('limit', 100))
    
    logs = []
    log_file = settings.BASE_DIR / 'logs' / 'django.log'
    
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                recent_lines = lines[-limit:] if len(lines) > limit else lines
                
                for line in recent_lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    timestamp = dt.now().strftime('%H:%M:%S.%f')[:-3]
                    level = 'INFO'
                    
                    if 'ERROR' in line or '500' in line or '404' in line:
                        level = 'ERROR'
                    elif 'WARNING' in line or 'WARN' in line:
                        level = 'WARNING'
                    elif '"POST' in line:
                        level = 'INFO'
                    elif '"GET' in line:
                        level = 'DEBUG'
                    
                    if '[' in line and ']' in line:
                        timestamp_match = line.split(']')[0].replace('[', '')
                        if '/' in timestamp_match:
                            timestamp = timestamp_match.split()[-1] if ' ' in timestamp_match else timestamp
                    
                    logs.append({
                        'timestamp': timestamp,
                        'level': level,
                        'message': line
                    })
        except Exception as e:
            logs.append({
                'timestamp': dt.now().strftime('%H:%M:%S.%f')[:-3],
                'level': 'ERROR',
                'message': f'Error reading log file: {str(e)}'
            })
    else:
        recent_errors = ErrorLog.objects.all()[:50]
        for err in recent_errors:
            timestamp = err.timestamp.strftime('%H:%M:%S.%f')[:-3]
            logs.append({
                'timestamp': timestamp,
                'level': err.level,
                'message': err.message
            })
    
    return JsonResponse({'logs': logs})


# ══════════════════════════════════════════════════════════════════════════════
# CHATTER SYSTEM - MIXINS AND APIs
# ══════════════════════════════════════════════════════════════════════════════

from django.views.generic import DetailView
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import ChatterMessage, ChatterActivity, PlannedActivity, ActivityType
import json


class ChatterMixin:
    """
    Mixin for adding chatter data to any DetailView.
    
    Usage:
        class LeadDetailView(ChatterMixin, DetailView):
            model = Lead
            template_name = 'crm/lead_detail.html'
    
    The mixin automatically adds to context:
        - whatsapp_messages: WhatsApp messages (placeholder for Phase 12)
        - chatter_messages: Emails + internal notes (ChatterMessage)
        - activities: Activity timeline (ChatterActivity audit log)
    
    Template usage:
        {% load chatter_tags %}
        {% include 'components/chatter.html' with object=lead %}
    """
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        content_type = ContentType.objects.get_for_model(obj)
        
        # WhatsApp messages (PLACEHOLDER - Phase 12)
        # TODO: Implement in Phase 12 (WhatsApp API integration)
        # from apps.marketing.models import WhatsAppMessage
        # context['whatsapp_messages'] = WhatsAppMessage.objects.filter(
        #     content_type=content_type,
        #     object_id=obj.id
        # ).order_by('sent_at')
        context['whatsapp_messages'] = []
        
        # Chatter messages (emails + notes)
        context['chatter_messages'] = ChatterMessage.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).select_related('author').order_by('-created_at')
        
        # Activities (audit log)
        context['activities'] = ChatterActivity.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).select_related('user').order_by('-created_at')[:100]  # Last 100

        # Planned activities (agendamentos estilo Odoo)
        context['planned_activities'] = PlannedActivity.objects.filter(
            content_type=content_type,
            object_id=obj.id
        ).select_related('activity_type', 'assigned_to', 'created_by').order_by('due_date')

        # Tipos de atividade disponíveis (para os tabs do formulário)
        context['activity_types'] = ActivityType.objects.all().order_by('name')

        return context


@login_required
@require_POST
def chatter_create_message(request):
    """
    API endpoint to create email or internal note.
    
    POST /api/chatter/message/
    Body JSON:
    {
        "object_type": "crm.lead",
        "object_id": "uuid-here",
        "message_type": "EMAIL" or "NOTE",
        "subject": "Subject (only for EMAIL)",
        "body": "Message content"
    }
    
    Returns:
        JSON: {"success": True/False, "message": "...", "id": "uuid"}
    
    Notes:
        - Creates ChatterMessage in database
        - If EMAIL: sends via SMTP (Task 3.9 - not implemented yet)
        - Creates ChatterActivity for audit log
    """
    try:
        data = json.loads(request.body)
        
        # Parse object type (e.g., "crm.lead" → app_label="crm", model="lead")
        object_type = data.get('object_type')
        object_id = data.get('object_id')
        message_type = data.get('message_type', 'NOTE')
        subject = data.get('subject', '')
        body = data.get('body', '')
        
        if not object_type or not object_id or not body:
            return JsonResponse({
                'success': False,
                'error': 'Missing required fields: object_type, object_id, body'
            }, status=400)
        
        # Parse ContentType
        try:
            app_label, model = object_type.split('.')
            content_type = ContentType.objects.get(app_label=app_label, model=model)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Invalid object_type: {object_type}'
            }, status=400)
        
        # Create ChatterMessage
        chatter_message = ChatterMessage.objects.create(
            content_type=content_type,
            object_id=object_id,
            author=request.user,
            message_type=message_type,
            subject=subject,
            body=body,
            is_internal=(message_type == 'NOTE')
        )
        
        # Create ChatterActivity (audit log)
        activity_type = 'EMAIL_SENT' if message_type == 'EMAIL' else 'COMMENT'
        description = f"sent an email" if message_type == 'EMAIL' else f"added an internal note"
        
        ChatterActivity.objects.create(
            content_type=content_type,
            object_id=object_id,
            user=request.user,
            activity_type=activity_type,
            description=description,
            details={
                'message_id': str(chatter_message.id),
                'message_type': message_type
            }
        )
        
        # TODO: If EMAIL, send via Celery (Task 3.9)
        # if message_type == 'EMAIL':
        #     from config.tasks import send_email_task
        #     send_email_task.delay(str(chatter_message.id))

        # Notificar seguidores (excluir o próprio autor)
        try:
            from apps.core.models import notify_followers
            obj = content_type.get_object_for_this_type(pk=object_id)
            notif_type = 'EMAIL' if message_type == 'EMAIL' else 'MENTION'
            if message_type == 'EMAIL':
                notif_title = f'Novo email em {content_type.name}: {subject or body[:60]}'
            else:
                notif_title = f'Nova nota em {obj} por {request.user.get_full_name() or request.user.username}'
            notify_followers(
                obj,
                notif_type,
                notif_title,
                message=body[:200],
                exclude_user=request.user,
            )
        except Exception:
            pass  # não falhar o pedido por causa das notificações

        return JsonResponse({
            'success': True,
            'message': 'Message created successfully',
            'id': str(chatter_message.id)
        })
    
    except Exception as e:
        print(f"[CHATTER API] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_POST
def chatter_send_whatsapp(request):
    """
    Send a WhatsApp message via Meta Cloud API for a CRM Lead.

    POST /api/chatter/whatsapp/
    Body JSON:
    {
        "lead_id": "<uuid>",
        "to_phone": "+351912345678",
        "message": "Hello!",
        "reply_to_wamid": "wamid.xxx"   // optional
    }
    """
    try:
        from apps.core.models import ChatterMessage
        from apps.core.whatsapp_utils import send_whatsapp_message

        data = json.loads(request.body)
        lead_id   = data.get('lead_id')
        to_phone  = data.get('to_phone', '').strip()
        body_text = data.get('message', '').strip()
        reply_to  = data.get('reply_to_wamid', '')

        if not to_phone or not body_text:
            return JsonResponse({'success': False, 'error': 'to_phone e message são obrigatórios'}, status=400)

        # Get company WhatsApp config via the active company of the request user
        user = request.user
        active_company = getattr(user, 'active_company', None)
        if not active_company:
            # Fallback: try the first company the user belongs to
            from apps.core.multi_company import get_user_active_company
            active_company = get_user_active_company(request)

        config = getattr(active_company, 'whatsapp_config', None) if active_company else None
        if not config or not config.has_whatsapp_configured:
            return JsonResponse({'success': False, 'error': 'WhatsApp não configurado para esta empresa'}, status=400)

        result = send_whatsapp_message(config, to_phone, body_text, reply_to or None)

        if result['success']:
            # Persist as ChatterMessage (direction=outbound)
            from django.contrib.contenttypes.models import ContentType
            from apps.crm.models import Lead
            ct = ContentType.objects.get_for_model(Lead)
            try:
                lead = Lead.objects.get(pk=lead_id)
                ChatterMessage.objects.create(
                    content_type=ct,
                    object_id=lead.pk,
                    message_type='WHATSAPP',
                    direction='outbound',
                    from_email='',
                    to_email='',
                    subject='',
                    body=body_text,
                    body_html='',
                    message_id=result['wamid'],
                    author=user,
                )
            except Exception as persist_exc:
                logger.warning('[WhatsApp] Could not persist outbound message: %s', persist_exc)

            return JsonResponse({'success': True, 'wamid': result['wamid']})

        return JsonResponse({'success': False, 'error': result['error']}, status=500)

    except Exception as exc:
        logger.exception('[WhatsApp] chatter_send_whatsapp error')
        return JsonResponse({'success': False, 'error': str(exc)}, status=500)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def whatsapp_webhook(request):
    """
    Meta WhatsApp Cloud API webhook endpoint.

    GET  /whatsapp/webhook/  — token verification challenge
    POST /whatsapp/webhook/  — inbound message delivery
    """
    if request.method == 'GET':
        mode      = request.GET.get('hub.mode', '')
        token     = request.GET.get('hub.verify_token', '')
        challenge = request.GET.get('hub.challenge', '')

        # Find a matching config by verify token
        config = CompanyWhatsAppConfig.objects.filter(
            webhook_verify_token=token, is_active=True
        ).first()

        if mode == 'subscribe' and config:
            logger.info('[WhatsApp Webhook] Verified for company=%s', config.company_id)
            from django.http import HttpResponse
            return HttpResponse(challenge, content_type='text/plain')

        logger.warning('[WhatsApp Webhook] GET verification failed: mode=%s token=%s', mode, token)
        from django.http import HttpResponse
        return HttpResponse('Forbidden', status=403)

    # POST — receive inbound messages
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, ValueError) as exc:
        logger.error('[WhatsApp Webhook] Invalid JSON: %s', exc)
        from django.http import HttpResponse
        return HttpResponse('Bad Request', status=400)

    messages_parsed = parse_webhook_payload(payload)
    logger.info('[WhatsApp Webhook] Received %d message(s)', len(messages_parsed))

    for msg in messages_parsed:
        _process_inbound_whatsapp(msg)

    # Meta expects a 200 OK immediately
    from django.http import HttpResponse
    return HttpResponse('EVENT_RECEIVED', content_type='text/plain')


def _process_inbound_whatsapp(msg: dict):
    """
    Match an inbound WhatsApp message to a CRM Lead and persist a ChatterMessage.
    Calls notify_followers() to alert subscribers.
    """
    from django.contrib.contenttypes.models import ContentType
    from apps.crm.models import Lead
    from apps.core.models import ChatterMessage
    from apps.core.models import notify_followers

    from_phone = msg['from_phone']
    body       = msg['body']
    wamid      = msg['wamid']

    # Find a Lead whose phone matches the sender
    lead = None
    for candidate in Lead.objects.filter(is_active=True).only('id', 'phone', 'title'):
        if phones_match(candidate.phone or '', from_phone):
            lead = candidate
            break

    if not lead:
        logger.info('[WhatsApp Webhook] No lead found for phone %s — skipping', from_phone)
        return

    ct = ContentType.objects.get_for_model(Lead)

    # Avoid duplicates by wamid
    if ChatterMessage.objects.filter(message_id=wamid).exists():
        logger.debug('[WhatsApp Webhook] Duplicate wamid %s, skipping', wamid)
        return

    from django.utils import timezone
    import datetime
    ts = msg.get('timestamp', 0)
    sent_at = (
        timezone.make_aware(datetime.datetime.utcfromtimestamp(ts))
        if ts else timezone.now()
    )

    ChatterMessage.objects.create(
        content_type=ct,
        object_id=lead.pk,
        message_type='WHATSAPP',
        direction='inbound',
        from_email=from_phone,
        to_email='',
        subject='',
        body=body,
        body_html='',
        message_id=wamid,
        sent_at=sent_at,
    )

    notify_followers(
        lead,
        'WHATSAPP',
        f'{lead.title} — WhatsApp de {msg.get("wa_name") or from_phone}',
        message=body[:200],
        link=f'/crm/leads/{lead.id}/',
    )
    logger.info('[WhatsApp Webhook] Saved inbound msg for lead %s (wamid=%s)', lead.id, wamid)


@login_required
@require_http_methods(["GET"])
def users_search_api(request):
    """
    API endpoint to search users for @ mentions in chatter.
    
    GET /api/users/search/?q=john
    
    Returns:
        JSON: [{"id": "uuid", "name": "John Doe", "username": "johndoe"}]
    
    Notes:
        - Used for autocomplete @ mentions in chatter textarea
        - Searches by username, first_name, last_name
        - Returns max 10 results
    """
    from apps.accounts.models import CustomUser
    
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 1:
        return JsonResponse([], safe=False)
    
    # Search users
    users = CustomUser.objects.filter(
        is_active=True
    ).filter(
        models.Q(username__icontains=query) |
        models.Q(first_name__icontains=query) |
        models.Q(last_name__icontains=query)
    )[:10]
    
    results = [{
        'id': str(user.id),
        'name': user.get_full_name(),
        'username': user.username
    } for user in users]
    
    return JsonResponse(results, safe=False)


# ══════════════════════════════════════════════════════════════════════════════
# PLANNED ACTIVITIES API
# ══════════════════════════════════════════════════════════════════════════════

def _parse_content_type(object_type):
    """Helper: parse 'crm.lead' → ContentType"""
    app_label, model = object_type.split('.')
    return ContentType.objects.get(app_label=app_label, model=model)


@login_required
@require_POST
def planned_activity_create(request):
    """
    POST /api/chatter/planned-activity/create/
    Body JSON: { object_type, object_id, activity_type_id, summary, due_date, assigned_to_id, note }
    """
    try:
        data = json.loads(request.body)
        object_type = data.get('object_type')
        object_id   = data.get('object_id')
        summary     = data.get('summary', '').strip()

        if not object_type or not object_id or not summary:
            return JsonResponse({'success': False, 'error': 'object_type, object_id e summary são obrigatórios'}, status=400)

        content_type = _parse_content_type(object_type)

        activity_type = None
        if data.get('activity_type_id'):
            activity_type = ActivityType.objects.filter(id=data['activity_type_id']).first()

        assigned_to = request.user
        if data.get('assigned_to_id'):
            from apps.accounts.models import CustomUser
            assigned_to = CustomUser.objects.filter(id=data['assigned_to_id']).first() or request.user

        due_date = None
        if data.get('due_date'):
            from datetime import date
            due_date = date.fromisoformat(data['due_date'])

        pa = PlannedActivity.objects.create(
            content_type=content_type,
            object_id=object_id,
            activity_type=activity_type,
            summary=summary,
            note=data.get('note', ''),
            due_date=due_date,
            assigned_to=assigned_to,
            created_by=request.user,
        )

        return JsonResponse({'success': True, 'id': str(pa.id)})

    except Exception as e:
        import traceback; traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def planned_activity_done(request, pk):
    """
    POST /api/chatter/planned-activity/<pk>/done/
    Body JSON: { done_note: '' }
    """
    try:
        pa = PlannedActivity.objects.get(pk=pk)
        data = json.loads(request.body) if request.body else {}
        from django.utils import timezone
        pa.status   = 'DONE'
        pa.done_at  = timezone.now()
        pa.done_note = data.get('done_note', '')
        pa.save()
        return JsonResponse({'success': True})
    except PlannedActivity.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def planned_activity_cancel(request, pk):
    """
    POST /api/chatter/planned-activity/<pk>/cancel/
    """
    try:
        pa = PlannedActivity.objects.get(pk=pk)
        pa.status = 'CANCELLED'
        pa.save()
        return JsonResponse({'success': True})
    except PlannedActivity.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def planned_activity_edit(request, pk):
    """
    POST /api/chatter/planned-activity/<pk>/edit/
    Body JSON: { summary, due_date, assigned_to_id, note, activity_type_id }
    """
    try:
        pa   = PlannedActivity.objects.get(pk=pk)
        data = json.loads(request.body)

        if data.get('summary'):
            pa.summary = data['summary'].strip()
        if data.get('note') is not None:
            pa.note = data['note']
        if data.get('due_date'):
            from datetime import date
            pa.due_date = date.fromisoformat(data['due_date'])
        if data.get('activity_type_id'):
            pa.activity_type = ActivityType.objects.filter(id=data['activity_type_id']).first()
        if data.get('assigned_to_id'):
            from apps.accounts.models import CustomUser
            pa.assigned_to = CustomUser.objects.filter(id=data['assigned_to_id']).first() or pa.assigned_to
        pa.save()
        return JsonResponse({'success': True})
    except PlannedActivity.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


# ─────────────────────────────────────────────────────────────────────────────
# NOTIFICATIONS API
# ─────────────────────────────────────────────────────────────────────────────

@login_required
@require_http_methods(['GET'])
def notifications_list_api(request):
    """
    GET /api/notifications/
    Query params:
      unread_only=true|false  (default false)
      limit=N                 (default 50)
    """
    unread_only = request.GET.get('unread_only', 'false').lower() == 'true'
    limit = min(int(request.GET.get('limit', 50)), 100)

    qs = Notification.objects.filter(user=request.user)
    if unread_only:
        qs = qs.filter(is_read=False)

    qs = qs.order_by('priority', '-created_at')[:limit]

    def _serialize(n):
        return {
            'id':       str(n.id),
            'type':     n.notification_type,
            'title':    n.title,
            'message':  n.message,
            'link':     n.link,
            'is_read':  n.is_read,
            'is_urgent': n.is_urgent,
            'priority':  n.priority,
            'created_at': n.created_at.strftime('%d/%m/%Y %H:%M'),
        }

    unread_qs    = Notification.objects.filter(user=request.user, is_read=False)
    unread_count = unread_qs.count()
    has_overdue  = unread_qs.filter(notification_type='ACTIVITY_OVERDUE').exists()
    has_today    = unread_qs.filter(notification_type='ACTIVITY_TODAY').exists()

    if has_overdue:
        badge_color = 'red'
    elif has_today:
        badge_color = 'yellow'
    else:
        badge_color = 'default'

    return JsonResponse({
        'unread_count': unread_count,
        'badge_color':  badge_color,
        'has_overdue':  has_overdue,
        'has_today':    has_today,
        'notifications': [_serialize(n) for n in qs],
    })


# Tipos de notificação que NÃO devem ser marcadas como lidas (persistem até actividade concluída)
_ACTIVITY_NOTIF_TYPES = ('ACTIVITY_OVERDUE', 'ACTIVITY_TODAY', 'ACTIVITY_UPCOMING')


@login_required
@require_POST
def notification_mark_read(request, notification_id):
    """POST /api/notifications/<uuid>/mark-read/"""
    try:
        n = Notification.objects.get(id=notification_id, user=request.user)
        # Notificações de actividade persistem até a actividade ser concluída — nunca marcar como lidas
        if n.notification_type not in _ACTIVITY_NOTIF_TYPES:
            n.mark_as_read()
        unread_qs    = Notification.objects.filter(user=request.user, is_read=False)
        unread_count = unread_qs.count()
        has_overdue  = unread_qs.filter(notification_type='ACTIVITY_OVERDUE').exists()
        has_today    = unread_qs.filter(notification_type='ACTIVITY_TODAY').exists()
        badge_color  = 'red' if has_overdue else ('yellow' if has_today else 'default')
        return JsonResponse({'success': True, 'unread_count': unread_count, 'badge_color': badge_color})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Não encontrada'}, status=404)


@login_required
@require_POST
def notifications_mark_all_read(request):
    """POST /api/notifications/mark-all-read/"""
    # Não marcar actividades como lidas — elas persistem até serem concluídas
    Notification.objects.filter(user=request.user, is_read=False).exclude(
        notification_type__in=_ACTIVITY_NOTIF_TYPES
    ).update(
        is_read=True,
        read_at=timezone.now(),
    )
    unread_qs    = Notification.objects.filter(user=request.user, is_read=False)
    unread_count = unread_qs.count()
    has_overdue  = unread_qs.filter(notification_type='ACTIVITY_OVERDUE').exists()
    has_today    = unread_qs.filter(notification_type='ACTIVITY_TODAY').exists()
    badge_color  = 'red' if has_overdue else ('yellow' if has_today else 'default')
    return JsonResponse({'success': True, 'unread_count': unread_count, 'badge_color': badge_color})
