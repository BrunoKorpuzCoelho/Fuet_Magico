import os
import sys
import django
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.contacts.models import Contact

# ── Static Portuguese data (no faker dependency) ──────────────────────────────
PT_FIRST_NAMES = [
    'Ana', 'João', 'Maria', 'Pedro', 'Sofia', 'Rui', 'Catarina', 'Tiago',
    'Inês', 'Filipe', 'Margarida', 'Carlos', 'Beatriz', 'Miguel', 'Sara',
    'Diogo', 'Marta', 'André', 'Francisca', 'Hugo', 'Rita', 'Nuno',
    'Leonor', 'Gonçalo', 'Raquel', 'Paulo', 'Cláudia', 'Luís', 'Patrícia', 'Jorge',
]
PT_LAST_NAMES = [
    'Silva', 'Santos', 'Ferreira', 'Pereira', 'Oliveira', 'Costa', 'Rodrigues',
    'Martins', 'Jesus', 'Sousa', 'Fernandes', 'Gonçalves', 'Gomes', 'Lopes',
    'Marques', 'Alves', 'Correia', 'Nunes', 'Carvalho', 'Matos', 'Pinto',
    'Moreira', 'Teixeira', 'Ribeiro', 'Cunha', 'Fonseca', 'Dias', 'Ramos',
]
COMPANY_SUFFIXES = ['Lda', 'SA', 'Unipessoal', '& Filhos', '& Associados']
COMPANY_NOUNS = [
    'Padaria Central', 'Doce Sabor', 'Pastelaria Requinte', 'Forno Artesanal',
    'Confeitaria Moderna', 'Aromas de Lisboa', 'Delícias do Norte',
    'Sabores Artesanais', 'Forno Tradicional', 'Pastelaria Gourmet',
    'Distribuidora AliCo', 'Ingredientes Plus', 'Embalagens Total',
    'Packaging Pro', 'Matérias-Primas JL', 'Distribuidora Nortenha',
    'Alimentos Qualidade', 'Fornecedor Central', 'TradeFoods', 'GerFood',
]
PT_CITIES = [
    'Lisboa', 'Porto', 'Braga', 'Coimbra', 'Aveiro', 'Faro', 'Setúbal',
    'Leiria', 'Viseu', 'Évora', 'Viana do Castelo', 'Beja', 'Guarda',
    'Castelo Branco', 'Santarém', 'Portalegre', 'Vila Real', 'Bragança',
]
PT_STREETS = [
    'Rua da Liberdade', 'Avenida da República', 'Rua do Comércio', 'Travessa das Flores',
    'Rua de Santo António', 'Avenida Central', 'Rua Nova', 'Rua do Carmo',
    'Avenida dos Aliados', 'Rua da Alegria', 'Rua Direita', 'Largo do Município',
    'Praça do Marquês', 'Rua da Igreja', 'Alameda das Acácias', 'Rua da Escola',
    'Beco da Misericórdia', 'Rua do Mercado', 'Avenida do Parque', 'Rua de São João',
]
EMAIL_DOMAINS = ['gmail.com', 'hotmail.com', 'outlook.pt', 'sapo.pt', 'mail.pt', 'yahoo.com']
NOTES_LIST = [
    'Cliente habitual. Prefere contacto por email.', 'Parceiro estratégico regional.',
    'Contacto obtido em feira de negócios.', 'Referência de outro cliente.',
    'Interessado em produtos sazonais.', 'Contacto inicial via website.',
    'Preferência por encomendas mensais.', 'Aguarda proposta comercial.',
]

def _name():
    return f'{random.choice(PT_FIRST_NAMES)} {random.choice(PT_LAST_NAMES)}'

def _company():
    return f'{random.choice(COMPANY_NOUNS)} {random.choice(COMPANY_SUFFIXES)}'

def _slug(text):
    for a, b in [('ã','a'),('â','a'),('á','a'),('à','a'),('ç','c'),('é','e'),('ê','e'),('í','i'),('ó','o'),('ô','o'),('ú','u'),(' ','.')]:
        text = text.replace(a, b)
    return ''.join(c for c in text.lower() if c.isalnum() or c == '.')

def _email(name=''):
    return f'{_slug(name) or "contacto"}{random.randint(1,99)}@{random.choice(EMAIL_DOMAINS)}'

def _company_email(cname):
    slug = _slug(cname.split()[0])
    return f'geral@{slug or "empresa"}{random.randint(1,99)}.pt'

def _street():
    return f'{random.choice(PT_STREETS)}, {random.randint(1, 999)}'

def _city():
    return random.choice(PT_CITIES)

def _postal():
    return f'{random.randint(1000, 9999)}-{random.randint(100, 999)}'

def _notes():
    return random.choice(NOTES_LIST)

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
        cname = _company()
        company = Contact.objects.create(
            name=cname,
            contact_category='COMPANY',
            email=_company_email(cname),
            phone=generate_phone(),
            whatsapp=generate_phone() if random.choice([True, False]) else '',
            address=_street(),
            city=_city(),
            postal_code=_postal(),
            nif=generate_nif(),
            notes=_notes() if random.choice([True, False]) else ''
        )
        companies.append(company)
        print(f"  ✓ {company.name}")

    print(f"\n✅ {len(companies)} empresas criadas!")

    print("\n👤 Criando 40 pessoas independentes...")
    independent_people = []
    for i in range(40):
        pname = _name()
        person = Contact.objects.create(
            name=pname,
            contact_category='PERSON',
            email=_email(pname),
            phone=generate_phone(),
            whatsapp=generate_phone() if random.choice([True, False]) else '',
            address=_street(),
            city=_city(),
            postal_code=_postal(),
            nif=generate_nif() if random.choice([True, False]) else '',
            notes=_notes() if random.choice([True, False]) else ''
        )
        independent_people.append(person)
        if (i + 1) % 10 == 0:
            print(f"  ✓ {i + 1} pessoas criadas...")

    print(f"\n✅ {len(independent_people)} pessoas independentes criadas!")

    print("\n👥 Criando 40 colaboradores (pessoas em empresas)...")
    employees = []
    for i in range(40):
        company = random.choice(companies)
        ename = _name()
        employee = Contact.objects.create(
            name=ename,
            contact_category='PERSON',
            company=company,
            position=random.choice(POSITIONS),
            email=_email(ename),
            phone=generate_phone(),
            whatsapp=generate_phone() if random.choice([True, False]) else '',
            address=_street() if random.choice([True, False]) else '',
            city=_city() if random.choice([True, False]) else '',
            postal_code=_postal() if random.choice([True, False]) else '',
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
