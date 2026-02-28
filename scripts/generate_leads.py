# -*- coding: utf-8 -*-
"""
Seed Demo: Gerar Leads
======================
Gera dados de demonstração para o CRM:
  1. ~1980 leads históricas backdatadas (33/mês × 60 meses = 5 anos)
  2. 15 leads por empresa ativa (5 WON, 5 LOST, 5 pipeline)

Apaga TODAS as leads existentes antes de gerar.

Uso:
    python manage.py seed --only demo_leads
    python scripts/generate_leads.py
"""

import os
import sys
import django
import random
from datetime import date, timedelta
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.crm.models import Lead, CRMStage, CRMTag
from apps.contacts.models import Contact
from apps.core.models import Company
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from faker import Faker

fake = Faker('pt_PT')
User = get_user_model()

# ── Títulos por tipo de empresa ───────────────────────────────────────────────

LEAD_TITLES_PASTRY = [
    'Encomenda Bolo de Casamento 3 andares',
    'Fornecimento Bolos Aniversário Mensal',
    'Parceria Eventos Corporativos',
    'Encomenda Doces Finos para Festa',
    'Bolos Personalizados Batizado',
    'Fornecimento Pastelaria para Hotel',
    'Encomenda Cupcakes Evento 200 pessoas',
    'Bolo Tema Infantil',
    'Parceria Catering Eventos',
    'Encomenda Bolos Premium',
    'Fornecimento Mensal Pastelaria',
    'Proposta Aniversário Infantil',
    'Encomenda Tarte Especial',
    'Parceria Eventos Sazonais',
    'Fornecimento Restaurante',
    'Encomenda Brunch Empresarial',
]

LEAD_TITLES_INGREDIENTS = [
    'Fornecimento Farinha Premium 500kg/mês',
    'Compra Chocolate Cobertura Belga',
    'Fornecimento Açúcar e Edulcorantes',
    'Parceria Matérias-Primas Orgânicas',
    'Compra Frutos Secos e Desidratados',
    'Fornecimento Aromas e Essências',
    'Compra Manteiga e Gorduras',
    'Fornecimento Frutas Congeladas',
    'Compra Fermento e Leveduras',
    'Parceria Ingredientes Importados',
]

LEAD_TITLES_PACKAGING = [
    'Fornecimento Caixas Bolos 1000un/mês',
    'Compra Embalagens Personalizadas',
    'Fornecimento Fitas e Laços Decorativos',
    'Parceria Embalagens Eco-Friendly',
    'Compra Sacos Papel Kraft',
    'Fornecimento Etiquetas Personalizadas',
    'Compra Tabuleiros e Bases Cartão',
    'Fornecimento Material Decoração',
    'Parceria Embalagens Premium',
    'Compra Caixas Cupcakes e Macarons',
]

LEAD_TITLES_GENERIC = [
    'Encomenda Bolo de Casamento — {contact}',
    'Fornecimento Doces para Evento — {contact}',
    'Parceria Bolos Corporativos — {contact}',
    'Encomenda Cupcakes Aniversário — {contact}',
    'Proposta Catering Pastelaria — {contact}',
    'Fornecimento Mensal Pastelaria — {contact}',
    'Bolos Personalizados Batizado — {contact}',
    'Encomenda Tarte Especial — {contact}',
    'Parceria Eventos Sazonais — {contact}',
    'Fornecimento Restaurante — {contact}',
    'Encomenda Brunch Empresarial — {contact}',
    'Proposta Aniversário Infantil — {contact}',
]

# ── Descrições ────────────────────────────────────────────────────────────────

DESCRIPTIONS_WON = [
    'Cliente muito satisfeito com proposta. Fechou contrato de 12 meses. Primeira entrega agendada.',
    'Negociação concluída com sucesso! Valores acordados, samples aprovadas. Contrato assinado.',
    'Excelente parceria estabelecida. Cliente aprovou qualidade e preços. Primeira encomenda paga.',
    'Deal fechado! Cliente gostou muito do atendimento e produtos. Parceria de longo prazo confirmada.',
    'Venda confirmada. Cliente satisfeito com condições comerciais. Início imediato.',
]

DESCRIPTIONS_LOST = [
    'Cliente escolheu concorrente por preço mais baixo. Feedback: qualidade boa mas preço alto.',
    'Lost para competitor local. Cliente preferiu fornecedor já conhecido.',
    'Não fechou: cliente adiou projeto por razões financeiras internas.',
    'Lost: cliente não aprovou samples. Preferiu outra marca.',
    'Não avançou: timing não estava certo para cliente. Pode reabrir no futuro.',
]

