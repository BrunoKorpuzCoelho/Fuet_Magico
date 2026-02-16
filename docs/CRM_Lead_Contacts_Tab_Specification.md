# 📋 CRM - Aba "Contactos" do Lead
## Especificação Detalhada e Recomendações

---

## 🎯 Objetivo da Aba

A aba "Contactos" dentro do formulário de Lead serve para **centralizar todas as informações de contacto** relacionadas com a oportunidade, permitindo:

1. **Visualizar** dados do contacto principal
2. **Gerir** pessoas de contacto (ContactPerson) associadas
3. **Consultar** histórico de interações
4. **Aceder rapidamente** a outras oportunidades do mesmo cliente
5. **Criar contactos** inline sem sair do formulário

---

## 📦 Estrutura Recomendada (4 Secções)

### **1. Informação do Contacto Principal** ⭐
*Mostrar se `lead.contact` existe, caso contrário mostrar botão para criar*

#### **1.1 Quando HÁ Contacto Associado:**

```
┌─────────────────────────────────────────────────────────┐
│ 👤 CONTACTO PRINCIPAL                                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Avatar]  Nome da Empresa Lda                          │
│            Tipo: Cliente • ID: #12345                   │
│                                                          │
│  📧 Email: geral@empresa.pt                             │
│  📞 Telefone: +351 123 456 789                          │
│  📍 Morada: Rua Exemplo, 123, 1000-001 Lisboa          │
│  🌐 Website: www.empresa.pt                             │
│  💼 NIF: 123456789                                      │
│                                                          │
│  [Ver Ficha Completa] [Editar Contacto]                │
└─────────────────────────────────────────────────────────┘
```

**Campos a mostrar:**
- **Avatar** (ou ícone por defeito baseado em `contact_category`)
- **Nome/Empresa** (`contact.name`)
- **Tipo de Contacto** (`contact.contact_type`: Cliente, Fornecedor, Ambos)
- **ID/Referência** (`contact.id` ou código interno)
- **Email** (`contact.email`)
- **Telefone** (`contact.phone`)
- **Telemóvel** (`contact.mobile` - se existir)
- **Morada completa** (`contact.street`, `city`, `zip_code`, `country`)
- **Website** (`contact.website` - se existir)
- **NIF/VAT** (`contact.tax_id` - se existir)

**Botões de ação:**
- **"Ver Ficha Completa"**: Link para `/contacts/<uuid>/` (abre em nova tab)
- **"Editar Contacto"**: Link para `/contacts/<uuid>/edit/`

---

#### **1.2 Quando NÃO HÁ Contacto Associado:**

```
┌─────────────────────────────────────────────────────────┐
│ ⚠️  NENHUM CONTACTO ASSOCIADO                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Esta oportunidade não está ligada a um contacto        │
│  existente. Dados de contacto inseridos:                │
│                                                          │
│  Nome: [valor de contact_name se existir]               │
│  Email: [valor de email_from se existir]                │
│  Telefone: [valor de phone se existir]                  │
│                                                          │
│  [+ Criar Novo Contacto] [🔍 Procurar e Associar]       │
└─────────────────────────────────────────────────────────┘
```

**Funcionalidades:**
- **"Criar Novo Contacto"**: Abre modal inline
  - Pré-preenche com `contact_name`, `email_from`, `phone` do Lead
  - Ao criar, associa automaticamente à Lead
  - Fecha modal e atualiza a aba
- **"Procurar e Associar"**: Abre modal com autocomplete
  - Busca por nome, email, telefone, NIF
  - Ao selecionar, associa à Lead
  - Atualiza campos `email_from`, `phone` com dados do Contact

---

### **2. Pessoas de Contacto** 👥
*Lista de ContactPerson associadas ao Contact principal*

```
┌─────────────────────────────────────────────────────────┐
│ 👥 PESSOAS DE CONTACTO (3)                              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ [Avatar] João Silva                   [✏️ Editar]│     │
│  │          CEO • Decisor                         │     │
│  │          📧 joao@empresa.pt                    │     │
│  │          📱 +351 912 345 678                   │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ [Avatar] Maria Santos              [✏️ Editar]│     │
│  │          CFO • Aprovador Financeiro            │     │
│  │          📧 maria@empresa.pt                   │     │
│  │          📱 +351 913 456 789                   │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  [+ Adicionar Pessoa de Contacto]                       │
└─────────────────────────────────────────────────────────┘
```

**Campos a mostrar por pessoa:**
- **Avatar** (ou iniciais)
- **Nome** (`person.name`)
- **Cargo/Função** (`person.job_title`)
- **Papel na Decisão** (`person.role`: Decisor, Influenciador, Aprovador, Utilizador)
- **Email** (`person.email`)
- **Telemóvel** (`person.mobile`)
- **Telefone direto** (`person.phone` - se diferente do principal)
- **Notas** (breve descrição, ex: "Contactar apenas após 14h")

