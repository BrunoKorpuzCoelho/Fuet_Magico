"""
Management command: seed_historical_leads

Cria dados históricos de CRM — leads WON e LOST backdatadas mês a mês
para um número configurável de anos, de forma a alimentar o motor de
pontuação preditiva e geração de leads sazonais.

Uso:
    python manage.py seed_historical_leads
    python manage.py seed_historical_leads --years 5
    python manage.py seed_historical_leads --years 3 --per-month 8
    python manage.py seed_historical_leads --years 5 --clear
"""

import random
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import models as dj_models


LEAD_TITLES = [
    "Encomenda Bolo de Casamento — {contact}",
    "Fornecimento Doces para Evento — {contact}",
    "Parceria Bolos Corporativos — {contact}",
    "Encomenda Cupcakes Aniversário — {contact}",
    "Proposta Catering Pastelaria — {contact}",
    "Fornecimento Mensal Pastelaria — {contact}",
    "Bolos Personalizados Batizado — {contact}",
    "Encomenda Tarte Especial — {contact}",
    "Parceria Eventos Sazonais — {contact}",
    "Fornecimento Restaurante — {contact}",
    "Encomenda Brunch Empresarial — {contact}",
    "Proposta Aniversário Infantil — {contact}",
]

DESCRIPTIONS_WON = [
    "Negocio fechado com sucesso. Cliente aprovou proposta e assinou contrato.",
    "Venda confirmada. Cliente muito satisfeito com qualidade dos produtos.",
    "Deal encerrado. Primeira entrega realizada e cliente validou.",
    "Contrato assinado. Parceria de longo prazo estabelecida com sucesso.",
    "Proposta aceite. Pagamento efetuado e encomenda em produção.",
]

DESCRIPTIONS_LOST = [
    "Cliente escolheu concorrente por preço mais reduzido.",
    "Lost — cliente adiou projeto por razões orçamentais internas.",
    "Não fechou. Cliente preferiu fornecedor local já conhecido.",
    "Lost. Samples não aprovadas — preferência por outro estilo.",
    "Timing não estava certo para o cliente. Possível reabertura futura.",
]

DESCRIPTIONS_ACTIVE = [
    "Em negociação. Aguardando proposta atualizada.",
    "Meeting agendado. Cliente interessado e a aguardar amostras.",
    "Proposta enviada. Aguardando feedback sobre condições.",
    "Em análise interna pelo cliente. Follow-up esta semana.",
    "Cliente comparando alternativas. Demonstração marcada.",
]

LOST_REASONS = [
    "Preço acima do orçamento do cliente",
    "Cliente escolheu concorrente",
    "Prazo de entrega não adequado",
    "Projeto adiado indefinidamente",
    "Amostras não aprovadas",
]

SOURCES = ['WEBSITE', 'REFERRAL', 'COLD_CALL', 'SOCIAL_MEDIA', 'OTHER']
PRIORITIES = ['LOW', 'MEDIUM', 'HIGH']