DESCRIPTIONS_ACTIVE = [
    'Cliente interessado. Aguardando envio de proposta comercial detalhada.',
    'Meeting agendado para próxima semana. Cliente quer ver samples.',
    'Em negociação de valores. Cliente pediu desconto para volume maior.',
    'Proposta enviada. Aguardando feedback do cliente sobre condições.',
    'Cliente gostou da apresentação. Em validação interna do budget.',
    'Follow-up agendado. Cliente comparando com outras opções.',
    'Demonstração marcada. Cliente muito interessado em qualidade.',
    'Em análise técnica. Cliente validando especificações dos produtos.',
]

LOST_REASONS = [
    'Preço acima do orçamento disponível pelo cliente',
    'Cliente escolheu concorrente com proposta mais competitiva',
    'Prazo de entrega não atende necessidade do cliente',
    'Cliente adiou projeto indefinidamente por questões internas',
    'Samples não aprovadas - cliente preferiu qualidade de outro fornecedor',
]

SOURCES = ['WEBSITE', 'REFERRAL', 'COLD_CALL', 'SOCIAL_MEDIA', 'OTHER']
PRIORITIES = ['LOW', 'MEDIUM', 'HIGH']


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_stages():
    """
    Lê os stages existentes na BD. NÃO cria nenhum stage novo.
    Devolve tuple (won_stage, lost_stage, pipeline_stages).
    Usa APENAS os flags is_won_stage / is_lost_stage — nunca nomes.
    """
    all_stages = list(CRMStage.objects.filter(is_active=True).order_by('sequence'))
    if not all_stages:
        raise RuntimeError(
            '❌ Nenhum stage CRM encontrado na BD!\n'
            '   Crie os estágios no admin antes de executar este script.'
        )

    won_stage = None
    lost_stage = None
    pipeline_stages = []

    for s in all_stages:
        if s.is_won_stage:
            won_stage = s
            print(f'  ✓ Stage WON: {s.name} (seq {s.sequence})')
        elif s.is_lost_stage:
            lost_stage = s
            print(f'  ✓ Stage LOST: {s.name} (seq {s.sequence})')
        else:
            pipeline_stages.append(s)
            print(f'  ✓ Stage pipeline: {s.name} (seq {s.sequence})')

    if not won_stage or not lost_stage:
        raise RuntimeError(
            '❌ Faltam stages WON e/ou LOST na BD!\n'
            '   Verifique que existe um stage com is_won_stage=True e outro com is_lost_stage=True.'
        )

    if not pipeline_stages:
        raise RuntimeError(
            '❌ Nenhum stage de pipeline encontrado!\n'
            '   Crie pelo menos 1 stage sem is_won_stage/is_lost_stage.'
        )

    pipeline_stages.sort(key=lambda s: s.sequence)
    print(f'  📊 {len(pipeline_stages)} pipeline stages + WON + LOST = {len(all_stages)} total')

    return won_stage, lost_stage, pipeline_stages


def get_title_for_company(company_name):
    """Devolve título aleatório adequado ao tipo de empresa."""
    if 'Fuet' in company_name or 'Mágico' in company_name:
        return random.choice(LEAD_TITLES_PASTRY)
    elif 'Ingrediente' in company_name or 'Doce' in company_name:
        return random.choice(LEAD_TITLES_INGREDIENTS)
    elif 'Embala' in company_name or 'Packaging' in company_name:
        return random.choice(LEAD_TITLES_PACKAGING)
    return random.choice(LEAD_TITLES_PASTRY)


def get_generic_title(contact_name):
    """Devolve título genérico com nome do contacto para leads históricas."""
    return random.choice(LEAD_TITLES_GENERIC).format(contact=contact_name)


# ── Configuração ──────────────────────────────────────────────────────────────

HISTORICAL_YEARS = 5        # 5 anos de histórico
HISTORICAL_PER_MONTH = 33   # 33 leads por mês → 33 × 60 = 1 980 leads
ACTIVE_PER_COMPANY = 15     # 15 leads por empresa ativa (5 WON + 5 LOST + 5 pipeline)
RECENT_MONTHS = 2           # últimos 2 meses → leads distribuídas pelos pipeline stages
HISTORICAL_WON_PER_MONTH = 25   # meses antigos: 25 WON
HISTORICAL_LOST_PER_MONTH = 8   # meses antigos: 8 LOST (33 - 25 = 8)


