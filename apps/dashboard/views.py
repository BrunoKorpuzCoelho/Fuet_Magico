from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from .models import UserSettings, Notification


@login_required
def dashboard_view(request):
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)
    unread_count = Notification.get_unread_count(request.user)
    
    apps = [
        {'name': 'CRM', 'icon': '🤝', 'url': reverse('crm:crm_home'), 'color': 'from-pink-500 to-rose-600'},
        {'name': 'Contactos', 'icon': '👥', 'url': '/contacts/', 'color': 'from-purple-500 to-indigo-600'},
        {'name': 'Inventário', 'icon': '📦', 'url': '#', 'color': 'from-blue-500 to-cyan-600'},
        {'name': 'Compras', 'icon': '🛒', 'url': '#', 'color': 'from-green-500 to-emerald-600'},
        {'name': 'Vendas', 'icon': '💰', 'url': '#', 'color': 'from-yellow-500 to-amber-600'},
        {'name': 'Website', 'icon': '🌐', 'url': '/', 'color': 'from-orange-500 to-red-600'},
        {'name': 'Financeiro', 'icon': '💳', 'url': '#', 'color': 'from-teal-500 to-green-600'},
        {'name': 'BOM', 'icon': '🎂', 'url': '#', 'color': 'from-indigo-500 to-purple-600'},
        {'name': 'Documentos', 'icon': '📄', 'url': '#', 'color': 'from-gray-500 to-slate-600'},
        {'name': 'Marketing', 'icon': '📱', 'url': '#', 'color': 'from-pink-500 to-fuchsia-600'},
        {'name': 'Relatórios', 'icon': '📊', 'url': '#', 'color': 'from-cyan-500 to-blue-600'},
        {'name': 'Configurações', 'icon': '⚙️', 'url': '#', 'color': 'from-slate-500 to-gray-600'},
    ]
    
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
