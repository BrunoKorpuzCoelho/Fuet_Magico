# -*- coding: utf-8 -*-
"""
Seed: Movimentos de Stock de Demonstração
==========================================
Gera 24 meses de entradas (receção), saídas (expedição) e ajustes de stock
validados, para alimentar relatórios, valorização e forecast.

Estrutura por mês (oldest → newest):
  • 1 receção mensal  — 8 linhas de produtos (ingredientes em bulk)
  • 4 expedições      — 3 linhas cada (saídas para clientes)
  • ajuste trimestral — a cada 3 meses (4 linhas, in ou out)

Total estimado: 24 receções + 96 expedições + 8 ajustes = 128 movimentos

Uso:
    python manage.py seed --only demo_inventory
"""

import random
from datetime import datetime
from decimal import Decimal

from django.utils import timezone

from apps.accounts.models import CustomUser
from apps.contacts.models import Contact
from apps.core.models import Company
from apps.inventory.models import (
    Product, StockMovement, StockMovementLine, StockQuant, Warehouse
)

# ── Parâmetros ────────────────────────────────────────────────────────────────
random.seed(42)          # resultado reprodutível

MONTHS               = 24   # meses de histórico
RECEIPT_LINES        = 8    # linhas por receção mensal
DELIVERIES_PER_MONTH = 4    # expedições por mês
DELIVERY_LINES       = 3    # linhas por expedição
ADJ_LINES            = 4    # linhas por ajuste trimestral


# ── Helper — data para N meses atrás ─────────────────────────────────────────

def _date(months_ago: int, day: int = 5) -> datetime:
    """Devolve datetime timezone-aware para N meses atrás no dia indicado."""
    now = timezone.now()
    total_months = now.year * 12 + (now.month - 1) - months_ago
    year  = total_months // 12
    month = total_months % 12 + 1
    day   = min(day, 28)
    hour  = random.randint(8, 17)
    minute = random.randint(0, 59)
    return timezone.make_aware(datetime(year, month, day, hour, minute))


# ── run() ─────────────────────────────────────────────────────────────────────

