"""
Script to create multiple companies and assign them to a user.
Usage: python manage.py shell < scripts/setup_companies.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.models import Company
from apps.accounts.models import CustomUser

def setup_companies():
    """Create multiple companies and assign to user"""
    
    print("=" * 60)
    print("SETUP COMPANIES - Multi-Company System")
    print("=" * 60)
    
    # Get or create default company (Fuet Mágico)
    fuet_magico, created = Company.objects.get_or_create(
        name="Fuet Mágico",
        defaults={
            'legal_name': 'Fuet Mágico Lda',
            'email': 'geral@fuetmagico.pt',
            'phone': '+351 123 456 789',
            'country': 'Portugal',
            'currency': 'EUR',
            'language': 'pt_PT'
        }
    )
    print(f"✓ {'Created' if created else 'Found'} company: {fuet_magico.name}")
    
    # Create additional test companies
    companies_data = [
        {
            'name': 'Cubix Solutions',
            'legal_name': 'Cubix Solutions Lda',
            'email': 'info@cubix.pt',
            'phone': '+351 987 654 321',
            'country': 'Portugal',
            'currency': 'EUR',
            'language': 'pt_PT'
        },
        {
            'name': 'Tech Innovations',
            'legal_name': 'Tech Innovations SA',
            'email': 'contact@techinnovations.pt',
            'phone': '+351 111 222 333',
            'country': 'Portugal',
            'currency': 'EUR',
            'language': 'pt_PT'
        },
    ]
    
    created_companies = [fuet_magico]
    
    for company_data in companies_data:
        company, created = Company.objects.get_or_create(
            name=company_data['name'],
            defaults=company_data
        )
        created_companies.append(company)
        print(f"✓ {'Created' if created else 'Found'} company: {company.name}")
    
    print("\n" + "=" * 60)
    print(f"Total companies in database: {Company.objects.count()}")
    print("=" * 60)
    
    # Assign companies to user
    print("\nAssigning companies to users...")
    
    # Get cubix user
    try:
        cubix = CustomUser.objects.get(username='cubix')
        
        # Clear existing companies and add all
        cubix.companies.clear()
        cubix.companies.add(*created_companies)
        
        # Set default company if not set
        if not cubix.default_company:
            cubix.default_company = fuet_magico
            cubix.save()
        
        print(f"✓ User 'cubix' now has access to {cubix.companies.count()} companies:")
        for company in cubix.companies.all():
            default = " (DEFAULT)" if company == cubix.default_company else ""
            print(f"  - {company.name}{default}")
            
    except CustomUser.DoesNotExist:
        print("⚠ User 'cubix' not found. Please create users first:")
        print("  python manage.py create_default_users")
    
    # Also assign to other users if they exist
    for username in ['daisy', 'admin', 'manager']:
        try:
            user = CustomUser.objects.get(username=username)
            user.companies.clear()
            user.companies.add(*created_companies)
            
            if not user.default_company:
                user.default_company = fuet_magico
                user.save()
            
            print(f"✓ User '{username}' now has access to {user.companies.count()} companies")
        except CustomUser.DoesNotExist:
            pass
    
    print("\n" + "=" * 60)
    print("✓ Setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Restart the Django server")
    print("2. Login and check the navbar dropdown")
    print("3. You should see a company selector above 'Meu Perfil'")
    print("=" * 60)

if __name__ == '__main__':
    setup_companies()
