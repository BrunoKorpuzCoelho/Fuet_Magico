"""
Seed script: Condições de Pagamento essenciais.

Usage:
    python manage.py shell < scripts/seed_payment_terms.py
    # ou
    python manage.py shell -c "exec(open('scripts/seed_payment_terms.py', encoding='utf-8').read())"

Cria as condições globais (owner_company=None) partilhadas por todas as empresas.
Idempotente — seguro correr múltiplas vezes.
"""

import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.purchases.models import PaymentTerm

# ── Definição das condições ──────────────────────────────────────────

TERMS = [
    {
        'name':        'Pagamento Imediato',
        'days':        0,
        'description': 'Pagamento no acto da encomenda ou entrega.',
        'is_default':  True,   # padrão para compras e vendas
    },
    {
        'name':        '30 Dias',
        'days':        30,
        'description': 'Pagamento a 30 dias da data da factura.',
        'is_default':  False,
    },
    {
        'name':        '60 Dias',
        'days':        60,
        'description': 'Pagamento a 60 dias da data da factura.',
        'is_default':  False,
    },
    {
        'name':        '90 Dias',
        'days':        90,
        'description': 'Pagamento a 90 dias da data da factura.',
        'is_default':  False,
    },
    {
        'name':        '180 Dias',
        'days':        180,
        'description': 'Pagamento a 180 dias da data da factura.',
        'is_default':  False,
    },
]

# ── Runner ───────────────────────────────────────────────────────────

def run():
    print('\n=== Seed: Condições de Pagamento ===\n')

    for data in TERMS:
        obj, created = PaymentTerm.objects.get_or_create(
            name=data['name'],
            owner_company=None,          # global — visível em todas as empresas
            defaults={
                'days':        data['days'],
                'description': data['description'],
                'is_default':  data['is_default'],
                'is_active':   True,
            },
        )
        if not created:
            # Actualiza campos caso já exista (idempotente)
            changed = False
            for field in ('days', 'description', 'is_active'):
                if getattr(obj, field) != data[field]:
                    setattr(obj, field, data[field])
                    changed = True
            if changed:
                obj.save()

        action = 'CREATED' if created else 'exists'
        default_mark = ' ★ Padrão' if data['is_default'] else ''
        print(f'  [{action}] {obj.name} ({obj.days} dias){default_mark}')

    print(f'\nTotal: {PaymentTerm.objects.filter(owner_company__isnull=True).count()} condições globais.\n')


run()
