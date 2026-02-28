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

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

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