**Funcionalidades:**
- **"Adicionar Pessoa"**: Modal inline para criar ContactPerson
  - Associa automaticamente ao Contact principal
  - Campos: nome, cargo, role, email, telemóvel
- **"Editar"**: Modal inline para editar
- Ordenação por **ordem de importância** (Decisor → Aprovador → Influenciador → Utilizador)

**⚠️ NOTA:** Só aparece se houver Contact associado

---

### **3. Outras Oportunidades deste Cliente** 🔄
*Histórico de Leads/Vendas do mesmo contacto*

```
┌─────────────────────────────────────────────────────────┐
│ 🔄 HISTÓRICO DE OPORTUNIDADES (5)                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📊 Resumo:                                              │
│     • Oportunidades abertas: 2 (€15.000)                │
│     • Oportunidades ganhas: 2 (€35.000)                 │
│     • Oportunidades perdidas: 1                         │
│     • Taxa de sucesso: 66% (2/3 fechadas)               │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ 🟢 Proposta Catering Dezembro • Ganho          │     │
│  │    €18.000 • 16 Jan 2026                       │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ 🟡 Renovação Contrato Anual • Proposta         │     │
│  │    €12.000 • 5 Fev 2026                        │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ 🔴 Bolo Aniversário Empresa • Perdido          │     │
│  │    €2.500 • 20 Dez 2025                        │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  [Ver Todas as Oportunidades (5)]                       │
└─────────────────────────────────────────────────────────┘
```

**Dados a mostrar:**
- **Resumo estatístico:**
  - Total de oportunidades
  - Total valor em aberto
  - Total valor ganho (histórico)
  - Taxa de conversão
- **Últimas 3-5 oportunidades:**
  - **Badge colorido** por estágio (🟢 Ganho, 🔴 Perdido, 🟡 Em progresso)
  - **Título** da oportunidade
  - **Estágio atual**
  - **Valor** estimado
  - **Data** de criação ou última atualização
  - Click → abre lead detail

**Ordenação:** Mais recentes primeiro

**⚠️ NOTA:** Só aparece se houver Contact associado

---

### **4. Histórico de Interações** 📅
*Timeline de atividades, emails, chamadas, reuniões*

```
┌─────────────────────────────────────────────────────────┐
│ 📅 HISTÓRICO DE INTERAÇÕES (12)                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Filtros: [Todas] [Emails] [Chamadas] [Reuniões]        │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ 📧 Email enviado: "Proposta Comercial"         │     │
│  │    Por: João Admin • 14 Fev 2026 15:32        │     │
│  │    Para: joao@empresa.pt                       │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ 📞 Chamada realizada (15 min)                  │     │
│  │    Por: Maria Vendas • 13 Fev 2026 10:00      │     │
│  │    Notas: Cliente interessado, pedir orçamento │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ 🤝 Reunião agendada                            │     │
│  │    20 Fev 2026 14:00 • Escritório cliente     │     │
│  │    Participantes: João Admin, João Silva (CEO) │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  [Carregar Mais (9 restantes)]                          │
└─────────────────────────────────────────────────────────┘
```

**Tipos de interações:**
1. **Emails** 📧
   - Enviados via sistema
   - Recebidos (se integração IMAP ativa)
   - Assunto, remetente/destinatário, data/hora
2. **Chamadas** 📞
   - Registadas manualmente ou via integração telefónica
   - Duração, notas, resultado
3. **Reuniões** 🤝
   - Agendadas (futuras) ou realizadas (passadas)
   - Local, participantes, agenda
4. **WhatsApp** 💬
   - Mensagens enviadas
   - Estado: enviado, lido, respondido
5. **Notas** 📝
   - Anotações rápidas dos comerciais
   - Observações importantes
6. **Atividades** ✅
   - To-Dos concluídas relacionadas com este contacto

**Funcionalidades:**
- **Filtros** por tipo de interação
- **Ordenação** cronológica (mais recente primeiro)
- **Paginação** (carregar mais)
- **Click** para expandir detalhes
- **"Adicionar Interação"**: Modal para registar manualmente

**⚠️ NOTA:** Só aparece se houver Contact associado

---

## 🔧 Implementação Técnica

### **Estrutura de Dados Necessária**

#### **Modelos Existentes:**
```python
# apps/crm/models.py
class Lead:
    contact = FK(Contact)  # ✅ JÁ EXISTE
    contact_name = CharField  # ✅ JÁ EXISTE (fallback)
    email_from = EmailField  # ✅ JÁ EXISTE (fallback)
    phone = CharField  # ✅ JÁ EXISTE (fallback)
```

