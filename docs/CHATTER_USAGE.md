# 📬 Sistema de Chatter - Guia de Uso

Sistema de comunicação universal estilo Odoo para Django. Funciona com **QUALQUER modelo** (Lead, Contact, Sale, Purchase, etc.) usando ContentType framework.

---

## ✨ Features

- ✅ **Universal**: Funciona com qualquer modelo Django via GenericForeignKey
- ✅ **5 Tabs**: WhatsApp, Enviar Mensagem, Nota, Log (audit), Atividade
- ✅ **Detecção Automática**: Identifica automaticamente o modelo e ID do objeto
- ✅ **APIs REST**: Endpoints prontos para criar mensagens/notas
- ✅ **Autocomplete @**: Mencionar usuários com autocomplete
- ✅ **Timeline**: Histórico completo de ações
- ✅ **Scrollbar Customizada**: Dourada, fina (6px), dark mode

---

## 📦 Componentes Criados

### 1. **Modelos** (`apps/core/models.py`)
- `ChatterMessage`: Emails + notas internas com GenericForeignKey
- `ChatterActivity`: Timeline de atividades (audit log)

### 2. **Template Tags** (`apps/core/templatetags/chatter_tags.py`)
- `content_type`: Converte objeto Django para "app_label.model"
  ```django
  {{ lead|content_type }} → "crm.lead"
  {{ contact|content_type }} → "contacts.contact"
  ```

### 3. **Componente Reutilizável** (`templates/components/chatter.html`)
- HTML completo com Alpine.js
- Inclui APIs, autocomplete, tabs, UI completa

### 4. **ChatterMixin** (`apps/core/views.py`)
- Mixin para DetailView que adiciona automaticamente:
  - `chatter_messages`: Emails + notas
  - `activities`: Timeline de ações
  - `whatsapp_messages`: WhatsApp (placeholder Fase 12)

### 5. **APIs REST** (`apps/core/views.py` + `apps/core/urls.py`)
- `POST /api/chatter/message/`: Criar email ou nota
- `POST /api/chatter/whatsapp/`: Enviar WhatsApp (placeholder)
- `GET /api/users/search/?q=john`: Autocomplete @ mentions

---

## 🚀 Como Usar

### **Passo 1: Criar uma DetailView com ChatterMixin**

```python
# apps/crm/views.py
from django.views.generic import DetailView
from apps.core.views import ChatterMixin
from .models import Lead

class LeadDetailView(ChatterMixin, DetailView):
    model = Lead
    template_name = 'crm/lead_detail.html'
    context_object_name = 'lead'
```

**Resultado:** A view adiciona automaticamente ao context:
- `chatter_messages` (QuerySet)
- `activities` (QuerySet)
- `whatsapp_messages` (lista vazia por enquanto)

---

### **Passo 2: Incluir o Componente no Template**

```django
{# templates/crm/lead_detail.html #}
{% extends 'base.html' %}
{% load static chatter_tags %}

{% block content %}
<div class="flex gap-0">
    <!-- FORMULÁRIO/CONTEÚDO (Esquerda - 70%) -->
    <div class="flex-1" style="max-width: 70%;">
        <div class="p-6">
            <h1>{{ lead.title }}</h1>
            <p>{{ lead.description }}</p>
            <!-- ... resto do conteúdo ... -->
        </div>
    </div>
    
    <!-- CHATTER (Direita - 30%) -->
    {% include 'components/chatter.html' with object=lead %}
</div>
{% endblock %}
```

**✨ É só isso!** O componente detecta automaticamente que é um Lead.

---

### **Passo 3: Adicionar a Rota**

```python
# apps/crm/urls.py
from django.urls import path
from . import views

app_name = 'crm'

urlpatterns = [
    # ...
    path('lead/<uuid:pk>/', views.LeadDetailView.as_view(), name='lead_detail'),
]
```

---

## 🎯 Funcionamento Interno

### **1. Detecção Automática do Objeto**

```django
{# No template #}
{% include 'components/chatter.html' with object=lead %}

{# Internamente, o componente faz: #}
<div x-data="chatterComponent('{{ object|content_type }}', '{{ object.id }}')">
{# Resultado: #}
<div x-data="chatterComponent('crm.lead', '123e4567-...')">
```

### **2. APIs Recebem object_type e object_id**

Quando o usuário envia uma mensagem:

```javascript
// JavaScript (dentro do componente)
fetch('/api/chatter/message/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        object_type: 'crm.lead',     // ← Auto-detectado!
        object_id: '123e4567-...',   // ← Auto-detectado!
        message_type: 'NOTE',
        body: 'Importante: cliente interessado'
    })
})
```

### **3. Backend Processa**

```python
# apps/core/views.py - chatter_create_message()
app_label, model = "crm", "lead"  # Parse "crm.lead"
content_type = ContentType.objects.get(app_label="crm", model="lead")

# Criar mensagem associada ao Lead
ChatterMessage.objects.create(
    content_type=content_type,
    object_id=object_id,  # UUID do Lead
    author=request.user,
    message_type='NOTE',
    body='Importante: cliente interessado'
)

# Criar atividade (audit log)
ChatterActivity.objects.create(
    content_type=content_type,
    object_id=object_id,
    user=request.user,
    activity_type='COMMENT',
    description='added an internal note'
)
```

---

## 💡 Exemplos para Outros Modelos

### **Contacts**

```python
# apps/contacts/views.py
from apps.core.views import ChatterMixin

class ContactDetailView(ChatterMixin, DetailView):
    model = Contact
    template_name = 'contacts/contact_detail.html'
```

```django
{# templates/contacts/contact_detail.html #}
{% include 'components/chatter.html' with object=contact %}
```

