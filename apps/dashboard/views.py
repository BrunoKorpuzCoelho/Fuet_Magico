from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from .models import UserSettings, Notification


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from .models import UserSettings, Notification
from apps.accounts.models import AppRole

# Mapa slug -> definição visual da app no dashboard
_APP_TILES = [
    {'slug': 'crm',       'name': 'CRM',          'icon': '🤝', 'url_name': 'crm:crm_home'},
    {'slug': 'contacts',  'name': 'Contactos',     'icon': '👥', 'url_name': None, 'url': '/contacts/'},
    {'slug': 'inventory', 'name': 'Inventário',    'icon': '📦', 'url_name': None, 'url': '#'},
    {'slug': 'purchases', 'name': 'Compras',       'icon': '🛒', 'url_name': None, 'url': '#'},
    {'slug': 'sales',     'name': 'Vendas',        'icon': '💰', 'url_name': None, 'url': '#'},
    {'slug': 'website',   'name': 'Website',       'icon': '🌐', 'url_name': None, 'url': '/'},
    {'slug': 'financial', 'name': 'Financeiro',    'icon': '💳', 'url_name': None, 'url': '#'},
    {'slug': 'bom',       'name': 'BOM',           'icon': '🎂', 'url_name': None, 'url': '#'},
    {'slug': 'documents', 'name': 'Documentos',    'icon': '📄', 'url_name': None, 'url': '#'},
    {'slug': 'marketing', 'name': 'Marketing',     'icon': '📱', 'url_name': None, 'url': '#'},
    {'slug': 'reports',   'name': 'Relatórios',    'icon': '📊', 'url_name': None, 'url': '#'},
]


@login_required
def dashboard_view(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    unread_count = Notification.get_unread_count(request.user)

    # --- Filtrar apps por AppRole na empresa ativa ---
    # Global ADMIN vê sempre tudo; os restantes só vêem apps onde têm acesso
    is_global_admin = (request.user.role == 'ADMIN')
    active_company_id = request.session.get('active_company_id')

    if is_global_admin:
        allowed_slugs = {tile['slug'] for tile in _APP_TILES}
    elif active_company_id:
        allowed_slugs = set(
            AppRole.objects.filter(
                user=request.user,
                company_id=active_company_id,
            ).values_list('app', flat=True)
        )
    else:
        allowed_slugs = set()

    apps = []
    for tile in _APP_TILES:
        if tile['slug'] not in allowed_slugs:
            continue
        url = tile.get('url') or ''
        if tile.get('url_name'):
            try:
                url = reverse(tile['url_name'])
            except Exception:
                url = '#'
        apps.append({'name': tile['name'], 'icon': tile['icon'], 'url': url})

    # Tile de Configurações do sistema — só para ADMIN global
    if is_global_admin:
        apps.append({'name': 'Configurações', 'icon': '⚙️', 'url': '#'})

    context = {
        'apps': apps,
        'user_settings': user_settings,
        'unread_count': unread_count,
    }

    return render(request, 'dashboard/index.html', context)


@login_required
@csrf_exempt
def toggle_dark_mode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)
        user_settings.dark_mode = data.get('dark_mode', False)
        user_settings.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
@csrf_exempt
def toggle_developer_mode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_settings, created = UserSettings.objects.get_or_create(user=request.user)
        user_settings.developer_mode = data.get('developer_mode', False)
        user_settings.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