#### **Modelos a Criar (Futuro):**
```python
# apps/contacts/models.py
class ContactPerson(BaseModel):
    """Pessoas de contacto de uma empresa"""
    contact = FK(Contact, related_name='persons')
    name = CharField(max_length=255)
    job_title = CharField(max_length=100, blank=True)  # CEO, CFO, etc.
    role = CharField(choices=ROLE_CHOICES)  # DECISION_MAKER, APPROVER, INFLUENCER, USER
    email = EmailField(blank=True)
    phone = CharField(max_length=50, blank=True)
    mobile = CharField(max_length=50, blank=True)
    notes = TextField(blank=True)
    is_primary = BooleanField(default=False)  # Contacto principal
    owner_company = FK(Company)

# apps/core/models.py (ou apps/crm/)
class Interaction(BaseModel):
    """Histórico de interações com contactos"""
    contact = FK(Contact, related_name='interactions')
    lead = FK(Lead, null=True, blank=True, related_name='interactions')  # Se relacionado com lead
    interaction_type = CharField(choices=TYPE_CHOICES)  # EMAIL, CALL, MEETING, WHATSAPP, NOTE
    subject = CharField(max_length=255)
    description = TextField(blank=True)
    direction = CharField(choices=[('IN', 'Recebida'), ('OUT', 'Enviada')])  # Para emails/chamadas
    duration_minutes = IntegerField(null=True, blank=True)  # Para chamadas/reuniões
    scheduled_date = DateTimeField(null=True, blank=True)  # Para reuniões futuras
    participants = JSONField(default=list, blank=True)  # Lista de participantes
    attachments = JSONField(default=list, blank=True)  # Ficheiros anexos
    created_by = FK(User, related_name='interactions_created')
    owner_company = FK(Company)
```

---

### **View Context (LeadCreateView/LeadUpdateView)**

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    if self.object and self.object.contact:
        contact = self.object.contact
        
        # Pessoas de contacto
        context['contact_persons'] = contact.persons.filter(is_active=True).order_by('-is_primary', 'name')
        
        # Outras oportunidades do mesmo contacto
        other_leads = Lead.objects.filter(
            contact=contact,
            is_active=True
        ).exclude(id=self.object.id).order_by('-created_at')[:5]
        
        context['other_leads'] = other_leads
        context['other_leads_stats'] = {
            'total': other_leads.count(),
            'open_count': other_leads.exclude(stage__is_won_stage=True).exclude(stage__is_lost_stage=True).count(),
            'open_value': other_leads.exclude(stage__is_won_stage=True).exclude(stage__is_lost_stage=True).aggregate(Sum('estimated_value'))['estimated_value__sum'] or 0,
            'won_count': other_leads.filter(stage__is_won_stage=True).count(),
            'won_value': other_leads.filter(stage__is_won_stage=True).aggregate(Sum('estimated_value'))['estimated_value__sum'] or 0,
            'lost_count': other_leads.filter(stage__is_lost_stage=True).count(),
            'conversion_rate': (won_count / (won_count + lost_count) * 100) if (won_count + lost_count) > 0 else 0
        }
        
        # Histórico de interações
        context['interactions'] = Interaction.objects.filter(
            contact=contact
        ).order_by('-created_at')[:10]
        
    return context
