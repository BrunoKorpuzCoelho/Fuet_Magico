import os
import sys
import django
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contacts.models import Contact
from faker import Faker

fake = Faker('pt_PT')

POSITIONS = [
    'CEO', 'CFO', 'CTO', 'Gerente', 'Diretor', 'Manager', 
    'Coordenador', 'Supervisor', 'Analista', 'Assistente',
    'Vendedor', 'Comprador', 'Consultor', 'Técnico'
]

def generate_nif():
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])

def generate_phone():
    prefixes = ['91', '92', '93', '96']
    return f"+351 {random.choice(prefixes)}{random.randint(1000000, 9999999)}"

def run():
    print("🗑️  Limpando contactos existentes...")
    Contact.objects.all().delete()

    print("\n🏢 Criando 20 empresas...")
    companies = []
    for i in range(20):
        company = Contact.objects.create(
            name=fake.company(),
            contact_category='COMPANY',
            email=fake.company_email(),
            phone=generate_phone(),
            whatsapp=generate_phone() if random.choice([True, False]) else '',
            address=fake.street_address(),
            city=fake.city(),
            postal_code=fake.postcode(),
            nif=generate_nif(),
            notes=fake.text(max_nb_chars=100) if random.choice([True, False]) else ''
        )
        companies.append(company)
        print(f"  ✓ {company.name}")

    print(f"\n✅ {len(companies)} empresas criadas!")

    print("\n👤 Criando 40 pessoas independentes...")
    independent_people = []
    for i in range(40):
        person = Contact.objects.create(
            name=fake.name(),
            contact_category='PERSON',
            email=fake.email(),
            phone=generate_phone(),
            whatsapp=generate_phone() if random.choice([True, False]) else '',
            address=fake.street_address(),
            city=fake.city(),
            postal_code=fake.postcode(),
            nif=generate_nif() if random.choice([True, False]) else '',
            notes=fake.text(max_nb_chars=100) if random.choice([True, False]) else ''
        )
        independent_people.append(person)
        if (i + 1) % 10 == 0:
            print(f"  ✓ {i + 1} pessoas criadas...")

    print(f"\n✅ {len(independent_people)} pessoas independentes criadas!")

    print("\n👥 Criando 40 colaboradores (pessoas em empresas)...")
    employees = []
    for i in range(40):
        company = random.choice(companies)
        employee = Contact.objects.create(
            name=fake.name(),
            contact_category='PERSON',
            company=company,
            position=random.choice(POSITIONS),
            email=fake.email(),
            phone=generate_phone(),
            whatsapp=generate_phone() if random.choice([True, False]) else '',
            address=fake.street_address() if random.choice([True, False]) else '',
            city=fake.city() if random.choice([True, False]) else '',
            postal_code=fake.postcode() if random.choice([True, False]) else '',
            nif='',
            notes=f'Colaborador da {company.name}'
        )
        employees.append(employee)
        if (i + 1) % 10 == 0:
            print(f"  ✓ {i + 1} colaboradores criados...")

    print(f"\n✅ {len(employees)} colaboradores criados!")

    print("\n" + "="*50)
    print("📊 RESUMO FINAL:")
    print("="*50)
    print(f"🏢 Empresas: {Contact.objects.filter(contact_category='COMPANY').count()}")
    print(f"👤 Pessoas independentes: {Contact.objects.filter(contact_category='PERSON', company__isnull=True).count()}")
    print(f"👥 Colaboradores: {Contact.objects.filter(contact_category='PERSON', company__isnull=False).count()}")
    print(f"📝 TOTAL: {Contact.objects.count()} contactos")
    print("="*50)

    print("\n✅ Dados gerados com sucesso!")
    print("\n💡 Acesse: http://127.0.0.1:8000/pt/contacts/")


if __name__ == '__main__':
    run()
