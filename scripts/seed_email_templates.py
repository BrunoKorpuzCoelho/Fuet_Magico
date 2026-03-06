# -*- coding: utf-8 -*-
"""
Seed: Email Templates
Cria templates de email do sistema para os diferentes módulos.
Cada template contém o body_html (conteúdo) que é injetado dentro
do EmailLayout (envelope).

Os placeholders usam sintaxe Django template: {{ contact_name }}, {{ lead_title }}, etc.

Uso:
    python manage.py shell -c "exec(open('scripts/seed_email_templates.py', encoding='utf-8').read())"
"""

from apps.core.models import EmailTemplate

print('A criar templates globais (owner_company=NULL — disponíveis a todas as empresas)...')
print()

# ─── Templates ────────────────────────────────────────────────────────────────

TEMPLATES = [

    # ══════════════════════════════════════
    # 1. Email de Agradecimento (CRM)
    # ══════════════════════════════════════
    {
        'name': 'Email de Agradecimento',
        'module': 'CRM',
        'language': 'pt_PT',
        'default_body_path': 'defaults/crm_thankyou.html',
        'subject': 'Obrigado pelo seu interesse, {{1}}!',
        'available_placeholders': {
            '1': {'field': 'lead.contact.name',           'fallback': 'Cliente'},
            '2': {'field': 'lead.title',                  'fallback': 'a sua oportunidade'},
            '3': {'field': 'lead.assigned_to.first_name', 'fallback': 'a equipa'},
            '4': {'field': 'lead.contact.company.name',   'fallback': 'a nossa empresa'},
        },
        'body_html': '''<p style="margin: 0 0 16px 0;">Olá <strong style="color: #f9fafb;">{{1}}</strong>,</p>

<p style="margin: 0 0 16px 0;">
    Muito obrigado pelo seu interesse e pela confiança depositada em nós.
    Foi um prazer conversar consigo sobre <strong style="color: #dbc693;">{{2}}</strong>
    e ficamos entusiasmados com a possibilidade de trabalharmos juntos.
</p>

<p style="margin: 0 0 16px 0;">
    Gostaríamos de destacar alguns pontos importantes da nossa conversa:
</p>

<ul style="margin: 0 0 16px 0; padding-left: 20px; color: #d1d5db;">
    <li style="margin-bottom: 8px;">Analisámos as suas necessidades e estamos preparados para apresentar uma solução à medida</li>
    <li style="margin-bottom: 8px;">A nossa equipa ficará dedicada ao seu projeto desde o primeiro dia</li>
    <li style="margin-bottom: 8px;">Garantimos acompanhamento contínuo durante todo o processo</li>
</ul>

<p style="margin: 0 0 16px 0;">
    Nos próximos dias, entrarei em contacto para agendarmos os próximos passos.
    Entretanto, não hesite em contactar-nos caso tenha alguma questão ou necessite de informação adicional.
</p>

<p style="margin: 0 0 16px 0;">
    Estamos ao seu inteiro dispor e ansiosos por iniciar esta parceria.
</p>

<p style="margin: 0;">
    Com os melhores cumprimentos,
</p>''',
    },

    # ══════════════════════════════════════
    # 2. Email de Boas-vindas (CRM)
    # ══════════════════════════════════════
    {
        'name': 'Email de Boas-vindas',
        'module': 'CRM',
        'language': 'pt_PT',
        'default_body_path': 'defaults/crm_welcome.html',
        'subject': 'Bem-vindo(a), {{1}}!',
        'available_placeholders': {
            '1': {'field': 'lead.contact.name',           'fallback': 'Cliente'},
            '2': {'field': 'lead.title',                  'fallback': 'a sua oportunidade'},
            '3': {'field': 'lead.assigned_to.first_name', 'fallback': 'a equipa'},
            '4': {'field': 'lead.contact.company.name',   'fallback': 'a nossa empresa'},
        },
        'body_html': '''<p style="margin: 0 0 16px 0;">Olá <strong style="color: #f9fafb;">{{1}}</strong>,</p>

<p style="margin: 0 0 16px 0;">
    Seja muito bem-vindo(a)! Estamos verdadeiramente felizes por tê-lo(a) connosco.
    A <strong style="color: #dbc693;">{{4}}</strong> está empenhada em oferecer-lhe
    a melhor experiência possível desde o primeiro momento.
</p>

<p style="margin: 0 0 16px 0;">
    Aqui está o que pode esperar de nós:
</p>

<ul style="margin: 0 0 16px 0; padding-left: 20px; color: #d1d5db;">
    <li style="margin-bottom: 8px;">Um acompanhamento personalizado e dedicado às suas necessidades</li>
    <li style="margin-bottom: 8px;">Respostas rápidas a todas as suas questões e solicitações</li>
    <li style="margin-bottom: 8px;">Acesso a soluções e serviços pensados para o seu sucesso</li>
</ul>

<p style="margin: 0 0 16px 0;">
    O meu nome é <strong style="color: #f9fafb;">{{3}}</strong> e serei o seu ponto de contacto.
    Não hesite em contactar-me sempre que precisar — estou aqui para ajudar.
</p>

<p style="margin: 0 0 16px 0;">
    Entretanto, convido-o(a) a explorar os nossos serviços e a conhecer melhor
    tudo o que temos para lhe oferecer.
</p>

<p style="margin: 0;">
    Com os melhores cumprimentos,
</p>''',
    },

    # ══════════════════════════════════════
    # 3. Email de Follow-up (CRM)
    # ══════════════════════════════════════
    {
        'name': 'Email de Follow-up',
        'module': 'CRM',
        'language': 'pt_PT',
        'default_body_path': 'defaults/crm_followup.html',
        'subject': 'Seguimento: {{2}}',
        'available_placeholders': {
            '1': {'field': 'lead.contact.name',           'fallback': 'Cliente'},
            '2': {'field': 'lead.title',                  'fallback': 'a sua oportunidade'},
            '3': {'field': 'lead.assigned_to.first_name', 'fallback': 'a equipa'},
            '4': {'field': 'lead.contact.company.name',   'fallback': 'a nossa empresa'},
        },
        'body_html': '''<p style="margin: 0 0 16px 0;">Olá <strong style="color: #f9fafb;">{{1}}</strong>,</p>

<p style="margin: 0 0 16px 0;">
    Espero que esteja tudo bem consigo. Estou a escrever-lhe para dar seguimento
    à nossa conversa sobre <strong style="color: #dbc693;">{{2}}</strong>.
</p>

<p style="margin: 0 0 16px 0;">
    Gostaria de saber se teve oportunidade de analisar a informação que partilhámos
    e se surgiu alguma questão que possamos esclarecer.
</p>

<p style="margin: 0 0 16px 0;">
    Fazemos questão de relembrar os principais benefícios que discutimos:
</p>

<ul style="margin: 0 0 16px 0; padding-left: 20px; color: #d1d5db;">
    <li style="margin-bottom: 8px;">Soluções adaptadas às suas necessidades específicas</li>
    <li style="margin-bottom: 8px;">Condições competitivas e flexíveis</li>
    <li style="margin-bottom: 8px;">Suporte dedicado durante todo o processo</li>
</ul>

<p style="margin: 0 0 16px 0;">
    Estou disponível para agendar uma reunião ou chamada nos próximos dias,
    no horário que lhe for mais conveniente. Basta responder a este email
    ou contactar-me diretamente.
</p>

<p style="margin: 0 0 16px 0;">
    Fico ao seu inteiro dispor.
</p>

<p style="margin: 0;">
    Com os melhores cumprimentos,
</p>''',
    },

    # ══════════════════════════════════════
    # 4. Enviar Proposta por Email (CRM)
    # ══════════════════════════════════════
    {
        'name': 'Enviar Proposta por Email',
        'module': 'CRM',
        'language': 'pt_PT',
        'default_body_path': 'defaults/crm_proposal.html',
        'subject': 'Proposta: {{2}}',
        'available_placeholders': {
            '1': {'field': 'lead.contact.name',           'fallback': 'Cliente'},
            '2': {'field': 'lead.title',                  'fallback': 'a sua oportunidade'},
            '3': {'field': 'lead.assigned_to.first_name', 'fallback': 'a equipa'},
            '4': {'field': 'lead.contact.company.name',   'fallback': 'a nossa empresa'},
        },
        'body_html': '''<p style="margin: 0 0 16px 0;">Olá <strong style="color: #f9fafb;">{{1}}</strong>,</p>

<p style="margin: 0 0 16px 0;">
    Conforme combinado, temos o prazer de lhe enviar a nossa proposta relativa a
    <strong style="color: #dbc693;">{{2}}</strong>.
</p>

<p style="margin: 0 0 16px 0;">
    Preparámos esta proposta com base nas necessidades que identificámos em conjunto
    e acreditamos que representa a melhor solução para si.
</p>

<p style="margin: 0 0 16px 0;">
    Resumo dos pontos principais da proposta:
</p>

<ul style="margin: 0 0 16px 0; padding-left: 20px; color: #d1d5db;">
    <li style="margin-bottom: 8px;">Âmbito do projeto definido de acordo com as suas especificações</li>
    <li style="margin-bottom: 8px;">Cronograma detalhado de execução e entregas</li>
    <li style="margin-bottom: 8px;">Condições comerciais transparentes e competitivas</li>
    <li style="margin-bottom: 8px;">Garantia de qualidade e suporte pós-implementação</li>
</ul>

<p style="margin: 0 0 16px 0;">
    Encontrará todos os detalhes no documento em anexo. Caso tenha alguma questão
    ou deseje ajustar algum ponto, não hesite em contactar-me. Terei todo o gosto
    em agendar uma reunião para analisarmos a proposta em conjunto.
</p>

<p style="margin: 0 0 16px 0;">
    Aguardamos o seu feedback e estamos ao seu dispor para avançar com os próximos passos.
</p>

<p style="margin: 0;">
    Com os melhores cumprimentos,
</p>''',
    },

    # ══════════════════════════════════════
    # 5. Envio de Orçamento (SALES)
    # ══════════════════════════════════════
    {
        'name': 'Envio de Orçamento',
        'module': 'SALES',
        'language': 'pt_PT',
        'default_body_path': 'defaults/sales_quotation.html',
        'subject': 'Orçamento {{2}}',
        'available_placeholders': {
            '1': {'field': 'order.client.name',    'fallback': 'Cliente'},
            '2': {'field': 'order.order_number',   'fallback': 'o seu orçamento'},
            '3': {'field': 'order.total',          'fallback': ''},
        },
        'body_html': '''<p style="margin: 0 0 16px 0;">Olá <strong style="color: #f9fafb;">{{1}}</strong>,</p>

<p style="margin: 0 0 16px 0;">
    Temos o prazer de lhe enviar o orçamento <strong style="color: #dbc693;">{{2}}</strong>,
    conforme solicitado.
</p>

<p style="margin: 0 0 16px 0;">
    Em anexo encontrará o documento completo com todos os artigos, quantidades,
    preços e condições de pagamento. Este orçamento é válido por 30 dias a partir
    da data de emissão.
</p>

<p style="margin: 0 0 16px 0;">
    Para confirmar a encomenda ou esclarecer qualquer dúvida, não hesite em
    responder a este email ou contactar-nos diretamente. Teremos todo o gosto
    em ajudar.
</p>

<p style="margin: 0 0 16px 0;">
    Muito obrigada pela sua preferência. Esperamos ter o prazer de trabalhar consigo.
</p>

<p style="margin: 0;">
    Com os melhores cumprimentos,
</p>''',
    },

]


# ─── Execução ─────────────────────────────────────────────────────────────────

def run():
    created = 0
    skipped = 0

    for tmpl_def in TEMPLATES:
        name = tmpl_def['name']
        existing = EmailTemplate.objects.filter(name=name, owner_company__isnull=True).first()

        if existing:
            print(f'  [SKIP] "{name}" já existe (id={existing.pk})')
            skipped += 1
            continue

        tmpl = EmailTemplate.objects.create(
            name=tmpl_def['name'],
            module=tmpl_def['module'],
            language=tmpl_def['language'],
            subject=tmpl_def['subject'],
            body_html=tmpl_def['body_html'],
            available_placeholders=tmpl_def['available_placeholders'],
            default_body_path=tmpl_def.get('default_body_path', ''),
            owner_company=None,  # global — todas as empresas
            template_type='BASE',  # template do sistema
        )
        print(f'  [OK] Criado: "{name}" (module={tmpl_def["module"]}, id={tmpl.pk})')
        created += 1

    print()
    print(f'Concluído: {created} criado(s), {skipped} já existia(m).')


if __name__ == '__main__':
    run()
