from .models import Notification


def notifications_context(request):
    """
    Injeta em todos os templates:
      - unread_count     : total não lidas
      - badge_color      : 'red' | 'yellow' | 'default'
      - has_overdue_notif: bool (para CSS condicional no badge)
    """
    if not request.user.is_authenticated:
        return {
            'unread_count': 0,
            'badge_color': 'default',
            'has_overdue_notif': False,
        }

    qs = Notification.objects.filter(user=request.user, is_read=False)
    unread_count = qs.count()

    has_overdue = qs.filter(notification_type='ACTIVITY_OVERDUE').exists()
    has_today   = qs.filter(notification_type='ACTIVITY_TODAY').exists()

    if has_overdue:
        badge_color = 'red'
    elif has_today:
        badge_color = 'yellow'
    else:
        badge_color = 'default'

    return {
        'unread_count': unread_count,
        'badge_color': badge_color,
        'has_overdue_notif': has_overdue,
    }