# ══════════════════════════════════════════════════════════════════════════════
# SECÇÃO 1: LEADS HISTÓRICAS (backdatadas)
# ══════════════════════════════════════════════════════════════════════════════

def generate_historical_leads(won_stage, lost_stage, pipeline_stages, contacts, users, company):
    """
    Gera HISTORICAL_PER_MONTH leads por mês durante HISTORICAL_YEARS anos,
    backdatadas de hoje para trás.

    Distribuição:
      - Meses antigos (> RECENT_MONTHS antes de hoje): 25 WON + 8 LOST = 33
      - Últimos RECENT_MONTHS meses: 33 divididos igualmente pelos pipeline stages
    """
    today = date.today()
    total_months = HISTORICAL_YEARS * 12
    total_created = 0

    # Calcular a data de corte: meses antigos vs recentes
    cutoff_date = date(today.year, today.month, 1) - timedelta(days=RECENT_MONTHS * 30)

    print(f'\n{"=" * 70}')
    print(f'📅 LEADS HISTÓRICAS — {HISTORICAL_YEARS} anos × {HISTORICAL_PER_MONTH}/mês = {total_months * HISTORICAL_PER_MONTH} leads')
    print(f'  Meses antigos (antes de {cutoff_date:%Y-%m}): {HISTORICAL_WON_PER_MONTH} WON + {HISTORICAL_LOST_PER_MONTH} LOST')
    print(f'  Meses recentes (últimos {RECENT_MONTHS}): {HISTORICAL_PER_MONTH} divididos por {len(pipeline_stages)} pipeline stages')
    print(f'{"=" * 70}')

    for month_offset in range(total_months, 0, -1):
        # Calcular ano e mês
        target_date = today - timedelta(days=month_offset * 30)
        year = target_date.year
        month = target_date.month

        try:
            first_day = date(year, month, 1)
        except ValueError:
            continue

        is_recent = first_day >= cutoff_date

        # ── Distribuição ──────────────────────────────────────────────
        if is_recent:
            # Últimos RECENT_MONTHS: dividir igualmente pelos pipeline stages
            n_pipeline = len(pipeline_stages)
            base_per_stage = HISTORICAL_PER_MONTH // n_pipeline
            remainder = HISTORICAL_PER_MONTH % n_pipeline

            distribution = []
            for i, ps in enumerate(pipeline_stages):
                count = base_per_stage + (1 if i < remainder else 0)
                distribution.extend([('PIPELINE', ps)] * count)
        else:
            # Meses antigos: 25 WON + 8 LOST
            distribution = (
                [('WON', won_stage)] * HISTORICAL_WON_PER_MONTH
                + [('LOST', lost_stage)] * HISTORICAL_LOST_PER_MONTH
            )

        random.shuffle(distribution)

        month_created = 0
        won_c = lost_c = pipe_c = 0

        for kind, stage in distribution:
            day = random.randint(1, 28)
            try:
                lead_date = date(year, month, day)
            except ValueError:
                lead_date = first_day

            if lead_date > today:
                lead_date = today - timedelta(days=random.randint(1, 10))

            contact = random.choice(contacts) if contacts else None
            contact_name = contact.name if contact else fake.name()

            title = get_generic_title(contact_name)
            estimated_value = Decimal(random.randint(200, 6000))

            if kind == 'WON':
                probability = 100
                description = random.choice(DESCRIPTIONS_WON)
                lost_reason = None
                close_date = lead_date + timedelta(days=random.randint(3, 30))
                won_c += 1
            elif kind == 'LOST':
                probability = 0
                description = random.choice(DESCRIPTIONS_LOST)
                lost_reason = random.choice(LOST_REASONS)
                close_date = lead_date + timedelta(days=random.randint(3, 30))
                lost_c += 1
            else:
                # PIPELINE — probabilidade baseada na posição do stage
                pos = pipeline_stages.index(stage) if stage in pipeline_stages else 0
                n = len(pipeline_stages)
                # Distribuir probabilidade linearmente: primeiro ~10%, último ~80%
                prob_base = 10 + int(70 * pos / max(n - 1, 1))
                probability = max(5, min(95, prob_base + random.randint(-5, 10)))
                description = random.choice(DESCRIPTIONS_ACTIVE)
                lost_reason = None
                close_date = lead_date + timedelta(days=random.randint(15, 90))
                pipe_c += 1

            lead = Lead.objects.create(
                owner_company=company,
                contact=contact,
                contact_name=contact_name,
                email_from=contact.email if contact and contact.email else '',
                phone=contact.phone if contact and contact.phone else '',
                title=title,
                description=description,
                estimated_value=estimated_value,
                probability=probability,
                priority=random.choice(PRIORITIES),
                stage=stage,
                source=random.choice(SOURCES),
                expected_close_date=close_date,
                assigned_to=random.choice(users),
                lost_reason=lost_reason,
                is_prospect=False,
            )

            # Backdate created_at / updated_at
            lead_dt = timezone.make_aware(
                timezone.datetime(lead_date.year, lead_date.month, lead_date.day,
                                  random.randint(8, 18), random.randint(0, 59))
            )
            Lead.objects.filter(pk=lead.pk).update(
                created_at=lead_dt,
                updated_at=lead_dt,
            )

            month_created += 1

        total_created += month_created

        if is_recent:
            print(
                f'  {year}-{month:02d}: {month_created} leads '
                f'(🔄 {pipe_c} pipeline — divididos por {len(pipeline_stages)} stages)'
            )
        else:
            print(
                f'  {year}-{month:02d}: {month_created} leads '
                f'(✅ {won_c} won · ❌ {lost_c} lost)'
            )

    print(f'\n  📊 Total históricas: {total_created} leads criadas')
    return total_created