```

---

## 🎨 Layout Visual Recomendado

```html
<div x-show="activeFormTab === 'contacts'" class="pt-4">
    {% if form.instance.contact %}
        <!-- Secção 1: Contacto Principal -->
        <div class="mb-6 p-4 bg-gray-800 rounded-lg border border-gray-700">
            <h3 class="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2">
                <svg>...</svg> CONTACTO PRINCIPAL
            </h3>
            <!-- Grid 2 colunas: Avatar + Info -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <!-- Avatar -->
                <div class="flex justify-center">
                    <div class="w-20 h-20 rounded-full bg-primary/20 flex items-center justify-center">
                        <span class="text-2xl font-bold text-primary">{{ form.instance.contact.name|slice:":2"|upper }}</span>
                    </div>
                </div>
                <!-- Info principal -->
                <div class="md:col-span-2 space-y-2">
                    <div>
                        <h4 class="text-lg font-bold text-white">{{ form.instance.contact.name }}</h4>
                        <p class="text-sm text-gray-400">{{ form.instance.contact.get_contact_type_display }}</p>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
                        <div class="flex items-center gap-2">
                            <svg class="w-4 h-4 text-gray-500">...</svg>
                            <span class="text-gray-300">{{ form.instance.contact.email }}</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <svg class="w-4 h-4 text-gray-500">...</svg>
                            <span class="text-gray-300">{{ form.instance.contact.phone }}</span>
                        </div>
                        <!-- Mais campos... -->
                    </div>
                    <div class="flex gap-2 mt-4">
                        <a href="{% url 'contact_detail' form.instance.contact.id %}" target="_blank" 
                           class="px-3 py-1 text-xs bg-gray-700 hover:bg-gray-600 text-white rounded">
                            Ver Ficha Completa
                        </a>
                        <a href="{% url 'contact_edit' form.instance.contact.id %}" 
                           class="px-3 py-1 text-xs bg-gray-700 hover:bg-gray-600 text-white rounded">
                            Editar Contacto
                        </a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Secção 2: Pessoas de Contacto -->
        <div class="mb-6 p-4 bg-gray-800 rounded-lg border border-gray-700">
            <h3 class="text-sm font-semibold text-gray-400 mb-4 flex items-center gap-2">
                <svg>...</svg> PESSOAS DE CONTACTO ({{ contact_persons|length }})
            </h3>
            {% if contact_persons %}
                <div class="space-y-2">
                    {% for person in contact_persons %}
                        <!-- Card de pessoa -->
                    {% endfor %}
                </div>
            {% else %}
                <p class="text-sm text-gray-500 text-center py-4">Nenhuma pessoa de contacto registada</p>
            {% endif %}
            <button type="button" class="mt-4 text-sm text-primary hover:text-primary/80">
                + Adicionar Pessoa de Contacto
            </button>
        </div>

        <!-- Secção 3: Outras Oportunidades -->
        <!-- ... -->

        <!-- Secção 4: Histórico de Interações -->
        <!-- ... -->

    {% else %}
        <!-- Estado vazio: sem contacto associado -->
        <div class="text-center py-12">
            <div class="w-16 h-16 mx-auto mb-4 bg-yellow-500/20 rounded-full flex items-center justify-center">
                <svg class="w-8 h-8 text-yellow-500">...</svg>
            </div>
            <h3 class="text-lg font-medium text-gray-400 mb-2">Nenhum Contacto Associado</h3>
            <p class="text-sm text-gray-500 mb-6">
                Esta oportunidade não está ligada a um contacto existente.<br>
                Crie um novo contacto ou procure um existente para associar.
            </p>
            <div class="flex justify-center gap-3">
                <button type="button" class="px-4 py-2 bg-primary hover:bg-primary/90 text-white rounded-lg">
                    + Criar Novo Contacto
                </button>
                <button type="button" class="px-4 py-2 border border-gray-600 hover:border-gray-500 text-gray-300 rounded-lg">
                    🔍 Procurar e Associar
                </button>
            </div>
        </div>
    {% endif %}
</div>
```

---

## 📌 Prioridades de Implementação

### **Fase 1 - Essencial (Agora)**
1. ✅ **Secção 1**: Mostrar dados do Contact se associado
2. ✅ **Estado vazio**: Botões criar/procurar se não associado

### **Fase 2 - Importante (Próxima Sprint)**
3. 🔄 **Modal criar contacto** inline
4. 🔄 **Modal procurar/associar** contacto
5. 🔄 **Secção 3**: Outras oportunidades do cliente

### **Fase 3 - Útil (Futuro)**
6. ⏳ **Modelo ContactPerson**
7. ⏳ **Secção 2**: Pessoas de contacto
8. ⏳ **Modal adicionar pessoa**

### **Fase 4 - Avançado (Muito Futuro)**
9. ⏳ **Modelo Interaction**
10. ⏳ **Secção 4**: Histórico de interações
11. ⏳ **Integração email/WhatsApp**

---

## 💡 Resumo das Recomendações

### **✅ O que DEVE ter:**
1. **Informações do contacto principal** quando associado
2. **Botões para criar/associar** contacto quando não há
3. **Outras oportunidades** do mesmo cliente (histórico)
4. **Pessoas de contacto** (ContactPerson) para empresas

### **❌ O que NÃO deve ter:**
1. ~~Marketing direto~~ (será app separada)
2. ~~Newsletter signup~~ (será em Contactos ou Marketing)
3. ~~Envio de emails~~ (será no Chatter/Activities)
4. ~~Campanhas~~ (será app Marketing)

### **🎯 Filosofia:**
- **Read-only** maioritariamente (consulta)
- **Quick actions** para criar/editar (modais)
- **Contexto rico** sobre o cliente
- **Facilitar decisão** comercial (histórico, taxa conversão)
- **Não duplicar** funcionalidades de outros módulos

---

## 🔗 Relações entre Módulos

```
Contact (1) ────┬──── (N) Lead
                │
                ├──── (N) ContactPerson
                │
                ├──── (N) SaleOrder (futuro)
                │
                ├──── (N) Invoice (futuro)
                │
                └──── (N) Interaction (futuro)

Lead (1) ────┬──── (N) Activity
             │
             ├──── (1) SaleOrder (conversão)
             │
             └──── (N) Interaction (futuro)
```

---

**Documento criado:** Fevereiro 2026  
**Autor:** GitHub Copilot  
**Status:** Especificação para implementação
