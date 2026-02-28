"""
Seed script: Unidades de Medida (UoM) para padaria/pastelaria.

Usage:
    python manage.py shell < scripts/seed_uom.py
    # ou
    python manage.py shell -c "exec(open('scripts/seed_uom.py', encoding='utf-8').read())"

Creates UoM categories and units with conversion factors.
Idempotent — safe to run multiple times.
"""

import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from decimal import Decimal
from apps.inventory.models import UoMCategory, UoM

# ── Helper ──────────────────────────────────────────────────────────

def get_or_create_category(name):
    cat, created = UoMCategory.objects.get_or_create(
        name=name,
        owner_company=None,
        defaults={'is_active': True},
    )
    action = 'CREATED' if created else 'exists'
    print(f'  [{action}] Categoria UdM: {name}')
    return cat


def get_or_create_uom(name, symbol, category, uom_type, factor, rounding=Decimal('0.01')):
    uom, created = UoM.objects.get_or_create(
        name=name,
        category=category,
        owner_company=None,
        defaults={
            'symbol': symbol,
            'uom_type': uom_type,
            'factor': Decimal(str(factor)),
            'rounding': rounding,
            'is_active': True,
        },
    )
    action = 'CREATED' if created else 'exists'
    print(f'    [{action}] {name} ({symbol}) — tipo={uom_type}, factor={factor}')
    return uom


# ── Categories ──────────────────────────────────────────────────────

print('\n=== Seed: Unidades de Medida ===\n')

cat_peso    = get_or_create_category('Peso')
cat_volume  = get_or_create_category('Volume')
cat_unidade = get_or_create_category('Unidade')
cat_tempo   = get_or_create_category('Tempo')

# ── Peso (referência = Grama) ───────────────────────────────────────

print('\n  Peso:')
get_or_create_uom('Grama',      'g',   cat_peso, 'reference', 1)
get_or_create_uom('Quilograma', 'kg',  cat_peso, 'bigger',    1000)
get_or_create_uom('Miligrama',  'mg',  cat_peso, 'smaller',   Decimal('0.001'), rounding=Decimal('0.001'))
get_or_create_uom('Tonelada',   't',   cat_peso, 'bigger',    1000000)
get_or_create_uom('Libra',      'lb',  cat_peso, 'bigger',    Decimal('453.592'))
get_or_create_uom('Onça',       'oz',  cat_peso, 'bigger',    Decimal('28.3495'))

# ── Volume (referência = Mililitro) ─────────────────────────────────

print('\n  Volume:')
get_or_create_uom('Mililitro',  'mL',  cat_volume, 'reference', 1)
get_or_create_uom('Litro',      'L',   cat_volume, 'bigger',    1000)
get_or_create_uom('Decilitro',  'dL',  cat_volume, 'bigger',    100)
get_or_create_uom('Centilitro', 'cL',  cat_volume, 'bigger',    10)
get_or_create_uom('Galão',      'gal', cat_volume, 'bigger',    Decimal('3785.41'))

# ── Unidade (referência = Unidade) ──────────────────────────────────

print('\n  Unidade:')
get_or_create_uom('Unidade',  'un',  cat_unidade, 'reference', 1, rounding=Decimal('1'))
get_or_create_uom('Dúzia',    'dz',  cat_unidade, 'bigger',    12, rounding=Decimal('1'))
get_or_create_uom('Caixa',    'cx',  cat_unidade, 'bigger',    1, rounding=Decimal('1'))
get_or_create_uom('Pacote',   'pct', cat_unidade, 'bigger',    1, rounding=Decimal('1'))
get_or_create_uom('Par',      'par', cat_unidade, 'bigger',    2, rounding=Decimal('1'))
get_or_create_uom('Centena',  'cen', cat_unidade, 'bigger',    100, rounding=Decimal('1'))

# ── Tempo (referência = Minuto) ─────────────────────────────────────

print('\n  Tempo:')
get_or_create_uom('Minuto',   'min', cat_tempo, 'reference', 1, rounding=Decimal('1'))
get_or_create_uom('Hora',     'h',   cat_tempo, 'bigger',    60, rounding=Decimal('0.01'))
get_or_create_uom('Segundo',  's',   cat_tempo, 'smaller',   Decimal('0.016667'), rounding=Decimal('1'))
get_or_create_uom('Dia',      'd',   cat_tempo, 'bigger',    1440, rounding=Decimal('0.01'))

# ── Summary ─────────────────────────────────────────────────────────

total_cats = UoMCategory.objects.filter(is_active=True, owner_company__isnull=True).count()
total_uoms = UoM.objects.filter(is_active=True, owner_company__isnull=True).count()
print(f'\n✅ Seed concluído: {total_cats} categorias UdM, {total_uoms} unidades de medida\n')
