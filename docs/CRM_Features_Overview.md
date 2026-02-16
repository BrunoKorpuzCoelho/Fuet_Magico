# 🎯 FUET MÁGICO - Sistema CRM
## Overview Completo de Funcionalidades

---

## 📋 Índice

1. [Gestão de Estágios (Pipeline)](#1-gestão-de-estágios-pipeline)
2. [Gestão de Leads/Oportunidades](#2-gestão-de-leadsoportunidades)
3. [Sistema de Atividades](#3-sistema-de-atividades)
4. [Pipeline Kanban (Vista Principal)](#4-pipeline-kanban-vista-principal)
5. [Sistema de Tags](#5-sistema-de-tags)
6. [Geração Automática de Leads](#6-geração-automática-de-leads)
7. [Integrações e Relações](#7-integrações-e-relações)
8. [Conversão de Leads](#8-conversão-de-leads)
9. [Multi-Company](#9-multi-company)
10. [Interface e UX](#10-interface-e-ux)

---

## 1. Gestão de Estágios (Pipeline)

### 1.1 Estágios Personalizáveis (CRMStage)
- **Estágios customizáveis** por empresa
- **Ordenação drag-and-drop** com sequência numérica
- **Cores personalizadas** (hex colors) para identificação visual
- **Estágios especiais**:
  - Estágio de vitória (`is_won_stage`)
  - Estágio de perda (`is_lost_stage`)
- **Collapse automático** (`fold_by_default`) para estágios menos usados
- **Routing em dias** (`routing_in_days`) para highlights de oportunidades paradas
- **Estágios padrão** criados automaticamente:
  - **New** (Novo) - cinza, routing 7 dias
  - **Qualified** (Qualificado) - azul
  - **Proposition** (Proposta) - amarelo
  - **Won** (Ganho) - verde, colapsado
  - **Lost** (Perdido) - vermelho, colapsado

### 1.2 CRUD de Estágios
- **Lista de estágios** com visualização de ordem e configurações
- **Criação de novos estágios** com validações
- **Edição inline** de sequência e configurações
- **Soft delete** (arquivamento sem perda de dados)
- **Reordenação visual** com Sortable.js
- **Validações**:
  - Nomes únicos por empresa
  - Cores em formato hexadecimal
  - Routing days ≥ 0

---

## 2. Gestão de Leads/Oportunidades

### 2.1 Modelo de Lead Completo
- **Informações básicas**:
  - Título da oportunidade
  - Descrição detalhada
  - Contacto associado (opcional)
  - Nome, email e telefone do contacto
- **Valores e probabilidade**:
  - Receita esperada (Expected Revenue)
  - Probabilidade de fecho (0-100%)
  - Priority stars (LOW: ⭐, MEDIUM: ⭐⭐, HIGH: ⭐⭐⭐)
- **Tracking e controlo**:
  - Estágio atual (FK para CRMStage)
  - Fonte da lead (Website, Referral, Cold Call, Social Media)
  - Data prevista de fecho
  - Vendedor responsável (assigned_to)
  - Motivo de perda (obrigatório se Lost)
- **Metadata**:
  - Data de criação
  - Última atualização de estágio
  - Empresa proprietária (multi-company)
  - Campo de notas com editor rico (Quill)

### 2.2 Formulário de Criação/Edição
- **Layout estilo Odoo** com design moderno
- **Campos inteligentes**:
  - Autocomplete de contactos com busca rápida
  - Date picker customizado (Air Datepicker) com tema dark
  - Dropdown de vendedor sem avatar
  - Campos numéricos sem spinners
  - Editor de texto rico (Quill) para notas
- **Barra de estágios superior**:
  - Navegação visual entre estágios
  - Fundo dourado para estágio selecionado
  - Texto branco em estágios ativos
- **Sistema de tags** com autocomplete e criação rápida
- **Auto-preenchimento**:
  - Vendedor = utilizador atual
  - Estágio = NEW (primeiro estágio)
- **Tabs organizadas**:
  - Notas (com editor Quill)
  - Contactos associados
- **Validações em tempo real**:
  - Receita esperada ≥ 0
  - Probabilidade entre 0-100%
  - Motivo obrigatório ao marcar como perdida

### 2.3 Vista de Detalhes
- **Layout de duas colunas**:
  - Informação principal (esquerda)
  - Activities/Chatter (direita)
- **Smart buttons** com contadores:
  - Vendas geradas (se convertida)
  - Documentos anexados
  - Atividades pendentes
- **Timeline de eventos** (AuditLog)
- **Histórico de mudanças** de estágio

### 2.4 Vista de Lista (Tabular)
- **Tabela completa** com:
  - Checkboxes para seleção múltipla
  - Título e contacto
  - Badge do estágio
  - Valor e barra de probabilidade
  - Avatar do responsável
  - Ações rápidas
- **Filtros avançados**:
  - Por estágio
  - Por responsável
  - Por período de criação
  - Por fonte
  - Por prioridade
- **Busca multi-campo**:
  - Título
  - Contacto
  - Descrição
- **Ordenação** por:
  - Receita esperada
  - Probabilidade
  - Data prevista de fecho
- **Paginação** (50 itens por página)
- **Bulk actions**:
  - Mudar estágio em massa
  - Atribuir responsável
  - Arquivar múltiplas leads

### 2.5 KPIs e Métricas
- **Total de Leads** no sistema
- **Valor Total do Pipeline**
- **Taxa de Conversão** (Won/Total)
- **Leads criadas este mês**
- **Receita prevista** por período

---

## 3. Sistema de Atividades

### 3.1 Tipos de Atividades
- **To-Do** (✅) - Tarefas gerais
- **Email** (📧) - Envio de emails
- **Call** (📞) - Chamadas telefónicas
- **WhatsApp** (💬) - Mensagens WhatsApp
- **Document** (📄) - Documentos a enviar/receber
- **Signature** (✍️) - Assinaturas pendentes

### 3.2 Gestão de Atividades
- **Criação via modal** dentro do detail view
- **Campos**:
  - Tipo de atividade
  - Título/resumo
  - Data limite (due date)
  - Responsável
  - Estado (done/pending)
  - Feedback ao concluir
- **Properties calculadas**:
  - `is_overdue`: detecta tarefas atrasadas
  - `status_color`: vermelho (overdue), amarelo (hoje), verde (ok)

### 3.3 Timeline de Atividades
- **Vista dentro de Lead Detail**
- **Ordenação** por data limite
- **Ícones coloridos** por tipo
- **Cores por status**:
  - Verde: no prazo
  - Amarelo: vence hoje
  - Vermelho: atrasada
- **Ações rápidas**:
  - Marcar como concluída (abre modal para feedback)
  - Editar atividade
- **Opacidade reduzida** para atividades concluídas
- **Feedback visível** em texto cinza

### 3.4 Validações
- Data limite não pode ser no passado
- Feedback obrigatório ao marcar como concluída
- Auto-preenchimento de `done_date` ao concluir

---

## 4. Pipeline Kanban (Vista Principal)

### 4.1 Layout Geral
- **Vista DEFAULT** do módulo CRM (`/crm/`)
- **Colunas dinâmicas** por estágio
- **Scroll horizontal** fluido
- **Altura responsiva** ao viewport
- **Colunas colapsáveis**:
  - Expandida: 300px
  - Colapsada: 150px (só header + contador)

### 4.2 Headers de Colunas
- **Barra colorida** no topo (cor do estágio)
- **Linha 1**: Nome do estágio + badge contador `(X)`
- **Linha 2**: Total estimado formatado (K/M/B)
- **Linha 3**: Progress bar horizontal
- **Botão "+"** para criar lead direto no estágio
- **Collapse/Expand** com Alpine.js

### 4.3 Cards de Lead
- **Design compacto** estilo Odoo
- **Informações visíveis**:
  - Título da lead
  - Receita esperada (formatada)
  - Nome do contacto
  - Priority stars (HIGH: ⭐⭐⭐)
  - Badge de source (cores por tipo)
  - Ícones de atividades
  - Avatar do responsável
- **Highlights visuais**:
  - Border amarelo: warning (perto do routing)
  - Border vermelho: overdue (ultrapassou routing)
- **Hover effect** com cursor pointer
- **Click** abre lead detail

### 4.4 Drag & Drop
- **Sortable.js** para inter-column drag
- **Funcionalidades**:
  - Arrastar entre qualquer coluna
  - Cursor muda para `move` nos cards
  - Update automático no backend
  - Atualização de totais em tempo real
- **Backend**:
  - Endpoint `/crm/leads/<uuid>/change-stage/`
  - Validação multi-company
  - Update de `stage_updated_at` (para routing)
  - Retorna novos totais e contadores
- **Validações**:
  - Modal de `lost_reason` ao arrastar para Lost
  - Aceita stages globais e da empresa
  - Security enforcement

### 4.5 Progress Bar e Routing
- **Progress bar simples** no header
- **Highlights nos cards** baseados em routing:
  - Verde (no prazo): `days_in_stage < routing_in_days`
  - Amarelo (warning): `days_in_stage == routing_in_days`
  - Vermelho (overdue): `days_in_stage > routing_in_days`
- **Cálculo dinâmico**: `(hoje - lead.stage_updated_at).days`

### 4.6 Filtros e Busca
- **Search bar** idêntica ao módulo Contactos
- **Field selector** com dropdown:
  - Título
  - Contacto
  - Source
  - Responsável
  - Descrição
- **View toggle**: Kanban ⟷ List
- **Botão "Novo"** para criar lead
- **Filtros planeados**:
  - Assigned to Me / All
  - Priority (HIGH/MEDIUM/LOW)
  - Date range picker
  - Tags
  - Source

### 4.7 Totais e Formatação
- **Formatação inteligente** de valores:
  - < 1.000: valor completo
  - ≥ 1.000: formato K (ex: 15.2K)
  - ≥ 1.000.000: formato M (ex: 3.5M)
  - ≥ 1.000.000.000: formato B (ex: 1.2B)
- **Sincronização Python ⟷ JavaScript**
- **Update em tempo real** após drag & drop

### 4.8 Responsive
- **Desktop (>1024px)**: colunas lado a lado
- **Tablet (768-1024px)**: 2-3 colunas visíveis
- **Mobile (<768px)** (planeado):
  - Accordion ou tabs verticais
  - Drag & drop desabilitado
  - Botão "Mover para..." em cada card

---

## 5. Sistema de Tags

### 5.1 Tags CRM (CRMTag)
- **Tags reutilizáveis** para categorização
- **Cores personalizadas** (hex colors)
- **Multi-company**: tags globais ou privadas
- **M2M relationship** com Leads

### 5.2 Interface de Tags
- **Autocomplete inteligente**:
  - Busca em tempo real
  - Criação rápida de novas tags
- **Modal de criação**:
  - Nome
  - Color picker com sugestões aleatórias
  - Preview em tempo real
- **Modal "Ver Todas"**:
  - Lista completa de tags
  - Busca e filtros
  - Seleção múltipla
- **Gestão completa**:
  - CRUD de tags em `/crm/tags/`
  - Bulk archive/unarchive
  - Bulk delete com confirmação
  - Check de leads associadas antes de apagar

### 5.3 Validações de Tags
- **Archive**: erro se já todas arquivadas
- **Unarchive**: erro se já todas ativas
- **Delete**: aviso se tags têm leads associadas
- **Modal de confirmação** com checkbox obrigatório

---

## 6. Geração Automática de Leads

### 6.1 Conceito
- **Baseado em histórico** de vendas
- **Recorrência sazonal**: aniversários, eventos sazonais
- **Follow-up automático** para clientes recorrentes

### 6.2 Configuração
- **Modal "Generate Leads"** no pipeline
- **Filtros disponíveis**:
  - Período histórico (mesmo mês ano passado, últimos X meses, custom)
  - Produtos específicos (ex: categoria "Aniversário")
  - Clientes com vendas no período
- **Preview em tempo real**:
  - Contagem de leads a gerar
  - Clientes afetados

### 6.3 Lógica de Geração
- **Busca vendas** no período histórico
- **Agrupa por contacto**
- **Cria Lead automaticamente** com:
  - Título customizável (template)
  - Receita estimada (média/soma vendas anteriores)
  - Estágio NEW
  - Source: GENERATED
  - Tags automáticas
  - Responsável da última venda
- **Cria Activity automática**:
  - Tipo: EMAIL ou WHATSAPP
  - Due date: hoje + X dias
  - Summary pré-definido
- **Evita duplicados**: não cria se já existe lead ativa para o contacto

### 6.4 Feedback
- Toast de sucesso: "✅ X leads geradas"
- Redirecionamento para pipeline filtrado
- Notificações para responsáveis

---

## 7. Integrações e Relações

### 7.1 Relação com Contactos
- **Foreign Key** Lead → Contact
- **Smart button** "CRM" no formulário de Contacto
- **Vista dedicada**: `/contacts/<uuid>/crm/`
- **Se 1 lead**: redireciona direto para detail
- **Se múltiplas**: mostra lista clicável
- **Colunas**: Referência, Estado, Valor Estimado, Data

### 7.2 Relação com Vendas (futura)
- **Conversão Lead → SaleOrder**
- **FK bidirecional**: Lead.sale_order / SaleOrder.lead
- **Smart buttons** em ambos os módulos
- **Tracking de origem**: vendas sabem de qual lead vieram

### 7.3 Relação com Documentos (futura)
- **Anexos** associados a Leads
- **Upload drag-and-drop**
- **Visualização** de PDFs, imagens, Excel
- **Download** e delete com permissões

### 7.4 Relação com Marketing (futura)
- **Campanhas** podem target leads
- **Tracking** de envios de email/WhatsApp
- **Conversões** rastreadas desde campanha até venda

### 7.5 Audit Log
- **Histórico completo** de mudanças
- **Tracking automático** via signals
- **Visualização** no lead detail
- **Campos rastreados**:
  - Mudança de estágio
  - Alteração de valores
  - Mudança de responsável
  - Updates de probability

---

## 8. Conversão de Leads

### 8.1 Lead → Venda
- **Botão "Converter em Venda"** no detail
- **Modal de confirmação** com preview
- **Dados copiados**:
  - Contacto
  - Receita estimada → total inicial
  - Produtos (se houver)
- **Updates automáticos**:
  - Lead.stage = WON
  - Lead.sale_order = FK para venda criada
- **Redirect** para sale_create com dados pré-preenchidos

### 8.2 Validações de Conversão
- Lead não pode estar WON ou LOST
- Contacto deve ser CLIENT ou BOTH
- Erro se contacto for apenas SUPPLIER
- Verificação de dados obrigatórios

---

## 9. Multi-Company

### 9.1 Isolamento de Dados
- **Todas as entidades** têm `owner_company`:
  - CRMStage
  - CRMTag
  - Lead
  - Activity
- **Filtros automáticos**:
  - Queries filtram por `get_active_company()`
  - Método `filter_by_company()` em cada model
- **Stages e Tags globais**:
  - `owner_company = NULL` → visível para todas empresas
  - `owner_company = X` → privado da empresa X

### 9.2 Validações Multi-Company
- **Drag & drop** valida ownership
- **APIs** verificam company do utilizador
- **Security enforcement** em todas operações
- **Aceita recursos globais** automaticamente

---

## 10. Interface e UX

### 10.1 Design System
- **Dark theme** consistente
- **Cores principais**:
  - Primary: #dbc693 (dourado)
  - Backgrounds: #1f2937, #374151
  - Text: #e5e7eb, #d1d5db
- **Tailwind CSS** para responsividade
- **Alpine.js** para interatividade

### 10.2 Componentes Customizados
- **Air Datepicker**:
  - Tema dark personalizado
  - Locale português
  - Botões "Hoje" e "Limpar"
- **Quill Editor**:
  - Tema dark
  - Toolbar completa
  - Suporte a imagens, links, code blocks
- **Custom Dropdown** (vendedor):
  - Sem avatar
  - Design consistente
  - Click away
- **Sortable.js**:
  - Drag smooth
  - Animações
  - Feedback visual

### 10.3 Navegação
- **Sub-navbar CRM**:
  - CRM (pipeline - default)
  - Sales (lista tabular)
  - Reporting (dashboards)
  - Configuração (dropdown)
- **Breadcrumbs** em todas páginas
- **Botões de ação** consistentes:
  - Guardar
  - Guardar e Criar Novo
  - Cancelar
  - Arquivar

### 10.4 Feedback Visual
- **Toasts** para sucessos/erros
- **Loading states** em botões
- **Skeletons** durante carregamento
- **Empty states** informativos
- **Modals** com animações suaves
- **Highlights** para dados importantes

### 10.5 Performance
- **Paginação** em listas grandes
- **Lazy loading** de imagens
- **Debounce** em buscas
- **Caching** de queries frequentes
- **Otimização** de queries N+1

### 10.6 Acessibilidade
- **Labels** descritivos
- **Placeholders** informativos
- **Validações** com mensagens claras
- **Focus states** visíveis
- **Navegação por teclado**

### 10.7 Responsividade
- **Desktop-first** design
- **Breakpoints** Tailwind:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px
- **Layouts adaptativos**:
  - Desktop: colunas lado a lado
  - Tablet: 2 colunas
  - Mobile: stack vertical
- **Touch-friendly** em mobile

---

## 📊 Resumo Estatístico

### Modelos de Dados
- **4 modelos principais**: CRMStage, CRMTag, Lead, Activity
- **Suporte multi-company** em todos
- **Soft delete** via `is_active`
- **UUID** como primary key
- **Timestamps** automáticos

### Views e Templates
- **Vista principal**: Pipeline Kanban
- **Vistas secundárias**: Lista, Detail, Create, Edit
- **15+ templates** entre principais e componentes
- **Template base** para smart buttons
- **Herança** e reutilização de código

### APIs e Endpoints
- **RESTful** para todas operações
- **AJAX** para interatividade
- **Validações** no backend
- **Respostas JSON** padronizadas
- **Multi-company** security em todas APIs

### Funcionalidades de Destaque
- ✅ **Pipeline visual** com drag & drop
- ✅ **Routing automático** com highlights
- ✅ **Tags customizáveis** por empresa
- ✅ **Editor de texto rico** para notas
- ✅ **Date picker moderno** com tema dark
- ✅ **Geração automática** de leads baseada em histórico
- ✅ **Conversão** para vendas com 1 click
- ✅ **Timeline de atividades** estilo Odoo
- ✅ **Multi-company** com isolamento total
- ✅ **Smart buttons** bidirecionais

---

## 🎯 Filosofia do Sistema

O CRM do **Fuet Mágico** foi desenvolvido com inspiração no **Odoo**, focando em:

1. **Simplicidade**: Interface limpa e intuitiva
2. **Produtividade**: Drag & drop, autocomplete, atalhos
3. **Visualização**: Pipeline claro, cores, badges, ícones
4. **Automação**: Geração de leads, atividades automáticas
5. **Integração**: Conectado com Contactos, Vendas, Marketing
6. **Escalabilidade**: Multi-company, tags ilimitadas, estágios customizáveis
7. **Performance**: Queries otimizadas, lazy loading, caching

---

**Documento gerado em:** Fevereiro 2026  
**Versão do Sistema:** 1.0  
**Status:** Em desenvolvimento ativo
