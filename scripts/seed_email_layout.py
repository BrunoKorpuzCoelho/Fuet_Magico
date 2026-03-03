# -*- coding: utf-8 -*-
"""
Seed: Email Layout
Cria o registo global de EmailLayout na base de dados, lendo o HTML
default de templates/emails/base_layout.html.

Uso:
    python manage.py shell -c "exec(open('scripts/seed_email_layout.py', encoding='utf-8').read())"
"""

import os

from django.conf import settings
from apps.core.models import EmailLayout


def run():
    default_path = os.path.join(settings.BASE_DIR, 'templates', 'emails', 'base_layout.html')

    if not os.path.exists(default_path):
        print(f'ERRO: Ficheiro default não encontrado em {default_path}')
        return

    with open(default_path, 'r', encoding='utf-8') as f:
        default_html = f.read()

    existing = EmailLayout.objects.first()
    if existing:
        print(f'Email Layout já existe (atualizado em {existing.updated_at:%Y-%m-%d %H:%M}).')
        print('Para restaurar o default, usa: EmailLayout.reset_to_default()')
    else:
        layout = EmailLayout.objects.create(html_content=default_html)
        print(f'Email Layout criado com sucesso (id={layout.pk}).')
        print(f'HTML carregado de: {default_path}')
        print(f'Tamanho: {len(default_html)} caracteres')


if __name__ == '__main__':
    run()
