"""
seed_product_categories.py
--------------------------
Seed demo product categories for a pastelaria / bakery business.

Creates a realistic hierarchy of ingredient and product categories
with parent-child relationships.

Run:
  python scripts/seed_product_categories.py
"""

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.inventory.models import Category
from apps.core.models import Company


# ── Category tree ────────────────────────────────────────────────────
# Format: { 'Parent': ['Child1', 'Child2', ...] }
# Top-level categories have None as parent.
TREE = {
    # ── Matérias-Primas (ingredientes base) ──────────────────────────
    'Matérias-Primas': [
        'Farinhas',
        'Açúcares & Adoçantes',
        'Gorduras & Óleos',
        'Ovos & Derivados',
        'Leite & Lacticínios',
        'Fermento & Leveduras',
        'Cacau & Chocolate',
        'Frutos Secos & Sementes',
        'Frutas & Polpas',
        'Aromas & Extratos',
        'Corantes & Aditivos',
        'Sal & Especiarias',
    ],

    # sub-subcategorias de Farinhas
    'Farinhas': [
        'Farinha de Trigo T55',
        'Farinha de Trigo T65',
        'Farinha de Trigo T150 (Integral)',
        'Farinha de Amêndoa',
        'Farinha de Arroz',
        'Farinha de Centeio',
        'Fécula de Batata',
        'Amido de Milho (Maizena)',
    ],

    # sub-subcategorias de Açúcares
    'Açúcares & Adoçantes': [
        'Açúcar Branco',
        'Açúcar em Pó (Glacé)',
        'Açúcar Mascavado',
        'Mel',
        'Glucose Líquida',
        'Açúcar Invertido',
    ],

    # sub-subcategorias de Cacau & Chocolate
    'Cacau & Chocolate': [
        'Chocolate Negro (70%+)',
        'Chocolate de Leite',
        'Chocolate Branco',
        'Cacau em Pó',
        'Manteiga de Cacau',
        'Pepitas de Chocolate',
    ],

    # sub-subcategorias de Gorduras
    'Gorduras & Óleos': [
        'Manteiga sem Sal',
        'Manteiga com Sal',
        'Margarina de Folhar',
        'Óleo de Girassol',
        'Azeite',
        'Natas',
    ],

    # ── Produtos Acabados ────────────────────────────────────────────
    'Produtos Acabados': [
        'Bolos Tradicionais',
        'Bolos Decorados',
        'Tartes & Tortas',
        'Pastelaria Fina',
        'Folhados',
        'Pão & Pão Especial',
        'Sobremesas Individuais',
        'Gelados & Semifrios',
        'Bolachas & Biscoitos',
    ],

    # sub-subcategorias de Bolos Tradicionais
    'Bolos Tradicionais': [
        'Bolo de Chocolate',
        'Bolo de Laranja',
        'Bolo de Cenoura',
        'Bolo Mármore',
        'Pão-de-Ló',
        'Bolo Inglês',
    ],

    # sub-subcategorias de Bolos Decorados
    'Bolos Decorados': [
        'Bolos de Aniversário',
        'Bolos de Casamento',
        'Bolos Temáticos',
        'Cupcakes',
        'Cake Pops',
    ],

    # sub-subcategorias de Pastelaria Fina
    'Pastelaria Fina': [
        'Éclairs',
        'Profiteroles',
        'Mil-Folhas',
        'Macarons',
        'Croissants',
        'Palmiers',
    ],

    # sub-subcategorias de Tartes
    'Tartes & Tortas': [
        'Tarte de Nata',
        'Tarte de Amêndoa',
        'Tarte de Frutas',
        'Cheesecake',
        'Tarte de Chocolate',
    ],

    # ── Embalagem ────────────────────────────────────────────────────
    'Embalagem': [
        'Caixas de Cartão',
        'Sacos de Papel',
        'Formas & Forminhas',
        'Fitas & Laços',
        'Etiquetas & Rótulos',
    ],

    # ── Decoração ────────────────────────────────────────────────────
    'Decoração': [
        'Pasta de Açúcar (Fondant)',
        'Glacê Real',
        'Sprinkles & Granulados',
        'Folha de Ouro / Prata',
        'Flores Comestíveis',
        'Moldes de Silicone',
        'Bicos de Pasteleiro',
    ],

    # ── Utensílios & Equipamento ─────────────────────────────────────
    'Utensílios & Equipamento': [
        'Formas de Forno',
        'Tabuleiros',
        'Espátulas & Raspadeiras',
        'Sacos de Pasteleiro',
        'Termómetros',
        'Balanças',
    ],
}

# Descriptions for top-level categories
DESCRIPTIONS = {
    'Matérias-Primas': 'Ingredientes base utilizados na produção de pastelaria e padaria.',
    'Produtos Acabados': 'Produtos finais prontos para venda ao cliente.',
    'Embalagem': 'Materiais de embalagem e apresentação dos produtos.',
    'Decoração': 'Itens decorativos e ferramentas de acabamento para pastelaria.',
    'Utensílios & Equipamento': 'Ferramentas, utensílios e equipamento de produção.',
}

TOP_LEVEL = [
    'Matérias-Primas',
    'Produtos Acabados',
    'Embalagem',
    'Decoração',
    'Utensílios & Equipamento',
]


def run():
    company = Company.objects.filter(name__icontains='Fuet').first()
    if not company:
        company = Company.objects.first()
    print(f"Empresa: {company.name}\n")

    # Clean existing demo categories for this company
    deleted, _ = Category.objects.filter(owner_company=company).delete()
    if deleted:
        print(f"🗑️  Removidas {deleted} categorias existentes.\n")

    created = 0
    cat_map = {}  # name → Category instance

    # 1. Create top-level categories
    for name in TOP_LEVEL:
        cat = Category.objects.create(
            name=name,
            description=DESCRIPTIONS.get(name, ''),
            parent=None,
            owner_company=company,
        )
        cat_map[name] = cat
        created += 1
        print(f"  ✅ {name}")

    # 2. Create children (and grandchildren)
    def create_children(parent_name):
        nonlocal created
        children = TREE.get(parent_name, [])
        parent = cat_map[parent_name]
        for child_name in children:
            cat = Category.objects.create(
                name=child_name,
                description='',
                parent=parent,
                owner_company=company,
            )
            cat_map[child_name] = cat
            created += 1
            print(f"    └─ {child_name}")
            # Check for grandchildren
            if child_name in TREE:
                for gc_name in TREE[child_name]:
                    gc = Category.objects.create(
                        name=gc_name,
                        description='',
                        parent=cat,
                        owner_company=company,
                    )
                    cat_map[gc_name] = gc
                    created += 1
                    print(f"       └─ {gc_name}")

    for top in TOP_LEVEL:
        create_children(top)

    print(f"\n🎉 Criadas {created} categorias de produto.")


if __name__ == '__main__':
    run()
