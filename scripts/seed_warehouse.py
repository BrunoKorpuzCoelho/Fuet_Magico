"""
Seed script: Armazém Padrão do sistema.

Usage:
    python manage.py shell < scripts/seed_warehouse.py
    # ou
    python manage.py shell -c "exec(open('scripts/seed_warehouse.py', encoding='utf-8').read())"

Creates the default warehouse so inventory works correctly.
Idempotent — safe to run multiple times.
"""

import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.inventory.models import Warehouse


def run():
    """Create default warehouse if it doesn't exist."""
    print('\n=== Seed: Armazém Padrão ===\n')

    wh, created = Warehouse.objects.get_or_create(
        code='WH',
        owner_company=None,
        defaults={
            'name': 'Armazém Principal',
            'is_default': True,
            'is_active': True,
        },
    )

    action = 'CREATED' if created else 'exists'
    print(f'  [{action}] {wh.name} (code={wh.code}, default={wh.is_default})')
    print(f'\n✅ Seed concluído — 1 armazém verificado.\n')
    return wh


if __name__ == '__main__' or '__file__' not in dir():
    run()
