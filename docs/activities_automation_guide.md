# 🤖 Guia de Automações de Atividades

**Como criar automações (workflows) através do Django Admin**

Este guia mostra como criar cadeias de atividades automáticas sem escrever código - tudo através do Admin Panel!

---

## 🎯 Conceito

Uma **automação** cria automaticamente uma nova atividade quando outra é concluída:

```
📞 CALL concluída com SUCCESS
    ↓ (automático)
📧 EMAIL criado 3 dias depois
    ↓ (se SUCCESS)
✅ TODO "Update CRM" criado 1 dia depois
```

---

## 📋 Pré-requisitos

1. **Templates criados** (já tens 21 defaults)
2. **Acesso ao Admin Panel**: `http://localhost:8000/admin/`
3. **Permissões de staff/superuser**

---

## 🛠️ Como Criar uma Automação

### Passo 1: Aceder ao Admin

1. Vai a `http://localhost:8000/admin/`
2. Login como superuser
3. Clica em **"Activity workflows"** (secção Core)

### Passo 2: Adicionar Workflow

Clica **"Add Activity Workflow"** e preenche:

#### **Secção: Workflow Info**
- **Name**: Nome descritivo (ex: "CALL Success → Follow-up Email")
- **Description**: Opcional, explica o que faz
- **Is active**: ✅ (para ativar)
- **Sequence**: Ordem de execução (se múltiplos workflows, menor = primeiro)

#### **Secção: Trigger Conditions (Quando disparar)**
- **Model**: Escolhe o objeto (Contact, Lead, etc.)
- **Trigger activity type**: Tipo de atividade que dispara (CALL, EMAIL, TODO, etc.)
- **Trigger result**: Resultado que dispara:
  - `SUCCESS` - Bem-sucedida
  - `FAILED` - Falhada
  - `NO_ANSWER` - Sem resposta
  - `CANCELLED` - Cancelada
  - `(Vazio)` - Qualquer resultado

#### **Secção: Action (O que criar)**
- **Next template**: Template da próxima atividade (ex: "Follow-up Email")
- **Delay days**: Dias de espera (0 = hoje, 3 = 3 dias depois)
- **Base date type**:
  - `DEADLINE` - Conta a partir da data limite da atividade original
  - `COMPLETION` - Conta a partir da data de conclusão (recomendado)
- **Chaining mode**:
  - `⚡ TRIGGER` - Cria automaticamente (sem confirmação)
  - `💡 SUGGEST` - Mostra modal a pedir confirmação (implementado em 3.13.8)

---

## 📝 Exemplos Práticos

### Exemplo 1: Seguimento Automático de Chamadas

**Objetivo:** Quando uma chamada é bem-sucedida, criar email de follow-up 3 dias depois.

**Configuração:**
```
Name: CALL Success → Follow-up Email
Model: Contact
Trigger activity type: CALL
Trigger result: SUCCESS
Next template: Follow-up Email
Delay days: 3
Base date type: COMPLETION
Chaining mode: TRIGGER
Is active: ✅
Sequence: 10
```

**Resultado:**
- João completa CALL com SUCCESS → Sistema cria EMAIL automaticamente 3 dias depois

---

### Exemplo 2: Retry em Caso de Falha

**Objetivo:** Se email falhar, tentar ligar 2 dias depois.

**Configuração:**
```
Name: EMAIL Failed → Retry Call
Model: Contact
Trigger activity type: EMAIL
Trigger result: FAILED
Next template: Callback Request
Delay days: 2
Base date type: COMPLETION
Chaining mode: TRIGGER
Is active: ✅
Sequence: 20
```

**Resultado:**
- Maria envia EMAIL que falha → Sistema cria CALL automaticamente 2 dias depois

---

### Exemplo 3: Cadeia Completa de Onboarding

Cria 3 workflows para automatizar onboarding de clientes:

**Workflow 1: First Contact → Welcome Email**
```
Trigger: CALL + SUCCESS
Ação: Email "Welcome Email" em 0 dias (imediato)
```

**Workflow 2: Welcome Email → Collect Documents**
```
Trigger: EMAIL + SUCCESS
Ação: Document "Collect ID Documents" em 1 dia
```

**Workflow 3: Documents → Contract Signature**
```
Trigger: DOCUMENT + SUCCESS
Ação: Signature "Service Agreement" em 2 dias
```

**Resultado da cascata:**
```
📞 CALL (TODAY) → ✅ SUCCESS
    ↓ (imediato)
📧 EMAIL (TODAY) → ✅ SUCCESS
    ↓ (1 dia)
📄 DOCUMENT (TOMORROW) → ✅ SUCCESS
    ↓ (2 dias)
✍️ SIGNATURE (DAY +3)
```

**Tudo automático!** João só completa a primeira CALL, o resto o sistema cria sozinho.

---

## 🔀 Workflows Múltiplos (Bifurcação)

Podes ter **vários workflows** para a mesma trigger condition:

**Cenário:** Quando CALL é bem-sucedida:

