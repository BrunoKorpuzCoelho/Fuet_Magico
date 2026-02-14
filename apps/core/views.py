from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.db import models
from apps.accounts.decorators import role_required
from .models import AuditLog, ErrorLog
from datetime import datetime


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
from .models import ChatterMessage, ChatterActivity
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
    API endpoint to send WhatsApp message.
    
    POST /api/chatter/whatsapp/
    Body JSON:
    {
        "object_type": "crm.lead",
        "object_id": "uuid-here",
        "message": "WhatsApp message text"
    }
    
    Returns:
        JSON: {"success": True/False, "message": "..."}
    
    Notes:
        - This is a PLACEHOLDER for Phase 12 (WhatsApp API)
        - Will be fully implemented when WhatsApp integration is added
    """
    try:
        data = json.loads(request.body)
        
        object_type = data.get('object_type')
        object_id = data.get('object_id')
        message = data.get('message', '')
        
        # Log for now (Phase 12 will implement actual WhatsApp API)
        print("=" * 80)
        print("[CHATTER API] chatter_send_whatsapp() CALLED - PLACEHOLDER")
        print(f"User: {request.user.get_full_name()}")
        print(f"Object Type: {object_type}")
        print(f"Object ID: {object_id}")
        print(f"Message: {message[:100]}...")
        print("=" * 80)
        
        # TODO: Implement in Phase 12 (WhatsApp API integration)
        # 1. Get phone number from object (Lead, Contact, etc.)
        # 2. Send via WhatsApp API
        # 3. Create WhatsAppMessage record
        # 4. Create ChatterActivity for audit log
        
        return JsonResponse({
            'success': True,
            'message': 'PLACEHOLDER - WhatsApp integration will be implemented in Phase 12'
        })
    
    except Exception as e:
        print(f"[CHATTER API] ERROR: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


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