class Command(BaseCommand):
    help = (
        "Cria leads históricas WON e LOST backdatadas mês a mês para alimentar "
        "o motor de pontuação preditiva e geração sazonal de leads."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--years', type=int, default=5,
            help='Quantos anos de histórico gerar (default: 5)',
        )
        parser.add_argument(
            '--per-month', type=int, default=5,
            help='Leads a criar por mês (default: 5; mín. 3 para ter WON+LOST)',
        )
        parser.add_argument(
            '--clear', action='store_true',
            help='Apaga todas as leads históricas (source != RETURNING) antes de gerar',
        )

    def handle(self, *args, **options):
        from apps.crm.models import Lead, CRMStage
        from apps.contacts.models import Contact
        from apps.core.models import Company
        from django.contrib.auth import get_user_model

        User = get_user_model()
        years = max(1, min(10, options['years']))
        per_month = max(3, options['per_month'])

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"\n{'=' * 60}\n  SEED HISTÓRICO CRM — {years} anos × 12 meses × {per_month} leads/mês"
            f"\n  Total estimado: {years * 12 * per_month} leads"
            f"\n{'=' * 60}\n"
        ))

        # ── Resolver company ────────────────────────────────────────────────
        # Prefer the company that owns WON/LOST stages; fallback to first active
        won_stage_any = CRMStage.objects.filter(is_active=True, is_won_stage=True).first()
        if won_stage_any and won_stage_any.owner_company:
            company = won_stage_any.owner_company
        else:
            company = Company.objects.filter(is_active=True).first()

        if not company:
            self.stdout.write(self.style.ERROR("❌  Nenhuma empresa encontrada. Cria uma primeiro."))
            return
        self.stdout.write(f"  Empresa: {company.name}")

        # ── Resolver stages ─────────────────────────────────────────────────
        company_q = dj_models.Q(owner_company__isnull=True) | dj_models.Q(owner_company=company)

        won_stage = CRMStage.objects.filter(is_active=True, is_won_stage=True).filter(company_q).first()
        lost_stage = CRMStage.objects.filter(is_active=True, is_lost_stage=True).filter(company_q).first()
        active_stages = list(
            CRMStage.objects.filter(
                is_active=True, is_won_stage=False, is_lost_stage=False
            ).filter(company_q).order_by('sequence')
        )

        if not won_stage or not lost_stage:
            self.stdout.write(self.style.ERROR(
                "❌  Estágios WON e/ou LOST não encontrados. "
                "Cria os estágios no CRM antes de executar este comando."
            ))
            return

        self.stdout.write(f"  Estágio WON:  {won_stage.name}")
        self.stdout.write(f"  Estágio LOST: {lost_stage.name}")
        self.stdout.write(f"  Estágios activos: {[s.name for s in active_stages]}")

        # ── Resolver utilizador ─────────────────────────────────────────────
        user = User.objects.filter(is_active=True, is_superuser=True).first() \
               or User.objects.filter(is_active=True).first()
        if not user:
            self.stdout.write(self.style.ERROR("❌  Nenhum utilizador encontrado."))
            return
        self.stdout.write(f"  Utilizador:   {user.username}\n")

        # ── Contactos disponíveis ────────────────────────────────────────────
        contacts = list(
            Contact.objects.filter(is_active=True)
            .filter(company_q)
            .order_by('?')[:200]
        )
        if not contacts:
            self.stdout.write(self.style.WARNING(
                "⚠️   Nenhum contacto encontrado. Leads serão criadas sem contacto."
            ))

        # ── Limpar (opcional) ────────────────────────────────────────────────
        if options['clear']:
            deleted, _ = Lead.objects.filter(
                owner_company=company,
                source__in=SOURCES,  # não apaga as RETURNING
            ).delete()
            self.stdout.write(self.style.WARNING(f"  🗑️   {deleted} leads apagadas.\n"))

        # ── Geração ──────────────────────────────────────────────────────────
        today = date.today()
        total_created = 0
        per_month_won  = max(1, per_month // 3)          # ~33% WON
        per_month_lost = max(1, per_month // 3)          # ~33% LOST
        per_month_active = per_month - per_month_won - per_month_lost  # resto activo

        for year_offset in range(1, years + 1):
            year_label = today.year - year_offset
            self.stdout.write(self.style.MIGRATE_LABEL(f"  Ano {year_label} (offset -{year_offset}):"))

            for month in range(1, 13):
                month_created = 0

                # Distribuição: WON, LOST, activos
                distribution = (
                    [(won_stage, 'WON')] * per_month_won
                    + [(lost_stage, 'LOST')] * per_month_lost
                    + [(random.choice(active_stages) if active_stages else won_stage, 'ACTIVE')]
                    * per_month_active
                )
                random.shuffle(distribution)

                for stage, kind in distribution:
                    # Data dentro do mês
                    day = random.randint(3, 26)
                    try:
                        lead_date = date(year_label, month, day)
                    except ValueError:
                        lead_date = date(year_label, month, 1)

                    # Nunca no futuro
                    if lead_date > today:
                        lead_date = today - timedelta(days=random.randint(1, 15))

                    contact = random.choice(contacts) if contacts else None
                    contact_name = contact.name if contact else f"Cliente {random.randint(100, 999)}"

                    title = random.choice(LEAD_TITLES).format(contact=contact_name)
                    estimated_value = Decimal(random.randint(200, 6000))

                    if kind == 'WON':
                        probability = 100
                        description = random.choice(DESCRIPTIONS_WON)
                        lost_reason = None
                        close_date = lead_date + timedelta(days=random.randint(3, 30))
                    elif kind == 'LOST':
                        probability = 0
                        description = random.choice(DESCRIPTIONS_LOST)
                        lost_reason = random.choice(LOST_REASONS)
                        close_date = lead_date + timedelta(days=random.randint(3, 30))
                    else:
                        # Active — só se ainda no passado recente
                        prob_map = {0: 10, 1: 25, 2: 45, 3: 70}
                        seq_idx = active_stages.index(stage) if stage in active_stages else 0
                        probability = prob_map.get(seq_idx, 30) + random.randint(-5, 10)
                        probability = max(5, min(95, probability))
                        description = random.choice(DESCRIPTIONS_ACTIVE)
                        lost_reason = None
                        close_date = lead_date + timedelta(days=random.randint(15, 90))

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
                        assigned_to=user,
                        lost_reason=lost_reason if kind == 'LOST' else None,
                        is_prospect=False,
                    )

                    # Backdate created_at (bypasses auto_now_add via update)
                    lead_dt = timezone.make_aware(
                        timezone.datetime(lead_date.year, lead_date.month, lead_date.day,
                                          random.randint(8, 18), random.randint(0, 59))
                    )
                    Lead.objects.filter(pk=lead.pk).update(
                        created_at=lead_dt,
                        updated_at=lead_dt,
                    )

                    total_created += 1
                    month_created += 1

                won_c  = sum(1 for s, k in distribution if k == 'WON')
                lost_c = sum(1 for s, k in distribution if k == 'LOST')
                actv_c = sum(1 for s, k in distribution if k == 'ACTIVE')
                self.stdout.write(
                    f"    {year_label}-{month:02d}: {month_created} leads "
                    f"(✅ {won_c} won · ❌ {lost_c} lost · 🔄 {actv_c} active)"
                )

        # ── Resumo ────────────────────────────────────────────────────────────
        self.stdout.write(self.style.SUCCESS(
            f"\n{'=' * 60}\n"
            f"  ✅  {total_created} leads históricas criadas com sucesso!\n"
            f"  💡  Agora vai a Definições → CRM → Recalcular Probabilidades\n"
            f"      para atualizar a pontuação preditiva com estes dados.\n"
            f"{'=' * 60}\n"
        ))
