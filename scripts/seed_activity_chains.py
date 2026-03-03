# -*- coding: utf-8 -*-
"""
Seed: Cadeias de Atividade
Cria 7 cadeias de automação para Leads e Contactos.

Uso:
    python manage.py shell -c "exec(open('scripts/seed_activity_chains.py', encoding='utf-8').read())"
"""

from apps.core.models import ActivityChain, ActivityChainStep, ScheduledActivity

# ─── Mapa de nomes dos blueprints (lookup em runtime) ────────────────────────
# Os UUIDs são gerados automaticamente, por isso usamos o nome como chave estável.
BP_NAMES = {
    # Documents
    "fatura":           "Processar Fatura",
    "recolher_docs":    "Recolher Documentos",
    "upload_cert":      "Upload Certificação",
    # Email
    "email_agradec":    "Email de Agradecimento",
    "email_boasvindas": "Email de Boas-vindas",
    "email_followup":   "Email de Follow-up",
    "email_proposta":   "Enviar Proposta por Email",
    # Phone Call
    "callback":         "Callback - Cliente Pediu para Ligar",
    "ligacao_followup": "Ligação de Follow-up",
    "primeira_ligacao": "Primeira Ligação - Contacto Inicial",
    "retry":            "Retry - Não Atendeu",
    # Signature
    "assinar_acordo":   "Assinatura de Acordo de Serviço",
    "assinar_contrato": "Assinatura de Contrato",
    "assinar_nda":      "Assinatura de NDA",
    # To-Do
    "atualizar_crm":    "Atualizar CRM",
    "enviar_contrato":  "Enviar Contrato",
    "pesquisar_cli":    "Pesquisar Cliente",
    "preparar_prop":    "Preparar Proposta",
    # WhatsApp
    "wa_followup":      "Follow-up via WhatsApp",
    "wa_lembrete":      "Lembrete de Reunião - WhatsApp",
    "wa_docs":          "Solicitar Documentos - WhatsApp",
}


def _build_bp():
    """Resolve os nomes de blueprints para UUIDs a partir da base de dados."""
    bp = {}
    missing = []
    for key, name in BP_NAMES.items():
        obj = ScheduledActivity.objects.filter(name=name).first()
        if obj:
            bp[key] = obj.id
        else:
            missing.append(name)
    if missing:
        raise ValueError(
            f"Blueprint(s) não encontrado(s) na BD: {missing}\n"
            "Corre primeiro: python manage.py setup_activity_templates"
        )
    return bp

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

def run():
    BP = _build_bp()
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


if __name__ == '__main__':
    run()
