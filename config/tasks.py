import re
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Stock Mínimo — verificação periódica (de 4 em 4 horas)
# ---------------------------------------------------------------------------

@shared_task(name='config.tasks.check_low_stock_periodic')
def check_low_stock_periodic():
    """
    Percorre todos os produtos ativos com min_stock > 0 e cria notificações
    SYSTEM para utilizadores da empresa quando o stock está abaixo do mínimo.
    Deduplica: não cria se já existir uma notificação não lida igual.
    """
    from django.db.models import Sum
    from django.contrib.auth import get_user_model
    from apps.inventory.models import Product, StockQuant
    from apps.core.models import Notification

    User = get_user_model()
    products = Product.objects.filter(
        is_active=True, min_stock__gt=0
    ).select_related('uom', 'owner_company')

    created_total = 0
    for product in products:
        on_hand = float(
            StockQuant.objects.filter(product=product)
            .aggregate(t=Sum('quantity'))['t'] or 0
        )
        if on_hand >= float(product.min_stock):
            continue

        if product.owner_company_id:
            users = list(User.objects.filter(
                is_active=True, companies=product.owner_company_id
            ))
        else:
            users = list(User.objects.filter(is_active=True, is_staff=True))

        if not users:
            continue

        uom_name = product.uom.name if product.uom else 'un.'
        title = f'Stock baixo: {product.name}'
        message = (
            f'O produto "{product.name}" tem {on_hand:.3g}\u00a0{uom_name} em mão, '
            f'abaixo do mínimo de {float(product.min_stock):.3g}\u00a0{uom_name}.'
        )
        product_url = f'/inventory/products/{product.pk}/edit/'

        bulk = []
        for user in users:
            already = Notification.objects.filter(
                user=user,
                notification_type='SYSTEM',
                title=title,
                is_read=False,
            ).exists()
            if not already:
                bulk.append(Notification(
                    user=user,
                    notification_type='SYSTEM',
                    title=title,
                    message=message,
                    link=product_url,
                ))
        if bulk:
            Notification.objects.bulk_create(bulk)
            created_total += len(bulk)

    logger.info('[check_low_stock_periodic] %d notification(s) created.', created_total)
    return created_total


# ---------------------------------------------------------------------------
# Polling IMAP — tarefa por utilizador
# ---------------------------------------------------------------------------

@shared_task(bind=True, max_retries=3, default_retry_delay=60, name='config.tasks.poll_imap_for_user')
def poll_imap_for_user(self, user_id: int):
    """
    Verifica o IMAP de um utilizador e guarda as respostas inbound no chatter.
    Chamada pela tarefa periodíca `poll_imap_all_active_users` (de 5 em 5 min).
    """
    from django.contrib.auth import get_user_model
    from django.contrib.contenttypes.models import ContentType
    from apps.core.models import ChatterMessage
    from apps.core.email_utils import poll_imap_replies_for_user

    User = get_user_model()
    try:
        user = User.objects.select_related('email_config').get(pk=user_id)
    except User.DoesNotExist:
        return

    try:
        config = user.email_config
    except Exception:
        return  # utilizador sem configuração SMTP/IMAP

    if not config.is_active or not config.has_smtp_configured:
        return

    # Todos os Message-IDs dos emails outbound deste utilizador
    outbound_qs = (
        ChatterMessage.objects
        .filter(
            author=user,
            message_type='EMAIL',
            direction=ChatterMessage.DIRECTION_OUTBOUND,
        )
        .exclude(message_id='')
        .values('content_type_id', 'object_id', 'message_id')
    )

    if not outbound_qs.exists():
        return

    # Mapa message_id → (content_type_id, object_id)
    msgid_to_record = {
        row['message_id']: (row['content_type_id'], row['object_id'])
        for row in outbound_qs
    }
    known_ids = set(msgid_to_record.keys())

    try:
        inbound = poll_imap_replies_for_user(config, known_message_ids=known_ids)
    except Exception as exc:
        logger.error('poll_imap_for_user: erro inesperado para user %s: %s', user_id, exc)
        raise self.retry(exc=exc)

    new_count = 0
    for em in inbound:
        imap_mid = em['imap_message_id']

        # Evitar duplicados
        if imap_mid and ChatterMessage.objects.filter(
            message_id=imap_mid,
            direction=ChatterMessage.DIRECTION_INBOUND,
        ).exists():
            continue

        # Associar ao registo via In-Reply-To / References
        record_ct_id = record_obj_id = None
        reply_ids = set(re.findall(r'<[^>]+>', em['in_reply_to']))
        reply_ids.update(re.findall(r'<[^>]+>', em['references']))
        for rid in reply_ids:
            if rid in msgid_to_record:
                record_ct_id, record_obj_id = msgid_to_record[rid]
                break

        if record_ct_id is None:
            continue

        try:
            ct = ContentType.objects.get(pk=record_ct_id)
            ChatterMessage.objects.create(
                content_type=ct,
                object_id=record_obj_id,
                author=None,                      # inbound — sem autor interno
                message_type='EMAIL',
                direction=ChatterMessage.DIRECTION_INBOUND,
                from_email=em['from_email'],
                subject=em['subject'],
                body=em['body'],
                message_id=imap_mid,
                in_reply_to=em['in_reply_to'],
                sent_at=em['date'],
                is_internal=False,
            )
            new_count += 1
        except Exception as e:
            logger.error('poll_imap_for_user: erro ao guardar inbound: %s', e)

    if new_count:
        logger.info(
            'poll_imap_for_user: user=%s guardou %d emails inbound', user_id, new_count
        )


# ---------------------------------------------------------------------------
# Polling IMAP — tarefa periódica (dispara uma task por utilizador)
# ---------------------------------------------------------------------------

@shared_task(name='config.tasks.poll_imap_all_active_users')
def poll_imap_all_active_users():
    """
    Tarefa periódica (Celery beat, cada 5 min):
    dispara `poll_imap_for_user` para todos os utilizadores com SMTP/IMAP ativo.
    """
    from apps.accounts.models import UserEmailConfig

    user_ids = list(
        UserEmailConfig.objects
        .filter(is_active=True)
        .exclude(app_password='')
        .values_list('user_id', flat=True)
    )
    for uid in user_ids:
        poll_imap_for_user.delay(uid)

    logger.info('poll_imap_all_active_users: disparou %d tarefas', len(user_ids))


# ---------------------------------------------------------------------------
# Tarefas de teste (mantidas para debug)
# ---------------------------------------------------------------------------

@shared_task(name='config.tasks.test_celery_task')
def test_celery_task(message):
    from time import sleep
    print(f'[Celery Test] Starting task with message: {message}')
    sleep(2)
    print('[Celery Test] Task completed successfully!')
    return f'Task completed: {message}'

