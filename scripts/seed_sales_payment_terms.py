#!/usr/bin/env python
"""Seed default PaymentTerms for the sales app.

Run:
    python manage.py shell < scripts/seed_sales_payment_terms.py
    # or
    python scripts/seed_sales_payment_terms.py
"""
import os
import sys
import django

# Allow running directly (not via manage.py shell)
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

from apps.sales.models import PaymentTerm

TERMS = [
    {'name': 'Pagamento Imediato', 'days': 0,   'description': 'Pagamento na entrega ou no acto.',          'is_default': True},
    {'name': '30 Dias',            'days': 30,  'description': 'Pagamento a 30 dias da data da fatura.',     'is_default': False},
    {'name': '60 Dias',            'days': 60,  'description': 'Pagamento a 60 dias da data da fatura.',     'is_default': False},
    {'name': '90 Dias',            'days': 90,  'description': 'Pagamento a 90 dias da data da fatura.',     'is_default': False},
    {'name': '180 Dias',           'days': 180, 'description': 'Pagamento a 180 dias da data da fatura.',    'is_default': False},
]

created = 0
skipped = 0
for t in TERMS:
    obj, was_created = PaymentTerm.objects.get_or_create(
        name=t['name'],
        owner_company=None,
        defaults={
            'days':        t['days'],
            'description': t['description'],
            'is_default':  t['is_default'],
            'is_active':   True,
        },
    )
    if was_created:
        created += 1
        print(f'  [+] Criada: {obj.name} ({obj.days}d)')
    else:
        skipped += 1
        print(f'  [~] Já existe: {obj.name}')

print(f'\nDone — {created} criada(s), {skipped} já existia(m).')
