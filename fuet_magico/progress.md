# 📊 WORKFLOW PROGRESS TRACKER

---

<!-- ⚠️ ATENÇÃO AI: NÃO APAGAR ESTA SEÇÃO ⚠️ -->
<!-- Esta seção de INSTRUÇÕES DAS 7 FASES deve SEMPRE permanecer -->
<!-- Apenas apague o conteúdo abaixo da seção "WORKFLOW ATUAL" na FASE 7 -->

## 📋 INSTRUÇÕES DAS 7 FASES

<!-- ⚠️ INÍCIO DA SEÇÃO PERMANENTE - NÃO APAGAR ⚠️ -->

### FASE 0: Compreensão da Solicitação

**Objetivo:** Garantir entendimento claro e alinhamento sobre o que será implementado.

- ❌ NÃO criar ficheiros
- ❌ NÃO mostrar código
- ✅ APENAS chat para entendimento
- ✅ Criar plano completo das 7 fases em progress.md
- ✅ Pedir confirmação: "Posso avançar para FASE 1?"

### FASE 1: Análise do Contexto do Projeto

**Objetivo:** Compreender o estado atual do projeto antes de implementar.

- ✅ Ler cubix_one/core/structure.md
- ✅ Identificar módulos existentes que possam ser afetados
- ✅ Mapear dependências e integrações necessárias
- ✅ Atualizar progress.md com descobertas
- ✅ Pedir confirmação: "Posso avançar para FASE 2?"

### FASE 2: Análise e Proposta de Implementação

**Objetivo:** Apresentar opções e fazer perguntas para decisão.

- ✅ Ler cubix_one/core/rules.md (69+ regras)
- ✅ Ler cubix_one/core/cyber_security.md (130+ regras)
- ❌ NÃO criar ficheiros
- ❌ NÃO mostrar código
- ✅ Apresentar 3-5 opções de implementação
- ✅ Fazer perguntas de decisão (formato múltipla escolha)
- ✅ Considerar requisitos de segurança
- ✅ Atualizar progress.md com opção escolhida
- ✅ Pedir confirmação: "Posso avançar para FASE 3?"

### FASE 3: Clarificação e Ajustes

**Objetivo:** Resolver dúvidas e ajustar a implementação conforme feedback.

- ✅ Processar respostas às perguntas da FASE 2
- ✅ Ajustar abordagem se necessário
- ✅ Confirmar consenso total
- ✅ Atualizar progress.md com ajustes finais
- ✅ Pedir confirmação: "Posso avançar para FASE 4?"

### FASE 4: Estrutura de Diretórios e Ficheiros

**Objetivo:** Definir a estrutura completa de ficheiros seguindo arquitetura modular.

- ✅ Apresentar estrutura de diretórios com legenda (⭐📝📁)
- ✅ Mostrar conteúdo dos **init**.py
- ✅ Explicar cada ficheiro
- ✅ Listar dependências
- ✅ Atualizar progress.md com estrutura aprovada
- ✅ Pedir confirmação: "Posso avançar para FASE 5?"

### FASE 5: Implementação do Código

**Objetivo:** Criar/modificar ficheiros seguindo todas as regras estabelecidas.

- ✅ Criar ficheiros na ordem correta
- ✅ Seguir TODAS as regras (rules.md + cyber_security.md)
- ✅ Anunciar cada ficheiro antes de criar
- ✅ Validar checklist de segurança
- ✅ Atualizar progress.md com ficheiros criados
- ✅ Pedir confirmação: "Posso avançar para FASE 6?"

### FASE 6: Documentação

**Objetivo:** Documentar a implementação e marcar tarefas como concluídas.

- ✅ Marcar checkboxes em tasks.md
- ✅ Criar resumo da implementação
- ✅ Documentar próximos passos
- ✅ Atualizar progress.md
- ✅ Pedir confirmação: "Posso avançar para FASE 7?"

### FASE 7: Finalização e Limpeza

**Objetivo:** Validar conformidade com regras e limpar progress.md.

- ✅ Validar compliance com regras aplicáveis
- ✅ Apresentar resumo de conformidade
- ✅ Checklist final de implementação
- ✅ LIMPAR TODO o conteúdo de progress.md (exceto estas instruções)
- ✅ Apresentar resumo final ao utilizador

<!-- ⚠️ FIM DA SEÇÃO PERMANENTE - NÃO APAGAR ⚠️ -->

---

<!-- ============================================================ -->
<!-- ⚠️ ATENÇÃO AI: A PARTIR DAQUI PODE SER APAGADO NA FASE 7 ⚠️ -->
<!-- Apenas o conteúdo ABAIXO desta linha deve ser limpo        -->
<!-- As INSTRUÇÕES DAS 7 FASES acima devem SEMPRE permanecer    -->
<!-- ============================================================ -->

---
## 🔄 MIGRAÇÃO: ActivityType como Tabela Separada

**Objetivo:** Converter `activity_type` de `CharField(choices=[...])` hardcoded para `ForeignKey(ActivityType)` — permitindo que o utilizador crie/edite/elimine tipos de atividade sem tocar no código.

**Estado:** 🟡 Em progresso

---

### 📋 FICHEIROS A ALTERAR

