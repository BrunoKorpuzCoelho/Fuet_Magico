"""
CRM Services — lógica de negócio isolada das views.
"""
from django.utils import timezone
from django.db import models as dj_models


def recalculate_stage_probabilities(company=None):
    """
    Recalcula a win_probability de cada estágio com base no histórico de leads.

    Lógica:
      Para cada estágio S com sequence P:
        - Pega todas as leads FECHADAS (ganhas ou perdidas) cujo estágio tem
          sequence >= P (i.e., leads que chegaram a esta fase ou passaram por ela).
        - win_probability = ganhas / (ganhas + perdidas) × 100

    Estágios won → 100%, estágios lost → 0%.

    Args:
        company: instância de Company ou None (calcula globalmente + por empresa)

    Returns:
        dict com slug do estágio → nova probabilidade
    """
    from .models import CRMStage, Lead, CRMConfig

    # Determina o conjunto de estágios a atualizar
    if company:
        stages_qs = CRMStage.objects.filter(
            dj_models.Q(owner_company__isnull=True) | dj_models.Q(owner_company=company),
            is_active=True
        )
    else:
        stages_qs = CRMStage.objects.filter(is_active=True)

    won_stages = list(stages_qs.filter(is_won_stage=True).values_list('id', flat=True))
    lost_stages = list(stages_qs.filter(is_lost_stage=True).values_list('id', flat=True))

    results = {}

    for stage in stages_qs:
        if stage.is_won_stage:
            new_prob = 100.0
        elif stage.is_lost_stage:
            new_prob = 0.0
        else:
            # Leads fechadas que chegaram a este nível ou além
            # (sequence do estágio delas >= sequence deste estágio)
            if company:
                closed_leads = Lead.objects.filter(
                    dj_models.Q(owner_company__isnull=True) | dj_models.Q(owner_company=company),
                    stage__sequence__gte=stage.sequence,
                    stage_id__in=(won_stages + lost_stages),
                )
            else:
                closed_leads = Lead.objects.filter(
                    stage__sequence__gte=stage.sequence,
                    stage_id__in=(won_stages + lost_stages),
                )

            total = closed_leads.count()
            if total == 0:
                # Sem histórico: probabilidade default progressiva por sequência
                # quanto mais avançado o estágio, maior a probabilidade base
                all_seqs = list(stages_qs.exclude(
                    is_won_stage=True
                ).exclude(
                    is_lost_stage=True
                ).order_by('sequence').values_list('sequence', flat=True))
                if all_seqs and len(all_seqs) > 1:
                    idx = all_seqs.index(stage.sequence) if stage.sequence in all_seqs else 0
                    new_prob = round(10 + (idx / (len(all_seqs) - 1)) * 80, 1)
                else:
                    new_prob = stage.win_probability  # mantém o atual
            else:
                won_count = closed_leads.filter(stage_id__in=won_stages).count()
                new_prob = round((won_count / total) * 100, 1)

        stage.win_probability = new_prob
        stage.save(update_fields=['win_probability'])
        results[stage.name] = new_prob

    # Atualiza a timestamp na config
    if company:
        config = CRMConfig.for_company(company)
        config.last_probability_update = timezone.now()
        config.save(update_fields=['last_probability_update'])

    return results


def apply_stage_probability_to_lead(lead):
    """
    Aplica a win_probability do estágio à lead, se:
    - predictive_scoring está ativo na config da empresa
    - probability_locked é False na lead
    - a lead não está num estágio won/lost (esses ficam em 100/0 fixos)
    """
    from .models import CRMConfig

    if lead.probability_locked:
        return

    stage = lead.stage
    if not stage:
        return

    # Estágios especiais: fixar probabilidade
    if stage.is_won_stage:
        if lead.probability != 100:
            lead.probability = 100
        return
    if stage.is_lost_stage:
        if lead.probability != 0:
            lead.probability = 0
        return

    # Verificar se predictive scoring está ativo para a empresa
    if lead.owner_company:
        config = CRMConfig.for_company(lead.owner_company)
        if not config.predictive_scoring:
            return

    # Aplicar a probabilidade histórica do estágio
    lead.probability = int(round(stage.win_probability))

def _seasonal_windows(years):
    """
    Retorna uma lista de tuplos (window_start, window_end) para cada ano de histórico.

    Para cada ano Y de 1 até `years`:
      - window_start = hoje - Y anos (mesmo mês/dia)
      - window_end   = window_start + 2 meses (~61 dias)

    Exemplo (hoje = 22/02/2026, years=2):
      Ano 1: 22/02/2025 → 22/04/2025
      Ano 2: 22/02/2024 → 22/04/2024
    """
    from django.utils import timezone
    from datetime import timedelta

    today = timezone.now().date()
    windows = []
    for y in range(1, years + 1):
        try:
            start = today.replace(year=today.year - y)
        except ValueError:
            # 29 de Fevereiro em ano não bissexto
            start = today.replace(year=today.year - y, day=28)
        end = start + timedelta(days=61)  # ~2 meses
        windows.append((start, end))
    return windows