# ══════════════════════════════════════════════════════════════════════════════
# SECÇÃO 2: LEADS POR EMPRESA (activas no pipeline)
# ══════════════════════════════════════════════════════════════════════════════

def generate_company_leads(won_stage, lost_stage, pipeline_stages, contacts, users, companies):
    """
    Gera ACTIVE_PER_COMPANY leads por empresa ativa.
    Distribui: 5 WON, 5 LOST, resto dividido igualmente pelos pipeline stages.
    Usa APENAS is_won_stage/is_lost_stage — nunca nomes.
    """
    total_created = 0
    n_pipeline = len(pipeline_stages)
    pipeline_count = ACTIVE_PER_COMPANY - 5 - 5  # 15 - 5 WON - 5 LOST = 5

    # Distribuir os 5 pipeline slots pelos stages existentes
    base_per_pipe = pipeline_count // n_pipeline
    remainder = pipeline_count % n_pipeline

    stage_distribution_template = (
        [won_stage] * 5
        + [lost_stage] * 5
    )
    for i, ps in enumerate(pipeline_stages):
        count = base_per_pipe + (1 if i < remainder else 0)
        stage_distribution_template.extend([ps] * count)

    for company in companies:
        print(f'\n{"─" * 60}')
        print(f'  🏢 {company.name} — {ACTIVE_PER_COMPANY} leads')
        print(f'{"─" * 60}')

        available_contacts = list(Contact.objects.filter(is_active=True)[:30])
        if not available_contacts:
            print(f'  ⚠️  Nenhum contacto disponível. A saltar.')
            continue

        distribution = list(stage_distribution_template)
        random.shuffle(distribution)

        for i in range(min(ACTIVE_PER_COMPANY, len(distribution))):
            contact = random.choice(available_contacts)
            stage = distribution[i]

            if stage.is_won_stage:
                probability = 100
                estimated_value = Decimal(random.randint(500, 5000))
                description = random.choice(DESCRIPTIONS_WON)
                lost_reason = None
                close_date = date.today() - timedelta(days=random.randint(1, 15))
            elif stage.is_lost_stage:
                probability = 0
                estimated_value = Decimal(random.randint(300, 3000))
                description = random.choice(DESCRIPTIONS_LOST)
                lost_reason = random.choice(LOST_REASONS)
                close_date = date.today() - timedelta(days=random.randint(1, 30))
            else:
                # Pipeline — probabilidade baseada na posição do stage
                pos = pipeline_stages.index(stage) if stage in pipeline_stages else 0
                n = len(pipeline_stages)
                prob_base = 10 + int(70 * pos / max(n - 1, 1))
                probability = max(5, min(95, prob_base + random.randint(-5, 10)))
                estimated_value = Decimal(random.randint(400, 4500))
                description = random.choice(DESCRIPTIONS_ACTIVE)
                lost_reason = None
                close_date = date.today() + timedelta(days=random.randint(7, 60))

            lead = Lead.objects.create(
                contact=contact,
                contact_name=contact.name,
                email_from=contact.email or fake.email(),
                phone=contact.phone or fake.phone_number(),
                title=get_title_for_company(company.name),
                description=description,
                estimated_value=estimated_value,
                probability=probability,
                priority=random.choice(PRIORITIES),
                stage=stage,
                source=random.choice(SOURCES),
                expected_close_date=close_date,
                assigned_to=random.choice(users),
                lost_reason=lost_reason,
                owner_company=company,
                notes=f'Lead criada automaticamente para {company.name}',
            )
            total_created += 1

            emoji = '🏆' if stage.is_won_stage else '❌' if stage.is_lost_stage else '🔄'
            print(f'  {emoji} {i+1:>2}/{ACTIVE_PER_COMPANY}: {lead.title[:45]}... [{stage.name}] €{estimated_value}')

    print(f'\n  📊 Total por empresa: {total_created} leads criadas')
    return total_created


