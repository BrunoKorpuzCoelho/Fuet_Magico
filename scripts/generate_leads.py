import os
import sys
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.crm.models import Lead, CRMStage, CRMTag
from apps.contacts.models import Contact
from apps.core.models import Company
from django.contrib.auth import get_user_model
from django.db import models
from faker import Faker

fake = Faker('pt_PT')
User = get_user_model()

# Títulos específicos para pastelaria
LEAD_TITLES_PASTRY = [
    'Encomenda Bolo de Casamento 3 andares',
    'Fornecimento Bolos Aniversário Mensal',
    'Parceria Eventos Corporativos',
    'Encomenda Doces Finos para Festa',
    'Bolos Personalizados Batizado',
    'Fornecimento Pastelaria para Hotel',
    'Encomenda Cupcakes Evento 200 pessoas',
    'Bolo Tema Infantil',
    'Parceria Catering Eventos',
    'Encomenda Bolos Premium',
]

LEAD_TITLES_INGREDIENTS = [
    'Fornecimento Farinha Premium 500kg/mês',
    'Compra Chocolate Cobertura Belga',
    'Fornecimento Açúcar e Edulcorantes',
    'Parceria Matérias-Primas Orgânicas',
    'Compra Frutos Secos e Desidratados',
    'Fornecimento Aromas e Essências',
    'Compra Manteiga e Gorduras',
    'Fornecimento Frutas Congeladas',
    'Compra Fermento e Leveduras',
    'Parceria Ingredientes Importados',
]

LEAD_TITLES_PACKAGING = [
    'Fornecimento Caixas Bolos 1000un/mês',
    'Compra Embalagens Personalizadas',
    'Fornecimento Fitas e Laços Decorativos',
    'Parceria Embalagens Eco-Friendly',
    'Compra Sacos Papel Kraft',
    'Fornecimento Etiquetas Personalizadas',
    'Compra Tabuleiros e Bases Cartão',
    'Fornecimento Material Decoração',
    'Parceria Embalagens Premium',
    'Compra Caixas Cupcakes e Macarons',
]

DESCRIPTIONS_WON = [
    'Cliente muito satisfeito com proposta. Fechou contrato de 12 meses. Primeira entrega agendada.',
    'Negociação concluída com sucesso! Valores acordados, samples aprovadas. Contrato assinado.',
    'Excelente parceria estabelecida. Cliente aprovou qualidade e preços. Primeira encomenda paga.',
    'Deal fechado! Cliente gostou muito do atendimento e produtos. Parceria de longo prazo confirmada.',
    'Venda confirmada. Cliente satisfeito com condições comerciais. Início imediato.',
]

DESCRIPTIONS_LOST = [
    'Cliente escolheu concorrente por preço mais baixo. Feedback: qualidade boa mas preço alto.',
    'Lost para competitor local. Cliente preferiu fornecedor já conhecido.',
    'Não fechou: cliente adiou projeto por razões financeiras internas.',
    'Lost: cliente não aprovou samples. Preferiu outra marca.',
    'Não avançou: timing não estava certo para cliente. Pode reabrir no futuro.',
]

DESCRIPTIONS_ACTIVE = [
    'Cliente interessado. Aguardando envio de proposta comercial detalhada.',
    'Meeting agendado para próxima semana. Cliente quer ver samples.',
    'Em negociação de valores. Cliente pediu desconto para volume maior.',
    'Proposta enviada. Aguardando feedback do cliente sobre condições.',
    'Cliente gostou da apresentação. Em validação interna do budget.',
    'Follow-up agendado. Cliente comparando com outras opções.',
    'Demonstração marcada. Cliente muito interessado em qualidade.',
    'Em análise técnica. Cliente validando especificações dos produtos.',
]

LOST_REASONS = [
    'Preço acima do orçamento disponível pelo cliente',
    'Cliente escolheu concorrente com proposta mais competitiva',
    'Prazo de entrega não atende necessidade do cliente',
    'Cliente adiou projeto indefinidamente por questões internas',
    'Samples não aprovadas - cliente preferiu qualidade de outro fornecedor',
]

SOURCES = ['WEBSITE', 'REFERRAL', 'COLD_CALL', 'SOCIAL_MEDIA', 'OTHER']
PRIORITIES = ['LOW', 'MEDIUM', 'HIGH']