#### 1. `apps/core/models.py`
- [ ] Criar novo modelo `ActivityType` (acima de `ScheduledActivity`)
  - Campos: `name` (ex: "Phone Call"), `code` (slug único ex: "CALL"), `is_active`
  - **SEM** `icon_svg`, `icon_color` — o visual fica no blueprint (`ScheduledActivity`)
- [ ] `ScheduledActivity.activity_type`: `CharField(choices)` → `ForeignKey(ActivityType)`
- [ ] Remover `ACTIVITY_TYPE_CHOICES` de `ScheduledActivity`
- [ ] Remover `default_icon_emoji` property (era baseada nos choices hardcoded)
- [ ] `ActivityWorkflow.trigger_activity_type`: `CharField(choices=ScheduledActivity.ACTIVITY_TYPE_CHOICES)` → `ForeignKey(ActivityType)`
- [ ] Remover referência a `ScheduledActivity.ACTIVITY_TYPE_CHOICES` em `ActivityWorkflow`
- [ ] Atualizar `ActivityWorkflow.matches_activity()` (comparação era por string, passa a ser por FK)
- [ ] **NÃO alterar** `ChatterActivity.ACTIVITY_TYPE_CHOICES` — esses são tipos de auditoria (CREATE, UPDATE, etc.), completamente diferentes

#### 2. `apps/core/migrations/`
- [ ] `python manage.py makemigrations core --name create_activity_type_model`
- [ ] Fazer data migration para criar os 7 tipos padrão (CALL, EMAIL, MEETING, TODO, WHATSAPP, DOCUMENT, SIGNATURE)
- [ ] Limpar tabela `core_scheduledactivity` antes da migration de FK (dados inválidos sem ActivityType FK)

#### 3. `apps/core/admin.py`
- [ ] Registar `ActivityTypeAdmin` com list_display, search_fields, list_filter
- [ ] Atualizar `ScheduledActivityAdmin`: `activity_type` passa de filter por string para filter por FK
- [ ] Atualizar `ActivityWorkflowAdmin`: mesmo

#### 4. `apps/core/forms.py`
- [ ] `ScheduledActivityForm.activity_type`: será automaticamente `ModelChoiceField` (Django gera automaticamente para FK)
- [ ] Garantir queryset correto (filtrar por `is_active=True` e `owner_company` global ou da empresa)
- [ ] Atualizar widget do select para dark mode

#### 5. `apps/core/signals.py`
- [ ] `activity_type = instance.step.activity.activity_type` → retorna agora objeto `ActivityType`, não string
- [ ] `trigger_activity_type=activity_type` no filter dos workflows → continua a funcionar (FK vs FK)
- [ ] Adaptar logs (`.name` ou `.code` em vez de string direta)

#### 6. `apps/crm/views.py`
- [ ] Pesquisa: `activity_type__icontains` → `activity_type__name__icontains`
- [ ] Order: `activity_type` → `activity_type__name`
- [ ] Passar `ActivityType.objects.filter(is_active=True)` ao contexto do form (para queryset)

#### 7. `apps/crm/urls.py`
- [ ] Adicionar URLs CRUD para `ActivityType`:
  - `activity-types/` → list
  - `activity-types/new/` → create
  - `activity-types/<uuid>/edit/` → edit
  - `activity-types/bulk-delete/` → bulk delete

#### 8. `apps/crm/views.py` (novas views)
- [ ] `activity_types_list_view`
- [ ] `activity_type_create_view`
- [ ] `activity_type_edit_view`
- [ ] `bulk_delete_activity_types`

#### 9. Templates
- [ ] `templates/crm/activities_list.html`: `{{ activity.get_activity_type_display }}` → `{{ activity.activity_type.name }}`
- [ ] `templates/crm/activity_form.html`: select já funciona com ModelChoiceField (testar dark mode)
- [ ] Criar `templates/crm/activity_type_list.html`
- [ ] Criar `templates/crm/activity_type_form.html`
- [ ] Adicionar link "Tipos de Atividade" ao menu Configuração em `crm_navbar.html` e `crm_navbar_simple.html`

#### 10. `apps/core/management/commands/setup_activity_templates.py`
- [ ] Importar `ActivityType`
- [ ] Primeiro criar/garantir os 7 tipos (`get_or_create` por `code`)
- [ ] Mudar `'activity_type': 'CALL'` → `'activity_type': ActivityType.objects.get(code='CALL')`

---

### 🔢 ORDEM DE EXECUÇÃO

1. Modelo `ActivityType` + atualizar `ScheduledActivity` + `ActivityWorkflow`
2. `makemigrations` → data migration → `migrate`
3. Limpar `core_scheduledactivity` existente (re-seed depois)
4. Signals + Forms + Admin
5. Views + URLs (CRUD ActivityType + adaptar existentes)
6. Templates
7. Seed command atualizado → correr `setup_activity_templates --clear`
8. `manage.py check` → 0 issues

---

### ✅ PROGRESSO

- [ ] Passo 1: Modelos
- [ ] Passo 2: Migrações
- [ ] Passo 3: Limpar dados antigos
- [ ] Passo 4: Signals + Forms + Admin
- [ ] Passo 5: Views + URLs
- [ ] Passo 6: Templates
- [ ] Passo 7: Seed + Verificação final