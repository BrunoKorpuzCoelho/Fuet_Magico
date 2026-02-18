# 🎯 Activities System - Quick Start Guide

## 📚 ÍNDICE
1. [Criar Templates](#1-criar-templates)
2. [Configurar Workflows](#2-configurar-workflows)
3. [Criar Activities Manualmente](#3-criar-activities-manualmente)
4. [Marcar Activities como Done](#4-marcar-activities-como-done)
5. [Exemplos Reais de Uso](#5-exemplos-reais-de-uso)

---

## 1️⃣ CRIAR TEMPLATES

Templates são modelos reutilizáveis para criar activities rapidamente.

### **Exemplo 1: Template Simples**
```python
from apps.core.models import ActivityTemplate

# Template para ligação de follow-up
call_template = ActivityTemplate.objects.create(
    name='Follow-up Call',
    activity_type='CALL',
    default_summary='Ligar para {{contact_name}}',
    default_description='Fazer follow-up da proposta enviada',
    due_days_offset=3,  # Criar para daqui a 3 dias
    icon='📞',  # Emoji ou 'fa-phone'
    decoration_type='warning',  # Cor laranja
)
```

### **Exemplo 2: Template com Auto-Delete**
```python
# Template para tarefas temporárias que não precisam ficar no histórico
temp_task = ActivityTemplate.objects.create(
    name='Quick Task',
    activity_type='TODO',
    default_summary='Tarefa rápida',
    due_days_offset=0,  # Para hoje
    keep_done_activities=False,  # ← Não guardar quando done
    auto_delete_done_after_days=7,  # ← Deletar após 7 dias
    icon='✅',
)
```

### **Exemplo 3: Template com Responsável Padrão**
```python
# Template que sempre atribui ao mesmo user
manager = User.objects.get(email='manager@fuetmagico.com')

approval_template = ActivityTemplate.objects.create(
    name='Manager Approval',
    activity_type='TODO',
    default_summary='Aprovar proposta',
    due_days_offset=1,
    default_assigned_to=manager,  # ← Sempre criar para manager
    icon='fa-check-circle',
    decoration_type='success',
)
```

### **Exemplo 4: Template Multi-Company**
```python
# Template global (para todas as empresas)
global_template = ActivityTemplate.objects.create(
    name='Welcome Call',
    activity_type='CALL',
    owner_company=None,  # ← NULL = global
)

# Template privado (só para uma empresa)
company = Company.objects.get(name='ACME Corp')
private_template = ActivityTemplate.objects.create(
    name='ACME Specific Task',
    activity_type='TODO',
    owner_company=company,  # ← Só visível para ACME
)
```

---

## 2️⃣ CONFIGURAR WORKFLOWS

Workflows criam activities automaticamente baseado em regras.

### **Exemplo 1: Workflow TRIGGER (Automático)**
```python
from apps.core.models import ActivityWorkflow
from django.contrib.contenttypes.models import ContentType

# Lead model
lead_ct = ContentType.objects.get(app_label='crm', model='lead')

# Se CALL marcada como SUCCESS → criar EMAIL automaticamente
workflow1 = ActivityWorkflow.objects.create(
    name='Lead Nurturing - Call Success',
    description='Quando call for bem sucedida, enviar email de follow-up',
    model=lead_ct,
    trigger_activity_type='CALL',
    trigger_result='SUCCESS',  # ← Só dispara se SUCCESS
    next_activity_template=email_template,
    delay_days=1,  # Email para amanhã
    base_date_type='COMPLETION',  # ← Contar a partir do done_date
    chaining_mode='TRIGGER',  # ← Criar AUTOMATICAMENTE
    sequence=10,
)
```

### **Exemplo 2: Workflow SUGGEST (Com Confirmação)**
```python
# Se CALL marcada como NO_ANSWER → SUGERIR nova call
workflow2 = ActivityWorkflow.objects.create(
    name='Lead Nurturing - No Answer Retry',
    description='Se não atender, sugerir nova tentativa',
    model=lead_ct,
    trigger_activity_type='CALL',
    trigger_result='NO_ANSWER',  # ← Só dispara se NO_ANSWER
    next_activity_template=retry_call_template,
    delay_days=2,  # Retry em 2 dias
    base_date_type='COMPLETION',
    chaining_mode='SUGGEST',  # ← Mostrar MODAL de confirmação
    sequence=20,
)
```

### **Exemplo 3: Base Date - DEADLINE vs COMPLETION**
```python
# Cenário: Call agendada para 10/02, mas feita em 12/02

# Workflow A: Conta a partir da DUE DATE (agendamento)
workflow_deadline = ActivityWorkflow.objects.create(
    trigger_activity_type='CALL',
    next_activity_template=email_template,
    delay_days=3,
    base_date_type='DEADLINE',  # ← Usa due_date (10/02)
)
# Resultado: Email criado para 13/02 (10 + 3)

# Workflow B: Conta a partir da DONE DATE (completamento)
workflow_completion = ActivityWorkflow.objects.create(
    trigger_activity_type='CALL',
    next_activity_template=email_template,
    delay_days=3,
    base_date_type='COMPLETION',  # ← Usa done_date (12/02)
)
# Resultado: Email criado para 15/02 (12 + 3)
```

### **Exemplo 4: Múltiplos Workflows (Sequence)**
```python
# Workflow 1: Se SUCCESS → Email (prioridade alta)
ActivityWorkflow.objects.create(
    trigger_activity_type='CALL',
    trigger_result='SUCCESS',
    next_activity_template=success_email_template,
    sequence=10,  # ← Executa PRIMEIRO
)

# Workflow 2: Se SUCCESS → Meeting (prioridade baixa)
ActivityWorkflow.objects.create(
    trigger_activity_type='CALL',
    trigger_result='SUCCESS',
    next_activity_template=meeting_template,
    sequence=20,  # ← Executa DEPOIS
)
# Ambos executam, mas na ordem: 10 → 20
```

---

## 3️⃣ CRIAR ACTIVITIES MANUALMENTE

### **Método 1: Usando Template**
```python
from apps.crm.models import Lead

lead = Lead.objects.get(pk='...')
user = request.user

# Criar activity a partir do template
activity = call_template.create_activity(
    content_object=lead,  # ← Objeto relacionado
    assigned_to=user,
)
```

### **Método 2: Criar Diretamente**
```python
from apps.core.models import ScheduledActivity
from django.contrib.contenttypes.models import ContentType

ct = ContentType.objects.get_for_model(lead)

activity = ScheduledActivity.objects.create(
    content_type=ct,
    object_id=lead.pk,
    activity_type='CALL',
    summary='Ligar para João Silva',
    description='Discutir proposta de serviço',
    due_date='2026-02-20',
    due_time='14:00',
    assigned_to=user,
    owner_company=user.company,
)
```

### **Método 3: Override de Campos do Template**
```python
# Usar template mas sobrescrever summary e due_date
activity = email_template.create_activity(
    content_object=lead,
    assigned_to=user,
    summary='Email urgente para {{contact_name}}',  # ← Override
    due_date='2026-02-18',  # ← Override (ignora due_days_offset)
)
```

---

## 4️⃣ MARCAR ACTIVITIES COMO DONE

### **Marcar como Completa**
```python
from django.utils import timezone

activity = ScheduledActivity.objects.get(pk='...')

# Marcar como done
activity.is_done = True
activity.result = 'SUCCESS'
activity.feedback = 'Cliente interessado, enviar proposta'
activity.save()  # ← Auto-fill done_date, dispara workflows
```

### **Ver Status da Activity**
```python
# Properties computadas
print(activity.is_overdue)  # True/False
print(activity.is_today)  # True/False
print(activity.status_color)  # 'red', 'yellow', 'green', 'blue'
print(activity.icon)  # '📞', '📧', '👥', etc.
```

### **Validações Automáticas**
```python
# ERRO: Due date no passado
activity = ScheduledActivity(
    due_date='2026-01-01',  # ← Passado
)
activity.clean()  # → ValidationError

# ERRO: Marcar done sem result
activity.is_done = True
activity.save()  # → ValidationError ('Result obrigatório quando done')

# CORRETO
activity.is_done = True
activity.result = 'SUCCESS'
activity.feedback = 'OK'
activity.save()  # ✅
```

---

## 5️⃣ EXEMPLOS REAIS DE USO

### **Caso 1: Lead Nurturing Flow**

```python
# 1. Criar templates
first_call = ActivityTemplate.objects.create(
    name='First Contact Call',
    activity_type='CALL',
    default_summary='Primeira ligação para {{contact_name}}',
    due_days_offset=0,
)

follow_up_email = ActivityTemplate.objects.create(
    name='Follow-up Email',
    activity_type='EMAIL',
    default_summary='Email de follow-up para {{contact_name}}',
    due_days_offset=1,
)

demo_meeting = ActivityTemplate.objects.create(
    name='Product Demo',
    activity_type='MEETING',
    default_summary='Demo do produto para {{company_name}}',
    due_days_offset=3,
)

# 2. Configurar workflows
lead_ct = ContentType.objects.get(app_label='crm', model='lead')

# Workflow 1: Call SUCCESS → Email
ActivityWorkflow.objects.create(
    name='Send Email After Successful Call',
    model=lead_ct,
    trigger_activity_type='CALL',
    trigger_result='SUCCESS',
    next_activity_template=follow_up_email,
    delay_days=0,
    base_date_type='COMPLETION',
    chaining_mode='TRIGGER',
)

# Workflow 2: Email SUCCESS → Meeting
ActivityWorkflow.objects.create(
    name='Schedule Demo After Email',
    model=lead_ct,
    trigger_activity_type='EMAIL',
    trigger_result='SUCCESS',
    next_activity_template=demo_meeting,
    delay_days=3,
    base_date_type='COMPLETION',
    chaining_mode='SUGGEST',  # ← User confirma antes de criar
)

# 3. Usar o flow
lead = Lead.objects.create(name='ACME Corp', ...)

# Criar primeira call
call = first_call.create_activity(
    content_object=lead,
    assigned_to=sales_user,
)

# 4. User marca call como SUCCESS
call.is_done = True
call.result = 'SUCCESS'
call.feedback = 'Cliente muito interessado!'
call.save()

# → Workflow 1 dispara: Email criado AUTOMATICAMENTE
# → Email agendado para hoje

# 5. User marca email como SUCCESS
email = ScheduledActivity.objects.get(...)
email.is_done = True
email.result = 'SUCCESS'
email.save()

# → Workflow 2 dispara: Modal aparece
# → "Quer criar Product Demo para daqui a 3 dias?" [Sim] [Editar] [Não]
```

### **Caso 2: Document Collection Flow**

```python
# Templates
doc_request = ActivityTemplate.objects.create(
    name='Request Documents',
    activity_type='EMAIL',
    default_summary='Solicitar documentos para {{contact_name}}',
)

doc_reminder = ActivityTemplate.objects.create(
    name='Documents Reminder',
    activity_type='WHATSAPP',
    default_summary='Lembrar {{contact_name}} dos documentos',
)

doc_received = ActivityTemplate.objects.create(
    name='Process Documents',
    activity_type='DOCUMENT',
    default_summary='Processar documentos de {{company_name}}',
)

# Workflows
sale_ct = ContentType.objects.get(app_label='sales', model='sale')

# Se email NÃO teve resposta → WhatsApp reminder
ActivityWorkflow.objects.create(
    model=sale_ct,
    trigger_activity_type='EMAIL',
    trigger_result='NO_ANSWER',
    next_activity_template=doc_reminder,
    delay_days=2,
    chaining_mode='TRIGGER',
)

# Se recebeu documentos → Processar
ActivityWorkflow.objects.create(
    model=sale_ct,
    trigger_activity_type='WHATSAPP',
    trigger_result='SUCCESS',
    next_activity_template=doc_received,
    delay_days=0,
    chaining_mode='TRIGGER',
)
```

### **Caso 3: Assinatura de Contrato**

```python
# Template com action_code (avançado)
signature_template = ActivityTemplate.objects.create(
    name='Contract Signature',
    activity_type='SIGNATURE',
    default_summary='Assinar contrato {{contract_number}}',
    action_code='''
# Executado ao marcar como done
from apps.sales.models import Sale
sale = content_object
if activity.result == 'SUCCESS':
    sale.status = 'CONTRACT_SIGNED'
    sale.save()
    # Enviar notificação
    send_notification(sale.owner, 'Contrato assinado!')
''',
)

# Workflow: Signature SUCCESS → Create Invoice
ActivityWorkflow.objects.create(
    trigger_activity_type='SIGNATURE',
    trigger_result='SUCCESS',
    next_activity_template=invoice_template,
    delay_days=1,
    chaining_mode='TRIGGER',
)
```

---

## 🔍 CONSULTAS ÚTEIS

### **Ver todas activities de um Lead**
```python
from apps.core.models import ScheduledActivity
from django.contrib.contenttypes.models import ContentType

lead_ct = ContentType.objects.get_for_model(lead)

activities = ScheduledActivity.objects.filter(
    content_type=lead_ct,
    object_id=lead.pk,
).order_by('due_date')
```

### **Ver activities atrasadas de um User**
```python
from django.utils import timezone

overdue = ScheduledActivity.objects.filter(
    assigned_to=user,
    is_done=False,
    due_date__lt=timezone.now().date(),
)
```

### **Ver activities de hoje**
```python
today = ScheduledActivity.objects.filter(
    assigned_to=user,
    is_done=False,
    due_date=timezone.now().date(),
)
```

### **Ver workflows ativos para Lead**
```python
lead_ct = ContentType.objects.get(app_label='crm', model='lead')

workflows = ActivityWorkflow.objects.filter(
    model=lead_ct,
    is_active=True,
).order_by('sequence')
```

---

## 🎨 UI/UX PATTERNS

### **Cores de Status**
```python
# Template de status badge
def activity_badge(activity):
    colors = {
        'red': '🔴',      # Atrasada
        'yellow': '🟡',   # Hoje
        'green': '🟢',    # Completa
        'blue': '🔵',     # Futura
    }
    return f"{colors[activity.status_color]} {activity.summary}"
```

### **Icons por Tipo**
```python
ICONS = {
    'CALL': '📞',
    'EMAIL': '📧',
    'MEETING': '👥',
    'TODO': '✅',
    'WHATSAPP': '💬',
    'DOCUMENT': '📄',
    'SIGNATURE': '✍️',
}
```

---

## 📝 BOAS PRÁTICAS

1. **Templates Claros**: Use nomes descritivos (`"Follow-up Call after Quote"` em vez de `"Call 1"`)
2. **Delay Realista**: Não criar activities com delay muito curto ou muito longo
3. **Feedback Obrigatório**: Sempre pedir feedback ao marcar como done
4. **SUGGEST para Decisões**: Use `chaining_mode='SUGGEST'` quando user pode querer pular
5. **TRIGGER para Automação**: Use `chaining_mode='TRIGGER'` para flows fixos
6. **Sequence Importa**: Defina sequence em workflows que podem conflitar
7. **Multi-Company**: Sempre setar `owner_company` em ambientes multi-tenant

---

**Próximo:** Implementar signals (Task 3.13.6) para workflows funcionarem automaticamente!