def create_stages():
    """Cria os stages padrão do CRM se não existirem"""
    stages_data = [
        {'name': 'New', 'sequence': 1, 'is_won_stage': False, 'is_lost_stage': False, 'color': '#17a2b8'},
        {'name': 'Qualified', 'sequence': 2, 'is_won_stage': False, 'is_lost_stage': False, 'color': '#6f42c1'},
        {'name': 'Proposition', 'sequence': 3, 'is_won_stage': False, 'is_lost_stage': False, 'color': '#fd7e14'},
        {'name': 'Negotiation', 'sequence': 4, 'is_won_stage': False, 'is_lost_stage': False, 'color': '#ffc107'},
        {'name': 'Won', 'sequence': 5, 'is_won_stage': True, 'is_lost_stage': False, 'color': '#28a745'},
        {'name': 'Lost', 'sequence': 6, 'is_won_stage': False, 'is_lost_stage': True, 'color': '#dc3545'},
    ]
    
    created_stages = {}
    for stage_data in stages_data:
        stage, created = CRMStage.objects.get_or_create(
            name=stage_data['name'],
            owner_company=None,  # Global stages
            defaults=stage_data
        )
        created_stages[stage_data['name']] = stage
        if created:
            print(f"  ✓ Stage criado: {stage.name}")
        else:
            print(f"  ℹ️  Stage já existe: {stage.name}")
    
    return created_stages


def get_lead_title_by_company(company_name):
    """Retorna títulos apropriados baseado no tipo de empresa"""
    if 'Fuet' in company_name or 'Mágico' in company_name:
        return random.choice(LEAD_TITLES_PASTRY)
    elif 'Ingrediente' in company_name or 'Doce' in company_name:
        return random.choice(LEAD_TITLES_INGREDIENTS)
    elif 'Embala' in company_name or 'Packaging' in company_name:
        return random.choice(LEAD_TITLES_PACKAGING)
    return random.choice(LEAD_TITLES_PASTRY)


