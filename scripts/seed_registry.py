# -*- coding: utf-8 -*-
"""
Seed Registry — Registo central de todos os seeds do sistema.

Cada seed é classificado como:
  ESSENTIAL — dados necessários para a aplicação funcionar em produção
  DEMO      — dados de teste/demonstração para desenvolvimento

Uso via management command:
  python manage.py seed --essential        # Produção: só dados obrigatórios
  python manage.py seed --demo             # Adiciona dados de demonstração
  python manage.py seed --all              # Tudo (essential + demo)
  python manage.py seed --list             # Mostra registro de seeds
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional


# ── Categorias ────────────────────────────────────────────────────────────────

class SeedCategory(str, Enum):
    ESSENTIAL = 'essential'
    DEMO = 'demo'


# ── Seed entry ────────────────────────────────────────────────────────────────

@dataclass
class SeedEntry:
    """Registo de um seed no sistema."""
    key: str                         # identificador único (ex: 'activity_templates')
    name: str                        # nome legível (ex: 'Blueprints de Atividades')
    category: SeedCategory           # ESSENTIAL ou DEMO
    order: int                       # ordem de execução (menor = primeiro)
    runner: str                      # caminho dotted para a função run() ou management command
    is_management_command: bool = False
    description: str = ''
    dependencies: list = field(default_factory=list)
    destructive: bool = False        # True = apaga dados existentes antes de inserir


# ── Registry ──────────────────────────────────────────────────────────────────

SEEDS: list[SeedEntry] = [

    # ╔══════════════════════════════════════════════════════════════════╗
    # ║  ESSENTIAL — Dados obrigatórios para produção                  ║
    # ╚══════════════════════════════════════════════════════════════════╝

    SeedEntry(
        key='default_company',
        name='Empresa Default',
        category=SeedCategory.ESSENTIAL,
        order=10,
        runner='create_default_company',
        is_management_command=True,
        description='Cria a empresa "Fuet Mágico" se não existir.',
    ),

    SeedEntry(
        key='default_users',
        name='Utilizadores Default',
        category=SeedCategory.ESSENTIAL,
        order=20,
        runner='create_default_users',
        is_management_command=True,
        description='Cria utilizadores admin (cubix) e manager (daisy).',
        dependencies=['default_company'],
    ),

    SeedEntry(
        key='activity_templates',
        name='Blueprints de Atividades',
        category=SeedCategory.ESSENTIAL,
        order=30,
        runner='setup_activity_templates',
        is_management_command=True,
        description='Cria 21 blueprints de atividades (calls, emails, todos, WhatsApp, docs, assinaturas).',
    ),

    SeedEntry(
        key='activity_chains',
        name='Cadeias de Automação',
        category=SeedCategory.ESSENTIAL,
        order=40,
        runner='scripts.seed_activity_chains',
        description='Cria 7 cadeias de automação para Leads e Contactos.',
        dependencies=['activity_templates'],
    ),

    SeedEntry(
        key='app_roles',
        name='Roles Aplicacionais',
        category=SeedCategory.ESSENTIAL,
        order=50,
        runner='scripts.seed_app_roles',
        description='Backfill de AppRole para todos os utilizadores existentes.',
        dependencies=['default_users'],
    ),

    SeedEntry(
        key='email_layout',
        name='Layout de Email (Envelope)',
        category=SeedCategory.ESSENTIAL,
        order=60,
        runner='scripts.seed_email_layout',
        description='Cria o registo global de EmailLayout a partir do ficheiro default.',
    ),

    SeedEntry(
        key='email_templates',
        name='Templates de Email',
        category=SeedCategory.ESSENTIAL,
        order=70,
        runner='scripts.seed_email_templates',
        description='Cria templates de email BASE do sistema (ex: Email de Agradecimento).',
        dependencies=['email_layout'],
    ),

    # ╔══════════════════════════════════════════════════════════════════╗
    # ║  DEMO — Dados de teste / demonstração                         ║
    # ╚══════════════════════════════════════════════════════════════════╝

    SeedEntry(
        key='demo_companies',
        name='Empresas de Demonstração',
        category=SeedCategory.DEMO,
        order=100,
        runner='scripts.setup_companies',
        description='Cria 3 empresas (Fuet Mágico, Doce Ingrediente, Embala+) e associa a utilizadores.',
        dependencies=['default_users'],
    ),

    SeedEntry(
        key='demo_contacts',
        name='Contactos de Demonstração',
        category=SeedCategory.DEMO,
        order=110,
        runner='scripts.generate_contacts',
        description='Gera 100 contactos falsos (20 empresas, 40 pessoas, 40 colaboradores) com Faker.',
        destructive=True,
    ),

    SeedEntry(
        key='demo_leads',
        name='Leads de Demonstração',
        category=SeedCategory.DEMO,
        order=120,
        runner='scripts.generate_leads',
        description='Gera ~1980 leads históricas (5 anos) + 15 por empresa ativa. Apaga tudo antes.',
        dependencies=['demo_companies', 'demo_contacts'],
        destructive=True,
    ),

    SeedEntry(
        key='demo_notifications',
        name='Notificações de Demonstração',
        category=SeedCategory.DEMO,
        order=130,
        runner='seed_notifications',
        is_management_command=True,
        description='Cria 12 notificações fake para o utilizador cubix.',
        dependencies=['default_users'],
    ),
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_seeds(category: Optional[SeedCategory] = None) -> list[SeedEntry]:
    """Devolve seeds filtrados por categoria, ordenados por `order`."""
    entries = sorted(SEEDS, key=lambda s: s.order)
    if category:
        entries = [s for s in entries if s.category == category]
    return entries


def get_essential_seeds() -> list[SeedEntry]:
    return get_seeds(SeedCategory.ESSENTIAL)


def get_demo_seeds() -> list[SeedEntry]:
    return get_seeds(SeedCategory.DEMO)


def get_seed_by_key(key: str) -> Optional[SeedEntry]:
    for s in SEEDS:
        if s.key == key:
            return s
    return None
