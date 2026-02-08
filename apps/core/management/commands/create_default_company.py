from django.core.management.base import BaseCommand
from apps.core.models import Company


class Command(BaseCommand):
    help = 'Creates the default company (Fuet Mágico) if it does not exist'

    def handle(self, *args, **options):
        # Check if company already exists
        if Company.objects.filter(name='Fuet Mágico').exists():
            self.stdout.write(
                self.style.WARNING('Default company "Fuet Mágico" already exists.')
            )
            return
        
        # Create default company
        company = Company.objects.create(
            name='Fuet Mágico',
            legal_name='Fuet Mágico, Lda.',
            currency='EUR',
            language='pt_PT',
            country='Portugal',
            is_active=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created default company: {company.name} (ID: {company.id})')
        )
        self.stdout.write(
            self.style.SUCCESS('You can now configure additional details in Django Admin.')
        )
