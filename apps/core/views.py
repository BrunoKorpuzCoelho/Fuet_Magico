from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
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