**Resultado:** `object_type = "contacts.contact"`

### **Sales**

```python
# apps/sales/views.py
class SaleOrderDetailView(ChatterMixin, DetailView):
    model = SaleOrder
    template_name = 'sales/saleorder_detail.html'
```

```django
{# templates/sales/saleorder_detail.html #}
{% include 'components/chatter.html' with object=sale %}
```

**Resultado:** `object_type = "sales.saleorder"`

---

## 🎨 Personalização

### **Layout 70/30 ou 100%**

**Opção 1: Chatter à direita (70/30)**
```django
<div class="flex gap-0">
    <div class="flex-1" style="max-width: 70%;">
        <!-- Conteúdo -->
    </div>
    {% include 'components/chatter.html' with object=lead %}
</div>
```

**Opção 2: Chatter full width abaixo**
```django
<div class="p-6">
    <!-- Conteúdo principal -->
    <h1>{{ lead.title }}</h1>
    <!-- ... -->
</div>

<!-- Chatter full width -->
<div class="border-t border-gray-700 mt-8">
    {% include 'components/chatter.html' with object=lead %}
</div>
```

### **Desabilitar Tabs**

Editar `templates/components/chatter.html` e remover ou ocultar tabs:

```html
<!-- Exemplo: Remover tab WhatsApp -->
<!-- <button type="button" @click="activeTab = 'whatsapp'">...</button> -->
```

---

## 🔌 APIs Disponíveis

### **1. Criar Mensagem/Nota**

```
POST /api/chatter/message/
Content-Type: application/json

{
    "object_type": "crm.lead",
    "object_id": "uuid-here",
    "message_type": "NOTE",      // "EMAIL" ou "NOTE"
    "subject": "Assunto",        // Opcional, só para EMAIL
    "body": "Conteúdo da mensagem"
}
```

**Resposta:**
```json
{
    "success": true,
    "message": "Message created successfully",
    "id": "uuid-da-mensagem"
}
```

### **2. Enviar WhatsApp (Placeholder Fase 12)**

```
POST /api/chatter/whatsapp/
Content-Type: application/json

{
    "object_type": "crm.lead",
    "object_id": "uuid-here",
    "message": "Olá! Como posso ajudar?"
}
```

**Resposta:**
```json
{
    "success": true,
    "message": "PLACEHOLDER - WhatsApp integration will be implemented in Phase 12"
}
```

### **3. Autocomplete @mentions**

```
GET /api/users/search/?q=john
```

**Resposta:**
```json
[
    {
        "id": "uuid",
        "name": "John Doe",
        "username": "johndoe"
    },
    {
        "id": "uuid",
        "name": "Johnny Walker",
        "username": "jwalker"
    }
]
```

---

## 🛠️ Estrutura de Ficheiros

```
Fuet_Magico/
├── apps/
│   └── core/
│       ├── models.py                     # ChatterMessage, ChatterActivity
│       ├── views.py                      # ChatterMixin, APIs REST
│       ├── urls.py                       # Rotas das APIs
│       ├── admin.py                      # Admin para modelos
│       └── templatetags/
│           ├── __init__.py
│           └── chatter_tags.py           # Filtro content_type
│
└── templates/
    └── components/
        └── chatter.html                  # Componente reutilizável
```

---

## ✅ Checklist de Implementação

Para usar o chatter num novo modelo:

- [ ] **View**: Adicionar `ChatterMixin` à DetailView
- [ ] **Template**: Incluir `{% include 'components/chatter.html' with object=meu_objeto %}`
- [ ] **Template Tags**: Carregar `{% load chatter_tags %}` no topo
- [ ] **Layout**: Usar layout 70/30 ou full width
- [ ] **Testar**: Criar nota interna
- [ ] **Testar**: Ver timeline de atividades

---

## 🚧 Roadmap

### ✅ Implementado (Fase 3.12)
- [x] Modelos ChatterMessage e ChatterActivity
- [x] Template tag `content_type`
- [x] Componente reutilizável chatter.html
- [x] ChatterMixin para DetailViews
- [x] APIs REST para mensagens/notas
- [x] Admin para ChatterMessage e ChatterActivity
- [x] Autocomplete @ para mentions
- [x] Timeline de atividades

### 🔜 Próximos Passos
- [ ] **Fase 3.9**: Envio real de emails via SMTP + Celery
- [ ] **Fase 12**: Integração WhatsApp API
- [ ] **Futuro**: Upload de anexos
- [ ] **Futuro**: Notificações em tempo real
- [ ] **Futuro**: Agendamento de atividades

---

## 📚 Documentação Adicional

- **Django ContentTypes**: https://docs.djangoproject.com/en/5.0/ref/contrib/contenttypes/
- **GenericForeignKey**: https://docs.djangoproject.com/en/5.0/ref/contrib/contenttypes/#generic-relations
- **Alpine.js**: https://alpinejs.dev/
- **Tailwind CSS**: https://tailwindcss.com/

---

## 🆘 Troubleshooting

### **1. "content_type is not a registered filter"**
**Solução:** Verificar se `{% load chatter_tags %}` está no topo do template.

### **2. "No context for object"**
**Solução:** Verificar se a view herda de `ChatterMixin` e usa `DetailView`.

### **3. "API returns 403 Forbidden"**
**Solução:** Verificar se CSRF token está incluído nas requests Ajax.

### **4. "Autocomplete @ não aparece"**
**Solução:** Verificar se Alpine.js está carregado no base.html.

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Consultar `fuet_magico/tasks.md` (Fase 3.12)
2. Ver exemplos nesta documentação
3. Verificar logs: `/logs/django.log`

---

**Desenvolvido em Fevereiro 2026** 🚀