**Workflow 1** (Sequence: 10):
```
Trigger: CALL + SUCCESS
Ação: EMAIL "Follow-up" em 3 dias
```

**Workflow 2** (Sequence: 20):
```
Trigger: CALL + SUCCESS
Ação: TODO "Update CRM" em 0 dias (imediato)
```

**Resultado:** Quando CALL bem-sucedida → Cria EMAIL + TODO simultaneamente!

---

## 🎨 Modos de Chaining

### ⚡ TRIGGER (Automático)
- Cria atividade **imediatamente** sem pedir confirmação
- Ideal para: Processos standard, follow-ups previsíveis
- Exemplo: "CALL SUCCESS → sempre criar email 3 dias depois"

### 💡 SUGGEST (Modal de Confirmação)
- Mostra **modal** a pedir confirmação ao utilizador
- Permite ajustar data/detalhes antes de criar
- Ideal para: Ações que dependem de contexto
- Exemplo: "EMAIL FAILED → sugerir retry call, mas deixar utilizador decidir"
- **Nota:** Implementação do modal em Task 3.13.8 (Views)

---

## 🧪 Testar Automações

### Teste Manual via Admin

1. Vai a **Scheduled Activities**
2. Cria uma atividade (ex: CALL ao Contact #1)
3. Marca como concluída:
   - `Is done`: ✅
   - `Result`: SUCCESS
   - `Done date`: Hoje
4. **Guarda**
5. Verifica logs no terminal (se `DEBUG=True`):
   ```
   Activity completed: CALL (result: SUCCESS, id: 123)
   Found 1 matching workflow(s) for activity 123
   ✓ Workflow 'CALL Success → Email' created activity: EMAIL 'Follow-up' (id: 124, due: 2026-02-20)
   ```
6. Volta à lista de atividades → Vês a nova EMAIL criada! 🎉

### Verificar Logs

No terminal onde corre `python manage.py runserver`, vês:

```
INFO Activity completed: CALL (result: SUCCESS, id: 45)
INFO Found 2 matching workflow(s) for activity 45
INFO ✓ Workflow 'CALL Success → Email' created activity: EMAIL 'Follow-up email' (id: 46, due: 2026-02-20)
INFO ✓ Workflow 'CALL Success → Update CRM' created activity: TODO 'Update contact in CRM' (id: 47, due: 2026-02-17)
INFO Workflow execution complete for activity 45: 2 created, 0 suggested
```

---

## 🐛 Troubleshooting

### Automação não dispara?

**Checklist:**
- [ ] Workflow está **Is active** = ✅?
- [ ] **Model** está correto (Contact, Lead, etc.)?
- [ ] **Trigger activity type** match com atividade completada?
- [ ] **Trigger result** match? (ou vazio para qualquer)
- [ ] Atividade foi marcada `is_done = True`?
- [ ] Atividade tem `result` preenchido?
- [ ] Ver logs no terminal para erros

### Workflow cria atividade duplicada?

- Pode ter múltiplos workflows a fazer match
- Verifica `sequence` para definir ordem
- Usa filtros mais específicos em `trigger_result`

### Atividade criada com data errada?

- Verifica `delay_days` (0 = hoje, 1 = amanhã, etc.)
- Verifica `base_date_type`:
  - `DEADLINE` → conta da `due_date` original
  - `COMPLETION` → conta da `done_date` (hoje)

---

## 🎓 Boas Práticas

### 1. Nomes Descritivos
✅ Bom: "CALL Success → Send Follow-up Email (3 days)"
❌ Mau: "Workflow 1"

### 2. Sequence Organizada
- Usa intervalos de 10: 10, 20, 30...
- Permite inserir novos workflows no meio depois

### 3. Testa em Desenvolvimento
- Cria workflows com `is_active = False` primeiro
- Testa manualmente
- Ativa só quando confirmar que funciona

### 4. Documenta Processos Complexos
- Usa campo `description` para explicar lógica
- Especialmente importante para cadeias longas

### 5. Usa SUGGEST para Casos Especiais
- Quando precisas de confirmação humana
- Quando valores dependem de contexto
- Para ações críticas (ex: enviar contrato)

---

## 🚀 Próximos Passos

Agora que tens automações a funcionar:

1. **Cria workflows standard** para processos comuns da tua empresa
2. **Testa com dados reais** em ambiente de desenvolvimento
3. **Ajusta delays** conforme necessidades do negócio
4. **Aguarda Task 3.13.8** para modais de SUGGEST mode
5. **Aguarda Task 3.13.12** para workflows fixtures (templates prontos a usar)

---

## 📚 Recursos

- **Models:** `apps/core/models.py` - ActivityWorkflow, ActivityTemplate
- **Signals:** `apps/core/signals.py` - trigger_activity_workflows
- **Admin:** `apps/core/admin.py` - ActivityWorkflowAdmin
- **Tasks:** `fuet_magico/tasks.md` - Section 3.13

---

**Automação implementada com sucesso! 🎉**

Agora podes criar cadeias complexas de atividades diretamente no Admin Panel, sem escrever uma única linha de código!
