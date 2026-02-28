"""
Management command: seed_historical_leads

DEPRECATED — esta funcionalidade foi absorvida por scripts/generate_leads.py.
Use: python manage.py seed --only demo_leads

Mantido apenas para compatibilidade.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        'DEPRECATED — use "python manage.py seed --only demo_leads". '
        'Gera leads históricas + leads por empresa num único script.'
    )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(
            '⚠️  Este comando está DEPRECATED.\n'
            '   Use: python manage.py seed --only demo_leads\n'
            '   Ou:  python scripts/generate_leads.py\n'
            '\n'
            '   A redirecionar para o script unificado...\n'
        ))
        from scripts.generate_leads import run
        run()