# ══════════════════════════════════════════════════════════════════════════════
# RUNNER
# ══════════════════════════════════════════════════════════════════════════════

def run():
    print('=' * 70)
    print('🎯 GERAÇÃO DE LEADS DE DEMONSTRAÇÃO')
    print('=' * 70)

    # ── Verificações ────────────────────────────────────────────────────────
    print('\n📊 Verificando pré-requisitos...')

    # Stages (lê da BD — NÃO cria nenhum)
    won_stage, lost_stage, pipeline_stages = load_stages()

    # Contactos
    contacts_count = Contact.objects.filter(is_active=True).count()
    if contacts_count == 0:
        print('\n❌ ERRO: Nenhum contacto encontrado!')
        print('💡 Execute primeiro: python manage.py seed --only demo_contacts')
        return
    contacts = list(Contact.objects.filter(is_active=True).order_by('?')[:200])
    print(f'  ✓ {contacts_count} contactos disponíveis')

    # Utilizadores
    users = list(User.objects.filter(is_active=True))
    if not users:
        print('\n❌ ERRO: Nenhum utilizador encontrado!')
        print('💡 Execute primeiro: python manage.py seed --only default_users')
        return
    print(f'  ✓ {len(users)} utilizadores disponíveis')

    # Empresas
    companies = Company.objects.filter(is_active=True)
    if companies.count() == 0:
        print('\n❌ ERRO: Nenhuma empresa encontrada!')
        print('💡 Execute primeiro: python manage.py seed --only demo_companies')
        return
    print(f'  ✓ {companies.count()} empresas ativas')

    # ── Limpar TODAS as leads ───────────────────────────────────────────────
    existing = Lead.objects.count()
    print(f'\n🗑️  Apagando {existing} leads existentes...')
    Lead.objects.all().delete()
    print(f'  ✓ {existing} leads removidas')

    # ── Empresa principal (para leads históricas) ───────────────────────────
    # Preferir "Fuet Mágico"; fallback para a primeira empresa ativa
    primary_company = (
        companies.filter(name__icontains='fuet').first()
        or companies.filter(name__icontains='mágico').first()
        or companies.first()
    )
    print(f'\n  Empresa principal (históricas): {primary_company.name}')

    # ── 1. Gerar leads históricas ───────────────────────────────────────────
    hist_count = generate_historical_leads(won_stage, lost_stage, pipeline_stages, contacts, users, primary_company)

    # ── 2. Gerar leads por empresa ──────────────────────────────────────────
    print(f'\n{"=" * 70}')
    print(f'🏢 LEADS POR EMPRESA — {ACTIVE_PER_COMPANY} por empresa × {companies.count()} empresas')
    print(f'{"=" * 70}')
    company_count = generate_company_leads(won_stage, lost_stage, pipeline_stages, contacts, users, companies)

    # ── Resumo final ────────────────────────────────────────────────────────
    total = hist_count + company_count
    print(f'\n{"=" * 70}')
    print(f'📊 RESUMO FINAL')
    print(f'{"=" * 70}')
    print(f'  📅 Leads históricas ({HISTORICAL_YEARS} anos): {hist_count}')
    print(f'  🏢 Leads por empresa ({ACTIVE_PER_COMPANY}/empresa):  {company_count}')
    print(f'  📝 TOTAL: {total} leads')
    print()
    print(f'  Distribuição por estágio:')
    for stage in CRMStage.objects.all().order_by('sequence'):
        count = Lead.objects.filter(stage=stage).count()
        total_value = Lead.objects.filter(stage=stage).aggregate(
            total=models.Sum('estimated_value')
        )['total'] or 0
        print(f'    • {stage.name}: {count} leads (€{total_value:,.2f})')
    print(f'\n{"=" * 70}')
    print('✅ Geração de leads concluída com sucesso!')
    print(f'{"=" * 70}')
    print(f'\n💡 Acesse: http://127.0.0.1:8000/crm/leads/')


if __name__ == '__main__':
    run()