def run():

    # ── Pré-requisitos ────────────────────────────────────────────────
    company = Company.objects.filter(name__icontains='Fuet').first()
    if not company:
        raise RuntimeError(
            '❌ Empresa "Fuet Mágico" não encontrada.\n'
            '   Corre primeiro: python manage.py seed --essential'
        )

    warehouse = (
        Warehouse.objects.filter(owner_company=company).first()
        or Warehouse.objects.filter(owner_company__isnull=True).first()
    )
    if not warehouse:
        raise RuntimeError(
            '❌ Nenhum armazém encontrado.\n'
            '   Corre primeiro: python manage.py seed --only default_warehouse'
        )

    products = list(
        Product.objects
        .filter(owner_company=company, product_type='storable', is_active=True)
        .order_by('internal_reference')
    )
    if not products:
        raise RuntimeError(
            '❌ Nenhum produto storable encontrado.\n'
            '   Corre primeiro: python manage.py seed --only demo_products'
        )

    # Subset para movimentos mensais (não é preciso usar todos os 700+)
    products_subset = products[:60]

    suppliers  = list(Contact.objects.filter(contact_category='company').order_by('?')[:8])
    customers  = list(Contact.objects.filter(contact_category='person').order_by('?')[:15])
    admin_user = CustomUser.objects.filter(is_staff=True).first()

    print(f'\n  Empresa : {company.name}')
    print(f'  Armazém : {warehouse.name}')
    print(f'  Produtos: {len(products)} storable ({len(products_subset)} usados nos movimentos mensais)')
    print(f'  Fornec. : {len(suppliers)} | Clientes: {len(customers)}')

    # ── Limpar movimentos existentes ──────────────────────────────────
    deleted, _ = StockMovement.objects.filter(owner_company=company).delete()
    if deleted:
        print(f'\n🗑️  Removidos {deleted} movimentos de stock existentes.')

    # Repor quants a zero
    StockQuant.objects.filter(
        warehouse=warehouse,
        product__owner_company=company,
    ).delete()

    # ── STOCK INICIAL — receção de abertura para TODOS os produtos ────
    BATCH_SIZE = 50  # linhas por movimento (evitar documentos gigantes)
    print(f'\n{"=" * 60}')
    print(f'📦 STOCK INICIAL — {len(products)} produtos em lotes de {BATCH_SIZE}')
    print(f'{"=" * 60}')

    opening_date = _date(MONTHS + 1, day=1)  # 1 mês antes do início do histórico
    total_opening = 0

    for batch_start in range(0, len(products), BATCH_SIZE):
        batch = products[batch_start:batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1

        opening = StockMovement.objects.create(
            movement_type='receipt',
            warehouse=warehouse,
            partner=random.choice(suppliers) if suppliers else None,
            state='draft',
            date=opening_date,
            origin=f'ABERTURA-{batch_num:02d}',
            notes=f'Stock inicial de abertura (lote {batch_num}).',
            responsible=admin_user,
            owner_company=company,
        )
        for product in batch:
            # Stock inicial realista: 50–300 unidades por produto
            qty        = Decimal(str(round(random.uniform(50, 300), 2)))
            unit_price = product.cost_price or Decimal('1.00')
            StockMovementLine.objects.create(
                stock_movement=opening,
                product=product,
                quantity=qty,
                unit_price=unit_price,
                uom=product.uom,
                tax_rate=product.tax_rate,
            )
        opening.action_validate()
        total_opening += len(batch)

    print(f'  ✓ Stock inicial criado para {total_opening} produtos ({batch_num} receção/ões de abertura)')

    # ── Gerar movimentos mês a mês (mais antigo → mais recente) ──────
    print(f'\n{"=" * 60}')
    print(f'📦 GERANDO {MONTHS} MESES DE MOVIMENTOS')
    print(f'{"=" * 60}')

    total_receipts    = 0
    total_deliveries  = 0
    total_adjustments = 0

    for months_ago in range(MONTHS, 0, -1):

        # ── RECEÇÃO mensal (1 por mês) ────────────────────────────────
        rec = StockMovement.objects.create(
            movement_type='receipt',
            warehouse=warehouse,
            partner=random.choice(suppliers) if suppliers else None,
            state='draft',
            date=_date(months_ago, day=random.randint(2, 8)),
            origin=f'PO-{months_ago:04d}',
            notes='Receção mensal de matérias-primas.',
            responsible=admin_user,
            owner_company=company,
        )
        receipt_products = random.sample(products_subset, min(RECEIPT_LINES, len(products_subset)))
        for product in receipt_products:
            qty         = Decimal(str(round(random.uniform(80, 500), 2)))
            unit_price  = (product.cost_price * Decimal(str(round(random.uniform(0.90, 1.08), 4)))).quantize(Decimal('0.01'))
            StockMovementLine.objects.create(
                stock_movement=rec,
                product=product,
                quantity=qty,
                unit_price=unit_price,
                uom=product.uom,
                tax_rate=product.tax_rate,
            )
        rec.action_validate()
        total_receipts += 1

        # ── EXPEDIÇÕES mensais (N por mês) ───────────────────────────
        for d in range(DELIVERIES_PER_MONTH):
            deliv = StockMovement.objects.create(
                movement_type='delivery',
                warehouse=warehouse,
                partner=random.choice(customers) if customers else None,
                state='draft',
                date=_date(months_ago, day=random.randint(10, 28)),
                origin=f'SO-{months_ago:04d}-{d+1:02d}',
                notes='',
                responsible=admin_user,
                owner_company=company,
            )
            deliv_products = random.sample(products_subset, min(DELIVERY_LINES, len(products_subset)))
            for product in deliv_products:
                qty        = Decimal(str(round(random.uniform(5, 25), 2)))
                unit_price = product.sale_price
                StockMovementLine.objects.create(
                    stock_movement=deliv,
                    product=product,
                    quantity=qty,
                    unit_price=unit_price,
                    uom=product.uom,
                    tax_rate=product.tax_rate,
                )
            try:
                deliv.action_validate()
                total_deliveries += 1
            except Exception:
                deliv.delete()

        # ── AJUSTE TRIMESTRAL (a cada 3 meses) ───────────────────────
        if months_ago % 3 == 0:
            direction = 'in' if (months_ago // 3) % 2 == 0 else 'out'
            label     = 'correção positiva' if direction == 'in' else 'quebra/perda'
            adj = StockMovement.objects.create(
                movement_type='adjustment',
                adjustment_direction=direction,
                warehouse=warehouse,
                partner=None,
                state='draft',
                date=_date(months_ago, day=15),
                origin='INVENTÁRIO FÍSICO',
                notes=f'Ajuste trimestral — {label}.',
                responsible=admin_user,
                owner_company=company,
            )
            adj_products = random.sample(products_subset, min(ADJ_LINES, len(products_subset)))
            for product in adj_products:
                qty        = Decimal(str(round(random.uniform(2, 18), 2)))
                unit_price = product.cost_price
                StockMovementLine.objects.create(
                    stock_movement=adj,
                    product=product,
                    quantity=qty,
                    unit_price=unit_price,
                    uom=product.uom,
                    tax_rate=product.tax_rate,
                )
            try:
                adj.action_validate()
                total_adjustments += 1
            except Exception:
                adj.delete()

        # Progress dot every 6 months
        if months_ago % 6 == 0:
            print(f'  ✓ Processados meses {months_ago}→{months_ago - 5} atrás...')

    # ── Resumo ────────────────────────────────────────────────────────
    total_on_hand = StockQuant.objects.filter(
        warehouse=warehouse,
        product__owner_company=company,
        quantity__gt=0,
    ).count()

    total_value = sum(
        sq.quantity * (sq.product.cost_price or Decimal('0'))
        for sq in StockQuant.objects.filter(
            warehouse=warehouse,
            product__owner_company=company,
        ).select_related('product')
    )

    print(f'\n{"=" * 60}')
    print(f'📊 RESUMO FINAL')
    print(f'{"=" * 60}')
    print(f'  📥 Receções  (entradas):   {total_receipts}')
    print(f'  📤 Expedições (saídas):    {total_deliveries}')
    print(f'  🔧 Ajustes:                {total_adjustments}')
    print(f'  ─────────────────────────────────────────')
    print(f'  📦 Total movimentos:       {total_receipts + total_deliveries + total_adjustments}')
    print(f'  🗃️  Produtos com stock > 0: {total_on_hand}')
    print(f'  💶 Valor stock total:      €{total_value:,.2f}')
    print(f'{"=" * 60}')
    print(f'✅ Movimentos de stock gerados com sucesso!\n')


if __name__ == '__main__':
    run()
