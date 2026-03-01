import logging
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_default_warehouse(sender, **kwargs):
    """Auto-create a default warehouse after migrations if none exists."""
    if sender.name != 'apps.inventory':
        return

    from apps.inventory.models import Warehouse

    # Only create if no warehouses exist at all
    if not Warehouse.objects.exists():
        Warehouse.objects.create(
            name='Armazém Principal',
            code='WH',
            is_default=True,
            owner_company=None,  # Global — visible to all companies
        )
        logger.info('Created default warehouse: Armazém Principal (WH)')


@receiver(post_save, sender='inventory.StockMovement')
def check_low_stock_after_validation(sender, instance, **kwargs):
    """
    After a stock movement is validated (state -> 'done'), check if any
    products in the movement dropped below their min_stock threshold.
    Creates a SYSTEM notification for each affected user (deduped).
    """
    if instance.state != 'done':
        return

    try:
        from django.contrib.auth import get_user_model
        from django.db.models import Sum
        from apps.core.models import Notification
        from apps.inventory.models import StockQuant

        User = get_user_model()

        # Resolve which users to notify
        if instance.owner_company_id:
            users = list(User.objects.filter(
                is_active=True,
                companies=instance.owner_company_id,
            ))
        else:
            users = list(User.objects.filter(is_active=True, is_staff=True))

        if not users:
            return

        for line in instance.lines.select_related('product__uom').all():
            product = line.product
            if not product.min_stock or product.min_stock <= 0:
                continue

            on_hand = float(
                StockQuant.objects.filter(product=product)
                .aggregate(t=Sum('quantity'))['t'] or 0
            )

            if on_hand >= float(product.min_stock):
                continue

            title = f'Stock baixo: {product.name}'
            uom_name = product.uom.name if product.uom else 'un.'
            message = (
                f'O produto "{product.name}" tem {on_hand:.3g} {uom_name} em mão, '
                f'abaixo do mínimo de {float(product.min_stock):.3g} {uom_name}.'
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
                logger.info('[low-stock] %d notification(s) created for "%s"', len(bulk), product.name)

    except Exception as exc:  # never crash the save
        logger.exception('[low-stock signal] unexpected error: %s', exc)
