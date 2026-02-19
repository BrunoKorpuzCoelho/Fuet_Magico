# -*- coding: utf-8 -*-
"""
Seed: Cadeias de Atividade
Cria 7 cadeias de automação para Leads e Contactos.

Uso:
    python manage.py shell -c "exec(open('scripts/seed_activity_chains.py', encoding='utf-8').read())"
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from apps.core.models import ActivityChain, ActivityChainStep, ScheduledActivity

# ─── Mapa de UUIDs dos blueprints ────────────────────────────────────────────
BP = {
    # Documents
    "fatura":           "04b31967-be65-4f89-a812-5f08f843549c",
    "recolher_docs":    "1226bf69-de38-4a37-8573-4ba4e68bab99",
    "upload_cert":      "becff0b5-93d7-41bc-be96-2630796a6dff",
    # Email
    "email_agradec":    "4f491102-7a8f-4bd3-9cfb-7608c1d4b9df",
    "email_boasvindas": "53c9982b-2d40-4a3a-b91b-fe94c89bffae",
    "email_followup":   "26743d37-6262-4f67-9522-cd24ef7464aa",
    "email_proposta":   "bdc06368-8e98-4ad5-8cb4-7d338dbe52cc",
    # Phone Call
    "callback":         "ef0850e8-efa8-40d1-8a02-61163c4c1fae",
    "ligacao_followup": "399f6cad-acc5-441a-9b84-142aef1088f7",
    "primeira_ligacao": "58acd619-ab13-476f-92c1-d3b2d62364b1",
    "retry":            "7489f944-e80d-49cb-a4af-9639f4c046ba",
    # Signature
    "assinar_acordo":   "7a7d38b7-a8ad-40f9-a54d-3509ad8b70b8",
    "assinar_contrato": "a4ed927f-32de-4c89-8a50-571c357e32b7",
    "assinar_nda":      "70b66ce5-2a12-4f9c-ba5f-bdacc1a21009",
    # To-Do
    "atualizar_crm":    "b66e1bd2-49e1-47c9-aeba-7a6ac2fbcc94",
    "enviar_contrato":  "aa01a97e-37cc-4963-8509-4c11dffe22d7",
    "pesquisar_cli":    "70d413c3-0b5f-4892-8c9a-b315bc95df6a",
    "preparar_prop":    "9d8f8818-c741-46a4-916a-c6cd687ac9bd",
    # WhatsApp
    "wa_followup":      "bc0071b1-4cd5-4e80-a462-bfe10e99706d",
    "wa_lembrete":      "3c10e011-4edf-49ab-aae8-6bc4a75def17",
    "wa_docs":          "2803cfd5-e445-4dab-a9d1-b6e878b71709",
}

# Helpers de conversão (delay_days guarda minutos internamente)
def dias(n):    return n * 1440
def horas(n):   return n * 60
def minutos(n): return n


# ─── Definição das cadeias ────────────────────────────────────────────────────
# Cada passo: (blueprint_key, delay, on_failure_key, on_failure_delay)
# on_failure_key=None → sem ação de insucesso

CHAINS = [

    # 1. Nova Lead — Qualificação Inicial
    {
        "name": "Nova Lead — Qualificação Inicial",
        "description": "Fluxo de entrada para qualquer nova lead: pesquisa, primeiro contacto telefónico e registo no CRM.",
        "applicable_model": "lead",
        "steps": [
            ("pesquisar_cli",    dias(0),   None,             dias(0)),
            ("primeira_ligacao", dias(1),   "retry",          dias(1)),
            ("email_boasvindas", dias(1),   None,             dias(0)),
            ("atualizar_crm",    horas(2),  None,             dias(0)),
        ],
    },

    # 2. Prospecção Fria (Cold Outreach)
    {
        "name": "Prospecção Fria (Cold Outreach)",
        "description": "Sequência de contacto para leads frias: email, ligação e WhatsApp com retries automáticos.",
        "applicable_model": "lead",
        "steps": [
            ("pesquisar_cli",    dias(0),   None,             dias(0)),
            ("email_followup",   dias(2),   "wa_followup",    dias(1)),
            ("primeira_ligacao", dias(3),   "retry",          dias(1)),
            ("ligacao_followup", dias(5),   "wa_followup",    dias(1)),
            ("atualizar_crm",    dias(1),   None,             dias(0)),
        ],
    },

    # 3. Apresentação de Proposta Comercial
    {
        "name": "Apresentação de Proposta Comercial",
        "description": "Prepara e envia proposta, faz follow-up por telefone e WhatsApp até obter resposta.",
        "applicable_model": "lead",
        "steps": [
            ("preparar_prop",    dias(0),   None,             dias(0)),
            ("email_proposta",   dias(1),   None,             dias(0)),
            ("ligacao_followup", dias(3),   "wa_followup",    dias(1)),
            ("wa_followup",      dias(5),   "ligacao_followup", dias(2)),
            ("atualizar_crm",    dias(1),   None,             dias(0)),
        ],
    },

    # 4. Fecho de Negócio e Contrato
    {
        "name": "Fecho de Negócio e Contrato",
        "description": "Envio de contrato, recolha de documentos, processamento de fatura e agradecimento ao cliente.",
        "applicable_model": "lead",
        "steps": [
            ("enviar_contrato",  dias(0),   None,             dias(0)),
            ("assinar_contrato", dias(2),   "ligacao_followup", dias(1)),
            ("recolher_docs",    dias(1),   "wa_docs",        dias(1)),
            ("fatura",           dias(2),   None,             dias(0)),
            ("email_agradec",    minutos(0),None,             dias(0)),
            ("atualizar_crm",    horas(1),  None,             dias(0)),
        ],
    },

    # 5. Follow-up Pós-Reunião
    {
        "name": "Follow-up Pós-Reunião",
        "description": "Após uma reunião: actualiza o CRM, envia agradecimento, proposta e faz follow-up de fecho.",
        "applicable_model": "lead",
        "steps": [
            ("atualizar_crm",    minutos(0),None,             dias(0)),
            ("email_agradec",    horas(1),  None,             dias(0)),
            ("email_proposta",   dias(2),   None,             dias(0)),
            ("ligacao_followup", dias(5),   "wa_followup",    dias(1)),
            ("atualizar_crm",    dias(2),   None,             dias(0)),
        ],
    },

    # 6. Onboarding de Novo Cliente
    {
        "name": "Onboarding de Novo Cliente",
        "description": "Fluxo completo de boas-vindas, recolha de documentos e assinatura de acordos para novos clientes.",
        "applicable_model": "contact",
        "steps": [
            ("email_boasvindas", minutos(0),None,             dias(0)),
            ("wa_docs",          dias(2),   "ligacao_followup", dias(1)),
            ("recolher_docs",    dias(3),   None,             dias(0)),
            ("upload_cert",      dias(2),   None,             dias(0)),
            ("assinar_nda",      dias(1),   "callback",       dias(1)),
            ("assinar_acordo",   dias(2),   None,             dias(0)),
            ("atualizar_crm",    minutos(0),None,             dias(0)),
        ],
    },

    # 7. Reactivação de Lead Fria
    {
        "name": "Reactivação de Lead Fria",
        "description": "Tenta reactivar leads que estagnaram: email, WhatsApp, ligação e nova proposta.",
        "applicable_model": "lead",
        "steps": [
            ("email_followup",   minutos(0),None,             dias(0)),
            ("wa_followup",      dias(3),   None,             dias(0)),
            ("callback",         dias(5),   "retry",          dias(2)),
            ("email_proposta",   dias(7),   None,             dias(0)),
            ("atualizar_crm",    dias(1),   None,             dias(0)),
        ],
    },
]


# ─── Execução ─────────────────────────────────────────────────────────────────
created = 0
updated = 0

for chain_def in CHAINS:
    name = chain_def["name"]

    # Apaga se já existir (pode ter ficado com encoding errado)
    deleted, _ = ActivityChain.objects.filter(name__icontains=name[:10]).delete()
    if deleted:
        updated += 1

    chain = ActivityChain.objects.create(
        name=name,
        description=chain_def["description"],
        applicable_model=chain_def["applicable_model"],
        owner_company=None,  # disponível para todas as empresas
        is_active=True,
    )

    for order, (bp_key, delay, fail_key, fail_delay) in enumerate(chain_def["steps"], start=1):
        ActivityChainStep.objects.create(
            chain=chain,
            activity_id=BP[bp_key],
            order=order,
            delay_days=delay,
            on_failure_activity_id=BP[fail_key] if fail_key else None,
            on_failure_delay_days=fail_delay,
        )

    print(f"  [OK] Criada: {name} ({len(chain_def['steps'])} passos)")
    created += 1

print(f"\nConcluído: {created} criadas, {updated} recriadas (encoding corrigido).")
