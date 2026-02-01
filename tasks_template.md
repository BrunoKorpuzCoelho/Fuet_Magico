# 📋 TEMPLATE PARA CRIAÇÃO DE FICHEIROS DE TAREFAS

> **Guia de Referência:** Como estruturar ficheiros de tarefas para projetos de desenvolvimento

---

## 🎯 ESTRUTURA OBRIGATÓRIA

### 1️⃣ CABEÇALHO DO PROJETO

```markdown
# 🎯 [NOME DO PROJETO] - DEVELOPMENT CHECKLIST

> **Stack:** [Tecnologias utilizadas - ex: Python 3.12+, Django 5.0+, Vue.js 3, PostgreSQL, Redis, etc]
> **Formato:** Checkboxes hierárquicos (Fase → Tarefa → Sub-tarefa)
> **Objetivo:** [Descrição breve do objetivo - ex: Desenvolvimento do zero - seguir todas as tasks = projeto funcionando ✅]
```

**Exemplo:**
```markdown
# 🎯 SISTEMA DE GESTÃO DE INVENTÁRIO - DEVELOPMENT CHECKLIST

> **Stack:** Python 3.11+, FastAPI, PostgreSQL 15+, Redis, Vue.js 3, Tailwind CSS
> **Formato:** Checkboxes hierárquicos (Fase → Tarefa → Sub-tarefa)
> **Objetivo:** Sistema completo de gestão de inventário com API REST e dashboard
```

---

### 2️⃣ PROGRESSO GERAL (Opcional mas Recomendado)

```markdown
## 📊 PROGRESSO GERAL

- **Fase 1:** 0/X features (0%) - [Nome da Fase]
- **Fase 2:** 0/X features (0%) - [Nome da Fase]
- **Fase 3:** 0/X features (0%) - [Nome da Fase]
...

**TOTAL:** 0/X features (0%)
```

---

### 3️⃣ ESTRUTURA DE FASES

Cada fase segue este formato:

```markdown
# 🚀 FASE X: [NOME DA FASE EM MAIÚSCULAS]

**⏱ Tempo estimado:** [X dias/semanas]
**🎯 Objetivo:** [Descrição clara do que esta fase vai implementar]
**📦 Dependências:** [Fases anteriores necessárias ou "Nenhuma"]

---
```

**Exemplo:**
```markdown
# 🚀 FASE 1: SETUP AMBIENTE E INFRAESTRUTURA

**⏱ Tempo estimado:** 3 dias
**🎯 Objetivo:** Configurar ambiente de desenvolvimento, Docker, banco de dados e estrutura inicial do projeto
**📦 Dependências:** Nenhuma (fase inicial)

---
```

---

### 4️⃣ ESTRUTURA DE TAREFAS

Cada tarefa dentro de uma fase segue este formato:

```markdown
## X.Y [Nome da Tarefa]

[RESUMO BREVE - 1 a 3 linhas explicando o que será implementado nesta tarefa]

- [ ] **[Grupo de sub-tarefas relacionadas]**
  - [ ] Sub-tarefa 1
  - [ ] Sub-tarefa 2
  - [ ] Sub-tarefa 3

- [ ] **[Outro grupo de sub-tarefas]**
  - [ ] Sub-tarefa 1
  - [ ] Sub-tarefa 2

- [ ] **Testing - [Nome da Tarefa]**
  - [ ] Test: [descrição do teste 1]
  - [ ] Test: [descrição do teste 2]
  - [ ] Test: [descrição do teste 3]

---
```

**Exemplo:**
```markdown
## 1.1 Preparação de Ambiente Virtual (venv)

Configurar ambiente virtual Python isolado para desenvolvimento, garantindo que as dependências do projeto não conflitem com outros projetos ou com o sistema.

- [ ] **Criar ambiente virtual**
  - [ ] Executar `python3 -m venv venv` na raiz do projeto
  - [ ] Verificar criação da pasta `venv/`
  - [ ] Adicionar `venv/` ao `.gitignore`

- [ ] **Ativar ambiente virtual**
  - [ ] Linux/Mac: executar `source venv/bin/activate`
  - [ ] Windows: executar `venv\Scripts\activate`
  - [ ] Verificar que prompt mostra `(venv)`

- [ ] **Instalar ferramentas base**
  - [ ] Executar `pip install --upgrade pip`
  - [ ] Executar `pip install wheel setuptools`
  - [ ] Verificar versão: `pip --version`

- [ ] **Testing - Ambiente Virtual**
  - [ ] Test: `which python` aponta para `venv/bin/python`
  - [ ] Test: `pip list` mostra apenas pacotes base
  - [ ] Test: desativar e reativar venv funciona

---
```

---

## ⚠️ REGRAS OBRIGATÓRIAS