def get_eligible_contacts(company, years=3):
    """
    Devolve a lista de contactos elegíveis para geração de leads — sem criar nada.

    Critérios de elegibilidade:
      1. Tem pelo menos uma lead GANHA dentro da janela sazonal (aniversário ±2 meses)
         em qualquer dos últimos `years` anos.
      2. NÃO tem nenhuma lead aberta no pipeline (não prospecta, não lost, não won).
      3. NÃO tem já um prospecto auto-gerado activo (source='RETURNING', is_prospect=True).

    Returns:
        list[dict] — cada dict tem: contact, contact_name, email_from, phone,
                     won_lead (a lead ganha mais recente), window_year (qual janela anual)
    """
    from .models import Lead, CRMStage
    from django.db import models as dj_models
    from django.utils import timezone

    company_q = dj_models.Q(owner_company__isnull=True) | dj_models.Q(owner_company=company)

    won_stages = list(
        CRMStage.objects.filter(is_active=True, is_won_stage=True).filter(company_q)
        .values_list('id', flat=True)
    )
    lost_stages = list(
        CRMStage.objects.filter(is_active=True, is_lost_stage=True).filter(company_q)
        .values_list('id', flat=True)
    )

    if not won_stages:
        return []

    windows = _seasonal_windows(years)

    # Leads ganhas dentro de qualquer janela sazonal
    window_q = dj_models.Q()
    for start, end in windows:
        window_q |= dj_models.Q(created_at__date__gte=start, created_at__date__lte=end)

    won_leads = (
        Lead.objects.filter(
            owner_company=company,
            is_active=True,
            stage_id__in=won_stages,
        )
        .filter(window_q)
        .select_related('contact')
        .order_by('-created_at')
    )

    # Indexar por contact_id (mais recente primeiro)
    contacts_seen = {}
    for lead in won_leads:
        if not lead.contact_id:
            continue
        if lead.contact_id not in contacts_seen:
            # Descobrir em que janela/ano cai
            lead_date = lead.created_at.date()
            year_match = None
            for idx, (start, end) in enumerate(windows, start=1):
                if start <= lead_date <= end:
                    year_match = idx
                    break
            contacts_seen[lead.contact_id] = {
                'contact': lead.contact,
                'contact_name': lead.contact_name or getattr(lead.contact, 'name', ''),
                'email_from': lead.email_from or getattr(lead.contact, 'email', ''),
                'phone': lead.phone or getattr(lead.contact, 'phone', ''),
                'won_lead': lead,
                'window_year': year_match,
            }

    if not contacts_seen:
        return []

    contact_ids = list(contacts_seen.keys())

    # Excluir contactos com lead aberta no pipeline
    contacts_in_pipeline = set(
        Lead.objects.filter(
            owner_company=company,
            is_active=True,
            is_prospect=False,
            contact_id__in=contact_ids,
        )
        .exclude(stage_id__in=lost_stages)
        .exclude(stage_id__in=won_stages)
        .values_list('contact_id', flat=True)
    )

    # Excluir contactos já com prospecto auto-gerado activo (evita duplicados entre runs)
    contacts_already_prospect = set(
        Lead.objects.filter(
            owner_company=company,
            is_active=True,
            is_prospect=True,
            source='RETURNING',
            contact_id__in=contact_ids,
        ).values_list('contact_id', flat=True)
    )

    excluded = contacts_in_pipeline | contacts_already_prospect

    return [
        info for cid, info in contacts_seen.items()
        if cid not in excluded
    ]


def generate_leads_from_history(company, years=3, user=None, limit=None):
    """
    Gera prospectos de seguimento para contactos elegíveis (ver get_eligible_contacts).

    Args:
        company: instância de Company
        years:   int — janela histórica (1-10)
        user:    User — assigned_to nas leads criadas
        limit:   int|None — máximo de leads a criar; None = todas elegíveis

    Returns:
        int — número de leads efectivamente criadas
    """
    from .models import CRMStage
    from django.db import models as dj_models

    company_q = dj_models.Q(owner_company__isnull=True) | dj_models.Q(owner_company=company)

    first_stage = (
        CRMStage.objects.filter(is_active=True, is_won_stage=False, is_lost_stage=False)
        .filter(company_q)
        .order_by('sequence')
        .first()
    )

    eligible = get_eligible_contacts(company, years)

    if limit is not None:
        try:
            eligible = eligible[:int(limit)]
        except (ValueError, TypeError):
            pass

    from .models import Lead

    created = 0
    for info in eligible:
        Lead.objects.create(
            owner_company=company,
            contact=info['contact'],
            contact_name=info['contact_name'],
            email_from=info['email_from'],
            phone=info['phone'],
            title=f"Seguimento — {info['contact_name']}",
            source='RETURNING',
            stage=first_stage,
            is_prospect=True,
            probability=10,
            assigned_to=user,
            description=(
                f"Lead gerada automaticamente (janela sazonal — "
                f"ano {info['window_year']} de {years})."
            ),
        )
        created += 1

    return created