def generate_leads():
    """Gera 15 leads para cada empresa"""
    
    print("=" * 70)
    print("🎯 GERAÇÃO DE LEADS - CRM")
    print("=" * 70)
    
    # Criar stages
    print("\n📊 Criando/Verificando stages do CRM...")
    stages = create_stages()
    
    # Verificar se existem contactos
    contacts_count = Contact.objects.count()
    if contacts_count == 0:
        print("\n❌ ERRO: Nenhum contacto encontrado!")
        print("💡 Execute primeiro: python scripts/generate_contacts.py")
        return
    
    print(f"\n✓ {contacts_count} contactos disponíveis")
    
    # Verificar users
    users = list(User.objects.filter(is_active=True))
    if not users:
        print("\n❌ ERRO: Nenhum utilizador encontrado!")
        print("💡 Execute primeiro: python manage.py create_default_users")
        return
    
    print(f"✓ {len(users)} utilizadores disponíveis")
    
    # Buscar todas as companies
    companies = Company.objects.filter(is_active=True)
    if companies.count() == 0:
        print("\n❌ ERRO: Nenhuma empresa encontrada!")
        print("💡 Execute primeiro: python scripts/setup_companies.py")
        return
    
    print(f"✓ {companies.count()} empresas ativas")
    
    # Limpar leads existentes
    print("\n🗑️  Limpando leads existentes...")
    deleted_count = Lead.objects.count()
    Lead.objects.all().delete()
    print(f"✓ {deleted_count} leads removidos")
    
    total_created = 0
    
    # Para cada company, criar 15 leads
    for company in companies:
        print(f"\n{'=' * 70}")
        print(f"🏢 Criando leads para: {company.name}")
        print(f"{'=' * 70}")
        
        # Buscar contactos ativos
        available_contacts = list(
            Contact.objects.filter(is_active=True)[:30]
        )
        
        if not available_contacts:
            print(f"  ⚠️  Nenhum contacto disponível. Pulando esta empresa.")
            continue
        
        # Distribuição de stages:
        # 5 WON, 5 LOST, 5 outras (NEW, QUALIFIED, PROPOSITION, NEGOTIATION)
        stage_distribution = (
            [stages['Won']] * 5 +
            [stages['Lost']] * 5 +
            [stages['New']] * 2 +
            [stages['Qualified']] * 1 +
            [stages['Proposition']] * 1 +
            [stages['Negotiation']] * 1
        )
        
        random.shuffle(stage_distribution)
        
        for i in range(15):
            contact = random.choice(available_contacts)
            stage = stage_distribution[i]
            
            # Valores baseados no estágio
            if stage.is_won_stage:
                probability = 100
                estimated_value = Decimal(random.randint(500, 5000))
                description = random.choice(DESCRIPTIONS_WON)
                lost_reason = None
                expected_close_date = datetime.now().date() - timedelta(days=random.randint(1, 15))
            elif stage.is_lost_stage:
                probability = 0
                estimated_value = Decimal(random.randint(300, 3000))
                description = random.choice(DESCRIPTIONS_LOST)
                lost_reason = random.choice(LOST_REASONS)
                expected_close_date = datetime.now().date() - timedelta(days=random.randint(1, 30))
            else:
                # Stages ativas (NEW, QUALIFIED, PROPOSITION, NEGOTIATION)
                probability = {
                    'New': random.randint(5, 15),
                    'Qualified': random.randint(20, 35),
                    'Proposition': random.randint(40, 60),
                    'Negotiation': random.randint(65, 85),
                }.get(stage.name, 50)
                estimated_value = Decimal(random.randint(400, 4500))
                description = random.choice(DESCRIPTIONS_ACTIVE)
                lost_reason = None
                expected_close_date = datetime.now().date() + timedelta(days=random.randint(7, 60))
            
            lead = Lead.objects.create(
                contact=contact,
                contact_name=contact.name,
                email_from=contact.email or fake.email(),
                phone=contact.phone or fake.phone_number(),
                title=get_lead_title_by_company(company.name),
                description=description,
                estimated_value=estimated_value,
                probability=probability,
                priority=random.choice(PRIORITIES),
                stage=stage,
                source=random.choice(SOURCES),
                expected_close_date=expected_close_date,
                assigned_to=random.choice(users),
                lost_reason=lost_reason,
                owner_company=company,
                notes=f'Lead criada automaticamente para {company.name}'
            )
            
            total_created += 1
            
            # Mostrar progresso
            stage_emoji = '🏆' if stage.is_won_stage else '❌' if stage.is_lost_stage else '🔄'
            print(f"  {stage_emoji} Lead {i+1}/15: {lead.title[:40]}... [{stage.name}] - €{estimated_value}")
        
        print(f"\n  ✅ {15} leads criadas para {company.name}")
    
    # Resumo final
    print(f"\n{'=' * 70}")
    print("📊 RESUMO FINAL")
    print(f"{'=' * 70}")
    print(f"🏢 Empresas: {companies.count()}")
    print(f"🎯 Total de Leads criadas: {total_created}")
    print(f"")
    print(f"📈 Distribuição por empresa (15 leads cada):")
    print(f"   • 5 leads WON (ganhas) 🏆")
    print(f"   • 5 leads LOST (perdidas) ❌")
    print(f"   • 2 leads NEW (novas) 🆕")
    print(f"   • 1 lead QUALIFIED (qualificada) ✅")
    print(f"   • 1 lead PROPOSITION (proposta) 📋")
    print(f"   • 1 lead NEGOTIATION (negociação) 🤝")
    print(f"")
    
    # Estatísticas por estágio
    print(f"📊 Estatísticas Globais:")
    for stage in CRMStage.objects.all().order_by('sequence'):
        count = Lead.objects.filter(stage=stage).count()
        total_value = Lead.objects.filter(stage=stage).aggregate(
            total=models.Sum('estimated_value')
        )['total'] or 0
        print(f"   • {stage.name}: {count} leads (€{total_value:,.2f})")
    
    print(f"\n{'=' * 70}")
    print("✅ Geração de leads concluída com sucesso!")
    print(f"{'=' * 70}")
    print(f"\n💡 Acesse: http://127.0.0.1:8000/crm/leads/")


if __name__ == '__main__':
    generate_leads()

# Always execute when loaded via shell
generate_leads()