### 🔗 DEPENDÊNCIAS ENTRE TAREFAS (REGRA CRÍTICA!)

> ⚠️ **ATENÇÃO:** Esta é a regra mais importante na criação de tarefas!

**PRINCÍPIO FUNDAMENTAL:**
- ✅ **Tarefas anteriores alimentam tarefas posteriores**
- ❌ **Uma tarefa NUNCA pode depender de uma tarefa que vem depois**

**REGRA DE OURO:**
```
Se a Tarefa 3 precisa de algo → isso DEVE ser criado na Tarefa 1 ou Tarefa 2
Se a Tarefa 7 precisa de algo → isso DEVE estar pronto nas Tarefas 1-6
```

**EXEMPLOS:**

✅ **CORRETO:**
```
Tarefa 1.1: Criar estrutura de pastas (cria app/models/)
Tarefa 1.2: Criar models.py (usa app/models/ da tarefa 1.1) ✓
Tarefa 1.3: Criar schemas.py (usa models da tarefa 1.2) ✓
```

❌ **ERRADO:**
```
Tarefa 1.1: Criar user schema (precisa de User model)
Tarefa 1.2: Criar product schema (precisa de Product model)
Tarefa 1.5: Criar models.py (cria User e Product models) ✗ ERRADO!
```
↑ Tarefa 1.1 e 1.2 dependem da 1.5 que vem depois!

**COMO CORRIGIR:**
```
Tarefa 1.1: Criar models.py (cria User e Product models) ✓
Tarefa 1.2: Criar user schema (usa User model da tarefa 1.1) ✓
Tarefa 1.3: Criar product schema (usa Product model da tarefa 1.1) ✓
```

**VALIDAÇÃO CONSTANTE:**
- Ao criar cada tarefa, pergunte: "Esta tarefa depende de algo?"
- Se SIM: "Esse algo já foi criado em tarefas anteriores?"
- Se NÃO: **REORGANIZE** - crie a dependência primeiro!

---

### ✅ O QUE DEVE CONTER:

1. **Título do Projeto** com as tecnologias no cabeçalho
2. **Fases numeradas** (Fase 1, Fase 2, etc.) com nomes descritivos
3. **Tarefas numeradas hierarquicamente** (1.1, 1.2, 2.1, 2.2, etc.)
4. **Resumo breve** de 1-3 linhas após cada título de tarefa
5. **Checklists** organizados em grupos lógicos
6. **Seção de Testing** no final de cada tarefa
7. **Separador `---`** entre tarefas
8. **DEPENDÊNCIAS RESPEITADAS** - tarefas sempre em ordem correta

### ❌ O QUE NÃO PODE CONTER:

1. **NUNCA incluir código** diretamente nas tarefas
2. **NUNCA incluir comandos completos** (exceto em sub-tarefas específicas)
3. **NUNCA incluir outputs de código**
4. **NUNCA incluir explicações técnicas longas** - só ações objetivas

---

## 📐 HIERARQUIA DE NUMERAÇÃO

```
FASE 1: NOME DA FASE
├── 1.1 Nome da Tarefa
│   ├── Resumo
│   ├── - [ ] Grupo 1
│   │   ├── - [ ] Sub-tarefa 1.1
│   │   └── - [ ] Sub-tarefa 1.2
│   └── - [ ] Testing
│
├── 1.2 Nome da Tarefa
│   ├── Resumo
│   └── ...
│
FASE 2: NOME DA FASE
├── 2.1 Nome da Tarefa
└── 2.2 Nome da Tarefa
```

---

## 🎨 EXEMPLO COMPLETO DE FASE

