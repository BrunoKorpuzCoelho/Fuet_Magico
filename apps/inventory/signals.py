import logging
from django.db.models.signals import post_migrate
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
