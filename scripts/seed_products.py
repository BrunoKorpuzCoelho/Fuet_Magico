"""
seed_products.py
-----------------
Seed ~1000 realistic pastry/bakery products (demo data).

Creates products across all categories with realistic Portuguese names,
prices, UoMs, and 6-digit incremental internal references (000001, 000002, …).

Prerequisites:
  - seed_uom.py already run
  - seed_product_categories.py already run

Run:
  python scripts/seed_products.py

Idempotent: Deletes existing products for the company before re-seeding.
"""

import os
import sys
from decimal import Decimal

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django

django.setup()

from apps.inventory.models import Product, Category, UoM, StockMovement, StockMovementLine
from apps.core.models import Company

# ═══════════════════════════════════════════════════════════════════════
# Product definitions
# Format per entry:
#   (name, category_path, uom_symbol, sale_price, cost_price, tax_rate, product_type)
#
# category_path  = exact Category.name already in DB
# uom_symbol     = UoM.symbol (kg, g, L, mL, un, dz, cx, pct, …)
# product_type   = storable | consumable | service
# ═══════════════════════════════════════════════════════════════════════

PRODUCTS = [
    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Farinhas
    # ──────────────────────────────────────────────────────────────────
    ('Farinha de Trigo T55 — Saco 25 kg', 'Farinha de Trigo T55', 'kg', '0.62', '0.45', '6', 'storable'),
    ('Farinha de Trigo T55 — Saco 5 kg', 'Farinha de Trigo T55', 'kg', '0.72', '0.52', '6', 'storable'),
    ('Farinha de Trigo T55 — Saco 1 kg', 'Farinha de Trigo T55', 'kg', '0.89', '0.60', '6', 'storable'),
    ('Farinha de Trigo T65 — Saco 25 kg', 'Farinha de Trigo T65', 'kg', '0.68', '0.48', '6', 'storable'),
    ('Farinha de Trigo T65 — Saco 5 kg', 'Farinha de Trigo T65', 'kg', '0.78', '0.55', '6', 'storable'),
    ('Farinha de Trigo T65 — Saco 1 kg', 'Farinha de Trigo T65', 'kg', '0.95', '0.65', '6', 'storable'),
    ('Farinha T150 Integral — Saco 25 kg', 'Farinha de Trigo T150 (Integral)', 'kg', '1.10', '0.80', '6', 'storable'),
    ('Farinha T150 Integral — Saco 5 kg', 'Farinha de Trigo T150 (Integral)', 'kg', '1.30', '0.95', '6', 'storable'),
    ('Farinha de Amêndoa Extra-Fina — 1 kg', 'Farinha de Amêndoa', 'kg', '12.50', '9.80', '6', 'storable'),
    ('Farinha de Amêndoa Extra-Fina — 5 kg', 'Farinha de Amêndoa', 'kg', '11.80', '9.20', '6', 'storable'),
    ('Farinha de Amêndoa com Pele — 1 kg', 'Farinha de Amêndoa', 'kg', '10.90', '8.50', '6', 'storable'),
    ('Farinha de Arroz — Saco 25 kg', 'Farinha de Arroz', 'kg', '1.20', '0.85', '6', 'storable'),
    ('Farinha de Arroz — Saco 1 kg', 'Farinha de Arroz', 'kg', '1.50', '1.05', '6', 'storable'),
    ('Farinha de Arroz Glutinoso — 1 kg', 'Farinha de Arroz', 'kg', '2.90', '2.10', '6', 'storable'),
    ('Farinha de Centeio Clara — 25 kg', 'Farinha de Centeio', 'kg', '0.95', '0.68', '6', 'storable'),
    ('Farinha de Centeio Escura — 25 kg', 'Farinha de Centeio', 'kg', '1.05', '0.75', '6', 'storable'),
    ('Farinha de Centeio Integral — 5 kg', 'Farinha de Centeio', 'kg', '1.40', '1.00', '6', 'storable'),
    ('Fécula de Batata — Saco 5 kg', 'Fécula de Batata', 'kg', '2.80', '2.00', '6', 'storable'),
    ('Fécula de Batata — Saco 1 kg', 'Fécula de Batata', 'kg', '3.20', '2.30', '6', 'storable'),
    ('Amido de Milho (Maizena) — Saco 5 kg', 'Amido de Milho (Maizena)', 'kg', '2.10', '1.50', '6', 'storable'),
    ('Amido de Milho (Maizena) — Saco 1 kg', 'Amido de Milho (Maizena)', 'kg', '2.50', '1.75', '6', 'storable'),
    ('Amido de Milho (Maizena) — 400 g', 'Amido de Milho (Maizena)', 'g', '3.80', '2.50', '6', 'storable'),
    ('Farinha de Trigo Sarraceno — 1 kg', 'Farinhas', 'kg', '4.50', '3.20', '6', 'storable'),
    ('Farinha de Espelta — 5 kg', 'Farinhas', 'kg', '2.80', '2.00', '6', 'storable'),
    ('Farinha de Espelta — 1 kg', 'Farinhas', 'kg', '3.20', '2.30', '6', 'storable'),
    ('Farinha de Aveia — 1 kg', 'Farinhas', 'kg', '2.60', '1.80', '6', 'storable'),
    ('Farinha de Milho Fina — 1 kg', 'Farinhas', 'kg', '1.15', '0.78', '6', 'storable'),
    ('Farinha de Coco — 500 g', 'Farinhas', 'g', '5.90', '4.10', '6', 'storable'),
    ('Farinha de Castanha — 500 g', 'Farinhas', 'g', '8.50', '6.20', '6', 'storable'),
    ('Sêmola de Trigo Duro — 5 kg', 'Farinhas', 'kg', '1.60', '1.10', '6', 'storable'),
    ('Farinha sem Glúten Mix — 1 kg', 'Farinhas', 'kg', '4.80', '3.40', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Açúcares & Adoçantes
    # ──────────────────────────────────────────────────────────────────
    ('Açúcar Branco Granulado — Saco 25 kg', 'Açúcar Branco', 'kg', '0.85', '0.60', '6', 'storable'),
    ('Açúcar Branco Granulado — Saco 5 kg', 'Açúcar Branco', 'kg', '0.95', '0.68', '6', 'storable'),
    ('Açúcar Branco Granulado — 1 kg', 'Açúcar Branco', 'kg', '1.10', '0.78', '6', 'storable'),
    ('Açúcar Branco Fino (Caster) — 5 kg', 'Açúcar Branco', 'kg', '1.20', '0.85', '6', 'storable'),
    ('Açúcar em Pó (Glacé) — Saco 5 kg', 'Açúcar em Pó (Glacé)', 'kg', '1.80', '1.25', '6', 'storable'),
    ('Açúcar em Pó (Glacé) — 1 kg', 'Açúcar em Pó (Glacé)', 'kg', '2.10', '1.45', '6', 'storable'),
    ('Açúcar em Pó Impalpável — 5 kg', 'Açúcar em Pó (Glacé)', 'kg', '2.50', '1.80', '6', 'storable'),
    ('Açúcar Mascavado Escuro — 5 kg', 'Açúcar Mascavado', 'kg', '2.80', '2.00', '6', 'storable'),
    ('Açúcar Mascavado Claro — 5 kg', 'Açúcar Mascavado', 'kg', '2.60', '1.85', '6', 'storable'),
    ('Açúcar Mascavado — 1 kg', 'Açúcar Mascavado', 'kg', '3.20', '2.30', '6', 'storable'),
    ('Açúcar Demerara — 1 kg', 'Açúcares & Adoçantes', 'kg', '2.40', '1.70', '6', 'storable'),
    ('Açúcar de Coco — 500 g', 'Açúcares & Adoçantes', 'g', '6.50', '4.60', '6', 'storable'),
    ('Mel Multifloral — Balde 5 kg', 'Mel', 'kg', '8.50', '6.20', '6', 'storable'),
    ('Mel Multifloral — Frasco 1 kg', 'Mel', 'kg', '9.80', '7.00', '6', 'storable'),
    ('Mel de Rosmaninho — 1 kg', 'Mel', 'kg', '14.50', '10.50', '6', 'storable'),
    ('Mel de Laranjeira — 1 kg', 'Mel', 'kg', '12.00', '8.80', '6', 'storable'),
    ('Mel de Eucalipto — 1 kg', 'Mel', 'kg', '10.50', '7.50', '6', 'storable'),
    ('Glucose Líquida — Balde 5 kg', 'Glucose Líquida', 'kg', '3.20', '2.20', '6', 'storable'),
    ('Glucose Líquida — 1 kg', 'Glucose Líquida', 'kg', '3.90', '2.70', '6', 'storable'),
    ('Glucose em Pó (DE 40) — 1 kg', 'Glucose Líquida', 'kg', '5.50', '3.90', '6', 'storable'),
    ('Açúcar Invertido (Trimoline) — 7 kg', 'Açúcar Invertido', 'kg', '4.50', '3.10', '6', 'storable'),
    ('Açúcar Invertido (Trimoline) — 1 kg', 'Açúcar Invertido', 'kg', '5.80', '4.00', '6', 'storable'),
    ('Isomalt — 1 kg', 'Açúcares & Adoçantes', 'kg', '9.80', '7.00', '6', 'storable'),
    ('Sorbitol em Pó — 1 kg', 'Açúcares & Adoçantes', 'kg', '7.50', '5.30', '6', 'storable'),
    ('Xarope de Agave — 1 L', 'Açúcares & Adoçantes', 'L', '8.90', '6.30', '6', 'storable'),
    ('Açúcar em Cubos — 1 kg', 'Açúcares & Adoçantes', 'kg', '1.80', '1.25', '6', 'storable'),
    ('Açúcar Perlado (Nib Sugar) — 1 kg', 'Açúcares & Adoçantes', 'kg', '4.80', '3.40', '6', 'storable'),
    ('Xarope de Maple — 500 mL', 'Açúcares & Adoçantes', 'mL', '12.50', '9.00', '6', 'storable'),
    ('Stevia em Pó — 250 g', 'Açúcares & Adoçantes', 'g', '15.00', '10.50', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Gorduras & Óleos
    # ──────────────────────────────────────────────────────────────────
    ('Manteiga sem Sal 82% MG — Bloco 5 kg', 'Manteiga sem Sal', 'kg', '7.80', '5.80', '6', 'storable'),
    ('Manteiga sem Sal 82% MG — 250 g', 'Manteiga sem Sal', 'g', '2.50', '1.80', '6', 'storable'),
    ('Manteiga sem Sal 84% MG Seca — 2 kg', 'Manteiga sem Sal', 'kg', '10.50', '8.00', '6', 'storable'),
    ('Manteiga sem Sal Clarificada — 1 kg', 'Manteiga sem Sal', 'kg', '14.00', '10.50', '6', 'storable'),
    ('Manteiga com Sal — Bloco 5 kg', 'Manteiga com Sal', 'kg', '7.50', '5.50', '6', 'storable'),
    ('Manteiga com Sal — 250 g', 'Manteiga com Sal', 'g', '2.30', '1.65', '6', 'storable'),
    ('Margarina de Folhar 82% — Placa 2 kg', 'Margarina de Folhar', 'kg', '4.20', '2.90', '6', 'storable'),
    ('Margarina de Folhar 82% — 10 kg', 'Margarina de Folhar', 'kg', '3.80', '2.60', '6', 'storable'),
    ('Margarina Multiusos — 10 kg', 'Margarina de Folhar', 'kg', '3.20', '2.20', '6', 'storable'),
    ('Óleo de Girassol — Garrafa 5 L', 'Óleo de Girassol', 'L', '2.20', '1.55', '6', 'storable'),
    ('Óleo de Girassol — Garrafa 1 L', 'Óleo de Girassol', 'L', '2.60', '1.80', '6', 'storable'),
    ('Óleo de Girassol Alto Oleico — 5 L', 'Óleo de Girassol', 'L', '3.40', '2.40', '6', 'storable'),
    ('Azeite Virgem Extra — Lata 5 L', 'Azeite', 'L', '6.80', '5.00', '6', 'storable'),
    ('Azeite Virgem Extra — Garrafa 750 mL', 'Azeite', 'mL', '5.90', '4.20', '6', 'storable'),
    ('Óleo de Coco Virgem — 1 L', 'Gorduras & Óleos', 'L', '9.50', '6.80', '6', 'storable'),
    ('Óleo de Coco Refinado — 1 L', 'Gorduras & Óleos', 'L', '7.20', '5.10', '6', 'storable'),
    ('Natas 35% MG UHT — 1 L', 'Natas', 'L', '3.50', '2.40', '6', 'storable'),
    ('Natas 35% MG Frescas — 1 L', 'Natas', 'L', '4.20', '3.00', '6', 'storable'),
    ('Natas 35% MG UHT — 10 L', 'Natas', 'L', '3.00', '2.10', '6', 'storable'),
    ('Natas Vegetais para Bater — 1 L', 'Natas', 'L', '3.80', '2.60', '6', 'storable'),
    ('Spray Desmoldante — 600 mL', 'Gorduras & Óleos', 'mL', '5.50', '3.80', '6', 'consumable'),
    ('Banha de Porco — 1 kg', 'Gorduras & Óleos', 'kg', '3.90', '2.70', '6', 'storable'),
    ('Creme de Leite Espesso — 1 L', 'Natas', 'L', '4.80', '3.40', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Ovos & Derivados
    # ──────────────────────────────────────────────────────────────────
    ('Ovos Frescos Classe M — Tabuleiro 30 un', 'Ovos & Derivados', 'un', '5.40', '3.80', '6', 'storable'),
    ('Ovos Frescos Classe L — Tabuleiro 30 un', 'Ovos & Derivados', 'un', '6.00', '4.20', '6', 'storable'),
    ('Ovos Frescos Classe XL — Tabuleiro 30 un', 'Ovos & Derivados', 'un', '6.80', '4.80', '6', 'storable'),
    ('Ovos Frescos Bio — Tabuleiro 30 un', 'Ovos & Derivados', 'un', '9.50', '7.00', '6', 'storable'),
    ('Ovos Frescos Classe M — Caixa 360 un', 'Ovos & Derivados', 'un', '55.00', '40.00', '6', 'storable'),
    ('Gema de Ovo Pasteurizada — 1 kg', 'Ovos & Derivados', 'kg', '7.50', '5.40', '6', 'storable'),
    ('Gema de Ovo Pasteurizada — 5 kg', 'Ovos & Derivados', 'kg', '6.80', '4.90', '6', 'storable'),
    ('Clara de Ovo Pasteurizada — 1 kg', 'Ovos & Derivados', 'kg', '4.80', '3.40', '6', 'storable'),
    ('Clara de Ovo Pasteurizada — 5 kg', 'Ovos & Derivados', 'kg', '4.20', '3.00', '6', 'storable'),
    ('Ovo Inteiro Líquido Pasteurizado — 5 kg', 'Ovos & Derivados', 'kg', '5.50', '3.90', '6', 'storable'),
    ('Ovo em Pó — 1 kg', 'Ovos & Derivados', 'kg', '18.00', '13.00', '6', 'storable'),
    ('Clara de Ovo em Pó — 500 g', 'Ovos & Derivados', 'g', '22.00', '16.00', '6', 'storable'),
    ('Gema de Ovo em Pó — 500 g', 'Ovos & Derivados', 'g', '25.00', '18.00', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Leite & Lacticínios
    # ──────────────────────────────────────────────────────────────────
    ('Leite Inteiro UHT — 1 L', 'Leite & Lacticínios', 'L', '0.85', '0.60', '6', 'storable'),
    ('Leite Inteiro UHT — 6 L (Pack)', 'Leite & Lacticínios', 'L', '0.75', '0.52', '6', 'storable'),
    ('Leite em Pó Inteiro — 1 kg', 'Leite & Lacticínios', 'kg', '8.50', '6.10', '6', 'storable'),
    ('Leite em Pó Desnatado — 1 kg', 'Leite & Lacticínios', 'kg', '7.80', '5.60', '6', 'storable'),
    ('Leite em Pó Inteiro — 5 kg', 'Leite & Lacticínios', 'kg', '7.50', '5.30', '6', 'storable'),
    ('Leite Condensado — Lata 397 g', 'Leite & Lacticínios', 'g', '2.20', '1.55', '6', 'storable'),
    ('Leite Condensado — Balde 5 kg', 'Leite & Lacticínios', 'kg', '6.50', '4.60', '6', 'storable'),
    ('Leite Evaporado — Lata 410 g', 'Leite & Lacticínios', 'g', '1.80', '1.25', '6', 'storable'),
    ('Leite de Coco — 400 mL', 'Leite & Lacticínios', 'mL', '2.50', '1.75', '6', 'storable'),
    ('Leite de Amêndoa — 1 L', 'Leite & Lacticínios', 'L', '2.80', '1.95', '6', 'storable'),
    ('Leite de Aveia — 1 L', 'Leite & Lacticínios', 'L', '2.60', '1.80', '6', 'storable'),
    ('Queijo Creme (Cream Cheese) — 1 kg', 'Leite & Lacticínios', 'kg', '6.50', '4.60', '6', 'storable'),
    ('Queijo Creme (Cream Cheese) — 2 kg', 'Leite & Lacticínios', 'kg', '5.80', '4.10', '6', 'storable'),
    ('Queijo Mascarpone — 500 g', 'Leite & Lacticínios', 'g', '5.20', '3.70', '6', 'storable'),
    ('Queijo Mascarpone — 2 kg', 'Leite & Lacticínios', 'kg', '8.50', '6.10', '6', 'storable'),
    ('Queijo Ricotta — 250 g', 'Leite & Lacticínios', 'g', '2.80', '1.95', '6', 'storable'),
    ('Iogurte Natural — 1 kg', 'Leite & Lacticínios', 'kg', '2.50', '1.75', '6', 'storable'),
    ('Iogurte Grego — 1 kg', 'Leite & Lacticínios', 'kg', '4.20', '3.00', '6', 'storable'),
    ('Leitelho (Buttermilk) — 1 L', 'Leite & Lacticínios', 'L', '3.20', '2.25', '6', 'storable'),
    ('Sour Cream — 500 g', 'Leite & Lacticínios', 'g', '3.50', '2.45', '6', 'storable'),
    ('Chantilly Spray — 500 mL', 'Leite & Lacticínios', 'mL', '4.80', '3.40', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Fermento & Leveduras
    # ──────────────────────────────────────────────────────────────────
    ('Fermento em Pó (Chemical) — 1 kg', 'Fermento & Leveduras', 'kg', '5.50', '3.80', '6', 'storable'),
    ('Fermento em Pó (Chemical) — 100 g', 'Fermento & Leveduras', 'g', '1.20', '0.80', '6', 'storable'),
    ('Fermento em Pó Royal — 100 g', 'Fermento & Leveduras', 'g', '1.50', '1.05', '6', 'storable'),
    ('Bicarbonato de Sódio — 1 kg', 'Fermento & Leveduras', 'kg', '3.20', '2.20', '6', 'storable'),
    ('Bicarbonato de Sódio — 250 g', 'Fermento & Leveduras', 'g', '1.50', '1.00', '6', 'storable'),
    ('Levedura Fresca — Bloco 500 g', 'Fermento & Leveduras', 'g', '1.80', '1.20', '6', 'storable'),
    ('Levedura Fresca — Bloco 42 g', 'Fermento & Leveduras', 'g', '0.45', '0.30', '6', 'storable'),
    ('Levedura Seca Instantânea — 500 g', 'Fermento & Leveduras', 'g', '4.50', '3.10', '6', 'storable'),
    ('Levedura Seca Instantânea — 125 g', 'Fermento & Leveduras', 'g', '2.20', '1.50', '6', 'storable'),
    ('Levedura Seca Ativa — 500 g', 'Fermento & Leveduras', 'g', '5.00', '3.50', '6', 'storable'),
    ('Cremor Tártaro — 100 g', 'Fermento & Leveduras', 'g', '3.80', '2.65', '6', 'storable'),
    ('Masa Madre (Levain) Desidratado — 500 g', 'Fermento & Leveduras', 'g', '8.50', '6.00', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Cacau & Chocolate
    # ──────────────────────────────────────────────────────────────────
    ('Chocolate Negro 70% Callebaut — 2.5 kg', 'Chocolate Negro (70%+)', 'kg', '14.50', '10.50', '6', 'storable'),
    ('Chocolate Negro 70% Callebaut — 10 kg', 'Chocolate Negro (70%+)', 'kg', '13.00', '9.40', '6', 'storable'),
    ('Chocolate Negro 55% Callebaut — 2.5 kg', 'Chocolate Negro (70%+)', 'kg', '12.80', '9.20', '6', 'storable'),
    ('Chocolate Negro 85% Cacao Barry — 1 kg', 'Chocolate Negro (70%+)', 'kg', '16.50', '12.00', '6', 'storable'),
    ('Chocolate Negro 64% Valrhona — 3 kg', 'Chocolate Negro (70%+)', 'kg', '22.00', '16.00', '6', 'storable'),
    ('Cobertura Negro 58% — 5 kg', 'Chocolate Negro (70%+)', 'kg', '9.80', '7.00', '6', 'storable'),
    ('Chocolate de Leite 33% Callebaut — 2.5 kg', 'Chocolate de Leite', 'kg', '13.00', '9.40', '6', 'storable'),
    ('Chocolate de Leite 33% Callebaut — 10 kg', 'Chocolate de Leite', 'kg', '11.80', '8.50', '6', 'storable'),
    ('Chocolate de Leite 40% Valrhona — 3 kg', 'Chocolate de Leite', 'kg', '20.50', '14.80', '6', 'storable'),
    ('Cobertura de Leite — 5 kg', 'Chocolate de Leite', 'kg', '8.90', '6.30', '6', 'storable'),
    ('Chocolate Branco 28% Callebaut — 2.5 kg', 'Chocolate Branco', 'kg', '13.50', '9.70', '6', 'storable'),
    ('Chocolate Branco 28% Callebaut — 10 kg', 'Chocolate Branco', 'kg', '12.00', '8.60', '6', 'storable'),
    ('Chocolate Branco Valrhona Ivoire — 3 kg', 'Chocolate Branco', 'kg', '21.00', '15.20', '6', 'storable'),
    ('Cobertura Branca — 5 kg', 'Chocolate Branco', 'kg', '8.50', '6.00', '6', 'storable'),
    ('Cacau em Pó Puro 22/24% — 1 kg', 'Cacau em Pó', 'kg', '8.50', '6.00', '6', 'storable'),
    ('Cacau em Pó Puro 22/24% — 5 kg', 'Cacau em Pó', 'kg', '7.50', '5.30', '6', 'storable'),
    ('Cacau em Pó Alcalino (Negro) — 1 kg', 'Cacau em Pó', 'kg', '10.00', '7.20', '6', 'storable'),
    ('Cacau em Pó Van Houten — 1 kg', 'Cacau em Pó', 'kg', '12.50', '9.00', '6', 'storable'),
    ('Manteiga de Cacau — 1 kg', 'Manteiga de Cacau', 'kg', '18.50', '13.50', '6', 'storable'),
    ('Manteiga de Cacau Mycryo — 550 g', 'Manteiga de Cacau', 'g', '22.00', '16.00', '6', 'storable'),
    ('Pepitas de Chocolate Negro — 1 kg', 'Pepitas de Chocolate', 'kg', '9.50', '6.80', '6', 'storable'),
    ('Pepitas de Chocolate Negro — 5 kg', 'Pepitas de Chocolate', 'kg', '8.50', '6.00', '6', 'storable'),
    ('Pepitas de Chocolate Branco — 1 kg', 'Pepitas de Chocolate', 'kg', '10.00', '7.20', '6', 'storable'),
    ('Pepitas de Chocolate de Leite — 1 kg', 'Pepitas de Chocolate', 'kg', '9.80', '7.00', '6', 'storable'),
    ('Granulado de Chocolate — 1 kg', 'Pepitas de Chocolate', 'kg', '6.50', '4.60', '6', 'storable'),
    ('Raspas de Chocolate Negro — 1 kg', 'Pepitas de Chocolate', 'kg', '12.00', '8.60', '6', 'storable'),
    ('Chocolate Ruby Callebaut — 2.5 kg', 'Cacau & Chocolate', 'kg', '19.80', '14.30', '6', 'storable'),
    ('Chocolate Gold Callebaut — 2.5 kg', 'Cacau & Chocolate', 'kg', '18.50', '13.30', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Frutos Secos & Sementes
    # ──────────────────────────────────────────────────────────────────
    ('Amêndoa Inteira com Pele — 1 kg', 'Frutos Secos & Sementes', 'kg', '11.50', '8.20', '6', 'storable'),
    ('Amêndoa Inteira sem Pele — 1 kg', 'Frutos Secos & Sementes', 'kg', '13.00', '9.40', '6', 'storable'),
    ('Amêndoa Laminada — 1 kg', 'Frutos Secos & Sementes', 'kg', '14.50', '10.50', '6', 'storable'),
    ('Amêndoa Laminada — 5 kg', 'Frutos Secos & Sementes', 'kg', '13.00', '9.40', '6', 'storable'),
    ('Amêndoa Palitada — 1 kg', 'Frutos Secos & Sementes', 'kg', '15.00', '10.80', '6', 'storable'),
    ('Noz Inteira (Metades) — 1 kg', 'Frutos Secos & Sementes', 'kg', '16.50', '12.00', '6', 'storable'),
    ('Noz Inteira (Metades) — 5 kg', 'Frutos Secos & Sementes', 'kg', '15.00', '10.80', '6', 'storable'),
    ('Noz Pecã (Metades) — 1 kg', 'Frutos Secos & Sementes', 'kg', '22.00', '16.00', '6', 'storable'),
    ('Avelã Inteira com Pele — 1 kg', 'Frutos Secos & Sementes', 'kg', '10.50', '7.50', '6', 'storable'),
    ('Avelã Inteira sem Pele — 1 kg', 'Frutos Secos & Sementes', 'kg', '12.50', '9.00', '6', 'storable'),
    ('Avelã Torrada Granulada — 1 kg', 'Frutos Secos & Sementes', 'kg', '13.50', '9.70', '6', 'storable'),
    ('Pistáchio Pelado Verde — 1 kg', 'Frutos Secos & Sementes', 'kg', '38.00', '28.00', '6', 'storable'),
    ('Pistáchio Granulado — 500 g', 'Frutos Secos & Sementes', 'g', '22.00', '16.00', '6', 'storable'),
    ('Castanha de Caju — 1 kg', 'Frutos Secos & Sementes', 'kg', '14.00', '10.00', '6', 'storable'),
    ('Pinhão — 500 g', 'Frutos Secos & Sementes', 'g', '28.00', '20.00', '6', 'storable'),
    ('Coco Ralado — 1 kg', 'Frutos Secos & Sementes', 'kg', '5.50', '3.80', '6', 'storable'),
    ('Coco Ralado Fino — 5 kg', 'Frutos Secos & Sementes', 'kg', '4.80', '3.40', '6', 'storable'),
    ('Coco Laminado (Flakes) — 1 kg', 'Frutos Secos & Sementes', 'kg', '6.50', '4.60', '6', 'storable'),
    ('Sésamo Branco — 1 kg', 'Frutos Secos & Sementes', 'kg', '5.80', '4.10', '6', 'storable'),
    ('Sésamo Negro — 500 g', 'Frutos Secos & Sementes', 'g', '7.50', '5.30', '6', 'storable'),
    ('Linhaça Dourada — 1 kg', 'Frutos Secos & Sementes', 'kg', '4.20', '2.95', '6', 'storable'),
    ('Sementes de Girassol — 1 kg', 'Frutos Secos & Sementes', 'kg', '3.80', '2.65', '6', 'storable'),
    ('Sementes de Abóbora — 1 kg', 'Frutos Secos & Sementes', 'kg', '8.50', '6.10', '6', 'storable'),
    ('Sementes de Chia — 500 g', 'Frutos Secos & Sementes', 'g', '6.50', '4.60', '6', 'storable'),
    ('Sementes de Papoila — 500 g', 'Frutos Secos & Sementes', 'g', '5.80', '4.10', '6', 'storable'),
    ('Praliné de Avelã 50% — 1 kg', 'Frutos Secos & Sementes', 'kg', '16.00', '11.50', '6', 'storable'),
    ('Praliné de Amêndoa — 1 kg', 'Frutos Secos & Sementes', 'kg', '18.00', '13.00', '6', 'storable'),
    ('Pasta de Avelã 100% — 1 kg', 'Frutos Secos & Sementes', 'kg', '15.00', '10.80', '6', 'storable'),
    ('Pasta de Amêndoa (Marzipan) — 1 kg', 'Frutos Secos & Sementes', 'kg', '10.50', '7.50', '6', 'storable'),
    ('Pasta de Pistáchio — 500 g', 'Frutos Secos & Sementes', 'g', '25.00', '18.00', '6', 'storable'),
    ('Flocos de Aveia — 1 kg', 'Frutos Secos & Sementes', 'kg', '2.20', '1.55', '6', 'storable'),
    ('Granola Crocante — 1 kg', 'Frutos Secos & Sementes', 'kg', '6.80', '4.80', '6', 'storable'),
    ('Nozes de Macadâmia — 500 g', 'Frutos Secos & Sementes', 'g', '25.00', '18.00', '6', 'storable'),
    ('Amendoim Torrado — 1 kg', 'Frutos Secos & Sementes', 'kg', '4.50', '3.10', '6', 'storable'),
    ('Pasta de Amendoim — 1 kg', 'Frutos Secos & Sementes', 'kg', '6.00', '4.20', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Frutas & Polpas
    # ──────────────────────────────────────────────────────────────────
    ('Polpa de Framboesa Congelada — 1 kg', 'Frutas & Polpas', 'kg', '9.50', '6.80', '6', 'storable'),
    ('Polpa de Manga Congelada — 1 kg', 'Frutas & Polpas', 'kg', '7.80', '5.50', '6', 'storable'),
    ('Polpa de Maracujá Congelada — 1 kg', 'Frutas & Polpas', 'kg', '8.50', '6.10', '6', 'storable'),
    ('Polpa de Morango Congelada — 1 kg', 'Frutas & Polpas', 'kg', '6.80', '4.80', '6', 'storable'),
    ('Polpa de Frutos Vermelhos — 1 kg', 'Frutas & Polpas', 'kg', '8.00', '5.70', '6', 'storable'),
    ('Polpa de Banana Congelada — 1 kg', 'Frutas & Polpas', 'kg', '5.50', '3.80', '6', 'storable'),
    ('Polpa de Limão — 1 kg', 'Frutas & Polpas', 'kg', '6.50', '4.60', '6', 'storable'),
    ('Polpa de Laranja — 1 kg', 'Frutas & Polpas', 'kg', '5.80', '4.10', '6', 'storable'),
    ('Polpa de Pêssego — 1 kg', 'Frutas & Polpas', 'kg', '6.00', '4.20', '6', 'storable'),
    ('Polpa de Coco Congelada — 1 kg', 'Frutas & Polpas', 'kg', '7.20', '5.10', '6', 'storable'),
    ('Compota de Morango — 2.5 kg', 'Frutas & Polpas', 'kg', '6.50', '4.60', '6', 'storable'),
    ('Compota de Framboesa — 2.5 kg', 'Frutas & Polpas', 'kg', '7.80', '5.60', '6', 'storable'),
    ('Compota de Alperce (Damasco) — 2.5 kg', 'Frutas & Polpas', 'kg', '6.80', '4.80', '6', 'storable'),
    ('Compota de Mirtilo — 2.5 kg', 'Frutas & Polpas', 'kg', '8.50', '6.10', '6', 'storable'),
    ('Compota de Figo — 2.5 kg', 'Frutas & Polpas', 'kg', '7.00', '5.00', '6', 'storable'),
    ('Compota de Cereja — 2.5 kg', 'Frutas & Polpas', 'kg', '7.50', '5.30', '6', 'storable'),
    ('Doce de Ovo — 1 kg', 'Frutas & Polpas', 'kg', '12.00', '8.60', '6', 'storable'),
    ('Frutas Cristalizadas Mistas — 1 kg', 'Frutas & Polpas', 'kg', '8.50', '6.00', '6', 'storable'),
    ('Laranja Cristalizada — 1 kg', 'Frutas & Polpas', 'kg', '9.00', '6.40', '6', 'storable'),
    ('Gengibre Cristalizado — 500 g', 'Frutas & Polpas', 'g', '7.50', '5.30', '6', 'storable'),
    ('Cerejas Confitadas Vermelhas — 1 kg', 'Frutas & Polpas', 'kg', '8.00', '5.70', '6', 'storable'),
    ('Passas Sultanas — 1 kg', 'Frutas & Polpas', 'kg', '4.50', '3.10', '6', 'storable'),
    ('Passas de Corinto — 1 kg', 'Frutas & Polpas', 'kg', '5.80', '4.10', '6', 'storable'),
    ('Arandos (Cranberries) Secos — 500 g', 'Frutas & Polpas', 'g', '6.50', '4.60', '6', 'storable'),
    ('Tâmaras Medjool — 500 g', 'Frutas & Polpas', 'g', '9.80', '7.00', '6', 'storable'),
    ('Figos Secos — 1 kg', 'Frutas & Polpas', 'kg', '7.80', '5.50', '6', 'storable'),
    ('Alperces (Damascos) Secos — 1 kg', 'Frutas & Polpas', 'kg', '8.50', '6.10', '6', 'storable'),
    ('Côco Fresco — un', 'Frutas & Polpas', 'un', '3.50', '2.40', '6', 'storable'),
    ('Limão Siciliano Fresco — un', 'Frutas & Polpas', 'un', '0.50', '0.30', '6', 'storable'),
    ('Laranja Fresca — un', 'Frutas & Polpas', 'un', '0.40', '0.25', '6', 'storable'),
    ('Framboesas Frescas — Cuvete 125 g', 'Frutas & Polpas', 'g', '3.80', '2.75', '6', 'storable'),
    ('Morangos Frescos — Cuvete 500 g', 'Frutas & Polpas', 'g', '3.50', '2.50', '6', 'storable'),
    ('Mirtilos Frescos — Cuvete 125 g', 'Frutas & Polpas', 'g', '3.50', '2.50', '6', 'storable'),
    ('Banana Fresca — kg', 'Frutas & Polpas', 'kg', '1.50', '1.00', '6', 'storable'),
    ('Maçã Granny Smith — kg', 'Frutas & Polpas', 'kg', '1.80', '1.25', '6', 'storable'),
    ('Pera Rocha — kg', 'Frutas & Polpas', 'kg', '2.20', '1.55', '6', 'storable'),
    ('Ananás Fresco — un', 'Frutas & Polpas', 'un', '2.80', '1.95', '6', 'storable'),
    ('Manga Fresca — un', 'Frutas & Polpas', 'un', '2.50', '1.75', '6', 'storable'),
    ('Maracujá Fresco — un', 'Frutas & Polpas', 'un', '0.80', '0.55', '6', 'storable'),
    ('Ruibarbo Congelado — 1 kg', 'Frutas & Polpas', 'kg', '5.50', '3.80', '6', 'storable'),
    ('Frutos Vermelhos Congelados Mix — 1 kg', 'Frutas & Polpas', 'kg', '6.00', '4.20', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Aromas & Extratos
    # ──────────────────────────────────────────────────────────────────
    ('Extrato de Baunilha Natural — 1 L', 'Aromas & Extratos', 'L', '45.00', '32.00', '6', 'storable'),
    ('Extrato de Baunilha Natural — 250 mL', 'Aromas & Extratos', 'mL', '14.50', '10.50', '6', 'storable'),
    ('Vagem de Baunilha Bourbon — 10 un', 'Aromas & Extratos', 'un', '28.00', '20.00', '6', 'storable'),
    ('Vagem de Baunilha Tahiti — 5 un', 'Aromas & Extratos', 'un', '22.00', '16.00', '6', 'storable'),
    ('Pasta de Baunilha — 250 g', 'Aromas & Extratos', 'g', '18.00', '13.00', '6', 'storable'),
    ('Açúcar Vanilado — 1 kg', 'Aromas & Extratos', 'kg', '6.50', '4.60', '6', 'storable'),
    ('Aroma de Baunilha — 1 L', 'Aromas & Extratos', 'L', '8.50', '6.00', '6', 'storable'),
    ('Aroma de Amêndoa Amarga — 1 L', 'Aromas & Extratos', 'L', '9.50', '6.80', '6', 'storable'),
    ('Aroma de Laranja — 1 L', 'Aromas & Extratos', 'L', '8.00', '5.70', '6', 'storable'),
    ('Aroma de Limão — 1 L', 'Aromas & Extratos', 'L', '8.00', '5.70', '6', 'storable'),
    ('Aroma de Rosa — 500 mL', 'Aromas & Extratos', 'mL', '12.00', '8.60', '6', 'storable'),
    ('Aroma de Flor de Laranjeira — 500 mL', 'Aromas & Extratos', 'mL', '10.50', '7.50', '6', 'storable'),
    ('Aroma de Rum — 1 L', 'Aromas & Extratos', 'L', '9.00', '6.40', '6', 'storable'),
    ('Aroma de Café — 1 L', 'Aromas & Extratos', 'L', '10.00', '7.20', '6', 'storable'),
    ('Aroma de Pistáchio — 500 mL', 'Aromas & Extratos', 'mL', '14.00', '10.00', '6', 'storable'),
    ('Aroma de Framboesa — 500 mL', 'Aromas & Extratos', 'mL', '11.00', '7.80', '6', 'storable'),
    ('Aroma de Caramelo — 1 L', 'Aromas & Extratos', 'L', '9.80', '7.00', '6', 'storable'),
    ('Aroma de Coco — 500 mL', 'Aromas & Extratos', 'mL', '9.50', '6.70', '6', 'storable'),
    ('Aroma de Menta — 500 mL', 'Aromas & Extratos', 'mL', '9.00', '6.40', '6', 'storable'),
    ('Aroma de Avelã — 500 mL', 'Aromas & Extratos', 'mL', '10.50', '7.50', '6', 'storable'),
    ('Água de Rosas — 500 mL', 'Aromas & Extratos', 'mL', '6.50', '4.60', '6', 'storable'),
    ('Água de Flor de Laranjeira — 500 mL', 'Aromas & Extratos', 'mL', '5.80', '4.10', '6', 'storable'),
    ('Pasta de Café — 250 g', 'Aromas & Extratos', 'g', '12.00', '8.60', '6', 'storable'),
    ('Café Solúvel — 500 g', 'Aromas & Extratos', 'g', '8.50', '6.00', '6', 'storable'),
    ('Matcha em Pó (Chá Verde) — 100 g', 'Aromas & Extratos', 'g', '15.00', '10.80', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Corantes & Aditivos
    # ──────────────────────────────────────────────────────────────────
    ('Corante Gel Vermelho — 28 g', 'Corantes & Aditivos', 'g', '4.50', '3.10', '6', 'storable'),
    ('Corante Gel Azul — 28 g', 'Corantes & Aditivos', 'g', '4.50', '3.10', '6', 'storable'),
    ('Corante Gel Amarelo — 28 g', 'Corantes & Aditivos', 'g', '4.50', '3.10', '6', 'storable'),
    ('Corante Gel Verde — 28 g', 'Corantes & Aditivos', 'g', '4.50', '3.10', '6', 'storable'),
    ('Corante Gel Rosa — 28 g', 'Corantes & Aditivos', 'g', '4.50', '3.10', '6', 'storable'),
    ('Corante Gel Preto — 28 g', 'Corantes & Aditivos', 'g', '5.00', '3.50', '6', 'storable'),
    ('Corante Gel Castanho — 28 g', 'Corantes & Aditivos', 'g', '4.50', '3.10', '6', 'storable'),
    ('Corante Gel Violeta — 28 g', 'Corantes & Aditivos', 'g', '4.50', '3.10', '6', 'storable'),
    ('Corante Gel Laranja — 28 g', 'Corantes & Aditivos', 'g', '4.50', '3.10', '6', 'storable'),
    ('Kit Corantes Gel 12 Cores', 'Corantes & Aditivos', 'un', '18.00', '12.80', '6', 'storable'),
    ('Corante em Pó Lipossolúvel Vermelho — 25 g', 'Corantes & Aditivos', 'g', '6.50', '4.60', '6', 'storable'),
    ('Corante em Pó Lipossolúvel Amarelo — 25 g', 'Corantes & Aditivos', 'g', '6.50', '4.60', '6', 'storable'),
    ('Corante em Pó Lipossolúvel Azul — 25 g', 'Corantes & Aditivos', 'g', '6.50', '4.60', '6', 'storable'),
    ('Corante Líquido Vermelho — 200 mL', 'Corantes & Aditivos', 'mL', '5.80', '4.10', '6', 'storable'),
    ('Corante Natural Beterraba em Pó — 100 g', 'Corantes & Aditivos', 'g', '8.50', '6.00', '6', 'storable'),
    ('Corante Natural Espirulina — 50 g', 'Corantes & Aditivos', 'g', '9.50', '6.80', '6', 'storable'),
    ('Corante Natural Cúrcuma em Pó — 100 g', 'Corantes & Aditivos', 'g', '5.00', '3.50', '6', 'storable'),
    ('Corante Spray Dourado — 100 mL', 'Corantes & Aditivos', 'mL', '8.00', '5.70', '23', 'storable'),
    ('Corante Spray Prateado — 100 mL', 'Corantes & Aditivos', 'mL', '8.00', '5.70', '23', 'storable'),
    ('Gelatina em Folha (200 bloom) — 500 g', 'Corantes & Aditivos', 'g', '15.00', '10.80', '6', 'storable'),
    ('Gelatina em Folha (200 bloom) — 1 kg', 'Corantes & Aditivos', 'kg', '26.00', '18.80', '6', 'storable'),
    ('Gelatina em Pó — 500 g', 'Corantes & Aditivos', 'g', '12.00', '8.60', '6', 'storable'),
    ('Agar-Agar em Pó — 100 g', 'Corantes & Aditivos', 'g', '15.00', '10.80', '6', 'storable'),
    ('Pectina NH (Nappage) — 500 g', 'Corantes & Aditivos', 'g', '22.00', '16.00', '6', 'storable'),
    ('Pectina Jaune — 500 g', 'Corantes & Aditivos', 'g', '18.00', '13.00', '6', 'storable'),
    ('Lecitina de Soja — 250 g', 'Corantes & Aditivos', 'g', '8.50', '6.00', '6', 'storable'),
    ('Goma Xantana — 250 g', 'Corantes & Aditivos', 'g', '10.00', '7.20', '6', 'storable'),
    ('Ácido Cítrico — 500 g', 'Corantes & Aditivos', 'g', '4.50', '3.10', '6', 'storable'),
    ('Ácido Tartárico — 250 g', 'Corantes & Aditivos', 'g', '5.50', '3.80', '6', 'storable'),
    ('Glicerina Vegetal — 500 mL', 'Corantes & Aditivos', 'mL', '6.00', '4.20', '6', 'storable'),
    ('CMC (Tylose) — 250 g', 'Corantes & Aditivos', 'g', '8.00', '5.70', '6', 'storable'),
    ('Dextrose em Pó — 1 kg', 'Corantes & Aditivos', 'kg', '4.50', '3.10', '6', 'storable'),
    ('Goma Guar — 250 g', 'Corantes & Aditivos', 'g', '7.50', '5.30', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Sal & Especiarias
    # ──────────────────────────────────────────────────────────────────
    ('Sal Fino — 1 kg', 'Sal & Especiarias', 'kg', '0.60', '0.40', '6', 'storable'),
    ('Sal Fino — 25 kg', 'Sal & Especiarias', 'kg', '0.35', '0.22', '6', 'storable'),
    ('Sal Grosso — 1 kg', 'Sal & Especiarias', 'kg', '0.55', '0.35', '6', 'storable'),
    ('Flor de Sal do Algarve — 250 g', 'Sal & Especiarias', 'g', '4.50', '3.10', '6', 'storable'),
    ('Sal Rosa dos Himalaias — 500 g', 'Sal & Especiarias', 'g', '3.80', '2.65', '6', 'storable'),
    ('Canela em Pó Ceilão — 500 g', 'Sal & Especiarias', 'g', '8.50', '6.00', '6', 'storable'),
    ('Canela em Pó Ceilão — 1 kg', 'Sal & Especiarias', 'kg', '14.50', '10.50', '6', 'storable'),
    ('Canela em Pau — 100 g', 'Sal & Especiarias', 'g', '5.50', '3.80', '6', 'storable'),
    ('Noz-Moscada Inteira — 100 g', 'Sal & Especiarias', 'g', '6.50', '4.60', '6', 'storable'),
    ('Noz-Moscada Moída — 50 g', 'Sal & Especiarias', 'g', '4.20', '2.95', '6', 'storable'),
    ('Gengibre Moído — 250 g', 'Sal & Especiarias', 'g', '5.00', '3.50', '6', 'storable'),
    ('Gengibre Fresco — kg', 'Sal & Especiarias', 'kg', '6.50', '4.60', '6', 'storable'),
    ('Cravinho (Cravo-da-Índia) — 50 g', 'Sal & Especiarias', 'g', '4.50', '3.10', '6', 'storable'),
    ('Cardamomo Moído — 50 g', 'Sal & Especiarias', 'g', '7.50', '5.30', '6', 'storable'),
    ('Cardamomo em Vagem — 50 g', 'Sal & Especiarias', 'g', '8.50', '6.00', '6', 'storable'),
    ('Pimenta Preta Moída — 250 g', 'Sal & Especiarias', 'g', '5.50', '3.80', '6', 'storable'),
    ('Erva-Doce (Anis) em Semente — 100 g', 'Sal & Especiarias', 'g', '3.20', '2.20', '6', 'storable'),
    ('Anis Estrelado — 50 g', 'Sal & Especiarias', 'g', '4.80', '3.40', '6', 'storable'),
    ('Açafrão em Pó — 2 g', 'Sal & Especiarias', 'g', '8.50', '6.00', '6', 'storable'),
    ('Cúrcuma Moída — 250 g', 'Sal & Especiarias', 'g', '4.50', '3.10', '6', 'storable'),
    ('Pimenta da Jamaica — 50 g', 'Sal & Especiarias', 'g', '4.00', '2.80', '6', 'storable'),
    ('Mixed Spice (4 Especiarias) — 100 g', 'Sal & Especiarias', 'g', '5.50', '3.80', '6', 'storable'),
    ('Raspa de Limão Desidratada — 250 g', 'Sal & Especiarias', 'g', '9.00', '6.40', '6', 'storable'),
    ('Raspa de Laranja Desidratada — 250 g', 'Sal & Especiarias', 'g', '8.50', '6.00', '6', 'storable'),
    ('Hortelã Seca — 100 g', 'Sal & Especiarias', 'g', '3.50', '2.40', '6', 'storable'),
    ('Lavanda Culinária Seca — 50 g', 'Sal & Especiarias', 'g', '5.80', '4.10', '6', 'storable'),
    ('Baunilha Bourbon em Pó — 50 g', 'Sal & Especiarias', 'g', '12.00', '8.60', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # MATÉRIAS-PRIMAS ▸ Outros ingredientes
    # ──────────────────────────────────────────────────────────────────
    ('Água Mineral — 6 L', 'Matérias-Primas', 'L', '0.50', '0.30', '6', 'consumable'),
    ('Vinagre de Sidra — 500 mL', 'Matérias-Primas', 'mL', '3.20', '2.20', '6', 'storable'),
    ('Vinho do Porto Ruby — 750 mL', 'Matérias-Primas', 'mL', '8.50', '6.00', '23', 'storable'),
    ('Vinho do Porto Tawny — 750 mL', 'Matérias-Primas', 'mL', '9.50', '6.80', '23', 'storable'),
    ('Vinho Madeira — 750 mL', 'Matérias-Primas', 'mL', '7.80', '5.50', '23', 'storable'),
    ('Licor de Amaretto — 700 mL', 'Matérias-Primas', 'mL', '12.50', '9.00', '23', 'storable'),
    ('Licor Grand Marnier — 700 mL', 'Matérias-Primas', 'mL', '25.00', '18.00', '23', 'storable'),
    ('Rum Escuro para Pastelaria — 1 L', 'Matérias-Primas', 'L', '10.00', '7.20', '23', 'storable'),
    ('Kirsch (Aguardente de Cereja) — 500 mL', 'Matérias-Primas', 'mL', '18.00', '13.00', '23', 'storable'),
    ('Cointreau — 700 mL', 'Matérias-Primas', 'mL', '22.00', '16.00', '23', 'storable'),
    ('Conhaque para Pastelaria — 1 L', 'Matérias-Primas', 'L', '9.50', '6.80', '23', 'storable'),
    ('Baileys para Pastelaria — 700 mL', 'Matérias-Primas', 'mL', '14.50', '10.50', '23', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # PRODUTOS ACABADOS ▸ Bolos Tradicionais
    # ──────────────────────────────────────────────────────────────────
    ('Bolo de Chocolate Clássico — Inteiro', 'Bolo de Chocolate', 'un', '18.00', '6.50', '6', 'storable'),
    ('Bolo de Chocolate Clássico — Fatia', 'Bolo de Chocolate', 'un', '2.80', '0.90', '6', 'storable'),
    ('Bolo de Chocolate Belga — Inteiro', 'Bolo de Chocolate', 'un', '22.00', '8.50', '6', 'storable'),
    ('Bolo de Chocolate Belga — Fatia', 'Bolo de Chocolate', 'un', '3.50', '1.20', '6', 'storable'),
    ('Bolo de Chocolate Lava (Coulant) — un', 'Bolo de Chocolate', 'un', '4.50', '1.50', '6', 'storable'),
    ('Bolo de Chocolate Húmido — Inteiro', 'Bolo de Chocolate', 'un', '16.50', '5.80', '6', 'storable'),
    ('Brownie Clássico — un', 'Bolo de Chocolate', 'un', '2.50', '0.80', '6', 'storable'),
    ('Brownie com Nozes — un', 'Bolo de Chocolate', 'un', '2.80', '0.95', '6', 'storable'),
    ('Bolo de Laranja Tradicional — Inteiro', 'Bolo de Laranja', 'un', '14.00', '4.80', '6', 'storable'),
    ('Bolo de Laranja — Fatia', 'Bolo de Laranja', 'un', '2.20', '0.75', '6', 'storable'),
    ('Bolo de Laranja com Calda — Inteiro', 'Bolo de Laranja', 'un', '15.50', '5.50', '6', 'storable'),
    ('Bolo de Laranja e Amêndoa — Inteiro', 'Bolo de Laranja', 'un', '17.00', '6.30', '6', 'storable'),
    ('Bolo de Cenoura com Cobertura — Inteiro', 'Bolo de Cenoura', 'un', '16.00', '5.20', '6', 'storable'),
    ('Bolo de Cenoura — Fatia', 'Bolo de Cenoura', 'un', '2.50', '0.80', '6', 'storable'),
    ('Bolo de Cenoura com Nozes — Inteiro', 'Bolo de Cenoura', 'un', '18.00', '6.50', '6', 'storable'),
    ('Bolo Mármore Clássico — Inteiro', 'Bolo Mármore', 'un', '12.00', '4.00', '6', 'storable'),
    ('Bolo Mármore — Fatia', 'Bolo Mármore', 'un', '1.80', '0.60', '6', 'storable'),
    ('Pão-de-Ló Tradicional — Inteiro', 'Pão-de-Ló', 'un', '10.00', '3.20', '6', 'storable'),
    ('Pão-de-Ló de Ovar — Inteiro', 'Pão-de-Ló', 'un', '14.00', '5.00', '6', 'storable'),
    ('Pão-de-Ló de Alfeizerão — Inteiro', 'Pão-de-Ló', 'un', '12.50', '4.50', '6', 'storable'),
    ('Pão-de-Ló Húmido — Inteiro', 'Pão-de-Ló', 'un', '11.00', '3.80', '6', 'storable'),
    ('Bolo Inglês Tradicional — Inteiro', 'Bolo Inglês', 'un', '10.50', '3.50', '6', 'storable'),
    ('Bolo Inglês com Frutas — Inteiro', 'Bolo Inglês', 'un', '12.00', '4.20', '6', 'storable'),
    ('Bolo Inglês — Fatia', 'Bolo Inglês', 'un', '1.80', '0.55', '6', 'storable'),
    ('Bolo de Banana — Inteiro', 'Bolos Tradicionais', 'un', '13.00', '4.50', '6', 'storable'),
    ('Bolo de Limão Húmido — Inteiro', 'Bolos Tradicionais', 'un', '14.50', '5.00', '6', 'storable'),
    ('Bolo de Maçã & Canela — Inteiro', 'Bolos Tradicionais', 'un', '14.00', '4.80', '6', 'storable'),
    ('Bolo de Noz — Inteiro', 'Bolos Tradicionais', 'un', '16.00', '5.80', '6', 'storable'),
    ('Bolo de Coco — Inteiro', 'Bolos Tradicionais', 'un', '14.50', '5.00', '6', 'storable'),
    ('Bolo de Iogurte — Inteiro', 'Bolos Tradicionais', 'un', '11.50', '3.80', '6', 'storable'),
    ('Bolo Rei — un', 'Bolos Tradicionais', 'un', '12.00', '4.50', '6', 'storable'),
    ('Bolo Rainha — un', 'Bolos Tradicionais', 'un', '10.50', '3.80', '6', 'storable'),
    ('Bolo de Arroz — un', 'Bolos Tradicionais', 'un', '0.90', '0.30', '6', 'storable'),
    ('Queque Tradicional — un', 'Bolos Tradicionais', 'un', '1.20', '0.40', '6', 'storable'),
    ('Queque de Chocolate — un', 'Bolos Tradicionais', 'un', '1.40', '0.48', '6', 'storable'),
    ('Queijada de Sintra — un', 'Bolos Tradicionais', 'un', '1.50', '0.50', '6', 'storable'),
    ('Travesseiro de Sintra — un', 'Bolos Tradicionais', 'un', '2.80', '0.95', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # PRODUTOS ACABADOS ▸ Bolos Decorados
    # ──────────────────────────────────────────────────────────────────
    ('Bolo Aniversário Chocolate — Pequeno', 'Bolos de Aniversário', 'un', '28.00', '10.00', '6', 'storable'),
    ('Bolo Aniversário Chocolate — Médio', 'Bolos de Aniversário', 'un', '38.00', '14.00', '6', 'storable'),
    ('Bolo Aniversário Chocolate — Grande', 'Bolos de Aniversário', 'un', '48.00', '18.00', '6', 'storable'),
    ('Bolo Aniversário Natas — Pequeno', 'Bolos de Aniversário', 'un', '25.00', '9.00', '6', 'storable'),
    ('Bolo Aniversário Natas — Médio', 'Bolos de Aniversário', 'un', '35.00', '12.50', '6', 'storable'),
    ('Bolo Aniversário Natas — Grande', 'Bolos de Aniversário', 'un', '45.00', '16.00', '6', 'storable'),
    ('Bolo Aniversário Frutas — Médio', 'Bolos de Aniversário', 'un', '40.00', '15.00', '6', 'storable'),
    ('Bolo Aniversário Red Velvet — Médio', 'Bolos de Aniversário', 'un', '42.00', '15.50', '6', 'storable'),
    ('Bolo Casamento 2 Andares — Clássico', 'Bolos de Casamento', 'un', '120.00', '45.00', '6', 'storable'),
    ('Bolo Casamento 3 Andares — Clássico', 'Bolos de Casamento', 'un', '180.00', '65.00', '6', 'storable'),
    ('Bolo Casamento 3 Andares — Premium', 'Bolos de Casamento', 'un', '250.00', '90.00', '6', 'storable'),
    ('Bolo Casamento 4 Andares — Luxo', 'Bolos de Casamento', 'un', '350.00', '130.00', '6', 'storable'),
    ('Bolo Casamento Nude Cake — 2 Andares', 'Bolos de Casamento', 'un', '95.00', '35.00', '6', 'storable'),
    ('Bolo Temático Infantil — Médio', 'Bolos Temáticos', 'un', '45.00', '16.00', '6', 'storable'),
    ('Bolo Temático Infantil — Grande', 'Bolos Temáticos', 'un', '60.00', '22.00', '6', 'storable'),
    ('Bolo Temático Empresarial — Médio', 'Bolos Temáticos', 'un', '55.00', '20.00', '6', 'storable'),
    ('Bolo Number Cake — Dígito', 'Bolos Temáticos', 'un', '35.00', '12.00', '6', 'storable'),
    ('Bolo Drip Cake — Médio', 'Bolos Temáticos', 'un', '38.00', '13.50', '6', 'storable'),
    ('Cupcake Baunilha — un', 'Cupcakes', 'un', '2.80', '0.90', '6', 'storable'),
    ('Cupcake Chocolate — un', 'Cupcakes', 'un', '2.80', '0.95', '6', 'storable'),
    ('Cupcake Red Velvet — un', 'Cupcakes', 'un', '3.00', '1.00', '6', 'storable'),
    ('Cupcake Limão — un', 'Cupcakes', 'un', '2.80', '0.90', '6', 'storable'),
    ('Cupcake Oreo — un', 'Cupcakes', 'un', '3.20', '1.10', '6', 'storable'),
    ('Cupcake Caramelo Salgado — un', 'Cupcakes', 'un', '3.20', '1.10', '6', 'storable'),
    ('Caixa Cupcakes Sortidos — 6 un', 'Cupcakes', 'cx', '15.00', '5.40', '6', 'storable'),
    ('Caixa Cupcakes Sortidos — 12 un', 'Cupcakes', 'cx', '28.00', '10.20', '6', 'storable'),
    ('Cake Pop Baunilha — un', 'Cake Pops', 'un', '2.50', '0.80', '6', 'storable'),
    ('Cake Pop Chocolate — un', 'Cake Pops', 'un', '2.50', '0.85', '6', 'storable'),
    ('Cake Pops Sortidos — Caixa 12', 'Cake Pops', 'cx', '25.00', '9.00', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # PRODUTOS ACABADOS ▸ Tartes & Tortas
    # ──────────────────────────────────────────────────────────────────
    ('Pastel de Nata — un', 'Tarte de Nata', 'un', '1.20', '0.35', '6', 'storable'),
    ('Pastel de Nata — Caixa 6 un', 'Tarte de Nata', 'cx', '6.50', '2.00', '6', 'storable'),
    ('Pastel de Nata — Caixa 12 un', 'Tarte de Nata', 'cx', '12.00', '3.80', '6', 'storable'),
    ('Pastel de Nata Premium — un', 'Tarte de Nata', 'un', '1.80', '0.55', '6', 'storable'),
    ('Tarte de Nata Grande — Inteiro', 'Tarte de Nata', 'un', '14.00', '4.80', '6', 'storable'),
    ('Tarte de Amêndoa — Inteiro', 'Tarte de Amêndoa', 'un', '16.00', '5.80', '6', 'storable'),
    ('Tarte de Amêndoa — Fatia', 'Tarte de Amêndoa', 'un', '2.50', '0.85', '6', 'storable'),
    ('Tarte de Amêndoa Individual — un', 'Tarte de Amêndoa', 'un', '3.00', '1.00', '6', 'storable'),
    ('Tarte de Frutas Vermelhas — Inteiro', 'Tarte de Frutas', 'un', '18.00', '6.50', '6', 'storable'),
    ('Tarte de Frutas da Estação — Inteiro', 'Tarte de Frutas', 'un', '20.00', '7.50', '6', 'storable'),
    ('Tartelete de Frutas — un', 'Tarte de Frutas', 'un', '3.80', '1.30', '6', 'storable'),
    ('Tarte de Limão Merengada — Inteiro', 'Tarte de Frutas', 'un', '16.50', '5.80', '6', 'storable'),
    ('Cheesecake New York — Inteiro', 'Cheesecake', 'un', '20.00', '7.20', '6', 'storable'),
    ('Cheesecake New York — Fatia', 'Cheesecake', 'un', '3.50', '1.10', '6', 'storable'),
    ('Cheesecake Frutos Vermelhos — Inteiro', 'Cheesecake', 'un', '22.00', '8.00', '6', 'storable'),
    ('Cheesecake Maracujá — Inteiro', 'Cheesecake', 'un', '22.00', '8.00', '6', 'storable'),
    ('Cheesecake Oreo — Inteiro', 'Cheesecake', 'un', '23.00', '8.50', '6', 'storable'),
    ('Cheesecake Japonês (Fluffy) — un', 'Cheesecake', 'un', '12.00', '4.20', '6', 'storable'),
    ('Cheesecake Individual — un', 'Cheesecake', 'un', '4.00', '1.40', '6', 'storable'),
    ('Tarte de Chocolate Ganache — Inteiro', 'Tarte de Chocolate', 'un', '18.00', '6.50', '6', 'storable'),
    ('Tarte de Chocolate Ganache — Fatia', 'Tarte de Chocolate', 'un', '3.00', '1.00', '6', 'storable'),
    ('Tarte Tatin de Maçã — Inteiro', 'Tartes & Tortas', 'un', '16.00', '5.80', '6', 'storable'),
    ('Tarte Frangipane — Inteiro', 'Tartes & Tortas', 'un', '17.00', '6.20', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # PRODUTOS ACABADOS ▸ Pastelaria Fina
    # ──────────────────────────────────────────────────────────────────
    ('Éclair de Chocolate — un', 'Éclairs', 'un', '3.50', '1.10', '6', 'storable'),
    ('Éclair de Baunilha — un', 'Éclairs', 'un', '3.50', '1.10', '6', 'storable'),
    ('Éclair de Café — un', 'Éclairs', 'un', '3.50', '1.10', '6', 'storable'),
    ('Éclair de Pistáchio — un', 'Éclairs', 'un', '4.00', '1.40', '6', 'storable'),
    ('Éclair de Caramelo — un', 'Éclairs', 'un', '3.80', '1.25', '6', 'storable'),
    ('Éclair de Framboesa — un', 'Éclairs', 'un', '3.80', '1.25', '6', 'storable'),
    ('Profiterole de Chocolate — Caixa 6', 'Profiteroles', 'cx', '8.00', '2.80', '6', 'storable'),
    ('Profiterole de Nata — un', 'Profiteroles', 'un', '1.50', '0.45', '6', 'storable'),
    ('Croquembouche Tradicional — un', 'Profiteroles', 'un', '45.00', '16.00', '6', 'storable'),
    ('Paris-Brest — un', 'Profiteroles', 'un', '4.50', '1.50', '6', 'storable'),
    ('Mil-Folhas Clássico — Inteiro', 'Mil-Folhas', 'un', '16.00', '5.50', '6', 'storable'),
    ('Mil-Folhas — Fatia', 'Mil-Folhas', 'un', '2.80', '0.90', '6', 'storable'),
    ('Mil-Folhas Individual — un', 'Mil-Folhas', 'un', '3.50', '1.15', '6', 'storable'),
    ('Mil-Folhas de Frutas — Inteiro', 'Mil-Folhas', 'un', '18.00', '6.50', '6', 'storable'),
    ('Macaron de Framboesa — un', 'Macarons', 'un', '2.00', '0.70', '6', 'storable'),
    ('Macaron de Chocolate — un', 'Macarons', 'un', '2.00', '0.70', '6', 'storable'),
    ('Macaron de Pistáchio — un', 'Macarons', 'un', '2.20', '0.80', '6', 'storable'),
    ('Macaron de Baunilha — un', 'Macarons', 'un', '2.00', '0.70', '6', 'storable'),
    ('Macaron de Caramelo Salgado — un', 'Macarons', 'un', '2.20', '0.75', '6', 'storable'),
    ('Macaron de Limão — un', 'Macarons', 'un', '2.00', '0.70', '6', 'storable'),
    ('Macaron de Rosa — un', 'Macarons', 'un', '2.20', '0.80', '6', 'storable'),
    ('Macaron de Café — un', 'Macarons', 'un', '2.00', '0.70', '6', 'storable'),
    ('Macaron de Maracujá — un', 'Macarons', 'un', '2.20', '0.75', '6', 'storable'),
    ('Macaron de Matcha — un', 'Macarons', 'un', '2.50', '0.90', '6', 'storable'),
    ('Caixa Macarons Sortidos — 6 un', 'Macarons', 'cx', '12.00', '4.00', '6', 'storable'),
    ('Caixa Macarons Sortidos — 12 un', 'Macarons', 'cx', '22.00', '7.50', '6', 'storable'),
    ('Caixa Macarons Sortidos — 24 un', 'Macarons', 'cx', '40.00', '14.00', '6', 'storable'),
    ('Croissant Simples — un', 'Croissants', 'un', '1.30', '0.40', '6', 'storable'),
    ('Croissant com Manteiga — un', 'Croissants', 'un', '1.50', '0.50', '6', 'storable'),
    ('Croissant de Amêndoa — un', 'Croissants', 'un', '2.20', '0.75', '6', 'storable'),
    ('Croissant de Chocolate — un', 'Croissants', 'un', '1.80', '0.60', '6', 'storable'),
    ('Pain au Chocolat — un', 'Croissants', 'un', '1.80', '0.60', '6', 'storable'),
    ('Croissant Misto (Fiambre e Queijo) — un', 'Croissants', 'un', '2.50', '0.85', '6', 'storable'),
    ('Mini Croissant — un', 'Croissants', 'un', '0.80', '0.25', '6', 'storable'),
    ('Palmier Grande — un', 'Palmiers', 'un', '1.80', '0.55', '6', 'storable'),
    ('Palmier Pequeno — un', 'Palmiers', 'un', '0.90', '0.28', '6', 'storable'),
    ('Palmier de Chocolate — un', 'Palmiers', 'un', '2.00', '0.65', '6', 'storable'),
    ('Palmier Caramelizado — un', 'Palmiers', 'un', '1.50', '0.45', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # PRODUTOS ACABADOS ▸ Folhados
    # ──────────────────────────────────────────────────────────────────
    ('Folhado de Salsicha — un', 'Folhados', 'un', '1.80', '0.60', '6', 'storable'),
    ('Folhado de Carne — un', 'Folhados', 'un', '2.20', '0.75', '6', 'storable'),
    ('Folhado de Frango — un', 'Folhados', 'un', '2.20', '0.75', '6', 'storable'),
    ('Rissol de Camarão — un', 'Folhados', 'un', '1.50', '0.50', '6', 'storable'),
    ('Rissol de Carne — un', 'Folhados', 'un', '1.30', '0.42', '6', 'storable'),
    ('Empada de Galinha — un', 'Folhados', 'un', '1.80', '0.60', '6', 'storable'),
    ('Empada de Atum — un', 'Folhados', 'un', '1.80', '0.60', '6', 'storable'),
    ('Croquete de Carne — un', 'Folhados', 'un', '1.20', '0.38', '6', 'storable'),
    ('Pastel de Bacalhau — un', 'Folhados', 'un', '1.50', '0.50', '6', 'storable'),
    ('Chamuça de Legumes — un', 'Folhados', 'un', '1.50', '0.48', '6', 'storable'),
    ('Chamuça de Frango — un', 'Folhados', 'un', '1.60', '0.52', '6', 'storable'),
    ('Vol-au-Vent Cogumelos — un', 'Folhados', 'un', '2.50', '0.85', '6', 'storable'),
    ('Folhado de Espinafres e Queijo — un', 'Folhados', 'un', '2.00', '0.68', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # PRODUTOS ACABADOS ▸ Pão & Pão Especial
    # ──────────────────────────────────────────────────────────────────
    ('Pão de Forma Branco — un', 'Pão & Pão Especial', 'un', '2.50', '0.80', '6', 'storable'),
    ('Pão de Forma Integral — un', 'Pão & Pão Especial', 'un', '3.00', '1.00', '6', 'storable'),
    ('Pão de Forma Sementes — un', 'Pão & Pão Especial', 'un', '3.50', '1.20', '6', 'storable'),
    ('Pão Francês — un', 'Pão & Pão Especial', 'un', '0.30', '0.10', '6', 'storable'),
    ('Pão Alentejano — un', 'Pão & Pão Especial', 'un', '2.80', '0.90', '6', 'storable'),
    ('Pão de Centeio — un', 'Pão & Pão Especial', 'un', '3.20', '1.10', '6', 'storable'),
    ('Pão Rústico de Massa Mãe — un', 'Pão & Pão Especial', 'un', '4.50', '1.50', '6', 'storable'),
    ('Pão Integral com Sementes — un', 'Pão & Pão Especial', 'un', '3.80', '1.30', '6', 'storable'),
    ('Pão de Milho (Broa) — un', 'Pão & Pão Especial', 'un', '3.50', '1.15', '6', 'storable'),
    ('Pão Ciabatta — un', 'Pão & Pão Especial', 'un', '2.80', '0.90', '6', 'storable'),
    ('Pão Focaccia — un', 'Pão & Pão Especial', 'un', '4.00', '1.35', '6', 'storable'),
    ('Baguete Francesa — un', 'Pão & Pão Especial', 'un', '1.50', '0.48', '6', 'storable'),
    ('Brioche Clássico — un', 'Pão & Pão Especial', 'un', '3.80', '1.30', '6', 'storable'),
    ('Brioche Individual — un', 'Pão & Pão Especial', 'un', '1.80', '0.60', '6', 'storable'),
    ('Pão de Leite — un', 'Pão & Pão Especial', 'un', '1.20', '0.38', '6', 'storable'),
    ('Pão com Chouriço — un', 'Pão & Pão Especial', 'un', '2.50', '0.85', '6', 'storable'),
    ('Pão de Alho — un', 'Pão & Pão Especial', 'un', '1.80', '0.58', '6', 'storable'),
    ('Bagel Simples — un', 'Pão & Pão Especial', 'un', '1.50', '0.48', '6', 'storable'),
    ('Bagel Sésamo — un', 'Pão & Pão Especial', 'un', '1.80', '0.58', '6', 'storable'),
    ('Pretzel Salgado — un', 'Pão & Pão Especial', 'un', '2.00', '0.65', '6', 'storable'),
    ('Pão Naan — un', 'Pão & Pão Especial', 'un', '1.80', '0.55', '6', 'storable'),
    ('Folar de Páscoa — un', 'Pão & Pão Especial', 'un', '8.00', '2.80', '6', 'storable'),
    ('Bola de Berlim Simples — un', 'Pão & Pão Especial', 'un', '1.20', '0.38', '6', 'storable'),
    ('Bola de Berlim com Creme — un', 'Pão & Pão Especial', 'un', '1.80', '0.58', '6', 'storable'),
    ('Donuts Chocolate — un', 'Pão & Pão Especial', 'un', '1.80', '0.60', '6', 'storable'),
    ('Donuts Açúcar e Canela — un', 'Pão & Pão Especial', 'un', '1.50', '0.48', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # PRODUTOS ACABADOS ▸ Sobremesas Individuais
    # ──────────────────────────────────────────────────────────────────
    ('Mousse de Chocolate Negro — Copo', 'Sobremesas Individuais', 'un', '3.80', '1.20', '6', 'storable'),
    ('Mousse de Chocolate de Leite — Copo', 'Sobremesas Individuais', 'un', '3.80', '1.20', '6', 'storable'),
    ('Mousse de Chocolate Branco — Copo', 'Sobremesas Individuais', 'un', '3.80', '1.25', '6', 'storable'),
    ('Mousse de Maracujá — Copo', 'Sobremesas Individuais', 'un', '3.50', '1.10', '6', 'storable'),
    ('Mousse de Manga — Copo', 'Sobremesas Individuais', 'un', '3.50', '1.10', '6', 'storable'),
    ('Panna Cotta Baunilha — Copo', 'Sobremesas Individuais', 'un', '3.50', '1.05', '6', 'storable'),
    ('Panna Cotta Frutos Vermelhos — Copo', 'Sobremesas Individuais', 'un', '4.00', '1.30', '6', 'storable'),
    ('Crème Brûlée Clássica — un', 'Sobremesas Individuais', 'un', '4.50', '1.40', '6', 'storable'),
    ('Crème Caramel — un', 'Sobremesas Individuais', 'un', '3.00', '0.90', '6', 'storable'),
    ('Tiramisu — Copo Individual', 'Sobremesas Individuais', 'un', '4.50', '1.50', '6', 'storable'),
    ('Tiramisu — Travessa (8 porções)', 'Sobremesas Individuais', 'un', '22.00', '8.00', '6', 'storable'),
    ('Pudim Flan Tradicional — un', 'Sobremesas Individuais', 'un', '2.50', '0.80', '6', 'storable'),
    ('Pudim Abade de Priscos — un', 'Sobremesas Individuais', 'un', '3.50', '1.15', '6', 'storable'),
    ('Leite-Creme Clássico — un', 'Sobremesas Individuais', 'un', '2.80', '0.85', '6', 'storable'),
    ('Arroz Doce Tradicional — Copo', 'Sobremesas Individuais', 'un', '2.50', '0.75', '6', 'storable'),
    ('Aletria — Copo', 'Sobremesas Individuais', 'un', '2.50', '0.75', '6', 'storable'),
    ('Serradura — Copo', 'Sobremesas Individuais', 'un', '3.50', '1.10', '6', 'storable'),
    ('Toucinho do Céu — Fatia', 'Sobremesas Individuais', 'un', '2.80', '0.90', '6', 'storable'),
    ('Molotof (Farófias) — Porção', 'Sobremesas Individuais', 'un', '3.00', '0.80', '6', 'storable'),
    ('Suspiro Merengue — un', 'Sobremesas Individuais', 'un', '1.50', '0.40', '6', 'storable'),
    ('Pavlova Individual — un', 'Sobremesas Individuais', 'un', '4.50', '1.50', '6', 'storable'),
    ('Opera Cake — Fatia', 'Sobremesas Individuais', 'un', '4.00', '1.40', '6', 'storable'),
    ('Entremet Chocolate — un', 'Sobremesas Individuais', 'un', '5.50', '2.00', '6', 'storable'),
    ('Entremet Frutas — un', 'Sobremesas Individuais', 'un', '5.50', '2.00', '6', 'storable'),
    ('Cannoli Siciliano — un', 'Sobremesas Individuais', 'un', '3.50', '1.10', '6', 'storable'),
    ('Natas do Céu — Copo', 'Sobremesas Individuais', 'un', '3.00', '0.95', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # PRODUTOS ACABADOS ▸ Gelados & Semifrios
    # ──────────────────────────────────────────────────────────────────
    ('Gelado Artesanal Baunilha — 500 mL', 'Gelados & Semifrios', 'mL', '6.50', '2.30', '6', 'storable'),
    ('Gelado Artesanal Chocolate — 500 mL', 'Gelados & Semifrios', 'mL', '6.50', '2.40', '6', 'storable'),
    ('Gelado Artesanal Morango — 500 mL', 'Gelados & Semifrios', 'mL', '6.50', '2.30', '6', 'storable'),
    ('Gelado Artesanal Pistáchio — 500 mL', 'Gelados & Semifrios', 'mL', '7.50', '2.80', '6', 'storable'),
    ('Gelado Artesanal Manga — 500 mL', 'Gelados & Semifrios', 'mL', '6.50', '2.30', '6', 'storable'),
    ('Gelado Artesanal Café — 500 mL', 'Gelados & Semifrios', 'mL', '6.50', '2.40', '6', 'storable'),
    ('Gelado Artesanal Caramelo — 500 mL', 'Gelados & Semifrios', 'mL', '6.50', '2.40', '6', 'storable'),
    ('Sorbet Limão — 500 mL', 'Gelados & Semifrios', 'mL', '6.00', '2.00', '6', 'storable'),
    ('Sorbet Framboesa — 500 mL', 'Gelados & Semifrios', 'mL', '6.50', '2.30', '6', 'storable'),
    ('Sorbet Manga — 500 mL', 'Gelados & Semifrios', 'mL', '6.50', '2.30', '6', 'storable'),
    ('Semifrio de Chocolate — Inteiro', 'Gelados & Semifrios', 'un', '18.00', '6.50', '6', 'storable'),
    ('Semifrio de Maracujá — Inteiro', 'Gelados & Semifrios', 'un', '18.00', '6.50', '6', 'storable'),
    ('Semifrio de Manga — Inteiro', 'Gelados & Semifrios', 'un', '18.00', '6.50', '6', 'storable'),
    ('Bolo Gelado Napolitano — Inteiro', 'Gelados & Semifrios', 'un', '16.00', '5.50', '6', 'storable'),
    ('Gelado 1 Bola — un', 'Gelados & Semifrios', 'un', '1.80', '0.55', '6', 'storable'),
    ('Gelado 2 Bolas — un', 'Gelados & Semifrios', 'un', '3.20', '1.00', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # PRODUTOS ACABADOS ▸ Bolachas & Biscoitos
    # ──────────────────────────────────────────────────────────────────
    ('Bolacha de Manteiga — Saco 250 g', 'Bolachas & Biscoitos', 'g', '3.50', '1.10', '6', 'storable'),
    ('Bolacha de Aveia — Saco 250 g', 'Bolachas & Biscoitos', 'g', '3.80', '1.20', '6', 'storable'),
    ('Bolacha de Chocolate — Saco 250 g', 'Bolachas & Biscoitos', 'g', '4.00', '1.30', '6', 'storable'),
    ('Bolacha de Amêndoa — Saco 200 g', 'Bolachas & Biscoitos', 'g', '4.50', '1.50', '6', 'storable'),
    ('Bolacha de Gengibre — Saco 200 g', 'Bolachas & Biscoitos', 'g', '3.80', '1.20', '6', 'storable'),
    ('Biscoito de Nata (Shortbread) — Saco 250 g', 'Bolachas & Biscoitos', 'g', '4.20', '1.40', '6', 'storable'),
    ('Biscoito de Canela — Saco 200 g', 'Bolachas & Biscoitos', 'g', '3.50', '1.10', '6', 'storable'),
    ('Cookie Chocolate Chip — un', 'Bolachas & Biscoitos', 'un', '2.20', '0.70', '6', 'storable'),
    ('Cookie Double Chocolate — un', 'Bolachas & Biscoitos', 'un', '2.50', '0.80', '6', 'storable'),
    ('Cookie White Chocolate & Macadâmia — un', 'Bolachas & Biscoitos', 'un', '2.80', '0.95', '6', 'storable'),
    ('Cookie Aveia e Passas — un', 'Bolachas & Biscoitos', 'un', '2.20', '0.70', '6', 'storable'),
    ('Cookie Manteiga de Amendoim — un', 'Bolachas & Biscoitos', 'un', '2.50', '0.80', '6', 'storable'),
    ('Caixa Cookies Sortidos — 6 un', 'Bolachas & Biscoitos', 'cx', '11.00', '3.80', '6', 'storable'),
    ('Financier Clássico — un', 'Bolachas & Biscoitos', 'un', '2.00', '0.65', '6', 'storable'),
    ('Madeleine Clássica — un', 'Bolachas & Biscoitos', 'un', '1.80', '0.55', '6', 'storable'),
    ('Cantucci (Biscotti) — Saco 200 g', 'Bolachas & Biscoitos', 'g', '4.50', '1.50', '6', 'storable'),
    ('Langue de Chat — Saco 150 g', 'Bolachas & Biscoitos', 'g', '3.80', '1.20', '6', 'storable'),
    ('Tuile de Amêndoa — un', 'Bolachas & Biscoitos', 'un', '1.50', '0.45', '6', 'storable'),
    ('Sablé Breton — un', 'Bolachas & Biscoitos', 'un', '2.00', '0.65', '6', 'storable'),
    ('Caixa Bolachas Artesanais — 500 g', 'Bolachas & Biscoitos', 'g', '12.00', '4.00', '6', 'storable'),

    # ──────────────────────────────────────────────────────────────────
    # EMBALAGEM
    # ──────────────────────────────────────────────────────────────────
    ('Caixa Cartão Branca 20×20×10 cm — 50 un', 'Caixas de Cartão', 'un', '18.00', '12.50', '23', 'consumable'),
    ('Caixa Cartão Branca 25×25×12 cm — 50 un', 'Caixas de Cartão', 'un', '22.00', '15.50', '23', 'consumable'),
    ('Caixa Cartão Branca 30×30×15 cm — 50 un', 'Caixas de Cartão', 'un', '28.00', '19.50', '23', 'consumable'),
    ('Caixa Cartão Kraft 15×15×8 cm — 50 un', 'Caixas de Cartão', 'un', '15.00', '10.50', '23', 'consumable'),
    ('Caixa Cartão Pastel Nata 6 un — 100 un', 'Caixas de Cartão', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Caixa Cartão Cupcake 6 un — 25 un', 'Caixas de Cartão', 'un', '14.00', '9.80', '23', 'consumable'),
    ('Caixa Macarons 12 un — 25 un', 'Caixas de Cartão', 'un', '16.00', '11.20', '23', 'consumable'),
    ('Caixa Bolo Andar Único — 25 un', 'Caixas de Cartão', 'un', '25.00', '17.50', '23', 'consumable'),
    ('Caixa Premium c/ Janela — 25 un', 'Caixas de Cartão', 'un', '20.00', '14.00', '23', 'consumable'),
    ('Saco de Papel Branco Pequeno — 500 un', 'Sacos de Papel', 'un', '15.00', '10.50', '23', 'consumable'),
    ('Saco de Papel Branco Médio — 500 un', 'Sacos de Papel', 'un', '18.00', '12.50', '23', 'consumable'),
    ('Saco de Papel Kraft — 500 un', 'Sacos de Papel', 'un', '20.00', '14.00', '23', 'consumable'),
    ('Saco de Papel c/ Janela — 250 un', 'Sacos de Papel', 'un', '18.00', '12.50', '23', 'consumable'),
    ('Saco de Celofane Transparente — 500 un', 'Sacos de Papel', 'un', '10.00', '7.00', '23', 'consumable'),
    ('Forma Papel Redonda 18 cm — 100 un', 'Formas & Forminhas', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Forma Papel Redonda 22 cm — 100 un', 'Formas & Forminhas', 'un', '15.00', '10.50', '23', 'consumable'),
    ('Forma Papel Redonda 26 cm — 50 un', 'Formas & Forminhas', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Forminha Cupcake Standard — 500 un', 'Formas & Forminhas', 'un', '6.00', '4.20', '23', 'consumable'),
    ('Forminha Cupcake Mini — 500 un', 'Formas & Forminhas', 'un', '5.00', '3.50', '23', 'consumable'),
    ('Forminha Muffin Tulipa — 200 un', 'Formas & Forminhas', 'un', '8.00', '5.60', '23', 'consumable'),
    ('Formas Silicone Financier — Placa 8', 'Formas & Forminhas', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Fita Cetim Branca 15mm — Rolo 50m', 'Fitas & Laços', 'un', '5.50', '3.80', '23', 'consumable'),
    ('Fita Cetim Rosa 15mm — Rolo 50m', 'Fitas & Laços', 'un', '5.50', '3.80', '23', 'consumable'),
    ('Fita Cetim Dourada 15mm — Rolo 50m', 'Fitas & Laços', 'un', '6.00', '4.20', '23', 'consumable'),
    ('Fita Organza — Rolo 50m', 'Fitas & Laços', 'un', '4.50', '3.10', '23', 'consumable'),
    ('Laço Autocolante Dourado — 50 un', 'Fitas & Laços', 'un', '8.00', '5.60', '23', 'consumable'),
    ('Etiqueta Adesiva Redonda 5 cm — 500 un', 'Etiquetas & Rótulos', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Etiqueta c/ Fio "Artesanal" — 200 un', 'Etiquetas & Rótulos', 'un', '8.00', '5.60', '23', 'consumable'),
    ('Etiqueta Ingredientes (Legal) — 1000 un', 'Etiquetas & Rótulos', 'un', '15.00', '10.50', '23', 'consumable'),
    ('Etiqueta de Validade — 500 un', 'Etiquetas & Rótulos', 'un', '6.00', '4.20', '23', 'consumable'),
    ('Autocolante Logo Personalizado — 1000 un', 'Etiquetas & Rótulos', 'un', '25.00', '17.50', '23', 'consumable'),

    # ──────────────────────────────────────────────────────────────────
    # DECORAÇÃO
    # ──────────────────────────────────────────────────────────────────
    ('Pasta de Açúcar Branca — 2.5 kg', 'Pasta de Açúcar (Fondant)', 'kg', '12.00', '8.50', '6', 'storable'),
    ('Pasta de Açúcar Branca — 1 kg', 'Pasta de Açúcar (Fondant)', 'kg', '5.80', '4.10', '6', 'storable'),
    ('Pasta de Açúcar Branca — 250 g', 'Pasta de Açúcar (Fondant)', 'g', '2.50', '1.75', '6', 'storable'),
    ('Pasta de Açúcar Vermelha — 250 g', 'Pasta de Açúcar (Fondant)', 'g', '3.00', '2.10', '6', 'storable'),
    ('Pasta de Açúcar Preta — 250 g', 'Pasta de Açúcar (Fondant)', 'g', '3.20', '2.25', '6', 'storable'),
    ('Pasta de Açúcar Rosa — 250 g', 'Pasta de Açúcar (Fondant)', 'g', '3.00', '2.10', '6', 'storable'),
    ('Pasta de Açúcar Azul — 250 g', 'Pasta de Açúcar (Fondant)', 'g', '3.00', '2.10', '6', 'storable'),
    ('Kit 10 Cores Pasta de Açúcar — 10×100 g', 'Pasta de Açúcar (Fondant)', 'un', '14.00', '9.80', '6', 'storable'),
    ('Pasta de Modelar (Gumpaste) — 500 g', 'Pasta de Açúcar (Fondant)', 'g', '6.50', '4.60', '6', 'storable'),
    ('Glacê Real Pronto — 500 g', 'Glacê Real', 'g', '4.80', '3.40', '6', 'storable'),
    ('Glacê Real em Pó — 1 kg', 'Glacê Real', 'kg', '8.50', '6.00', '6', 'storable'),
    ('Cobertura Espelho (Mirror Glaze) Chocolate — 1 kg', 'Glacê Real', 'kg', '12.00', '8.50', '6', 'storable'),
    ('Cobertura Espelho Neutra — 1 kg', 'Glacê Real', 'kg', '10.00', '7.00', '6', 'storable'),
    ('Nappage Neutro (Geleia Brilho) — 1 kg', 'Glacê Real', 'kg', '6.50', '4.60', '6', 'storable'),
    ('Nappage Alperce — 1 kg', 'Glacê Real', 'kg', '7.00', '5.00', '6', 'storable'),
    ('Sprinkles Confetti Multicolor — 500 g', 'Sprinkles & Granulados', 'g', '5.50', '3.80', '6', 'storable'),
    ('Sprinkles Estrelas Douradas — 200 g', 'Sprinkles & Granulados', 'g', '4.50', '3.10', '6', 'storable'),
    ('Sprinkles Corações Rosa — 200 g', 'Sprinkles & Granulados', 'g', '4.50', '3.10', '6', 'storable'),
    ('Granulado Colorido (Jimmies) — 500 g', 'Sprinkles & Granulados', 'g', '4.00', '2.80', '6', 'storable'),
    ('Granulado de Chocolate — 500 g', 'Sprinkles & Granulados', 'g', '5.00', '3.50', '6', 'storable'),
    ('Pérolas de Açúcar Brancas — 200 g', 'Sprinkles & Granulados', 'g', '4.00', '2.80', '6', 'storable'),
    ('Pérolas de Açúcar Douradas — 200 g', 'Sprinkles & Granulados', 'g', '5.50', '3.80', '6', 'storable'),
    ('Vermicelli Coloridos — 500 g', 'Sprinkles & Granulados', 'g', '3.80', '2.65', '6', 'storable'),
    ('Meringue Kisses Sortidos — Caixa', 'Sprinkles & Granulados', 'un', '8.00', '3.00', '6', 'storable'),
    ('Folha de Ouro Comestível — 5 Folhas', 'Folha de Ouro / Prata', 'un', '12.00', '8.50', '23', 'consumable'),
    ('Folha de Prata Comestível — 5 Folhas', 'Folha de Ouro / Prata', 'un', '10.00', '7.00', '23', 'consumable'),
    ('Pó Dourado Comestível — 10 g', 'Folha de Ouro / Prata', 'g', '8.50', '6.00', '23', 'consumable'),
    ('Pó Prateado Comestível — 10 g', 'Folha de Ouro / Prata', 'g', '7.50', '5.30', '23', 'consumable'),
    ('Lustre Dourado Spray — 100 mL', 'Folha de Ouro / Prata', 'mL', '9.50', '6.70', '23', 'consumable'),
    ('Flores de Açúcar Rosas — 12 un', 'Flores Comestíveis', 'un', '8.50', '6.00', '6', 'consumable'),
    ('Flores de Açúcar Margaridas — 12 un', 'Flores Comestíveis', 'un', '7.50', '5.30', '6', 'consumable'),
    ('Flores Comestíveis Secas — 10 g', 'Flores Comestíveis', 'g', '6.50', '4.60', '6', 'consumable'),
    ('Pétalas de Rosa Cristalizadas — 50 g', 'Flores Comestíveis', 'g', '9.00', '6.40', '6', 'consumable'),
    ('Violetas Cristalizadas — 50 g', 'Flores Comestíveis', 'g', '9.50', '6.70', '6', 'consumable'),
    ('Wafer Paper (Papel de Arroz) A4 — 25 un', 'Flores Comestíveis', 'un', '8.00', '5.60', '6', 'consumable'),
    ('Impressão Comestível — Folha A4', 'Flores Comestíveis', 'un', '3.50', '2.45', '6', 'consumable'),
    ('Transfer de Chocolate — Folha', 'Flores Comestíveis', 'un', '4.50', '3.10', '6', 'consumable'),
    ('Molde Silicone Rosas — un', 'Moldes de Silicone', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Molde Silicone Folhas — un', 'Moldes de Silicone', 'un', '10.00', '7.00', '23', 'consumable'),
    ('Molde Silicone Letras e Números — un', 'Moldes de Silicone', 'un', '14.00', '9.80', '23', 'consumable'),
    ('Molde Silicone Esferas 3D — un', 'Moldes de Silicone', 'un', '15.00', '10.50', '23', 'consumable'),
    ('Molde Silicone Bombons — un', 'Moldes de Silicone', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Set Bicos Pasteleiro Inox — 12 un', 'Bicos de Pasteleiro', 'un', '15.00', '10.50', '23', 'consumable'),
    ('Set Bicos Pasteleiro Inox — 24 un', 'Bicos de Pasteleiro', 'un', '25.00', '17.50', '23', 'consumable'),
    ('Bico Pasteleiro Saint-Honoré — un', 'Bicos de Pasteleiro', 'un', '3.50', '2.45', '23', 'consumable'),
    ('Bico Pasteleiro Sultane — un', 'Bicos de Pasteleiro', 'un', '3.50', '2.45', '23', 'consumable'),
    ('Bico Pasteleiro Estrela Aberta — un', 'Bicos de Pasteleiro', 'un', '2.80', '1.95', '23', 'consumable'),
    ('Bico Pasteleiro Redondo Liso — un', 'Bicos de Pasteleiro', 'un', '2.50', '1.75', '23', 'consumable'),
    ('Bico Pasteleiro Folha — un', 'Bicos de Pasteleiro', 'un', '2.80', '1.95', '23', 'consumable'),
    ('Adaptador para Bicos — un', 'Bicos de Pasteleiro', 'un', '1.80', '1.25', '23', 'consumable'),

    # ──────────────────────────────────────────────────────────────────
    # UTENSÍLIOS & EQUIPAMENTO
    # ──────────────────────────────────────────────────────────────────
    ('Forma Redonda Antiaderente 18 cm', 'Formas de Forno', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Forma Redonda Antiaderente 22 cm', 'Formas de Forno', 'un', '15.00', '10.50', '23', 'consumable'),
    ('Forma Redonda Antiaderente 26 cm', 'Formas de Forno', 'un', '18.00', '12.60', '23', 'consumable'),
    ('Forma Redonda Desmontável 24 cm', 'Formas de Forno', 'un', '16.00', '11.20', '23', 'consumable'),
    ('Forma Quadrada 20×20 cm', 'Formas de Forno', 'un', '14.00', '9.80', '23', 'consumable'),
    ('Forma Rectangular 30×20 cm', 'Formas de Forno', 'un', '15.00', '10.50', '23', 'consumable'),
    ('Forma de Bundt (Savarin) — un', 'Formas de Forno', 'un', '22.00', '15.40', '23', 'consumable'),
    ('Forma de Tarte Canelada 28 cm', 'Formas de Forno', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Forma Loaf (Pão Inglês) — un', 'Formas de Forno', 'un', '10.00', '7.00', '23', 'consumable'),
    ('Set Formas Redondas 3 pcs', 'Formas de Forno', 'un', '35.00', '24.50', '23', 'consumable'),
    ('Tabuleiro Forno 60×40 cm Alumínio', 'Tabuleiros', 'un', '18.00', '12.60', '23', 'consumable'),
    ('Tabuleiro Forno 60×40 cm Perfurado', 'Tabuleiros', 'un', '22.00', '15.40', '23', 'consumable'),
    ('Tabuleiro Antiaderente 40×30 cm', 'Tabuleiros', 'un', '14.00', '9.80', '23', 'consumable'),
    ('Tapete Silicone 60×40 cm', 'Tabuleiros', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Tapete Silicone Macarons 40×30 cm', 'Tabuleiros', 'un', '8.00', '5.60', '23', 'consumable'),
    ('Grelha de Arrefecimento Inox', 'Tabuleiros', 'un', '10.00', '7.00', '23', 'consumable'),
    ('Espátula de Silicone Grande — un', 'Espátulas & Raspadeiras', 'un', '5.50', '3.80', '23', 'consumable'),
    ('Espátula de Silicone Pequena — un', 'Espátulas & Raspadeiras', 'un', '3.80', '2.65', '23', 'consumable'),
    ('Espátula Angular Inox 25 cm', 'Espátulas & Raspadeiras', 'un', '8.00', '5.60', '23', 'consumable'),
    ('Espátula Angular Inox 15 cm', 'Espátulas & Raspadeiras', 'un', '6.00', '4.20', '23', 'consumable'),
    ('Espátula Lisa Inox 30 cm', 'Espátulas & Raspadeiras', 'un', '9.00', '6.30', '23', 'consumable'),
    ('Raspadeira de Massa (Corne) — un', 'Espátulas & Raspadeiras', 'un', '2.50', '1.75', '23', 'consumable'),
    ('Raspadeira Inox — un', 'Espátulas & Raspadeiras', 'un', '4.50', '3.10', '23', 'consumable'),
    ('Set Alisadores Bolo — 3 pcs', 'Espátulas & Raspadeiras', 'un', '8.00', '5.60', '23', 'consumable'),
    ('Saco Pasteleiro Descartável 46 cm — 100 un', 'Sacos de Pasteleiro', 'un', '8.00', '5.60', '23', 'consumable'),
    ('Saco Pasteleiro Descartável 30 cm — 100 un', 'Sacos de Pasteleiro', 'un', '6.00', '4.20', '23', 'consumable'),
    ('Saco Pasteleiro Reutilizável Silicone — un', 'Sacos de Pasteleiro', 'un', '8.50', '5.95', '23', 'consumable'),
    ('Saco Pasteleiro Reutilizável Pano — un', 'Sacos de Pasteleiro', 'un', '6.00', '4.20', '23', 'consumable'),
    ('Termómetro Digital Culinário — un', 'Termómetros', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Termómetro Infravermelho — un', 'Termómetros', 'un', '25.00', '17.50', '23', 'consumable'),
    ('Termómetro de Chocolate — un', 'Termómetros', 'un', '18.00', '12.60', '23', 'consumable'),
    ('Termómetro de Forno — un', 'Termómetros', 'un', '8.00', '5.60', '23', 'consumable'),
    ('Balança Digital Precisão 0.1g — un', 'Balanças', 'un', '25.00', '17.50', '23', 'consumable'),
    ('Balança Digital 5kg — un', 'Balanças', 'un', '18.00', '12.60', '23', 'consumable'),
    ('Balança Comercial 15kg — un', 'Balanças', 'un', '85.00', '60.00', '23', 'consumable'),

    # ──────────────────────────────────────────────────────────────────
    # SERVIÇOS
    # ──────────────────────────────────────────────────────────────────
    ('Serviço de Decoração Personalizada — Hora', 'Produtos Acabados', 'h', '25.00', '15.00', '23', 'service'),
    ('Serviço Entrega Local (até 10 km)', 'Produtos Acabados', 'un', '5.00', '3.00', '23', 'service'),
    ('Serviço Entrega Regional (10-50 km)', 'Produtos Acabados', 'un', '15.00', '9.00', '23', 'service'),
    ('Consultoria Menu Eventos — Hora', 'Produtos Acabados', 'h', '35.00', '20.00', '23', 'service'),
    ('Workshop Pastelaria (por Pessoa)', 'Produtos Acabados', 'un', '45.00', '18.00', '23', 'service'),
    ('Montagem Bolo Casamento no Local', 'Produtos Acabados', 'un', '50.00', '25.00', '23', 'service'),
    ('Degustação Bolo Casamento — Sessão', 'Produtos Acabados', 'un', '25.00', '12.00', '23', 'service'),
    ('Aluguer Mesa de Doces — Evento', 'Produtos Acabados', 'un', '80.00', '35.00', '23', 'service'),

    # ──────────────────────────────────────────────────────────────────
    # EXTRAS — Produtos de suporte / consumíveis de produção
    # ──────────────────────────────────────────────────────────────────
    ('Papel Vegetal Rolo 50m', 'Utensílios & Equipamento', 'un', '5.50', '3.80', '23', 'consumable'),
    ('Película Aderente Profissional — Rolo 300m', 'Utensílios & Equipamento', 'un', '8.50', '5.95', '23', 'consumable'),
    ('Papel de Alumínio — Rolo 150m', 'Utensílios & Equipamento', 'un', '7.00', '4.90', '23', 'consumable'),
    ('Luvas Descartáveis Nitrilo M — Cx 100', 'Utensílios & Equipamento', 'cx', '8.00', '5.60', '23', 'consumable'),
    ('Luvas Descartáveis Nitrilo L — Cx 100', 'Utensílios & Equipamento', 'cx', '8.00', '5.60', '23', 'consumable'),
    ('Touca Descartável — Cx 100', 'Utensílios & Equipamento', 'cx', '5.00', '3.50', '23', 'consumable'),
    ('Avental Descartável — Cx 50', 'Utensílios & Equipamento', 'cx', '12.00', '8.40', '23', 'consumable'),
    ('Detergente Desengordurante — 5 L', 'Utensílios & Equipamento', 'L', '8.50', '5.95', '23', 'consumable'),
    ('Desinfetante Superfícies — 5 L', 'Utensílios & Equipamento', 'L', '9.50', '6.65', '23', 'consumable'),
    ('Álcool Alimentar 96° — 1 L', 'Utensílios & Equipamento', 'L', '6.00', '4.20', '23', 'consumable'),

    # ──────────────────────────────────────────────────────────────────
    # Mais matérias-primas diversas para chegar a ~1000
    # ──────────────────────────────────────────────────────────────────
    ('Caramelo Líquido Pronto — 1 kg', 'Matérias-Primas', 'kg', '5.50', '3.80', '6', 'storable'),
    ('Caramelo Salgado (Dulce de Leche) — 1 kg', 'Matérias-Primas', 'kg', '6.80', '4.80', '6', 'storable'),
    ('Creme Pasteleiro em Pó — 1 kg', 'Matérias-Primas', 'kg', '8.00', '5.70', '6', 'storable'),
    ('Base Mousse Chocolate — 2.5 kg', 'Matérias-Primas', 'kg', '12.50', '9.00', '6', 'storable'),
    ('Base Panna Cotta — 1 kg', 'Matérias-Primas', 'kg', '9.00', '6.40', '6', 'storable'),
    ('Preparado Crème Brûlée — 1 kg', 'Matérias-Primas', 'kg', '10.50', '7.50', '6', 'storable'),
    ('Preparado Chantilly Vegetal — 1 L', 'Matérias-Primas', 'L', '3.80', '2.65', '6', 'storable'),
    ('Massa Folhada Congelada — 10 kg', 'Matérias-Primas', 'kg', '5.50', '3.80', '6', 'storable'),
    ('Massa Quebrada Congelada — 5 kg', 'Matérias-Primas', 'kg', '6.00', '4.20', '6', 'storable'),
    ('Discos Massa Filo — Pct 500 g', 'Matérias-Primas', 'g', '4.50', '3.10', '6', 'storable'),
    ('Massa Brick — Pct 10 Folhas', 'Matérias-Primas', 'un', '3.50', '2.45', '6', 'storable'),
    ('Biscoitos Champagne (Palitos) — 500 g', 'Matérias-Primas', 'g', '5.50', '3.80', '6', 'storable'),
    ('Bolacha Maria Farinha — 1 kg', 'Matérias-Primas', 'kg', '3.50', '2.45', '6', 'storable'),
    ('Bolacha Oreo — 440 g', 'Matérias-Primas', 'g', '3.80', '2.65', '6', 'storable'),
    ('Bolacha Digestiva — 1 kg', 'Matérias-Primas', 'kg', '4.00', '2.80', '6', 'storable'),
    ('Nutella — 3 kg', 'Matérias-Primas', 'kg', '12.00', '8.50', '6', 'storable'),
    ('Nutella — 750 g', 'Matérias-Primas', 'g', '5.50', '3.80', '6', 'storable'),
    ('Doce de Leite Argentino — 1 kg', 'Matérias-Primas', 'kg', '7.50', '5.30', '6', 'storable'),
    ('Malte em Pó (Diastático) — 500 g', 'Matérias-Primas', 'g', '6.50', '4.60', '6', 'storable'),
    ('Melhorador de Pão — 1 kg', 'Matérias-Primas', 'kg', '8.00', '5.70', '6', 'storable'),
    ('Glúten Vital de Trigo — 1 kg', 'Matérias-Primas', 'kg', '6.50', '4.60', '6', 'storable'),
    ('Proteína de Soja Texturizada — 1 kg', 'Matérias-Primas', 'kg', '5.80', '4.10', '6', 'storable'),
    ('Tinta Comestível para Aerógrafo — 30 mL', 'Decoração', 'mL', '6.50', '4.60', '23', 'consumable'),
    ('Set Tintas Aerógrafo 8 Cores', 'Decoração', 'un', '35.00', '24.50', '23', 'consumable'),
    ('Pó de Cacau para Decoração — 250 g', 'Decoração', 'g', '4.50', '3.10', '6', 'consumable'),
    ('Palitos Decorativos "Feliz Aniversário" — 10 un', 'Decoração', 'un', '3.50', '2.45', '23', 'consumable'),
    ('Velas de Aniversário Glitter — 12 un', 'Decoração', 'un', '2.80', '1.95', '23', 'consumable'),
    ('Velas de Aniversário Números 0-9 — un', 'Decoração', 'un', '1.50', '1.05', '23', 'consumable'),
    ('Base Bolo Dourada Redonda 26 cm — 10 un', 'Decoração', 'un', '8.00', '5.60', '23', 'consumable'),
    ('Base Bolo Dourada Redonda 30 cm — 10 un', 'Decoração', 'un', '10.00', '7.00', '23', 'consumable'),
    ('Base Bolo Quadrada 30 cm — 10 un', 'Decoração', 'un', '12.00', '8.40', '23', 'consumable'),
    ('Suporte Bolo Rotativo (Prato Giratório)', 'Decoração', 'un', '22.00', '15.40', '23', 'consumable'),
    ('Stencil Decorativo Flores — un', 'Decoração', 'un', '5.50', '3.80', '23', 'consumable'),
    ('Stencil Decorativo Padrão Geométrico — un', 'Decoração', 'un', '5.50', '3.80', '23', 'consumable'),
    ('Caramelo em Folha — 10 Folhas', 'Decoração', 'un', '7.00', '4.90', '6', 'consumable'),
    ('Chocolate de Cobertura para Drip — 500 g', 'Decoração', 'g', '6.50', '4.60', '6', 'consumable'),
]


def run():
    company = Company.objects.filter(name__icontains='Fuet').first()
    if not company:
        company = Company.objects.first()

    if not company:
        print('❌  Nenhuma empresa encontrada. Crie uma empresa primeiro.')
        return

    print(f'Empresa: {company.name}\n')

    # ── Build lookup maps ────────────────────────────────────────────
    cat_map = {}
    for cat in Category.objects.filter(owner_company=company):
        cat_map[cat.name] = cat
    # Also include global categories (owner_company=None)
    for cat in Category.objects.filter(owner_company__isnull=True):
        if cat.name not in cat_map:
            cat_map[cat.name] = cat

    uom_map = {}
    for uom in UoM.objects.filter(owner_company__isnull=True):
        uom_map[uom.symbol] = uom
    # Company-specific UoMs
    for uom in UoM.objects.filter(owner_company=company):
        uom_map[uom.symbol] = uom

    print(f'  Categorias disponíveis: {len(cat_map)}')
    print(f'  UdMs disponíveis: {len(uom_map)}')
    print()

    # ── Clean existing products (+ dependent stock movements) ───────
    products_qs = Product.objects.filter(owner_company=company)
    if products_qs.exists():
        # Delete stock movement lines referencing these products first
        lines_deleted, _ = StockMovementLine.objects.filter(product__owner_company=company).delete()
        if lines_deleted:
            print(f'🗑️  Removidas {lines_deleted} linhas de movimento de stock dependentes.')
        # Delete now-empty or company-owned stock movements
        moves_deleted, _ = StockMovement.objects.filter(owner_company=company).delete()
        if moves_deleted:
            print(f'🗑️  Removidos {moves_deleted} movimentos de stock dependentes.')
        deleted, _ = products_qs.delete()
        print(f'🗑️  Removidos {deleted} produtos existentes.\n')

    # ── Create products ──────────────────────────────────────────────
    created = 0
    skipped = 0
    errors = []

    for i, (name, cat_name, uom_sym, sale, cost, tax, ptype) in enumerate(PRODUCTS, start=1):
        ref = f'{i:06d}'  # 000001, 000002, …

        # Resolve category
        category = cat_map.get(cat_name)
        if not category:
            errors.append(f'  ⚠️  Categoria não encontrada: "{cat_name}" (produto: {name})')
            skipped += 1
            continue

        # Resolve UoM
        uom = uom_map.get(uom_sym)
        if not uom:
            errors.append(f'  ⚠️  UdM não encontrada: "{uom_sym}" (produto: {name})')
            skipped += 1
            continue

        Product.objects.create(
            name=name,
            internal_reference=ref,
            product_type=ptype,
            category=category,
            uom=uom,
            sale_price=Decimal(sale),
            cost_price=Decimal(cost),
            tax_rate=Decimal(tax),
            owner_company=company,
        )
        created += 1

    # ── Summary ──────────────────────────────────────────────────────
    print(f'✅  Criados {created} produtos.')
    if skipped:
        print(f'⚠️  {skipped} produtos ignorados por erros:')
        for e in errors:
            print(e)

    total = Product.objects.filter(owner_company=company).count()
    print(f'\n📦 Total de produtos na empresa: {total}')


if __name__ == '__main__':
    run()