```markdown
# 🚀 FASE 1: CONFIGURAÇÃO INICIAL

**⏱ Tempo estimado:** 2 dias
**🎯 Objetivo:** Preparar ambiente de desenvolvimento e estrutura base do projeto
**📦 Dependências:** Nenhuma

---

## 1.1 Ambiente Virtual Python (venv)

Criar ambiente virtual isolado para desenvolvimento, garantindo separação de dependências e evitando conflitos com outros projetos.

- [ ] **Criar venv**
  - [ ] Executar `python3 -m venv venv`
  - [ ] Verificar criação de `venv/`
  - [ ] Adicionar `venv/` ao `.gitignore`

- [ ] **Configurar ativação**
  - [ ] Linux/Mac: `source venv/bin/activate`
  - [ ] Windows: `venv\Scripts\activate`
  - [ ] Confirmar prompt com `(venv)`

- [ ] **Testing - Ambiente Virtual**
  - [ ] Test: `which python` aponta para venv
  - [ ] Test: venv ativa e desativa corretamente

---

## 1.2 Instalação de Dependências

Instalar todas as bibliotecas e frameworks necessários para o desenvolvimento do projeto usando pip e requirements.txt.

- [ ] **Criar requirements.txt**
  - [ ] Criar ficheiro na raiz
  - [ ] Adicionar FastAPI>=0.104.0
  - [ ] Adicionar uvicorn[standard]>=0.24.0
  - [ ] Adicionar sqlalchemy>=2.0.0

- [ ] **Instalar dependências**
  - [ ] Executar `pip install -r requirements.txt`
  - [ ] Verificar instalação sem erros
  - [ ] Executar `pip freeze > requirements.lock`

- [ ] **Testing - Dependências**
  - [ ] Test: `pip list` mostra todos os pacotes
  - [ ] Test: `python -c "import fastapi"` sem erros
  - [ ] Test: `fastapi --version` retorna versão

---

# 🚀 FASE 2: BACKEND API

**⏱ Tempo estimado:** 1 semana
**🎯 Objetivo:** Criar API REST completa com autenticação e CRUD
**📦 Dependências:** Fase 1

---

## 2.1 Estrutura de Pastas

Organizar projeto em módulos separados seguindo boas práticas de arquitetura, facilitando manutenção e escalabilidade.

- [ ] **Criar estrutura base**
  - [ ] Criar pasta `app/`
  - [ ] Criar pasta `app/api/`
  - [ ] Criar pasta `app/models/`
  - [ ] Criar pasta `app/schemas/`
  - [ ] Criar `__init__.py` em cada pasta

- [ ] **Criar arquivos principais**
  - [ ] Criar `app/main.py`
  - [ ] Criar `app/config.py`
  - [ ] Criar `app/database.py`

- [ ] **Testing - Estrutura**
  - [ ] Test: todas as pastas existem
  - [ ] Test: imports funcionam corretamente
  - [ ] Test: estrutura segue padrão definido

---
```

---

## 🔑 PONTOS-CHAVE

### ✨ Características de Boas Tarefas:

- **Objetivas:** Cada checkbox é uma ação clara e específica
- **Testáveis:** Sempre incluir seção de Testing
- **Sequenciais:** Ordem lógica de execução - dependências sempre antes!
- **Sem dependências inversas:** Se tarefa X precisa de Y, então Y vem antes de X
- **Independentes:** Cada tarefa pode ser completada de forma autônoma (mas respeitando ordem)
- **Resumo claro:** 1-3 linhas explicando o propósito

### 🎯 Foco em:

- **Ações, não código:** "Criar ficheiro X" em vez de mostrar o código
- **Checklists, não tutoriais:** Passos para marcar, não explicações longas
- **Testes sempre:** Cada tarefa tem validação

---

## 📝 TEMPLATE RÁPIDO PARA COPIAR

```markdown
## X.Y [Nome da Tarefa]

[Resumo breve em 1-3 linhas do que será implementado]

- [ ] **[Grupo de ações]**
  - [ ] Ação 1
  - [ ] Ação 2
  - [ ] Ação 3

- [ ] **Testing - [Nome da Tarefa]**
  - [ ] Test: descrição do teste
  - [ ] Test: descrição do teste

---
```

---

## 🚀 COMO USAR ESTE TEMPLATE

1. **Defina o projeto:** Nome e tecnologias no cabeçalho
2. **Liste as fases:** Identifique as grandes etapas (Setup, Frontend, Backend, Deploy, etc.)
3. **Detalhe cada fase:** Para cada fase, crie tarefas numeradas (1.1, 1.2, etc.)
4. **Adicione resumos:** Cada tarefa tem 1-3 linhas explicando o objetivo
5. **Crie checklists:** Liste todas as ações necessárias em checkboxes
6. **Inclua testes:** Sempre adicione seção de Testing
7. **Separe tarefas:** Use `---` entre cada tarefa

---

## ✅ CHECKLIST DE VALIDAÇÃO

Antes de considerar o ficheiro de tarefas completo, verifique:

- [ ] Título do projeto está claro com tecnologias listadas
- [ ] Todas as fases estão numeradas e nomeadas
- [ ] Cada tarefa tem número hierárquico (X.Y)
- [ ] Cada tarefa tem resumo de 1-3 linhas
- [ ] Todas as ações estão em checkboxes
- [ ] Não há código dentro das tarefas
- [ ] Cada tarefa tem seção Testing
- [ ] Tarefas estão separadas por `---`
- [ ] Ordem das tarefas é lógica e sequencial
- [ ] **DEPENDÊNCIAS VALIDADAS:** Nenhuma tarefa depende de tarefas posteriores
- [ ] **ORDEM CORRETA:** Se Tarefa X precisa de Y, então Y aparece antes de X

---

**🎯 Este template garante ficheiros de tarefas profissionais, organizados e fáceis de seguir!**