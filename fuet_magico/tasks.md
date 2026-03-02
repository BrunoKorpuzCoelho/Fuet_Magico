# 🎯 FUET MÁGICO - FULL STACK MANAGEMENT SYSTEM - DEVELOPMENT CHECKLIST

> **Stack:** Python 3.12+, Django 5.0+, Django ORM, PostgreSQL 17+, Redis, Celery, JavaScript Native, Tailwind CSS (via CDN)
> **Formato:** Checkboxes hierárquicos (Fase → Tarefa → Sub-tarefa)
> **Objetivo:** Sistema completo de gestão empresarial para Fuet Mágico - incluindo Vendas, Inventário, Compras, CRM, Financeiro, Marketing, Configurador de Produtos e Website Institucional. Desenvolvimento do zero - seguir todas as tasks = projeto funcionando ✅

---

## � LEGENDA

- ✅ **Concluído** - Tarefa completa e funcional
- ⭐ **Extra** - Funcionalidade opcional que adiciona valor/UX mas não é obrigatória
- ⏳ **Futuro** - Depende de outros módulos/fases ainda não implementados
- ❌ **Obsoleto** - Removido ou já não é necessário

---

## 📊 PROGRESSO GERAL

- **Fase 1:** 131/131 tarefas (100%) - Setup Ambiente e Infraestrutura ✅ COMPLETA!
- **Fase 2:** 90/90 tarefas (100%) - Frontend - Website Institucional ✅ COMPLETA!
- **Fase 3:** 531/531 tarefas (100%) - Backend - Estrutura Base Django ✅ COMPLETA!
- **Fase 4:** 297/499 tarefas (60%) - App: Contactos 🔄 parcial
- **Fase 5:** 659/949 tarefas (69%) - App: CRM (Customer Relationship Management) 🔄 parcial
- **Fase 6:** ~285/~650 tarefas (~44%) - App: Inventário (Produtos, Stock, Armazéns, Movimentos) 🔄 parcial
- **Fase 7:** 0/152 tarefas (0%) - App: Compras
- **Fase 8:** 0/247 tarefas (0%) - App: Vendas
- **Fase 9:** 0/94 tarefas (0%) - App: Financeiro
- **Fase 10:** 0/358 tarefas (0%) - BOM (Bill of Materials) - Sistema de Receitas
- **Fase 11:** 138/190 tarefas (73%) - Sistema de PDFs (Documentos) 🔄 parcial
- **Fase 12:** 203/511 tarefas (40%) - App: WhatsApp Templates & Activities 🔄 parcial
- **Fase 13:** 0/44 tarefas (0%) - Stock Management Avançado
- **Fase 14:** 0/52 tarefas (0%) - PDF Scanning (Entrada de Compras)
- **Fase 15:** 0/222 tarefas (0%) - App: Relatórios e Dashboard
- **Fase 16:** 0/107 tarefas (0%) - App: Configurações e Parâmetros
- **Fase 17:** 0/53 tarefas (0%) - Integração Final e Deployment
- **Fase 18:** 96/410 tarefas (23%) - Testes Automatizados UI (Playwright) 🔄 parcial

**TOTAL:** 2263/4955 tarefas (45.7%)

---

# 🚀 FASE 1: SETUP AMBIENTE E INFRAESTRUTURA

**⏱ Tempo estimado:** 2-3 dias
**🎯 Objetivo:** Configurar ambiente de desenvolvimento Python, Django, PostgreSQL, Redis e estrutura inicial do projeto
**📦 Dependências:** Nenhuma (fase inicial)

---

## 1.1 Preparação de Ambiente Virtual (venv) ✅

Configurar ambiente virtual Python isolado para desenvolvimento, garantindo que as dependências do projeto não conflitem com outros projetos ou com o sistema.

- [x] **Criar ambiente virtual**
  - [x] Executar `python -m venv venv` na raiz do projeto
  - [x] Verificar criação da pasta `venv/`
  - [x] Adicionar `venv/` ao `.gitignore`

- [x] **Ativar ambiente virtual**
  - [x] WSL: executar `source venv/bin/activate`
  - [x] Verificar que prompt mostra `(venv)`
  - [x] Documentar comando de ativação no README

- [x] **Instalar ferramentas base**
  - [x] Executar `pip install --upgrade pip`
  - [x] Executar `pip install wheel setuptools`
  - [x] Verificar versão: `pip --version` (pip 26.0)

- [x] **Testing - Ambiente Virtual**
  - [x] Test: `which python` aponta para `venv/bin/python`
  - [x] Test: `pip list` mostra apenas pacotes base (packaging, pip, setuptools, wheel)
  - [x] Test: desativar e reativar venv funciona

---

## 1.2 Instalação de Dependências Python ✅

Instalar todas as bibliotecas necessárias para o projeto (Django, PostgreSQL adapter, Redis, Celery, etc.).

- [x] **Criar requirements.txt**
  - [x] Adicionar Django==5.0.*
  - [x] Adicionar psycopg2-binary (PostgreSQL adapter)
  - [x] Adicionar redis
  - [x] Adicionar celery
  - [x] Adicionar python-dotenv (variáveis de ambiente)
  - [x] Adicionar Pillow (imagens)
  - [x] Adicionar reportlab (PDFs)
  - [x] Adicionar PyPDF2 (leitura de PDFs)
  - [x] Adicionar requests (APIs)
  - [x] Adicionar python-dateutil

- [x] **Instalar dependências**
  - [x] Executar `pip install -r requirements.txt`
  - [x] Verificar instalação: `pip list` (34 pacotes)
  - [x] Documentar versões instaladas (Django 5.0.14, psycopg2-binary 2.9.11, redis 7.1.0, celery 5.6.2)

- [x] **Testing - Dependências**
  - [x] Test: `python -c "import django; print(django.get_version())"` retorna 5.0.14 ✅
  - [x] Test: `python -c "import psycopg2"` sem erros ✅
  - [x] Test: `python -c "import redis"` sem erros ✅

---

## 1.3 Configuração PostgreSQL ✅

Configurar banco de dados PostgreSQL para o projeto.

- [x] **Criar base de dados**
  - [x] Instalar PostgreSQL 17+ (já instalado)
  - [x] Criar database: `fuet_magico_db`
  - [x] Criar user: `cubix` com password `cubix123`
  - [x] Conceder privilégios ao user na database

- [x] **Configurar conexão**
  - [x] Criar arquivo `.env` na raiz
  - [x] Adicionar DATABASE_URL com string de conexão
  - [x] Adicionar `.env` ao `.gitignore`

- [x] **Testing - PostgreSQL**
  - [x] Test: conectar ao PostgreSQL via script Python ✅
  - [x] Test: database `fuet_magico_db` criada e acessível ✅
  - [x] Test: user `cubix` tem acesso completo ✅

---

## 1.4 Configuração Redis ✅

Configurar Redis para cache e Celery.

- [x] **Instalar Redis**
  - [x] Instalar Redis via WSL Ubuntu
  - [x] Iniciar serviço Redis (`sudo service redis-server start`)
  - [x] Verificar porta padrão: 6379 ✅

- [x] **Configurar conexão**
  - [x] REDIS_URL já configurado no `.env` (redis://localhost:6379/0)
  - [x] Testar conexão via redis-cli e Python ✅

- [x] **Testing - Redis**
  - [x] Test: `redis-cli ping` retorna PONG ✅
  - [x] Test: Python conecta ao Redis (Windows → WSL) ✅

---

## 1.5 Criação do Projeto Django ✅

Criar estrutura base do projeto Django.

- [x] **Criar projeto**
  - [x] Executar `django-admin startproject config .` ✅
  - [x] Verificar criação de `config/` e `manage.py` ✅
  - [x] Testar: `python manage.py --version` (5.0.14) ✅

- [x] **Configurar settings.py**
  - [x] Importar `os` e `python-dotenv` ✅
  - [x] Carregar variáveis de `.env` ✅
  - [x] Configurar DATABASES com PostgreSQL ✅
  - [x] Configurar CACHES com Redis ✅
  - [x] Configurar STATIC_URL e STATIC_ROOT ✅
  - [x] Configurar MEDIA_URL e MEDIA_ROOT ✅
  - [x] Adicionar ALLOWED_HOSTS ✅
  - [x] Configurar segurança (SESSION, CSRF, XSS) ✅
  - [x] Configurar Celery settings ✅

- [x] **Configurar timezone e linguagem**
  - [x] Definir LANGUAGE_CODE = 'pt-pt' ✅
  - [x] Definir TIME_ZONE = 'Europe/Lisbon' ✅
  - [x] Definir USE_TZ = True ✅

- [x] **Testing - Projeto Django**
  - [x] Test: `python manage.py check` sem erros ✅
  - [x] Test: `python manage.py migrate` cria tabelas iniciais ✅
  - [x] Test: `python manage.py runserver` inicia em http://127.0.0.1:8000/ ✅

---

## 1.6 Estrutura de Diretórios ✅

Criar estrutura de pastas para organização do projeto.

- [x] **Criar diretórios base**
  - [x] Criar `/static/` (arquivos estáticos) ✅
  - [x] Criar `/static/css/` ✅
  - [x] Criar `/static/js/` ✅
  - [x] Criar `/static/images/` ✅
  - [x] Criar `/static/fonts/` ✅
  - [x] Criar `/static/icons/` ✅
  - [x] Criar `/static/website/` (assets do website institucional) ✅
  - [x] Criar `/static/website/images/` ✅
  - [x] Criar `/static/website/favicon/` ✅
  - [x] Criar `/media/` (uploads) ✅
  - [x] Criar `/media/products/` ✅
  - [x] Criar `/media/documents/` ✅
  - [x] Criar `/media/uploads/` ✅
  - [x] Criar `/templates/` (templates HTML standalone) ✅

- [x] **Criar diretórios para apps**
  - [x] Criar `/apps/` (todas as apps Django) ✅
  - [x] Adicionar `__init__.py` em `/apps/` ✅

- [x] **Configurar Django**
  - [x] Adicionar `templates` a TEMPLATES['DIRS'] ✅
  - [x] Criar arquivos exemplo (global.css, main.js) ✅

- [x] **Testing - Estrutura**
  - [x] Test: verificar todas as pastas foram criadas ✅
  - [x] Test: Django reconhece templates e static files (`python manage.py check`) ✅

---

## 1.7 Configuração Celery ✅

Configurar Celery para tarefas assíncronas (emails, WhatsApp, etc.).

- [x] **Criar celery.py**
  - [x] Criar `config/celery.py` ✅
  - [x] Configurar Celery app com autodiscover_tasks ✅
  - [x] Importar Celery no `config/__init__.py` ✅

- [x] **Configurar settings**
  - [x] CELERY_BROKER_URL (Redis) já configurado no .env ✅
  - [x] CELERY_RESULT_BACKEND (Redis) já configurado ✅
  - [x] Configurar timezone do Celery (Europe/Lisbon) ✅
  - [x] Adicionar serializers e task tracking ✅

- [x] **Criar tasks de teste**
  - [x] Criar `config/tasks.py` com tasks exemplo ✅
  - [x] test_celery_task, send_email_task, process_whatsapp_message ✅

- [x] **Testing - Celery**
  - [x] Test: executar worker `celery -A config worker --pool=solo` ✅
  - [x] Test: criar task de teste e executar (test/auto/test_celery.py) ✅
  - [x] Test: verificar logs do worker e task execution ✅

---

## 1.8 Git e Controlo de Versão ✅

Configurar repositório Git para controlo de versão.

- [x] **Inicializar Git**
  - [x] Git já inicializado (repositório existente) ✅
  - [x] `.gitignore` completo e funcional ✅
  - [x] venv/, .env, __pycache__/, *.pyc, media/, staticfiles/, db.sqlite3 ignorados ✅

- [x] **Preparado para commit**
  - [x] Estrutura completa pronta para versionar ✅
  - [x] Commit será feito quando o utilizador decidir ⏳

- [x] **Testing - Git**
  - [x] Test: `git status` funciona corretamente ✅
  - [x] Test: arquivos sensíveis não estão tracked (.env, venv/, etc.) ✅
  - [x] Test: `git check-ignore` confirma todos os paths sensíveis ignorados ✅

---

# 🚀 FASE 2: FRONTEND - WEBSITE INSTITUCIONAL (HTML COPY)

**⏱ Tempo estimado:** 3-4 dias
**🎯 Objetivo:** Copiar exatamente o HTML do website https://v0-fuet-magico.vercel.app/ e integrar no Django
**📦 Dependências:** Fase 1 (estrutura Django criada)

---

## 2.1 Análise e Extração do HTML ✅

Extrair todo o código HTML do website de referência.

- [x] **Acessar e analisar website**
  - [x] Abrir https://v0-fuet-magico.vercel.app/
  - [x] Inspecionar código fonte (View Page Source)
  - [x] Identificar estrutura: header, sections, footer

- [x] **Extrair HTML completo**
  - [x] Copiar todo o HTML da página
  - [x] Identificar todos os recursos externos (imagens, fonts, etc.)
  - [x] Listar todos os links de CDN (Tailwind CSS, etc.)

- [x] **Documentar estrutura**
  - [x] Criar documento com lista de seções
  - [x] Documentar IDs e classes importantes

- [x] **Testing - Extração**
  - [x] Test: HTML copiado está completo
  - [x] Test: todas as URLs de recursos identificadas

**Implementação Completa em:** `templates/website/home.html` (586 linhas)

**Estrutura Identificada:**
- Header: Navbar com logo "Fuet Mágico by Daisy" (fixed, scroll-responsive)
- Secções: #inicio (hero), #sobre, #portfolio, #servicos, #precos, #testemunhos, #contacto
- Footer: Completo com informações de contacto e redes sociais

**Recursos Externos:**
- CDN: Tailwind CSS (https://cdn.tailwindcss.com)
- Fonts: Google Fonts - Delius (https://fonts.googleapis.com/css2?family=Delius)
- Imagens: Hospedadas em https://v0-fuet-magico.vercel.app/ (hero bg, portfolio, about, etc.)

**JavaScript Incluído:**
- Mobile menu toggle
- Portfolio filter system (all, infantis, adultos, casamento, minimalistas, tematicos)
- Smooth scroll navigation
- Navbar scroll behavior (transparent → white)

---

## 2.2 Criação do Template Base ✅

Criar template Django com o HTML extraído.

- [x] **Criar home template**
  - [x] Criar `templates/website/home.html`
  - [x] Colar HTML completo extraído
  - [x] Adicionar `{% load static %}` no topo
  - [x] Manter estrutura HTML exatamente como está

- [x] **Configurar Tailwind CSS via CDN**
  - [x] Verificar link CDN do Tailwind no <head>
  - [x] Garantir que está exatamente como no website original
  - [x] Não modificar configurações do Tailwind

- [x] **Testing - Template**
  - [x] Test: template criado em `templates/website/home.html`
  - [x] Test: {% load static %} no início do arquivo

- [x] **Configurar View e URL**
  - [x] Criar `apps/website/views.py` com função `home()`
  - [x] Criar `apps/website/urls.py` com rota raiz
  - [x] Incluir URLs do website em `config/urls.py`

**Implementação Completa:**
- Template: `templates/website/home.html` (762 linhas)
- View: `apps/website/views.py` - função home()
- URLs: rota raiz (`/`) configurada
- Tailwind CSS e Google Fonts (Delius) configurados
- Todas as cores personalizadas (#e6a3a7) aplicadas
- Carrossel de testemunhos funcionando
- Formulário de contacto com validação

---

## 2.3 Download e Organização de Imagens ✅

Baixar todas as imagens do website e organizá-las no projeto.

- [x] **Identificar todas as imagens**
  - [x] Listar todas as URLs de imagens do website
  - [x] Criar mapeamento: nome → URL

- [x] **Download de imagens**
  - [x] Baixar todas as imagens para `/static/images/`
  - [x] Manter nomes de arquivo originais
  - [x] Organizar em subpastas se necessário (cakes, avatars, etc.)

- [x] **Atualizar URLs no template**
  - [x] Substituir URLs absolutas por `{% static 'images/...' %}`
  - [x] Verificar todos os src de <img>
  - [x] Verificar backgrounds em CSS inline

- [x] **Testing - Imagens**
  - [x] Test: todas as imagens baixadas em `/static/images/`
  - [x] Test: nenhuma URL absoluta externa permanece no HTML

**Implementação Completa:**
- ✅ 18 imagens únicas baixadas (24 referências no total)
- ✅ Estrutura organizada: `/static/images/` (raiz), `/cakes/`, `/avatars/`
- ✅ Todas as URLs substituídas por `{% static %}`
- ✅ Background hero-bg atualizado no CSS inline
- ✅ Zero URLs externas remanescentes no template

---

## 2.4 Extração e Organização de JavaScript ✅

Extrair scripts JavaScript e organizá-los.

- [x] **Identificar scripts**
  - [x] Identificar todos os <script> no HTML
  - [x] Separar scripts inline vs externos

- [x] **Criar arquivos JS**
  - [x] Criar `/static/js/website.js`
  - [x] Copiar todo o JavaScript inline para website.js
  - [x] Manter funcionalidades: smooth scroll, form validation, etc.

- [x] **Incluir no template**
  - [x] Adicionar `<script src="{% static 'js/website.js' %}"></script>`
  - [x] Verificar ordem de carregamento

- [x] **Testing - JavaScript**
  - [x] Test: scripts funcionam (console sem erros)
  - [x] Test: interações funcionam (forms, botões, etc.)

**Implementação Completa:**
- ✅ JavaScript extraído do HTML (141 linhas)
- ✅ Criado `/static/js/website.js` sem comentários (seguindo rules.md)
- ✅ Template atualizado com `{% static 'js/website.js' %}`
- ✅ Todas as funcionalidades mantidas: menu mobile, carousel, filtros, smooth scroll, navbar scroll behavior
- ✅ Código limpo e auto-explicativo conforme regras gerais

---

## 2.5 Criação da App 'website' ✅

Criar app Django para gerenciar o website institucional.

- [x] **Criar app**
  - [x] Executar `python manage.py startapp website apps/website`
  - [x] Mover `apps/website` se criado fora
  - [x] Adicionar 'apps.website' ao INSTALLED_APPS

- [x] **Criar view**
  - [x] Criar `apps/website/views.py`
  - [x] Criar função `home_view` que renderiza `website/home.html`

- [x] **Criar URLs**
  - [x] Criar `apps/website/urls.py`
  - [x] Adicionar rota: `path('', home_view, name='home')`
  - [x] Incluir no `config/urls.py`: `path('', include('apps.website.urls'))`

- [x] **Testing - App Website**
  - [x] Test: acessar `http://localhost:8000/` mostra o website
  - [x] Test: página carrega sem erros 404

**Implementação Completa:**
- ✅ App criada em `/apps/website/`
- ✅ View `home()` renderiza `website/home.html`
- ✅ URLs configuradas: rota raiz (`''`) aponta para home view
- ✅ App registrada em INSTALLED_APPS
- ✅ Routing completo: config/urls.py → apps/website/urls.py → views.home

---

## 2.6 Validação Visual Completa ✅

Comparar visualmente o website copiado com o original.

- [x] **Comparação visual**
  - [x] Abrir original e cópia lado a lado
  - [x] Verificar header é idêntico
  - [x] Verificar todas as seções (Sobre, Portfólio, Serviços, etc.)
  - [x] Verificar footer é idêntico
  - [x] Verificar cores e espaçamentos

- [x] **Verificar funcionalidades**
  - [x] Test: navegação smooth scroll funciona
  - [x] Test: filtros de portfólio funcionam
  - [x] Test: formulários validam
  - [x] Test: botões WhatsApp/Instagram funcionam

- [x] **Responsividade**
  - [x] Test: mobile (375px)
  - [x] Test: tablet (768px)
  - [x] Test: desktop (1920px)

- [x] **Testing - Validação Final**
  - [x] Test: website 95%+ idêntico ao original
  - [x] Test: todas as imagens carregam
  - [x] Test: todos os links funcionam

**Validação Completa:**
- ✅ Servidor Django iniciado sem erros (http://127.0.0.1:8000/)
- ✅ Simple Browser aberto para visualização
- ✅ Sem erros no HTML, JS ou Python (0 issues encontrados)
- ✅ Todas as imagens locais configuradas
- ✅ JavaScript extraído e funcional
- ✅ Cores atualizadas (#dbc693)
- ✅ Template renderiza corretamente
- ✅ App website integrada ao Django

---

# 🚀 FASE 3: BACKEND - ESTRUTURA BASE DJANGO

**⏱ Tempo estimado:** 2-3 dias
**🎯 Objetivo:** Criar estrutura de autenticação, permissions, base models e admin Django
**📦 Dependências:** Fase 1 (Django configurado)

---

## 3.1 Sistema de Autenticação e Usuários

Criar sistema de autenticação customizado.

- [x] **Criar app 'accounts'**
  - [x] Executar `python manage.py startapp accounts apps/accounts`
  - [x] Adicionar 'apps.accounts' ao INSTALLED_APPS

- [x] **Criar modelo CustomUser**
  - [x] Estender AbstractUser em `apps/accounts/models.py`
  - [x] Adicionar campos: phone, avatar, role (ADMIN, MANAGER, EMPLOYEE)
  - [x] Adicionar AUTH_USER_MODEL = 'accounts.CustomUser' no settings

- [x] **Criar forms e views**
  - [x] Criar LoginView, LogoutView
  - [x] Criar template de login standalone

- [x] **Configurar URLs**
  - [x] Criar `apps/accounts/urls.py`
  - [x] Adicionar rotas: /login/, /logout/
  - [x] Incluir no config/urls.py

- [x] **Testing - Autenticação**
  - [x] Test: makemigrations e migrate sem erros
  - [x] Test: criar superuser funciona
  - [x] Test: login e logout funcionam

---

## 3.2 Django Admin Customização

Configurar Django Admin para gestão.

- [x] **Customizar Admin**
  - [x] Configurar admin.site.site_header = 'Fuet Mágico Admin'
  - [x] Configurar admin.site.site_title = 'Fuet Mágico'
  - [x] Configurar admin.site.index_title = 'Gestão'

- [x] **Registrar CustomUser no admin**
  - [x] Criar UserAdmin em `apps/accounts/admin.py`
  - [x] Configurar list_display, search_fields, list_filter

- [x] **Testing - Admin**
  - [x] Test: acessar /admin/ funciona
  - [x] Test: login com superuser funciona
  - [x] Test: visualizar usuários no admin

---

## 3.3 Middleware e Permissions

Criar middleware para controlo de acesso.

- [x] **Criar middleware de autenticação**
  - [x] Criar `apps/accounts/middleware.py`
  - [x] Verificar se usuário está autenticado em rotas protegidas
  - [x] Adicionar ao MIDDLEWARE no settings

- [x] **Criar decorators**
  - [x] Criar `@login_required_custom`
  - [x] Criar `@role_required(role='ADMIN')`

- [x] **Testing - Middleware**
  - [x] Test: rotas protegidas redirecionam para login
  - [x] Test: decorators funcionam corretamente

---

## 3.4 Modelos Base (Abstract Models)

Criar modelos abstratos para reutilização.

- [x] **Criar BaseModel**
  - [x] Criar `apps/core/` (app helper)
  - [x] Criar `apps/core/models.py`
  - [x] Criar AbstractBaseModel com: id (UUID), created_at, updated_at, is_active

- [x] **Adicionar ao INSTALLED_APPS**
  - [x] Adicionar 'apps.core'

- [x] **Testing - Base Models**
  - [x] Test: outros models podem herdar de BaseModel

---

## 3.5 Configuração de Media Files

Configurar upload e servir arquivos de media.

- [x] **Configurar settings**
  - [x] Verificar MEDIA_URL = '/media/'
  - [x] Verificar MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

- [x] **Configurar URLs para desenvolvimento**
  - [x] Adicionar static serve de media em `config/urls.py`
  - [x] Adicionar `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`

- [x] **Testing - Media**
  - [x] Test: upload de arquivo via admin funciona
  - [x] Test: acessar arquivo em /media/ funciona

---

## 3.6 Templates Base e Estrutura

Criar templates base para o sistema interno (não website).

- [x] **Criar base template**
  - [x] Criar `templates/base.html` (sistema interno)
  - [x] Incluir Tailwind CSS via CDN
  - [x] Criar navbar com menu
  - [x] Criar sidebar (se necessário)
  - [x] Criar footer

- [x] **Criar templates de componentes**
  - [x] Criar `templates/components/navbar.html`
  - [x] Criar `templates/components/messages.html` (Django messages)

- [x] **Testing - Templates Base**
  - [x] Test: base.html renderiza corretamente
  - [x] Test: herança de templates funciona

---

## 3.7 Dashboard Principal

Criar dashboard principal do sistema.

- [x] **Criar app 'dashboard'**
  - [x] Executar `python manage.py startapp dashboard apps/dashboard`
  - [x] Adicionar ao INSTALLED_APPS

- [x] **Criar view e template**
  - [x] Criar `dashboard_view` em views.py
  - [x] Criar template `dashboard/index.html` (standalone)
  - [x] Mostrar resumo: vendas, compras, stock, clientes

- [x] **Configurar rota**
  - [x] Criar urls.py: `path('dashboard/', dashboard_view, name='dashboard')`
  - [x] Incluir no config/urls.py

- [x] **Testing - Dashboard**
  - [x] Test: acessar /dashboard/ funciona
  - [x] Test: usuário não autenticado é redirecionado

---

## 3.8 Sistema de Logs e Auditoria

Criar sistema para logging de ações.

- [x] **Criar modelo AuditLog**
  - [x] Criar em `apps/core/models.py`
  - [x] Campos: user, action, model_name, object_id, timestamp, details (JSON)

- [x] **Criar signals**
  - [x] Criar signals para log automático em save/delete
  - [x] Registrar signals

- [x] **Registrar no Admin**
  - [x] Criar AuditLogAdmin
  - [x] Configurar list_display, search, filters

- [x] **Testing - Audit Log**
  - [x] Test: criar objeto gera log
  - [x] Test: visualizar logs no admin

---

## 3.9 Configuração de Email

Configurar envio de emails.

- [x] **Configurar settings**
  - [x] Adicionar EMAIL_BACKEND
  - [x] Adicionar EMAIL_HOST, EMAIL_PORT
  - [x] Adicionar EMAIL_HOST_USER, EMAIL_HOST_PASSWORD (via .env)
  - [x] Adicionar DEFAULT_FROM_EMAIL

- [x] **Criar templates de email**
  - [x] Criar `templates/emails/base.html`
  - [x] Criar template de teste

- [x] **Criar helper function**
  - [x] Criar `apps/core/utils.py`
  - [x] Criar função `send_email_notification(to, subject, template, context)`

- [x] **Testing - Email**
  - [x] Test: enviar email de teste funciona
  - [x] Test: template renderiza corretamente

---

## 3.10 DevTools - Sistema de Logs Avançado

Criar visualizador de logs no DevTools com 3 tipos de logs.

- [x] **Criar modelo ErrorLog**
  - [x] Criar em `apps/core/models.py`
  - [x] Campos: level (ERROR, WARNING, CRITICAL), message, traceback, request_path, user, timestamp
  - [x] Criar handler customizado do Python logging
  - [x] Registrar no Admin

- [x] **Criar APIs de logs**
  - [x] Criar `apps/core/views.py` com APIs REST
  - [x] API endpoint: `/api/audit-logs/` (paginado, 300 por página)
  - [x] API endpoint: `/api/error-logs/` (paginado, 300 por página)
  - [x] API endpoint: `/api/application-logs/` (logs reais do sistema)
  - [x] Implementar filtros: user, date_range, action, level

- [x] **Criar páginas de visualização**
  - [x] Criar `templates/devtools/application_logs.html` (tempo real)
  - [x] Criar `templates/devtools/audit_logs.html` (histórico com scroll infinito)
  - [x] Criar `templates/devtools/error_logs.html` (histórico com scroll infinito)
  - [x] Estilo VS Code: monospace, cores por tipo, timestamps

- [x] **Atualizar DevTools dropdown**
  - [x] Atualizar links em `templates/base.html`
  - [x] Application Logs → `/devtools/logs/application/`
  - [x] Audit Logs → `/devtools/logs/audit/`
  - [x] Error Logs → `/devtools/logs/error/`
  - [x] Persistência com localStorage (mantém ativo entre páginas)

- [x] **Implementar scroll infinito**
  - [x] JavaScript para detectar scroll no fim da página
  - [x] Carregar mais 300 logs quando atingir o fim
  - [x] Loading indicator durante carregamento
  - [x] Performance: paginação eficiente

- [x] **Implementar streaming (Application Logs)**
  - [x] Polling a cada 3s com dados reais do sistema
  - [x] Auto-scroll quando novos logs chegam
  - [x] Botão para pausar auto-scroll
  - [x] Limitar a 1000 logs em memória (remover antigos)

- [x] **Testing - DevTools Logs**
  - [x] Test: visualizar Audit Logs funciona
  - [x] Test: visualizar Error Logs funciona
  - [x] Test: Application Logs em tempo real funciona
  - [x] Test: scroll infinito carrega mais logs
  - [x] Test: performance com 10k+ logs

---

## 3.11 Sistema Multi-Company

Criar modelo Company e suporte multi-company no sistema.

- [x] **Criar modelo Company**
  - [x] Criar em `apps/core/models.py`
  - [x] Herdar de AbstractBaseModel
  - [x] Campos básicos: name (unique), legal_name, vat, company_registry
  - [x] Campos contacto: email, phone, website
  - [x] Campos morada: address, city, postal_code, country (default: 'Portugal')
  - [x] Campos regionais: currency (default: 'EUR'), language (default: 'pt_PT')
  - [x] Campo branding: logo (ImageField)
  - [x] Campo hierarquia: parent_company (FK self, para grupos empresariais)
  - [x] Property is_subsidiary

- [x] **Adicionar suporte multi-company ao User**
  - [x] Adicionar campo companies (ManyToManyField para Company)
  - [x] Adicionar campo default_company (ForeignKey para Company)
  - [x] User pode pertencer a múltiplas companies
  - [x] User tem uma company default

- [x] **Criar migrations**
  - [x] Executar makemigrations core
  - [x] Executar makemigrations accounts
  - [x] Executar migrate

- [x] **Criar empresa default**
  - [x] Criar management command `create_default_company`
  - [x] Criar empresa "Fuet Mágico" com:
    - [x] name: "Fuet Mágico"
    - [x] legal_name: "Fuet Mágico, Lda."
    - [x] currency: "EUR"
    - [x] language: "pt_PT"
    - [x] country: "Portugal"
  - [x] Executar comando: `python manage.py create_default_company`

- [x] **Registrar no Admin**
  - [x] Criar CompanyAdmin em `apps/core/admin.py`
  - [x] Configurar list_display: name, vat, city, country, currency, language, is_active
  - [x] Configurar search_fields: name, legal_name, vat, email, city
  - [x] Configurar list_filter: is_active, country, currency
  - [x] Fieldsets: Basic Info, Contact, Address, Regional Settings, Branding, Hierarchy, System

- [x] **Adicionar seletor de company no sistema**
  - [x] Adicionar dropdown de company no navbar (quando user tem múltiplas)
  - [x] Salvar company_id selecionada na session
  - [x] Filtrar dados por company_id em todas as queries

- [x] **Implementar company_id em modelos EXISTENTES**
  - [x] Adicionar owner_company (FK) aos modelos: Contact, ContactTag
  - [x] Criar migrations (0004_contact_owner_company_contacttag_owner_company)
  - [x] Auto-preencher owner_company com active_company em contact_create_view
  - [x] Filtrar por owner_company em contact_list_view
  - **Nota:** Para modelos futuros (Lead, Sale, Purchase, Product), adicionar owner_company na task de criação

- [x] **Testing - Multi-Company**
  - [x] Test: criar company funciona
  - [x] Test: empresa default criada
  - [x] Test: user pode ter múltiplas companies
  - [x] Test: filtros por company funcionam (Contact e ContactTag)


## 3.12.1 Modelos de Base de Dados do Chatter

Criar modelos para mensagens, notas e atividades com GenericForeignKey.

- [x] **Criar modelo ChatterMessage**
  - [x] Criar em `apps/core/models.py`
  - [x] Herdar de AbstractBaseModel
  - [x] **GenericForeignKey (funciona com QUALQUER modelo - Lead, Contact, Sale, etc.):**
    ```python
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    ```
  - [x] **Campos principais:**
    - [x] author (ForeignKey CustomUser, on_delete=SET_NULL, nullable)
    - [x] message_type (CharField, max_length=10, choices=[('EMAIL', 'Email'), ('NOTE', 'Nota Interna')])
    - [x] subject (CharField, max_length=255, blank=True) - só para emails
    - [x] body (TextField) - conteúdo da mensagem/nota
    - [x] to_email (EmailField, blank=True, null=True) - destinatário
    - [x] cc_emails (TextField, blank=True) - CC separados por vírgula
  - [x] **Anexos:**
    - [x] attachments (JSONField, default=list, blank=True)
      ```python
      # Exemplo:
      [
        {"filename": "fatura.pdf", "url": "/media/attachments/fatura.pdf"},
        {"filename": "foto.jpg", "url": "/media/attachments/foto.jpg"}
      ]
      ```
  - [x] **Status:**
    - [x] is_internal (BooleanField, default=False) - True = nota interna
    - [x] sent_at (DateTimeField, null=True, blank=True) - quando enviado
  - [x] **Meta:**
    ```python
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['author']),
            models.Index(fields=['message_type']),
        ]
        verbose_name = 'Mensagem do Chatter'
        verbose_name_plural = 'Mensagens do Chatter'
    ```
  - [x] **Methods:**
    ```python
    def __str__(self):
        return f"{self.get_message_type_display()} - {self.author} - {self.created_at}"
    
    @property
    def is_email(self):
        return self.message_type == 'EMAIL'
    
    @property
    def is_note(self):
        return self.message_type == 'NOTE'
    ```

- [x] **Criar modelo ChatterActivity**
  - [x] Criar em `apps/core/models.py`
  - [x] Herdar de AbstractBaseModel
  - [x] **GenericForeignKey:**
    ```python
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    ```
  - [x] **Campos:**
    - [x] user (ForeignKey CustomUser, on_delete=SET_NULL, null=True)
    - [x] activity_type (CharField, max_length=20, choices=[...])
      ```python
      ACTIVITY_TYPES = [
          ('CREATE', 'Criado'),
          ('UPDATE', 'Atualizado'),
          ('DELETE', 'Eliminado'),
          ('STATUS_CHANGE', 'Mudança de Estado'),
          ('STAGE_CHANGE', 'Mudança de Estágio'),
          ('ASSIGNMENT', 'Atribuído'),
          ('EMAIL_SENT', 'Email Enviado'),
          ('WHATSAPP_SENT', 'WhatsApp Enviado'),
          ('CALL', 'Chamada'),
          ('MEETING', 'Reunião'),
          ('COMMENT', 'Comentário'),
      ]
      ```
    - [x] description (TextField) - texto legível: "mudou o estágio de New para Qualified"
    - [x] details (JSONField, default=dict, blank=True)
      ```python
      # Exemplo:
      {
        "field": "stage",
        "old_value": "New",
        "new_value": "Qualified"
      }
      ```
  - [x] **Meta:**
    ```python
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user']),
        ]
        verbose_name = 'Atividade do Chatter'
        verbose_name_plural = 'Atividades do Chatter'
    ```
  - [x] **Methods:**
    ```python
    def __str__(self):
        return f"{self.user} - {self.get_activity_type_display()} - {self.created_at}"
    ```

- [x] **Criar migrations**
  - [x] Executar `python manage.py makemigrations core`
  - [x] Executar `python manage.py migrate`

- [x] **Registrar no Admin**
  - [x] ChatterMessageAdmin:
    ```python
    from django.contrib import admin
    from apps.core.models import ChatterMessage, ChatterActivity
    
    @admin.register(ChatterMessage)
    class ChatterMessageAdmin(admin.ModelAdmin):
        list_display = ['id', 'content_object', 'author', 'message_type', 'subject', 'is_internal', 'created_at']
        list_filter = ['message_type', 'is_internal', 'created_at']
        search_fields = ['subject', 'body', 'to_email']
        readonly_fields = ['content_type', 'object_id', 'sent_at', 'created_at', 'updated_at']
        fieldsets = (
            ('Objeto Relacionado', {
                'fields': ('content_type', 'object_id')
            }),
            ('Mensagem', {
                'fields': ('author', 'message_type', 'subject', 'body')
            }),
            ('Email', {
                'fields': ('to_email', 'cc_emails', 'sent_at')
            }),
            ('Anexos e Status', {
                'fields': ('attachments', 'is_internal')
            }),
            ('Timestamps', {
                'fields': ('created_at', 'updated_at')
            }),
        )
    ```
  - [x] ChatterActivityAdmin:
    ```python
    @admin.register(ChatterActivity)
    class ChatterActivityAdmin(admin.ModelAdmin):
        list_display = ['id', 'content_object', 'user', 'activity_type', 'description', 'created_at']
        list_filter = ['activity_type', 'created_at']
        search_fields = ['description']
        readonly_fields = ['content_type', 'object_id', 'created_at']
        fieldsets = (
            ('Objeto Relacionado', {
                'fields': ('content_type', 'object_id')
            }),
            ('Atividade', {
                'fields': ('user', 'activity_type', 'description', 'details')
            }),
            ('Timestamp', {
                'fields': ('created_at',)
            }),
        )
    ```

- [x] **Testing - Modelos**
  - [x] Test: criar ChatterMessage EMAIL funciona *(testado — email real enviado com sucesso)*
  - [x] Test: criar ChatterMessage NOTE funciona
  - [x] Test: GenericForeignKey funciona com Lead
  - [x] Test: GenericForeignKey funciona com Contact
  - [x] Test: criar ChatterActivity funciona
  - [x] Test: attachments JSON guarda lista de ficheiros
  - [x] Test: details JSON guarda mudanças de campos
  - [x] Test: is_email e is_note properties funcionam

---

## 3.12.2 Template Tags Personalizados

Criar template tags para facilitar uso do chatter.

- [x] **Criar pasta templatetags**
  - [x] Criar `apps/core/templatetags/` (se não existir)
  - [x] Criar `apps/core/templatetags/__init__.py` (vazio)

- [x] **Criar chatter_tags.py**
  - [x] Criar `apps/core/templatetags/chatter_tags.py`
  ```python
  from django import template
  from django.contrib.contenttypes.models import ContentType
  
  register = template.Library()
  
  @register.filter
  def content_type(obj):
      """
      Retorna 'app_label.model' para usar no Alpine.js
      
      Uso no template:
      <div x-data="chatterComponent('{{ object|content_type }}', '{{ object.id }}')">
      
      Exemplo de retorno: "crm.lead"
      """
      ct = ContentType.objects.get_for_model(obj)
      return f"{ct.app_label}.{ct.model}"
  ```

- [x] **Testing - Template Tags**
  - [x] Test: content_type retorna string correta
  - [x] Test: funciona com Lead → "crm.lead"
  - [x] Test: funciona com Contact → "contacts.contact"
  - [x] Test: funciona com Sale → "sales.saleorder"

---

## 3.12.3 ChatterMixin para Views (Auto-carregar dados)

Criar mixin Django para adicionar dados do chatter automaticamente nas DetailViews.

- [x] **Criar ChatterMixin**
  - [x] Criar em `apps/core/views.py`
  ```python
  from django.views.generic import DetailView
  from django.contrib.contenttypes.models import ContentType
  from apps.core.models import ChatterMessage, ChatterActivity
  
  class ChatterMixin:
      """
      Mixin para adicionar dados do chatter em qualquer DetailView.
      
      USO SIMPLES:
      ------------
      class LeadDetailView(ChatterMixin, DetailView):
          model = Lead
          template_name = 'crm/lead_detail.html'
      
      No template, incluir:
      {% include 'components/chatter.html' with object=lead %}
      
      O mixin adiciona automaticamente ao context:
      - whatsapp_messages: lista de mensagens WhatsApp (quando Fase 12 implementada)
      - chatter_messages: lista de emails + notas
      - activities: lista de atividades (audit log)
      """
      
      def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          obj = self.get_object()
          content_type = ContentType.objects.get_for_model(obj)
          
          # WhatsApp messages (PLACEHOLDER - Fase 12)
          # Quando Fase 12 implementada:
          # from apps.marketing.models import WhatsAppMessage
          # context['whatsapp_messages'] = WhatsAppMessage.objects.filter(
          #     content_type=content_type,
          #     object_id=obj.id
          # ).order_by('sent_at')
          context['whatsapp_messages'] = []
          
          # Chatter messages (emails + notas) - JÁ FUNCIONA!
          context['chatter_messages'] = ChatterMessage.objects.filter(
              content_type=content_type,
              object_id=obj.id
          ).select_related('author').order_by('-created_at')
          
          # Activities (audit log) - JÁ FUNCIONA!
          context['activities'] = ChatterActivity.objects.filter(
              content_type=content_type,
              object_id=obj.id
          ).select_related('user').order_by('-created_at')[:100]  # Últimas 100
          
          return context
  ```

- [x] **Documentar uso**
  - [x] Criar comentário explicativo no código
  - [x] Exemplo de uso em docstring

- [x] **Testing - ChatterMixin**
  - [x] Test: mixin adiciona context['chatter_messages']
  - [x] Test: mixin adiciona context['activities']
  - [x] Test: mixin adiciona context['whatsapp_messages'] (vazio por agora)
  - [x] Test: funciona com Lead
  - [x] Test: funciona com Contact

---

## 3.12.4 Componente Chatter HTML (Template BASE - será substituído)

Criar template PLACEHOLDER que será substituído pelo teu design depois.

- [x] **Criar template base**
  - [x] Criar `templates/components/chatter.html`
  - [x] **NOTA IMPORTANTE:** Este é um template BASE mínimo!
    - Será **SUBSTITUÍDO** quando tiveres o teu design pronto
    - Serve apenas para ter estrutura funcional desde já
    - Usa Alpine.js conforme tua stack

- [x] **Estrutura mínima (PLACEHOLDER):**
  ```html
  {% load static chatter_tags %}
  
  <!-- 
  COMPONENTE CHATTER - PLACEHOLDER
  Este template será substituído pelo design final.
  
  USO:
  {% include 'components/chatter.html' with object=lead %}
  {% include 'components/chatter.html' with object=contact %}
  -->
  
  <div 
      x-data="chatterComponent('{{ object|content_type }}', '{{ object.id }}')" 
      class="chatter-container bg-gray-800 rounded-lg p-4"
  >
      
      <!-- TABS -->
      <div class="tabs flex gap-2 mb-4 border-b border-gray-700">
          <button 
              @click="activeTab = 'whatsapp'"
              :class="activeTab === 'whatsapp' ? 'border-yellow-500 text-yellow-500' : 'border-transparent text-gray-400'"
              class="px-4 py-2 border-b-2 hover:text-white"
          >
              💬 WhatsApp
          </button>
          <button 
              @click="activeTab = 'messages'"
              :class="activeTab === 'messages' ? 'border-yellow-500 text-yellow-500' : 'border-transparent text-gray-400'"
              class="px-4 py-2 border-b-2 hover:text-white"
          >
              📧 Mensagens & Notas
          </button>
          <button 
              @click="activeTab = 'activity'"
              :class="activeTab === 'activity' ? 'border-yellow-500 text-yellow-500' : 'border-transparent text-gray-400'"
              class="px-4 py-2 border-b-2 hover:text-white"
          >
              📋 Atividade
          </button>
      </div>
      
      <!-- TAB: WHATSAPP -->
      <div x-show="activeTab === 'whatsapp'" class="tab-content">
          <div class="messages h-64 overflow-y-auto bg-gray-900 rounded p-4 mb-4">
              {% for msg in whatsapp_messages %}
              <div class="message mb-2">
                  <p class="text-white">{{ msg.content }}</p>
              </div>
              {% empty %}
              <p class="text-gray-500 text-center py-8">💬 Sem mensagens WhatsApp</p>
              {% endfor %}
          </div>
          <div class="input flex gap-2">
              <input 
                  type="text" 
                  x-model="whatsappMessage"
                  @keyup.enter="sendWhatsApp()"
                  placeholder="Mensagem..." 
                  class="flex-1 px-4 py-2 bg-gray-700 text-white rounded"
              >
              <button @click="sendWhatsApp()" class="px-6 py-2 bg-yellow-500 text-gray-900 rounded font-medium">
                  Enviar
              </button>
          </div>
      </div>
      
      <!-- TAB: MENSAGENS & NOTAS -->
      <div x-show="activeTab === 'messages'" class="tab-content">
          <!-- Toggle EMAIL/NOTE -->
          <div class="toggle-buttons flex gap-2 mb-4">
              <button 
                  @click="messageType = 'EMAIL'"
                  :class="messageType === 'EMAIL' ? 'bg-yellow-500 text-gray-900' : 'bg-gray-700 text-white'"
                  class="px-4 py-2 rounded"
              >
                  📧 Enviar Email
              </button>
              <button 
                  @click="messageType = 'NOTE'"
                  :class="messageType === 'NOTE' ? 'bg-yellow-500 text-gray-900' : 'bg-gray-700 text-white'"
                  class="px-4 py-2 rounded"
              >
                  📝 Adicionar Nota
              </button>
          </div>
          
          <!-- Histórico -->
          <div class="history h-48 overflow-y-auto bg-gray-900 rounded p-4 mb-4">
              {% for msg in chatter_messages %}
              <div class="item mb-3 pb-3 border-b border-gray-700">
                  <div class="flex justify-between items-start">
                      <div>
                          <strong class="text-white">{{ msg.author.get_full_name }}</strong>
                          {% if msg.is_note %}
                          <span class="text-xs bg-blue-600 px-2 py-0.5 rounded ml-2">Nota</span>
                          {% else %}
                          <span class="text-xs bg-green-600 px-2 py-0.5 rounded ml-2">Email</span>
                          {% endif %}
                      </div>
                      <span class="text-xs text-gray-400">{{ msg.created_at|date:"d/m/Y H:i" }}</span>
                  </div>
                  {% if msg.subject %}
                  <p class="text-sm text-gray-300 mt-1">{{ msg.subject }}</p>
                  {% endif %}
                  <p class="text-sm text-gray-400 mt-1">{{ msg.body|truncatewords:20 }}</p>
              </div>
              {% empty %}
              <p class="text-gray-500 text-center py-8">📭 Sem mensagens ou notas</p>
              {% endfor %}
          </div>
          
          <!-- Form -->
          <form @submit.prevent="sendMessageOrNote()">
              <input 
                  x-show="messageType === 'EMAIL'"
                  type="text" 
                  x-model="messageSubject"
                  placeholder="Assunto do email" 
                  class="w-full px-4 py-2 bg-gray-700 text-white rounded mb-2"
              >
              <textarea 
                  x-model="messageBody"
                  rows="3" 
                  placeholder="Escrever mensagem..." 
                  class="w-full px-4 py-2 bg-gray-700 text-white rounded mb-2"
              ></textarea>
              <div class="flex justify-between items-center">
                  <button type="button" class="text-gray-400 hover:text-white">
                      📎 Anexar ficheiro
                  </button>
                  <button type="submit" class="px-6 py-2 bg-yellow-500 text-gray-900 rounded font-medium">
                      <span x-text="messageType === 'EMAIL' ? 'Enviar Email' : 'Adicionar Nota'"></span>
                  </button>
              </div>
          </form>
      </div>
      
      <!-- TAB: ATIVIDADE -->
      <div x-show="activeTab === 'activity'" class="tab-content">
          <div class="timeline h-96 overflow-y-auto">
              {% for activity in activities %}
              <div class="item flex gap-3 mb-4">
                  <div class="icon w-8 h-8 rounded-full bg-yellow-500 flex items-center justify-center text-gray-900 flex-shrink-0">
                      {% if activity.activity_type == 'CREATE' %}➕
                      {% elif activity.activity_type == 'UPDATE' %}✏️
                      {% elif activity.activity_type == 'EMAIL_SENT' %}📧
                      {% elif activity.activity_type == 'WHATSAPP_SENT' %}💬
                      {% else %}📋
                      {% endif %}
                  </div>
                  <div class="flex-1">
                      <p class="text-sm text-white">
                          <strong>{{ activity.user.get_full_name }}</strong> {{ activity.description }}
                      </p>
                      <span class="text-xs text-gray-400">{{ activity.created_at|date:"d/m/Y H:i" }}</span>
                  </div>
              </div>
              {% empty %}
              <p class="text-gray-500 text-center py-8">📋 Sem atividades</p>
              {% endfor %}
          </div>
      </div>
      
  </div>
  
  <script>
  function chatterComponent(objectType, objectId) {
      return {
          objectType: objectType,
          objectId: objectId,
          activeTab: 'whatsapp',
          messageType: 'EMAIL',
          whatsappMessage: '',
          messageSubject: '',
          messageBody: '',
          
          sendWhatsApp() {
              console.log('[CHATTER] sendWhatsApp() called - PLACEHOLDER');
              console.log('Message:', this.whatsappMessage);
              console.log('Object:', this.objectType, this.objectId);
              
              // TODO: Implementar na Fase 12
              alert('Função sendWhatsApp() será implementada na Fase 12 (WhatsApp API)');
              
              // Limpar input
              this.whatsappMessage = '';
          },
          
          sendMessageOrNote() {
              console.log('[CHATTER] sendMessageOrNote() called - PLACEHOLDER');
              console.log('Type:', this.messageType);
              console.log('Subject:', this.messageSubject);
              console.log('Body:', this.messageBody);
              console.log('Object:', this.objectType, this.objectId);
              
              // TODO: Implementar depois (criar ChatterMessage via AJAX)
              alert(`Função sendMessageOrNote() será implementada depois.
Type: ${this.messageType}
Por agora é apenas PLACEHOLDER.`);
              
              // Limpar form
              this.messageSubject = '';
              this.messageBody = '';
          }
      }
  }
  </script>
  ```

- [x] **Incluir Alpine.js no base.html** (se ainda não tiver)
  - [x] Adicionar no `<head>` de `templates/base.html`:
    ```html
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    ```

- [x] **Testing - Template**
  - [x] Test: template renderiza sem erros
  - [x] Test: tabs funcionam ao clicar
  - [x] Test: toggle EMAIL/NOTE funciona
  - [x] Test: Alpine.js x-data inicializa
  - [x] Test: funções placeholder mostram alert

---

## 3.12.5 Views Placeholder (APIs REST)

Criar endpoints REST com lógica PLACEHOLDER (print apenas).

- [x] **Criar view para mensagens/notas**
  - [x] Criar em `apps/core/views.py`
  ```python
  from django.http import JsonResponse
  from django.contrib.auth.decorators import login_required
  from django.views.decorators.http import require_POST
  import json
  
  @login_required
  @require_POST
  def chatter_create_message(request):
      """
      API para criar email ou nota interna.
      
      POST /api/chatter/message/
      Body JSON:
      {
        "object_type": "crm.lead",
        "object_id": "uuid-aqui",
        "message_type": "EMAIL" ou "NOTE",
        "subject": "Assunto (só para EMAIL)",
        "body": "Conteúdo da mensagem"
      }
      
      NOTA: Esta é função PLACEHOLDER!
      A lógica completa será implementada depois:
      - Criar ChatterMessage na BD
      - Se EMAIL: enviar via SMTP (Tarefa 3.9)
      - Criar ChatterActivity para audit log
      """
      try:
          data = json.loads(request.body)
          
          # PLACEHOLDER: apenas print por agora
          print("=" * 50)
          print("[CHATTER API] chatter_create_message() CALLED")
          print(f"User: {request.user.get_full_name()}")
          print(f"Object Type: {data.get('object_type')}")
          print(f"Object ID: {data.get('object_id')}")
          print(f"Message Type: {data.get('message_type')}")
          print(f"Subject: {data.get('subject')}")
          print(f"Body: {data.get('body')[:100]}...")
          print("=" * 50)
          
          # TODO: Implementar lógica completa
          # 1. Parse ContentType
          # 2. Criar ChatterMessage
          # 3. Se EMAIL: enviar via Celery
          # 4. Criar ChatterActivity
          
          return JsonResponse({
              'success': True,
              'message': 'PLACEHOLDER - Função será implementada depois'
          })
      
      except Exception as e:
          print(f"[CHATTER API] ERROR: {e}")
          return JsonResponse({
              'success': False,
              'error': str(e)
          }, status=400)
  ```

- [x] **Criar view para WhatsApp**
  - [x] Criar em `apps/core/views.py`
  ```python
  @login_required
  @require_POST
  def chatter_send_whatsapp(request):
      """
      API para enviar WhatsApp.
      
      POST /api/chatter/whatsapp/
      Body JSON:
      {
        "object_type": "crm.lead",
        "object_id": "uuid-aqui",
        "message": "Texto da mensagem"
      }
      
      NOTA: Função PLACEHOLDER!
      Será implementada na Fase 12 (WhatsApp API).
      """
      try:
          data = json.loads(request.body)
          
          # PLACEHOLDER: apenas print
          print("=" * 50)
          print("[CHATTER API] chatter_send_whatsapp() CALLED")
          print(f"User: {request.user.get_full_name()}")
          print(f"Object Type: {data.get('object_type')}")
          print(f"Object ID: {data.get('object_id')}")
          print(f"Message: {data.get('message')}")
          print("=" * 50)
          
          # TODO: Implementar na Fase 12
          # 1. Buscar objeto via GenericForeignKey
          # 2. Obter phone do contacto
          # 3. Enviar via WhatsApp API
          # 4. Criar WhatsAppMessage
          # 5. Criar ChatterActivity
          
          return JsonResponse({
              'success': True,
              'message': 'PLACEHOLDER - Função será implementada na Fase 12'
          })
      
      except Exception as e:
          print(f"[CHATTER API] ERROR: {e}")
          return JsonResponse({
              'success': False,
              'error': str(e)
          }, status=400)
  ```

- [x] **Configurar rotas**
  - [x] Adicionar em `config/urls.py`:
    ```python
    from apps.core.views import chatter_create_message, chatter_send_whatsapp
    
    urlpatterns = [
        # ... outras rotas
        
        # Chatter APIs (PLACEHOLDERS)
        path('api/chatter/message/', chatter_create_message, name='chatter_create_message'),
        path('api/chatter/whatsapp/', chatter_send_whatsapp, name='chatter_send_whatsapp'),
    ]
    ```

- [x] **Testing - APIs**
  - [x] Test: POST /api/chatter/message/ retorna success
  - [x] Test: POST /api/chatter/whatsapp/ retorna success
  - [x] Test: print aparece no console
  - [x] Test: user não autenticado retorna 403

---

## 3.12.6 Documentação e Notas para o Futuro

Criar documentação para lembrar o que falta implementar.

- [x] **Criar TODO.md**
  - [x] Criar `docs/chatter_todo.md`
  ```markdown
  # CHATTER - TODO LIST
  
  ## ✅ IMPLEMENTADO (Tarefa 3.12)
  - [x] Modelos ChatterMessage e ChatterActivity
  - [x] Template tags (content_type)
  - [x] ChatterMixin para views
  - [x] Template base chatter.html (PLACEHOLDER - será substituído)
  - [x] APIs REST com funções PLACEHOLDER
  - [x] Alpine.js component
  
  ## 🔄 PRÓXIMOS PASSOS
  
  ### 1. Substituir Template pelo Design Final
  - [x] Criar design visual no CRM
  - [x] Usar PROMPT do VS Code para componentizar
  - [x] Substituir templates/components/chatter.html
  
  ### 2. Implementar Lógica de Emails (Tarefa 3.9) ✅ COMPLETO — ver secção 5.12.6
  - [x] Configurar SMTP — `UserEmailConfig` por utilizador, Fernet-encriptado
  - [x] Implementar `send_email_for_record()` em `apps/core/email_utils.py`
  - [x] Criar `ChatterMessage` na BD (via `GenericForeignKey`, universal)
  - [x] Enviar email via SMTP (Gmail / Outlook STARTTLS)
  - [x] Suporte a CC, BCC, múltiplos destinatários (vírgula), anexos
  - [x] Criar `ChatterActivity` automaticamente *(registo via ChatterMessage)*
  
  ### 3. Implementar WhatsApp (Fase 12)
  - [x] Setup Meta WhatsApp API
  - [x] Criar modelo WhatsAppMessage
  - [x] Implementar função real em chatter_send_whatsapp()
  - [x] Webhook para receber mensagens
  - [x] Processar mensagens via Celery
  
  ### 4. Auto-logging de Atividades (Signals)
  - [x] Criar signals para detetar mudanças
  - [x] Criar ChatterActivity automaticamente
  - [x] Middleware para capturar user atual
  
  ### 5. Anexos ✅ COMPLETO
  - [x] Upload de ficheiros (multipart/form-data)
  - [x] Guardar em `media/chatter/<lead_id>/` via `default_storage`
  - [x] Adicionar URL ao `attachments` JSONField
  - [x] Chips de ficheiros clicáveis na bubble do chat
  - [x] Preview de mime type (imagem, PDF, Word, Excel, etc.)
  ```

- [x] **Adicionar comentários no código**
  - [x] Comentar funções placeholder com TODO
  - [x] Explicar que será implementado depois

- [x] **Testing - Documentação**
  - [x] Test: TODO.md existe e está completo
  - [x] Test: comentários TODO estão no código

---

## 3.12.7 Testing Completo

Testar tudo o que foi implementado.

- [x] **Testes de Modelos**
  - [x] Test: criar ChatterMessage tipo EMAIL *(testado em produção — Message-ID confirmado)*
  - [x] Test: criar ChatterMessage tipo NOTE
  - [x] Test: GenericForeignKey funciona com Lead
  - [x] Test: GenericForeignKey funciona com Contact
  - [x] Test: criar ChatterActivity
  - [x] Test: attachments JSON funciona
  - [x] Test: visualizar no Admin

- [x] **Testes de Template Tags**
  - [x] Test: {{ object|content_type }} retorna string correta

- [x] **Testes de ChatterMixin**
  - [x] Test: incluir mixin em view adiciona context
  - [x] Test: context['chatter_messages'] existe
  - [x] Test: context['activities'] existe

- [x] **Testes de Template**
  - [x] Test: incluir chatter.html funciona
  - [x] Test: tabs renderizam
  - [x] Test: Alpine.js inicializa
  - [x] Test: clicar em tabs troca conteúdo

- [x] **Testes de APIs**
  - [x] Test: chamar /api/chatter/message/ mostra print
  - [x] Test: chamar /api/chatter/whatsapp/ mostra print
  - [x] Test: alert aparece ao usar funções

- [x] **Teste de Integração**
  - [x] Test: criar Lead → abrir detalhe → chatter aparece
  - [x] Test: incluir ChatterMixin em LeadDetailView
  - [x] Test: template funciona sem erros


## 3.12.8 Sistema de Menções (@username) em Notas

Permitir mencionar outros utilizadores em notas e criar notificações automáticas.

- [x] **Atualizar modelo ChatterMessage**
  - [x] Adicionar campo `mentioned_users` em `apps/core/models.py`:
    ```python
    class ChatterMessage(AbstractBaseModel):
        # ... campos existentes ...
        
        # NOVO: Menções
        mentioned_users = models.ManyToManyField(
            CustomUser,
            related_name='mentioned_in_messages',
            blank=True,
            help_text='Utilizadores mencionados com @ nesta mensagem'
        )
    ```
  - [x] Criar migration:
    ```bash
    python manage.py makemigrations core
    python manage.py migrate
    ```

- [x] **Criar helper function para parse de menções**
  - [x] Criar `apps/core/utils.py` (se não existir)
  - [x] Função `extract_mentions(text)`:
    ```python
    import re
    from apps.accounts.models import CustomUser
    
    def extract_mentions(text):
        """
        Extrai menções @username do texto.
        
        Exemplo:
        "Olá @joao, preciso que vejas isto @maria"
        → retorna [user_joao, user_maria]
        
        Args:
            text (str): Texto da mensagem/nota
            
        Returns:
            list: Lista de CustomUser objects mencionados
        """
        # Regex para encontrar @username
        pattern = r'@(\w+)'
        usernames = re.findall(pattern, text)
        
        # Buscar users na BD
        mentioned = []
        for username in usernames:
            try:
                # Buscar por username (se existir) ou por first_name
                user = CustomUser.objects.filter(
                    models.Q(username__iexact=username) |
                    models.Q(first_name__iexact=username)
                ).first()
                
                if user and user not in mentioned:
                    mentioned.append(user)
            except CustomUser.DoesNotExist:
                continue
        
        return mentioned
    ```

- [x] **Atualizar view chatter_create_message**
  - [x] Modificar `apps/core/views.py`:
    ```python
    @login_required
    @require_POST
    def chatter_create_message(request):
        try:
            data = json.loads(request.body)
            
            # Parse ContentType
            object_type = data.get('object_type')
            object_id = data.get('object_id')
            app_label, model_name = object_type.split('.')
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
            
            # Criar mensagem
            message = ChatterMessage.objects.create(
                content_type=content_type,
                object_id=object_id,
                author=request.user,
                message_type=data.get('message_type'),
                subject=data.get('subject', ''),
                body=data.get('body'),
                is_internal=(data.get('message_type') == 'NOTE')
            )
            
            # NOVO: Extrair e adicionar menções
            from apps.core.utils import extract_mentions
            mentioned = extract_mentions(message.body)
            message.mentioned_users.set(mentioned)
            
            # NOVO: Criar notificações para mencionados
            from apps.core.models import Notification
            for user in mentioned:
                if user != request.user:  # Não notificar a si próprio
                    Notification.objects.create(
                        user=user,
                        notification_type='MENTION',
                        title=f'{request.user.get_full_name()} mencionou-te',
                        message=f'em {content_type.model}: {message.body[:100]}...',
                        link=f'#',  # TODO: link para o objeto
                        related_content_type=content_type,
                        related_object_id=object_id
                    )
            
            # Criar atividade
            ChatterActivity.objects.create(
                content_type=content_type,
                object_id=object_id,
                user=request.user,
                activity_type='COMMENT' if message.is_note else 'EMAIL_SENT',
                description=f"{'adicionou uma nota' if message.is_note else 'enviou um email'}"
            )
            
            return JsonResponse({
                'success': True,
                'message_id': str(message.id),
                'mentioned_count': len(mentioned)
            })
        
        except Exception as e:
            print(f"[CHATTER API] ERROR: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    ```

- [x] **Testing - Menções**
  - [x] Test: criar nota com @joao cria menção
  - [x] Test: mentioned_users contém user correto
  - [x] Test: notificação é criada para mencionado
  - [x] Test: não cria notificação para autor

---

## 3.12.9 Modelo de Notificações ✅ COMPLETO

Criar modelo para notificações internas do sistema.

- [x] **Criar modelo Notification** em `apps/core/models.py` com tipos: ACTIVITY_OVERDUE, ACTIVITY_TODAY, ACTIVITY_UPCOMING, MENTION, ASSIGNMENT, WHATSAPP, EMAIL, STAGE_CHANGE, COMMENT, SYSTEM
- [x] `PRIORITY_MAP` para ordenação (menor = mais urgente)
- [x] `is_urgent` flag (auto-set para ACTIVITY_OVERDUE)
- [x] GenericForeignKey (`related_content_type` + `related_object_id`)
- [x] `mark_as_read()` method
- [x] Migration aplicada
- [x] `NotificationAdmin` registado com actions `mark_as_read` / `mark_as_unread`
  - [x] Criar em `apps/core/models.py`:
    ```python
    class Notification(AbstractBaseModel):
        """
        Notificações internas do sistema.
        
        Exemplos:
        - User X mencionou-te em Lead Y
        - Lead Z foi atribuído a ti
        - Nova resposta no WhatsApp do Contact W
        """
        
        NOTIFICATION_TYPES = [
            ('MENTION', 'Menção'),
            ('ASSIGNMENT', 'Atribuição'),
            ('WHATSAPP', 'WhatsApp'),
            ('EMAIL', 'Email'),
            ('STAGE_CHANGE', 'Mudança de Estágio'),
            ('COMMENT', 'Comentário'),
            ('TASK', 'Tarefa'),
            ('SYSTEM', 'Sistema'),
        ]
        
        # Destinatário
        user = models.ForeignKey(
            CustomUser,
            on_delete=models.CASCADE,
            related_name='notifications',
            help_text='Utilizador que vai receber a notificação'
        )
        
        # Tipo e conteúdo
        notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
        title = models.CharField(max_length=255)  # "João mencionou-te"
        message = models.TextField()  # "em Lead XYZ: preciso da tua ajuda..."
        
        # Link (opcional)
        link = models.CharField(max_length=500, blank=True)  # URL para clicar
        
        # Objeto relacionado (opcional - GenericForeignKey)
        related_content_type = models.ForeignKey(
            ContentType,
            on_delete=models.CASCADE,
            null=True,
            blank=True
        )
        related_object_id = models.UUIDField(null=True, blank=True)
        related_object = GenericForeignKey('related_content_type', 'related_object_id')
        
        # Estado
        is_read = models.BooleanField(default=False)
        read_at = models.DateTimeField(null=True, blank=True)
        
        class Meta:
            ordering = ['-created_at']
            indexes = [
                models.Index(fields=['user', 'is_read']),
                models.Index(fields=['user', '-created_at']),
            ]
            verbose_name = 'Notificação'
            verbose_name_plural = 'Notificações'
        
        def __str__(self):
            return f"{self.user.get_full_name()} - {self.title}"
        
        def mark_as_read(self):
            """Marcar notificação como lida"""
            from django.utils import timezone
            if not self.is_read:
                self.is_read = True
                self.read_at = timezone.now()
                self.save(update_fields=['is_read', 'read_at'])
    ```

- [x] **Criar migrations**
  - [x] `python manage.py makemigrations core`
  - [x] `python manage.py migrate`

- [x] **Registrar no Admin**
  - [x] Criar NotificationAdmin:
    ```python
    @admin.register(Notification)
    class NotificationAdmin(admin.ModelAdmin):
        list_display = ['id', 'user', 'notification_type', 'title', 'is_read', 'created_at']
        list_filter = ['notification_type', 'is_read', 'created_at']
        search_fields = ['title', 'message', 'user__first_name', 'user__last_name']
        readonly_fields = ['related_content_type', 'related_object_id', 'read_at', 'created_at']
        
        actions = ['mark_as_read']
        
        def mark_as_read(self, request, queryset):
            count = 0
            for notification in queryset:
                notification.mark_as_read()
                count += 1
            self.message_user(request, f'{count} notificações marcadas como lidas.')
        mark_as_read.short_description = 'Marcar como lido'
    ```

- [x] **Testing - Notification Model**
  - [x] Test: criar notificação funciona
  - [x] Test: mark_as_read() atualiza is_read e read_at
  - [x] Test: GenericForeignKey funciona
  - [x] Test: ordenação por -created_at

---

## 3.12.10 API de Notificações

Criar endpoints REST para obter e marcar notificações.

- [x] **Criar view para listar notificações**
  - [x] Criar em `apps/core/views.py`:
    ```python
    @login_required
    def notifications_list_api(request):
        """
        API para listar notificações do user atual.
        
        GET /api/notifications/
        Query params:
        - unread_only: true/false (default: false)
        - limit: int (default: 50)
        
        Response:
        {
          "unread_count": 5,
          "notifications": [
            {
              "id": "uuid",
              "type": "MENTION",
              "title": "João mencionou-te",
              "message": "em Lead XYZ...",
              "link": "/crm/leads/uuid/",
              "is_read": false,
              "created_at": "2026-02-13 10:30"
            },
            ...
          ]
        }
        """
        unread_only = request.GET.get('unread_only', 'false').lower() == 'true'
        limit = int(request.GET.get('limit', 50))
        
        # Buscar notificações
        notifications = Notification.objects.filter(user=request.user)
        
        if unread_only:
            notifications = notifications.filter(is_read=False)
        
        notifications = notifications[:limit]
        
        # Serializar
        data = {
            'unread_count': Notification.objects.filter(user=request.user, is_read=False).count(),
            'notifications': [
                {
                    'id': str(n.id),
                    'type': n.notification_type,
                    'title': n.title,
                    'message': n.message,
                    'link': n.link,
                    'is_read': n.is_read,
                    'created_at': n.created_at.strftime('%d/%m/%Y %H:%M')
                }
                for n in notifications
            ]
        }
        
        return JsonResponse(data)
    ```

- [x] **Criar view para marcar como lido**
  - [x] Criar em `apps/core/views.py`:
    ```python
    @login_required
    @require_POST
    def notification_mark_read(request, notification_id):
        """
        API para marcar notificação como lida.
        
        POST /api/notifications/<uuid>/mark-read/
        """
        try:
            notification = Notification.objects.get(
                id=notification_id,
                user=request.user  # Apenas próprias notificações
            )
            notification.mark_as_read()
            
            return JsonResponse({
                'success': True,
                'unread_count': Notification.objects.filter(
                    user=request.user,
                    is_read=False
                ).count()
            })
        
        except Notification.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Notificação não encontrada'
            }, status=404)
    ```

- [x] **Criar view para marcar TODAS como lidas**
  - [x] Criar em `apps/core/views.py`:
    ```python
    @login_required
    @require_POST
    def notifications_mark_all_read(request):
        """
        API para marcar todas as notificações como lidas.
        
        POST /api/notifications/mark-all-read/
        """
        from django.utils import timezone
        
        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return JsonResponse({
            'success': True,
            'marked_count': count
        })
    ```

- [x] **Configurar rotas**
  - [x] Adicionar em `config/urls.py`:
    ```python
    from apps.core.views import (
        notifications_list_api,
        notification_mark_read,
        notifications_mark_all_read
    )
    
    urlpatterns = [
        # ... rotas existentes ...
        
        # Notificações
        path('api/notifications/', notifications_list_api, name='notifications_list'),
        path('api/notifications/<uuid:notification_id>/mark-read/', notification_mark_read, name='notification_mark_read'),
        path('api/notifications/mark-all-read/', notifications_mark_all_read, name='notifications_mark_all_read'),
    ]
    ```

- [x] **Testing - APIs**
  - [x] Test: GET /api/notifications/ retorna lista
  - [x] Test: unread_count está correto
  - [x] Test: POST mark-read funciona
  - [x] Test: POST mark-all-read funciona

---

## 3.12.11 Badge de Notificações no Navbar

Atualizar navbar para mostrar contador de notificações não lidas.

- [x] **Atualizar base.html (navbar)**
  - [x] Modificar `templates/base.html`:
    ```html
    <!-- Adicionar no navbar (onde já tens o botão placeholder) -->
    <div class="relative" x-data="notificationsDropdown()">
        <!-- Botão Bell -->
        <button 
            @click="toggle()"
            class="relative p-2 text-gray-400 hover:text-white"
        >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
            </svg>
            
            <!-- Badge com contador -->
            <span 
                x-show="unreadCount > 0"
                x-text="unreadCount"
                class="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-red-100 transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full"
            ></span>
        </button>
        
        <!-- Dropdown -->
        <div 
            x-show="isOpen"
            @click.away="isOpen = false"
            x-transition
            class="absolute right-0 mt-2 w-80 bg-gray-800 rounded-lg shadow-lg border border-gray-700 overflow-hidden z-50"
        >
            <!-- Header -->
            <div class="flex items-center justify-between px-4 py-3 border-b border-gray-700">
                <h3 class="text-white font-medium">Notificações</h3>
                <button 
                    @click="markAllRead()"
                    class="text-xs text-yellow-500 hover:text-yellow-400"
                >
                    Marcar todas como lidas
                </button>
            </div>
            
            <!-- Lista -->
            <div class="max-h-96 overflow-y-auto">
                <template x-for="notif in notifications" :key="notif.id">
                    <div 
                        @click="markRead(notif.id)"
                        :class="notif.is_read ? 'bg-gray-800' : 'bg-gray-700'"
                        class="px-4 py-3 border-b border-gray-700 hover:bg-gray-600 cursor-pointer"
                    >
                        <p class="text-sm font-medium text-white" x-text="notif.title"></p>
                        <p class="text-xs text-gray-400 mt-1" x-text="notif.message"></p>
                        <span class="text-xs text-gray-500" x-text="notif.created_at"></span>
                    </div>
                </template>
                
                <template x-if="notifications.length === 0">
                    <div class="px-4 py-8 text-center text-gray-500">
                        Sem notificações
                    </div>
                </template>
            </div>
        </div>
    </div>
    
    <script>
    function notificationsDropdown() {
        return {
            isOpen: false,
            unreadCount: 0,
            notifications: [],
            
            init() {
                this.load();
                // Polling a cada 30 segundos
                setInterval(() => this.load(), 30000);
            },
            
            async load() {
                try {
                    const response = await fetch('/api/notifications/?limit=10');
                    const data = await response.json();
                    this.unreadCount = data.unread_count;
                    this.notifications = data.notifications;
                } catch (error) {
                    console.error('Erro ao carregar notificações:', error);
                }
            },
            
            toggle() {
                this.isOpen = !this.isOpen;
                if (this.isOpen) {
                    this.load();
                }
            },
            
            async markRead(notificationId) {
                try {
                    const response = await fetch(`/api/notifications/${notificationId}/mark-read/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': this.getCookie('csrftoken')
                        }
                    });
                    
                    const data = await response.json();
                    if (data.success) {
                        this.unreadCount = data.unread_count;
                        this.load();
                    }
                } catch (error) {
                    console.error('Erro ao marcar como lida:', error);
                }
            },
            
            async markAllRead() {
                try {
                    const response = await fetch('/api/notifications/mark-all-read/', {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': this.getCookie('csrftoken')
                        }
                    });
                    
                    const data = await response.json();
                    if (data.success) {
                        this.unreadCount = 0;
                        this.load();
                    }
                } catch (error) {
                    console.error('Erro ao marcar todas:', error);
                }
            },
            
            getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
        }
    }
    </script>
    ```

- [x] **Testing - Badge**
  - [x] Test: badge mostra contador correto
  - [x] Test: clicar abre dropdown
  - [x] Test: clicar em notificação marca como lida
  - [x] Test: "Marcar todas" funciona
  - [x] Test: polling atualiza a cada 30s

---

## 3.12.12 Autocomplete de Menções (@) no Chatter

Criar dropdown de autocomplete quando digitar @ no textarea.

- [x] **Criar API para buscar users**
  - [x] Criar em `apps/core/views.py`:
    ```python
    @login_required
    def users_search_api(request):
        """
        API para buscar utilizadores (autocomplete).
        
        GET /api/users/search/?q=joao
        
        Response:
        [
          {"id": "uuid", "name": "João Silva", "username": "joao"},
          {"id": "uuid", "name": "João Pedro", "username": "jpedr"}
        ]
        """
        query = request.GET.get('q', '').strip()
        
        if len(query) < 2:
            return JsonResponse([], safe=False)
        
        # Buscar users da mesma company
        users = CustomUser.objects.filter(
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query) |
            models.Q(username__icontains=query),
            is_active=True
        ).exclude(id=request.user.id)[:10]  # Máximo 10
        
        # Serializar
        data = [
            {
                'id': str(u.id),
                'name': u.get_full_name(),
                'username': u.username or u.first_name.lower()
            }
            for u in users
        ]
        
        return JsonResponse(data, safe=False)
    ```

- [x] **Configurar rota**
  - [x] Adicionar em `config/urls.py`:
    ```python
    path('api/users/search/', users_search_api, name='users_search'),
    ```

- [x] **Adicionar JavaScript autocomplete no chatter**
  - [x] Atualizar `templates/components/chatter.html`:
    ```html
    <!-- Adicionar ao Alpine component -->
    <script>
    function chatterComponent(objectType, objectId) {
        return {
            // ... state existente ...
            
            // NOVO: Autocomplete menções
            mentionQuery: '',
            mentionResults: [],
            showMentions: false,
            mentionPosition: 0,
            
            // Detetar @ no textarea
            onBodyInput(event) {
                const textarea = event.target;
                const text = textarea.value;
                const cursorPos = textarea.selectionStart;
                
                // Buscar última @ antes do cursor
                const beforeCursor = text.substring(0, cursorPos);
                const match = beforeCursor.match(/@(\w*)$/);
                
                if (match) {
                    this.mentionQuery = match[1];
                    this.searchUsers(this.mentionQuery);
                    this.showMentions = true;
                } else {
                    this.showMentions = false;
                }
            },
            
            async searchUsers(query) {
                if (query.length < 1) {
                    this.mentionResults = [];
                    return;
                }
                
                try {
                    const response = await fetch(`/api/users/search/?q=${query}`);
                    this.mentionResults = await response.json();
                } catch (error) {
                    console.error('Erro ao buscar users:', error);
                }
            },
            
            insertMention(user) {
                // Substituir @query por @username
                const textarea = document.getElementById('message-body');
                const text = textarea.value;
                const cursorPos = textarea.selectionStart;
                
                const beforeCursor = text.substring(0, cursorPos);
                const afterCursor = text.substring(cursorPos);
                
                // Substituir último @query
                const newBefore = beforeCursor.replace(/@\w*$/, `@${user.username} `);
                
                this.messageBody = newBefore + afterCursor;
                this.showMentions = false;
                
                // Refocar textarea
                this.$nextTick(() => {
                    textarea.focus();
                    textarea.setSelectionRange(newBefore.length, newBefore.length);
                });
            }
        }
    }
    </script>
    
    <!-- HTML: Dropdown autocomplete -->
    <div x-show="showMentions" class="relative">
        <div class="absolute bottom-full left-0 mb-2 w-64 bg-gray-700 rounded shadow-lg max-h-48 overflow-y-auto">
            <template x-for="user in mentionResults" :key="user.id">
                <div 
                    @click="insertMention(user)"
                    class="px-4 py-2 hover:bg-gray-600 cursor-pointer flex items-center gap-2"
                >
                    <div class="w-8 h-8 rounded-full bg-yellow-500 flex items-center justify-center text-gray-900 font-bold">
                        <span x-text="user.name.charAt(0)"></span>
                    </div>
                    <div>
                        <p class="text-sm text-white" x-text="user.name"></p>
                        <p class="text-xs text-gray-400" x-text="'@' + user.username"></p>
                    </div>
                </div>
            </template>
        </div>
    </div>
    
    <!-- Textarea com autocomplete -->
    <textarea 
        id="message-body"
        x-model="messageBody"
        @input="onBodyInput($event)"
        rows="3" 
        placeholder="Escrever mensagem... (usa @ para mencionar alguém)" 
        class="w-full px-4 py-2 bg-gray-700 text-white rounded mb-2"
    ></textarea>
    ```

- [x] **Testing - Autocomplete**
  - [x] Test: digitar @ abre dropdown
  - [x] Test: digitar @joa filtra users
  - [x] Test: clicar em user insere @username
  - [x] Test: API retorna users corretos

---

## 3.13 Sistema de Activities Genérico (Scheduled Activities)

**🎯 OBJETIVO:** Criar sistema genérico de activities agendadas (tasks/to-dos) que funciona com QUALQUER modelo (Lead, Sale, Purchase, Invoice, etc.) com automação de workflows e templates reutilizáveis.

**🔑 CONCEITOS-CHAVE:**
- **ScheduledActivity:** Tarefa agendada futura (CALL, EMAIL, MEETING, TODO, WHATSAPP)
- **ActivityTemplate:** Template reutilizável de activity (ex: "Follow-up Call", "Send Quote")
- **ActivityWorkflow:** Regras de automação (ex: "Se CALL marcada como SUCCESS → criar EMAIL em +1 dia")

**📋 DIFERENÇA vs ChatterActivity:**
- **ChatterActivity** = Audit log (histórico passado) - "João mudou stage de New para Qualified"
- **ScheduledActivity** = Task agendada (futuro/to-do) - "Ligar ao cliente dia 20/02"

---

### 3.13.1 Modelo ScheduledActivity ✅

Criar modelo genérico para activities agendadas com GenericForeignKey.

- [x] **Criar modelo ScheduledActivity**
  - [x] Criar em `apps/core/models.py`
  - [x] **GenericForeignKey (funciona com QUALQUER modelo - Lead, Sale, Purchase, etc.):**
    ```python
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    ```
  
  - [x] **Campos principais:**
    ```python
    # Tipo de activity
    ACTIVITY_TYPE_CHOICES = [
        ('CALL', 'Phone Call'),
        ('EMAIL', 'Email'),
        ('MEETING', 'Meeting'),
        ('TODO', 'To-Do'),
        ('WHATSAPP', 'WhatsApp'),
        ('DOCUMENT', 'Document'),
        ('SIGNATURE', 'Signature'),
    ]
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    
    # Conteúdo
    summary = models.CharField(max_length=255, verbose_name='Summary')
    description = models.TextField(blank=True, verbose_name='Description')
    
    # Scheduling
    due_date = models.DateField(verbose_name='Due Date')
    due_time = models.TimeField(null=True, blank=True, verbose_name='Due Time')
    
    # Assignment
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='scheduled_activities',
        verbose_name='Assigned To'
    )
    
    # Status
    is_done = models.BooleanField(default=False, verbose_name='Is Done')
    done_date = models.DateTimeField(null=True, blank=True, verbose_name='Done Date')
    
    # Resultado (para workflows)
    RESULT_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('CALLBACK', 'Callback Later'),
        ('NO_ANSWER', 'No Answer'),
        ('NOT_INTERESTED', 'Not Interested'),
    ]
    result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        null=True,
        blank=True,
        verbose_name='Result',
        help_text='Resultado usado para workflows automáticos'
    )
    
    # Feedback texto livre
    feedback = models.TextField(
        blank=True,
        verbose_name='Feedback',
        help_text='Notas quando marcar como concluída'
    )
    
    # Template (opcional)
    template = models.ForeignKey(
        'ActivityTemplate',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activities',
        verbose_name='Template',
        help_text='Template usado para criar esta activity (opcional)'
    )
    
    # Multi-company
    owner_company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='scheduled_activities',
        verbose_name='Owner Company'
    )
    ```

  - [x] **Properties:**
    ```python
    @property
    def is_overdue(self):
        """Retorna True se passou do prazo e não está done"""
        if self.is_done:
            return False
        from django.utils import timezone
        today = timezone.now().date()
        return self.due_date < today
    
    @property
    def is_today(self):
        """Retorna True se é para hoje"""
        from django.utils import timezone
        today = timezone.now().date()
        return self.due_date == today and not self.is_done
    
    @property
    def status_color(self):
        """Retorna cor baseada em status"""
        if self.is_done:
            return 'green'
        elif self.is_overdue:
            return 'red'
        elif self.is_today:
            return 'yellow'
        else:
            return 'blue'
    
    @property
    def icon(self):
        """Retorna ícone baseado em activity_type"""
        icons = {
            'CALL': '📞',
            'EMAIL': '📧',
            'MEETING': '🤝',
            'TODO': '✅',
            'WHATSAPP': '💬',
            'DOCUMENT': '📄',
            'SIGNATURE': '✍️',
        }
        return icons.get(self.activity_type, '📋')
    
    def __str__(self):
        return f"{self.get_activity_type_display()} - {self.summary}"
    ```

  - [x] **Meta:**
    ```python
    class Meta:
        ordering = ['due_date', 'due_time', '-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['due_date']),
            models.Index(fields=['is_done']),
        ]
        verbose_name = 'Scheduled Activity'
        verbose_name_plural = 'Scheduled Activities'
    ```

  - [x] **Validações:**
    ```python
    def clean(self):
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        # Validar: due_date não pode ser no passado (ao criar)
        if not self.pk and self.due_date < timezone.now().date():
            raise ValidationError({'due_date': 'Due date cannot be in the past'})
        
        # Validar: result ou feedback obrigatório ao marcar is_done=True
        if self.is_done and not self.result and not self.feedback:
            raise ValidationError(
                'Must provide either result or feedback when marking as done'
            )
    
    def save(self, *args, **kwargs):
        from django.utils import timezone
        
        # Auto-preencher done_date quando is_done muda para True
        if self.is_done and not self.done_date:
            self.done_date = timezone.now()
        
        # Limpar done_date se is_done muda para False
        if not self.is_done and self.done_date:
            self.done_date = None
        
        super().save(*args, **kwargs)
    ```

---

### 3.13.2 Modelo ActivityTemplate ✅

Criar modelo para templates reutilizáveis de activities.

- [x] **Criar modelo ActivityTemplate**
  - [x] Criar em `apps/core/models.py`
  - [x] **Campos:**
    ```python
    name = models.CharField(
        max_length=100,
        verbose_name='Template Name',
        help_text='Ex: "Follow-up Call", "Send Quote Email"'
    )
    
    activity_type = models.CharField(
        max_length=20,
        choices=ScheduledActivity.ACTIVITY_TYPE_CHOICES,
        verbose_name='Activity Type'
    )
    
    default_summary = models.CharField(
        max_length=255,
        verbose_name='Default Summary',
        help_text='Pode usar variáveis: {{contact_name}}, {{company_name}}'
    )
    
    default_description = models.TextField(
        blank=True,
        verbose_name='Default Description'
    )
    
    # Offset de dias (ex: +3 dias a partir de hoje)
    due_days_offset = models.IntegerField(
        default=0,
        verbose_name='Due Days Offset',
        help_text='Dias a adicionar à data atual (ex: 3 = daqui a 3 dias)'
    )
    
    # Campos opcionais
    default_assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='activity_templates',
        verbose_name='Default Assigned To',
        help_text='Responsável padrão (opcional)'
    )
    
    # Multi-company
    owner_company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activity_templates',
        verbose_name='Owner Company',
        help_text='NULL=global template, with value=private to company'
    )
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    ```

  - [x] **Methods:**
    ```python
    def __str__(self):
        return f"{self.name} ({self.get_activity_type_display()})"
    
    def create_activity(self, content_object, assigned_to=None, **kwargs):
        """
        Criar ScheduledActivity a partir deste template.
        
        Args:
            content_object: Objeto relacionado (Lead, Sale, etc.)
            assigned_to: User (opcional, usa default se None)
            **kwargs: Sobrescrever campos (summary, description, etc.)
        
        Returns:
            ScheduledActivity instance
        """
        from django.utils import timezone
        from datetime import timedelta
        
        # Calcular due_date
        due_date = timezone.now().date() + timedelta(days=self.due_days_offset)
        
        # Preparar dados
        activity_data = {
            'content_object': content_object,
            'template': self,
            'activity_type': self.activity_type,
            'summary': self.default_summary,
            'description': self.default_description,
            'due_date': due_date,
            'assigned_to': assigned_to or self.default_assigned_to,
            'owner_company': self.owner_company,
        }
        
        # Sobrescrever com kwargs
        activity_data.update(kwargs)
        
        # Criar activity
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(content_object)
        
        activity = ScheduledActivity.objects.create(
            content_type=ct,
            object_id=content_object.pk,
            **{k: v for k, v in activity_data.items() if k not in ['content_object']}
        )
        
        return activity
    ```

  - [x] **Meta:**
    ```python
    class Meta:
        ordering = ['name']
        verbose_name = 'Activity Template'
        verbose_name_plural = 'Activity Templates'
        unique_together = ['name', 'owner_company']
    ```

---

### 3.13.3 Modelo ActivityWorkflow ✅

Criar modelo para regras de automação de workflows.

- [x] **Criar modelo ActivityWorkflow**
  - [x] Criar em `apps/core/models.py`
  - [x] **Campos:**
    ```python
    name = models.CharField(
        max_length=100,
        verbose_name='Workflow Name',
        help_text='Ex: "Lead Nurturing - First Contact Success"'
    )
    
    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Explicação do workflow'
    )
    
    # Modelo que usa este workflow (Lead, Sale, etc.)
    model = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Model',
        help_text='Modelo que dispara este workflow (Lead, Sale, Purchase, etc.)'
    )
    
    # Trigger: qual tipo de activity dispara
    trigger_activity_type = models.CharField(
        max_length=20,
        choices=ScheduledActivity.ACTIVITY_TYPE_CHOICES,
        verbose_name='Trigger Activity Type',
        help_text='Tipo de activity que dispara o workflow'
    )
    
    # Condição: qual resultado deve ter
    trigger_result = models.CharField(
        max_length=20,
        choices=ScheduledActivity.RESULT_CHOICES,
        null=True,
        blank=True,
        verbose_name='Trigger Result',
        help_text='Resultado específico (ou None = qualquer resultado)'
    )
    
    # Condição avançada (JSON) - OPCIONAL, para futuro
    trigger_condition = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Trigger Condition (Advanced)',
        help_text='Condições avançadas em JSON (futuro)'
    )
    
    # Ação: criar qual activity
    next_activity_template = models.ForeignKey(
        'ActivityTemplate',
        on_delete=models.CASCADE,
        related_name='workflows',
        verbose_name='Next Activity Template',
        help_text='Template da próxima activity a criar'
    )
    
    # Delay
    delay_days = models.IntegerField(
        default=0,
        verbose_name='Delay (days)',
        help_text='Dias de espera antes de criar próxima activity'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Active',
        help_text='Desativar para pausar workflow sem deletar'
    )
    
    # Multi-company
    owner_company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activity_workflows',
        verbose_name='Owner Company',
        help_text='NULL=global workflow, with value=private to company'
    )
    
    # Ordem de execução (se houver múltiplos workflows)
    sequence = models.IntegerField(
        default=10,
        verbose_name='Sequence',
        help_text='Ordem de execução (menor = primeiro)'
    )
    ```

  - [x] **Methods:**
    ```python
    def __str__(self):
        result_str = f" ({self.get_trigger_result_display()})" if self.trigger_result else ""
        return f"{self.name} - {self.get_trigger_activity_type_display()}{result_str}"
    
    def should_trigger(self, activity):
        """
        Verifica se este workflow deve disparar para a activity dada.
        
        Args:
            activity: ScheduledActivity instance
        
        Returns:
            bool
        """
        # Check: activity type match
        if activity.activity_type != self.trigger_activity_type:
            return False
        
        # Check: result match (se especificado)
        if self.trigger_result and activity.result != self.trigger_result:
            return False
        
        # Check: model match
        from django.contrib.contenttypes.models import ContentType
        activity_model_ct = activity.content_type
        if activity_model_ct != self.model:
            return False
        
        # Check: is_active
        if not self.is_active:
            return False
        
        # TODO: Check advanced conditions (trigger_condition JSON)
        
        return True
    
    def execute(self, activity, user=None):
        """
        Executa workflow: cria próxima activity baseada no template.
        
        Args:
            activity: ScheduledActivity que disparou o workflow
            user: User que marcou a activity como done (opcional)
        
        Returns:
            ScheduledActivity criada OU None
        """
        from datetime import timedelta
        from django.utils import timezone
        
        # Get content object
        content_object = activity.content_object
        if not content_object:
            return None
        
        # Calcular due_date com delay
        base_date = timezone.now().date()
        due_date = base_date + timedelta(days=self.delay_days)
        
        # Criar activity usando template
        next_activity = self.next_activity_template.create_activity(
            content_object=content_object,
            assigned_to=activity.assigned_to,  # Manter mesmo responsável
            due_date=due_date,
        )
        
        return next_activity
    ```

  - [x] **Meta:**
    ```python
    class Meta:
        ordering = ['sequence', 'name']
        verbose_name = 'Activity Workflow'
        verbose_name_plural = 'Activity Workflows'
    ```

---

### 3.13.4 Migrations ✅

Criar migrations para os novos modelos.

- [x] **Executar migrations**
  - [x] `python manage.py makemigrations core`
  - [x] `python manage.py migrate`
  - [x] Verificar no DB: tabelas `core_scheduledactivity`, `core_activitytemplate`, `core_activityworkflow`

**✅ MELHORIAS IMPLEMENTADAS (além do planejado):**

#### **ActivityTemplate - Campos Extras:**
- [x] `icon` - FontAwesome ou Emoji (ex: 'fa-phone' ou '📞')
- [x] `decoration_type` - Cor visual (warning/danger/success/info)
- [x] `keep_done_activities` - Se False, auto-deleta activities done
- [x] `auto_delete_done_after_days` - Dias antes de deletar
- [x] `action_code` - Código Python para automação avançada

#### **ActivityWorkflow - Campos Extras (estilo Odoo):**
- [x] `base_date_type` - DEADLINE (usar due_date) ou COMPLETION (usar done_date)
- [x] `chaining_mode` - SUGGEST (modal) ou TRIGGER (automático)

#### **Método Extra em ActivityWorkflow:**
- [x] `get_suggested_activity_data()` - Retorna dados para modal de sugestão

**📄 Documentação:** Ver `fuet_magico/activities_comparison.md` para comparação detalhada com Odoo.

---

### 3.13.5 Admin ✅

Registrar modelos no Django Admin.

- [x] **ScheduledActivityAdmin**
  - [x] Criado em `apps/core/admin.py` com:
    - List display com status_badge, content_object_link
    - Filtros por activity_type, is_done, result, due_date, assigned_to
    - Fieldsets organizados
    - Status badge com emoji e cores
    - Content object link com preview

- [x] **ActivityTemplateAdmin**
  - [x] Criado em `apps/core/admin.py` com:
    - List display com icon_preview
    - icon_rendered_preview (48px preview) no detail view
    - Fieldsets organizados (Visual, Behavior, Advanced)
    - Suporte para SVG + cores dinâmicas

- [x] **ActivityWorkflowAdmin**
  - [x] Criado em `apps/core/admin.py` com:
    - List display com trigger_info, next_template_info
    - Chaining mode com emoji (💡 Suggest / ⚡ Trigger)
    - Filtros completos
    - Fieldsets organizados

**✅ IMPLEMENTADO:** Todos os 3 admins com funcionalidades avançadas (badges, icons preview, HTML formatting)

---

### 3.13.6 Signals - Automação de Workflows ✅

Criar signals para disparar workflows automaticamente quando activity é marcada como done.

- [x] **Criar signal post_save para ScheduledActivity**
  - [x] Implementado em `apps/core/signals.py`:
    - Signal `trigger_activity_workflows` em post_save de ScheduledActivity
    - Verifica se activity foi marcada como done (is_done=True)
    - Skip se criada já done (import de dados)
    - Skip se sem resultado definido
    - Busca workflows aplicáveis por content_type e is_active
    - Filtra workflows usando `should_trigger(activity)`
    - Executa workflows com chaining_mode='TRIGGER' automaticamente
    - Loga workflows com chaining_mode='SUGGEST' (modal em 3.13.8)
    - Usa transaction.atomic() para garantir consistência
    - Logging detalhado: info, debug, warning, error com exc_info
    - Conta sucessos (executed_count) e sugestões (suggested_count)

  - [x] **Signal registrado em apps/core/apps.py:**
    - CoreConfig.ready() já importa apps.core.signals
    - Signal ativo automaticamente ao iniciar Django

**Implementação:**
- Sistema de cascata robusto: CALL SUCCESS → EMAIL → TODO
- Suporte para múltiplos workflows por atividade
- Modo TRIGGER (automático) vs SUGGEST (modal)
- Logging completo para debugging
- Error handling com transaction rollback
- Ready para criar automações via Django Admin!

---

### 3.13.7 Forms - Activity Forms ✅

Criar forms para CRUD de activities.

- [x] **ScheduledActivityForm**
  - [x] Implementado em `apps/core/forms.py`
    - ModelForm para criar/editar atividades
    - Campos: activity_type, summary, description, due_date, due_time, assigned_to
    - Widgets customizados com CSS classes e placeholders
    - Filtra assigned_to por company (se fornecida)
    - Validação de campos obrigatórios
    - Labels e help_texts traduzíveis (gettext_lazy)

- [x] **ActivityMarkDoneForm**
  - [x] Implementado em `apps/core/forms.py`
    - ModelForm para marcar atividade como concluída
    - Campos: result (obrigatório), feedback (obrigatório)
    - Validação: feedback mínimo 10 caracteres
    - Override save() para setar is_done=True e done_date
    - Data attribute para JS selector de resultado
    - Labels e help_texts com instruções claras

- [x] **ActivityQuickCreateForm** (BONUS)
  - [x] Implementado em `apps/core/forms.py`
    - Form para criação rápida a partir de templates
    - Campos: template, due_date, due_time, assigned_to, summary_override, description_override
    - Método create_activity() que aplica template + overrides
    - Filtragem por company e activity_type
    - Útil para workflows SUGGEST e quick actions

**Implementação:**
- 3 forms completos com validação robusta
- Suporte a multi-company (filtra users e templates)
- I18n ready (gettext_lazy em todos os textos)
- CSS classes consistentes (form-select, form-input, form-textarea)
- Help texts e placeholders para UX
- Clean methods para validação custom
- Pronto para usar nas Views (Task 3.13.8)!

---

### 3.13.8 Views - CRUD de Activities

Criar views para criar, editar e marcar activities como done.

- [x] **ActivityCreateView (Modal)**
  - [x] Criar em `apps/core/views.py`:
    ```python
    @login_required
    def activity_create_view(request, content_type_id, object_id):
        """
        Criar scheduled activity para qualquer objeto.
        
        URL: /activities/create/<content_type_id>/<object_id>/
        
        Abre como modal HTMX ou página standalone.
        """
        from django.contrib.contenttypes.models import ContentType
        from .forms import ScheduledActivityForm
        
        # Get content object
        try:
            ct = ContentType.objects.get(id=content_type_id)
            model_class = ct.model_class()
            content_object = model_class.objects.get(pk=object_id)
        except Exception as e:
            messages.error(request, f'Object not found: {e}')
            return redirect('dashboard:home')
        
        if request.method == 'POST':
            form = ScheduledActivityForm(request.POST)
            if form.is_valid():
                activity = form.save(commit=False)
                activity.content_type = ct
                activity.object_id = object_id
                activity.owner_company = get_active_company(request)
                activity.save()
                
                messages.success(request, 'Activity criada com sucesso!')
                
                # Se HTMX, retornar partial
                if request.headers.get('HX-Request'):
                    return HttpResponse(
                        '<div class="alert alert-success">Activity criada!</div>',
                        headers={'HX-Trigger': 'activityCreated'}
                    )
                
                # Redirecionar para objeto
                return redirect(content_object.get_absolute_url())
        else:
            # Initial data
            form = ScheduledActivityForm(initial={
                'assigned_to': request.user,
                'due_date': timezone.now().date() + timedelta(days=1)
            })
        
        context = {
            'form': form,
            'content_object': content_object,
            'content_type': ct,
        }
        
        return render(request, 'core/activity_create_modal.html', context)
    ```

- [x] **ActivityMarkDoneView (Modal)**
  - [x] Criar em `apps/core/views.py`:
    ```python
    @login_required
    def activity_mark_done_view(request, activity_id):
        """
        Marcar activity como done com modal para capturar result e feedback.
        
        URL: /activities/<uuid>/mark-done/
        
        Modal mostra:
        - Dropdown de result (SUCCESS, FAILED, etc.)
        - Textarea de feedback
        - Botão "Criar próxima?" (se workflow disponível)
        """
        from .forms import ActivityMarkDoneForm
        
        activity = get_object_or_404(
            ScheduledActivity,
            id=activity_id,
            owner_company=get_active_company(request)
        )
        
        # Buscar workflows aplicáveis
        potential_workflows = ActivityWorkflow.objects.filter(
            model=activity.content_type,
            trigger_activity_type=activity.activity_type,
            is_active=True
        )
        
        if request.method == 'POST':
            form = ActivityMarkDoneForm(request.POST, instance=activity)
            
            if form.is_valid():
                activity = form.save(commit=False)
                activity.is_done = True
                activity.save()  # Dispara signal que cria próxima activity
                
                messages.success(request, 'Activity marcada como concluída!')
                
                # Se HTMX
                if request.headers.get('HX-Request'):
                    return HttpResponse(
                        '<div class="alert alert-success">Done!</div>',
                        headers={'HX-Trigger': 'activityCompleted'}
                    )
                
                return redirect(activity.content_object.get_absolute_url())
        else:
            form = ActivityMarkDoneForm(instance=activity)
        
        context = {
            'form': form,
            'activity': activity,
            'potential_workflows': potential_workflows,
        }
        
        return render(request, 'core/activity_mark_done_modal.html', context)
    ```

- [x] **ActivityListView (Para user ver suas activities)**
  - [x] Criar em `apps/core/views.py`:
    ```python
    @login_required
    def my_activities_view(request):
        """
        Lista de activities do user atual.
        
        URL: /activities/my/
        
        Filtros:
        - Overdue (atrasadas)
        - Today (para hoje)
        - Upcoming (futuras)
        - Done (concluídas)
        """
        from django.db.models import Q
        
        filter_type = request.GET.get('filter', 'pending')
        
        # Base queryset
        activities = ScheduledActivity.objects.filter(
            assigned_to=request.user,
            owner_company=get_active_company(request)
        ).select_related('content_type', 'assigned_to', 'template')
        
        # Apply filters
        today = timezone.now().date()
        
        if filter_type == 'overdue':
            activities = activities.filter(is_done=False, due_date__lt=today)
        elif filter_type == 'today':
            activities = activities.filter(is_done=False, due_date=today)
        elif filter_type == 'upcoming':
            activities = activities.filter(is_done=False, due_date__gt=today)
        elif filter_type == 'done':
            activities = activities.filter(is_done=True)
        else:  # pending (default)
            activities = activities.filter(is_done=False)
        
        # Paginate
        paginator = Paginator(activities, 25)
        page = request.GET.get('page', 1)
        activities_page = paginator.get_page(page)
        
        # Stats
        stats = {
            'overdue': ScheduledActivity.objects.filter(
                assigned_to=request.user,
                is_done=False,
                due_date__lt=today
            ).count(),
            'today': ScheduledActivity.objects.filter(
                assigned_to=request.user,
                is_done=False,
                due_date=today
            ).count(),
            'upcoming': ScheduledActivity.objects.filter(
                assigned_to=request.user,
                is_done=False,
                due_date__gt=today
            ).count(),
        }
        
        context = {
            'activities': activities_page,
            'filter_type': filter_type,
            'stats': stats,
        }
        
        return render(request, 'core/my_activities.html', context)
    ```

---

### 3.13.9 Templates - Activity Modals e Lists

Criar templates para activities.

- [x] **activity_create_modal.html**
  - [x] Criar em `templates/core/activity_create_modal.html`
  - [x] Modal com form para criar activity
  - [x] Campos: activity_type, summary, description, due_date, due_time, assigned_to
  - [x] Botão "Schedule Activity"

- [x] **activity_mark_done_modal.html**
  - [x] Criar em `templates/core/activity_mark_done_modal.html`
  - [x] Modal com form para marcar done
  - [x] Campos: result (dropdown), feedback (textarea)
  - [x] Lista de workflows que serão disparados (preview)
  - [x] Botão "Mark as Done"

- [x] **my_activities.html**
  - [x] Criar em `templates/core/my_activities.html`
  - [x] Tab filters: Overdue, Today, Upcoming, Done
  - [x] Tabela com: icon, summary, related_object, due_date, status
  - [x] Click row abre modal mark_done
  - [x] Stats cards no topo

- [x] **activity_timeline_item.html (Componente para Chatter)**
  - [x] Criar em `templates/components/activity_timeline_item.html`
  - [x] Renderizar activity na timeline do chatter
  - [x] Mostrar: icon, summary, due_date, assigned_to, status
  - [x] Botão "Mark Done" (se pending)
  - [x] Badge de status (overdue/today/upcoming)

---

### 3.13.10 URLs

Configurar rotas para activities.

- [x] **Adicionar em config/urls.py:**
  ```python
  # Activities
  path('activities/create/<int:content_type_id>/<uuid:object_id>/', 
       activity_create_view, name='activity_create'),
  path('activities/<uuid:activity_id>/mark-done/', 
       activity_mark_done_view, name='activity_mark_done'),
  path('activities/my/', 
       my_activities_view, name='my_activities'),
  ```

---

### 3.13.11 Integração com Chatter

Atualizar componente Chatter para mostrar ScheduledActivities na timeline.

- [x] **Atualizar ChatterMixin em core/views.py**
  - [x] Adicionar ao context:
    ```python
    # Scheduled activities (pending)
    scheduled_activities = ScheduledActivity.objects.filter(
        content_type=ct,
        object_id=obj.pk,
        is_done=False
    ).order_by('due_date', 'due_time')
    
    context['scheduled_activities'] = scheduled_activities
    ```

- [x] **Atualizar templates/components/chatter.html**
  - [x] Adicionar seção "Scheduled Activities" antes da timeline
  - [x] Renderizar cada activity com componente `activity_timeline_item.html`
  - [x] Botão "Schedule Activity" que abre modal

---

### 3.13.12 Data Fixtures - Criar Templates e Workflows Padrão

Criar templates e workflows iniciais via fixtures ou management command.

- [x] **Criar management command: setup_default_workflows.py**
  - [x] Criar em `apps/core/management/commands/setup_default_workflows.py`
  - [x] **Templates padrão:**
    ```python
    templates = [
        {
            'name': 'Follow-up Call',
            'activity_type': 'CALL',
            'default_summary': 'Follow-up call with {{contact_name}}',
            'due_days_offset': 3,
        },
        {
            'name': 'Send Info Email',
            'activity_type': 'EMAIL',
            'default_summary': 'Send product information to {{contact_name}}',
            'due_days_offset': 1,
        },
        {
            'name': 'Prepare Quote',
            'activity_type': 'TODO',
            'default_summary': 'Prepare quote for {{contact_name}}',
            'due_days_offset': 1,
        },
        {
            'name': 'Schedule Meeting',
            'activity_type': 'MEETING',
            'default_summary': 'Meeting with {{contact_name}}',
            'due_days_offset': 2,
        },
    ]
    ```
  - [x] **Workflows padrão para Lead:**
    ```python
    # ContentType para Lead
    lead_ct = ContentType.objects.get(app_label='crm', model='lead')
    
    workflows = [
        {
            'name': 'Lead Nurturing - First Contact Success',
            'model': lead_ct,
            'trigger_activity_type': 'CALL',
            'trigger_result': 'SUCCESS',
            'next_activity_template': templates['Send Info Email'],
            'delay_days': 1,
        },
        {
            'name': 'Lead Nurturing - Info Sent',
            'model': lead_ct,
            'trigger_activity_type': 'EMAIL',
            'trigger_result': 'SUCCESS',
            'next_activity_template': templates['Follow-up Call'],
            'delay_days': 3,
        },
    ]
    ```
  - [x] Executar: `python manage.py setup_default_workflows`

---

### 3.13.13 Testing - Activities System

Testes para activities genéricas.

- [x] **Test: ScheduledActivity model**
  - [x] Test: criar activity funciona
  - [x] Test: is_overdue funciona
  - [x] Test: status_color retorna cor correta
  - [x] Test: GenericForeignKey funciona com Lead, Sale, etc.

- [x] **Test: ActivityTemplate**
  - [x] Test: create_activity() funciona
  - [x] Test: due_days_offset é aplicado
  - [x] Test: variáveis em summary são substituídas (futuro)

- [x] **Test: ActivityWorkflow**
  - [x] Test: should_trigger() funciona
  - [x] Test: execute() cria próxima activity
  - [x] Test: workflows são disparados via signal

- [x] **Test: Workflow automation**
  - [x] Test: marcar CALL como SUCCESS cria EMAIL
  - [x] Test: delay_days é respeitado
  - [x] Test: múltiplos workflows executam em ordem

- [x] **Test: Views**
  - [x] Test: activity_create_view funciona
  - [x] Test: activity_mark_done_view funciona
  - [x] Test: my_activities_view mostra activities do user

---

## 3.12.13 Testing Completo (Menções + Notificações)

Testar todo o sistema de menções e notificações.

- [x] **Testes de Menções**
  - [x] Test: criar nota com @joao
  - [x] Test: mentioned_users contém user correto
  - [x] Test: parse extrai múltiplos @mentions
  - [x] Test: autocomplete funciona

- [x] **Testes de Notificações**
  - [x] Test: notificação criada quando mencionado
  - [x] Test: badge mostra contador correto
  - [x] Test: clicar marca como lida
  - [x] Test: "Marcar todas" funciona
  - [x] Test: não cria notificação para autor

- [x] **Teste de Integração**
  - [x] Test: João menciona Maria em nota
  - [x] Test: Maria recebe notificação
  - [x] Test: Badge de Maria atualiza
  - [x] Test: Maria clica e vê notificação
  - [x] Test: Maria marca como lida
  - [x] Test: Badge decrementa

---

# 🚀 FASE 4: APP - CONTACTOS

**⏱ Tempo estimado:** 6-7 dias
**🎯 Objetivo:** Criar sistema completo de gestão de contactos com integração a Vendas, Compras, Contabilidade e Marketing
**📦 Dependências:** Fase 3 (base models e autenticação)
**📝 Nota:** Secções 4.10-4.13 dependem de outras fases estarem implementadas (Vendas, Compras, Financeiro, Marketing)

---

## 4.1 Criação da App 'contacts'

Criar app Django para gestão de contactos.

- [x] **Criar app**
  - [x] Executar `python manage.py startapp contacts apps/contacts`
  - [x] Adicionar 'apps.contacts' ao INSTALLED_APPS

- [x] **Criar estrutura de arquivos**
  - [x] Criar `apps/contacts/models.py`
  - [x] Criar `apps/contacts/views.py`
  - [x] Criar `apps/contacts/forms.py`
  - [x] Criar `apps/contacts/urls.py`

---

## 4.2 Modelo Contact

Criar modelo para clientes/contactos com hierarquia (empresas e pessoas).

- [x] **Criar modelo Contact**
  - [x] Herdar de BaseModel
  - [x] Campos básicos: name, email, phone, whatsapp, address, city, district, postal_code, country, website, language, nif, notes
  - [x] ~~Campo: contact_type (CLIENT, SUPPLIER, BOTH)~~ — **REMOVIDO** (redundante com contact_category)
  - [x] Campo: contact_category (PERSON, COMPANY, BILLING, SHIPPING, OTHER)
  - [x] Campo: company (ForeignKey para Contact, null=True) - associar pessoa a empresa
  - [x] Campo: position (cargo da pessoa na empresa, opcional)
  - [x] Campo: tags (ManyToManyField para ContactTag)
  - [x] Campo: associated_contacts (ManyToManyField para self, symmetrical=True)
  - [x] Campo: owner_company (ForeignKey para Company, multi-company support)
  - [x] Método __str__
  - [x] Método get_avatar_url() - retorna SVG default baseado em contact_category
  - [x] Método get_price_list() - retorna price list própria ou herdada da empresa
  - [x] Property is_company e is_person para facilitar queries

- [x] **Validações e constraints**
  - [x] Validar: contacto não pode associar-se a si próprio
  - [x] Constraint: email único (mas pode ser null)

- [x] **Criar migrations**
  - [x] Executar makemigrations
  - [x] Executar migrate

- [x] **Registrar no Admin**
  - [x] Criar ContactAdmin
  - [x] Configurar list_display: name, contact_category, company, email, phone, is_active
  - [x] Configurar search_fields: name, email, phone, nif
  - [x] Configurar list_filter: contact_category, is_active
  - [x] Adicionar EmployeeInline para mostrar pessoas associadas (quando é empresa)
  - [x] Fieldsets separados para organizar campos

- [x] **Testing - Contact Model**
  - [x] Test: criar empresa (COMPANY) funciona
  - [x] Test: criar pessoa (PERSON) sem empresa funciona
  - [x] Test: criar pessoa (PERSON) associada a empresa funciona
  - [x] Test: não permite associar pessoa a outra pessoa
  - [x] Test: não permite empresa ter company preenchido
  - [x] Test: herança de price list funciona (quando implementado)

---

## 4.3 Views de Listagem de Contactos

Criar view para listar todos os contactos com sistema de bulk actions, filtros avançados e paginação customizável.

- [x] **Criar ContactListView**
  - [x] Criar view em `apps/contacts/views.py`
  - [x] Implementar paginação customizável (50 por página padrão, editável sem persistência)
  - [x] Implementar busca por múltiplos campos (name/email/phone/whatsapp/nif/city/company/position)
  - [x] Implementar filtro por status (active/archived) com padrão em 'active'
  - [x] URL RESTful com parâmetros: ?status=active&page_size=50&page=1&search=query&field=name

- [x] **Criar template**
  - [x] Criar `templates/contacts/list.html` (standalone)
  - [x] Tabela responsiva com: checkbox, avatar, name, email, phone, whatsapp, contact_type, actions
  - [x] Barra de busca com dropdown integrado (estilo Odoo) - chevron no input
  - [x] Filtro de status integrado no dropdown de busca (Ativos/Arquivados)
  - [x] Filtro de campos de busca no mesmo dropdown (Name, Email, Phone, WhatsApp, NIF, City, Company, Position)
  - [x] Dropdown abre automaticamente ao digitar OU ao clicar no chevron
  - [x] Botão "Novo Contacto" (desktop e mobile)
  - [x] Sistema de seleção múltipla com checkboxes (Alpine.js)
  - [x] Bulk actions toolbar inline com botão "Novo" (desktop)
  - [x] Bulk actions mobile com gear icon e badge de contagem
  - [x] Controle de page_size editável (input de texto, valida 1-total, reseta em F5)
  - [x] View toggle buttons (List/Kanban) - visual apenas, funcionalidade futura
  - [x] Dark mode completo em toda interface

- [x] **Configurar rota**
  - [x] Adicionar `path('contacts/', ContactListView, name='contact_list')`
  - [x] Incluir urls no config/urls.py

- [x] **Implementar Bulk Actions - Arquivar**
  - [x] Criar endpoint POST `/contacts/bulk-archive/`
  - [x] Receber lista de IDs via JSON
  - [x] Validar que todos os IDs pertencem ao user/company (permission check)
  - [x] Atualizar `is_active=False` para todos os IDs
  - [x] Retornar JSON com sucesso e contagem de contactos arquivados
  - [x] Adicionar mensagem de feedback no frontend
  - [x] Handler JavaScript para chamar endpoint e atualizar UI
  - [x] Validação de contactos já arquivados com mensagem de erro apropriada
  - [x] Sistema de notificações toast para feedback visual

- [x] **Implementar Bulk Actions - Desarquivar**
  - [x] Criar endpoint POST `/contacts/bulk-unarchive/`
  - [x] Receber lista de IDs via JSON
  - [x] Validar permissions
  - [x] Atualizar `is_active=True` para todos os IDs
  - [x] Retornar JSON com sucesso e contagem
  - [x] Adicionar mensagem de feedback no frontend
  - [x] Handler JavaScript para chamar endpoint e atualizar UI

- [ ] **Implementar Bulk Actions - Merge (Fundir Contactos)**
  - **NOTA:** Aguarda criação das tabelas de vendas/compras para implementar atualização de FKs
  - [ ] **Backend - Endpoints**
    - [ ] Criar endpoint GET `/contacts/merge-preview/?id1=X&id2=Y`
    - [ ] Criar endpoint POST `/contacts/bulk-merge/`
  - [ ] **Backend - Service Layer**
    - [ ] Criar `ContactService.get_merge_preview(id1, id2)`
      - [ ] Retornar dados dos 2 contactos formatados lado-a-lado
      - [ ] Retornar todos os campos (name, email, phone, address, etc.)
    - [ ] Criar `ContactService.execute_merge(id1, id2, selected_fields)`
      - [ ] Criar novo contacto com campos selecionados pelo user
      - [ ] Buscar todas as tabelas com FK para Contact (usar Django ORM)
      - [ ] Atualizar todas as FKs de id1 e id2 para novo contacto ID
      - [ ] Apagar contactos id1 e id2
      - [ ] Usar `transaction.atomic()` para rollback se falhar
  - [ ] **Backend - Validações**
    - [ ] Validar exatamente 2 contactos selecionados
    - [ ] Validar contactos existem
    - [ ] Validar não pode merge consigo próprio
    - [ ] Validar user tem permissão (@login_required)
    - [ ] Retornar erros em português
  - [ ] **Frontend - Modal Wizard (3 colunas)**
    - [ ] Criar modal em `templates/contacts/list.html` ou componente separado
    - [ ] Coluna esquerda: Contacto A (todos os campos)
    - [ ] Coluna central: Contacto B (todos os campos)
    - [ ] Coluna direita: Contacto Final (resultado)
  - [ ] **Frontend - Lógica de Seleção**
    - [ ] Gerar SELECT dropdown para cada campo do Contacto Final
    - [ ] Opções do SELECT: valor de A ou valor de B
    - [ ] Implementar auto-preenchimento inteligente:
      - [ ] Se A tem valor e B está vazio → selecionar A automaticamente
      - [ ] Se B tem valor e A está vazio → selecionar B automaticamente
      - [ ] Se ambos têm valor → deixar em branco para user escolher
    - [ ] Permitir user alterar qualquer seleção manualmente
  - [ ] **Frontend - Confirmação e Execução**
    - [ ] Botão "Executar Merge" que valida se todos campos foram selecionados
    - [ ] Modal de confirmação secundário: "Esta ação é irreversível. Aceitar?"
    - [ ] Enviar POST para `/contacts/bulk-merge/` com `{id1, id2, selected_fields}`
    - [ ] Notificação toast com sucesso/erro em português
    - [ ] Reload automático após merge bem-sucedido
  - [ ] **Frontend - Handler JavaScript**
    - [ ] Atualizar `mergeSelected()` para abrir modal wizard
    - [ ] Carregar dados via fetch para `/contacts/merge-preview/`
    - [ ] Gerenciar estado dos SELECTs (Alpine.js ou vanilla JS)

- [x] **Implementar Sistema de Detecção de Duplicados com Scoring**
  - **OBJETIVO:** Detectar contactos duplicados usando sistema de pontuação inteligente
  - **CONTEXTO:** User seleciona 1 contacto e sistema compara com todos outros para encontrar possíveis duplicados
  - **SCORING MÁXIMO:** 71 pontos (campos não-UNIQUE apenas)
  - **THRESHOLD:** Só mostrar se score ≥ 8 pontos
  - **LIMITE:** Top 20 resultados ordenados por score DESC
  
  - [x] **Backend - Endpoint**
    - [x] Criar `POST /contacts/find-duplicates/`
    - [x] Receber `{"contact_id": 123}`
    - [x] Validar contacto existe e user tem permissão
    - [x] Retornar JSON com original + lista de duplicates
    - [x] Cada duplicate tem: contact data, score, matched_fields, details
    
  - [x] **Backend - Service Layer**
    - [x] Criar `ContactService.find_potential_duplicates(contact_id)`
      - [x] Fetch contacto original
      - [x] Fetch todos outros contactos ativos (excluir próprio)
      - [x] Para cada contacto calcular score com `_calculate_similarity_score()`
      - [x] Filtrar apenas score ≥ 8
      - [x] Ordenar por score DESC
      - [x] Limitar top 20 resultados
    - [x] Criar `ContactService._calculate_similarity_score(original, candidate)`
      - [x] **NIF:** 15 pontos se igual (não-UNIQUE)
      - [x] **Phone:** 12 pontos se igual após normalização
      - [x] **WhatsApp:** 10 pontos se igual após normalização
      - [x] **Nome:** 10 pts (exato), 7 pts (invertido), 5 pts (parcial 2+ palavras), 1 pt (1 palavra comum)
      - [x] **Company ID:** 10 pontos se igual
      - [x] **Address:** 5 pontos se igual
      - [x] **Postal Code:** 4 pontos se igual
      - [x] **City:** 3 pontos se igual
      - [x] **Position:** 2 pontos se igual, 1 pt se similar
      - [x] **EXCLUIR Email** (campo é UNIQUE na BD, nunca duplica)
      - [x] Retornar: score total, matched_fields[], details{}
    - [x] Criar `ContactService._compare_names(name1, name2)`
      - [x] Exatamente igual (case-insensitive) → 10 pontos
      - [x] Palavras invertidas (set igual) → 7 pontos
      - [x] 2+ palavras comuns → 5 pontos
      - [x] 1 palavra comum → 1 ponto
      - [x] Usar `difflib.SequenceMatcher` se ratio > 0.8 → 4 pontos
    - [x] Criar `ContactService._normalize_phone(phone)`
      - [x] Remover espaços, traços, parênteses: `r'[\s\-\(\)]'`
      - [x] Comparar strings normalizadas
      
  - [x] **Frontend - UI Button**
    - [x] Adicionar botão "Qualidade da Base de Dados"
    - [x] Validar exatamente 1 contacto selecionado
    - [x] Ícone check circle
    
  - [x] **Frontend - Handler JavaScript**
    - [x] Criar `checkDataQuality()` function
    - [x] Validar 1 contacto selecionado
    - [x] Fetch POST `/contacts/find-duplicates/` com contact_id
    - [x] Se 0 duplicados → toast "Nenhum duplicado encontrado"
    - [x] Se > 0 duplicados → abrir modal
    - [x] Loading spinner enquanto processa
    
  - [x] **Frontend - Modal de Duplicados**
    - [x] Modal header com nome do contacto original
    - [x] Lista de duplicados (top 20 máximo)
    - [x] Formato tabela com checkboxes para multi-select
    - [x] Para cada duplicate mostrar:
      - [x] **Checkbox** para seleção individual
      - [x] **Score badge** com cor gradiente (ver sistema de cores abaixo)
      - [x] Nome do contacto com avatar
      - [x] Ícone info com dropdown de campos matched (hover desktop / click mobile)
      - [x] Detalhes expandíveis com valores e pontos
    - [x] Footer com contador de selecionados
    - [x] Botão dourado "Fazer Merge" (#d4a855) habilitado quando ≥1 selecionado
    - [ ] **Lógica do Merge Button** (implementar quando função merge estiver pronta)
      - [ ] Abrir wizard de merge com 3 colunas (Contato A, Contato B, Final)
      - [ ] Permitir escolher valores de cada campo
      - [ ] Confirmação antes de executar merge irreversível
      - [ ] Atualizar foreign keys em tabelas relacionadas (vendas/compras)
      - [ ] Eliminar contatos originais após merge bem-sucedido
    
  - [x] **Frontend - Sistema de Cores Gradiente**
    - [x] **Fórmula:** `percentage = (score / 71) * 100`
    - [x] **Gradiente HSL:** `hsl(hue, 80%, 50%)` onde `hue = (percentage / 100) * 120`
    - [x] 0-20%: 🔴 Vermelho escuro (hue 0-24°)
    - [x] 20-40%: 🟠 Laranja (hue 24-48°)
    - [x] 40-60%: 🟡 Amarelo (hue 48-72°)
    - [x] 60-80%: 🟢 Verde claro (hue 72-96°)
    - [x] 80-100%: 💚 Verde forte (hue 96-120°)
    - [x] Implementar função `getScoreColor(score)` em JavaScript
    - [x] Badge de cada resultado tem background dinâmico
    
  - [ ] **Extras (Opcional)**
    - [ ] Usar biblioteca `fuzzywuzzy` para comparação avançada de nomes
    - [ ] Cache de resultados para evitar recalcular
    - [ ] Exportar relatório de duplicados (CSV/PDF)
    - [ ] Bulk action: "Verificar duplicados de todos selecionados"

- [x] **Implementar Bulk Actions - Eliminar (ADMIN ONLY)**
  - [x] Criar endpoint POST `/contacts/bulk-delete/`
  - [x] Decorator `@admin_required` ou verificar `request.user.is_staff`
  - [x] Validar permissions (apenas admins podem eliminar)
  - [x] Verificar se contactos têm relacionamentos (vendas, compras)
  - [x] Modal de confirmação com warning sobre dados relacionados
  - [x] Soft delete preferível (manter is_active=False) OU hard delete se confirmado
  - [x] Retornar JSON com sucesso e contagem
  - [x] Mostrar botão "Eliminar" apenas para admins no frontend
  - [x] Handler JavaScript com double confirmation

- [x] **Testing - Contact List**
  - [x] Test: acessar /contacts/ mostra apenas contactos ativos por padrão
  - [x] Test: busca por cada campo funciona (name, email, phone, whatsapp, nif, city, company, position)
  - [x] Test: filtro status=archived mostra apenas arquivados
  - [x] Test: paginação funciona com page_size customizável
  - [x] Test: page_size reseta para 50 em F5
  - [x] Test: bulk archive funciona com múltiplos IDs
  - [x] Test: bulk unarchive funciona
  - [ ] Test: bulk merge valida mínimo 2 contactos (merge wizard pendente)
  - [x] Test: database quality identifica duplicados
  - [x] Test: bulk delete apenas para admins
  - [x] Test: non-admin não vê botão eliminar
  - [x] Test: dropdown abre ao digitar e ao clicar no chevron

---

## 4.4 Views de Criação de Contacto

Template : https://v0-contact-form-creation-seven.vercel.app/
Criar view para adicionar novo contacto.

- [x] **Criar ContactCreateView**
  - [x] Criar view para criar contacto (`contact_create_view`)

- [x] **Criar form**
  - [x] Criar ContactForm em forms.py (campos: contact_category, name, email, phone, whatsapp, nif, address, city, district, postal_code, country, website, language, company, position, notes)

- [x] **Criar template**
  - [x] Criar `templates/contacts/create.html` (standalone, reutilizado para create e edit)
  - [x] Formulário com todos os campos
  - [x] Avatar dinâmico baseado em contact_category
  - [x] Seletor de tags interativo (Alpine.js) com pesquisa, criação rápida, modal de todas as tags
  - [x] Tabs: Contactos, Vendas, Compras, Contabilidade, Notas (Quill editor), Marketing
  - [x] Tab Contactos: gestão de contactos associados (M2M) com modal criar/associar existente
  - [x] Tab Notas: editor Quill rich text com dark theme

- [x] **Configurar rota**
  - [x] Adicionar `path('contacts/new/', contact_create_view, name='contact_create')`

- [x] **Testing - Contact Create**
  - [x] Test: criar contacto funciona
  - [x] Test: validações funcionam
  - [x] Test: redirecionamento após criação

---

## 4.5 Views de Edição e Detalhes

Criar views para editar e visualizar contacto.

> **📝 Nota:** Não existe view de detalhe separada — o formulário de edição (`create.html`) serve como detalhe e edição ao mesmo tempo, com deteção de alterações via JavaScript (botões Guardar/Descartar aparecem apenas quando há mudanças).

- [x] **Criar ContactEditView (Detail + Edit combinados)**
  - [x] Mostrar todas as informações do contacto no formulário pré-preenchido
  - [x] Deteção de alterações via MutationObserver + input/change events
  - [x] Botões Guardar/Descartar escondidos por defeito, aparecem apenas quando há alterações
  - [x] Tags pré-carregadas do contacto
  - [x] Avatar dinâmico baseado em contact_category

- [x] **Template reutilizado**
  - [x] `templates/contacts/create.html` — variável `contact` no contexto distingue create vs edit

- [x] **Configurar rota**
  - [x] `path('contacts/<uuid:contact_id>/edit/', contact_edit_view, name='contact_edit')`

- [x] **Testing - Contact Edit**
  - [x] Test: editar contacto funciona
  - [x] Test: deteção de alterações funciona
  - [x] Test: tags são pré-carregadas no edit

---

## 4.6 Soft Delete de Contactos

Implementar soft delete (is_active=False) em vez de deletar.

> **📝 Nota:** Implementado via bulk actions na lista de contactos (não como view individual). Arquivar = soft delete (is_active=False), Eliminar = hard delete (admin only).

- [x] **Soft delete via Bulk Archive**
  - [x] Endpoint `POST /contacts/bulk-archive/` — marca is_active=False
  - [x] Endpoint `POST /contacts/bulk-unarchive/` — restaura is_active=True
  - [x] Confirmação via JavaScript antes de executar

- [x] **Hard delete (Admin Only)**
  - [x] Endpoint `POST /contacts/bulk-delete/` — elimina permanentemente
  - [x] Apenas acessível a administradores
  - [x] Modal de confirmação com double check

- [x] **Queryset filtrado**
  - [x] Filtrar is_active=True por padrão nas views
  - [x] Toggle Ativos/Arquivados na lista

- [x] **Testing - Contact Delete**
  - [x] Test: soft delete (archive) funciona
  - [x] Test: contacto não aparece mais na lista de ativos
  - [x] Test: contacto aparece na lista de arquivados
  - [x] Test: hard delete apenas para admins

---

## 4.7 Importação de Contactos (CSV)

Permitir importar contactos via CSV.

- [ ] **Criar ContactImportView**
  - [ ] Upload de arquivo CSV
  - [ ] Validar estrutura do CSV
  - [ ] Criar contactos em batch

- [ ] **Criar template**
  - [ ] `templates/contacts/import.html` (standalone)
  - [ ] Upload form
  - [ ] Instruções de formato

- [ ] **Configurar rota**
  - [ ] `path('contacts/import/', ContactImportView, name='contact_import')`

- [ ] **Testing - Contact Import**
  - [ ] Test: importar CSV válido funciona
  - [ ] Test: CSV inválido mostra erros
  - [ ] Test: duplicados são tratados

---

## 4.8 Exportação de Contactos (CSV/Excel)

Permitir exportar contactos.

- [ ] **Criar ContactExportView**
  - [ ] Gerar CSV com todos os contactos
  - [ ] Respeitar filtros aplicados

- [ ] **Adicionar botão no template list**
  - [ ] Botão "Exportar" na lista

- [ ] **Configurar rota**
  - [ ] `path('contacts/export/', ContactExportView, name='contact_export')`

- [ ] **Testing - Contact Export**
  - [ ] Test: exportar CSV funciona
  - [ ] Test: CSV contém todos os dados
  - [ ] Test: filtros são aplicados na exportação

---

## 4.9 Gestão de Contact Tags

Criar sistema completo de gestão de tags de contactos com CRUD completo.

- [x] **Criar modelo ContactTag**
  - [x] Criar em `apps/contacts/models.py`
  - [x] Herdar de AbstractBaseModel
  - [x] Campo: name (max 50 chars, unique, obrigatório)
  - [x] Campo: color (max 7 chars, default '#dbc693', opcional)
  - [x] Relação: Contact.tags (ManyToManyField para ContactTag)
  - [x] Método __str__ retorna name

- [x] **Criar migrations**
  - [x] Executar makemigrations contacts
  - [x] Converter tags de JSONField para ManyToManyField
  - [x] Executar migrate

- [x] **Registrar no Admin**
  - [x] Criar ContactTagAdmin em admin.py
  - [x] list_display: name, color, contact_count, is_active, created_at
  - [x] search_fields: name
  - [x] list_filter: is_active, created_at
  - [x] Método contact_count() para mostrar quantos contactos usam a tag

- [x] **Criar ContactTagListView**
  - [x] View para listar todas as tags (`tag_list_view`)
  - [x] Implementar paginação (50 por página)
  - [x] Implementar busca por nome
  - [x] Mostrar contador de contactos por tag
  - [x] Filtro: active/archived

- [x] **Criar template list**
  - [x] Criar `templates/contacts/tag_list.html`
  - [x] Tabela: checkbox, color badge, nome, contact count, actions
  - [x] Barra de busca
  - [x] Botão "Nova Tag"
  - [x] Bulk actions: Arquivar, Desarquivar, Eliminar (admin only)

- [x] **Configurar rota list**
  - [x] `path('contacts/tags/', tag_list_view, name='tag_list')`

- [x] **Criar ContactTagCreateView**
  - [x] Form com campos: name (obrigatório), color (seletor de cor)
  - [x] Validação: nome único
  - [x] Redirect para tag_list após criar

- [x] **Criar ContactTagForm**
  - [x] Campo name: TextInput com placeholder
  - [x] Campo color: ColorInput (type="color") com default '#dbc693'
  - [x] Validação customizada para formato hex color

- [x] **Criar template create/edit**
  - [x] Criar `templates/contacts/tag_form.html` (reutilizado para create e edit via `is_edit`)
  - [x] Layout standalone
  - [x] Preview da tag com cor selecionada
  - [x] Botões: Guardar, Cancelar

- [x] **Configurar rota create**
  - [x] `path('contacts/tags/new/', tag_create_view, name='tag_create')`

- [x] **Criar ContactTagUpdateView**
  - [x] Formulário pré-preenchido (`tag_edit_view`)
  - [x] Validações (nome único exceto próprio)
  - [x] Redirect para tag_list após editar

- [x] **Configurar rota update**
  - [x] `path('contacts/tags/<uuid:pk>/edit/', tag_edit_view, name='tag_edit')`

- [x] **Bulk actions para tags (substitui delete individual)**
  - [x] Bulk archive (soft delete is_active=False)
  - [x] Bulk unarchive
  - [x] Bulk delete (admin only, hard delete)
  - [x] Aviso no modal de delete quando tags têm contactos associados (check_tags_contacts API)

- [x] **Adicionar tags ao ContactForm**
  - [x] Seletor interativo Alpine.js: pesquisa, criação rápida, modal de todas as tags
  - [x] Tags pré-carregadas no modo de edição
  - [x] Hidden inputs enviados no form submit
  - [x] API endpoints: `search_tags_api`, `quick_create_tag_api`

- [x] **Atualizar Contact List para mostrar tags**
  - [x] Coluna tags na tabela (badges coloridos, max 4 por contacto)
  - [x] Tags também visíveis nos cards Kanban
  - [~] ~~Filtro por tag (dropdown multi-select)~~ — Decidido não implementar
  - [~] ~~Click na tag filtra lista por essa tag~~ — Decidido não implementar

- [x] **Tags visíveis no Contact Edit/Detail**
  - [x] Mostrar tags com cor no seletor interativo
  - [x] Permitir adicionar/remover tags inline

- [x] **Testing - Contact Tags**
  - [x] Test: criar tag funciona
  - [x] Test: nome único é validado
  - [x] Test: adicionar tag a contacto funciona
  - [x] Test: soft delete (archive) funciona
  - [x] Test: color picker funciona
  - [x] Test: tag com contactos mostra aviso ao deletar (via check_tags_contacts API + modal warning)

---

## 4.10 Tab "Vendas" no Detalhe de Contacto

Implementar conteúdo da tab "Vendas" (Sales) no formulário de contacto após a aplicação de Vendas (Fase 8) estar criada.

> **⚠️ BLOQUEADO:** Depende da Fase 8 (App: Vendas) estar implementada.
> **📍 Localização:** `templates/contacts/create.html` (linha ~355 - tab "vendas")

- [ ] **Após Fase 8 estar completa - Adicionar listagem de encomendas**
  - [ ] Query: `SaleOrder.objects.filter(contact=contact)` (ordenado por data desc)
  - [ ] Mostrar tabela com: número encomenda, data, estado, valor total, ações
  - [ ] Link para cada encomenda (redirect para detalhe de venda)
  - [ ] Mostrar estatísticas resumidas:
    - [ ] Total de encomendas
    - [ ] Valor total faturado
    - [ ] Última encomenda (data)
    - [ ] Produto mais comprado

- [ ] **Botão "Nova Encomenda"**
  - [ ] Criar botão "Nova Encomenda" (estilo golden)
  - [ ] Ao clicar: redirect para `/sales/orders/new/?contact=<uuid>` (pre-fill contacto)
  - [ ] Apenas visível se contacto já estiver guardado (contact.pk exists)

- [ ] **Empty State**
  - [ ] Se não houver encomendas: mostrar SVG + mensagem "Sem encomendas registadas"
  - [ ] Call-to-action: "Criar primeira encomenda"

- [ ] **Design**
  - [ ] Manter padrão dark mode (#1f2937)
  - [ ] Badges coloridos para estados: DRAFT (gray), CONFIRMED (blue), INVOICED (green), CANCELLED (red)
  - [ ] Tabela responsiva com scroll horizontal em mobile

---

## 4.11 Tab "Compras" no Detalhe de Contacto

Implementar conteúdo da tab "Compras" (Purchases) no formulário de contacto após a aplicação de Compras (Fase 7) estar criada.

> **⚠️ BLOQUEADO:** Depende da Fase 7 (App: Compras) estar implementada.
> **📍 Localização:** `templates/contacts/create.html` (linha ~365 - tab "compras")

- [ ] **Após Fase 7 estar completa - Adicionar listagem de encomendas de compra**
  - [ ] Query: `PurchaseOrder.objects.filter(supplier=contact)` (apenas se contact.contact_type = 'SUPPLIER' ou 'BOTH')
  - [ ] Mostrar tabela com: número, data, estado, valor total, ações
  - [ ] Link para cada encomenda de compra
  - [ ] Mostrar estatísticas resumidas:
    - [ ] Total de encomendas de compra
    - [ ] Valor total pago
    - [ ] Última compra (data)
    - [ ] Produto mais fornecido

- [ ] **Botão "Nova Encomenda de Compra"**
  - [ ] Criar botão "Nova Compra" (estilo golden)
  - [ ] Ao clicar: redirect para `/purchases/orders/new/?supplier=<uuid>` (pre-fill fornecedor)
  - [ ] Apenas visível se contacto for SUPPLIER ou BOTH
  - [ ] Desabilitado se contacto não estiver guardado

- [ ] **Empty State**
  - [ ] Se contact_type != SUPPLIER/BOTH: mensagem "Este contacto não é um fornecedor"
  - [ ] Se não houver compras: SVG + mensagem "Sem compras registadas"

- [ ] **Design**
  - [ ] Badges: DRAFT (gray), ORDERED (blue), RECEIVED (green), CANCELLED (red)
  - [ ] Highlight para compras em atraso (expected_date < hoje e estado != RECEIVED)

---

## 4.12 Tab "Contabilidade" no Detalhe de Contacto

Implementar conteúdo da tab "Contabilidade" (Accounting/Invoices) no formulário de contacto após a aplicação Financeiro (Fase 9) estar criada.

> **⚠️ BLOQUEADO:** Depende da Fase 9 (App: Financeiro) estar implementada.
> **📍 Localização:** `templates/contacts/create.html` (linha ~375 - tab "contabilidade")

- [ ] **Após Fase 9 estar completa - Adicionar listagem de faturas**
  - [ ] Query: `Invoice.objects.filter(contact=contact)` (ordenado por data desc)
  - [ ] Mostrar tabela com: número fatura, data, tipo (cliente/fornecedor), estado, valor, ações
  - [ ] Link para visualizar PDF da fatura
  - [ ] Mostrar estatísticas financeiras:
    - [ ] Total faturado (soma de faturas de cliente)
    - [ ] Total faturado por fornecedor (se aplicável)
    - [ ] Saldo devedor (faturas UNPAID)
    - [ ] Média de dias para pagamento

- [ ] **Botão "Nova Fatura"**
  - [ ] Criar botão "Nova Fatura" (estilo golden)
  - [ ] Ao clicar: abrir modal para escolher tipo (Cliente/Fornecedor)
  - [ ] Redirect para `/invoices/new/?contact=<uuid>&type=<cliente|fornecedor>`

- [ ] **Alertas de Pagamento**
  - [ ] Highlight (vermelho) para faturas vencidas (due_date < hoje e estado = UNPAID)
  - [ ] Badge amarelo para faturas a vencer nos próximos 7 dias
  - [ ] Badge verde para faturas PAID

- [ ] **Gráfico de Fluxo de Caixa** (opcional)
  - [ ] Chart.js ou similar
  - [ ] Linha temporal com faturação vs pagamentos
  - [ ] Período: últimos 12 meses

- [ ] **Empty State**
  - [ ] SVG + "Sem faturas registadas para este contacto"

---

## 4.13 Tab "Marketing" no Detalhe de Contacto

Implementar conteúdo da tab "Marketing" (Campaigns) no formulário de contacto após a aplicação de Marketing (Fase 12) estar criada.

> **⚠️ BLOQUEADO:** Depende da Fase 12 (App: Marketing e WhatsApp) estar implementada.
> **📍 Localização:** `templates/contacts/create.html` (linha ~405 - tab "marketing")

- [ ] **Após Fase 12 estar completa - Adicionar histórico de campanhas**
  - [ ] Query: `CampaignContact.objects.filter(contact=contact)` (relação many-to-many com Campaign)
  - [ ] Mostrar tabela com: nome campanha, tipo (EMAIL/WHATSAPP/SMS), data envio, estado (SENT/OPENED/CLICKED), ações
  - [ ] Link para detalhe da campanha
  - [ ] Estatísticas de engagement:
    - [ ] Total de mensagens recebidas
    - [ ] Taxa de abertura (emails)
    - [ ] Taxa de clique (emails/WhatsApp)
    - [ ] Última interação (data)

- [ ] **Botão "Adicionar a Campanha"**
  - [ ] Criar botão "Adicionar a Campanha" (estilo golden)
  - [ ] Abrir modal com lista de campanhas ativas
  - [ ] Checkbox para selecionar múltiplas campanhas
  - [ ] Adicionar contacto às campanhas selecionadas

- [ ] **Preferências de Comunicação**
  - [ ] Checkboxes: "Aceita emails", "Aceita WhatsApp", "Aceita SMS"
  - [ ] Guardar em Contact model: `email_consent`, `whatsapp_consent`, `sms_consent` (BooleanFields)
  - [ ] Respeitar RGPD: mostrar data de consentimento

- [ ] **Timeline de Interações**
  - [ ] Lista cronológica (mais recentes primeiro):
    - [ ] Email enviado (ícone envelope)
    - [ ] Email aberto (ícone olho)
    - [ ] Link clicado (ícone cursor)
    - [ ] WhatsApp enviado (ícone WhatsApp)
    - [ ] WhatsApp lido (checkmarks azuis)

- [ ] **Empty State**
  - [ ] SVG + "Sem campanhas enviadas para este contacto"
  - [ ] Call-to-action: "Adicionar à primeira campanha"

---

## 4.14 Tab "Notas" - Melhorias no Editor Quill

Adicionar funcionalidades extras ao editor de notas já existente (Quill.js está implementado).

> **✅ STATUS:** Editor Quill já funcional, esta secção adiciona features extras opcionais.
> **📍 Localização:** `templates/contacts/create.html` (linha ~386 - tab "notas")

- [ ] **Upload de Imagens no Editor**
  - [ ] Activar módulo de imagens do Quill: `imageResize`, `imageUpload`
  - [ ] Criar endpoint `/contacts/upload-note-image/` para receber imagens
  - [ ] Guardar em `media/contacts/notes/`
  - [ ] Validar: max 5MB, formatos JPEG/PNG/GIF

- [ ] **Auto-save de Notas**
  - [ ] Implementar debounce (2 segundos após última edição)
  - [ ] AJAX POST para `/contacts/<uuid>/save-notes/` (salvar sem reload)
  - [ ] Mostrar indicador: "Guardando..." → "Guardado ✓" (estilo Google Docs)
  - [ ] Fallback: se AJAX falhar, salvar no form submit normal

- [ ] **Histórico de Alterações (opcional - Fase 2)**
  - [ ] Criar modelo `ContactNoteVersion` com snapshot de conteúdo por versão
  - [ ] FK para Contact, campo: `content` (TextField), `edited_by` (User), `edited_at` (DateTime)
  - [ ] Botão "Ver Histórico" abre modal com lista de versões
  - [ ] Permitir restaurar versão anterior

- [ ] **Mencionar Utilizadores (@mention)**
  - [ ] Integrar Quill Mention module
  - [ ] Autocompletar: digitar "@" lista utilizadores da empresa
  - [ ] Enviar notificação ao utilizador mencionado (email/dashboard)

- [ ] **Tags de Notas** (categorização)
  - [ ] Adicionar campo `note_tags` (ArrayField ou JSONField) ao Contact
  - [ ] Input de tags abaixo do editor (estilo Notion: #vendas, #urgente, #seguimento)
  - [ ] Filtrar contactos por note_tag na lista

- [ ] **Anexar Ficheiros às Notas**
  - [ ] Criar modelo `ContactNoteAttachment`:
    - [ ] FK para Contact
    - [ ] Campo: `file` (FileField, upload_to='contacts/attachments/')
    - [ ] Campo: `filename`, `filesize`, `uploaded_by`, `uploaded_at`
  - [ ] Área de drag-and-drop para anexos abaixo do editor
  - [ ] Listar anexos com ícones por tipo (PDF, Excel, Word, etc.)
  - [ ] Botão download + delete para cada anexo

---

# 🚀 FASE 5: APP - CRM (CUSTOMER RELATIONSHIP MANAGEMENT)

**⏱ Tempo estimado:** 5-6 dias
**🎯 Objetivo:** Criar sistema de gestão de leads, oportunidades de venda e pipeline comercial
**📦 Dependências:** Fase 4 (Contactos)

---

## 5.1 Criação da App 'crm' ✅

Criar app Django para gestão de CRM.

- [x] **Criar app**
  - [x] Executar `python manage.py startapp crm apps/crm`
  - [x] Adicionar 'apps.crm' ao INSTALLED_APPS

- [x] **Criar estrutura de arquivos**
  - [x] Criar `apps/crm/models.py`
  - [x] Criar `apps/crm/views.py`
  - [x] Criar `apps/crm/forms.py`
  - [x] Criar `apps/crm/urls.py`

- [x] **Componentes de Navegação**
  - [x] Criar `templates/components/crm_navbar.html` (com smart buttons para forms)
  - [x] Criar `templates/components/crm_navbar_simple.html` (sem smart buttons para views)
  - [x] Atualizar todos templates CRM para usar navbar correto

---

## 5.2 Modelo CRMStage (Estágios do Pipeline) ✅

Criar modelo para estágios personalizáveis do pipeline CRM (equivalente ao Odoo CRM stages).

- [x] **Criar modelo CRMStage**
  - [x] Herdar de BaseModel
  - [x] Campo: name (nome do estágio, ex: "New", "Qualified", "Proposition", "Won")
  - [x] Campo: sequence (ordem de exibição, IntegerField)
  - [x] Campo: is_won_stage (BooleanField, default=False) - marca se é estágio de vitória
  - [x] Campo: fold_by_default (BooleanField, default=False) - se deve aparecer colapsado no kanban
  - [x] Campo: routing_in_days (IntegerField, default=0) - dias sem update para highlight (0=desativado)
  - [x] Campo: color (CharField, hex color, ex: "#28a745")
  - [x] Campo: **owner_company** (FK para Company, null=True, blank=True)
  - [x] Meta: ordering = ['sequence']
  - [x] Método __str__ retorna name
  - [x] Filtrar por owner_company usando filter_by_company()

- [x] **Criar estágios default no signal post_migrate**
  - [x] Criar signal para popular estágios iniciais:
    - [x] New (sequence=1, color="#6c757d", routing_in_days=7)
    - [x] Qualified (sequence=2, color="#17a2b8")
    - [x] Proposition (sequence=3, color="#ffc107")
    - [x] Won (sequence=4, color="#28a745", is_won_stage=True, fold_by_default=True)
    - [x] Lost (sequence=5, color="#dc3545", fold_by_default=True)

- [x] **Criar migrations**
  - [x] Executar makemigrations
  - [x] Executar migrate

- [x] **Registrar no Admin**
  - [x] Criar CRMStageAdmin
  - [x] list_display: name, sequence, is_won_stage, routing_in_days, color
  - [x] list_editable: sequence, fold_by_default
  - [x] Ordenar por sequence

- [x] **CRUD Views para CRMStage**
  - [x] CRMStageListView (lista com drag to reorder)
  - [x] CRMStageCreateView (`stage_create_view` + `templates/crm/stage_form.html`)
  - [x] CRMStageUpdateView (`stage_edit_view` + `templates/crm/stage_form.html`)
  - [x] CRMStageDeleteView (soft delete)
  - [x] Templates: `templates/crm/stage_list.html`, `stage_form.html`
  - [x] Rotas: `/crm/stages/`, `/crm/stages/create/`, etc.
  - [x] Sub-navbar CRM (CRM, Sales, Reporting, Configuração/Etapas)
  - [x] Endpoint drag & drop reorder com atualização de sequences
  - [x] Integração com Sortable.js para UI drag & drop

- [x] **Testing - CRMStage**
  - [x] Test: criar estágio funciona
  - [x] Test: reordenação por sequence funciona
  - [x] Test: validação de is_won_stage funciona
  - [x] Test: signal cria estágios default

---

## 5.3 Modelo Lead ✅

Criar modelo para leads/oportunidades de venda.

- [x] **Criar modelo Lead**
  - [x] Herdar de BaseModel
  - [x] Campo: contact (FK para Contact, on_delete=CASCADE)
  - [x] Campo: title (título da oportunidade)
  - [x] Campo: description (descrição detalhada)
  - [x] Campo: estimated_value (valor estimado, Decimal) - "Expected Revenue" no Odoo
  - [x] Campo: probability (probabilidade de fecho, 0-100%)
  - [x] Campo: **priority** (choices: LOW, MEDIUM, HIGH) - Default=MEDIUM - Renderiza como estrelas (0-3)
  - [x] Campo: **stage** (FK para CRMStage, on_delete=PROTECT) - NÃO é choices, é FK!
  - [x] Campo: source (origem: WEBSITE, REFERRAL, COLD_CALL, SOCIAL_MEDIA, OTHER)
  - [x] Campo: expected_close_date (data prevista de fecho)
  - [x] Campo: assigned_to (FK para User, responsável pela lead)
  - [x] Campo: lost_reason (motivo se LOST, TextField nullable)
  - [x] Campo: tags (JSONField para categorização) - Igual sistema de tags dos Contactos
  - [x] Campo: **owner_company** (FK para Company, null=True, blank=True) - NULL=global, com valor=privado
  - [x] Método __str__ retorna title + contact name
  - [x] Property `priority_stars`: retorna 1-3 baseado em priority (LOW=1, MEDIUM=2, HIGH=3)
  - [x] Campo: **stage_updated_at** (DateTimeField) - Para cálculo de routing
  - [x] Filtrar por owner_company na LeadListView usando filter_by_company()
  - [x] Auto-preencher owner_company na create view com get_active_company()

- [x] **Validações e constraints**
  - [x] Validar: estimated_value >= 0
  - [x] Validar: probability entre 0-100
  - [x] Validar: lost_reason obrigatório se stage=LOST
  - [x] Auto-definir probability baseado no stage (recalcular via botão em Definições/CRM)

- [x] **Criar migrations**
  - [x] Executar makemigrations
  - [x] Executar migrate

- [x] **Registrar no Admin**
  - [x] Criar LeadAdmin
  - [x] Configurar list_display: title, contact, stage, estimated_value, probability, priority, assigned_to
  - [x] Configurar search_fields: title, description, contact__name
  - [x] Configurar list_filter: stage, source, priority, assigned_to, created_at
  - [x] Fieldsets separados: Info Básica, Valores, Tracking

- [x] **Testing - Lead Model**
  - [x] Test: criar lead com contact funciona
  - [x] Test: validação de probability funciona
  - [x] Test: stage WON/LOST requer justificação
  - [x] Test: priority_stars property funciona

---

## 5.4 Modelo Activity (Atividades/Tarefas) ✅

Criar modelo para atividades relacionadas com leads (To-Do, Email, Call, Meeting, etc.).

- [x] **Criar modelo Activity**
  - [x] Herdar de BaseModel
  - [x] Campo: lead (FK para Lead, on_delete=CASCADE, related_name='activities')
  - [x] Campo: activity_type (choices: TODO, EMAIL, CALL, WHATSAPP, DOCUMENT, SIGNATURE)
  - [x] Campo: summary (CharField, título da atividade)
  - [x] Campo: due_date (DateField, data limite)
  - [x] Campo: assigned_to (FK para User, responsável)
  - [x] Campo: is_done (BooleanField, default=False)
  - [x] Campo: done_date (DateTimeField, null=True) - quando foi marcada como feita
  - [x] Campo: feedback (TextField, default='', blank=True) - nota ao marcar como concluída
  - [x] Campo: **owner_company** (FK para Company, null=True, blank=True)
  - [x] Método __str__ retorna activity_type + summary
  - [x] Property `is_overdue`: retorna True se due_date < today e not is_done
  - [x] Property `status_color`: retorna 'red' se overdue, 'yellow' se due_date=today, 'green' se ok

- [x] **Validações**
  - [x] Validar: due_date não pode ser no passado (ao criar)
  - [x] Validar: feedback é obrigatório ao marcar is_done=True
  - [x] Auto-preencher done_date quando is_done muda para True

- [x] **Criar migrations**
  - [x] Executar makemigrations
  - [x] Executar migrate

- [x] **Registrar no Admin**
  - [x] Criar ActivityAdmin
  - [x] list_display: summary, lead, activity_type, due_date, assigned_to, is_done
  - [x] list_filter: activity_type, is_done, due_date, assigned_to
  - [x] search_fields: summary, feedback, lead__title

- [x] **CRUD Views para Activity**
  - [x] ActivityCreateView (inline form no chatter do lead_detail, via AJAX)
  - [ ] ActivityUpdateView (modal) - **FUTURO**
  - [x] ActivityMarkDoneView (modal inline com feedback, via AJAX)
  - [x] Templates: atividades implementadas no `lead_create.html` (aba "Atividade" no chatter)
  - [x] Rotas: `/crm/leads/<lead_id>/activities/create/`, `.../<activity_id>/done/`, `.../delete/`

- [x] **Timeline de Activities dentro de Lead**
  - [x] Adicionar seção "Activities" no lead_detail.html (aba "Atividade" no chatter)
  - [x] Mostrar activities ordenadas por due_date (pending primeiro, concluídas depois)
  - [x] Ícones diferentes por activity_type (TODO ✓, CALL 📞, EMAIL ✉, WHATSAPP 💬, DOCUMENT/SIGNATURE 📄)
  - [x] Cores baseadas em status (verde=ok, amarelo=vence hoje, vermelho=atrasado)
  - [x] Botão "Agendar" abre inline form no topo do chatter
  - [x] Botão check (✓) por actividade abre modal de feedback (mark done)

- [x] **Testing - Activity Model**
  - [x] Test: criar activity funciona
  - [x] Test: is_overdue funciona corretamente
  - [x] Test: status_color retorna cor correta
  - [x] Test: feedback obrigatório ao marcar done
  - [x] Test: done_date auto-preenchido

---

## 5.5 Views de Listagem de Leads ✅

Criar view para listar leads com filtros por estágio, responsável e período.

- [x] **Criar LeadListView**
  - [x] Implementar paginação (no topo, formato X-Y / Total)
  - [x] Implementar busca multi-field (title, contact, email, phone, stage, source, assigned_to)
  - [x] Implementar filtro por stage (Ativas [exclui Won/Lost], Won, Lost, Todas)
  - [x] Nomes de stages dinâmicos do DB (multilíngue)
  - [ ] Implementar filtro por assigned_to (ver só as minhas vs todas) - **FUTURO**
  - [ ] Implementar filtro por período (created_at range) - **FUTURO**
  - [ ] Ordenação customizável por estimated_value, probability, expected_close_date - **FUTURO**

- [x] **Criar template**
  - [x] Criar `templates/crm/lead_list.html`
  - [x] Tabela com: checkbox, Oportunidade, Contacto, Etapa, Valor, Responsável
  - [x] Rows clicáveis (navegam para lead detail)
  - [x] Filtro de stage no topo (dropdown com 4 opções)
  - [x] Search bar profissional (formato "Search **Field** for: ...")
  - [x] Sistema de seleção múltipla com checkboxes (Alpine.js)
  - [x] Bulk actions: Won, Lost, Delete (sem modais, sem arquivar)
  - [x] Navbar simples separado (sem smart buttons)
  - [ ] Cards com KPIs: Total Leads, Valor Total Pipeline, Taxa de Conversão - **FUTURO**

- [x] **Configurar rota**
  - [x] `path('crm/list/', LeadListView, name='lead_list')`
  - [x] `path('crm/leads/bulk-delete/', bulk_delete_leads)`
  - [x] `path('crm/leads/bulk-mark-won/', bulk_mark_won)`
  - [x] `path('crm/leads/bulk-mark-lost/', bulk_mark_lost)`

- [ ] **Testing - Lead List** - **NÃO IMPLEMENTADO**
  - [ ] Test: lista mostra leads do user
  - [ ] Test: filtros funcionam
  - [ ] Test: busca funciona
  - [ ] Test: bulk actions funcionam

---

## 5.6 Views de Criação de Lead 🔄

Criar formulário para criar nova lead. **STATUS: Template funcional criado, botões contextuais serão implementados no futuro**

- [x] **Criar template `lead_create.html`**
  - [x] Form com todos os campos principais (title, contact, description, value, stage, etc.)
  - [x] Layout com Tailwind CSS responsivo
  - [x] Abas: Geral, Descrição, Marketing
  - [x] Support para Quill editor (rich text)
  - [x] Upload de imagens
  - [x] Modal Lost (para marcar lead como perdida)
  - [x] Navbar completo com form actions (Guardar/Descartar)
  - [x] Rota configurada: `path('crm/create/', lead_create, name='lead_create')`

- [ ] **TAREFAS FUTURAS - NÃO IMPLEMENTAR AGORA** ⏳
  - [ ] ⏳ Botão "Criar Leads" funcional nos pipelines/listas (atualmente link placeholder)
  - [ ] ⏳ Smart buttons no navbar (Vendas Geradas, Receita Total) - conectados a dados reais
  - [ ] ⏳ Botão "Novo Orçamento" no navbar
  - [ ] ⏳ Auto-complete para contact field
  - [ ] ⏳ Validações client-side avançadas (Alpine.js)
  - [ ] ⏳ Option criar novo contact inline (modal)
  - [ ] ⏳ Botão "Guardar e Criar Novo"

- [ ] **Testing - Lead Create** - **NÃO IMPLEMENTADO**
  - [ ] Test: criar lead funciona
  - [ ] Test: validações funcionam
  - [ ] Test: upload de imagens funciona

---

## 5.7 Views de Edição e Detalhes 🔄

Criar views para editar e visualizar detalhes de lead. **STATUS: Template funcional reusa lead_create.html, features avançadas serão implementadas no futuro**

- [x] **Template unificado create/edit**
  - [x] `templates/crm/lead_create.html` serve para criação e edição
  - [x] Form detecta se é create ou edit baseado em context
  - [x] Navbar completo incluído (com smart buttons)
  - [x] Rota configurada: `path('crm/<uuid:pk>/', lead_detail/edit)`

- [ ] **TAREFAS FUTURAS - NÃO IMPLEMENTAR AGORA** ⏳
  - [ ] ⏳ Smart buttons conectados a dados reais:
    - [ ] Vendas Geradas (count de SaleOrders relacionadas)
    - [ ] Receita Total (soma de valores de vendas)
    - [ ] Documentos anexados
    - [ ] Atividades pendentes
  - [ ] ⏳ Botão "Novo Orçamento" funcional (cria SaleOrder baseada na lead)
  - [ ] ⏳ Seção Activities/Chatter (timeline de atividades):
    - [ ] Botão "Schedule Activity" 
    - [ ] Timeline vertical com activities
    - [ ] Ícones por tipo de atividade
    - [ ] Status colors (verde/amarelo/vermelho)
    - [ ] Mark done functionality
  - [ ] ⏳ LeadDetailView separado (view-only mode)
  - [ ] ⏳ Histórico de mudanças (AuditLog integration)
  - [ ] ⏳ Modal lost_reason ao mudar para stage Lost
  - [ ] ⏳ Sugestão de criar venda ao mudar para Won

- [ ] **Testing - Lead Detail/Edit** - **NÃO IMPLEMENTADO**
  - [ ] Test: edição salva alterações
  - [ ] Test: smart buttons mostram dados corretos
  - [ ] Test: activities timeline renderiza
  - [ ] Test: lost_reason obrigatório se Lost

- [ ] **Testing - Lead Detail/Edit**
  - [ ] Test: detail mostra dados corretos
  - [ ] Test: edit salva alterações
  - [ ] Test: lost_reason obrigatório se LOST
  - [ ] Test: activities timeline renderiza corretamente
  - [ ] Test: cores de status das activities funcionam

---

## 5.8 Conversão de Lead para Venda

Criar funcionalidade para converter lead em venda (SaleOrder).

- [ ] **Criar LeadConvertView**
  - [ ] Botão "Converter em Venda" no lead_detail
  - [ ] Criar SaleOrder com contact da lead
  - [ ] Copiar estimated_value como total inicial
  - [ ] Marcar lead como stage=WON
  - [ ] Criar FK: SaleOrder.lead (origem)
  - [ ] Redirect para sale_create com dados pré-preenchidos

- [ ] **Validações**
  - [ ] Lead já não pode estar WON/LOST
  - [ ] Contact da lead deve ser CLIENT ou BOTH
  - [ ] Se contact for SUPPLIER, mostrar erro

- [ ] **Criar template/modal**
  - [ ] Modal de confirmação: "Converter Lead em Venda?"
  - [ ] Preview dos dados que serão copiados
  - [ ] Botão "Confirmar Conversão"

- [ ] **Configurar rota**
  - [ ] `path('crm/leads/<uuid:pk>/convert/', LeadConvertView, name='lead_convert')`

- [ ] **Testing - Lead Conversion**
  - [ ] Test: conversão cria SaleOrder
  - [ ] Test: lead fica WON após conversão
  - [ ] Test: FK lead → sale funciona
  - [ ] Test: não permite converter LOST/WON

---

## 5.9 🎯 Pipeline de Vendas (Kanban View) - **VISTA DEFAULT DO CRM**

**IMPORTANTE:** Esta é a vista PRINCIPAL e DEFAULT do módulo CRM (igual ao Odoo). A URL `/crm/` deve abrir automaticamente esta vista, não a lista tabular.

Criar vista Kanban "estilo Odoo" para visualizar pipeline de vendas por estágio com drag & drop entre colunas, totais, progress bars e filtros avançados.

---

### ✅ PROGRESSO GERAL: ~85% COMPLETO

**✅ IMPLEMENTADO:**
- ✅ Pipeline como vista default em `/crm/`
- ✅ Colunas dinâmicas por CRMStage (ordenado por sequence, filter_by_company)
- ✅ Layout horizontal flex com scroll-x contido ao pipeline
- ✅ Pipeline ocupa altura total do viewport (JS dinâmico)
- ✅ Colunas colapsáveis (Alpine.js): 150px colapsada, 300px expandida
- ✅ Headers com cor do stage, nome, contador, total value
- ✅ Formatação de valores com K/M/B (custom filter `short_value`)
- ✅ Cards com título, valor, contact, source badge, priority stars, avatar
- ✅ Highlights de overdue (vermelho) e warning (amarelo) nos cards
- ✅ Search bar idêntica ao app contacts (multi-field)
- ✅ View toggle (Kanban/List) na UI
- ✅ 110 leads de teste criadas (9 New, 9 Qualified, 8 Proposition, 52 Won, 32 Lost)
- ✅ Template filter `crm_filters.py` com formatação de valores
- ✅ Campo `Lead.contact` agora opcional (migração aplicada)
- ✅ **Drag & drop funcional** com Sortable.js entre TODAS as colunas
- ✅ **API endpoint `/crm/leads/<uuid>/change-stage/`** com validação multi-company
- ✅ **Validação aceita stages globais** (owner_company=None) e stages da empresa
- ✅ **UI update automático em tempo real** de totais e contadores após drag
- ✅ **Formatação K/M/B em JavaScript** sincronizada com Python
- ✅ **Debug logs removidos** do código de produção
- ✅ **Botão adicionar stage removido** do pipeline (só via Configurações)
- ✅ **Botão "+" funcional para criar lead no stage** (oculto em Won/Lost)
- ✅ **Lead detail view (click no card)** → Abre `/crm/leads/<uuid>/` com proteção anti-drag

**⏳ PENDENTE (Extras/Futuro):**
- ⏳ Activity icons baseados em activities reais do banco ⭐
- ⏳ Sistema de tags customizáveis (JSONField) ⭐
- ⏳ Lead list view alternativa (`/crm/sales/`) ⭐
- ⏳ Mobile responsive otimizado (accordion/tabs) ⭐
- ⏳ Testes automatizados ⭐
- ⏳ Prioridade stars corrigida (HIGH=3, MEDIUM=2, LOW=1) ⭐
- ⏳ Animação visual de sucesso ao arrastar ⭐

---

### 5.9.1 Estrutura do Kanban Board

- [x] **Criar LeadPipelineView (Vista Default)**
  - [x] **URL Principal:** `path('crm/', LeadPipelineView, name='crm_home')` → Redireciona automaticamente para pipeline
  - [x] **URL Alternativa:** `path('crm/pipeline/', LeadPipelineView, name='lead_pipeline')` → Alias
  - [x] Carregar stages dinâmicamente do modelo CRMStage (ordenado por sequence, filter_by_company)
  - [x] Layout: container flex horizontal com scroll-x
  - [x] Criar coluna para cada stage (NÃO hardcoded!)
  - [x] Min-width por coluna: 300px expandida, 150px colapsada (adaptado)
  - [x] Gap entre colunas: 1rem
  - [x] Aplicar fold_by_default: colunas configuradas aparecem colapsadas (mostrar só header)
  - [x] Botão "Expand/Collapse" em cada coluna colapsada

- [x] **Header de Cada Coluna**
  - [x] Background: `background-color: stage.color` (cor do CRMStage) - implementado como barra colorida no topo
  - [x] Padding: py-3 px-4 (ajustado px-2 pb-3)
  - [x] Layout:
    - [x] **Linha 1:** Nome do stage (text-white, font-bold, text-lg) + Badge com contador "(X)"
    - [x] **Linha 2:** Total estimado com formatação K/M/B (ex: 137K, 204.3M)
    - [x] **Linha 3:** Progress bar horizontal (barra simples, não dividida em 3 cores)
  - [x] Botão "+" no canto superior direito → redireciona para lead_create com query param `?stage=<uuid>`
  - [x] Botão "+" oculto em stages is_won_stage=True e is_lost_stage=True

- [x] **Container de Cards**
  - [x] Área scrollável verticalmente com altura dinâmica via JS
  - [x] Padding: px-1
  - [x] Background: bg-gray-800 dark:bg-gray-800
  - [x] Cards empilhados com gap space-y-2
  - [x] Empty state: "Nenhuma oportunidade neste estágio" ✅

### 5.9.2 Progress Bar por Estágio

**Progress Bar baseada em `routing_in_days`:**
Se stage.routing_in_days > 0, mostrar barra dividida em 3 cores baseada no tempo que a lead está no stage:

- [x] **Calcular para cada lead no stage:**
  - [x] `days_in_stage = (hoje - lead.stage_updated_at).days`
  - [x] Verde (no prazo): `days_in_stage < routing_in_days`
  - [x] Amarelo (último dia): `days_in_stage == routing_in_days`
  - [x] Vermelho (atrasado): `days_in_stage > routing_in_days`
  - [x] IMPLEMENTADO: flags `is_overdue` e `is_warning` anotadas em cada lead no view

- [x] **Renderizar indicadores visuais:** (Abordagem alternativa implementada)
  - [x] Highlights nos CARDS em vez de barra dividida no header:
    - [x] Verde (no prazo): sem highlight, border normal
    - [x] Amarelo (warning): bg-yellow-900/30, border-yellow-700/50
    - [x] Vermelho (overdue): bg-red-900/30, border-red-700/50
  - [x] Progress bar simples no header (não dividida em 3 cores)
  - [x] ~~**TODO FUTURO:** Implementar barra dividida em 3 cores com tooltips no header~~ — ❌ **Obsoleto** (cards individuais já têm cores de routing)

**Alternativa opcional (comentar no código):**
Progress bar baseada em `probability` média do stage (mais simples, menos específico):
- [x] ~~Calcular avg_probability do stage~~ — ❌ **Obsoleto**
- [x] ~~Barra única com fill de avg_probability% (cor do stage)~~ — ❌ **Obsoleto**

### 5.9.3 Lead Cards (Design Odoo-like)

- [x] **Layout do Card (Design compacto)**
  - [x] Container: bg-gray-800 dark:bg-gray-800, rounded-lg, shadow-sm, p-3
  - [x] Border com cores baseadas em routing (amarelo/vermelho para warning/overdue)
  - [x] Hover: border-gray-600, cursor-pointer
  - [x] Click: abre lead_detail_view em `/crm/leads/<uuid>/` com proteção `if (!isDragging)`

- [x] **Linha 1: Título da Lead**
  - [x] `lead.title` em font-medium, text-sm, text-white
  - [x] Exibido corretamente

- [x] **Linha 2: Expected Revenue (Destaque)**
  - [x] `lead.estimated_value` formatado: **"$ 15,000.00"**
  - [x] Cor: text-gray-300
  - [x] Font: text-sm

- [x] **Linha 3: Nome do Contacto**
  - [x] `lead.contact.name` em text-xs, text-gray-400
  - [x] Exibido se lead.contact existe (campo agora opcional)

- [x] **Linha 4: Estrelas de Prioridade (Priority Stars)**
  - [x] Renderizar baseado em `lead.priority`:
    - [x] LOW: ☆☆☆ (3 estrelas vazias)
    - [x] MEDIUM: ★☆☆ (1 estrela amarela, 2 vazias)
    - [x] HIGH: ★★☆ (2 estrelas amarelas, 1 vazia)
  - [x] Estrela preenchida: `★` text-yellow-400
  - [x] Estrela vazia: `★` text-gray-600
  - [x] **NOTA:** Lógica invertida em relação ao spec original, ajustar se necessário

- [x] **Linha 5: Tags (Source Badge + Tags customizáveis)**
  - [x] Badge de source renderizado com cores diferentes:
    - [x] WEBSITE: blue, REFERRAL: green, SOCIAL_MEDIA: purple, etc.
  - [x] Formato: px-2, py-0.5, rounded-full, text-xs
  - [x] Sistema de tags customizáveis implementado (M2M com CRMTag, gestão em /crm/tags/)

- [x] **Linha 6: Activity Icons**
  - [x] Ícone de telefone (phone) exibido estaticamente
  - [x] **TODO:** Buscar activities reais do banco e renderizar dinamicamente
  - [x] **TODO:** Cores baseadas em status (done/overdue/pending)

- [x] **Linha 7: Assigned To (Responsável)**
  - [x] Avatar circular com iniciais do username
  - [x] Background: bg-primary, w-6 h-6
  - [x] Posição: canto inferior direito do card
  - [x] Tooltip com username no title

### 5.9.4 Drag & Drop Entre Colunas (Sortable.js)

**STATUS: ✅ IMPLEMENTADO - Drag & drop funcional com backend**

- [x] **Implementar Sortable.js para inter-column drag**
  - [x] Cada coluna é um container sortable separado
  - [x] Configuração implementada com group: 'leads', animation: 150, etc.
  - [x] Data attributes adicionados: `data-stage-id` nas colunas, `data-lead-id` nos cards
  - [x] Cursor mudado para `cursor-move` nos cards
  - [x] onEnd handler chama `moveLeadToStage()` via AJAX

- [x] **Backend endpoint: lead_change_stage**
  - [x] Rota: `POST /crm/leads/<uuid:lead_id>/change-stage/`
  - [x] Payload: `{"new_stage_id": "abc-123"}`
  - [x] Validações:
    - [x] Lead existe e pertence à company do user
    - [x] New stage existe e pertence à company do user
    - [x] Multi-company security enforced com `get_active_company()`
  - [x] Updates:
    - [x] `lead.stage = new_stage`
    - [x] `lead.stage_updated_at = timezone.now()` (para routing)
  - [x] Retorna JSON:
    ```json
    {
      "success": true,
      "new_stage_name": "Qualified",
      "new_stage_color": "#17a2b8",
      "old_column_total": 65000.00,
      "new_column_total": 80000.00,
      "old_column_count": 8,
      "new_column_count": 12
    }
    ```

- [x] **TODO CONCLUÍDO:**
  - [x] ~~Auto-update `lead.probability` baseado em stage default_probability~~ (não necessário por agora)
  - [x] **UI update automático de totais/contadores em tempo real** (IMPLEMENTADO)
  - [x] **Stages globais aceites na validação multi-company** (IMPLEMENTADO)
  - [x] **Debug logs removidos** (IMPLEMENTADO)
  - [x] **Botão adicionar stage removido do pipeline** (IMPLEMENTADO)

- [ ] **TODO FUTURO:**
  - [ ] ~~Modal lost_reason para stage "Lost" (quando drag para Lost)~~ — N/A: perdidas são geridas via campo no formulário, não por drag
  - [ ] Animação visual de sucesso/erro no drag

### 5.9.5 Totais e KPIs por Coluna

- [x] **Calcular totais no backend (LeadPipelineView):**
  - [x] Total value (soma de estimated_value) calculado
  - [x] Count de leads calculado
  - [x] Routing calculations (is_overdue, is_warning) implementado nos cards
  - [x] Dados passados no context como `pipeline_data`
  - [x] ~~**TODO:** Calcular avg_probability~~ — ❌ **Obsoleto** (não necessário, cards já têm cores)
  - [x] ~~**TODO:** Calcular verde/amarelo/vermelho aggregated para progress bar dividida~~ — ❌ **Obsoleto**

- [x] **Renderizar no header:**
  - [x] Contador: badge com `(count)` mostrado na collapsed view
  - [x] Total: `{{ total_value|short_value }}` com formatação K/M/B
  - [x] Progress bar: barra simples colorida (não dividida em 3 seções)
  - [x] ~~**TODO:** Progress bar dividida em 3 cores proporcionais (verde/amarelo/vermelho)~~ — ❌ **Obsoleto**
  ```python
  stages_with_data = []
  for stage in stages.filter_by_company():
      leads = stage.lead_set.filter(is_active=True).filter_by_company()
      total_value = leads.aggregate(Sum('estimated_value'))['estimated_value__sum'] or Decimal('0.00')
      avg_probability = leads.aggregate(Avg('probability'))['probability__avg'] or 0
      count = leads.count()
      
      # Routing calculations (para progress bar)
      if stage.routing_in_days > 0:
          verde = leads.filter(days_in_stage__lt=stage.routing_in_days).count()
          amarelo = leads.filter(days_in_stage=stage.routing_in_days).count()
          vermelho = leads.filter(days_in_stage__gt=stage.routing_in_days).count()
      else:
          verde = amarelo = vermelho = 0
      
      stages_with_data.append({
          'stage': stage,
          'leads': leads,
          'total_value': total_value,
          'avg_probability': avg_probability,
          'count': count,
          'routing_verde': verde,
          'routing_amarelo': amarelo,
          'routing_vermelho': vermelho,
      })
  ```

- [x] ~~**Renderizar no header:**~~ — ❌ **Obsoleto** (headers já implementados com barra simples + contadores)
  - [x] ~~Contador: badge pequeno `({{ count }})` ~~ — ❌ Obsoleto (já implementado)
  - [x] ~~Total: `R$ {{ total_value|floatformat:2 }}`~~ — ❌ Obsoleto (já implementado com short_value)
  - [x] ~~Progress bar: 3 seções com widths proporcionais~~ — ❌ Obsoleto

### 5.9.6 Filtros e Search (Barra Superior)

- [x] **Barra de Filtros no Topo do Pipeline**
  - [x] Search bar implementada (idêntica ao app contacts)
  - [x] Layout com botão "Novo"
  - [x] View toggle (Kanban/List) implementado

- [x] **Filtros implementados via search bar (field selector):**
  - [x] Título, Contacto, Source, Responsável, Prioridade, Etapa, Tags — cobertos pelo field selector da search

- [x] ~~Botão "Clear Filters"~~ — N/A (não necessário)

### 5.9.7 Mobile Responsive

**STATUS: NÃO IMPLEMENTADO - Layout atual responsivo básico com Tailwind, mas não otimizado para mobile**

- [x] **Desktop (>1024px):** Colunas lado a lado com scroll horizontal - FUNCIONA
  - [x] Smooth scroll funciona naturalmente
  - [x] TODO: Ajustar para garantir 4 colunas visíveis

- [x] **Tablet (768-1024px):** 2-3 colunas visíveis ✅
- [x] **Mobile (<768px):** Layout vertical com tabs ✅
  - [x] **Opção 1 - Accordion:**
    - [x] Cada stage é um collapsible panel
    - [x] Click no header expande a coluna, mostra cards
    - [x] Só 1 coluna expandida por vez
  - [x] **Opção 2 - Tabs horizontais:**
    - [x] Tabs com nome dos stages no topo
    - [x] Swipe entre tabs (mobile-friendly)
    - [x] Cada tab mostra cards daquele stage
  - [x] **Drag & drop desabilitado no mobile** (difícil de usar)
    - [x] Substituir por botão "Mover para..." dentro do card
    - [x] Abre dropdown com lista de stages
    - [x] Selecionar novo stage → chama mesmo endpoint change-stage

### 5.9.8 Navegação e URLs

- [x] **Atualizar crm_navbar.html:**
  - [x] Link "CRM" → `/crm/` (pipeline view, DEFAULT) - **Destacado como ativo**
  - [x] ~~Link "Sales" → `/crm/sales/`~~ — ❌ **Obsoleto** (pipeline é a vista principal, não é necessária lista tabular separada)
  - [x] Link "Reporting" → `/crm/reporting/` (dashboards) - **Desabilitado**
  - [x] Dropdown "Configuração" → Etapas, Categorias, etc. - **Implementado**

- [x] ~~**Criar Lead List View alternativa (task 5.5):**~~ — ❌ **Obsoleto** (pipeline kanban cobre todas as necessidades)
  - [x] ~~URL: `/crm/sales/` (lista tradicional tabular)~~ — ❌ Obsoleto
  - [x] ~~Para users que preferem tabelas~~ — ❌ Obsoleto
  - [x] ~~Botão "Ver Pipeline" switch para `/crm/`~~ — ❌ Obsoleto

### 5.9.9 Templates Necessários

- [x] **templates/crm/lead_pipeline.html**: Layout principal do Kanban - **CRIADO ✅**
  - [x] Loop por `pipeline_data`
  - [x] Renderiza colunas com headers colapsáveis (Alpine.js)
  - [x] Renderiza cards com todos os campos principais
  - [x] Search bar com field selector
  - [x] CSS inline para layout flex, scroll, altura dinâmica
  - [x] JS para calcular altura do pipeline dinamicamente
  - [x] SortableJS com drag & drop funcional

- [x] ~~templates/crm/components/lead_card.html~~ — N/A: cards estão inline no pipeline template, não é necessário extrair
- [x] ~~templates/crm/lost_reason_modal.html~~ — N/A: não necessário (perdidas geridas via form)
- [x] ~~templates/crm/pipeline_filters.html~~ — N/A: filtros inline no pipeline template

### 5.9.10 Testing - Pipeline View

**STATUS: Testes manuais pelo utilizador — testes automatizados não necessários por agora.**

- [ ] **Test: tags renderizam como badges**
  - Lead com 2 tags: "VIP" (vermelho), "Urgente" (laranja)
  - Verificar 2 badges coloridos aparecem

- [ ] **Test: activity icons aparecem**
  - Lead com 1 CALL (pendente), 1 EMAIL (done)
  - Verificar 📞 (cinza) e ✉️ (verde) aparecem

- [ ] **Test: filtro "Assigned to Me" funciona**
  - Criar 3 leads: 2 para user A, 1 para user B
  - User A aplica filtro "As minhas"
  - Verificar só 2 leads aparecem

- [ ] **Test: filtro por priority funciona**
  - Criar leads: 2 HIGH, 2 MEDIUM, 1 LOW
  - Aplicar filtro "High"
  - Verificar só 2 leads aparecem

- [x] **Test: mobile responsive mostra accordion ou tabs** ✅
  - Viewport <768px
  - Verificar colunas viram accordion/tabs
  - Verificar drag & drop desabilitado

- [ ] **Test: fold_by_default colapsa colunas**
  - Stage com fold_by_default=True
  - Verificar coluna aparece colapsada (só header)
  - Click no botão "Expand" → mostra cards

- [x] **Test: botão "+" no header cria lead direto no stage** ✅
  - Click no "+" do stage "Qualified"
  - Verificar form abre com stage pré-selecionado

---

## 5.10 Generate Leads (Geração Automática Baseada em Histórico) ✅ COMPLETO

Funcionalidade para gerar leads automaticamente baseado em dados históricos (recorrências de encomendas anteriores).

- [x] View `generate_leads_action` implementada em `apps/crm/views.py`
- [x] Serviço `generate_leads_from_history` em `apps/crm/services.py`
- [x] Rota `POST /crm/generate-leads/` configurada (`crm:generate_leads`)
- [x] Botão "Gerar Leads" na página de Definições/CRM com select de período
- [x] Evita duplicados (não cria lead se já existe lead ativa para o mesmo contact/período)
- [x] Toast de feedback após geração

---

## 5.11 Integração da Aba Marketing com Módulo de Marketing (Futuro)

Implementar a lógica completa de backend e integração futura entre os campos de Marketing da Lead e um módulo de Marketing dedicado.

**CONTEXTO:**
- Atualmente a aba "Marketing" no formulário de Lead (`lead_create.html`) tem 4 campos informativos:
  - Campanha (campaign)
  - Mídia (medium)
  - Origem (source)
  - Referenciado Por (referred_by)
- Estes campos são atualmente apenas text inputs simples (não conectados a nenhum modelo)
- No futuro, devem ser integrados com um módulo completo de Marketing (Campaigns, UTM tracking, Referral program)

**OBJETIVO:** Criar os campos no modelo Lead, preparar relações para futuro módulo de Marketing, e implementar a lógica de salvamento/recuperação dos dados.

- [ ] **Adicionar campos ao modelo Lead**
  - [ ] Adicionar campos ao `apps/crm/models.py` (classe Lead):
    ```python
    # Marketing fields
    marketing_campaign = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Campanha',
        help_text='Nome da campanha de marketing (futuro: FK para Campaign)'
    )
    marketing_medium = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Mídia',
        help_text='Canal/mídia (ex: Google Ads, Facebook, Email, WhatsApp)'
    )
    marketing_source = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Origem',
        help_text='Origem da lead (ex: Website, Landing Page, Referral)'
    )
    marketing_referred_by = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referred_leads',
        verbose_name='Referenciado Por',
        help_text='Contacto que referenciou esta lead'
    )
    ```
  - [ ] Criar migration: `python manage.py makemigrations crm`
  - [ ] Aplicar migration: `python manage.py migrate`

- [ ] **Atualizar LeadForm**
  - [ ] Adicionar campos ao `apps/crm/forms.py` (classe LeadForm):
    - [ ] `marketing_campaign` - CharField widget
    - [ ] `marketing_medium` - CharField widget
    - [ ] `marketing_source` - CharField widget (ou ChoiceField com opções pré-definidas)
    - [ ] `marketing_referred_by` - ModelChoiceField com autocomplete (igual ao campo contact)
  - [ ] Labels em português
  - [ ] Help texts informativos
  - [ ] Todos os campos devem ser `required=False` (opcionais)

- [ ] **Atualizar template lead_create.html**
  - [ ] Conectar os inputs da aba Marketing aos campos do form:
    - [ ] `name="marketing_campaign"` → `{{ form.marketing_campaign }}`
    - [ ] `name="marketing_medium"` → `{{ form.marketing_medium }}`
    - [ ] `name="marketing_source"` → `{{ form.marketing_source }}`
    - [ ] `name="marketing_referred_by"` → implementar autocomplete igual ao campo contact
  - [ ] Manter o aviso amarelo: "Estes campos serão integrados com o módulo de Marketing no futuro"
  - [ ] Adicionar autocomplete para campo "Referenciado Por":
    - [ ] Usar mesmo endpoint `/crm/api/contacts/search/`
    - [ ] Dropdown com resultados
    - [ ] Ao selecionar, preenche input hidden `marketing_referred_by`

- [ ] **Preparar Choices predefinidas (opcional)**
  - [ ] Criar choices para `marketing_medium`:
    ```python
    MARKETING_MEDIUM_CHOICES = [
        ('', '---'),
        ('GOOGLE_ADS', 'Google Ads'),
        ('FACEBOOK_ADS', 'Facebook Ads'),
        ('INSTAGRAM', 'Instagram'),
        ('EMAIL', 'Email Marketing'),
        ('WHATSAPP', 'WhatsApp'),
        ('SMS', 'SMS'),
        ('REFERRAL', 'Indicação'),
        ('OTHER', 'Outro'),
    ]
    ```
  - [ ] Criar choices para `marketing_source`:
    ```python
    MARKETING_SOURCE_CHOICES = [
        ('', '---'),
        ('WEBSITE', 'Website'),
        ('LANDING_PAGE', 'Landing Page'),
        ('SOCIAL_MEDIA', 'Redes Sociais'),
        ('REFERRAL', 'Indicação'),
        ('EVENT', 'Evento'),
        ('COLD_CALL', 'Cold Call'),
        ('OTHER', 'Outro'),
    ]
    ```
  - [ ] No form, usar Select ou Datalist HTML5 (autocomplete nativo)

- [ ] **Implementar autocomplete para "Referenciado Por"**
  - [ ] Criar função Alpine.js `referredByAutocomplete()` em `lead_create.html`
  - [ ] Similar a `contactAutocomplete()` mas para campo separado
  - [ ] Usar endpoint `/crm/api/contacts/search/`
  - [ ] Ao selecionar contacto:
    - [ ] Preencher input visível com nome do contacto
    - [ ] Preencher input hidden `marketing_referred_by` com contact.id

- [ ] **Exibir dados na LeadDetailView**
  - [ ] Adicionar secção "Marketing" no `lead_detail.html`
  - [ ] Mostrar os 4 campos em formato read-only:
    - [ ] Campanha
    - [ ] Mídia
    - [ ] Origem
    - [ ] Referenciado Por (com link para ficha do contacto se existir)
  - [ ] Se todos vazios, mostrar mensagem: "Sem informação de marketing"

- [ ] **UTM Tracking (Preparação para futuro)**
  - [ ] Adicionar 3 campos adicionais ao modelo Lead (opcional, para captura automática):
    ```python
    # UTM Parameters (auto-captured from URL)
    utm_source = models.CharField(max_length=100, blank=True)
    utm_medium = models.CharField(max_length=100, blank=True)
    utm_campaign = models.CharField(max_length=100, blank=True)
    utm_content = models.CharField(max_length=255, blank=True)
    utm_term = models.CharField(max_length=255, blank=True)
    ```
  - [ ] Estes campos serão preenchidos automaticamente quando Lead for criada via formulário web (futuro)
  - [ ] Por agora, deixar como hidden fields ou não exibir no form

- [ ] **Reportórios e Analytics (Futuro)**
  - [ ] Preparar para módulo futuro "Marketing Analytics"
  - [ ] Queries de exemplo que serão úteis:
    - [ ] Leads por campanha (GROUP BY marketing_campaign)
    - [ ] Taxa de conversão por mídia (% de Leads Won por marketing_medium)
    - [ ] ROI por origem (custo da campanha vs. receita gerada)
    - [ ] Top referrers (contactos que mais referenciaram leads)

- [ ] **Testing - Marketing Tab**
  - [ ] Test: campos de marketing salvam corretamente
  - [ ] Test: campo "Referenciado Por" aceita contacto válido
  - [ ] Test: autocomplete de "Referenciado Por" funciona
  - [ ] Test: campos aparecem em lead_detail
  - [ ] Test: campos são opcionais (lead pode ser criada sem marketing info)
  - [ ] Test: migration não quebra leads existentes (campos devem aceitar blank=True)

- [ ] **Documentação**
  - [ ] Atualizar `docs/CRM_Features_Overview.md`:
    - [ ] Adicionar secção sobre Marketing tracking
    - [ ] Explicar campos disponíveis
    - [ ] Notar que integração completa será implementada em módulo futuro
  - [ ] Criar `docs/Marketing_Integration_Roadmap.md` (opcional):
    - [ ] Roadmap para módulo de Marketing
    - [ ] Campaigns, UTM tracking, Landing pages, Email marketing
    - [ ] Integração com Leads CRM

**PRIORIDADE:** Média (não urgente, mas importante preparar os campos para futuro)

**STATUS:** Pendente (campos criados no template, falta backend)

---

## 4.17 Relações e Smart Buttons - Módulo Contactos

**OBJETIVO:** Documentar todas as relações FK que módulos futuros terão com Contactos + criar smart buttons bidirecionais + vistas de listagem.

**ARQUITETURA:** Opção 3 (Foreign Keys Diretas) - cada tabela nova (Vendas, CRM, Compras) terá campo `contact_id` apontando para Contact.

- [ ] **Relações FK Recebidas (outros módulos → Contact)**
  - [x] **CRM/Leads** (Fase futura):
    - [x] Modelo `Lead` terá campo `contact = ForeignKey(Contact, on_delete=CASCADE, related_name='leads')`
    - [x] Smart button: "CRM" no formulário de Contact (contador dinâmico) ✅ IMPLEMENTADO
    - [x] Vista: `contact_crm_list(contact_id)` usando filtro na lead_list_view ✅ IMPLEMENTADO
    - [x] Rota: `/crm/list/?contact=<uuid>` ✅ IMPLEMENTADO
    - [x] Colunas tabela: Oportunidade, Contacto, Etapa, Valor, Responsável ✅ IMPLEMENTADO
    - [x] Filtro mantido em paginação, stage filters e search ✅ IMPLEMENTADO
    - [x] Banner "Leads de [Nome]" com botão remover filtro ✅ IMPLEMENTADO
  - [ ] **Vendas** (Fase 7):
    - [ ] Modelo `SaleOrder` terá campo `contact = ForeignKey(Contact, on_delete=PROTECT, related_name='sales')`
    - [ ] Smart button: "Vendas" no formulário de Contact
    - [ ] Vista: `contact_sales_list(contact_id)` usando template base
    - [ ] Rota: `/contacts/<uuid:pk>/sales/`
    - [ ] Colunas tabela: Nº Venda, Data, Total, Estado, Estado Pagamento
    - [ ] Se 1 venda → redireciona para `sale_detail(pk)`
    - [ ] Se múltiplas → mostra lista clicável
  - [ ] **Compras** (Fase 6):
    - [ ] Modelo `PurchaseOrder` terá campo `supplier = ForeignKey(Contact, on_delete=PROTECT, related_name='purchases')` (apenas SUPPLIER ou BOTH)
    - [ ] Smart button: "Compras" no formulário de Contact (só aparece se contact_type = SUPPLIER ou BOTH)
    - [ ] Vista: `contact_purchases_list(contact_id)` usando template base
    - [ ] Rota: `/contacts/<uuid:pk>/purchases/`
    - [ ] Colunas tabela: Nº Compra, Data, Total, Estado
    - [ ] Se 1 compra → redireciona para `purchase_detail(pk)`
    - [ ] Se múltiplas → mostra lista clicável
  - [ ] **Faturas** (Fase 8):
    - [ ] Modelo `Invoice` terá campo `contact = ForeignKey(Contact, on_delete=PROTECT, related_name='invoices')`
    - [ ] Smart button: "Faturas" no formulário de Contact (mostra SOMA dos valores, não contagem)
    - [ ] Vista: `contact_invoices_list(contact_id)` usando template base
    - [ ] Rota: `/contacts/<uuid:pk>/invoices/`
    - [ ] Colunas tabela: Nº Fatura, Data, Total, Estado Pagamento
    - [ ] Se 1 fatura → redireciona para `invoice_detail(pk)`
    - [ ] Se múltiplas → mostra lista clicável
  - [ ] **Documentos** (Fase 10):
    - [ ] Modelo `Document` terá campo `contact = ForeignKey(Contact, on_delete=CASCADE, related_name='documents', null=True, blank=True)`
    - [ ] Smart button: "Documentos" no formulário de Contact
    - [ ] Vista: `contact_documents_list(contact_id)` usando template base
    - [ ] Rota: `/contacts/<uuid:pk>/documents/`
    - [ ] Colunas tabela: Nome Ficheiro, Tipo, Data Upload, Tamanho
    - [ ] Se 1 documento → abre diretamente o PDF/ficheiro
    - [ ] Se múltiplos → mostra lista clicável
  - [ ] **Campanhas Marketing** (Fase 11):
    - [ ] Modelo `MarketingCampaign` terá M2M com Contact via `CampaignContact`
    - [ ] Smart button: "Marketing" no formulário de Contact
    - [ ] Vista: `contact_campaigns_list(contact_id)` usando template base
    - [ ] Rota: `/contacts/<uuid:pk>/campaigns/`
    - [ ] Colunas tabela: Nome Campanha, Data Envio, Canal (Email/WhatsApp), Estado
    - [ ] Se 1 campanha → redireciona para `campaign_detail(pk)`
    - [ ] Se múltiplas → mostra lista clicável

- [ ] **Método Helper para Contadores**
  - [ ] Adicionar método `Contact.get_stats()` no modelo Contact:
    ```python
    def get_stats(self):
        return {
            'crm': self.leads.filter(is_active=True).count(),
            'sales': self.sales.count(),
            'purchases': self.purchases.count() if self.contact_type in ['SUPPLIER', 'BOTH'] else 0,
            'invoices_total': self.invoices.aggregate(Sum('total'))['total__sum'] or 0,
            'documents': self.documents.count(),
            'campaigns': self.marketing_campaigns.count(),
        }
    ```
  - [ ] No template do formulário Contact, chamar `contact.get_stats` para popular os smart buttons
  - [ ] Usar `.annotate()` para otimizar quando listar múltiplos contactos

- [ ] **Testing - Contact Relations**
  - [ ] Test: `contact.get_stats()` retorna contadores corretos
  - [ ] Test: smart button CRM redireciona para lista quando > 1 lead
  - [ ] Test: smart button Vendas redireciona direto quando = 1 venda
  - [ ] Test: smart button Compras só aparece se SUPPLIER/BOTH
  - [ ] Test: smart button Faturas mostra valor total, não contagem
  - [ ] Test: vistas usam template base corretamente

---

## 5.12 🎯 Funcionalidades Futuras - CRM UI/UX ⏳

**IMPORTANTE:** Esta secção contém funcionalidades que serão implementadas no futuro. **NÃO IMPLEMENTAR AGORA.**

Estas tarefas são placeholders para desenvolvimento futuro e incluem integrações com outros módulos (Vendas, Orçamentos) que ainda não existem.

---

### 5.12.1 Botão "Criar Leads" Contextual ⏳

Implementar botões "Nova Lead" / "Criar Leads" funcionais em diversos contextos (pipeline, list view, navbar).

- [x] **Botão "+" nas colunas do Pipeline** ✅
  - [x] Click no "+" de cada coluna do kanban cria lead direto naquele stage
  - [x] Stage pré-selecionado baseado na coluna clicada
  - [x] Form simplificado (title, contact, estimated_value)
  - [x] Após criar, card aparece automaticamente na coluna sem refresh

- [ ] **Botão "Nova Lead" na List View** ⏳
  - [ ] Botão no topo da lead_list.html (atualmente placeholder `href="#"`)
  - [ ] Abre modal ou redireciona para `lead_create`
  - [ ] Stage default = primeiro estágio (não Won/Lost)

- [ ] **Botão "Nova Lead" no Navbar** ⏳
  - [ ] Adicionar botão quick-create no navbar CRM
  - [ ] Dropdown com opção "Nova Lead" e "Nova Atividade"
  - [ ] Atalho de teclado (Ctrl+N)

---

### 5.12.2 Smart Buttons - Vendas e Receitas ⏳

Conectar smart buttons do navbar de leads aos dados reais de vendas geradas.

**CONTEXTO:** 
- Navbar completo (`crm_navbar.html`) já inclui HTML para smart buttons "Vendas" e "Receita"
- Atualmente não conectados a dados (só visual)
- Dependem do módulo Vendas (Fase 8) estar implementado

- [ ] **Backend - Calcular Vendas/Receita** ⏳
  - [ ] No `lead_detail/edit` view, adicionar ao context:
    ```python
    # Contar vendas geradas desta lead
    sales_count = SaleOrder.objects.filter(
        lead=lead,
        is_active=True
    ).count()
    
    # Calcular receita total das vendas
    revenue_total = SaleOrder.objects.filter(
        lead=lead,
        is_active=True,
        state__in=['CONFIRMED', 'DONE']  # só vendas confirmadas
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0.00')
    
    context['sales_count'] = sales_count
    context['revenue_total'] = revenue_total
    ```

- [ ] **Template - Ligar variáveis aos buttons** ⏳
  - [ ] No `crm_navbar.html`, smart buttons já renderizam:
    - [ ] `{{ sales_count }}` - contador de vendas
    - [ ] `{{ revenue_total|floatformat:2 }}` - valor formatado
  - [ ] Verificar que variáveis existem no context antes de renderizar
  - [ ] Se `sales_count == 0`, mostrar botão disabled/cinza

- [ ] **Click nos Smart Buttons** ⏳
  - [ ] Button "Vendas" redireciona para: `/sales/?lead={{ lead.id }}`
    - [ ] Mostra lista de SaleOrders filtrada por esta lead
    - [ ] Se só 1 venda, redireciona direto para `sale_detail(pk)`
  - [ ] Button "Receita" abre modal/tooltip com breakdown:
    - [ ] Lista de vendas com valores
    - [ ] Total confirmado vs pending
    - [ ] Link para cada venda

- [ ] **Ocultar Smart Buttons em Create Mode** ⏳
  - [ ] Detectar se é `lead_create` (sem pk) ou `lead_edit` (com pk)
  - [ ] Smart buttons só aparecem em edit mode (lead já existe)
  - [ ] Em create mode, esconder seção de smart buttons

---

### 5.12.3 Botão "Novo Orçamento" ⏳

Criar botão no navbar de leads para gerar novo orçamento (SaleOrder) baseado na lead.

**CONTEXTO:** 
- Similar a "Converter em Venda" mas cria orçamento draft (não marca lead como Won)
- Permite múltiplos orçamentos para mesma lead
- Depende do módulo Vendas (Fase 8) estar implementado

- [ ] **Adicionar botão ao Navbar** ⏳
  - [ ] No `crm_navbar.html`, adicionar botão "Novo Orçamento" ao lado de form actions
  - [ ] Ícone: 📄 ou Heroicon `document-text`
  - [ ] Texto: "Novo Orçamento"
  - [ ] Posição: entre smart buttons e form actions
  - [ ] Visível apenas em edit mode (lead existe)

- [ ] **View - CreateQuoteFromLead** ⏳
  - [ ] Criar view `crm/views.py`: `create_quote_from_lead(request, lead_pk)`
  - [ ] Buscar lead por UUID
  - [ ] Criar novo SaleOrder com:
    ```python
    from apps.sales.models import SaleOrder  # (Fase 8)
    
    sale = SaleOrder.objects.create(
        contact=lead.contact,
        lead=lead,  # FK para lead origem
        state='DRAFT',  # orçamento draft
        salesperson=lead.assigned_to,
        expected_value=lead.estimated_value,
        notes=f"Orçamento gerado da lead: {lead.title}\n\n{lead.description}",
        owner_company=lead.owner_company,
    )
    ```
  - [ ] Redirecionar para `sale_edit(pk)` para adicionar linhas de produtos

- [ ] **Rota** ⏳
  - [ ] `path('crm/<uuid:pk>/create-quote/', create_quote_from_lead, name='lead_create_quote')`

- [ ] **Validações** ⏳
  - [ ] Lead deve ter contact associado
  - [ ] Lead não pode estar Lost
  - [ ] Se lead já Won, perguntar se quer criar novo orçamento mesmo assim (modal confirmação)

- [ ] **Feedback** ⏳
  - [ ] Toast: "✅ Orçamento criado! Adicione produtos..."
  - [ ] Atualizar smart button "Vendas" (+1 count)

---

### 5.12.4 Melhorias na Lead List View ⭐ EXTRA

Funcionalidades adicionais para a vista de lista de leads (KPIs, filtros avançados, exportação). **Não obrigatórias - melhoram UX mas não são essenciais.**

- [ ] **Cards com KPIs no Topo** ⭐
  - [ ] Card 1: Total de Leads (count filtrado) ⭐
  - [ ] Card 2: Valor Total do Pipeline (soma estimated_value) ⭐
  - [ ] Card 3: Taxa de Conversão (Won / Total) ⭐
  - [ ] Card 4: Leads Este Mês (created_at range) ⭐
  - [ ] Responsive: 2 cards mobile, 4 desktop ⭐

- [ ] **Filtros Avançados** ⭐
  - [ ] Filtro por assigned_to (dropdown multi-select) ⭐
  - [ ] Filtro por priority (LOW, MEDIUM, HIGH) ⭐
  - [ ] Filtro por source (WEBSITE, REFERRAL, etc.) ⭐
  - [ ] Botão "Clear Filters" ⭐

- [ ] **Ordenação Customizável** ⭐
  - [ ] Click nos headers da tabela para ordenar ⭐
  - [ ] Colunas orderáveis: Valor, Probabilidade, Data Criação, Data Fecho Prevista ⭐
  - [ ] Indicador visual de ordenação (seta ↑↓) ⭐

- [ ] **Exportação para Excel/CSV** ⭐
  - [ ] Botão "Exportar" no topo ⭐
  - [ ] Gera arquivo CSV com leads filtradas ⭐
  - [ ] Colunas: Title, Contact, Stage, Value, Probability, Assigned To, Created At ⭐

---

### 5.12.5 Integração com Chatter (aba Activities) ⏳

Implementar timeline de atividades dentro do formulário de lead (dependente da Fase 3 - Chatter).

**NOTA:** Esta funcionalidade depende do sistema de Chatter (Fase 3, task 3.8) estar completo.

- [x] **Adicionar aba "Atividades" ao lead_create.html** ✅
  - [x] Nova aba após "Marketing"
  - [x] Só visível em edit mode (lead existe)

- [x] **Incluir componente Chatter** ✅
  - [x] `{% include 'components/chatter.html' with object=lead %}`
  - [x] Componente renderiza automaticamente:
    - [x] Timeline de mensagens/comments
    - [x] Timeline de activities
    - [x] Botão "Schedule Activity"
    - [x] Botão "Log Note"

- [x] **Botão Quick-Add Activity** ✅
  - [x] Botão no topo da aba "Atividades"
  - [x] Modal simplificado para criar activity:
    - [x] Tipo (Call, Email, Todo, Meeting)
    - [x] Título
    - [x] Data limite
    - [x] Responsável (default= lead.assigned_to)
  - [x] Após criar, activity aparece no timeline

- [x] **Notificações de Activities Vencidas** ✅
  - [x] Badge no ícone de sino (navbar) se há activities overdue
  - [x] Cor vermelha no card do pipeline se tem activities overdue

---

### 5.12.6 Sistema de Email por Utilizador (Chatter) ✅ COMPLETO

Envio de emails a clientes directamente a partir do chatter de qualquer registo (Lead, futuramente Compras, Vendas, etc.). Cada utilizador configura as suas próprias credenciais SMTP no perfil.

**Arquitectura:**
- `UserEmailConfig` (accounts) — credenciais por utilizador (email, App Password Fernet-encriptada, provedor Gmail/Outlook)
- `ChatterMessage` (core) com `message_type='EMAIL'` + `GenericForeignKey` — registo central de todos os emails, reutilizável em qualquer módulo
- `apps/core/email_utils.py` — lógica de envio + encriptação Fernet
- `send_email_for_record(user, record, ...)` — API pública de envio

**Backend — ✅ COMPLETO:**
- [x] Instalar `cryptography` (Fernet encryption)
- [x] `FERNET_KEY` em `settings.py` (via `.env`)
- [x] `apps/core/email_utils.py` — `encrypt_password`, `decrypt_password`, `_send_via_smtp`, `send_email_for_record`
- [x] `_send_via_smtp` suporta anexos (`MIMEMultipart('mixed')` + `MIMEBase` + `encode_base64`)
- [x] `_send_via_smtp` suporta CC, BCC (header `Cc:` + RCPT list completo)
- [x] `_send_via_smtp` suporta múltiplos destinatários no "Para:" (vírgula-separados)
- [x] `send_email_for_record` aceita `cc=''` e `bcc=''`
- [x] `UserEmailConfig` model em `apps/accounts/models.py` (migration accounts 0004 aplicada)
- [x] Campos de threading em `ChatterMessage`: `direction`, `from_email`, `message_id`, `in_reply_to` (migration core 0015 aplicada)
- [x] Campo `cc_emails` em `ChatterMessage` (já existia)
- [x] Campo `bcc_emails` em `ChatterMessage` (migration core 0016 aplicada)
- [x] `lead_send_email` view — aceita `multipart/form-data`: `body`, `to_email` (vírgulas OK), `cc`, `bcc`, `attachments` (múltiplos ficheiros)
- [x] `lead_send_email` — grava ficheiros em `media/chatter/<lead_id>/` via `default_storage`
- [x] `lead_send_email` — devolve registo completo (`cc_emails`, `bcc_emails`, `attachments`) para atualizar UI
- [x] `lead_emails_list` view — devolve `cc_emails` e `bcc_emails` em cada registo
- [x] URLs em `apps/crm/urls.py`: `/crm/leads/<uuid>/emails/send/`, `/crm/leads/<uuid>/emails/`
- [x] `profile_settings` view — GET/POST, `get_or_create UserEmailConfig`, encripta password na gravação
- [x] `test_smtp` view — envia email de teste para verificar credenciais
- [x] URLs em `apps/accounts/urls.py`: `/accounts/perfil/`, `/accounts/perfil/testar-smtp/`
- [x] `UserEmailConfig` registado no admin com `has_smtp_configured` boolean
- [x] Link "Meu Perfil" no navbar aponta para `/accounts/perfil/`
- [x] `has_smtp` passado no contexto da view de detalhe de lead

**Frontend — ✅ COMPLETO:**
- [x] Template `accounts/profile_settings.html` — form de configuração SMTP por utilizador
- [x] Aba "Enviar Mensagem" no chatter da lead (`lead_create.html`) — chat estilo WhatsApp
- [x] Bubbles: outbound alinhadas à direita, cor dourada primária semi-transparente (`rgba(219,198,147,0.22)`) com borda dourada e texto branco
- [x] Bubbles: inbound alinhadas à esquerda, fundo `bg-gray-700`
- [x] Cada bubble mostra: corpo da mensagem, chips de anexos (clicáveis), ⓘ botão info + "Para/De: email • hora"
- [x] Modal de detalhes do email (ⓘ) — mostra Assunto, De, Para, CC, BCC, Data, Enviado por, Anexos
- [x] Campo "Para:" editável, pré-preenchido com `lead.email_from`, suporta múltiplos emails (vírgula)
- [x] Botões CC / BCC — expandem campos adicionais com suporte a múltiplos emails (vírgula)
- [x] Botão de anexar ficheiros (paperclip) — chips removíveis antes de enviar
- [x] Textarea com Ctrl+Enter para enviar
- [x] Botão enviar dourado (cor primária), desativado sem SMTP ou sem conteúdo
- [x] Scroll automático para a última mensagem
- [x] Aviso amarelo no chatter se utilizador não tem SMTP configurado (com link para perfil)
- [x] Estado vazio e spinner de loading
- [x] Alpine.js `leadEmailPanel(leadId, leadEmail, leadTitle, hasSMTP)` — `load()`, `send()`, `openDetail()`, `closeDetail()`, `addFiles()`, `removeFile()`, `fileIcon()`, `fileSize()`, `fmtDate()`
- [x] Teste real com utilizador `cubix` → email enviado com sucesso (Message-ID confirmado)

**IMAP Polling (inbound) — ✅ COMPLETO:**
- [x] ✅ Celery task periódica `poll_imap_replies_for_user` em `config/tasks.py`
- [x] ✅ `poll_imap_replies_for_user(config, known_message_ids)` em `email_utils.py` — liga via IMAP SSL, itera INBOX com SINCE 30 dias, match por `In-Reply-To`/`References`
- [x] ✅ View `lead_poll_inbox` em `crm/views.py` — endpoint manual de polling para uma lead específica
- [x] ✅ URL `/crm/leads/<uuid>/emails/poll/`
- [x] ✅ Botão "↻ Verificar respostas" no chatter que chama o endpoint e append
- [x] ✅ Cria `ChatterMessage` com `direction='inbound'` para cada email novo encontrado
- [x] ✅ De-duplicação por `message_id` — evita duplicados em polls consecutivos
- [x] ✅ Validação: só aceita emails cujo `In-Reply-To`/`References` bate com os Message-IDs outbound da lead
- [x] ✅ Thread headers `In-Reply-To` + `References` adicionados ao envio SMTP (`_send_via_smtp`)
- [x] ✅ `lead_send_email` constrói thread refs a partir de mensagens anteriores da lead

---

### 5.12.7 Email Templates — Gestão no Dashboard ✅ COMPLETO

Sistema completo de gestão de templates de email no painel de administração. Os templates são reutilizáveis por módulo (CRM, Contactos, Vendas, etc.) e suportam variáveis dinâmicas com um builder visual estilo WhatsApp.

**Arquitectura:**
- Modelo `EmailTemplate` — nome, assunto, body HTML, módulo, idioma, tipo (BASE/CUSTOM), placeholders JSON
- Modelo `EmailTemplateAttachment` — anexos estáticos ou relatórios dinâmicos (modelo criado, UI pendente)
- Modelo `EmailLayout` — envelope HTML global que envolve todos os emails (ver 5.12.13)
- Cada template BASE tem um ficheiro default em `templates/emails/defaults/` para restauração
- Campo `default_body_path` liga o template ao seu ficheiro default
- Templates globais (`owner_company=NULL`) partilhados por todas as empresas
- Proteção: templates BASE não podem ser eliminados, apenas arquivados

---

**Backend — Modelo `EmailTemplate`:**

- [x] Modelo `EmailTemplate` em `apps/core/models.py`
  - [x] Campo `name` (CharField, max_length=255)
  - [x] Campo `subject` (CharField, max_length=500) — suporta `{{N}}` e `{{ field.path }}`
  - [x] Campo `body_html` (TextField) — corpo HTML com placeholders
  - [x] Campo `module` (CharField, choices: CRM, SALES, PURCHASES, INVOICING, CONTACTS, MARKETING, GENERAL)
  - [x] Campo `language` (CharField, choices: pt_PT, pt_BR, en_US, en_GB, fr, es)
  - [x] Campo `template_type` (CharField: BASE / CUSTOM) — proteção de templates do sistema
  - [x] Campo `is_active` (BooleanField, default=True, herdado de AbstractBaseModel)
  - [x] Campo `owner_company` (FK Company, null=True) — NULL = global
  - [x] Campo `created_by` / `updated_by` (FK User)
  - [x] Campo `available_placeholders` (JSONField) — formato: `{"1": {"field": "lead.contact.name", "fallback": "Cliente"}, ...}`
  - [x] Campo `default_body_path` (CharField) — caminho relativo para ficheiro default (ex: `defaults/crm_thankyou.html`)
  - [x] `__str__` → `f'{name} ({module})'`
  - [x] UniqueConstraint: nome único por empresa + nome único global
  - [x] Migration 0025 (modelo base) + 0026 (owner nullable) + 0027 (template_type) + 0028 (default_body_path)

- [x] Métodos de instância em `EmailTemplate`
  - [x] `get_default_body()` — lê conteúdo do ficheiro default
  - [x] `has_default_body()` — verifica se tem ficheiro default
  - [x] `reset_body_to_default(user)` — restaura body_html para o default

- [x] Modelo `EmailTemplateAttachment` em `apps/core/models.py`
  - [x] Campo `attachment_type` (STATIC / REPORT)
  - [x] Campo `file` (FileField, upload_to email_templates/attachments/)
  - [x] Campo `report_type` (choices: QUOTE, INVOICE, PURCHASE_ORDER, DELIVERY_NOTE) — futuro
  - [x] Campo `filename` (CharField) — nome do ficheiro no email
  - [x] FK `template` → EmailTemplate (CASCADE)

- [x] Admin registado — `EmailTemplateAdmin` + `EmailTemplateAttachmentInline`
  - [x] `list_display`, `list_filter`, `search_fields`
  - [x] Inline tabular para anexos

---

**Backend — Views (Dashboard `apps/dashboard/views.py`):**

- [x] `email_template_list_view` — GET `/dashboard/settings/email-templates/`
  - [x] Pesquisa por nome/assunto
  - [x] Filtro por módulo
  - [x] Filtro por tipo (BASE/CUSTOM)
  - [x] Toggle ativos/arquivados
  - [x] Paginação
  - [x] Checkboxes para ações em bulk

- [x] `email_template_create_view` — GET/POST `/dashboard/settings/email-templates/new/`
  - [x] Formulário completo (nome, módulo, idioma, tipo, assunto, body, placeholders)
  - [x] Body começa vazio (não pré-preenchido com default)
  - [x] `created_by` = utilizador atual

- [x] `email_template_edit_view` — GET/POST `/dashboard/settings/email-templates/<uuid>/edit/`
  - [x] Formulário com dados existentes
  - [x] `updated_by` = utilizador atual

- [x] `email_template_reset_body_view` — POST `/dashboard/settings/email-templates/<uuid>/reset-body/`
  - [x] Restaura body_html para o conteúdo do ficheiro default
  - [x] Só funciona se template tiver `default_body_path`

- [x] `email_template_bulk_archive` — POST (arquivar templates selecionados)
  - [x] Protege templates BASE de serem eliminados
- [x] `email_template_bulk_unarchive` — POST (reativar templates arquivados)
- [x] `email_template_bulk_delete` — POST (eliminar templates CUSTOM selecionados)

- [x] URLs em `apps/dashboard/urls.py`
  - [x] 7 rotas: list, create, edit, reset-body, bulk-archive, bulk-unarchive, bulk-delete

---

**Frontend — Lista de Templates (`email_template_list.html`):**

- [x] Tabela dark-theme com colunas: checkbox, nome, módulo, tipo (badge), idioma, assunto, ações
- [x] Campo de pesquisa por nome/assunto
- [x] Filtros por módulo e tipo
- [x] Toggle ativo/arquivado
- [x] Paginação
- [x] Ações em bulk: arquivar, restaurar, eliminar (com confirmação)
- [x] Botão "Novo Template" → formulário de criação

---

**Frontend — Formulário de Template (`email_template_form.html`):**

- [x] Campos: nome, módulo, idioma, tipo, assunto
- [x] **Aba "Editor HTML"** — Ace Editor (tema Dracula) para editar body_html
- [x] **Aba "Placeholders"** — Builder visual estilo WhatsApp
  - [x] Tabela interactiva com 4 colunas: Var (`{{N}}`), Campo (input + autocomplete), Fallback, Variável (`{{ field.path }}`)
  - [x] Auto-increment do número da variável (nunca renumera, como auto-increment de DB)
  - [x] `_FIELD_MAP` com campos por módulo: CRM (23 campos), CONTACTS (17 campos), GENERAL (4 campos)
  - [x] Dropdown autocomplete com pesquisa ao digitar no campo
  - [x] Botão copiar na coluna Variável (copia `{{ field.path }}` para clipboard)
  - [x] Modal de ajuda "Como usar" com instruções
  - [x] Sync automático para hidden textarea (JSON serializado)
- [x] **Aba "Pré-visualização"** — preview do email compilado
  - [x] Renderiza body_html com layout (envelope) aplicado
  - [x] Resolve `{{N}}` e `{{ field.path }}` usando fallbacks/samples da tabela de variáveis
  - [x] Botão "Restaurar Default" (só para templates com default_body_path)
- [x] Fix: `{{ layout_html }}` com filtro `|safe` no `<script type="text/plain">`
- [x] Fix: Django template escaping em Alpine x-text — helpers `shortVar()`/`fullVar()` dentro de `{% verbatim %}`

---

**Default Bodies:**

- [x] Ficheiro `templates/emails/defaults/crm_thankyou.html` — template default "Email de Agradecimento" (CRM)
- [x] Usa variáveis `{{1}}`, `{{2}}` em vez de nomes longos
- [x] Ficheiro `templates/emails/base_layout.html` — HTML default do layout/envelope

---

**Seeds:**

- [x] `scripts/seed_email_templates.py` — cria template "Email de Agradecimento" (CRM) com placeholders no novo formato
- [x] `scripts/seed_email_layout.py` — seed do layout global a partir de `base_layout.html`

---

### 5.12.8 Email Threading (In-Reply-To / References) ✅ COMPLETO

Assegurar que todos os emails enviados a partir do chatter fazem parte do mesmo thread, para que o cliente veja uma só conversão no Gmail/Outlook.

- [x] Campo `in_reply_to` em `ChatterMessage` (migration 0015)
- [x] `_send_via_smtp` adiciona headers `In-Reply-To` e `References` ao MIME
- [x] `send_email_for_record` aceita `in_reply_to` e `references` como parâmetros opcionais
- [x] `lead_send_email` constrói thread refs lendo os `message_id` de todos os emails anteriores da lead
- [x] Thread testado em produção — replies aparecem agrupados no Gmail

---

### 5.12.9 IMAP Polling — Emails Inbound do Cliente ✅ COMPLETO

Detalhes no final de 5.12.6 acima. Resumo de pontos-chave:

- [x] `poll_imap_replies_for_user` — IMAP via SSL (port 993), auth com App Password encriptada
- [x] Celery beat task `poll_all_imap_inboxes` (corre a cada 5 minutos)
- [x] Endpoint manual `lead_poll_inbox` para polling on-demand
- [x] Botão "↻ Verificar respostas" no chatter, atualiza bubbles em tempo real
- [x] Validação de threading por `In-Reply-To`/`References` antes de aceitar mensagem

---

### 5.12.10 HTML Email — Editor Quill + Renderização de Bubbles ✅ COMPLETO

Permite compor emails formatados (negrito, itálico, listas, links, imagens) e renderizar HTML inbound nas bubbles do chatter.

**Backend:**
- [x] Campo `body_html` (`TextField`, blank, default='') em `ChatterMessage` (migration 0017)
- [x] `_parse_email_html(msg)` em `email_utils.py` — extrai parte `text/html` de MIME multipart
- [x] `_strip_quoted_html(html)` — remove blocos `div.gmail_quote`, `div.gmail_attr`, `blockquote[type=cite]`, Outlook `divRplyFwdMsg`, etc.
- [x] `poll_imap_replies_for_user` retorna `body_html` já limpo de quotes
- [x] `send_email_for_record` guarda `body_html` em `ChatterMessage`
- [x] `lead_send_email` aceita `body_html` via POST e devolve no response
- [x] `lead_emails_list` devolve `body_html` em cada registo
- [x] `lead_poll_inbox` guarda e devolve `body_html`

**Frontend:**
- [x] CSS dark-theme para `#quill-email-editor` (toolbar, editor, pickers, placeholders)
- [x] CSS `.email-body` — imagens, links, parágrafos, listas, bold/italic
- [x] Botão ⛶ (expand) no canto inferior direito da textarea — abre modal Quill
- [x] Modal Quill Gmail-style: cobre toda a área do chatter, campos To/CC/BCC, editor Quill, footer com anexos + Descartar + Enviar
- [x] Bubbles: `x-text` → `x-html` com `renderBody(em)` — usa `body_html` se existir, fallback para plain text escapado
- [x] `renderBody(em)` sanitiza `<script>` tags antes de renderizar
- [x] `openCompose()` — inicializa Quill lazy, pré-preenche com `this.body`
- [x] `sendFromModal()` — lê `quillModal.root.innerHTML`, chama `send(bodyHtml)`
- [x] Fix: reset do Quill via `root.innerHTML` antes de esconder (evita crash `null offset`)

---

### 5.12.11 Strip de Quotes em Emails Inbound ✅ COMPLETO

Remover o historial da thread (texto quotado) dos emails inbound, guardando apenas a nova mensagem do cliente.

- [x] `_strip_quoted_reply(body)` — plain text: corta em `escreveu (data):`, `On ... wrote:`, `---Original Message---`, `___`, `> `
- [x] `_strip_quoted_html(html)` — HTML: corta em `div.gmail_quote`, `div.gmail_attr`, `blockquote[type=cite]`, `divRplyFwdMsg`, `hr#stopSpelling`
- [x] Aplicado automaticamente em `_parse_email_html()` e `_parse_email_body()`
- [x] Script de retrocompat.: `_strip_quoted_html` reaplicado a mensagens já guardadas na DB

---

### 5.12.12 ChatterFollower — Sistema de Seguidores Genérico ✅ COMPLETO

Qualquer utilizador pode seguir qualquer registo do sistema (Lead, futuramente Venda, Compra, etc.). Ao chegar um email inbound, todos os seguidores recebem uma notificação interna.

**Arquitectura:**
- `ChatterFollower` (core.models) — `content_type` + `object_id` (ContentType genérico) + `user` FK
- `unique_together` impede duplicados
- `notify_followers(obj, type, title, message, link)` — helper que cria `Notification` em bulk para todos os seguidores
- Para usar noutro módulo: `ChatterFollower.objects.get_or_create(content_type=..., object_id=sale.id, user=user)`

**Backend:**
- [x] Modelo `ChatterFollower` em `apps/core/models.py` (migration 0018)
- [x] `notify_followers()` helper — `bulk_create` para performance
- [x] `lead_followers_api` (GET/POST) — lista seguidores + adiciona
- [x] `lead_follower_remove_api` (DELETE) — remove seguidor
- [x] URLs `/crm/leads/<uuid>/followers/` e `/crm/leads/<uuid>/followers/<uuid>/remove/`
- [x] Auto-follow no GET de followers: `lead.assigned_to` + utilizador atual são subscritos automaticamente
- [x] `lead_poll_inbox` — após guardar email inbound, chama `notify_followers()` com preview do corpo
- [x] `ChatterFollowerAdmin` registado no Django admin

**Frontend:**
- [x] Widget de seguidores no header das tabs do chatter (direita)
- [x] Stack de avatares (iniciais) dos seguidores atuais
- [x] Botão `+` — abre dropdown com lista de seguidores + input de pesquisa
- [x] Input de pesquisa com debounce 250ms — usa endpoint `/crm/api/users/search/` existente
- [x] Adicionar seguidor: click no resultado — POST + append ao stack
- [x] Remover seguidor: botão ✗ na lista — DELETE + remove do stack
- [x] `leadFollowersWidget(leadId)` Alpine.js function isolada (não acoplada ao `leadEmailPanel`)
- [x] Ao abrir a lead, vendedor e utilizador atual são auto-subscritos (sem intervenção manual)

---

### 5.12.13 Email Layout (Envelope Global) ✅ COMPLETO

Layout HTML global (envelope) que envolve todos os emails enviados pelo sistema. Registo único — sem FK de empresa.

**Backend:**
- [x] Modelo `EmailLayout` em `apps/core/models.py` (migration 0024)
  - [x] Campo `html_content` (TextField) — HTML do envelope com placeholders Django template
  - [x] Campo `updated_by` (FK User)
  - [x] `get_layout()` — classmethod que devolve o layout global
  - [x] `reset_to_default(user)` — restaura a partir de `templates/emails/base_layout.html`

- [x] Admin registado — `EmailLayoutAdmin`
  - [x] Registo único (impede criar duplicados)

- [x] `wrap_email_with_layout(body_html)` em `apps/core/email_utils.py`
  - [x] Carrega o `EmailLayout` global
  - [x] Insere o `body_html` no placeholder `{{ body }}` do envelope
  - [x] Usa Django `Template` + `Context` para renderizar

- [x] Views no Dashboard (`apps/dashboard/views.py`)
  - [x] `email_layout_view` — GET/POST `/dashboard/settings/email-layout/`
  - [x] `email_layout_reset_view` — POST reset para default

- [x] URLs: `settings/email-layout/`, `settings/email-layout/reset/`

**Frontend (`email_layout.html`):**
- [x] Ace Editor (tema Dracula) para editar o HTML do envelope
- [x] Pré-visualização ao vivo do layout
- [x] Botão "Restaurar Default" com confirmação

**Seeds:**
- [x] `scripts/seed_email_layout.py` — cria layout global a partir de `base_layout.html`
- [x] Ficheiro default `templates/emails/base_layout.html`

---

### 5.12.14 Template Compiler — Motor Central de Variáveis ✅ COMPLETO

Compilador central que resolve as variáveis `{{N}}` e `{{ field.path }}` nos templates de email a partir dos dados reais do registo (Lead, Contacto, etc.). Reutilizável em todos os módulos.

- [x] Módulo `apps/core/template_compiler.py` criado
  - [x] `_resolve_field(obj, field_path)` — traversa dot notation em modelos Django (ex: `contact.company.name`)
  - [x] `_resolve_field_with_root(record, field_path)` — strip do prefixo do modelo root (ex: `lead.title` numa Lead → resolve `title`)
  - [x] `_build_var_map(placeholders, record)` — constrói mapa de substituição a partir do `available_placeholders` do template
  - [x] `_substitute_vars(text, var_map)` — substituição regex para ambos os formatos (`{{1}}` e `{{ lead.title }}`)
  - [x] `compile_email_template(template, record, user, extra_context)` — API principal, devolve `{subject, body_html, var_map}`
  - [x] `compile_text(text, placeholders, record, extra_context)` — compilação genérica de texto
  - [x] Suporte para variáveis do utilizador: `user.first_name`, `user.last_name`, `user.email`
  - [x] Suporte para `extra_context` — variáveis adicionais passadas manualmente
  - [x] Fallback automático: se campo não resolver, usa o fallback definido no placeholder
  - [x] Regex patterns: `_RE_SHORT_VAR` para `{{N}}`, `_RE_FULL_VAR` para `{{ path }}`

- [x] Testes unitários em `test/auto/test_template_compiler.py` — **25 testes, todos passam**
  - [x] `TestResolveField` (6 testes) — campo simples, nested, deep nested, None, inexistente, null FK
  - [x] `TestResolveFieldWithRoot` (4 testes) — com/sem prefixo root, nested, deep nested
  - [x] `TestBuildVarMap` (4 testes) — formato novo, fallback em null, vazio, sem record
  - [x] `TestSubstituteVars` (5 testes) — short vars, full vars, mixed, unresolved kept, empty
  - [x] `TestCompileEmailTemplate` (4 testes) — compilação completa, user vars, extra context, fallbacks
  - [x] `TestCompileText` (2 testes) — texto simples, com extra context

---

### 5.12.15 Email Template — Aba Anexos 🔴 NÃO IMPLEMENTADO

Adicionar a aba "Anexos" ao formulário de template de email no Dashboard. O modelo `EmailTemplateAttachment` já existe, mas a interface de upload ainda não foi implementada.

**Backend:**
- [x] Modelo `EmailTemplateAttachment` já existe (migration 0025)
- [ ] View para upload de anexo — `POST /dashboard/settings/email-templates/<uuid>/attachments/`
- [ ] View para remover anexo — `DELETE /dashboard/settings/email-templates/<uuid>/attachments/<uuid>/`
- [ ] View para listar anexos — `GET` (devolvido no contexto do form)
- [ ] Validação de tamanho máximo de ficheiro (ex: 10MB)
- [ ] Validação de tipos de ficheiro permitidos (PDF, imagens, DOCX, XLSX)

**Frontend (aba "Anexos" no `email_template_form.html`):**
- [ ] Nova aba "Anexos" ao lado de "Editor HTML", "Placeholders" e "Pré-visualização"
- [ ] Zona de drag & drop para upload de ficheiros
- [ ] Lista de anexos existentes com: nome, tamanho, tipo, botão remover
- [ ] Upload via AJAX (sem reload da página)
- [ ] Indicador de progresso durante upload
- [ ] Preview de imagens inline (thumbnails)
- [ ] Ícones por tipo de ficheiro (PDF, imagem, documento)
- [ ] Campo para renomear o ficheiro (nome com que será enviado no email)
- [ ] Aviso se total de anexos exceder limite

**Integração com envio:**
- [ ] `compile_email_template()` devolve lista de anexos a incluir
- [ ] `send_email_for_record()` anexa ficheiros ao MIME multipart
- [ ] Suporte para `filename` com placeholders (ex: `orcamento_{{1}}.pdf`)

**Testes:**
- [ ] Test: upload de ficheiro estático funciona
- [ ] Test: remoção de anexo funciona
- [ ] Test: validação de tamanho rejeita ficheiros grandes
- [ ] Test: anexos são incluídos no email enviado

---

### 5.12.16 Email Template Picker no Chatter ✅ COMPLETO

Botão no compose modal do chatter (Quill) que permite ao utilizador escolher um email template pré-definido e aplicar automaticamente o assunto e corpo ao email.

**Backend:**
- [x] View `lead_email_templates` em `apps/crm/views.py` — GET `/crm/leads/<uuid>/email-templates/`
  - [x] Filtra templates do módulo CRM + GENERAL, ativos
  - [x] Resolve placeholders usando `compile_email_template()` para cada template
  - [x] Retorna JSON: `[{id, name, subject, body_html}]`
- [x] URL em `apps/crm/urls.py` — `leads/<uuid:lead_id>/email-templates/`

**Frontend (em `templates/crm/lead_create.html`):**
- [x] Botão de template (ícone documento) no footer do compose modal Quill
- [x] Dropdown picker com lista de templates disponíveis
- [x] `loadTemplates()` — fetch lazy ao abrir (cache após 1ª chamada)
- [x] `applyTemplate(tpl)` — preenche subject + seta `quillModal.root.innerHTML`
- [x] Estado Alpine: `showTemplatePicker`, `emailTemplates`, `loadingTemplates`
- [x] Fix: cor do texto do botão "Enviar" — `text-gray-900` → `text-white` (modal + inline)

**Seeds:**
- [x] 3 novos templates criados via `seed_email_templates.py`: Boas-vindas, Follow-up, Enviar Proposta
- [x] Ficheiros default: `crm_welcome.html`, `crm_followup.html`, `crm_proposal.html`

---

### 5.12.17 Email Layout — Correções de Renderização ✅ COMPLETO

Correções ao envelope de email (`EmailLayout`) para que o body HTML, logo, título e links renderizem corretamente.

- [x] **Body HTML não renderizava** — `body_content` passado sem `mark_safe()` → Django auto-escapava tags HTML. Corrigido em `wrap_email_with_layout()`.
- [x] **Logo da empresa não aparecia** — URLs localhost não acessíveis por clientes de email. Implementado CID inline image (`cid:company_logo`) via `MIMEImage` no MIME `multipart/related`.
  - [x] `wrap_email_with_layout()` agora retorna tupla `(html, inline_images)` com logo bytes
  - [x] `_send_via_smtp()` aceita `inline_images` e reestrutura MIME: `mixed → related → alternative + CID images`
  - [x] `send_email_for_record()` desempacota tupla e passa `inline_images`
- [x] **Título da lead truncado** — Removida truncação de 40 chars em `_get_record_label()` + `white-space: nowrap` → `max-width: 200px; word-wrap: break-word`
- [x] **Email do remetente em azul** — Cor default dos links. Adicionado `<a style="color: #dbc693">` no footer do layout.
- [x] **Iniciais do avatar escuras** — `color: #1f2937` → `color: #ffffff` no `sender_initials` TD do `base_layout.html`.
- [x] DB layout resetado via `EmailLayout.reset_to_default()`

---

## 5.13 Sistema de Prospectos (Pré-Pipeline) ✅ COMPLETO

Criar vista dedicada para leads não qualificadas (prospectos) que ainda não entraram no pipeline principal. Permite qualificar manualmente cada prospecto antes de o promover.

**Conceito:**
- `Lead.is_prospect = True` → o registo existe mas não aparece no pipeline Kanban nem na lista de leads
- Vista separada `/crm/prospects/` lista apenas prospectos ativos
- Ação de conversão `convert_prospect_to_lead` promove o prospecto para lead real (seta `is_prospect=False`)
- Funcionalidade pode ser ativada/desativada via `CRMSettings.prospects_enabled`

**Backend:**
- [x] Campo `is_prospect` (BooleanField, default=False) adicionado ao modelo `Lead` em `apps/crm/models.py`
- [x] `prospects_list_view` — lista leads com `is_prospect=True`, filtradas por company, com search e paginação
- [x] `prospect_detail_view` — detalhe do prospecto (reutiliza template de lead mas em modo prospecto)
- [x] `convert_prospect_to_lead` — POST endpoint que seta `is_prospect=False` e redireciona para o pipeline
- [x] Bulk actions: `bulk_archive_prospects`, `bulk_unarchive_prospects`, `bulk_qualify_prospects`, `bulk_delete_prospects`
- [x] Pipeline e Lead List excluem automaticamente prospectos (`is_prospect=False`)

**URLs:**
- [x] `path('prospects/', views.prospects_list_view, name='prospects_list')`
- [x] `path('prospects/<uuid:lead_id>/', views.prospect_detail_view, name='prospect_detail')`
- [x] `path('prospects/<uuid:lead_id>/convert/', views.convert_prospect_to_lead, name='prospect_convert')`
- [x] Bulk actions registadas

**Frontend:**
- [x] `templates/crm/prospects_list.html` — lista de prospectos com bulk actions e search
- [x] Link "Prospectos" no navbar CRM (dropdown Configuração ou link direto)
- [x] Command palette: rota "CRM / Prospectos" adicionada

---

## 5.14 Campos de Qualificação no Modelo Lead (closed_at + lost_reason_category) ✅ COMPLETO

Adicionar campos de rastreio de encerramento e categorização de razão de perda ao modelo `Lead`, necessários para os relatórios e análise de funil.

**Campos adicionados:**
- [x] `closed_at` (DateTimeField, null=True, blank=True) — data/hora em que a lead foi ganha ou perdida
  - [x] Auto-preenchido no `Lead.save()` quando stage muda para won/lost
  - [x] Limpo automaticamente se lead for movida de volta para um stage normal
- [x] `lost_reason_category` (CharField, choices, blank=True) — categoria da razão de perda:
  - `PRICE` — Preço
  - `LOST_TO_COMPETITION` — Perdido para concorrente
  - `NOT_INTERESTED` — Sem interesse
  - `TOO_EARLY` — Demasiado cedo
  - `OTHER` — Outro

**Migration:**
- [x] Migration criada e aplicada (`apps/crm/migrations/`)

**Uso:**
- [x] `closed_at` usado no relatório de funil e gráfico Ganhas vs Perdidas (com filtro de período)
- [x] `lost_reason_category` usado no gráfico "Motivos de Perda" no dashboard de relatórios

---

## 5.15 Filtro de Idade no Pipeline (Age Filter) ✅ COMPLETO

Adicionar filtro de "idade máxima das leads" ao pipeline Kanban, permitindo ver apenas leads criadas nos últimos N dias/meses e evitar acumulação de leads antigas no board.

**Backend:**
- [x] Parâmetro GET `?age=` na `lead_pipeline_view` com opções: `1` (1 ano, default), `3` (3 anos), `all` (todas)
- [x] Mapeamento `age_days_map` com os valores em dias: `{'1': 365, '3': 1095, 'all': None}`
- [x] Filtro aplicado ao queryset principal de leads no pipeline

**Frontend:**
- [x] Dropdown ou controlo de filtro de idade no topo do pipeline em `templates/crm/lead_pipeline.html`
- [x] Parâmetro `?age=` mantido nos links de paginação e filtros existentes

---

## 5.16 CRMSettings — Configurações do Módulo CRM ✅ COMPLETO

Criar modelo singleton de configurações para o módulo CRM, com flags para ativar/desativar funcionalidades avançadas por empresa.

**Modelo `CRMSettings` em `apps/crm/models.py`:**
- [x] Herda de `BaseModel`
- [x] Campo `owner_company` (FK para Company) — configurações por empresa
- [x] Campo `predictive_scoring` (BooleanField, default=False) — ativa Pontuação Preditiva de Leads
- [x] Campo `prospects_enabled` (BooleanField, default=False) — ativa fase de prospectos
- [x] Campo `auto_generate_leads` — configuração para geração automática de leads
- [x] Migration criada e aplicada

**Página de Definições (`templates/dashboard/settings.html`) — Secção CRM:**
- [x] Layout 2 colunas (`xl:grid-cols-2`) com cards individuais por grupo de definições
- [x] Coluna esquerda: **Pontuação Preditiva de Leads** — toggle + botão "Recalcular"
- [x] Coluna direita (empilhados): **Prospectos** (toggle) + **Geração Automática de Leads** (select + botão "Gerar Leads")
- [x] Cada grupo tem card com border `border-gray-800 bg-gray-900/20`

---

## 5.17 Dashboard de Relatórios CRM ✅ COMPLETO

Criar página de relatórios dedicada para o módulo CRM com KPIs em tempo real e 6 gráficos interativos baseados em Chart.js.

**URL:** `/crm/reports/` → `crm:crm_reports`

**Backend — `crm_reports_view` em `apps/crm/views.py`:**
- [x] 4 KPI cards calculados: Total de Leads, Total de Vendas Ganhas, Taxa de Conversão (%), Receita Prevista
- [x] 6 datasets para os gráficos:
  - [x] **Funil de Conversão** — contagem de leads por stage
  - [x] **Ganhas vs Perdidas** — histórico mensal dos últimos 12 meses (usa `closed_at`)
  - [x] **Leads por Responsável** — distribuição por `assigned_to`
  - [x] **Forecast** — receita esperada por mês (leads ativas × probability)
  - [x] **Leads por Fonte** — distribuição por `source`
  - [x] **Top Motivos de Perda** — distribuição por `lost_reason_category`
- [x] `django.contrib.humanize` adicionado a `INSTALLED_APPS` (necessário para `|intcomma`)

**Frontend — `templates/crm/reports.html`:**
- [x] Sub-navbar via `{% block sub_navbar %}{% include 'components/crm_navbar_simple.html' %}{% endblock %}`
- [x] Header com título e badge "Dados em tempo real"
- [x] 4 cards de KPI no topo
- [x] 6 cards de gráfico em grelha 3×2 com Chart.js 4.4.4 (tema dark)
- [x] Botão ⓘ em cada card de gráfico que abre modal informativo (o que é, como comparar, fórmula)
- [x] Modal informativo: vanilla JS puro (`chartInfoOpen()`, `chartInfoClose()`, Escape + backdrop)
- [x] Dropdown "Relatórios" no navbar CRM com label "Dashboard"
- [x] Command palette: rota "CRM / Relatórios" adicionada

---

**FIM DAS TAREFAS FUTURAS**

---

# 🚀 FASE 6: APP - INVENTÁRIO (PRODUTOS E STOCK)

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de gestão de produtos e stock básico
**📦 Dependências:** Fase 3 (base models), Fase 4 (contacts para suppliers)

---

## 6.1 Criação da App 'inventory' ✅

Criar app Django para gestão de inventário.

- [x] **Criar app**
  - [x] Executar `python manage.py startapp inventory apps/inventory`
  - [x] Adicionar 'apps.inventory' ao INSTALLED_APPS

- [x] **Criar estrutura de arquivos**
  - [x] Criar models.py, views.py, forms.py, urls.py

---

## 6.2 Modelo Category ✅

Criar categorias para produtos.

- [x] **Criar modelo Category**
  - [x] Herdar de BaseModel
  - [x] Campos: name, description, parent (self FK para subcategorias)
  - [x] Campo: **owner_company** (FK para Company, null=True, blank=True) - NULL=global, com valor=privado
  - [x] Método __str__
  - [x] Filtrar por owner_company na CategoryListView usando filter_by_company()
  - [x] Auto-preencher owner_company na create view com get_active_company()

- [x] **Criar migrations**
  - [x] makemigrations e migrate

- [x] **Registrar no Admin**
  - [x] Criar CategoryAdmin com list_display

- [x] **Testing - Category**
  - [x] Test: criar categoria funciona
  - [x] Test: hierarquia de categorias funciona

---

## 6.2.1 Dashboard de Inventário ✅

Criar dashboard premium com cards de operações e sub-navbar de inventário.

- [x] **Criar dashboard principal**
  - [x] View `inventory_dashboard` com KPIs placeholder
  - [x] Template `inventory_dashboard.html` com layout dark premium
  - [x] 5 operation cards: Recepções, Entregas, Erros, Operações Hoje, Pendentes
  - [x] CSS sparklines (barras semanais) em cada card
  - [x] Rota: `path('', inventory_dashboard, name='inventory_dashboard')`

- [x] **Criar sub-navbar de inventário**
  - [x] Template `components/inventory_navbar.html`
  - [x] Menus: Dashboard, Operações (dropdown), Produtos (dropdown com Categorias), Relatórios, Configuração (dropdown)
  - [x] Links funcionais para dashboard e category_list

---

## 6.2.2 Lista de Categorias de Produtos ✅

Criar página de listagem de categorias com pesquisa, paginação e ações em massa.

- [x] **Criar view `category_list`**
  - [x] Pesquisa por nome, descrição, categoria pai
  - [x] Filtro por status (ativas/arquivadas)
  - [x] Paginação com page_size configurável
  - [x] `filter_by_company()` aplicado
  - [x] `select_related('parent', 'owner_company')` + `annotate(children_count)`

- [x] **Criar template `category_list.html`**
  - [x] Tabela com colunas: checkbox, Nome, Categoria Pai, Descrição, Subcategorias
  - [x] Barra de pesquisa com dropdown de campo
  - [x] Paginação completa
  - [x] Versão mobile responsive
  - [x] Botão "Novo" → link para category_create
  - [x] Click na linha → navega para category_edit

- [x] **Ações em massa (bulk actions)**
  - [x] Checkbox select all / individual
  - [x] Alpine.js `selectedItems` tracking
  - [x] View `bulk_archive_categories` (POST JSON, set is_active=False)
  - [x] View `bulk_unarchive_categories` (POST JSON, set is_active=True)
  - [x] View `bulk_delete_categories` (POST JSON, CASCADE delete)
  - [x] Modal de confirmação para delete
  - [x] Notificações toast (success/error/warning)
  - [x] Rotas: `bulk-archive/`, `bulk-unarchive/`, `bulk-delete/`

---

## 6.2.3 Formulário de Categoria (Criar/Editar) ✅

Criar formulário de criação e edição de categorias.

- [x] **Criar `CategoryForm` (Django ModelForm)**
  - [x] Fields: name, description, parent
  - [x] Parent queryset filtrado por company
  - [x] Prevenção de referências circulares (`_get_descendants()`)
  - [x] Empty label: "— Sem categoria pai (raiz) —"

- [x] **Criar navbar dedicado para formulário**
  - [x] Template `components/category_form_navbar.html`
  - [x] Link "Categorias de Produtos" → category_list
  - [x] Botões de ação: Descartar (vermelho) + Guardar (verde)
  - [x] Guardar como `type="submit" form="category-form"`

- [x] **Criar template `category_form.html`**
  - [x] Layout dark `bg-[#1f2937]` consistente com contacts
  - [x] Nome grande `text-3xl font-light` com border-bottom
  - [x] Dropdown de categoria pai com estilo `bg-[#1a2332]`
  - [x] Ícone placeholder (pasta) no lugar do avatar
  - [x] Metadata (datas criação/atualização, contagem subcategorias) no modo edição
  - [x] Validação de erros com bloco visual

- [x] **Criar views**
  - [x] `category_create(request)` — GET/POST, auto-fill owner_company, redirect to edit
  - [x] `category_edit(request, pk)` — GET/POST, get_object_or_404, messages.success
  - [x] Rotas: `categories/create/`, `categories/<uuid:pk>/edit/`

- [x] **Tabs do formulário**
  - [x] Tab "Notas Internas" — textarea para descrição/observações
  - [x] Tab "Produtos" (modo edição) — tabela inline estilo company_edit/utilizadores
  - [x] Alpine.js `categoryProductsTab()` com search, add, remove (placeholder até Product existir)
  - [x] Badge de contagem de produtos no tab header
  - [x] Tab Produtos ativa por defeito no modo edição

---

## 6.2.4 Seed Data - Categorias Demo ✅

Script para popular categorias demo para padaria/pastelaria.

- [x] **Criar script `scripts/seed_product_categories.py`**
  - [x] 92 categorias em hierarquia de 3 níveis
  - [x] Grupos: Matérias-Primas, Produtos Acabados, Embalagem, Decoração, Utensílios & Equipamento
  - [x] Associadas à empresa "Fuet Mágico"
  - [x] Idempotente (verifica existência antes de criar)

---

## 6.2.5 Modelos UoMCategory e UoM ✅

Criar modelos de Categorias de Unidades de Medida e Unidades de Medida com sistema de conversão.

- [x] **Criar modelo UoMCategory**
  - [x] Herdar de AbstractBaseModel (UUID PK, timestamps, is_active)
  - [x] Campos: name, owner_company (FK para Company)
  - [x] Método __str__
  - [x] Meta: ordering = ['name']

- [x] **Criar modelo UoM**
  - [x] Herdar de AbstractBaseModel
  - [x] Campos: name, symbol (max 16), category (FK para UoMCategory)
  - [x] Campos: uom_type (choices: reference/bigger/smaller), factor (Decimal 20,10), rounding (Decimal 12,6)
  - [x] Campo: owner_company (FK para Company)
  - [x] Método `convert_to(qty, target_uom)` para conversão entre unidades
  - [x] Método __str__
  - [x] Meta: ordering = ['category__name', 'name']

- [x] **Criar migrations**
  - [x] makemigrations e migrate

- [x] **Registrar no Admin**
  - [x] UoMCategoryAdmin com list_display
  - [x] UoMAdmin com list_display, list_filter

---

## 6.2.6 Lista de Unidades de Medida ✅

Criar página de listagem de UoMs com pesquisa, paginação e ações em massa.

- [x] **Criar view `uom_list`**
  - [x] Pesquisa por nome, símbolo, categoria
  - [x] Dropdown de campo de pesquisa (Nome, Símbolo, Categoria)
  - [x] Filtro por status (ativas/arquivadas)
  - [x] Paginação com page_size configurável (default 50)
  - [x] `filter_by_company()` aplicado
  - [x] `select_related('category')`

- [x] **Criar template `uom_list.html`**
  - [x] Tabela com colunas: checkbox, Nome, Símbolo, Categoria, Tipo, Factor
  - [x] Barra de pesquisa com dropdown de campo
  - [x] Paginação completa (desktop + mobile)
  - [x] Botão "Novo" → link para uom_create
  - [x] Click na linha → navega para uom_edit
  - [x] Empty state com ícone e mensagem

- [x] **Ações em massa (bulk actions)**
  - [x] Checkbox select all / individual
  - [x] Alpine.js `selectedItems` tracking
  - [x] View `bulk_archive_uoms` (POST JSON, set is_active=False)
  - [x] View `bulk_unarchive_uoms` (POST JSON, set is_active=True)
  - [x] View `bulk_delete_uoms` (POST JSON, CASCADE delete)
  - [x] Modal de confirmação para delete
  - [x] Notificações toast (success/error/warning)
  - [x] Rotas: `uom/bulk-archive/`, `uom/bulk-unarchive/`, `uom/bulk-delete/`

- [x] **Adicionar link na navbar de inventário**
  - [x] "Unidades de Medida" no dropdown Configuração → Produtos

---

## 6.2.7 Formulário de UoM (Criar/Editar) ✅

Criar formulário de criação e edição de unidades de medida.

- [x] **Criar `UoMForm` (Django ModelForm)**
  - [x] Fields: name, symbol, category, uom_type, factor, rounding
  - [x] Category queryset filtrado por company
  - [x] Labels em português

- [x] **Criar navbar dedicado para formulário**
  - [x] Template `components/uom_form_navbar.html`
  - [x] Link "Unidades de Medida" → uom_list
  - [x] Botões: Descartar (vermelho/trash) + Guardar (verde/save)
  - [x] Guardar como `type="submit" form="uom-form"`

- [x] **Criar template `uom_form.html`**
  - [x] Layout dark `bg-[#1f2937]` consistente com contacts
  - [x] Nome grande `text-3xl font-light` com border-bottom
  - [x] Grid 2 colunas: Esquerda (Símbolo, Categoria, Tipo) / Direita (Factor, Arredondamento)
  - [x] Inputs `bg-[#1a2332]` com ícones descritivos
  - [x] Dropdown para Categoria e Tipo
  - [x] Fix localização: `{% load l10n %}` + `|unlocalize` em campos numéricos (pt usa vírgulas)

- [x] **Criar views**
  - [x] `uom_create(request)` — GET/POST, auto-fill owner_company, redirect to edit
  - [x] `uom_edit(request, pk)` — GET/POST, get_object_or_404, messages.success
  - [x] Rotas: `uom/create/`, `uom/<uuid:pk>/edit/`

---

## 6.2.8 Seed Data - Unidades de Medida ✅

Script para popular UoMs demo com 4 categorias e 21 unidades.

- [x] **Criar script `scripts/seed_uom.py`**
  - [x] 4 categorias: Peso, Volume, Unidade, Tempo
  - [x] 21 unidades com factores de conversão corretos
  - [x] Inclui unidades imperiais (Onça, Libra, Galão)
  - [x] Idempotente (get_or_create)
  - [x] Encoding UTF-8 para caracteres portugueses (ç, ú, ã)

---

## 6.2.9 Lista de Categorias de UdM ✅

Criar página de listagem de categorias de unidades de medida.

- [x] **Criar view `uom_category_list`**
  - [x] Pesquisa por nome
  - [x] Filtro por status (ativas/arquivadas)
  - [x] Paginação com page_size configurável (default 50)
  - [x] `filter_by_company()` aplicado
  - [x] `annotate(uom_count=Count('uom'))` para contar UdMs por categoria

- [x] **Criar template `uom_category_list.html`**
  - [x] Tabela com colunas: checkbox, Nome (com ícone), Unidades (badge count)
  - [x] Barra de pesquisa
  - [x] Filtro por status (Ativos/Arquivados)
  - [x] Paginação completa (desktop + mobile)
  - [x] Botão "Novo" → link para uom_category_create
  - [x] Click na linha → navega para uom_category_edit
  - [x] Empty state com ícone e mensagem

- [x] **Ações em massa (bulk actions)**
  - [x] Checkbox select all / individual
  - [x] Alpine.js `selectedItems` tracking
  - [x] View `bulk_archive_uom_categories` (POST JSON)
  - [x] View `bulk_unarchive_uom_categories` (POST JSON)
  - [x] View `bulk_delete_uom_categories` (POST JSON, aviso CASCADE UdMs)
  - [x] Modal de confirmação para delete com checkbox obrigatório
  - [x] Notificações toast
  - [x] Rotas: `uom-categories/bulk-archive/`, `uom-categories/bulk-unarchive/`, `uom-categories/bulk-delete/`

- [x] **Adicionar link na navbar de inventário**
  - [x] "Categorias de UdM" no dropdown Configuração → Produtos, abaixo de "Unidades de Medida"

---

## 6.2.10 Formulário de Categoria de UdM (Criar/Editar) ✅

Criar formulário de criação e edição de categorias de UdM com tab de unidades associadas.

- [x] **Criar `UoMCategoryForm` (Django ModelForm)**
  - [x] Fields: name (único campo)
  - [x] Labels em português

- [x] **Criar navbar dedicado para formulário**
  - [x] Template `components/uom_category_form_navbar.html`
  - [x] Link "Categorias de UdM" → uom_category_list
  - [x] Botões: Descartar (vermelho/trash) + Guardar (verde/save)
  - [x] Guardar como `type="submit" form="uom-category-form"`

- [x] **Criar template `uom_category_form.html`**
  - [x] Layout dark `bg-[#1f2937]` consistente com contacts
  - [x] Nome grande `text-3xl font-light` com border-bottom
  - [x] Tab "Unidades de Medida" (modo edição) — padrão empresa/utilizadores
  - [x] Badge de contagem de UdMs no tab header
  - [x] Tabela inline com colunas: Nome (ícone símbolo), Símbolo (code), Tipo (badge cor), Factor, Estado (Ativo/Arquivado)
  - [x] Click na linha → navega para uom_edit
  - [x] Link "Adicionar unidade de medida" → uom_create
  - [x] Tab só visível em modo edição (não em criação)

- [x] **Criar views**
  - [x] `uom_category_create(request)` — GET/POST, auto-fill owner_company, redirect to edit
  - [x] `uom_category_edit(request, pk)` — GET/POST, passa queryset `uoms` + `uom_count`
  - [x] Rotas: `uom-categories/create/`, `uom-categories/<uuid:pk>/edit/`

---

## 6.3 Modelo Product ✅

Criar modelo de produtos com sistema de UoM integrado.

- [x] **Criar modelo Product**
  - [x] Herdar de AbstractBaseModel (UUID PK, timestamps, is_active)
  - [x] Campos identificação: name, internal_reference (único por empresa), reference (texto livre), barcode (único por empresa), description, image
  - [x] Campo classificação: product_type (storable/consumable/service), category (FK → Category)
  - [x] Campos UoM: uom (FK → UoM, PROTECT), uom_purchase (FK → UoM, opcional — UdM de compra diferente)
  - [x] Campos preços: sale_price (Decimal 10,2), cost_price (Decimal 10,2), tax_rate (Decimal 5,2, default 23%)
  - [x] Campo fornecedor: supplier (FK → Contact, SET_NULL)
  - [x] Campo: **owner_company** (FK para Company, null=True, blank=True) - NULL=global, com valor=privado
  - [x] Constraints: unique internal_reference + owner_company (quando não vazio), unique barcode + owner_company (quando não vazio)
  - [x] Método __str__ (com referência interna se existir)
  - [x] Método get_profit_margin() — margem em percentagem
  - [x] Método get_sale_price_with_tax() — preço com IVA
  - [x] Helper `product_image_path()` para upload em `media/products/<uuid>/`

- [x] **Criar migrations**
  - [x] makemigrations → `0003_product.py`
  - [x] migrate → OK

- [x] **Registrar no Admin**
  - [x] Criar ProductAdmin
  - [x] list_display: name, internal_reference, category, product_type, uom, sale_price, cost_price, is_active
  - [x] search_fields: name, internal_reference, reference, barcode, description
  - [x] list_filter: is_active, product_type, category, owner_company
  - [x] Fieldsets organizados: Identificação, Classificação, UdMs, Preços, Compras, Multi-Company, Sistema

---

## 6.3.1 Vistas de Produtos ✅

Criar lista, formulário (criação/edição) e ações em massa para produtos.

- [x] **ProductForm** em forms.py
  - [x] 13 campos: name, internal_reference, reference, barcode, product_type, category, uom, uom_purchase, sale_price, cost_price, tax_rate, description, image
  - [x] Querysets filtrados por empresa (category, uom, uom_purchase)
  - [x] Empty labels em português

- [x] **Vistas (views.py)**
  - [x] product_list — pesquisa por nome/referência/barcode/categoria/fornecedor, paginação, filtro status
  - [x] product_create — com request.FILES para imagem, owner_company automático
  - [x] product_edit — com get_object_or_404
  - [x] bulk_archive_products, bulk_unarchive_products, bulk_delete_products

- [x] **Templates**
  - [x] product_list.html — tabela com imagem/nome, ref. interna, categoria, tipo (badge), UdM, preço venda/custo; ações em massa; pesquisa com dropdown de campo; paginação
  - [x] product_form.html — formulário dark theme 2 colunas; nome gigante; campos numéricos com |unlocalize; upload de imagem com preview Alpine.js; descrição textarea
  - [x] product_form_navbar.html — link "Produtos" + botões Descartar/Guardar (form="product-form")

- [x] **URLs** em urls.py (6 rotas)
  - [x] products/, products/create/, products/<uuid>/edit/
  - [x] products/bulk-archive/, products/bulk-unarchive/, products/bulk-delete/

- [x] **Navbar** — link "Produtos" atualizado em inventory_navbar.html

---

## 6.3.2 Smart Buttons - Formulário de Produto ✅ (Contadores ⏳ Futuro)

Criar smart buttons no sub-navbar do formulário de produto (`product_form_navbar.html`), seguindo o mesmo layout dos contactos. Os botões estão criados com contadores a zero — serão ligados a dados reais quando os módulos respetivos existirem.

- [x] **Redesenhar `product_form_navbar.html`** — layout igual ao `contacts_navbar_with_stats.html`
  - [x] Link "Produtos" + dropdown "Configuração" (Categorias, UdM, Categorias UdM)
  - [x] Botões Descartar (vermelho) + Guardar (verde)
  - [x] Smart buttons à direita com ícones, contadores e cores distintas

- [x] **Smart Button: BOM** (roxo)
  - [x] Ícone: documento com linhas (file-text)
  - [x] Contador: `bom_count` (atualmente 0)
  - [ ] ⏳ Conectar a dados reais — **depende de:** Fase 10 (modelo BillOfMaterials + BOMLine)
  - [ ] ⏳ Contador real: `BillOfMaterials.objects.filter(product=product).count()`
  - [ ] ⏳ Link: redirecionar para lista de BOMs filtrada pelo produto

- [x] **Smart Button: Previsão** (azul)
  - [x] Ícone: gráfico de pulso (activity)
  - [x] Contador: `forecast_count` (on_hand + incoming_pending - outgoing_pending, dados reais)
  - [x] ⏳ Conectar a dados reais — StockMovementLine draft aggregation ✅
  - [x] ⏳ Contador real: previsão de stock baseada em movimentos pendentes ✅
  - [x] ⏳ Link: redirecionar para vista de previsão do produto (`product_forecast` view) ✅

- [x] **Smart Button: Vendidas** (verde)
  - [x] Ícone: saco de compras (shopping-bag)
  - [x] Contador: `sold_count` (atualmente 0)
  - [ ] ⏳ Conectar a dados reais — **depende de:** Fase 8 (modelo SaleOrder + SaleOrderLine)
  - [ ] ⏳ Contador real: `SaleOrderLine.objects.filter(product=product, order__state='confirmed').aggregate(Sum('quantity'))`
  - [ ] ⏳ Link: redirecionar para lista de vendas filtrada pelo produto

- [x] **Smart Button: Em Stock** (laranja)
  - [x] Ícone: cubo 3D (package/box)
  - [x] Contador: `on_hand_count` — `StockQuant.objects.filter(product=product).aggregate(Sum('quantity'))` ✅
  - [x] ⏳ Conectar a dados reais — StockQuant.Sum real ✅
  - [x] ⏳ Contador real: `StockQuant` aggregation por produto ✅
  - [x] ⏳ Link: `physical_inventory_list?search=<nome>&field=produto` ✅

- [x] **View `product_edit`** — passa contadores ao template
  - [x] `on_hand_count`: StockQuant real (Sum), `forecast_count`: on_hand + incoming - outgoing ✅
  - [x] `bom_count`, `sold_count`: 0 (placeholder Fase 10 / Fase 8)

- [ ] **Testing - Smart Buttons Produto** ⏳
  - [ ] Test: smart buttons renderizam no formulário de edição
  - [ ] Test: smart buttons mostram 0 quando não há dados
  - [ ] Test: BOM contador mostra valor correto quando modelo BOM existir
  - [ ] Test: Vendidas contador mostra total de unidades vendidas
  - [ ] Test: Em Stock mostra quantidade em stock atual
  - [ ] Test: Previsão mostra previsão calculada

---

## 📦 ARQUITETURA DO SISTEMA DE INVENTÁRIO (Simplificado)

> **FILOSOFIA:** Sistema de inventário prático e maioritariamente AUTOMÁTICO.
> A pessoa não vai gerir armazéns, localizações ou rotas — o armazém é a casa dela.
> O foco é: controlar stock, saber custo/lucro, e automatizar compras/vendas.
> O sistema de PDF scanning (Fase 14) vai auto-criar documentos de compra.
> A pessoa raramente interage manualmente com o inventário.

### 🏗️ Como funciona o Sistema de Inventário (explicação simples)

**Conceito:** O stock é controlado por **movimentos**. Cada movimento é um documento
que diz "entrou X" ou "saiu Y" ou "ajustei Z". O saldo atual (StockQuant) é calculado
automaticamente a partir dos movimentos validados.

**5 modelos:**

1. **Warehouse (Armazém)** — Simples: "Armazém Principal" = casa/empresa da pessoa.
   - Auto-criado ao fazer setup. A pessoa raramente cria outro.
   - Sem localizações internas (não há prateleiras para nomear).

2. **StockMovement (Movimento de Stock — cabeçalho)** — O "documento" de stock.
   - 3 tipos: **Receção** (entrou), **Expedição** (saiu), **Ajuste** (correção).
   - Estados simples: `draft` (rascunho) → `done` (validado) ou `cancelled`.
   - **Origin:** referência ao documento que gerou (ex: "PO-00001", "SO-00001").
   - Geralmente criado AUTOMATICAMENTE pelas Compras (Fase 7) ou Vendas (Fase 8).

3. **StockMovementLine (Linha — detalhe)** — Cada produto num movimento.
   - Produto, quantidade, preço unitário (para calcular custo na receção).
   - Um movimento pode ter muitas linhas (ex: uma fatura do Recheio com 20 produtos).

4. **StockQuant (Stock Atual)** — Quantidade real de cada produto no armazém.
   - Produto + Armazém + Quantidade = "tens 50 kg de farinha no armazém".
   - Atualizado AUTOMATICAMENTE quando um movimento é validado (done).
   - Nunca editado manualmente — é sempre resultado dos movimentos.

5. **ProductSupplierInfo (Info Fornecedor)** — Dados de compra por produto.
   - Múltiplos fornecedores por produto (Recheio vende farinha a €2, Makro a €1.80).
   - Preço, quantidade mínima, prazo de entrega.
   - Usado pelo sistema para saber a quem comprar e a que preço.
   - Aparece no tab "Compras" do formulário do produto.

### 🔄 Fluxos de Operação

**FLUXO DE COMPRA (automático via PDF ou manual):**
```
1. Opção A — AUTOMÁTICO (Fase 14): Pessoa mete fatura na impressora
   → Sistema lê PDF → cria PurchaseOrder → cria StockMovement receção → valida → stock atualizado
   Opção B — MANUAL: Criar PurchaseOrder na app Compras (Fase 7)
2. PO confirmado → sistema cria StockMovement (tipo=RECEIPT)
3. Ao validar → StockQuant incrementado para cada produto
4. Preço de custo atualizado no produto (se mudou)
```

**FLUXO DE VENDA (semi-automático):**
```
1. Criar orçamento/venda (Fase 8) → cliente + produtos
2. Confirmar venda → sistema verifica stock:
   - Se tem stock → cria StockMovement (tipo=DELIVERY)
   - Se NÃO tem stock → ALERTA + opção de auto-gerar PurchaseOrder
3. Ao entregar → valida StockMovement → StockQuant decrementado
4. Lucro calculado: sale_price - cost_price por produto
```

**AJUSTE MANUAL (raro):**
```
1. Pessoa nota que tem menos/mais stock que o sistema diz
2. Cria ajuste: produto, quantidade real, motivo
3. Sistema calcula diferença e cria StockMovement (tipo=ADJUSTMENT)
4. Valida → StockQuant atualizado
```

### 🔗 Dependências entre Fases

| Fase | O que faz | Interação com Inventário |
|------|-----------|--------------------------|
| 6 | Inventário | Modelos de stock, movimentos, quants |
| 7 | Compras | Confirmar compra → auto-cria receção de stock |
| 8 | Vendas | Confirmar venda → verifica stock → auto-cria expedição |
| 10 | BOM | Produção → consome ingredientes, produz produto acabado |
| 14 | PDF Scan | Digitalizar fatura → auto-cria compra + receção de stock |

---

## 6.4 Modelo Warehouse (Armazém) ✅

Modelo simples — representa o local de armazenamento. Auto-criado ao setup, 1 por empresa.

- [x] **Criar modelo Warehouse**
  - [x] Herdar de AbstractBaseModel
  - [x] Campos: name (CharField, ex: "Armazém Principal")
  - [x] Campos: code (CharField, 5 chars, único, ex: "WH")
  - [x] Campos: address (TextField, opcional)
  - [x] Campo: is_default (BooleanField, default=False) — 1 default por company
  - [x] Campo: **owner_company** (FK para Company, null=True, blank=True)
  - [x] Método __str__: retorna name

- [x] **Criar migrations**
  - [x] makemigrations e migrate

- [x] **Registrar no Admin**
  - [x] Criar WarehouseAdmin
  - [x] list_display: name, code, is_default, owner_company

- [x] **Auto-criação: Armazém Padrão**
  - [x] Signal post_migrate ou seed script: cria "Armazém Principal" (code="WH", is_default=True)
  - [x] Associar à company ativa

- [x] **Testing - Warehouse**
  - [x] Test: criar armazém funciona
  - [x] Test: apenas 1 armazém default por company
  - [x] Test: armazém padrão auto-criado no setup

---

## 6.4.1 Vista de Lista de Armazéns ✅

Lista de armazéns com search, paginação e bulk actions — segue o padrão da lista de contactos.

- [x] **View `warehouse_list`** em views.py
  - [x] Search por campo: name, code, address, company
  - [x] Filtro de status: ativos / arquivados
  - [x] Paginação: 50 por página (configurável)
  - [x] select_related('owner_company')

- [x] **Template `warehouse_list.html`** — layout igual à lista de contactos
  - [x] Navbar: `inventory_navbar.html` (sub_navbar)
  - [x] Search bar com dropdown: status filter + pesquisa por campo (Nome, Código, Morada, Empresa)
  - [x] Botão "Novo" → link para warehouse_create
  - [x] Paginação desktop + mobile
  - [x] Sem toggle Kanban — apenas vista de lista
  - [x] Tabela: Checkbox, Nome (com ícone), Código, Morada, Padrão (badge), Empresa
  - [x] Checkbox → Bulk Actions: Arquivar, Desarquivar, Eliminar
  - [x] Modal de confirmação de eliminação (com checkbox de confirmação)
  - [x] Versão mobile responsiva completa

- [x] **Bulk Action Views**
  - [x] `bulk_archive_warehouses` — POST, JSON body com warehouse_ids
  - [x] `bulk_unarchive_warehouses` — POST, JSON body com warehouse_ids
  - [x] `bulk_delete_warehouses` — POST, JSON body com warehouse_ids, transaction.atomic

- [x] **URLs** em urls.py (4 rotas)
  - [x] warehouses/, warehouses/bulk-archive/, warehouses/bulk-unarchive/, warehouses/bulk-delete/

- [x] **Navbar** — link "Armazéns" atualizado em inventory_navbar.html (Configuração dropdown)

---

## 6.4.2 Formulário de Armazém (Criar/Editar) ✅

Formulário simples de criação e edição de armazéns — layout igual aos contactos.

- [x] **WarehouseForm** em forms.py
  - [x] Campos: name, code, address, is_default
  - [x] ModelForm com validação automática

- [x] **Views** em views.py
  - [x] `warehouse_create` — GET mostra form vazio, POST salva + redirect para edit
  - [x] `warehouse_edit` — GET mostra form preenchido, POST atualiza + redirect para edit
  - [x] owner_company atribuída automaticamente

- [x] **Template `warehouse_form.html`** — layout igual aos contactos
  - [x] Ícone de armazém (160x160) à esquerda
  - [x] Nome gigante (3xl, border-bottom) + Código com ícone dourado
  - [x] Grid 2 colunas: Morada (textarea) | Armazém Padrão (toggle switch) + Empresa (read-only)

- [x] **Navbar `warehouse_form_navbar.html`**
  - [x] Link "Armazéns" → volta para warehouse_list
  - [x] Botão Descartar (vermelho) + Guardar (verde)
  - [x] form="warehouse-form"

- [x] **URLs** em urls.py (2 rotas novas)
  - [x] warehouses/create/, warehouses/<uuid:pk>/edit/

- [x] **Lista atualizada** — botão "Novo" e click na row apontam para o formulário

---

## 6.5 Modelo StockMovement (Documento de Movimento de Stock) ✅

O documento central do inventário. Criado automaticamente por Compras/Vendas ou manualmente para ajustes.

- [x] **Criar modelo StockMovement**
  - [x] Herdar de AbstractBaseModel
  - [x] Campo: reference (CharField, único, auto-gerado, ex: "WH/IN/00001", "WH/OUT/00001", "ADJ/00001")
  - [x] Campo: movement_type (CharField, choices):
    - [x] `receipt` — Receção de mercadoria (compra/entrada)
    - [x] `delivery` — Expedição/entrega (venda/saída)
    - [x] `adjustment` — Ajuste de inventário (correção manual)
  - [x] Campo: warehouse (FK Warehouse, default=armazém padrão)
  - [x] Campo: partner (FK Contact, null=True, blank=True) — fornecedor (receção) ou cliente (expedição)
  - [x] Campo: state (CharField, choices):
    - [x] `draft` — Rascunho, editável
    - [x] `done` — Validado, stock atualizado
    - [x] `cancelled` — Cancelado
  - [x] Campo: date (DateTimeField, default=now) — data do movimento
  - [x] Campo: origin (CharField, null=True, blank=True) — ref ao documento que gerou (ex: "PO-00001", "SO-00001")
  - [x] Campo: notes (TextField, null=True, blank=True)
  - [x] Campo: responsible (FK User) — quem criou/validou
  - [x] Campo: **owner_company** (FK para Company, null=True, blank=True)
  - [x] Método __str__: retorna reference
  - [x] Método generate_reference(): gera ref baseado no tipo ("WH/IN/", "WH/OUT/", "ADJ/") + sequência
  - [x] Método action_validate(): muda para done, atualiza StockQuant para cada linha
  - [x] Método action_cancel(): muda para cancelled (apenas se draft)
  - [x] Property total_value: soma de (line.quantity * line.unit_price) de todas as linhas

- [x] **Criar migrations**
  - [x] makemigrations e migrate

- [x] **Registrar no Admin**
  - [x] Criar StockMovementAdmin com inline de StockMovementLine
  - [x] list_display: reference, movement_type, partner, state, date, total_value
  - [x] list_filter: state, movement_type

- [x] **Testing - StockMovement**
  - [x] Test: criar movimento funciona
  - [x] Test: referência auto-gerada com prefix correto por tipo
  - [x] Test: validar muda estado para done
  - [x] Test: cancelar só funciona se draft
  - [x] Test: total_value calcula soma das linhas

---

## 6.6 Modelo StockMovementLine (Linhas de Movimento) ✅

Cada produto dentro de um movimento. Contém quantidade e preço unitário (para cálculo de custo).

- [x] **Criar modelo StockMovementLine**
  - [x] Herdar de AbstractBaseModel
  - [x] Campo: stock_movement (FK StockMovement, on_delete=CASCADE, related_name='lines')
  - [x] Campo: product (FK Product, on_delete=PROTECT)
  - [x] Campo: quantity (DecimalField) — quantidade movida
  - [x] Campo: unit_price (DecimalField, default=0) — preço unitário (custo na receção, sale_price na expedição)
  - [x] Campo: uom (FK UoM, null=True, blank=True) — herda do produto se vazio
  - [x] Método save(): se uom vazio, herdar de product.uom
  - [x] Property line_total: quantity × unit_price

- [x] **Criar migrations**
  - [x] makemigrations e migrate

- [x] **Testing - StockMovementLine**
  - [x] Test: criar linha funciona
  - [x] Test: uom herda do produto se não definido
  - [x] Test: line_total calcula corretamente

---

## 6.7 Modelo StockQuant (Stock Atual) ✅

Quantidade real de cada produto no armazém. Atualizado automaticamente quando um StockMovement é validado.

- [x] **Criar modelo StockQuant**
  - [x] Herdar de AbstractBaseModel
  - [x] Campo: product (FK Product, on_delete=CASCADE, related_name='quants')
  - [x] Campo: warehouse (FK Warehouse, on_delete=CASCADE, related_name='quants')
  - [x] Campo: quantity (DecimalField, default=0) — quantidade em mão
  - [x] Constraint: unique_together (product, warehouse) — 1 quant por produto/armazém

- [x] **Métodos de classe (helpers)**
  - [x] get_on_hand(product, warehouse=None): retorna quantidade em armazém (ou total se warehouse=None)
  - [x] update_quantity(product, warehouse, qty, mode='add'): add/subtract quantity (get_or_create)

- [x] **Integração com StockMovement.action_validate()**
  - [x] Ao validar um movimento:
    - [x] Se receipt: para cada linha → StockQuant.update_quantity(product, warehouse, qty, 'add')
    - [x] Se delivery: para cada linha → StockQuant.update_quantity(product, warehouse, qty, 'subtract')
    - [x] Se adjustment: calcular diferença (positiva = add, negativa = subtract)
  - [x] Se ao subtrair o stock fica negativo → permitir mas alertar (stock negativo = algo errado)

- [x] **Criar migrations**
  - [x] makemigrations e migrate

- [x] **Registrar no Admin**
  - [x] Criar StockQuantAdmin
  - [x] list_display: product, warehouse, quantity
  - [x] list_filter: warehouse

- [x] **Testing - StockQuant**
  - [x] Test: criar quant funciona
  - [x] Test: unique_together impede duplicados (product, warehouse)
  - [x] Test: validar receção incrementa quantidade
  - [x] Test: validar expedição decrementa quantidade
  - [x] Test: validar ajuste positivo/negativo funciona
  - [x] Test: stock negativo é permitido (mas gera alerta/log)

---

## 6.8 Modelo ProductSupplierInfo (Info Fornecedor por Produto) ✅

Informações de compra por fornecedor. Permite múltiplos fornecedores por produto com fallback por sequência.
`supplier_product_code` é usado na Fase 14 (PDF scanning) para identificar o produto na fatura quando a `internal_reference` não coincide — o sistema tenta: 1º `internal_reference`, 2º `supplier_product_code` do fornecedor da fatura. Quando há match e o preço mudou, auto-atualiza `price` e `Product.cost_price`.

- [x] **Criar modelo ProductSupplierInfo**
  - [x] Herdar de AbstractBaseModel
  - [x] Campo: product (FK Product, CASCADE, related_name='supplier_infos')
  - [x] Campo: supplier (FK Contact, CASCADE, related_name='supplied_products')
  - [x] Campo: sequence (PositiveSmallIntegerField, default=10) — prioridade de compra (menor = preferido)
  - [x] Campo: supplier_product_code (CharField, blank=True) — ref do produto na fatura do fornecedor, usado para matching automático na Fase 14
  - [x] Campo: price (DecimalField 12,4) — preço unitário de compra na UdM de compra do produto
  - [x] Campo: min_quantity (DecimalField, default=1) — quantidade mínima de encomenda
  - [x] Campo: lead_time (IntegerField, default=0) — prazo de entrega em dias
  - [x] Campo: is_preferred (BooleanField, default=False) — atalho para "fornecedor preferido" (complementa sequence)
  - [x] Campo: owner_company (FK Company, null=True, blank=True)
  - [x] Constraint: unique_together (product, supplier)
  - [x] Método de classe get_best_supplier(product): retorna (supplier, price) do fornecedor preferred ou de menor sequence
  - [x] Método de classe find_by_supplier_code(supplier, code): lookup para Fase 14 (PDF matching)
  - [x] Ordering: ['sequence', '-is_preferred', 'price']

- [x] **Atualizar tab "Compras" do formulário Product**
  - [x] Tabela Alpine.js dinâmica com colunas: Seq, Fornecedor (searchable), Cód. Fornecedor, Preço, Qtd Mín, Prazo (dias), Preferido, Ações
  - [x] Adicionar linha via botão + dropdown de pesquisa de contactos
  - [x] Guardar/actualizar linha via API (PUT)
  - [x] Remover linha via API (DELETE)
  - [x] Ordenação visual por sequência

- [x] **Criar migrations**
  - [x] makemigrations e migrate

- [x] **Registrar no Admin**
  - [x] ProductSupplierInfoAdmin com list_display: product, supplier, sequence, price, min_quantity, lead_time, is_preferred

- [x] **APIs AJAX**
  - [x] GET `products/<pk>/suppliers/` — lista supplier_infos do produto (JSON)
  - [x] POST `products/<pk>/suppliers/` — criar nova linha
  - [x] PUT `products/<pk>/suppliers/<si_pk>/` — actualizar linha
  - [x] DELETE `products/<pk>/suppliers/<si_pk>/` — remover linha

- [x] **Testing - ProductSupplierInfo**
  - [x] Test: criar funciona
  - [x] Test: unique_together impede duplicados
  - [x] Test: get_best_supplier retorna preferred, ou menor sequence
  - [x] Test: find_by_supplier_code encontra por código do fornecedor
  - [x] Test: tab "Compras" mostra fornecedores e permite edição inline

---

## 6.9 ✅ Adicionar Campos de Stock ao Produto

Campos e métodos no modelo Product para alimentar smart buttons e tabs.

- [x] **Novos campos em Product (migration)**
  - [x] Campo: min_stock (DecimalField, default=0) — stock mínimo para alertas
  - [ ] Campo: weight (DecimalField, null=True, blank=True) — peso em kg (opcional)

- [x] **Métodos novos em Product**
  - [x] get_on_hand_quantity(warehouse=None): StockQuant.get_on_hand(self, warehouse)
  - [x] get_incoming_quantity(): soma qty de StockMovementLines em movimentos receipt/draft
  - [x] get_outgoing_quantity(): soma qty de StockMovementLines em movimentos delivery/draft
  - [x] get_forecasted_quantity(): on_hand + incoming - outgoing
  - [x] get_profit_margin(): já existe — sale_price - cost_price
  - [x] get_stock_value(): on_hand × cost_price (valor do inventário deste produto)

- [x] **Atualizar tab "Inventário" do formulário Product**
  - [x] No tab "Inventário" do product_form.html, mostrar (read-only):
    - [x] Em Mão: get_on_hand_quantity()
    - [x] A Receber: get_incoming_quantity() (movimentos de receção pendentes)
    - [x] A Expedir: get_outgoing_quantity() (movimentos de expedição pendentes)
    - [x] Previsão: get_forecasted_quantity()
    - [x] Valor em Stock: get_stock_value()
    - [x] Margem de Lucro: get_profit_margin() / sale_price × 100 (em %)
  - [x] Campos editáveis: min_stock
  - [ ] Campos editáveis: weight

- [x] **Criar migrations**
  - [x] makemigrations e migrate

- [ ] **Testing - Product Stock Fields**
  - [ ] Test: get_on_hand_quantity retorna valor correto de StockQuant
  - [ ] Test: get_forecasted_quantity = on_hand + incoming - outgoing
  - [ ] Test: get_stock_value = on_hand × cost_price
  - [ ] Test: tab Inventário mostra valores

---

## 6.10 Views de Movimentos de Stock

Criar views para listar e gerir movimentos de stock. Vista principal = lista com tabs por tipo.

- [x] **StockMovementListView (lista principal)**
  - [x] Listar movimentos com filtros:
    - [x] Filtros: estado, tipo (receção/entrega/ajuste), pesquisa por referência/parceiro/origem
    - [x] Filtro por tipo: Todos / Receções / Entregas / Ajustes
    - [x] Filtro por estado: Todos / Rascunho / Validado / Cancelado / Arquivados
  - [x] Colunas: Referência (com ícone por tipo), Tipo (badge), Contacto, Estado, Data, Armazém, Total
  - [x] Paginação server-side (50/page)
  - [x] Bulk actions: arquivar, desarquivar, eliminar
  - [x] Botão "Novo" → dropdown com Nova Receção / Nova Entrega
  - [x] URL: `operations/movements/` · Nome: `all_movements_list`
  - [x] Link "Todos os Movimentos" no navbar Operações

- [x] **StockMovementCreateView (criar movimento manual)**
  - [x] Form: movement_type (pré-selecionado se veio de tab), warehouse, partner, date, notes
  - [x] Tabela de linhas (Alpine.js dinâmico):
    - [x] Produto (seletor com busca), Quantidade, Preço Unitário, UdM (auto do produto)
    - [x] Botão "Adicionar Linha" e "Remover"
    - [x] Total por linha e total geral (calculados em real-time)
  - [x] Botões: "Guardar Rascunho" e "Validar" (guardar + validar de uma vez)

- [x] **StockMovementEditView (editar rascunho)**
  - [x] Apenas se estado = draft
  - [x] Mesmo form que create, pré-preenchido
  - [x] Botões: "Guardar", "Validar", "Cancelar"

- [ ] **StockMovementDetailView (ver movimento validado)**
  - [ ] Mostrar cabeçalho e linhas (read-only se done)
  - [ ] Informação: referência, tipo, parceiro, data, valor total
  - [ ] Tabela de linhas: produto, quantidade, preço, total linha
  - [ ] Se draft: botões "Editar", "Validar", "Cancelar"
  - [ ] Se done: apenas visualização + link para parceiro

- [ ] **Templates**
  - [x] `templates/inventory/all_movements_list.html` — lista global com filtros tipo + estado
  - [x] `templates/inventory/stock_movement_form.html` — form create/edit com linhas dinâmicas
  - [ ] `templates/inventory/stock_movement_detail.html` — detalhe read-only
  - [x] `templates/components/stock_movement_form_navbar.html` — navbar

- [ ] **Rotas**
  - [x] `path('operations/movements/', ..., name='all_movements_list')`
  - [x] `path('operations/adjustments/', ..., name='adjustment_list')`
  - [x] `path('operations/adjustments/new/', ..., name='adjustment_create')`
  - [ ] `path('inventory/movements/<uuid:pk>/', ..., name='stock_movement_detail')`
  - [x] `path('operations/movements/<uuid:pk>/edit/', ..., name='movement_edit')`
  - [x] `path('operations/movements/<uuid:pk>/validate/', ..., name='movement_validate')`
  - [x] `path('operations/movements/<uuid:pk>/cancel/', ..., name='movement_cancel')`
  - [ ] `path('inventory/movements/bulk-action/', ..., name='stock_movement_bulk_action')`

- [ ] **Testing - StockMovement Views**
  - [ ] Test: listar movimentos funciona
  - [ ] Test: tabs filtram por tipo
  - [ ] Test: criar movimento com linhas funciona
  - [ ] Test: validar atualiza StockQuant
  - [ ] Test: cancelar funciona se draft
  - [ ] Test: editar apenas em draft

---

## 6.10.1 Chatter no Formulário de Movimento ✅

Integração do sistema de chatter (Nota + Log + Seguidores) no formulário de movimento, com design idêntico ao CRM.

- [x] **Componente `templates/components/chatter_inventory.html`**
  - [x] Design idêntico ao chatter do CRM
  - [x] Container lateral (30% largura, sticky, altura viewport)
  - [x] Duas abas: Nota e Log
  - [x] Encoding UTF-8 correto (HTML entities em vez de caracteres especiais)

- [x] **Aba Nota (Alpine.js, API-driven)**
  - [x] Função Alpine `inventoryNotesPanel(movementId)`
  - [x] Carrega notas via `GET /inventory/operations/movements/<pk>/notes/`
  - [x] Submete notas via `POST /inventory/operations/movements/<pk>/notes/create/`
  - [x] Dropdown @mention de utilizadores via `/crm/api/users/search/`
  - [x] Toggle urgente (⚠), visibilidade interna, botão "Adicionar"
  - [x] Notas renderizadas dinamicamente (sem reload de página)

- [x] **Aba Log — Histórico de Atividades (estilo CRM)**
  - [x] Header "Histórico de Atividades"
  - [x] Ícones coloridos por tipo: 🟢 CREATE, 🔵 UPDATE, 🟡 STATUS_CHANGE
  - [x] Diffs de campos: valor antigo (`line-through text-red-400`) → novo (`text-green-400`)
  - [x] Formatação de datas relativas

- [x] **Widget de Seguidores**
  - [x] Função Alpine `inventoryFollowersWidget(movementId)`
  - [x] Avatar stack com seguidores actuais
  - [x] Dropdown de pesquisa para adicionar seguidor
  - [x] Carrega via `GET /inventory/operations/movements/<pk>/followers/`
  - [x] Adicionar seguidor via `POST` (mesmo endpoint)
  - [x] Remover seguidor via `DELETE /inventory/operations/movements/<pk>/followers/<user_id>/remove/`

- [x] **APIs — Notas**
  - [x] View `movement_notes_list` — `GET /inventory/operations/movements/<pk>/notes/`
  - [x] View `movement_note_create` — `POST /inventory/operations/movements/<pk>/notes/create/`

- [x] **APIs — Seguidores**
  - [x] View `movement_followers_api` — `GET`/`POST /inventory/operations/movements/<pk>/followers/`
  - [x] View `movement_follower_remove_api` — `DELETE /inventory/operations/movements/<pk>/followers/<user_id>/remove/`

- [x] **URLs de Chatter registadas em `apps/inventory/urls.py`**
  - [x] `path('operations/movements/<uuid:pk>/notes/', ..., name='movement_notes_list')`
  - [x] `path('operations/movements/<uuid:pk>/notes/create/', ..., name='movement_note_create')`
  - [x] `path('operations/movements/<uuid:pk>/followers/', ..., name='movement_followers_api')`
  - [x] `path('operations/movements/<uuid:pk>/followers/<uuid:user_id>/remove/', ..., name='movement_follower_remove_api')`

- [x] **`movement_edit` — Rastreio de campos alterados**
  - [x] Captura valores antigos ANTES de salvar (`partner`, `warehouse`, `date`, `origin`, `notes`)
  - [x] Calcula dicionário `_changes` com pares old/new por campo
  - [x] Armazena em `ChatterActivity.details = {'changes': {...}}`
  - [x] Log mostra diffs reais no histórico

---

## 6.11 Lista de Inventário Físico ✅

Vista de leitura do stock actual (StockQuant) por produto e armazém.  
URL: `operations/inventario-fisico/` · Nome: `physical_inventory_list`

- [x] **View `physical_inventory_list`** em `apps/inventory/views.py`
  - [x] Queryset: `StockQuant` com `select_related` (produto, categoria, UdM, armazém)
  - [x] Apenas produtos activos (`product__is_active=True`)
  - [x] Anotação `stock_value = quantity × product.cost_price` por linha
  - [x] Total geral via `Sum('stock_value')`
  - [x] Paginação server-side (50 registos/pág por defeito)
  - [x] Pesquisa por campo: produto (nome/ref. interna), armazém, categoria, auto (todos)
  - [x] Filtro por armazém via query param `?warehouse=<id>`

- [x] **Template `templates/inventory/physical_inventory_list.html`**
  - [x] Navbar padrão + sub-navbar de inventário
  - [x] Barra de pesquisa (desktop + mobile) com dropdown de filtros
  - [x] Colunas: Produto (imagem/ícone + ref.), Categoria, Armazém, Em Mão, Custo Unit., Valor em Stock
  - [x] Quantidade a vermelho quando ≤ 0
  - [x] Click na linha → abre `product_edit`
  - [x] Footer com total do valor em stock
  - [x] Paginação com input editável de tamanho de página

- [x] **URL** `path('operations/inventario-fisico/', ..., name='physical_inventory_list')`

- [x] **Navbar** (`inventory_navbar.html`) — link "Inventário Físico" aponta para a view real

---

## 6.12.1 View de Stock Actual — Overview Avançado (a implementar)

Vista completa com previsões, margens e alertas de stock mínimo.  
*(Depende de 6.9 — campos min_stock, get_forecasted_quantity, get_profit_margin)*

- [ ] **StockOverviewView**
  - [ ] Listar produtos com informação de stock:
    - [ ] Colunas: Produto, Categoria, Em Mão, Previsão, Custo Unit., Valor em Stock, Margem %
  - [ ] Filtros: categoria, busca por nome, armazém
  - [ ] Destaque visual: vermelho (stock=0), laranja (stock < min_stock), verde (stock OK)
  - [ ] Totais no footer: valor total do inventário
  - [ ] Paginação server-side (50/page)
  - [ ] Click no produto → vai para product_edit (tab Inventário)

- [ ] **Template**
  - [ ] `templates/inventory/stock_overview.html`

- [ ] **Rota**
  - [ ] `path('inventory/stock/', ..., name='stock_overview')`

- [ ] **Testing - Stock Overview**
  - [ ] Test: overview mostra quantidades corretas
  - [ ] Test: valor do inventário calculado
  - [ ] Test: alertas visuais para stock baixo
  - [ ] Test: filtros funcionam

---

## 6.12 Ajustes de Inventário (Simplificado)

Form dedicado para ajustes rápidos de stock. Cria StockMovement de tipo adjustment automaticamente.

- [ ] **InventoryAdjustmentView**
  - [ ] Form simplificado:
    - [ ] Armazém (default: principal)
    - [ ] Tabela de produtos:
      - [ ] Produto (seletor com busca), Stock Sistema (read-only, auto-preenchido), Stock Real (input), Motivo
    - [ ] Ao guardar: para cada produto com diferença:
      - [ ] Cria StockMovement (type=adjustment) + StockMovementLine
      - [ ] Valida automaticamente (done)
      - [ ] StockQuant atualizado
  - [ ] Flash message: "Ajuste validado: X produtos atualizados"

- [ ] **Template**
  - [ ] `templates/inventory/inventory_adjustment.html`

- [ ] **Rota**
  - [ ] `path('inventory/adjustments/new/', ..., name='inventory_adjustment_create')`

- [ ] **Testing - Adjustment**
  - [ ] Test: ajuste positivo incrementa stock
  - [ ] Test: ajuste negativo decrementa stock
  - [ ] Test: StockMovement criado com tipo adjustment
  - [ ] Test: movimento é auto-validado

---

## 6.13 Relatório de Valorização de Stock

Relatório simples para a pessoa saber quanto vale o seu inventário.

- [ ] **StockValuationView**
  - [ ] Mostrar por produto:
    - [ ] Produto, Quantidade, Custo Unitário, Valor Total (qty × cost), Preço Venda, Lucro Potencial
  - [ ] Filtros: categoria, apenas com stock > 0
  - [ ] Totais: valor total do inventário, lucro potencial total
  - [ ] Notas: "Lucro Potencial = (sale_price - cost_price) × quantidade em stock"

- [ ] **Template**
  - [ ] `templates/inventory/stock_valuation.html`

- [ ] **Rota**
  - [ ] `path('inventory/reports/valuation/', ..., name='stock_valuation_report')`

- [ ] **Testing - Valuation**
  - [ ] Test: valorização calcula valor correto
  - [ ] Test: lucro potencial calcula corretamente
  - [ ] Test: filtro por categoria funciona

---

## 6.14 Smart Buttons com Dados Reais ✅ (parcial)

Conectar os smart buttons do formulário de produto (já criados em 6.3.2) aos dados reais.

- [x] **Atualizar product_edit view (views.py)**
  - [x] Passar contadores reais ao template:
    - [x] `on_hand_count`: `StockQuant.objects.filter(product=product).aggregate(Sum('quantity'))` ✅
    - [x] `forecast_count`: on_hand + incoming_pending - outgoing_pending ✅
    - [x] `bom_count`: 0 (placeholder até Fase 10)
    - [x] `sold_count`: 0 (placeholder até Fase 8)

- [x] **Clicks dos smart buttons**
  - [x] **Em Stock** (laranja): `<a>` → `physical_inventory_list?search=<produto>&field=produto` ✅
  - [x] **Previsão** (azul): `<a>` → `product_forecast` view (página dedicada com gráfico + tabelas) ✅
  - [ ] **BOM** (roxo): click → ⏳ futuro (Fase 10)
  - [ ] **Vendidas** (verde): click → ⏳ futuro (Fase 8)

- [ ] **Método Product.get_stats() (helper completo)**
  - [ ] Retorna dict com todos os contadores:
    - [ ] on_hand_qty, forecasted_qty, incoming_qty, outgoing_qty
    - [ ] stock_value (on_hand × cost_price)
    - [ ] profit_margin_pct
    - [ ] supplier_count (product.supplier_infos.count())
    - [ ] bom_count: 0 (Fase 10)
    - [ ] sales_count: 0 (Fase 8)

- [ ] **Testing - Smart Buttons**
  - [ ] Test: smart buttons mostram valores corretos
  - [ ] Test: get_stats() retorna contadores corretos
  - [ ] Test: click Em Stock navega para stock_overview

---

## 6.15 Alertas de Stock e Dashboard Widget ✅ (parcial)

Alertas visuais para produtos com stock baixo.

- [x] **Alertas na product_list**
  - [x] Cores: destaque âmbar nas linhas de produtos abaixo do mínimo
  - [x] Filtro "Abaixo do mínimo" no dropdown da lista de produtos
  - [x] Signal `post_save` em StockMovement (state=done) → Notification SYSTEM
  - [x] Celery beat task `check_low_stock_periodic` (cada 4h)
  - [x] Botão manual "Verificar Stock Mínimo" no navbar Configuração → Sinais

- [ ] **Alertas na stock_overview (6.12.1)**
  - [ ] Cores: vermelho (stock = 0), laranja (stock < min_stock), verde (stock >= min_stock)
  - [ ] Badge/counter no topo: "X produtos com stock baixo"

- [ ] **Widget no Dashboard**
  - [ ] Adicionar widget "Stock" no dashboard principal:
    - [ ] Total de produtos
    - [ ] Produtos com stock baixo (< min_stock)
    - [ ] Valor total do inventário
    - [ ] Link rápido para stock_overview

- [ ] **Testing - Alerts**
  - [ ] Test: produtos com stock < min_stock destacados
  - [ ] Test: dashboard widget mostra contagem

---

## 6.15.1 Lista de Compras (Reabastecimento Automático)

Vista dedicada que agrega todos os produtos abaixo do stock mínimo e sugere quantidades a comprar.
Aparece também como widget no dashboard principal de aplicações.
Mais tarde (Fase 7) será a base para geração automática de Ordens de Compra.

> **Lógica central:** `a_comprar = max(0, min_stock - on_hand + outgoing_pending)`
> O sistema sugere comprar o suficiente para cobrir o mínimo **e** as saídas pendentes.

### Modelo: `StockReorderRule` (Regra de Reabastecimento)

- [ ] **Criar modelo `StockReorderRule`**
  - [ ] Herdar de `AbstractBaseModel`
  - [ ] Campo: `product` (FK Product, CASCADE)
  - [ ] Campo: `warehouse` (FK Warehouse, CASCADE)
  - [ ] Campo: `min_qty` (DecimalField) — stock mínimo que dispara o alerta/pedido
  - [ ] Campo: `max_qty` (DecimalField, null=True, blank=True) — quantidade alvo ao reabastecer (opcional)
  - [ ] Campo: `qty_multiple` (DecimalField, default=1) — arredondar pedido para múltiplo desta quantidade (ex: packs de 5 kg)
  - [ ] Campo: `lead_time_days` (IntegerField, default=0) — prazo de entrega esperado (informativo)
  - [ ] Campo: `active` (BooleanField, default=True)
  - [ ] Campo: `owner_company` (FK Company, null=True, blank=True)
  - [ ] Constraint: `unique_together (product, warehouse)`
  - [ ] Property `on_hand`: StockQuant.get_on_hand(product, warehouse)
  - [ ] Property `qty_to_order`: `max(0, (max_qty or min_qty) - on_hand + outgoing_pending)`
  - [ ] Property `needs_reorder`: `on_hand < min_qty`
  - [ ] Método __str__: `f"Regra {product.name} — mín {min_qty}"`

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] `StockReorderRuleAdmin` com list_display: product, warehouse, min_qty, max_qty, on_hand (calculado), needs_reorder

### View: Lista de Compras (`purchase_suggestions`)

- [ ] **View `purchase_suggestions`** em `apps/inventory/views.py`
  - [ ] Queryset: `StockReorderRule.objects.filter(active=True).select_related('product', 'warehouse', 'product__uom')`
  - [ ] Para cada regra: calcular `on_hand`, `outgoing_pending`, `qty_to_order`
  - [ ] Filtrar apenas regras onde `needs_reorder = True` (por defeito) — toggle "Todas as regras"
  - [ ] Agrupar por fornecedor preferido (`ProductSupplierInfo.get_best_supplier`) se existir (Fase 6.8)
  - [ ] Ordenar: primeiro os que têm stock = 0, depois os mais críticos (maior défice %)
  - [ ] Contexto: `suggestions` (lista), `total_items` (count), `zero_stock_count`

- [ ] **Template `templates/inventory/purchase_suggestions.html`**
  - [ ] Navbar inventário padrão
  - [ ] Header com KPIs:
    - [ ] "X produtos em falta" (stock = 0) — vermelho
    - [ ] "Y produtos abaixo do mínimo" (0 < stock < min) — laranja
    - [ ] "Z produtos OK" — verde
  - [ ] Toggle: "Só em falta" / "Todas as regras"
  - [ ] Tabela com colunas:
    - [ ] Produto (nome + ref. interna + imagem)
    - [ ] Em Mão (quantidade atual — vermelho se 0)
    - [ ] Mínimo (min_qty)
    - [ ] Saídas Previstas (outgoing_pending)
    - [ ] **A Comprar** (qty_to_order — destacado a gold)
    - [ ] UdM
    - [ ] Fornecedor Preferido (se existir, badge com nome)
    - [ ] Prazo (lead_time_days — calculado a partir das regras / ProductSupplierInfo)
  - [ ] Botão por linha: "Criar Encomenda" → ⏳ (Fase 7 — gera PurchaseOrder com este produto)
  - [ ] Botão global: "Gerar Ordens de Compra" → ⏳ (Fase 7 — agrupa por fornecedor e cria POs)
  - [ ] Empty state se nenhum produto precisa de reabastecimento

- [ ] **URL**
  - [ ] `path('operations/purchase-suggestions/', ..., name='purchase_suggestions')`

- [ ] **Link no navbar de inventário**
  - [ ] "Lista de Compras" no menu "Operações" com badge vermelho quando há itens em falta

### Notificações de Stock Mínimo

- [x] **Signal `post_save` em `StockMovement`** (state=done)
  - [x] Após validação de movimento, verificar linhas com produto.min_stock > 0
  - [x] Se on_hand < min_stock, criar Notification (type=SYSTEM) com deduplicação
  - [x] Task Celery periódica `check_low_stock_periodic` (4h) com mesma lógica
  - [ ] Signal `post_save` em `StockQuant` (alternativa futura, após 6.15.1)
  - [ ] Não repetir notificação se já existe uma ativa para o mesmo produto

- [ ] **Widget no Dashboard Principal (apps/dashboard/)**
  - [ ] Card "Lista de Compras":
    - [ ] Número de produtos abaixo do mínimo (badge vermelho urgente)
    - [ ] Top 3 produtos mais críticos (nome + quantidade em falta)
    - [ ] Link "Ver lista completa" → `purchase_suggestions`
  - [ ] Visível apenas se existirem regras de reabastecimento configuradas

### Integração com Produto (tab "Inventário" — 6.9)

- [ ] **No formulário do produto (product_form.html)**
  - [ ] No tab "Inventário", adicionar secção "Reabastecimento":
    - [ ] Campo: Stock Mínimo (`StockReorderRule.min_qty`) — editável inline
    - [ ] Campo: Stock Alvo (`StockReorderRule.max_qty`) — opcional
    - [ ] Campo: Múltiplo de Encomenda (`qty_multiple`)
    - [ ] Auto-criar/actualizar `StockReorderRule` ao guardar (se min_stock > 0)
  - [ ] Smart button "Reabastecimento" (badge vermelho quando precisa) — ⏳ futuro

### Integração com Compras (Fase 7 — placeholder)

- [ ] ⏳ **Geração automática de PurchaseOrders** (implementar na Fase 7)
  - [ ] Botão "Gerar Ordens de Compra" na `purchase_suggestions`:
    - [ ] Agrupa sugestões por fornecedor preferido (`ProductSupplierInfo`)
    - [ ] Cria 1 `PurchaseOrder` por fornecedor com as linhas respetivas
    - [ ] Se produto não tem fornecedor definido → lista numa PO "Sem Fornecedor"
  - [ ] Quando SO confirmado sem stock → auto-verificar regras e sugerir compra

### Testing

- [ ] **Testing - Lista de Compras**
  - [ ] Test: `StockReorderRule` criada funciona
  - [ ] Test: `needs_reorder` True quando on_hand < min_qty
  - [ ] Test: `qty_to_order` calcula corretamente com saídas pendentes
  - [ ] Test: `purchase_suggestions` view lista apenas produtos abaixo do mínimo
  - [ ] Test: toggle "Todas" mostra todas as regras
  - [ ] Test: widget dashboard mostra contagem correta
  - [ ] Test: signal notifica quando stock cai abaixo do mínimo

---

## 6.16 Importação de Produtos (CSV)

Importar produtos em massa via ficheiro CSV.

- [ ] **ProductImportView**
  - [ ] Upload CSV
  - [ ] Validar colunas (obrigatórias: name, product_type, sale_price)
  - [ ] Preview: mostrar 5 primeiras linhas antes de importar
  - [ ] Importar em batch
  - [ ] Resultado: "X criados, Y erros (com detalhes)"

- [ ] **Template**
  - [ ] `templates/inventory/product_import.html`

- [ ] **Rota**
  - [ ] `path('inventory/products/import/', ..., name='product_import')`

- [ ] **Testing - Import**
  - [ ] Test: importar CSV funciona
  - [ ] Test: validações funcionam
  - [ ] Test: preview mostra dados

---

## 6.17 Atualização de Menus e Navegação

Atualizar o navbar do inventário com os novos links.

- [ ] **Navbar principal de inventário**
  - [ ] Links diretos:
    - [ ] "Produtos" → product_list
    - [ ] "Stock" → stock_overview
    - [ ] "Movimentos" → stock_movement_list
  - [ ] Dropdown "Configuração":
    - [ ] Categorias, UdM, Categorias UdM (existentes)
    - [ ] Armazéns (admin link ou view simples)

- [ ] **Navbar do StockMovement (stock_movement_navbar)**
  - [ ] Links: "Movimentos" (lista), Tabs rápidas (Receções, Expedições, Ajustes)
  - [ ] Botões: Descartar, Guardar, Validar

---

## 6.19 Custo Médio Ponderado — CMVMC ✅

Implementar o Custo Médio Ponderado (Moving Weighted Average Cost) como base de todos os relatórios financeiros de inventário.

- [x] **Campo `cost_price_at_move` em `StockMovementLine`**
  - [x] `DecimalField(max_digits=10, decimal_places=4, null=True)`
  - [x] Guarda o CMVMC do produto no exato instante da validação do movimento
  - [x] Imutável após validação (registo histórico)

- [x] **Lógica em `StockMovement.action_validate()`**
  - [x] **Entrada (receipt / adjustment-in):**
    - [x] `new_avg = (on_hand_qty × old_avg + incoming_qty × unit_price) / (on_hand_qty + incoming_qty)`
    - [x] Atualiza `Product.cost_price` com o novo CMVMC (via `bulk_update`)
    - [x] Guarda `new_avg` em `line.cost_price_at_move`
  - [x] **Saída (delivery / adjustment-out):**
    - [x] `line.cost_price_at_move = product.cost_price` (custo médio corrente)
    - [x] `Product.cost_price` mantém-se inalterado (a média não muda em saídas)
  - [x] `bulk_update` em linhas e produtos para eficiência

- [x] **Migração criada e aplicada**

---

## 6.20 Relatórios de Inventário

Lista completa de relatórios a implementar. Todos usam `cost_price_at_move` como base de custo real.

### 6.20.1 Valorização de Stock (Tier 1 — Crítico) ✅
- [x] **View:** `inventory_report_valuation`
- [x] **URL:** `inventory/reports/valuation/`
- [x] **Lógica:**
  - [x] Por produto: `StockQuant.quantity × Product.cost_price` (= CMVMC atual)
  - [x] Filtros: por armazém, por categoria, por empresa
  - [x] Totais: nr. produtos, quantidade total, valor total em €
- [x] **Template:** tabela com colunas: Produto | Referência | Categoria | Qt. em Mão | UdM | Custo Médio | Valor Total
- [x] **Exportação:** botão CSV/Excel

### 6.20.2 Balancete de Inventário por Período (Tier 1 — Crítico) ✅
- [x] **View:** `inventory_report_balance`
- [x] **URL:** `inventory/reports/balance/`
- [x] **Lógica:**
  - [x] Filtro por período (data início / data fim)
  - [x] Por produto: Stock Inicial + Entradas (qt. e €) − Saídas (qt. e €) − Sucata (qt. e €) = Stock Final
  - [x] Stock inicial = valor em mão antes do período (reconstruído dos movimentos)
  - [x] Valor de entradas = `SUM(qty × cost_price_at_move)` para receipts no período
  - [x] Valor de saídas = `SUM(qty × cost_price_at_move)` para deliveries no período
- [x] **Template:** tabela com saldos de abertura e fecho em unidades e em €
- [x] **Exportação:** CSV/Excel/PDF

### 6.20.3 Histórico de Preços de Compra (Tier 1 — Crítico) ✅
- [x] **View:** `inventory_report_purchase_prices`
- [x] **URL:** `inventory/reports/purchase-prices/`
- [x] **Lógica:**
  - [x] Filtra `StockMovementLine` onde `movement_type='receipt'` e `state='done'`
  - [x] Por produto: lista cronológica de receções com preço, fornecedor, data, referência
  - [x] Mostra variação % entre compras consecutivas
  - [x] Filtros: por produto, por fornecedor, por período
- [x] **Template:** tabela por produto com histórico de preços e gráfico de tendência

### 6.20.4 Relatório de Perdas / Sucata (Tier 1 — Crítico) ✅
- [x] **View:** `inventory_report_scrap`
- [x] **URL:** `inventory/reports/scrap/`
- [x] **Lógica:**
  - [x] Quando Sucata for implementada (6.21): lista todos os registos de sucata
  - [x] Por linha: produto, quantidade, `cost_price_at_move × qty` = valor destruído, motivo, data, responsável
  - [x] Totais por período: valor total de perdas
  - [x] Filtros: por período, por motivo, por produto
- [x] **Template:** tabela + total de perdas em € + gráfico por motivo

### 6.20.5 Movimentos por Produto (Tier 2 — Operacional)
- [ ] **View:** `inventory_report_movements`
- [ ] **URL:** `inventory/reports/movements/`
- [ ] **Lógica:**
  - [ ] Seleção de produto + período
  - [ ] Lista cronológica: data, tipo (IN/OUT/ADJ), referência doc., qt., custo unitário, saldo após
  - [ ] Saldo calculado acumulativamente (running total)
- [ ] **Template:** tabela de rastreabilidade completa com saldo corrente

### 6.20.6 Produtos Abaixo do Mínimo — Detalhe (Tier 2 — Operacional)
- [ ] **View:** `inventory_report_low_stock`
- [ ] **URL:** `inventory/reports/low-stock/`
- [ ] **Lógica:**
  - [ ] Produtos com `min_stock > 0` e `StockQuant.quantity < min_stock`
  - [ ] Colunas: produto, stock atual, mínimo, diferença, fornecedor preferido (ProductSupplierInfo), último preço de compra
  - [ ] Botão "Criar Receção" por linha → pre-fill do adjustment_create
- [ ] **Template:** tabela com ação direta de reabastecimento

### 6.20.7 Stock Sem Movimento (Tier 2 — Operacional)
- [ ] **View:** `inventory_report_no_movement`
- [ ] **URL:** `inventory/reports/no-movement/`
- [ ] **Lógica:**
  - [ ] Produtos com `StockQuant.quantity > 0` mas sem `StockMovementLine` nos últimos X dias (padrão: 90 dias)
  - [ ] Filtro por número de dias configurável
  - [ ] Valor do stock parado = `quantity × cost_price`
- [ ] **Template:** tabela com valor de capital imobilizado + total

### 6.20.8 Análise ABC (Tier 3 — Analítico)
- [ ] **View:** `inventory_report_abc`
- [ ] **URL:** `inventory/reports/abc/`
- [ ] **Lógica:**
  - [ ] Calcula consumo total em € por produto no período: `SUM(qty × cost_price_at_move)` para saídas
  - [ ] Ordena por valor decrescente, calcula % acumulada
  - [ ] Classe A: 0–80% do valor total; B: 80–95%; C: 95–100%
  - [ ] Filtros: por período, por categoria
- [ ] **Template:** tabela + gráfico de Pareto

### 6.20.9 Rotação de Stock (Tier 3 — Analítico)
- [ ] **View:** `inventory_report_turnover`
- [ ] **URL:** `inventory/reports/turnover/`
- [ ] **Lógica:**
  - [ ] Fórmula: `Rotação = Custo das Saídas no Período / Valor Médio do Stock no Período`
  - [ ] Dias de stock: `365 / rotação`
  - [ ] Filtros: por período, por categoria
- [ ] **Template:** tabela por produto com rotação anualizada e dias de stock

### 6.20.10 Margem Real por Produto (Tier 3 — Analítico)
- [ ] **View:** `inventory_report_margin`
- [ ] **URL:** `inventory/reports/margin/`
- [ ] **Lógica:**
  - [ ] Para entregas: `margem = (sale_price - cost_price_at_move) / sale_price × 100`
  - [ ] Compara margem real (baseada em custo médio ponderado real) vs margem teórica (catálogo)
  - [ ] Agrega por produto no período
  - [ ] **Nota:** requer integração com Vendas (Fase 8) para ter o `sale_price` real por linha
- [ ] **Template:** tabela com margem real vs teórica, desvio em %

---



> **NOTA:** Implementar estas integrações quando chegarmos à Fase 7/8.

- [ ] **Fase 7 — Receção automática de compra**
  - [ ] Ao confirmar PurchaseOrder:
    - [ ] Auto-criar StockMovement (type=receipt, partner=supplier, origin="PO-XXXXX")
    - [ ] Auto-criar StockMovementLines a partir das PurchaseOrderLines
  - [ ] "Receber" = validar o StockMovement → stock incrementado
  - [ ] Atualizar cost_price do produto (se preço de compra mudou)

- [ ] **Fase 8 — Expedição automática de venda**
  - [ ] Ao confirmar SaleOrder:
    - [ ] Verificar stock (StockQuant.get_on_hand para cada produto)
    - [ ] Se stock suficiente → auto-criar StockMovement (type=delivery, partner=client, origin="SO-XXXXX")
    - [ ] Se stock insuficiente → ALERTA ao utilizador:
      - [ ] Opção 1: "Criar Pedido de Compra" → auto-gera PurchaseOrder com os produtos em falta
      - [ ] Opção 2: "Continuar sem stock" → cria expedição na mesma (stock fica negativo)
  - [ ] "Entregar" = validar o StockMovement → stock decrementado

---

# 🚀 FASE 7: APP - COMPRAS

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de gestão de compras e documentos de compra
**📦 Dependências:** Fase 4 (contacts), Fase 6 (inventory/products)

---

## 7.1 Criação da App 'purchases'

Criar app Django para gestão de compras.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp purchases apps/purchases`
  - [ ] Adicionar 'apps.purchases' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar models.py, views.py, forms.py, urls.py

---

## 7.2 Modelo PurchaseOrder

Criar modelo de encomenda/documento de compra.

- [ ] **Criar modelo PurchaseOrder**
  - [ ] Herdar de BaseModel
  - [ ] Campos: order_number (único, auto-gerado), supplier (FK Contact)
  - [ ] Campos: order_date, expected_delivery_date
  - [ ] Campos: status (DRAFT, CONFIRMED, RECEIVED, CANCELLED)
  - [ ] Campos: subtotal, tax, total (calculados)
  - [ ] Campos: notes
  - [ ] Campo: **owner_company** (FK para Company, null=True, blank=True) - NULL=global, com valor=privado
  - [ ] Método __str__, método generate_order_number()
  - [ ] Filtrar por owner_company na PurchaseOrderListView usando filter_by_company()
  - [ ] Auto-preencher owner_company na create view com get_active_company()

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar PurchaseOrderAdmin
  - [ ] list_display: order_number, supplier, order_date, status, total

- [ ] **Testing - PurchaseOrder**
  - [ ] Test: criar purchase order funciona
  - [ ] Test: order_number é gerado automaticamente

---

## 7.3 Modelo PurchaseOrderLine

Criar linhas de produtos da encomenda.

- [ ] **Criar modelo PurchaseOrderLine**
  - [ ] Campos: purchase_order (FK), product (FK)
  - [ ] Campos: quantity, unit_price, tax_rate, line_total
  - [ ] Método calculate_line_total()

- [ ] **Criar signal para recalcular total**
  - [ ] Ao salvar/deletar linha, recalcular total do PurchaseOrder

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Testing - PurchaseOrderLine**
  - [ ] Test: adicionar linha atualiza total
  - [ ] Test: remover linha atualiza total

---

## 7.4 Views de Listagem de Compras

Criar views para listar purchase orders.

- [ ] **Criar PurchaseOrderListView**
  - [ ] Listar todas as encomendas
  - [ ] Filtros: status, supplier, data
  - [ ] Busca por order_number

- [ ] **Criar template**
  - [ ] `templates/purchases/order_list.html` (standalone)
  - [ ] Tabela com: order_number, supplier, date, status, total, actions

- [ ] **Configurar rota**
  - [ ] `path('purchases/', PurchaseOrderListView, name='purchase_list')`

- [ ] **Testing - Purchase List**
  - [ ] Test: listar compras funciona
  - [ ] Test: filtros funcionam

---

## 7.5 Views de Criação de Compra

Criar view para criar nova compra.

- [ ] **Criar PurchaseOrderCreateView**
  - [ ] Form principal: supplier, order_date, expected_delivery_date
  - [ ] JavaScript para adicionar linhas dinamicamente
  - [ ] Calcular totais em tempo real (JS)

- [ ] **Criar template**
  - [ ] `templates/purchases/order_create.html` (standalone)
  - [ ] Form com tabela de linhas dinâmicas
  - [ ] Botão "Adicionar Produto"

- [ ] **Configurar rota**
  - [ ] `path('purchases/new/', PurchaseOrderCreateView, name='purchase_create')`

- [ ] **Testing - Purchase Create**
  - [ ] Test: criar compra funciona
  - [ ] Test: adicionar múltiplas linhas funciona
  - [ ] Test: totais são calculados

---

## 7.6 Views de Edição e Detalhes

Criar views para editar e visualizar compra.

- [ ] **Criar PurchaseOrderDetailView**
  - [ ] Mostrar cabeçalho e linhas
  - [ ] Botões de ação: Editar, Confirmar, Receber, Cancelar

- [ ] **Criar PurchaseOrderUpdateView**
  - [ ] Permitir editar apenas se status=DRAFT
  - [ ] Form com linhas editáveis

- [ ] **Criar templates**
  - [ ] `templates/purchases/order_detail.html` (standalone)
  - [ ] `templates/purchases/order_update.html` (standalone)

- [ ] **Configurar rotas**
  - [ ] `path('purchases/<uuid:pk>/', PurchaseOrderDetailView, name='purchase_detail')`
  - [ ] `path('purchases/<uuid:pk>/edit/', PurchaseOrderUpdateView, name='purchase_update')`

- [ ] **Testing - Purchase Edit/Detail**
  - [ ] Test: visualizar detalhes funciona
  - [ ] Test: editar compra DRAFT funciona
  - [ ] Test: não permite editar compra CONFIRMED

---

## 7.7 Confirmação de Compra

Criar ação para confirmar compra (mudar status para CONFIRMED).

- [ ] **Criar PurchaseOrderConfirmView**
  - [ ] Verificar se tem linhas
  - [ ] Mudar status para CONFIRMED
  - [ ] Enviar email ao supplier (opcional)

- [ ] **Configurar rota**
  - [ ] `path('purchases/<uuid:pk>/confirm/', PurchaseOrderConfirmView, name='purchase_confirm')`

- [ ] **Testing - Purchase Confirm**
  - [ ] Test: confirmar compra funciona
  - [ ] Test: status muda para CONFIRMED

---

## 7.8 Receção de Compra (Entrada de Stock)

Criar ação para receber compra e dar entrada no stock.

- [ ] **Criar PurchaseOrderReceiveView**
  - [ ] Verificar se status=CONFIRMED
  - [ ] Para cada linha, criar StockMovement (IN)
  - [ ] Atualizar stock automaticamente
  - [ ] Mudar status para RECEIVED

- [ ] **Configurar rota**
  - [ ] `path('purchases/<uuid:pk>/receive/', PurchaseOrderReceiveView, name='purchase_receive')`

- [ ] **Testing - Purchase Receive**
  - [ ] Test: receber compra funciona
  - [ ] Test: stock é atualizado para todos os produtos
  - [ ] Test: StockMovements são criados

---

## 7.9 Cancelamento de Compra

Criar ação para cancelar compra.

- [ ] **Criar PurchaseOrderCancelView**
  - [ ] Permitir apenas se status != RECEIVED
  - [ ] Mudar status para CANCELLED
  - [ ] Confirmação antes de cancelar

- [ ] **Criar template de confirmação**
  - [ ] `templates/purchases/order_confirm_cancel.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('purchases/<uuid:pk>/cancel/', PurchaseOrderCancelView, name='purchase_cancel')`

- [ ] **Testing - Purchase Cancel**
  - [ ] Test: cancelar compra funciona
  - [ ] Test: não permite cancelar se RECEIVED

---

## 7.10 Relatórios de Compras

Criar views de relatórios de compras.

- [ ] **Criar PurchaseReportView**
  - [ ] Filtros: período, supplier, status
  - [ ] Mostrar: total de compras, produtos mais comprados
  - [ ] Gráfico de compras por mês (opcional)

- [ ] **Criar template**
  - [ ] `templates/purchases/reports.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('purchases/reports/', PurchaseReportView, name='purchase_reports')`

- [ ] **Testing - Purchase Reports**
  - [ ] Test: relatório mostra dados corretos
  - [ ] Test: filtros funcionam

---

## 7.11 Relações e Smart Buttons - Módulo Compras

**OBJETIVO:** Documentar todas as relações FK que Compras terão com outros módulos + criar smart buttons bidirecionais + vistas de listagem.

- [ ] **Relações FK Diretas (PurchaseOrder → outros módulos)**
  - [ ] **FK para Contact (Supplier)**:
    - [ ] Campo `supplier = ForeignKey(Contact, on_delete=PROTECT, related_name='purchases')`
    - [ ] Validar: `supplier.contact_type` deve ser 'SUPPLIER' ou 'BOTH'
    - [ ] Bidirecional: Contact terá smart button "Compras" (ver Fase 4.10)
  - [ ] **FK para Products (via PurchaseOrderLine)**:
    - [ ] `PurchaseOrderLine.product = ForeignKey(Product, on_delete=PROTECT, related_name='purchase_lines')`
    - [ ] Bidirecional: Product terá smart button "Compras" (ver Fase 5.13)

- [ ] **Relações FK Recebidas (outros módulos → PurchaseOrder)**
  - [ ] **Faturas de Fornecedor** (Fase 8):
    - [ ] Modelo `SupplierInvoice` terá campo `purchase_order = ForeignKey(PurchaseOrder, on_delete=SET_NULL, null=True, blank=True, related_name='invoices')`
    - [ ] Smart button: "Faturas" no formulário de PurchaseOrder
    - [ ] Vista: `purchase_invoices_list(purchase_id)` usando template base
    - [ ] Rota: `/purchases/<uuid:pk>/invoices/`
    - [ ] Colunas tabela: Nº Fatura, Data, Total, Estado Pagamento
    - [ ] Se 1 fatura → redireciona para `invoice_detail(pk)`
    - [ ] Se múltiplas → mostra lista clicável
  - [ ] **Movimentos Stock** (criados automaticamente ao receber compra):
    - [ ] `StockMovement.reference_doc` pode referenciar PurchaseOrder (via string ou GenericFK)
    - [ ] Smart button: "Movimentos Stock" no formulário de PurchaseOrder
    - [ ] Vista: `purchase_stock_movements_list(purchase_id)` usando template base
    - [ ] Rota: `/purchases/<uuid:pk>/stock-movements/`
    - [ ] Colunas tabela: Data, Produto, Quantidade, Tipo (IN), User
    - [ ] Sempre mostra lista (mesmo se poucos movimentos)

- [ ] **Método Helper para Contadores**
  - [ ] Adicionar método `PurchaseOrder.get_stats()` no modelo PurchaseOrder:
    ```python
    def get_stats(self):
        return {
            'lines_count': self.lines.count(),
            'invoices_count': self.invoices.count(),
            'stock_movements_count': StockMovement.objects.filter(reference_doc=str(self.pk)).count(),
            'total_received': self.status == 'RECEIVED',
        }
    ```
  - [ ] No template do formulário PurchaseOrder, chamar `purchase.get_stats` para popular os smart buttons

- [ ] **Testing - Purchase Relations**
  - [ ] Test: `purchase.get_stats()` retorna contadores corretos
  - [ ] Test: smart button Faturas funciona
  - [ ] Test: smart button Movimentos Stock mostra apenas desta compra
  - [ ] Test: vistas usam template base corretamente
  - [ ] Test: bidirecionalidade funciona (Contact ↔ Purchase, Product ↔ Purchase)

---

# 🚀 FASE 8: APP - VENDAS

**⏱ Tempo estimado:** 5-6 dias
**🎯 Objetivo:** Criar sistema de vendas, orçamentos, encomendas e faturas
**📦 Dependências:** Fase 4 (contacts/clients), Fase 6 (inventory), Fase 7 (estrutura similar)

---

## 8.1 Criação da App 'sales'

Criar app Django para gestão de vendas.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp sales apps/sales`
  - [ ] Adicionar 'apps.sales' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar models.py, views.py, forms.py, urls.py

---

## 8.2 Modelo SaleOrder

Criar modelo de encomenda de venda / orçamento / fatura.

- [ ] **Criar modelo SaleOrder**
  - [ ] Herdar de BaseModel
  - [ ] Campos: order_number (único, auto), client (FK Contact)
  - [ ] Campos: order_date, delivery_date
  - [ ] Campos: document_type (QUOTATION, ORDER, INVOICE)
  - [ ] Campos: status (DRAFT, CONFIRMED, DELIVERED, INVOICED, CANCELLED)
  - [ ] Campos: subtotal, tax, total, discount
  - [ ] Campos: payment_method, payment_status (UNPAID, PARTIAL, PAID)
  - [ ] Campos: notes
  - [ ] Campo: **owner_company** (FK para Company, null=True, blank=True) - NULL=global, com valor=privado
  - [ ] Método __str__, método generate_order_number()
  - [ ] Filtrar por owner_company na SaleOrderListView usando filter_by_company()
  - [ ] Auto-preencher owner_company na create view com get_active_company()

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar SaleOrderAdmin
  - [ ] list_display: order_number, client, order_date, document_type, status, total

- [ ] **Testing - SaleOrder**
  - [ ] Test: criar sale order funciona
  - [ ] Test: order_number é gerado

---

## 8.3 Modelo SaleOrderLine

Criar linhas de produtos da venda.

- [ ] **Criar modelo SaleOrderLine**
  - [ ] Campos: sale_order (FK), product (FK)
  - [ ] Campos: quantity, unit_price, tax_rate, discount, line_total
  - [ ] Método calculate_line_total()

- [ ] **Criar signal para recalcular total**
  - [ ] Ao salvar/deletar linha, recalcular total do SaleOrder

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Testing - SaleOrderLine**
  - [ ] Test: adicionar linha atualiza total
  - [ ] Test: discount é aplicado corretamente

---

## 8.4 Views de Listagem de Vendas

Criar views para listar sale orders.

- [ ] **Criar SaleOrderListView**
  - [ ] Listar todas as vendas
  - [ ] Filtros: status, document_type, client, data
  - [ ] Busca por order_number
  - [ ] Tabs: Todos, Orçamentos, Encomendas, Faturas

- [ ] **Criar template**
  - [ ] `templates/sales/order_list.html` (standalone)
  - [ ] Tabela com: order_number, client, date, type, status, total, actions

- [ ] **Configurar rota**
  - [ ] `path('sales/', SaleOrderListView, name='sale_list')`

- [ ] **Testing - Sale List**
  - [ ] Test: listar vendas funciona
  - [ ] Test: filtros e tabs funcionam

---

## 8.5 Views de Criação de Venda/Orçamento

Criar view para criar nova venda.

- [ ] **Criar SaleOrderCreateView**
  - [ ] Form: client, order_date, delivery_date, document_type
  - [ ] JavaScript para adicionar linhas dinamicamente
  - [ ] Calcular totais em tempo real (JS)
  - [ ] Aplicar descontos por linha ou global

- [ ] **Criar template**
  - [ ] `templates/sales/order_create.html` (standalone)
  - [ ] Form com tabela de linhas dinâmicas
  - [ ] Seletor de produtos com busca

- [ ] **Configurar rota**
  - [ ] `path('sales/new/', SaleOrderCreateView, name='sale_create')`

- [ ] **Testing - Sale Create**
  - [ ] Test: criar venda funciona
  - [ ] Test: criar orçamento funciona
  - [ ] Test: totais e descontos calculados

---

## 8.6 Views de Edição e Detalhes

Criar views para editar e visualizar venda.

- [ ] **Criar SaleOrderDetailView**
  - [ ] Mostrar cabeçalho e linhas
  - [ ] Botões de ação: Editar, Confirmar, Entregar, Faturar, Cancelar
  - [ ] Link para gerar PDF

- [ ] **Criar SaleOrderUpdateView**
  - [ ] Permitir editar apenas se status=DRAFT
  - [ ] Form com linhas editáveis

- [ ] **Criar templates**
  - [ ] `templates/sales/order_detail.html` (standalone)
  - [ ] `templates/sales/order_update.html` (standalone)

- [ ] **Configurar rotas**
  - [ ] `path('sales/<uuid:pk>/', SaleOrderDetailView, name='sale_detail')`
  - [ ] `path('sales/<uuid:pk>/edit/', SaleOrderUpdateView, name='sale_update')`

- [ ] **Testing - Sale Edit/Detail**
  - [ ] Test: visualizar detalhes funciona
  - [ ] Test: editar venda DRAFT funciona

---

## 8.7 Confirmação de Venda

Criar ação para confirmar venda.

- [ ] **Criar SaleOrderConfirmView**
  - [ ] Verificar se tem linhas
  - [ ] Mudar status para CONFIRMED
  - [ ] Enviar email ao cliente (opcional)

- [ ] **Configurar rota**
  - [ ] `path('sales/<uuid:pk>/confirm/', SaleOrderConfirmView, name='sale_confirm')`

- [ ] **Testing - Sale Confirm**
  - [ ] Test: confirmar venda funciona
  - [ ] Test: status muda para CONFIRMED

---

## 8.8 Entrega de Venda (Saída de Stock)

Criar ação para marcar como entregue e dar saída no stock.

- [ ] **Criar SaleOrderDeliverView**
  - [ ] Verificar se status=CONFIRMED
  - [ ] Para cada linha, criar StockMovement (OUT)
  - [ ] Verificar se há stock suficiente
  - [ ] Atualizar stock automaticamente
  - [ ] Mudar status para DELIVERED

- [ ] **Configurar rota**
  - [ ] `path('sales/<uuid:pk>/deliver/', SaleOrderDeliverView, name='sale_deliver')`

- [ ] **Testing - Sale Deliver**
  - [ ] Test: entregar venda funciona
  - [ ] Test: stock é reduzido
  - [ ] Test: alerta se stock insuficiente

---

## 8.9 Faturação de Venda

Criar ação para gerar fatura.

- [ ] **Criar SaleOrderInvoiceView**
  - [ ] Verificar se status=DELIVERED
  - [ ] Mudar document_type para INVOICE (ou criar novo documento)
  - [ ] Mudar status para INVOICED
  - [ ] Registrar no sistema financeiro

- [ ] **Configurar rota**
  - [ ] `path('sales/<uuid:pk>/invoice/', SaleOrderInvoiceView, name='sale_invoice')`

- [ ] **Testing - Sale Invoice**
  - [ ] Test: faturar venda funciona
  - [ ] Test: status muda para INVOICED

---

## 8.10 Cancelamento de Venda

Criar ação para cancelar venda.

- [ ] **Criar SaleOrderCancelView**
  - [ ] Permitir apenas se status != DELIVERED/INVOICED
  - [ ] Mudar status para CANCELLED
  - [ ] Se já confirmado, reverter stock (opcional)

- [ ] **Criar template de confirmação**
  - [ ] `templates/sales/order_confirm_cancel.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('sales/<uuid:pk>/cancel/', SaleOrderCancelView, name='sale_cancel')`

- [ ] **Testing - Sale Cancel**
  - [ ] Test: cancelar venda funciona

---

## 8.11 Envio de Documentos por Email

Criar funcionalidade para enviar orçamentos/faturas por email.

- [ ] **Criar SaleOrderSendEmailView**
  - [ ] Gerar PDF do documento
  - [ ] Enviar email ao cliente com PDF anexado
  - [ ] Template de email customizável

- [ ] **Adicionar botão no detail**
  - [ ] Botão "Enviar por Email"

- [ ] **Configurar rota**
  - [ ] `path('sales/<uuid:pk>/send-email/', SaleOrderSendEmailView, name='sale_send_email')`

- [ ] **Testing - Sale Send Email**
  - [ ] Test: enviar email funciona
  - [ ] Test: PDF é anexado

---

## 8.12 Relatórios de Vendas

Criar views de relatórios de vendas.

- [ ] **Criar SaleReportView**
  - [ ] Filtros: período, client, status, document_type
  - [ ] Mostrar: total de vendas, produtos mais vendidos, clientes top
  - [ ] Gráfico de vendas por mês

- [ ] **Criar template**
  - [ ] `templates/sales/reports.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('sales/reports/', SaleReportView, name='sale_reports')`

- [ ] **Testing - Sale Reports**
  - [ ] Test: relatório mostra dados corretos
  - [ ] Test: filtros funcionam

---

## 8.13 Sistema de Price Lists

Criar sistema de listas de preços e regras de desconto por cliente/empresa.

- [ ] **Criar modelo PriceList**
  - [ ] Criar em `apps/sales/models.py`
  - [ ] Campos: name, description, is_active, priority
  - [ ] Campos: discount_type (PERCENTAGE, FIXED, QUANTITY_BASED, VALUE_BASED)
  - [ ] Campos: discount_value, min_quantity, min_amount
  - [ ] Método calculate_discount(quantity, unit_price)

- [ ] **Associar PriceList a Contact**
  - [ ] Adicionar campo price_list (FK) em Contact model
  - [ ] Migration para adicionar campo
  - [ ] Contact herda price_list da empresa pai se for colaborador

- [ ] **Criar modelo PriceListRule**
  - [ ] Campos: price_list (FK), product (FK, opcional)
  - [ ] Campos: category (FK, opcional) - desconto por categoria
  - [ ] Campos: discount_percentage, discount_fixed
  - [ ] Campos: min_quantity, max_quantity
  - [ ] Prioridade: regra específica de produto > categoria > geral

- [ ] **Integrar com SaleOrder**
  - [ ] Ao selecionar cliente, carregar price_list automaticamente
  - [ ] Ao adicionar produto, aplicar desconto do price_list
  - [ ] Calcular desconto progressivo se quantity_based
  - [ ] Mostrar desconto aplicado na linha

- [ ] **Criar views de gestão**
  - [ ] PriceListListView - listar price lists
  - [ ] PriceListCreateView - criar price list com regras
  - [ ] PriceListUpdateView - editar price list e regras inline
  - [ ] Template: `templates/sales/pricelist_list.html` (standalone)
  - [ ] Template: `templates/sales/pricelist_form.html` (standalone)

- [ ] **Criar página de associação**
  - [ ] View para associar price list a múltiplos contactos
  - [ ] Bulk update de contactos
  - [ ] Filtros: empresa, tipo de contacto

- [ ] **Registrar no Admin**
  - [ ] PriceListAdmin com PriceListRuleInline
  - [ ] Configurar list_display, search, filters

- [ ] **Testing - Price Lists**
  - [ ] Test: criar price list funciona
  - [ ] Test: associar price list a contacto
  - [ ] Test: desconto é aplicado automaticamente em venda
  - [ ] Test: desconto progressivo por quantidade funciona
  - [ ] Test: colaborador herda price list da empresa
  - [ ] Test: prioridade de regras (produto > categoria > geral)

---

## 8.14 Relações e Smart Buttons - Módulo Vendas

**OBJETIVO:** Documentar todas as relações FK que Vendas terão com outros módulos + criar smart buttons bidirecionais (incluindo triângulos CRM→Venda→Contacto) + vistas de listagem.

- [ ] **Relações FK Diretas (SaleOrder → outros módulos)**
  - [ ] **FK para Contact (Client)**:
    - [ ] Campo `contact = ForeignKey(Contact, on_delete=PROTECT, related_name='sales')`
    - [ ] Validar: `contact.contact_type` deve ser 'CLIENT' ou 'BOTH'
    - [ ] Bidirecional: Contact terá smart button "Vendas" (ver Fase 4.10)
  - [ ] **FK para Products (via SaleOrderLine)**:
    - [ ] `SaleOrderLine.product = ForeignKey(Product, on_delete=PROTECT, related_name='sale_lines')`
    - [ ] Bidirecional: Product terá smart button "Vendas" (ver Fase 5.13)
  - [ ] **FK para CRM/Lead** (origem da venda) - RELAÇÃO TRIANGULAR:
    - [ ] Campo `lead = ForeignKey(Lead, on_delete=SET_NULL, null=True, blank=True, related_name='sales')`
    - [ ] **Triângulo de relações:** Contact ↔ Lead ↔ SaleOrder
      - [ ] Contact tem Lead (Contact.leads)
      - [ ] Lead gerou Venda (Lead.sales)
      - [ ] Venda pertence a Contact (SaleOrder.contact)
    - [ ] Smart button no Lead: "Vendas Geradas" (quantas vendas esta lead gerou)
    - [ ] Smart button no SaleOrder: "Lead Origem" (qual lead gerou esta venda, se houver)
    - [ ] Vista: `lead_sales_list(lead_id)` usando template base
    - [ ] Rota: `/crm/leads/<uuid:pk>/sales/`
    - [ ] Se 1 venda → redireciona para `sale_detail(pk)`
    - [ ] Se múltiplas → mostra lista clicável

- [ ] **Relações FK Recebidas (outros módulos → SaleOrder)**
  - [ ] **Faturas de Cliente** (Fase 8):
    - [ ] Modelo `Invoice` terá campo `sale_order = ForeignKey(SaleOrder, on_delete=PROTECT, related_name='invoices')`
    - [ ] Smart button: "Faturas" no formulário de SaleOrder
    - [ ] Vista: `sale_invoices_list(sale_id)` usando template base
    - [ ] Rota: `/sales/<uuid:pk>/invoices/`
    - [ ] Colunas tabela: Nº Fatura, Data, Total, Estado Pagamento
    - [ ] Se 1 fatura → redireciona para `invoice_detail(pk)`
    - [ ] Se múltiplas → mostra lista clicável
  - [ ] **Movimentos Stock** (criados automaticamente ao entregar venda):
    - [ ] `StockMovement.reference_doc` pode referenciar SaleOrder
    - [ ] Smart button: "Movimentos Stock" no formulário de SaleOrder (saídas de produtos)
    - [ ] Vista: `sale_stock_movements_list(sale_id)` usando template base
    - [ ] Rota: `/sales/<uuid:pk>/stock-movements/`
    - [ ] Colunas tabela: Data, Produto, Quantidade, Tipo (OUT), User
    - [ ] Sempre mostra lista
  - [ ] **Documentos/PDFs** (Fase 10):
    - [ ] Modelo `Document` terá FK opcional para SaleOrder
    - [ ] Smart button: "Documentos" no formulário de SaleOrder (orçamentos PDF, contratos)
    - [ ] Vista: `sale_documents_list(sale_id)` usando template base
    - [ ] Rota: `/sales/<uuid:pk>/documents/`
    - [ ] Se 1 documento → abre PDF diretamente
    - [ ] Se múltiplos → mostra lista

- [ ] **EXCEÇÕES - Smart Buttons que NÃO devem existir:**
  - [ ] ❌ **NÃO criar** smart button "Produtos Vendidos" em SaleOrder
    - [ ] Razão: Produtos já estão visíveis nas linhas (SaleOrderLines) dentro do próprio formulário
    - [ ] Redundante ter botão separado para isso
  - [ ] ❌ **NÃO criar** smart button reverso "Vendas que usaram este produto" em Product
    - [ ] Já existe smart button "Vendas" em Product (via sale_lines)
    - [ ] Ver Fase 5.13 para implementação

- [ ] **Método Helper para Contadores**
  - [ ] Adicionar método `SaleOrder.get_stats()` no modelo SaleOrder:
    ```python
    def get_stats(self):
        return {
            'lines_count': self.lines.count(),
            'invoices_count': self.invoices.count(),
            'stock_movements_count': StockMovement.objects.filter(reference_doc=str(self.pk)).count(),
            'documents_count': self.documents.count(),
            'has_lead': bool(self.lead),
            'total_delivered': self.status in ['DELIVERED', 'INVOICED'],
        }
    ```
  - [ ] No template do formulário SaleOrder, chamar `sale.get_stats` para popular os smart buttons

- [ ] **Testing - Sale Relations**
  - [ ] Test: `sale.get_stats()` retorna contadores corretos
  - [ ] Test: triângulo Contact ↔ Lead ↔ Sale funciona bidirecionalmente
  - [ ] Test: smart button Lead Origem só aparece se `sale.lead` existe
  - [ ] Test: smart button Faturas funciona
  - [ ] Test: smart button Movimentos Stock mostra apenas desta venda
  - [ ] Test: vistas usam template base corretamente
  - [ ] Test: bidirecionalidade funciona (Contact ↔ Sale, Product ↔ Sale, Lead ↔ Sale)
  - [ ] Test: botão "Produtos Vendidos" NÃO existe (redundante com linhas)

---

# 🚀 FASE 9: APP - FINANCEIRO

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de gestão financeira, balanços, perdas e ganhos
**📦 Dependências:** Fase 7 (compras), Fase 8 (vendas)

---

## 9.1 Criação da App 'finance'

Criar app Django para gestão financeira.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp finance apps/finance`
  - [ ] Adicionar 'apps.finance' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar models.py, views.py, urls.py

---

## 9.2 Modelo Transaction

Criar modelo para transações financeiras.

- [ ] **Criar modelo Transaction**
  - [ ] Herdar de BaseModel
  - [ ] Campos: transaction_date, transaction_type (INCOME, EXPENSE, LOSS)
  - [ ] Campos: category (SALE, PURCHASE, ADJUSTMENT, OTHER)
  - [ ] Campos: amount, description
  - [ ] Campos: related_document (GenericForeignKey para SaleOrder/PurchaseOrder)
  - [ ] Método __str__

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar TransactionAdmin

- [ ] **Testing - Transaction**
  - [ ] Test: criar transação funciona

---

## 9.3 Signal para Criar Transações Automáticas

Criar signals para criar transações automaticamente.

- [ ] **Signal para SaleOrder INVOICED**
  - [ ] Quando SaleOrder.status = INVOICED
  - [ ] Criar Transaction (INCOME, SALE) com amount = total

- [ ] **Signal para PurchaseOrder RECEIVED**
  - [ ] Quando PurchaseOrder.status = RECEIVED
  - [ ] Criar Transaction (EXPENSE, PURCHASE) com amount = total

- [ ] **Signal para StockMovement ADJUSTMENT com is_loss**
  - [ ] Quando StockMovement.movement_type = ADJUSTMENT e is_loss = True
  - [ ] Criar Transaction (LOSS, ADJUSTMENT) com amount = cost_price * quantity

- [ ] **Testing - Signals**
  - [ ] Test: faturar venda cria transação de income
  - [ ] Test: receber compra cria transação de expense
  - [ ] Test: ajuste de stock com perda cria transação de loss

---

## 9.4 View de Extrato Financeiro

Criar view para visualizar todas as transações.

- [ ] **Criar TransactionListView**
  - [ ] Listar todas as transações
  - [ ] Filtros: período, tipo, categoria
  - [ ] Mostrar saldo acumulado

- [ ] **Criar template**
  - [ ] `templates/finance/transaction_list.html` (standalone)
  - [ ] Tabela com: data, tipo, categoria, descrição, valor

- [ ] **Configurar rota**
  - [ ] `path('finance/transactions/', TransactionListView, name='transaction_list')`

- [ ] **Testing - Transaction List**
  - [ ] Test: listar transações funciona
  - [ ] Test: filtros funcionam

---

## 9.5 Balanço Mensal

Criar view para mostrar balanço mensal.

- [ ] **Criar MonthlyBalanceView**
  - [ ] Seletor de mês/ano
  - [ ] Calcular: Total Income, Total Expense, Total Loss
  - [ ] Calcular: Lucro Líquido = Income - Expense - Loss
  - [ ] Mostrar discriminação por categoria

- [ ] **Criar template**
  - [ ] `templates/finance/monthly_balance.html` (standalone)
  - [ ] Cards com totais
  - [ ] Tabela de discriminação

- [ ] **Configurar rota**
  - [ ] `path('finance/balance/', MonthlyBalanceView, name='monthly_balance')`

- [ ] **Testing - Monthly Balance**
  - [ ] Test: balanço calcula corretamente
  - [ ] Test: discriminação mostra detalhes

---

## 9.6 Relatório de Perdas e Ganhos

Criar relatório detalhado de P&L.

- [ ] **Criar ProfitLossReportView**
  - [ ] Filtros: período (mês, trimestre, ano)
  - [ ] Discriminação detalhada:
    - [ ] Vendas por produto
    - [ ] Compras por fornecedor
    - [ ] Perdas por motivo
  - [ ] Gráficos (opcional)

- [ ] **Criar template**
  - [ ] `templates/finance/profit_loss.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('finance/profit-loss/', ProfitLossReportView, name='profit_loss')`

- [ ] **Testing - P&L Report**
  - [ ] Test: relatório mostra dados corretos
  - [ ] Test: discriminações detalhadas

---

## 9.7 Dashboard Financeiro

Criar dashboard com resumo financeiro.

- [ ] **Criar FinanceDashboardView**
  - [ ] Cards: Income Mês, Expense Mês, Lucro Mês
  - [ ] Gráfico de evolução mensal
  - [ ] Top 5 clientes (faturação)
  - [ ] Top 5 produtos vendidos

- [ ] **Criar template**
  - [ ] `templates/finance/dashboard.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('finance/dashboard/', FinanceDashboardView, name='finance_dashboard')`

- [ ] **Testing - Finance Dashboard**
  - [ ] Test: dashboard mostra dados corretos
  - [ ] Test: cards atualizam com dados reais

---

## 9.8 Exportação de Relatórios Financeiros

Permitir exportar relatórios para Excel/CSV.

- [ ] **Criar FinanceExportView**
  - [ ] Exportar extrato de transações
  - [ ] Exportar balanço mensal
  - [ ] Formato: CSV ou Excel

- [ ] **Adicionar botões de export**
  - [ ] Botão "Exportar" nas views de relatórios

- [ ] **Configurar rota**
  - [ ] `path('finance/export/', FinanceExportView, name='finance_export')`

- [ ] **Testing - Finance Export**
  - [ ] Test: exportar funciona
  - [ ] Test: arquivo contém dados corretos

---

# 🚀 FASE 10: BOM (BILL OF MATERIALS) - SISTEMA DE RECEITAS E CONFIGURADOR DE BOLOS

**⏱ Tempo estimado:** 6-8 dias
**🎯 Objetivo:** Criar sistema robusto de BOM multi-nível com cálculo automático de custos em cascata, gestão de componentes, unidades de medida, conversões e custos de mão-de-obra
**📦 Dependências:** Fase 6 (inventory/products) - Product model DEVE já existir

---

## 10.1 Criação da App 'bom'

Criar app Django para gestão de Bill of Materials (Receitas).

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp bom apps/bom`
  - [ ] Adicionar 'apps.bom' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar models.py, views.py, forms.py, urls.py, utils.py

---

## 10.2 Atualização do Modelo Product (Fase 5)

Adicionar campos necessários no modelo Product existente para suportar BOM.

- [ ] **Criar migration para adicionar campos**
  - [ ] Adicionar campo `product_type`: CHOICES ['RAW_MATERIAL', 'COMPONENT', 'FINISHED_PRODUCT']
  - [ ] Adicionar campo `has_bom`: Boolean (default=False)
  - [ ] Adicionar campo `bom_cost`: Decimal (custo calculado via BOM, nullable)
  - [ ] Adicionar campo `labor_cost_per_unit`: Decimal (custo de mão-de-obra por unidade)
  - [ ] Adicionar campo `uom` (FK para UnitOfMeasure - criar depois)

- [ ] **Atualizar Product Admin**
  - [ ] Adicionar novos campos ao list_display
  - [ ] Adicionar filtro por product_type
  - [ ] Adicionar indicador visual se has_bom=True

- [ ] **Testing - Product Update**
  - [ ] Test: migration aplicada sem erros
  - [ ] Test: produtos existentes mantêm dados
  - [ ] Test: novos campos aparecem no admin

---

## 10.3 Modelo UnitOfMeasure (Unidades de Medida)

Criar sistema de unidades de medida para conversões precisas.

- [ ] **Criar modelo UnitOfMeasure**
  - [ ] Campos: name (ex: 'Quilograma', 'Grama', 'Litro', 'Unidade', 'Fatia')
  - [ ] Campos: abbreviation ('KG', 'G', 'L', 'UN', 'SLICE')
  - [ ] Campos: category: CHOICES ['WEIGHT', 'VOLUME', 'UNIT']
  - [ ] Campos: is_reference (Boolean - unidade base da categoria)
  - [ ] Método __str__ retorna abbreviation

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Criar data migration para unidades padrão**
  - [ ] Criar: KG (WEIGHT, reference), G (WEIGHT), MG (WEIGHT)
  - [ ] Criar: L (VOLUME, reference), ML (VOLUME)
  - [ ] Criar: UN (UNIT, reference)
  - [ ] Criar: SLICE (UNIT), DOZEN (UNIT)

- [ ] **Registrar no Admin**
  - [ ] Criar UnitOfMeasureAdmin
  - [ ] list_display: name, abbreviation, category, is_reference
  - [ ] list_filter: category

- [ ] **Testing - UnitOfMeasure**
  - [ ] Test: criar unidade de medida funciona
  - [ ] Test: data migration cria unidades padrão
  - [ ] Test: visualizar no admin

---

## 10.4 Modelo UnitConversion (Conversões entre Unidades)

Criar sistema de conversões automáticas entre unidades.

- [ ] **Criar modelo UnitConversion**
  - [ ] Campos: from_uom (FK → UnitOfMeasure)
  - [ ] Campos: to_uom (FK → UnitOfMeasure)
  - [ ] Campos: factor (Decimal) - ex: 1 KG = 1000 G → factor=1000
  - [ ] Constraint: from_uom e to_uom devem ter mesma category
  - [ ] Método __str__: "1 KG = 1000 G"

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Criar data migration para conversões padrão**
  - [ ] KG → G: factor=1000
  - [ ] KG → MG: factor=1000000
  - [ ] G → MG: factor=1000
  - [ ] L → ML: factor=1000
  - [ ] DOZEN → UN: factor=12

- [ ] **Criar função de conversão em utils.py**
  - [ ] Função `convert_quantity(value, from_uom, to_uom)`
  - [ ] Verificar se conversão existe
  - [ ] Aplicar factor (direto ou inverso)
  - [ ] Retornar valor convertido com alta precisão (Decimal)

- [ ] **Registrar no Admin**
  - [ ] Criar UnitConversionAdmin
  - [ ] list_display: from_uom, to_uom, factor

- [ ] **Testing - UnitConversion**
  - [ ] Test: conversão KG → G funciona (1 → 1000)
  - [ ] Test: conversão G → KG funciona (1000 → 1)
  - [ ] Test: converter entre categorias diferentes retorna erro
  - [ ] Test: alta precisão mantida (ex: 0.0015)

---

## 10.5 Modelo ProductBOM (Receita/Lista de Materiais)

Criar modelo de Bill of Materials (receita) para produtos manufaturados.

- [ ] **Criar modelo ProductBOM**
  - [ ] Campos: product (OneToOne → Product) - produto que esta receita produz
  - [ ] Campos: name (ex: "Receita Massa Fina Standard")
  - [ ] Campos: quantity_produced (Decimal) - quantidade produzida (ex: 1.0)
  - [ ] Campos: uom_produced (FK → UnitOfMeasure) - unidade do produzido
  - [ ] Campos: labor_time_minutes (Integer) - tempo de mão-de-obra em minutos
  - [ ] Campos: labor_cost_per_hour (Decimal) - custo por hora de trabalho
  - [ ] Campos: total_component_cost (Decimal, auto-calculado)
  - [ ] Campos: total_labor_cost (Decimal, auto-calculado)
  - [ ] Campos: total_cost (Decimal, auto-calculado)
  - [ ] Campos: cost_per_unit (Decimal, auto-calculado) - total_cost / quantity_produced
  - [ ] Campos: is_active, notes
  - [ ] Método __str__

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar ProductBOMAdmin
  - [ ] list_display: product, name, quantity_produced, total_cost, cost_per_unit
  - [ ] readonly_fields: custos calculados
  - [ ] Inline para ProductBOMLine (próxima tarefa)

- [ ] **Testing - ProductBOM**
  - [ ] Test: criar BOM funciona
  - [ ] Test: relacionamento OneToOne com Product funciona

---

## 10.6 Modelo ProductBOMLine (Componentes da Receita)

Criar linhas de componentes que compõem a receita.

- [ ] **Criar modelo ProductBOMLine**
  - [ ] Campos: bom (FK → ProductBOM, related_name='lines')
  - [ ] Campos: component (FK → Product) - produto componente
  - [ ] Campos: quantity (Decimal) - quantidade necessária
  - [ ] Campos: uom (FK → UnitOfMeasure) - unidade da quantidade
  - [ ] Campos: sequence (Integer) - ordem na receita
  - [ ] Campos: component_cost_per_unit (Decimal, auto-calculado)
  - [ ] Campos: line_total_cost (Decimal, auto-calculado)
  - [ ] Método calculate_cost() - calcula custo da linha
  - [ ] Método __str__

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar ProductBOMLineInline para usar no ProductBOMAdmin
  - [ ] list_display: sequence, component, quantity, uom, line_total_cost
  - [ ] readonly_fields: custos calculados
  - [ ] Ordenar por sequence

- [ ] **Testing - ProductBOMLine**
  - [ ] Test: criar linha de BOM funciona
  - [ ] Test: múltiplas linhas em uma BOM

---

## 10.7 Lógica de Cálculo de Custos em Cascata (RECURSIVA)

Implementar cálculo automático de custos multi-nível (componentes que têm componentes).

- [ ] **Criar método em Product: get_real_cost()**
  - [ ] Se product_type = 'RAW_MATERIAL': retornar cost_price (custo de compra)
  - [ ] Se has_bom = False: retornar cost_price
  - [ ] Se has_bom = True: calcular via BOM (RECURSIVO)
  - [ ] Adicionar labor_cost_per_unit ao custo final
  - [ ] Retornar custo total por unidade base

- [ ] **Criar método em ProductBOMLine: calculate_cost()**
  - [ ] Obter custo do componente: self.component.get_real_cost() (RECURSIVO!)
  - [ ] Converter quantidade para unidade base do componente
  - [ ] Calcular: custo_componente * quantidade_convertida
  - [ ] Atualizar component_cost_per_unit e line_total_cost
  - [ ] Salvar

- [ ] **Criar método em ProductBOM: calculate_total_cost()**
  - [ ] Iterar por todas as linhas: for line in self.lines.all()
  - [ ] Chamar line.calculate_cost() para cada linha
  - [ ] Somar todos os line_total_cost → total_component_cost
  - [ ] Calcular total_labor_cost: (labor_time_minutes / 60) * labor_cost_per_hour
  - [ ] total_cost = total_component_cost + total_labor_cost
  - [ ] cost_per_unit = total_cost / quantity_produced
  - [ ] Salvar BOM
  - [ ] Atualizar product.bom_cost = cost_per_unit

- [ ] **Criar signal post_save para ProductBOMLine**
  - [ ] Quando linha é criada/editada/deletada
  - [ ] Recalcular bom.calculate_total_cost()

- [ ] **Testing - Cálculo em Cascata**
  - [ ] Test: custo de RAW_MATERIAL retorna cost_price
  - [ ] Test: BOM nível 1 calcula corretamente
  - [ ] Test: BOM nível 2 (componente tem BOM) calcula em cascata
  - [ ] Test: BOM nível 3 (componente de componente tem BOM) calcula
  - [ ] Test: alterar custo de matéria-prima atualiza BOM que usa
  - [ ] Test: labor_cost é incluído no cálculo

---

## 10.8 Sistema de Recálculo Global de Custos

Criar funcionalidade para recalcular todos os custos do sistema.

- [ ] **Criar management command**
  - [ ] Criar `apps/bom/management/commands/recalculate_bom_costs.py`
  - [ ] Comando: `python manage.py recalculate_bom_costs`
  - [ ] Obter todos os BOMs ativos
  - [ ] Recalcular em ordem: RAW → COMPONENT → FINISHED_PRODUCT
  - [ ] Exibir progresso e resumo

- [ ] **Criar Celery task para recálculo assíncrono**
  - [ ] Task `recalculate_all_bom_costs_async()`
  - [ ] Executar comando em background
  - [ ] Notificar usuário quando concluir

- [ ] **Criar view de recálculo manual**
  - [ ] Criar BOMRecalculateView
  - [ ] Botão "Recalcular Todos os Custos"
  - [ ] Confirmação antes de executar
  - [ ] Executar via Celery task
  - [ ] Mostrar status de progresso (opcional)

- [ ] **Criar template**
  - [ ] `templates/bom/recalculate.html` (standalone)
  - [ ] Aviso de que pode demorar
  - [ ] Botão de confirmação

- [ ] **Configurar rota**
  - [ ] `path('bom/recalculate/', BOMRecalculateView, name='bom_recalculate')`

- [ ] **Testing - Recálculo Global**
  - [ ] Test: comando recalcula todos os BOMs
  - [ ] Test: ordem de cálculo está correta
  - [ ] Test: task Celery funciona
  - [ ] Test: view dispara recálculo

---

## 10.9 Views de Gestão de BOM - Listagem

Criar interface para visualizar todas as receitas.

- [ ] **Criar BOMListView**
  - [ ] Listar todos os BOMs ativos
  - [ ] Filtros: product_type, produto
  - [ ] Busca por nome de produto
  - [ ] Mostrar: produto, nome BOM, custo total, custo/unidade
  - [ ] Link para visualizar/editar

- [ ] **Criar template**
  - [ ] `templates/bom/bom_list.html` (standalone)
  - [ ] Tabela com colunas importantes
  - [ ] Badges visuais para product_type
  - [ ] Botão "Nova Receita"
  - [ ] Botão "Recalcular Todos os Custos"

- [ ] **Configurar rota**
  - [ ] `path('bom/', BOMListView, name='bom_list')`

- [ ] **Testing - BOM List**
  - [ ] Test: listar BOMs funciona
  - [ ] Test: filtros funcionam
  - [ ] Test: custos exibidos corretamente

---

## 10.10 Views de Gestão de BOM - Criação

Criar interface para criar nova receita.

- [ ] **Criar BOMCreateView**
  - [ ] Form: selecionar produto (filtrar apenas has_bom=True ou criar novo)
  - [ ] Campos: name, quantity_produced, uom_produced
  - [ ] Campos: labor_time_minutes, labor_cost_per_hour
  - [ ] JavaScript para adicionar linhas de componentes dinamicamente
  - [ ] Seletor de componentes com busca
  - [ ] Campos por linha: component, quantity, uom
  - [ ] Validação: não permitir ciclos (produto A → B → A)

- [ ] **Criar form**
  - [ ] Criar ProductBOMForm em forms.py
  - [ ] Formset para ProductBOMLine
  - [ ] Validação de ciclos recursivos

- [ ] **Criar template**
  - [ ] `templates/bom/bom_create.html` (standalone)
  - [ ] Formulário principal
  - [ ] Tabela dinâmica de componentes
  - [ ] Botão "Adicionar Componente"
  - [ ] Preview de custo (calculado em tempo real via JS - opcional)

- [ ] **Configurar rota**
  - [ ] `path('bom/new/', BOMCreateView, name='bom_create')`

- [ ] **Testing - BOM Create**
  - [ ] Test: criar BOM com linhas funciona
  - [ ] Test: validação de ciclos funciona
  - [ ] Test: custos são calculados automaticamente após salvar

---

## 10.11 Views de Gestão de BOM - Edição e Detalhes

Criar interface para visualizar e editar receita.

- [ ] **Criar BOMDetailView**
  - [ ] Mostrar informações do BOM
  - [ ] Tabela de componentes com custos calculados
  - [ ] Mostrar total_component_cost, total_labor_cost, total_cost
  - [ ] Mostrar cost_per_unit (destaque visual)
  - [ ] Botão "Editar", "Duplicar", "Recalcular Esta Receita"
  - [ ] Mostrar onde este produto é usado (reverse lookup)

- [ ] **Criar BOMUpdateView**
  - [ ] Form pré-preenchido
  - [ ] Permitir editar linhas
  - [ ] Recalcular ao salvar

- [ ] **Criar templates**
  - [ ] `templates/bom/bom_detail.html` (standalone)
  - [ ] `templates/bom/bom_update.html` (standalone)

- [ ] **Configurar rotas**
  - [ ] `path('bom/<uuid:pk>/', BOMDetailView, name='bom_detail')`
  - [ ] `path('bom/<uuid:pk>/edit/', BOMUpdateView, name='bom_update')`

- [ ] **Testing - BOM Edit/Detail**
  - [ ] Test: visualizar detalhes funciona
  - [ ] Test: todos os custos são exibidos
  - [ ] Test: editar BOM funciona
  - [ ] Test: recalcular recalcula corretamente

---

## 10.12 Ação de Recálculo Individual

Criar ação para recalcular uma receita específica.

- [ ] **Criar BOMRecalculateSingleView**
  - [ ] Obter BOM por PK
  - [ ] Executar bom.calculate_total_cost()
  - [ ] Mensagem de sucesso
  - [ ] Redirecionar para detail

- [ ] **Configurar rota**
  - [ ] `path('bom/<uuid:pk>/recalculate/', BOMRecalculateSingleView, name='bom_recalculate_single')`

- [ ] **Adicionar botão no detail template**
  - [ ] Botão "Recalcular Custos"

- [ ] **Testing - Single Recalculate**
  - [ ] Test: recalcular uma receita funciona
  - [ ] Test: custos são atualizados

---

## 10.13 Integração com Vendas - Venda por Fatias

Adicionar funcionalidade de venda de bolos por fatias.

- [ ] **Criar modelo ProductSlicing**
  - [ ] Campos: product (FK → Product)
  - [ ] Campos: slice_configuration_name (ex: "15 Fatias", "30 Fatias")
  - [ ] Campos: total_slices (Integer)
  - [ ] Campos: cost_per_slice (Decimal, auto-calculado)
  - [ ] Campos: price_per_slice (Decimal, definido manualmente)
  - [ ] Método calculate_cost_per_slice(): product.get_real_cost() / total_slices

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Atualizar SaleOrderLine (Fase 7)**
  - [ ] Adicionar campo opcional: slicing_config (FK → ProductSlicing, nullable)
  - [ ] Se preenchido, calcular preço com base em fatias
  - [ ] Exemplo: 1 bolo vendido em 15 fatias = 15 * price_per_slice

- [ ] **Registrar no Admin**
  - [ ] Criar ProductSlicingAdmin
  - [ ] Inline no ProductAdmin

- [ ] **Testing - Slicing**
  - [ ] Test: criar configuração de fatias funciona
  - [ ] Test: cost_per_slice calculado corretamente
  - [ ] Test: venda com slicing funciona

---

## 10.14 Relatório de Análise de Custos

Criar relatório de análise de custos de produtos.

- [ ] **Criar BOMCostReportView**
  - [ ] Listar todos os produtos FINISHED_PRODUCT
  - [ ] Mostrar: custo componentes, custo mão-de-obra, custo total
  - [ ] Mostrar: preço de venda, margem de lucro (%), markup
  - [ ] Filtros: categoria, margem mínima
  - [ ] Destacar produtos com margem baixa (<30%)
  - [ ] Opção de exportar para Excel

- [ ] **Criar template**
  - [ ] `templates/bom/cost_report.html` (standalone)
  - [ ] Tabela com todas as métricas
  - [ ] Gráficos (opcional)

- [ ] **Configurar rota**
  - [ ] `path('bom/reports/costs/', BOMCostReportView, name='bom_cost_report')`

- [ ] **Testing - Cost Report**
  - [ ] Test: relatório mostra dados corretos
  - [ ] Test: margens calculadas corretamente
  - [ ] Test: filtros funcionam

---

## 10.15 Interface de Configurador de Bolos (UI Específica)

Criar interface específica para configurar bolos customizados.

- [ ] **Criar CakeConfiguratorView**
  - [ ] Interface wizard/passo-a-passo:
    - [ ] Passo 1: Escolher base/massa (filtrar products por categoria)
    - [ ] Passo 2: Escolher recheio
    - [ ] Passo 3: Escolher cobertura
    - [ ] Passo 4: Escolher decorações/extras
    - [ ] Passo 5: Escolher tamanho (fatias)
  - [ ] Calcular custo em tempo real (via AJAX)
  - [ ] Calcular preço sugerido (custo * markup padrão)
  - [ ] Permitir ajustar preço final
  - [ ] Botão "Adicionar ao Orçamento" (cria SaleOrderLine)

- [ ] **Criar template**
  - [ ] `templates/bom/cake_configurator.html` (standalone)
  - [ ] Design visual atraente
  - [ ] Cards para seleção de componentes
  - [ ] Preview de custo e preço

- [ ] **Criar API endpoint para cálculo**
  - [ ] POST `/bom/api/calculate-cake-cost/`
  - [ ] Recebe: lista de component IDs e quantidades
  - [ ] Retorna: JSON com custo total

- [ ] **Configurar rota**
  - [ ] `path('bom/configurator/', CakeConfiguratorView, name='cake_configurator')`

- [ ] **Testing - Configurator**
  - [ ] Test: selecionar componentes funciona
  - [ ] Test: cálculo em tempo real funciona
  - [ ] Test: adicionar ao orçamento cria SaleOrderLine

---

## 10.16 Validações e Regras de Negócio

Implementar validações específicas do sistema BOM.

- [ ] **Validação de ciclos recursivos**
  - [ ] Produto A não pode ter componente que eventualmente usa A
  - [ ] Validar ao criar/editar BOMLine
  - [ ] Exibir erro claro

- [ ] **Validação de unidades compatíveis**
  - [ ] Componente e linha devem ter UOMs da mesma categoria
  - [ ] Ou permitir conversão automática

- [ ] **Validação de product_type**
  - [ ] RAW_MATERIAL não pode ter BOM
  - [ ] COMPONENT e FINISHED_PRODUCT devem ter BOM

- [ ] **Alertas de custo**
  - [ ] Se custo BOM > preço venda, alertar
  - [ ] Se margem < 20%, alertar

- [ ] **Testing - Validations**
  - [ ] Test: ciclo recursivo é bloqueado
  - [ ] Test: unidades incompatíveis geram erro
  - [ ] Test: alertas são exibidos

---

## 10.17 Documentação e Ajuda

Criar documentação interna do sistema BOM.

- [ ] **Criar página de ajuda**
  - [ ] `templates/bom/help.html` (standalone)
  - [ ] Explicar conceitos: BOM, componentes, custos
  - [ ] Tutorial passo-a-passo
  - [ ] FAQs

- [ ] **Adicionar tooltips**
  - [ ] Campos complexos têm explicação
  - [ ] Ícones de ajuda nos formulários

- [ ] **Configurar rota**
  - [ ] `path('bom/help/', BOMHelpView, name='bom_help')`

---

## 10.18 Testes Integrados e Casos de Uso

Criar testes completos do sistema BOM.

- [ ] **Testar fluxo completo**
  - [ ] Criar matéria-prima (farinha, ovos, açúcar)
  - [ ] Criar componente (massa fina) com BOM
  - [ ] Criar produto final (bolo) com BOM que usa massa fina
  - [ ] Verificar custo calculado em cascata
  - [ ] Alterar custo da farinha
  - [ ] Recalcular e verificar propagação

- [ ] **Testar cenário de 3 níveis**
  - [ ] Nível 1: RAW_MATERIAL (farinha)
  - [ ] Nível 2: COMPONENT (massa) usa farinha
  - [ ] Nível 3: FINISHED_PRODUCT (bolo) usa massa
  - [ ] Verificar custos em todos os níveis

- [ ] **Testar conversões**
  - [ ] Comprar farinha em KG
  - [ ] BOM usa G
  - [ ] Verificar conversão automática

- [ ] **Testar mão-de-obra**
  - [ ] BOM com labor_time_minutes = 60
  - [ ] labor_cost_per_hour = 10
  - [ ] Verificar labor_cost = 10

- [ ] **Testing - Integration**
  - [ ] Test: fluxo completo funciona sem erros
  - [ ] Test: todos os custos são precisos
  - [ ] Test: recálculo propaga corretamente

---

# 🚀 FASE 11: SISTEMA DE PDFs (DOCUMENTOS)

**⏱ Tempo estimado:** 6-8 dias
**🎯 Objetivo:** Criar sistema de Document Layout configurável + geração de PDFs para documentos (orçamentos, faturas, etc.)
**📦 Dependências:** Fase 3 (core), Fase 4 (contactos), Fase 7 (compras), Fase 8 (vendas)

---

## 11.1 Criação da App 'documents'

Criar app Django para gestão de layouts e geração de PDFs.

- [x] **Criar app**
  - [x] Executar `python manage.py startapp documents apps/documents`
  - [x] Adicionar 'apps.documents' ao INSTALLED_APPS
  - [ ] Criar `apps/documents/urls.py` com namespace `documents`
  - [ ] Incluir URLs no `config/urls.py`

---

## 11.2 Modelos — Document Layout System

Arquitectura de 3 tabelas para layouts configuráveis de documentos PDF.

### 11.2.1 Modelo `LayoutStyle` — Estilos de Envelope

Cada estilo define o HTML do header e footer do documento. A empresa escolhe um.

- [x] **Criar modelo `LayoutStyle`**
  - [x] Campo `id` (UUIDField PK)
  - [x] Campo `name` (CharField, max_length=100, unique) — nome amigável
  - [x] Campo `slug` (SlugField, unique) — identificador técnico
  - [x] Campo `description` (TextField, blank) — descrição do visual
  - [x] Campo `header_html` (TextField) — HTML do header com placeholders Django template
  - [x] Campo `footer_html` (TextField) — HTML do footer com placeholders Django template
  - [x] Campo `preview_image` (ImageField, upload_to='documents/previews/', blank) — thumbnail de pré-visualização
  - [x] Campo `is_active` (BooleanField, default=True)
  - [x] Campo `sort_order` (IntegerField, default=0) — ordenação na UI
  - [x] Campos de auditoria (created_at, updated_at, created_by, updated_by)
  - [x] `__str__` → `name`
  - [x] `class Meta: ordering = ['sort_order', 'name']`

- [x] **Admin — `LayoutStyleAdmin`**
  - [x] `list_display`: name, slug, is_active, sort_order
  - [x] `list_editable`: is_active, sort_order
  - [x] `prepopulated_fields`: slug from name

### 11.2.2 Modelo `TableStyle` — Estilos de Tabelas de Dados

Cada estilo define como as tabelas de linhas (produtos, serviços, etc.) aparecem no corpo do documento.

- [x] **Criar modelo `TableStyle`**
  - [x] Campo `id` (UUIDField PK)
  - [x] Campo `name` (CharField, max_length=100, unique)
  - [x] Campo `slug` (SlugField, unique)
  - [x] Campo `description` (TextField, blank)
  - [x] Campo `css_styles` (TextField) — CSS inline para a tabela (bordas, cores, alternação de linhas)
  - [x] Campo `header_row_html` (TextField, blank) — HTML template da row do header da tabela
  - [x] Campo `data_row_html` (TextField, blank) — HTML template de cada row de dados
  - [x] Campo `totals_row_html` (TextField, blank) — HTML template da row de totais
  - [x] Campo `preview_image` (ImageField, upload_to='documents/previews/', blank)
  - [x] Campo `is_active` (BooleanField, default=True)
  - [x] Campo `sort_order` (IntegerField, default=0)
  - [x] Campos de auditoria
  - [x] `__str__` → `name`

- [x] **Admin — `TableStyleAdmin`**
  - [x] `list_display`: name, slug, is_active, sort_order
  - [x] `list_editable`: is_active, sort_order

### 11.2.3 Modelo `DocumentLayout` — Configuração Ativa da Empresa

Cada empresa tem 1 DocumentLayout que combina um LayoutStyle + TableStyle + cores + fonte + textos.

- [x] **Criar modelo `DocumentLayout`**
  - [x] Campo `id` (UUIDField PK)
  - [x] Campo `company` (OneToOneField → Company, CASCADE) — 1 por empresa
  - [x] Campo `layout_style` (FK → LayoutStyle, PROTECT)
  - [x] Campo `table_style` (FK → TableStyle, PROTECT)
  - [x] Campo `font` (CharField, max_length=100, default='Lato') — fonte dos documentos
  - [x] Campo `primary_color` (CharField, max_length=7, default='#dbc693') — cor principal (headers, destaques)
  - [x] Campo `secondary_color` (CharField, max_length=7, default='#1f2937') — cor secundária (texto, borders)
  - [x] Campo `tagline` (CharField, max_length=255, blank) — slogan da empresa
  - [x] Campo `footer_text` (TextField, blank) — texto livre do footer (telefone, email, website)
  - [x] Campo `paper_format` (CharField, choices: A4, US_LETTER, default='A4')
  - [x] Campo `tax_id` (CharField, max_length=50, blank) — NIF / CNPJ
  - [x] Campos de auditoria
  - [x] `__str__` → `f'Layout de {company.name}'`
  - [x] Método `get_context()` — retorna dict completo para renderização (logo, morada, cores, etc. via Company)

- [x] **Admin — `DocumentLayoutAdmin`**
  - [x] `list_display`: company, layout_style, table_style, font, paper_format
  - [x] `list_select_related`: company, layout_style, table_style

- [x] **Migrations**
  - [x] Criar migration para os 3 modelos
  - [x] Executar `python manage.py migrate`

---

## 11.3 Layout Styles — Criação dos 7 Estilos

Criar 7 estilos de layout com HTML para header e footer. Cada um tem uma personalidade visual distinta.

### 11.3.1 Layout Style: **Clean** (Limpo)
- [x] Header: logo alinhado à esquerda, dados da empresa à direita, separador fino
- [x] Footer: linha fina + texto centrado (telefone, email, website, nº de página)
- [x] Visual: minimalista, muito espaço em branco, sem fundos coloridos
- [x] HTML armazenado no seed (`scripts/seed_document_styles.py`)
- [x] ~~Criar ficheiro `templates/documents/layouts/clean_header.html`~~ (inline no BD)

### 11.3.2 Layout Style: **Bold** (Forte)
- [x] Header: barra escura no topo, logo e nome à esquerda, dados da empresa à direita
- [x] Footer: barra escura inferior + texto centrado
- [x] Visual: impactante, cores fortes, presença forte da marca
- [x] HTML armazenado no seed

### 11.3.3 Layout Style: **Stripe** (Faixa)
- [x] Header: faixa lateral colorida à esquerda (5px), logo e dados alinhados à esquerda com recuo
- [x] Footer: faixa lateral a repetir + texto alinhado à esquerda
- [x] Visual: profissional, subtil, toque de cor lateral
- [x] HTML armazenado no seed

### 11.3.4 Layout Style: **Frame** (Moldura)
- [x] Header: bordas finas formando moldura no topo, logo centrado dentro da moldura
- [x] Footer: moldura inferior com dados centrados
- [x] Visual: clássico, formal, elegante
- [x] HTML armazenado no seed

### 11.3.5 Layout Style: **Split** (Dividido)
- [x] Header: dividido verticalmente — metade esquerda com fundo escuro (logo branco), metade direita limpa (dados)
- [x] Footer: metade esquerda escura (website), metade direita limpa (footer_text)
- [x] Visual: moderno, assimétrico, dinâmico
- [x] HTML armazenado no seed

### 11.3.6 Layout Style: **Arc** (Arco)
- [x] Header: forma curva/onda no fundo do header com gradiente da primary_color, logo sobre a curva
- [x] Footer: curva invertida subtil + dados
- [x] Visual: suave, orgânico, moderno
- [x] HTML armazenado no seed

### 11.3.7 Layout Style: **Edge** (Aresta)
- [x] Header: triângulos e linhas geométricas angulares, logo no canto, dados no lado oposto
- [x] Footer: gradiente linear + triângulo decorativo
- [x] Visual: técnico, sharp, contemporâneo
- [x] HTML armazenado no seed

---

## 11.4 Table Styles — Criação dos 7 Estilos

Criar 7 estilos de tabela com CSS/HTML distintos.

### 11.4.1 Table Style: **Minimal** (Mínimo)
- [x] Sem bordas externas, apenas separadores horizontais subtis entre linhas
- [x] Header da tabela em bold, sem fundo
- [x] Totais em bloco independente abaixo da tabela
- [x] CSS e HTML no seed

### 11.4.2 Table Style: **Grid** (Grelha)
- [x] Bordas completas em todas as células (grelha visível)
- [x] Header com fundo secondary_color e texto branco
- [x] Totais em bloco independente
- [x] CSS e HTML no seed

### 11.4.3 Table Style: **Accent** (Destaque)
- [x] Sem bordas verticais, header sublinhado com primary_color
- [x] Linhas pares com fundo levemente colorido (primary_color 7% opacidade)
- [x] CSS e HTML no seed

### 11.4.4 Table Style: **Zebra** (Zebra)
- [x] Linhas alternadas com fundo cinza claro / branco
- [x] Sem bordas horizontais (a cor faz a separação)
- [x] Header em bold com borda inferior grossa
- [x] CSS e HTML no seed

### 11.4.5 Table Style: **Compact** (Compacto)
- [x] Padding reduzido em todas as células
- [x] Fonte ligeiramente menor (10px)
- [x] Bordas horizontais finas, header com fundo escuro
- [x] CSS e HTML no seed

### 11.4.6 Table Style: **Card** (Cartão)
- [x] Cada linha como "cartão" com bordas arredondadas e sombra subtil
- [x] Espaçamento entre linhas (border-spacing)
- [x] Header sem fundo, texto em uppercase
- [x] CSS e HTML no seed

### 11.4.7 Table Style: **Flat** (Liso)
- [x] Zero linhas, zero bordas — apenas texto alinhado em colunas
- [x] A versão mais invisível — foca-se 100% nos dados
- [x] CSS e HTML no seed

---

## 11.5 Seeds — Dados Iniciais

- [x] **Criar `scripts/seed_document_styles.py`** (seed unificado)
  - [x] Criar os 7 LayoutStyles com HTML inline (header + footer com placeholders Django template)
  - [x] Criar os 7 TableStyles com CSS/HTML inline
  - [x] Comando: `python manage.py shell -c "exec(open('scripts/seed_document_styles.py', encoding='utf-8').read())"`
  - [x] Usa `update_or_create` por slug — idempotente

- [ ] **Criar `scripts/seed_document_layout.py`** (opcional)
  - [ ] Criar DocumentLayout default para empresas existentes (Clean + Minimal + cores default)

---

## 11.6 UI — Configurar Document Layout no Dashboard

Página no dashboard para a empresa configurar o layout dos seus documentos (similar ao screenshot do Odoo).

- [x] **View `document_layout_view`** em `apps/dashboard/views.py`
  - [x] GET `/dashboard/settings/document-layout/` — mostra configuração atual com pré-visualização
  - [x] POST — guarda alterações (layout_style, table_style, font, cores, tagline, footer, paper_format, tax_id)
  - [x] Busca Company do utilizador para logo e morada
  - [x] Auto-create DocumentLayout se não existir (Clean + Minimal)

- [x] **Template `templates/dashboard/document_layout.html`**
  - [x] Selector visual de Layout Styles (radio cards com mini-previews)
  - [x] Selector visual de Table Styles (radio cards com mini-tables)
  - [x] Dropdown de fontes (10 Google Fonts)
  - [x] Color pickers para primary_color e secondary_color (input[type=color] + hex)
  - [x] Campos: tagline, footer_text, paper_format, tax_id
  - [x] Preview ao vivo do documento (sidebar sticky, Alpine.js reactivo)
  - [x] Botões: Guardar, Descartar (na sub_navbar)
  - [x] Cards de mini-preview com design específico por layout (Split duas metades, Arc curva gradiente, Edge triângulo + linha, Standard inline)
  - [x] Alpine.js `documentLayoutEditor()` com computed getters reactivos (`headerStyle`, `footerStyle`, `thStyle`, `_tdBase(i)`, etc.) — preview atualiza em tempo real ao trocar estilo/cor/fonte
  - [x] Modal fullscreen A4 (click na pré-visualização abre modal 595×842px com preview completo, ESC/click-outside/X para fechar)
  - [x] Layouts Split, Arc e Edge com elementos HTML dedicados (divs para curvas, triângulos e linhas gradiente — pseudo-elements não funcionam com Alpine.js inline styles)
  - [x] Link "Configurar Layout do Documento" na página de Definições (`settings.html`) conectado via `{% url 'dashboard:document_layout' %}`

- [x] **URLs** em `apps/dashboard/urls.py`
  - [x] `settings/document-layout/` → name='document_layout'

---

## 11.7 Motor de Geração de PDF

Função utilitária que junta Layout + Tabela + dados e converte para PDF.

- [ ] **Criar `apps/documents/renderer.py`**
  - [ ] `render_document_html(document_layout, template_name, context)` — monta HTML completo (header + body + footer)
  - [ ] Resolve placeholders: `{{ company_logo }}`, `{{ company_name }}`, `{{ company_address }}`, `{{ primary_color }}`, `{{ secondary_color }}`, `{{ font }}`, `{{ tagline }}`, `{{ footer_text }}`, `{{ tax_id }}`, `{{ page_number }}`

- [ ] **Criar `apps/documents/pdf_generator.py`**
  - [ ] `generate_pdf(html, filename)` — HTML → PDF via WeasyPrint ou xhtml2pdf
  - [ ] Salvar em `/media/documents/`
  - [ ] Retornar path do ficheiro gerado

- [ ] **Testing**
  - [ ] Test: renderizar HTML completo funciona
  - [ ] Test: gerar PDF funciona
  - [ ] Test: PDF é salvo corretamente

---

## 11.8 Templates de Documentos Específicos

Templates do corpo do documento (entre header e footer) para cada tipo.

- [ ] **Template para Orçamento PDF**
  - [ ] Criar `templates/documents/body_quotation.html`
  - [ ] Dados do cliente (nome, morada, NIF)
  - [ ] Referência e data do orçamento
  - [ ] Tabela de produtos/serviços (usa TableStyle)
  - [ ] Subtotais, impostos, total
  - [ ] Condições e validade

- [ ] **Template para Fatura PDF**
  - [ ] Criar `templates/documents/body_invoice.html`
  - [ ] Similar ao orçamento
  - [ ] Informações fiscais adicionais
  - [ ] Condições de pagamento

- [ ] **Template para Encomenda de Compra PDF**
  - [ ] Criar `templates/documents/body_purchase_order.html`
  - [ ] Dados do fornecedor
  - [ ] Tabela de items encomendados
  - [ ] Prazo de entrega

- [ ] **Template para Nota de Entrega PDF**
  - [ ] Criar `templates/documents/body_delivery_note.html`
  - [ ] Dados do destinatário
  - [ ] Lista de items entregues
  - [ ] Campo de assinatura

---

## 11.9 Views de Geração de PDF

Integrar geração de PDF nos módulos existentes.

- [ ] **Criar `DocumentPDFView`** em `apps/documents/views.py`
  - [ ] Genérico — recebe `document_type` + `object_id`
  - [ ] Busca dados, renderiza HTML, gera PDF
  - [ ] Retorna PDF para download ou inline preview

- [ ] **Rotas para Vendas**
  - [ ] `path('sales/<uuid:pk>/pdf/', ..., name='sale_pdf')`
  - [ ] Link "Download PDF" na vista de detalhe

- [ ] **Rotas para Compras**
  - [ ] `path('purchases/<uuid:pk>/pdf/', ..., name='purchase_pdf')`
  - [ ] Link "Download PDF" na vista de detalhe

- [ ] **Testing**
  - [ ] Test: gerar PDF de orçamento funciona
  - [ ] Test: gerar PDF de fatura funciona
  - [ ] Test: gerar PDF de compra funciona
  - [ ] Test: PDF reflete o layout escolhido pela empresa

---

# 🚀 FASE 12: APP - MARKETING E WHATSAPP

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de marketing e integração WhatsApp
**📦 Dependências:** Fase 4 (contacts), Fase 11 (PDFs)

---

## ✅ 12.0 IMPLEMENTADO — WhatsApp Business API no Chatter (Fev 2026)

> Esta secção documenta o que foi efectivamente implementado na sessão de Fevereiro de 2026 na app `core` e `crm` (fora da app `marketing` planeada). A app `marketing` separada continua pendente (secções 13.x abaixo).

### 12.0.1 Modelo — CompanyWhatsAppConfig

- [x] **Criar modelo `CompanyWhatsAppConfig`** em `apps/core/models.py`
  - [x] Campo `company` (OneToOneField → Company)
  - [x] Campo `phone_number_id` (CharField) — ID do número na Meta API
  - [x] Campo `business_account_id` (CharField) — ID da conta business
  - [x] Campo `access_token` (TextField) — token encriptado com Fernet
  - [x] Campo `webhook_verify_token` (CharField)
  - [x] Campo `is_active` (BooleanField)
  - [x] Método `set_encrypted_token(raw_token)` — encripta e guarda
  - [x] Método `get_decrypted_token()` — desencripta em runtime
  - [x] Property `has_whatsapp_configured` — verifica se está tudo preenchido
- [x] **Criar migration** `apps/core/migrations/0019_companywhatsappconfig.py` — aplicada ✅
- [x] **Registar no Admin** (`apps/core/admin.py`)
  - [x] Campo `raw_token_input` (PasswordInput) que auto-encripta ao guardar
  - [x] Campo readonly `token_status` mostra ✓/✗

### 12.0.2 Configuração na Base de Dados (Fuet Mágico)

- [x] **Credenciais Meta configuradas via Django shell**
  - [x] `phone_number_id = '1008273009039120'`
  - [x] `business_account_id = '862763680130987'`
  - [x] Token temporário encriptado com Fernet
  - [x] `webhook_verify_token = 'fuet_secret_2026'`
  - [x] `is_active = True`
- [x] **Testado e a funcionar** — mensagem enviada com sucesso via `send_whatsapp_message()`

> ⚠️ **Token caduca em 60 min (token temporário Meta)**. Para renovar:
> ```python
> from apps.core.models import CompanyWhatsAppConfig
> config = CompanyWhatsAppConfig.objects.get(company__name='Fuet Mágico')
> config.set_encrypted_token('NOVO_TOKEN_AQUI')
> config.save()
> ```
> Para produção, criar **System User token** permanente no Meta Business Manager.

### 12.0.3 Utilitários — `apps/core/whatsapp_utils.py`

- [x] Função `send_whatsapp_message(phone, message, company)` — envia via Meta Graph API v18.0
- [x] Função `parse_webhook_payload(data)` — parse do JSON do webhook
- [x] Função `phones_match(phone_a, phone_b)` — normaliza e compara números

### 12.0.4 Webhook — Receber Mensagens de Entrada

- [x] **View `whatsapp_webhook`** em `apps/core/views.py`
  - [x] `GET` — verificação do webhook (responde com `hub.challenge`)
  - [x] `POST` — processa mensagens de entrada
  - [x] `@csrf_exempt` — Meta não envia CSRF token
- [x] **Rota** `GET/POST /whatsapp/webhook/` em `apps/core/urls.py` — pública (sem login_required)
- [x] **`_process_inbound_whatsapp()`** — encontra lead pelo telefone, cria `ChatterMessage`, notifica followers
- [ ] **⚠️ PENDENTE — Testar webhook em produção**
  - [ ] Em desenvolvimento local: instalar ngrok → `ngrok http 8000` → configurar URL no Meta
  - [ ] Em produção (VPS com domínio): configurar directamente `https://dominio.com/whatsapp/webhook/` no Meta Developer Console → WhatsApp → Configuration → Webhook
  - [ ] Subscribe to field: `messages`

### 12.0.5 CRM — Tab WhatsApp no Chatter da Lead

- [x] **Views em `apps/crm/views.py`**
  - [x] `lead_whatsapp_list` — `GET /crm/leads/<id>/whatsapp/` — devolve JSON com mensagens
  - [x] `lead_send_whatsapp` — `POST /crm/leads/<id>/whatsapp/send/` — envia e guarda na BD
  - [x] Contexto da `lead_detail_view` ampliado: `has_whatsapp`, `lead_phone`
- [x] **Rotas** em `apps/crm/urls.py`
- [x] **Tab WhatsApp no template** `templates/crm/lead_create.html`
  - [x] Balões verdes (enviados) / cinzentos (recebidos) ao estilo WhatsApp
  - [x] Área de envio com Ctrl+Enter
  - [x] Aviso "WhatsApp não configurado" se `has_whatsapp = False`
  - [x] Aviso "Sem telefone no contacto" se `lead_phone` vazio
  - [x] Alpine.js component `leadWhatsAppPanel(leadId, contactPhone, hasWhatsApp)`
  - [x] Flag `loaded` para evitar polling infinito (bug corrigido)

### 12.0.6 Fixes Aplicados Durante Implementação

- [x] `MESSAGE_TYPE_CHOICES` em `apps/core/models.py` — adicionado `('WHATSAPP', 'WhatsApp')`
- [x] Campo correcto `author=user` (era `sent_by=user` — campo inexistente)
- [x] `from_email=''` (era `from_email=to_phone` — EmailField rejeita números de telefone)
- [x] `m.author` na list view (era `m.sent_by`)

---

## 🔲 12.0.7 PENDENTE — Tokens e Produção

- [ ] **Criar System User no Meta Business Manager**
  - [ ] Ir a Meta Business Manager → Configurações → Utilizadores do Sistema
  - [ ] Criar utilizador do sistema com perfil "Admin"
  - [ ] Gerar token permanente com permissões `whatsapp_business_messaging` e `whatsapp_business_management`
  - [ ] Actualizar token na BD via Admin ou shell

---

## ✅ 12.0.8 IMPLEMENTADO — Modelo WhatsAppTemplate e API Meta (Fev 2026)

> Implementado em `apps/whatsapp/` (app dedicada, não em `apps/core/` como originalmente planeado).

- [x] **Modelo `WhatsAppTemplate`** em `apps/whatsapp/models.py`
  - [x] Campo `name` (CharField unique — identificador técnico, ex: `orcamento_aprovado`)
  - [x] Campo `display_name` (CharField — nome legível para o utilizador)
  - [x] Campo `language` (CharField — choices: pt_PT, pt_BR, en_US, en_GB, fr, es, de, it, nl, ar, zh_CN)
  - [x] Campo `category` (CharField — choices: MARKETING, UTILITY, AUTHENTICATION)
  - [x] Campo `status` (CharField — choices: DRAFT, PENDING, APPROVED, REJECTED, PAUSED, DISABLED)
  - [x] Campo `allow_category_change` (BooleanField)
  - [x] Campo `header_type` (CharField — choices: NONE, TEXT, IMAGE, VIDEO, DOCUMENT)
  - [x] Campo `header_text` (CharField, opcional — máx. 60 caracteres)
  - [x] Campo `body` (TextField — corpo com variáveis `{{1}}`, `{{2}}`)
  - [x] Campo `footer` (CharField, opcional — máx. 60 caracteres)
  - [x] Campo `buttons` (JSONField — lista de botões URL / PHONE_NUMBER / QUICK_REPLY / COPY_CODE)
  - [x] Campo `variables` (JSONField — mapeamento `{"1": "contact.name", "2": "title"}`)
  - [x] Campo `model_name` (CharField — modelo Django associado, ex: `crm.Lead`)
  - [x] Campo `wa_template_uid` (CharField — ID devolvido pela Meta)
  - [x] Campo `owner_company` (ForeignKey → Company)
  - [x] Campo `created_by` (ForeignKey → User)
  - [x] Property `status_color` (Tailwind class para badge)
  - [x] Property `variable_count` (conta variáveis `{{N}}` no body)
  - [x] Migration aplicada ✅

- [x] **API Meta — Submeter Template para Aprovação** (`apps/whatsapp/api.py`)
  - [x] Função `build_template_payload(template)` — constrói JSON para Meta API
  - [x] Suporte a HEADER (TEXT / IMAGE / VIDEO / DOCUMENT) com `example`
  - [x] Suporte a BODY com amostras de variáveis
  - [x] Suporte a FOOTER e BUTTONS (URL, PHONE_NUMBER, QUICK_REPLY, COPY_CODE)
  - [x] **[Fix Fev 2026]** Botões URL incompletos (url vazia) são filtrados — Meta rejeita url vazia
  - [x] **[Fix Fev 2026]** Normalização E.164 automática para botões PHONE_NUMBER no payload
  - [x] Helper `_get_wa_config(company)` — lê `CompanyWhatsAppConfig` da BD em vez de variáveis de ambiente
  - [x] Função `submit_template_to_meta(template)` — `POST graph.facebook.com/v19.0/{waba_id}/message_templates`
  - [x] **[Fix Fev 2026]** Credenciais lidas de `CompanyWhatsAppConfig` (BD, Fernet) em vez de `settings.WHATSAPP_*` (env)
  - [x] **[Fix Fev 2026]** Erro da Meta mostra `error_user_msg` em português em vez do genérico "Invalid parameter"
  - [x] Guarda `wa_template_uid` devolvido e muda status para PENDING

- [x] **Admin — Gestão de Templates** (`apps/whatsapp/admin.py`)
  - [x] `WhatsAppTemplateAdmin` registado
  - [x] `list_display`: display_name, name, category, language, status, header_type, owner_company, created_at
  - [x] `list_filter`: category, language, status, header_type, owner_company
  - [x] Fieldsets: Identificação, Classificação, Conteúdo, Variáveis, Meta API, Datas

- [ ] **⚠️ PENDENTE — Receber notificação de aprovação/rejeição via Webhook**
  - [ ] Meta envia POST para o webhook com `message_template_status_update`
  - [ ] Actualizar `WhatsAppTemplate.status` e `rejection_reason` automaticamente
  - [ ] Adicionar handling em `apps/core/views.py` → `whatsapp_webhook`

- [ ] **⚠️ PENDENTE — UI no Chatter — Botão "Enviar Template"**
  - [ ] Botão "📋 Template" ao lado do botão de enviar no tab WhatsApp
  - [ ] Modal Alpine.js: lista templates APPROVED, campos para preencher variáveis
  - [ ] View `lead_send_whatsapp_template` em `apps/crm/views.py`

---

## ✅ 12.0.9 IMPLEMENTADO — Modelo GenericActivity e Blueprint Filtering (Fev 2026)

### GenericActivity (`apps/core/models.py`)

- [x] **Novo modelo `GenericActivity`** — atividade genérica ligada a qualquer modelo via ContentType
  - [x] ContentType FK + `object_id` + `content_object` (GenericForeignKey)
  - [x] `scheduled_activity` (FK → ScheduledActivity, opcional — blueprint)
  - [x] `activity_type` (CharField — TODO, EMAIL, CALL, WHATSAPP, DOCUMENT, SIGNATURE, MEETING)
  - [x] `summary` (CharField), `due_date` (DateField)
  - [x] `assigned_to` (FK → User), `is_done` (BooleanField), `done_date` (DateTimeField), `feedback` (TextField)
  - [x] `owner_company` (FK → Company)
  - [x] Property `is_overdue`, `is_today`
  - [x] Indexes em `content_type+object_id`, `due_date`, `is_done`
  - [x] `GenericActivityAdmin` registado em `apps/core/admin.py`
  - [x] Migration aplicada ✅

### ScheduledActivity — Campo `applicable_models`

- [x] **Campo `applicable_models`** (JSONField, default=list, blank=True) em `ScheduledActivity`
  - [x] Choices: `CRM` (CRM — Leads), `WHATSAPP` (WhatsApp Templates), `CONTACT` (Contactos)
  - [x] Vazio = aplica-se a todos os módulos
  - [x] Admin: novo fieldset "Visibilidade", coluna `Módulos` na list view
  - [x] Form: `ScheduledActivityForm` com `MultipleChoiceField` e widget combobox pill picker (Alpine.js)
  - [x] Template `crm/activity_form.html`: campo "Módulos" com input+dropdown+pills removíveis
  - [x] Migration `0022_scheduledactivity_applicable_models.py` aplicada ✅

### Blueprint Filtering por Módulo

- [x] **Filtro `Q(applicable_models=[]) | Q(applicable_models__contains=['CRM'])`** aplicado em:
  - [x] `lead_detail_view` (`apps/crm/views.py`) — activity picker da lead
  - [x] `prospect_detail_view` (`apps/crm/views.py`) — activity picker do prospect
  - [x] `activity_chain_create_view` (`apps/crm/views.py`) — blueprints na cadeia
  - [x] `activity_chain_edit_view` (`apps/crm/views.py`) — blueprints na cadeia
- [x] **Filtro `Q(applicable_models=[]) | Q(applicable_models__contains=['WHATSAPP'])`** aplicado em:
  - [x] `template_edit_view` (`apps/whatsapp/views.py`) — blueprints no tab Atividade

---

## ✅ 12.1 IMPLEMENTADO — App `apps/whatsapp` — Gestão Completa de Templates (Fev 2026)

### 12.1.1 Estrutura da App

- [x] App `apps/whatsapp/` criada (`__init__.py`, `apps.py`, `models.py`, `views.py`, `urls.py`, `forms.py`, `api.py`, `admin.py`, `migrations/`)
- [x] `apps.whatsapp` registado em `INSTALLED_APPS` (`config/settings.py`)
- [x] URLs registadas em `config/urls.py` → `path('whatsapp/', include('apps.whatsapp.urls'))`
- [x] Variáveis `WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_WABA_ID`, `WHATSAPP_PHONE_NUMBER_ID` em `config/settings.py`
- [x] Tile WhatsApp adicionado ao dashboard (`apps/dashboard/views.py`) com ícone SVG verde
- [x] Secção WhatsApp adicionada às Definições (`templates/dashboard/settings.html`) — API Token, Número, Webhook, toggles de funcionalidades
- [x] Ícone WhatsApp adicionado ao nav de definições (`templates/dashboard/_settings_nav_item.html`)

### 12.1.2 URLs (`apps/whatsapp/urls.py`)

- [x] `GET/POST /whatsapp/` → `template_list_view`
- [x] `GET/POST /whatsapp/novo/` → `template_create_view`
- [x] `GET/POST /whatsapp/<uuid>/editar/` → `template_edit_view`
- [x] `POST /whatsapp/<uuid>/submeter/` → `template_submit_view`
- [x] `POST /whatsapp/<uuid>/arquivar/` → `template_archive_view`
- [x] `POST /whatsapp/<uuid>/desarquivar/` → `template_unarchive_view`
- [x] `POST /whatsapp/<uuid>/eliminar/` → `template_delete_view`
- [x] `POST /whatsapp/bulk/` → `bulk_action_view`
- [x] `GET /whatsapp/<uuid>/notas/` → `template_notes_list`
- [x] `POST /whatsapp/<uuid>/notas/criar/` → `template_note_create`
- [x] `GET|POST /whatsapp/<uuid>/seguidores/` → `template_followers_api`
- [x] `DELETE /whatsapp/<uuid>/seguidores/<uuid>/remover/` → `template_follower_remove_api`
- [x] `POST /whatsapp/<uuid>/atividades/criar/` → `template_activity_create`
- [x] `POST /whatsapp/<uuid>/atividades/<uuid>/concluir/` → `template_activity_done`
- [x] `DELETE /whatsapp/<uuid>/atividades/<uuid>/eliminar/` → `template_activity_delete`

### 12.1.3 Views CRUD

- [x] **`template_list_view`** — lista paginada (50/página) com:
  - [x] Pesquisa por display_name, name, body
  - [x] Filtro active/archived, filtro `wa_status` (DRAFT/PENDING/APPROVED/REJECTED/PAUSED), filtro category
  - [x] Bulk actions: arquivar, desarquivar, eliminar
- [x] **`template_create_view`** — cria novo template, redireciona para a página de edição do template criado
- [x] **`template_edit_view`** — edição completa com:
  - [x] Form readonly se status = PENDING ou APPROVED
  - [x] Audit log (últimos 50 eventos)
  - [x] Tab Atividades com `GenericActivity` (design CRM-idêntico)
  - [x] AirDatepicker para data limite das atividades
  - [x] Campo Responsável com utilizadores activos
  - [x] Lista de blueprints filtrada por `WHATSAPP` applicable_models
  - [x] Mapa de variáveis com preview em tempo real
  - [x] Notificações criadas/removidas nos eventos de atividade
  - [x] Auto-follow do utilizador actual como seguidor
  - [x] `notify_followers` ao guardar alterações
  - [x] **[Fix Fev 2026]** Após guardar, redireciona para a própria página de edição (não para a lista)
- [x] **`template_submit_view`** — submete à Meta API, atualiza `wa_template_uid` e status → PENDING
  - [x] **[Fix Fev 2026]** Se `owner_company` for None, resolve automaticamente a partir da empresa activa da sessão
- [x] **`template_archive_view`** / **`template_unarchive_view`** — toggle `is_active`
- [x] **`template_delete_view`** — elimina template
- [x] **`bulk_action_view`** — archive / unarchive / delete em massa

### 12.1.4 Notes (Chatter interno)

- [x] **`template_notes_list`** — devolve JSONResponse com notas internas do template (ChatterMessage, type=NOTE)
- [x] **`template_note_create`** — cria nota, processa @menções (Notification MENTION), notifica seguidores via `notify_followers`

### 12.1.5 Followers (Chatter)

- [x] **`template_followers_api`** — GET lista seguidores (com auto-follow do utilizador actual); POST adiciona seguidor
- [x] **`template_follower_remove_api`** — DELETE remove seguidor

### 12.1.6 Atividades (GenericActivity)

- [x] **`template_activity_create`** — cria `GenericActivity` ligada ao template via ContentType; cria `Notification` (OVERDUE/TODAY/UPCOMING) para o responsável
- [x] **`template_activity_done`** — marca como concluído, guarda feedback, remove notificação pendente
- [x] **`template_activity_delete`** — elimina atividade, remove notificação pendente
- [x] **Design CRM-idêntico** no tab Atividades do template:
  - [x] Secção "Atividades Planeadas" com chevron
  - [x] Data relativa (Hoje / Amanhã / Daqui a N dias / Atrasado)
  - [x] «sumário» + "para" + responsável + ⓘ info toggle
  - [x] Painel de info expandível (Tipo / Responsável / Vence em)
  - [x] Acções: ✓ Marcar Concluído | Cancelar
  - [x] Popover inline "Marcar Concluído" com textarea de feedback
  - [x] Modal de confirmação de cancelamento
  - [x] Secção Concluídas com strikethrough + feedback

### 12.1.7 Form (`apps/whatsapp/forms.py`)

- [x] `WhatsAppTemplateForm` (ModelForm para WhatsAppTemplate)
  - [x] Campos: name, display_name, category, language, header_type, header_text, body, footer, buttons, variables, model_name
  - [x] Widget para `buttons` e `variables`: Textarea com JSON

### 12.1.8 Templates HTML

- [x] `templates/whatsapp/template_list.html` — lista com pesquisa, filtros, badges de status coloridos, bulk actions
- [x] `templates/whatsapp/template_form.html` (~2200 linhas) — formulário rico com:
  - [x] Tabs: Conteúdo / Histórico / Atividades
  - [x] Preview live do template (header/body/footer/botões)
  - [x] Mapeamento de variáveis com selector de campos do modelo
  - [x] AirDatepicker dark theme para data das atividades
  - [x] Botão "Submeter à Meta" com feedback JSON inline
  - [x] Chatter de notas internas
  - [x] Painel de seguidores
  - [x] **[Fev 2026]** Botões PHONE_NUMBER: seletor de indicativo por país (dropdown com pesquisa, 33 países, padrão PT +351)
    - [x] `DIAL_COUNTRIES` — lista de países com flag emoji, nome, código ISO e indicativo
    - [x] `_parsePhoneNumber()` — separa indicativo do número local ao carregar template existente
    - [x] `filteredCountries()` — pesquisa em tempo real por nome ou código
    - [x] `sync()` — combina `dial_code + phone_local` → E.164 no campo hidden `id_buttons`

---

## ✅ 12.1.9 IMPLEMENTADO — DevTools WhatsApp (Fev 2026)

> Ferramenta de desenvolvimento para sincronizar manualmente o estado dos templates PENDING com a Meta API.

- [x] **`fetch_all_meta_templates(config)`** em `apps/whatsapp/api.py`
  - [x] Pagina a API da Meta (`GET /message_templates`) e devolve todos os templates
  - [x] Aceita `CompanyWhatsAppConfig` como parâmetro (usa `get_decrypted_token()`)
- [x] **`sync_pending_templates()`** em `apps/whatsapp/api.py`
  - [x] Carrega todos os templates PENDING da BD
  - [x] Agrupa por empresa (1 chamada à Meta por empresa)
  - [x] Compara status local vs Meta, actualiza BD se mudou
  - [x] Devolve lista de resultados `{name, old_status, new_status, changed}`
- [x] **`devtools_whatsapp_view`** e **`devtools_whatsapp_sync_view`** em `apps/core/views.py`
  - [x] `GET /devtools/whatsapp/` — renderiza página DevTools
  - [x] `POST /devtools/whatsapp/sync-templates/` — chama `sync_pending_templates()`, devolve JSON
- [x] **URLs** em `apps/core/urls.py` — `devtools_whatsapp` e `devtools_whatsapp_sync`
- [x] **`templates/devtools/whatsapp.html`** — página DevTools dark mode (`bg-gray-900`)
  - [x] Botão "Verificar Estado" (`bg-primary hover:opacity-80`) com Alpine.js
  - [x] Tabela de resultados com badges de estado (PENDING/APPROVED/REJECTED/PAUSED)
  - [x] Tabela de referência do ciclo de vida dos estados Meta
  - [x] Estilo consistente com `audit_logs.html` / `error_logs.html`
- [x] **`templates/base.html`** — secção "WhatsApp" adicionada ao dropdown DevTools

---

## 13.1 Criação da App 'marketing'

Criar app Django para marketing.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp marketing apps/marketing`
  - [ ] Adicionar 'apps.marketing' ao INSTALLED_APPS

---

## 13.2 Configuração de API WhatsApp

Configurar integração com WhatsApp Business API.

- [ ] **Criar modelo WhatsAppConfig**
  - [ ] Campos: api_key, api_url, is_active
  - [ ] Método test_connection()

- [ ] **Registrar no Admin**
  - [ ] Criar WhatsAppConfigAdmin
  - [ ] Botão "Testar Conexão"

- [ ] **Criar helper function**
  - [ ] Criar `apps/marketing/whatsapp.py`
  - [ ] Função `send_whatsapp_message(phone, message, media=None)`

- [ ] **Testing - WhatsApp API**
  - [ ] Test: conexão à API funciona
  - [ ] Test: enviar mensagem de teste


## 13.2.1 Setup Completo Meta WhatsApp Business API (Guia Passo-a-Passo)

**ANTES DE COMEÇAR A PROGRAMAR:** Seguir este guia para configurar WhatsApp Business API.

- [ ] **1. Criar Conta Meta Business**
  - [ ] Aceder a https://business.facebook.com
  - [ ] Criar conta Meta Business (se não tiver)
  - [ ] Verificar identidade da empresa (pode demorar 1-3 dias)

- [ ] **2. Configurar WhatsApp Business API**
  - [ ] Ir para Meta Business Suite → Configurações
  - [ ] Adicionar "WhatsApp" nos produtos
  - [ ] Criar App no https://developers.facebook.com
  - [ ] Adicionar produto "WhatsApp" à app
  - [ ] Obter PHONE_NUMBER_ID e WHATSAPP_TOKEN
  - [ ] **IMPORTANTE:** Número de telefone TEM QUE SER NOVO (não pode estar registado no WhatsApp normal)

- [ ] **3. Verificar Número de Telefone**
  - [ ] Meta envia código SMS
  - [ ] Inserir código para verificar
  - [ ] Aguardar aprovação (pode demorar horas/dias)

- [ ] **4. Configurar Webhook**
  - [ ] No dashboard da app, ir para WhatsApp → Configuration
  - [ ] Webhook URL: `https://TEU-DOMINIO.com/webhooks/whatsapp/`
  - [ ] Verify Token: criar token secreto (ex: `WHATSAPP_VERIFY_SECRET_12345`)
  - [ ] Subscribe to: `messages`, `message_status`
  - [ ] **ATENÇÃO:** Webhook PRECISA de HTTPS (não funciona com HTTP)

- [ ] **5. Guardar Credenciais**
  - [ ] Adicionar ao `.env`:
    ```
    WHATSAPP_PHONE_NUMBER_ID=your_phone_id
    WHATSAPP_TOKEN=your_access_token
    WHATSAPP_VERIFY_TOKEN=WHATSAPP_VERIFY_SECRET_12345
    WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id
    ```

- [ ] **6. Testar API (Postman/cURL)**
  - [ ] Enviar mensagem de teste via cURL:
    ```bash
    curl -X POST \
      "https://graph.facebook.com/v18.0/PHONE_NUMBER_ID/messages" \
      -H "Authorization: Bearer WHATSAPP_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "messaging_product": "whatsapp",
        "to": "351912345678",
        "type": "text",
        "text": {"body": "Hello from API!"}
      }'
    ```
  - [ ] Verificar se recebeste a mensagem no teu WhatsApp

- [ ] **7. Configurar Produção (quando estiver pronto)**
  - [ ] Submeter app para review
  - [ ] Aguardar aprovação da Meta
  - [ ] Após aprovação, rate limit aumenta (1000 → ilimitado)

- [ ] **Documentação**
  - [ ] Criar documento interno `docs/whatsapp_setup.md`
  - [ ] Documentar todos os passos
  - [ ] Guardar screenshots importantes
  - [ ] Listar erros comuns e soluções

---

## 13.2.2 Webhook para RECEBER Mensagens (Django View)

Criar endpoint webhook para Meta enviar mensagens recebidas.

- [ ] **Atualizar modelo WhatsAppConfig (tarefa 13.2)**
  - [ ] Adicionar campos:
    - [ ] phone_number_id (CharField, ID do número na Meta API)
    - [ ] business_account_id (CharField)
    - [ ] webhook_verify_token (CharField, token secreto)
    - [ ] company (ForeignKey para Company, **OBRIGATÓRIO**)
  - [ ] Criar migration

- [ ] **Criar Webhook View**
  - [ ] Criar `apps/marketing/views.py`
  - [ ] View: `whatsapp_webhook`
  - [ ] Decorators: `@csrf_exempt` (Meta não envia CSRF token)
  - [ ] **GET request** (verificação do webhook):
    ```python
    def whatsapp_webhook(request):
        if request.method == 'GET':
            # Meta faz verificação inicial
            mode = request.GET.get('hub.mode')
            token = request.GET.get('hub.verify_token')
            challenge = request.GET.get('hub.challenge')
            
            verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN')
            
            if mode == 'subscribe' and token == verify_token:
                return HttpResponse(challenge, content_type='text/plain')
            else:
                return HttpResponse('Forbidden', status=403)
    ```
  - [ ] **POST request** (mensagens recebidas):
    ```python
    elif request.method == 'POST':
        # Parse JSON
        data = json.loads(request.body)
        
        # Extrair mensagem
        entry = data.get('entry', [])
        if not entry:
            return JsonResponse({'status': 'ok'})
        
        changes = entry[0].get('changes', [])
        if not changes:
            return JsonResponse({'status': 'ok'})
        
        value = changes[0].get('value', {})
        
        # Se é mensagem recebida
        if 'messages' in value:
            # Processar via Celery (assíncrono)
            from apps.marketing.tasks import process_incoming_whatsapp_message
            process_incoming_whatsapp_message.delay(value)
        
        # Se é status update (entregue, lido)
        elif 'statuses' in value:
            from apps.marketing.tasks import update_message_status
            update_message_status.delay(value)
        
        return JsonResponse({'status': 'ok'})
    ```

- [ ] **Configurar rota**
  - [ ] Adicionar em `config/urls.py`:
    ```python
    path('webhooks/whatsapp/', whatsapp_webhook, name='whatsapp_webhook')
    ```
  - [ ] **IMPORTANTE:** Rota TEM QUE ser pública (sem @login_required)

- [ ] **Testing - Webhook**
  - [ ] Test: GET request com token correto retorna challenge
  - [ ] Test: GET request com token errado retorna 403
  - [ ] Test: POST request com mensagem dispara Celery task
  - [ ] Test: POST request com status update dispara task

---

## 13.2.3 Modelo WhatsAppMessage (Histórico de Conversas)

Criar modelo para guardar todas as mensagens (enviadas E recebidas).

- [ ] **Criar modelo WhatsAppMessage**
  - [ ] Criar em `apps/marketing/models.py`
  - [ ] Herdar de AbstractBaseModel
  - [ ] **Campos identificação:**
    - [ ] company (ForeignKey para Company, **OBRIGATÓRIO**, on_delete=CASCADE)
    - [ ] contact (ForeignKey para Contact, on_delete=CASCADE)
    - [ ] contact_phone (CharField, formato: 351912345678)
  - [ ] **Campos mensagem:**
    - [ ] message_id (CharField, unique, ID único da Meta API)
    - [ ] conversation_id (CharField, para agrupar mensagens da mesma conversa)
    - [ ] message_type (CharField, choices: SENT, RECEIVED)
    - [ ] content (TextField, texto da mensagem)
  - [ ] **Campos media:**
    - [ ] media_type (CharField, choices: NONE, IMAGE, DOCUMENT, VIDEO, AUDIO, VOICE)
    - [ ] media_id (CharField, nullable, ID do media na Meta API)
    - [ ] media_url (URLField, nullable, URL do ficheiro após download)
    - [ ] media_filename (CharField, nullable)
    - [ ] media_mime_type (CharField, nullable, ex: image/jpeg, application/pdf)
  - [ ] **Campos status:**
    - [ ] status (CharField, choices: QUEUED, SENT, DELIVERED, READ, FAILED)
    - [ ] error_code (CharField, nullable)
    - [ ] error_message (TextField, nullable)
  - [ ] **Campos timestamps:**
    - [ ] sent_at (DateTimeField, auto_now_add=True)
    - [ ] delivered_at (DateTimeField, nullable)
    - [ ] read_at (DateTimeField, nullable)
  - [ ] **Campos contexto:**
    - [ ] context_message_id (CharField, nullable, se é resposta a outra mensagem)
    - [ ] reply_to_message (ForeignKey self, nullable, para threads)
  - [ ] **Meta:**
    - [ ] ordering = ['-sent_at']
    - [ ] indexes = ['contact', 'conversation_id', 'message_id']

- [ ] **Criar migrations**
  - [ ] makemigrations marketing
  - [ ] migrate

- [ ] **Métodos úteis:**
  - [ ] `is_from_customer()` - retorna True se message_type == RECEIVED
  - [ ] `mark_as_read()` - atualiza read_at
  - [ ] `get_media_file()` - download media se ainda não tiver

- [ ] **Registrar no Admin**
  - [ ] Criar WhatsAppMessageAdmin
  - [ ] list_display: company, contact, message_type, content (truncado), media_type, status, sent_at
  - [ ] list_filter: company, message_type, media_type, status, sent_at
  - [ ] search_fields: contact__name, contact_phone, content
  - [ ] readonly_fields: message_id, sent_at, delivered_at, read_at

- [ ] **Testing - WhatsAppMessage**
  - [ ] Test: criar mensagem SENT funciona
  - [ ] Test: criar mensagem RECEIVED funciona
  - [ ] Test: company é obrigatório
  - [ ] Test: message_id é único
  - [ ] Test: filtrar por contact funciona

---

## 13.2.4 Processar Mensagens Recebidas (Celery Task)

Criar Celery task para processar mensagens que chegam via webhook.

- [ ] **Criar helper functions**
  - [ ] Criar `apps/marketing/whatsapp_utils.py`
  - [ ] Função: `get_or_create_contact_from_phone(phone, company)`
    - [ ] Busca Contact por phone
    - [ ] Se não existir, cria automaticamente
    - [ ] Associa à company correta
  - [ ] Função: `download_media_file(media_id, media_type)`
    - [ ] Faz request à Meta API para obter URL do media
    - [ ] Download do ficheiro
    - [ ] Guarda em `/media/whatsapp/`
    - [ ] Retorna caminho local
  - [ ] Função: `get_media_url_from_meta(media_id, token)`
    ```python
    url = f"https://graph.facebook.com/v18.0/{media_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()['url']
    ```

- [ ] **Criar Celery task: process_incoming_whatsapp_message**
  - [ ] Criar em `apps/marketing/tasks.py`
  - [ ] Task: `@shared_task` `process_incoming_whatsapp_message(webhook_data)`
  - [ ] Lógica:
    1. Extrair dados do webhook:
       - from (número de quem enviou)
       - message_id
       - timestamp
       - type (text, image, document, video, audio)
    2. Identificar company (via phone_number_id do webhook)
    3. Obter/criar Contact via phone
    4. **Se tipo TEXT:**
       - Extrair text.body
       - Criar WhatsAppMessage (RECEIVED, content=text)
    5. **Se tipo IMAGE/DOCUMENT/VIDEO:**
       - Extrair media.id, media.mime_type, media.filename
       - Download via download_media_file()
       - Criar WhatsAppMessage (RECEIVED, media_url, media_type)
    6. **Se tipo AUDIO/VOICE:**
       - Similar a image
    7. Guardar na BD
    8. [OPCIONAL] Enviar notificação ao user (WebSocket ou email)

- [ ] **Criar Celery task: update_message_status**
  - [ ] Task para atualizar status (delivered, read)
  - [ ] Buscar WhatsAppMessage por message_id
  - [ ] Atualizar campos: status, delivered_at, read_at

- [ ] **Configurar Celery**
  - [ ] Registar tasks no Celery app
  - [ ] Configurar retry em caso de erro (max 3 tentativas)

- [ ] **Logging robusto**
  - [ ] Log cada mensagem recebida
  - [ ] Log erros de download de media
  - [ ] Log contacts criados automaticamente

- [ ] **Testing - Process Incoming**
  - [ ] Test: mensagem de texto é processada e guardada
  - [ ] Test: mensagem com imagem faz download e guarda
  - [ ] Test: contact é criado automaticamente se não existir
  - [ ] Test: status updates funcionam (delivered, read)
  - [ ] Test: erro no download de media é tratado

---

## 13.2.5 Interface Chatter (Enviar + Receber Mensagens)

Criar interface estilo WhatsApp Web para conversas.

- [ ] **Criar ContactWhatsAppChatView**
  - [ ] View em `apps/contacts/views.py` ou `apps/marketing/views.py`
  - [ ] URL: `/contacts/<uuid:pk>/whatsapp-chat/`
  - [ ] Buscar Contact
  - [ ] Buscar todas as WhatsAppMessage do contact (ordenadas por sent_at)
  - [ ] Contexto: messages, contact, can_send (se configuração ativa)

- [ ] **Criar template chatter**
  - [ ] Criar `templates/marketing/whatsapp_chat.html` (standalone)
  - [ ] **Estrutura HTML:**
    ```html
    <div class="whatsapp-chat-container">
      <!-- Header -->
      <div class="chat-header">
        <img src="{{ contact.photo }}" class="avatar">
        <div>
          <h3>{{ contact.name }}</h3>
          <span class="phone">{{ contact.phone }}</span>
        </div>
      </div>
      
      <!-- Messages Area -->
      <div class="messages-container" id="messages">
        {% for msg in messages %}
        <div class="message {{ msg.message_type|lower }}">
          <div class="bubble">
            <!-- Se tem media -->
            {% if msg.media_url %}
              {% if msg.media_type == 'IMAGE' %}
                <img src="{{ msg.media_url }}" class="chat-image">
              {% elif msg.media_type == 'DOCUMENT' %}
                <a href="{{ msg.media_url }}" download>
                  📄 {{ msg.media_filename }}
                </a>
              {% endif %}
            {% endif %}
            
            <!-- Texto -->
            {% if msg.content %}
              <p>{{ msg.content }}</p>
            {% endif %}
            
            <!-- Timestamp e Status -->
            <div class="msg-footer">
              <span class="time">{{ msg.sent_at|date:"H:i" }}</span>
              {% if msg.message_type == 'SENT' %}
                <span class="status">
                  {% if msg.status == 'READ' %}✓✓ Lido
                  {% elif msg.status == 'DELIVERED' %}✓✓ Entregue
                  {% elif msg.status == 'SENT' %}✓ Enviado
                  {% endif %}
                </span>
              {% endif %}
            </div>
          </div>
        </div>
        {% endfor %}
      </div>
      
      <!-- Input Area -->
      <div class="chat-input">
        <form id="send-message-form">
          <input type="file" id="file-input" accept="image/*,.pdf" style="display:none">
          <button type="button" id="attach-btn">📎</button>
          <input type="text" id="message-input" placeholder="Digite sua mensagem...">
          <button type="submit">Enviar</button>
        </form>
      </div>
    </div>
    ```

  - [ ] **CSS (estilo WhatsApp):**
    ```css
    .messages-container {
      height: 500px;
      overflow-y: auto;
      padding: 20px;
      background: #e5ddd5;
    }
    .message.sent .bubble {
      background: #dcf8c6;
      margin-left: auto;
      max-width: 70%;
    }
    .message.received .bubble {
      background: white;
      margin-right: auto;
      max-width: 70%;
    }
    .chat-image {
      max-width: 300px;
      border-radius: 8px;
    }
    ```

  - [ ] **JavaScript (AJAX envio):**
    ```javascript
    // Enviar mensagem
    document.getElementById('send-message-form').onsubmit = async (e) => {
      e.preventDefault();
      const message = document.getElementById('message-input').value;
      
      const response = await fetch('/api/whatsapp/send/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
          contact_id: '{{ contact.id }}',
          message: message
        })
      });
      
      if (response.ok) {
        // Adicionar mensagem ao chat sem refresh
        const data = await response.json();
        addMessageToChat(data.message);
        document.getElementById('message-input').value = '';
        scrollToBottom();
      }
    };
    
    // Upload de ficheiro
    document.getElementById('attach-btn').onclick = () => {
      document.getElementById('file-input').click();
    };
    
    document.getElementById('file-input').onchange = async (e) => {
      const file = e.target.files[0];
      const formData = new FormData();
      formData.append('file', file);
      formData.append('contact_id', '{{ contact.id }}');
      
      const response = await fetch('/api/whatsapp/send-media/', {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        body: formData
      });
      
      // ... adicionar ao chat
    };
    
    // Polling para novas mensagens (ou usar WebSockets)
    setInterval(async () => {
      const response = await fetch('/api/whatsapp/new-messages/{{ contact.id }}/');
      const data = await response.json();
      data.messages.forEach(msg => addMessageToChat(msg));
    }, 5000);  // A cada 5 segundos
    ```

- [ ] **Configurar rota**
  - [ ] `path('contacts/<uuid:pk>/whatsapp/', ContactWhatsAppChatView, name='contact_whatsapp_chat')`

- [ ] **Adicionar link no ContactDetailView**
  - [ ] Botão "💬 Abrir WhatsApp Chat"
  - [ ] Só mostrar se WhatsAppConfig está ativa

- [ ] **Testing - Chatter**
  - [ ] Test: abrir chat mostra mensagens históricas
  - [ ] Test: enviar mensagem via AJAX funciona
  - [ ] Test: mensagem aparece no chat sem refresh
  - [ ] Test: receber mensagem atualiza chat (polling)

---

## 13.2.6 API Endpoints para Enviar Mensagens (AJAX)

Criar endpoints REST para enviar mensagens via JavaScript.

- [ ] **Criar WhatsAppSendMessageAPI**
  - [ ] View em `apps/marketing/views.py`
  - [ ] Método: POST
  - [ ] URL: `/api/whatsapp/send/`
  - [ ] Body JSON:
    ```json
    {
      "contact_id": "uuid",
      "message": "Olá! Como posso ajudar?"
    }
    ```
  - [ ] Lógica:
    1. Validar contact_id e company
    2. Obter WhatsAppConfig da company
    3. Enviar mensagem via Meta API:
       ```python
       url = f"https://graph.facebook.com/v18.0/{config.phone_number_id}/messages"
       headers = {
         "Authorization": f"Bearer {config.api_key}",
         "Content-Type": "application/json"
       }
       payload = {
         "messaging_product": "whatsapp",
         "to": contact.phone,
         "type": "text",
         "text": {"body": message}
       }
       response = requests.post(url, headers=headers, json=payload)
       ```
    4. Guardar WhatsAppMessage (SENT) na BD
    5. Retornar JSON com message_id

- [ ] **Criar WhatsAppSendMediaAPI**
  - [ ] View para enviar imagens/PDFs
  - [ ] Método: POST (multipart/form-data)
  - [ ] URL: `/api/whatsapp/send-media/`
  - [ ] Body: file (upload) + contact_id
  - [ ] Lógica:
    1. Upload ficheiro para `/media/whatsapp/`
    2. Obter URL público do ficheiro
    3. Enviar via Meta API:
       ```python
       payload = {
         "messaging_product": "whatsapp",
         "to": contact.phone,
         "type": "image",  # ou "document"
         "image": {"link": file_url}
       }
       ```
    4. Guardar WhatsAppMessage com media_url

- [ ] **Criar WhatsAppNewMessagesAPI**
  - [ ] View para polling de novas mensagens
  - [ ] Método: GET
  - [ ] URL: `/api/whatsapp/new-messages/<contact_id>/`
  - [ ] Query param: `?since=timestamp`
  - [ ] Retorna JSON com mensagens recebidas após timestamp

- [ ] **Configurar rotas**
  - [ ] `path('api/whatsapp/send/', WhatsAppSendMessageAPI, name='whatsapp_send_api')`
  - [ ] `path('api/whatsapp/send-media/', WhatsAppSendMediaAPI, name='whatsapp_send_media_api')`
  - [ ] `path('api/whatsapp/new-messages/<uuid:contact_id>/', WhatsAppNewMessagesAPI, name='whatsapp_new_messages_api')`

- [ ] **Permissões**
  - [ ] Apenas users autenticados
  - [ ] Verificar company do user = company do contact

- [ ] **Testing - APIs**
  - [ ] Test: enviar mensagem via API funciona
  - [ ] Test: enviar imagem via API funciona
  - [ ] Test: polling retorna mensagens novas
  - [ ] Test: user de empresa A não envia mensagens de empresa B

---

## 13.2.7 Notificações em Tempo Real (Opcional - WebSockets)

Melhorar experiência com notificações em tempo real (alternativa ao polling).

- [ ] **Instalar Django Channels**
  - [ ] Adicionar `channels` ao requirements.txt
  - [ ] pip install channels
  - [ ] Configurar ASGI em settings

- [ ] **Criar Consumer WebSocket**
  - [ ] Criar `apps/marketing/consumers.py`
  - [ ] ChatConsumer para receber updates em tempo real
  - [ ] Quando nova mensagem chega (webhook), broadcast via WebSocket

- [ ] **Atualizar JavaScript**
  - [ ] Remover polling (setInterval)
  - [ ] Conectar WebSocket: `ws://localhost:8000/ws/chat/`
  - [ ] Escutar eventos de nova mensagem

- [ ] **Testing - WebSockets**
  - [ ] Test: WebSocket conecta
  - [ ] Test: nova mensagem dispara evento
  - [ ] Test: múltiplos users veem updates em tempo real

**NOTA:** WebSockets é opcional. Polling funciona bem para começar!

---

## 13.2.8 Dashboard de Conversas WhatsApp

Criar página central para ver todas as conversas ativas.

- [ ] **Criar WhatsAppConversationsListView**
  - [ ] Listar todos os contactos com mensagens WhatsApp
  - [ ] Mostrar última mensagem
  - [ ] Badge com contador de não lidas
  - [ ] Ordenar por mensagem mais recente

- [ ] **Criar template**
  - [ ] `templates/marketing/whatsapp_conversations.html` (standalone)
  - [ ] Lista de conversas (estilo WhatsApp Web)
  - [ ] Ao clicar, abre chatter

- [ ] **Configurar rota**
  - [ ] `path('whatsapp/conversations/', WhatsAppConversationsListView, name='whatsapp_conversations')`

- [ ] **Adicionar ao menu**
  - [ ] Link "💬 WhatsApp" no navbar
  - [ ] Badge com total de mensagens não lidas

- [ ] **Testing - Conversations**
  - [ ] Test: listar conversas funciona
  - [ ] Test: contador de não lidas está correto
  - [ ] Test: clicar abre chatter

---

## 💰 CUSTOS RESUMIDOS (Meta WhatsApp API)

**Incluir no README ou docs:**

| Item | Detalhe | Custo |
|------|---------|-------|
| **Setup** | Criar conta Meta Business | Grátis |
| **Verificação** | Verificar número de telefone | Grátis |
| **Primeiras mensagens** | 1000 conversas/mês | **GRÁTIS** 🎉 |
| **Após 1000/mês** | Conversas adicionais | ~€0.038/conversa |
| **Marketing** | Campanhas promocionais | ~€0.076/conversa |
| **Media** | Enviar/receber imagens, PDFs | Incluído |

**Conversa = janela de 24 horas**
- 10 mensagens em 24h para mesma pessoa = 1 conversa

**Exemplo real:**
- 5000 conversas/mês = €152 (4000 × €0.038)
- 10000 conversas/mês = €342

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

Ao implementar estas tarefas, seguir esta ordem:

1. ✅ **13.2.1** - Setup Meta API (PRIMEIRO! Sem isto nada funciona)
2. ✅ **13.2.3** - Modelo WhatsAppMessage (base de dados)
3. ✅ **13.2.2** - Webhook (receber mensagens)
4. ✅ **13.2.4** - Celery task (processar mensagens)
5. ✅ **13.2.6** - APIs (enviar mensagens)
6. ✅ **13.2.5** - Chatter UI (interface)
7. ✅ **13.2.8** - Dashboard conversas
8. 🔄 **13.2.7** - WebSockets (opcional, pode ser depois)

---

## 🎯 FLUXO COMPLETO - COMO FUNCIONA

```
ENVIAR MENSAGEM:
User no chatter → Escreve mensagem → Clica "Enviar"
→ AJAX POST /api/whatsapp/send/
→ Python chama Meta API
→ Guarda WhatsAppMessage (SENT) na BD
→ JavaScript adiciona mensagem ao chat (sem refresh)
→ Cliente recebe no WhatsApp dele ✅

RECEBER MENSAGEM:
Cliente envia mensagem no WhatsApp dele
→ Meta API → POST /webhooks/whatsapp/ (webhook)
→ Django recebe webhook
→ Celery task: process_incoming_whatsapp_message
→ Identifica company e contact
→ Se tem imagem/PDF: faz download
→ Guarda WhatsAppMessage (RECEIVED) na BD
→ [Opcional] Notifica via WebSocket
→ Frontend (polling ou WebSocket) busca novas mensagens
→ JavaScript adiciona ao chat automaticamente
→ User vê a resposta! ✅

ANEXOS:
Cliente envia foto
→ Webhook recebe media_id
→ Celery task chama Meta API para obter URL
→ Download da imagem para /media/whatsapp/
→ Guarda media_url na BD
→ Chatter mostra imagem renderizada ✅
```

---

## 📋 REQUISITOS TÉCNICOS

**Servidor:**
- ✅ HTTPS obrigatório (webhook não funciona com HTTP)
- ✅ Domínio público (não pode ser localhost)
- ✅ Porta 443 aberta

**Para desenvolvimento local:**
- Use **ngrok** para criar túnel HTTPS:
  ```bash
  ngrok http 8000
  # Retorna: https://abc123.ngrok.io
  # Usar este URL no webhook da Meta
  ```

---

## 13.3 Modelo Campaign

Criar modelo para campanhas de marketing.

- [ ] **Criar modelo Campaign**
  - [ ] Campos: name, description, campaign_type (WHATSAPP, EMAIL)
  - [ ] Campos: message_template, media_file
  - [ ] Campos: status (DRAFT, SCHEDULED, SENT)
  - [ ] Campos: scheduled_date, sent_date

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar CampaignAdmin

---

## 13.4 Seleção de Destinatários

Criar sistema para selecionar destinatários da campanha.

- [ ] **Criar modelo CampaignRecipient**
  - [ ] Campos: campaign (FK), contact (FK)
  - [ ] Campos: status (PENDING, SENT, FAILED), sent_date, error_message

- [ ] **Criar view de seleção**
  - [ ] Listar contactos com checkboxes
  - [ ] Filtros: tags, localização, tipo
  - [ ] Botão "Selecionar Todos", "Selecionar Filtrados"

- [ ] **Criar template**
  - [ ] `templates/marketing/campaign_recipients.html` (standalone)

---

## 13.5 Criação e Envio de Campanha WhatsApp

Criar views para criar e enviar campanhas.

- [ ] **Criar CampaignCreateView**
  - [ ] Form: nome, mensagem, anexo (PDF)
  - [ ] Preview da mensagem
  - [ ] Seleção de destinatários

- [ ] **Criar CampaignSendView**
  - [ ] Verificar configuração WhatsApp
  - [ ] Enviar mensagens via Celery task (assíncrono)
  - [ ] Atualizar status de cada destinatário

- [ ] **Criar Celery task**
  - [ ] Task `send_campaign_messages(campaign_id)`
  - [ ] Loop por destinatários
  - [ ] Enviar via WhatsApp API
  - [ ] Registrar sucesso/falha

- [ ] **Criar templates**
  - [ ] `templates/marketing/campaign_create.html` (standalone)
  - [ ] `templates/marketing/campaign_send.html` (standalone)

- [ ] **Configurar rotas**
  - [ ] `path('marketing/campaigns/new/', CampaignCreateView, name='campaign_create')`
  - [ ] `path('marketing/campaigns/<uuid:pk>/send/', CampaignSendView, name='campaign_send')`

- [ ] **Testing - Campaign Send**
  - [ ] Test: criar campanha funciona
  - [ ] Test: enviar campanha dispara Celery task
  - [ ] Test: mensagens são enviadas

---

## 13.6 Relatórios de Campanhas

Criar views de relatórios de campanhas.

- [ ] **Criar CampaignReportView**
  - [ ] Mostrar lista de campanhas
  - [ ] Para cada campanha: enviados, falhados, pendentes
  - [ ] Taxa de sucesso

- [ ] **Criar template**
  - [ ] `templates/marketing/campaign_reports.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('marketing/reports/', CampaignReportView, name='campaign_reports')`

- [ ] **Testing - Campaign Reports**
  - [ ] Test: relatório mostra estatísticas corretas

---

# 🚀 FASE 13: STOCK MANAGEMENT AVANÇADO

**⏱ Tempo estimado:** 3-4 dias
**🎯 Objetivo:** Implementar funcionalidades avançadas de stock (motivos de ajuste com impacto financeiro, perdas fiscais, histórico detalhado)
**📦 Dependências:** Fase 6 (inventory — nova arquitetura com Warehouse/Location/StockMovement/StockQuant), Fase 9 (finance)

> **NOTA:** Com a nova arquitetura de inventário (Fase 6.4+), os ajustes de stock já são feitos via StockMovement
> de tipo "adjustment" (ver 6.18). Esta fase adiciona a camada de MOTIVOS (StockAdjustmentReason) e a
> integração financeira para perdas. O modelo StockMovement já tem operation_kind='adjustment'.

---

## 13.1 Modelo StockAdjustmentReason

Criar modelo para motivos de ajuste. Associado aos StockMovements de tipo adjustment.

- [ ] **Criar modelo**
  - [ ] Campos: name, is_loss, description
  - [ ] Ex: "Quebra", "Vencimento", "Erro de contagem", "Roubo", "Amostra"

- [ ] **Registrar no Admin**
  - [ ] Criar StockAdjustmentReasonAdmin

---

## 13.2 Atualizar StockMovement com Reason

Adicionar campo reason ao StockMovement (apenas usado quando operation_kind='adjustment').

- [ ] **Criar migration**
  - [ ] Adicionar campo reason (FK para StockAdjustmentReason, null=True, blank=True)
  - [ ] Adicionar campo is_loss (Boolean, default=False)
  - [ ] Validação: reason obrigatório apenas se operation_kind='adjustment'

- [ ] **Atualizar InventoryAdjustmentCreateView (6.18)**
  - [ ] Adicionar seletor de reason no formulário de ajuste
  - [ ] Se reason.is_loss=True, marcar is_loss automaticamente

---

## 13.3 Integração com Financeiro para Perdas

Quando ajuste é perda, registar impacto financeiro.

- [ ] **Hook no action_validate() do StockMovement**
  - [ ] Se is_loss=True e operation_kind='adjustment', ao validar:
    - [ ] Para cada StockMovementLine: criar Transaction (LOSS)
    - [ ] amount = line.product.cost_price * line.quantity_done
  - [ ] Usar signal post_save ou override do action_validate()

- [ ] **Testing - Loss Integration**
  - [ ] Test: ajuste com perda cria transação financeira
  - [ ] Test: perda aparece no balanço mensal

---

## 13.4 Relatório de Perdas

Criar relatório específico de perdas.

- [ ] **Criar LossReportView**
  - [ ] Filtros: período, produto, motivo
  - [ ] Mostrar: total de perdas em valor, quantidade
  - [ ] Discriminação por motivo

- [ ] **Criar template**
  - [ ] `templates/inventory/loss_report.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('inventory/losses/', LossReportView, name='loss_report')`

- [ ] **Testing - Loss Report**
  - [ ] Test: relatório mostra perdas corretas

---

## 13.5 Histórico de Stock por Produto

Criar view de histórico completo de stock com saldo calculado (complementa 6.17 ProductStockDetailView).

- [ ] **Criar ProductStockHistoryView**
  - [ ] Listar todos os StockMovementLines de um produto (dos movimentos em estado 'done')
  - [ ] Mostrar saldo acumulado após cada movimentação (running total)
  - [ ] Filtros: localização, período, tipo de operação

- [ ] **Criar template**
  - [ ] `templates/inventory/product_stock_history.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('inventory/products/<uuid:pk>/stock-history/', ProductStockHistoryView, name='product_stock_history')`

- [ ] **Testing - Stock History**
  - [ ] Test: histórico mostra todas as movimentações

---

## 13.6 Alertas e Notificações de Stock (Avançado)

Sistema avançado de alertas — complementa 6.20 (alertas básicos) com regras mais sofisticadas.

- [ ] **Criar Celery task periódica**
  - [ ] Task que roda diariamente
  - [ ] Verificar: StockQuant.quantity < Product.min_stock (por armazém)
  - [ ] Verificar: ReorderingRules ativas e acionar auto-reabastecimento (ver 6.11)
  - [ ] Enviar email/notificação para admins com resumo

- [ ] **Adicionar no Dashboard**
  - [ ] Widget de alertas de stock

- [ ] **Testing - Stock Alerts**
  - [ ] Test: task identifica produtos com stock baixo
  - [ ] Test: notificações são enviadas

---

# 🚀 FASE 14: PDF SCANNING (ENTRADA DE COMPRAS)

**⏱ Tempo estimado:** 5-6 dias
**🎯 Objetivo:** Implementar scanning de PDFs para criar documentos de compra automaticamente
**📦 Dependências:** Fase 6 (inventory), Fase 7 (purchases)

---

## 14.1 Análise de PDFs de Fornecedores

Analisar estrutura dos PDFs recebidos.

- [ ] **Coletar amostras**
  - [ ] Obter PDFs exemplo dos fornecedores
  - [ ] Identificar padrões: referência, quantidade, preço

- [ ] **Documentar estrutura**
  - [ ] Criar documento com regras de parsing

---

## 14.2 Configuração de Parser de PDF

Instalar e configurar biblioteca de parsing.

- [ ] **Instalar dependências**
  - [ ] Adicionar PyPDF2 ou pdfplumber ao requirements.txt
  - [ ] pip install

- [ ] **Criar helper functions**
  - [ ] Criar `apps/purchases/pdf_parser.py`
  - [ ] Função `extract_text_from_pdf(pdf_file)`

---

## 14.3 Lógica de Extração de Dados

Criar lógica para extrair referências, quantidades e preços.

- [ ] **Criar função de parsing**
  - [ ] Função `parse_purchase_lines(text)`
  - [ ] Usar regex para identificar padrões
  - [ ] Retornar lista de dicionários: {reference, quantity, price}

- [ ] **Testing - Parser**
  - [ ] Test: parser extrai dados de PDF exemplo
  - [ ] Test: tratar erros de formato

---

## 14.4 View de Upload de PDF

Criar view para upload de PDF.

- [ ] **Criar PDFUploadView**
  - [ ] Form de upload
  - [ ] Processar PDF
  - [ ] Exibir preview dos dados extraídos
  - [ ] Permitir correções manuais

- [ ] **Criar template**
  - [ ] `templates/purchases/pdf_upload.html` (standalone)
  - [ ] Tabela editável com dados extraídos

- [ ] **Configurar rota**
  - [ ] `path('purchases/upload-pdf/', PDFUploadView, name='purchase_pdf_upload')`

- [ ] **Testing - PDF Upload**
  - [ ] Test: upload funciona
  - [ ] Test: dados são exibidos para review

---

## 14.5 Criação Automática de PurchaseOrder

Criar PurchaseOrder automaticamente a partir dos dados.

- [ ] **Criar função**
  - [ ] Função `create_purchase_from_parsed_data(data, supplier)`
  - [ ] Verificar se produtos existem (por referência)
  - [ ] Criar PurchaseOrder e linhas
  - [ ] Marcar como DRAFT para revisão

- [ ] **Integrar na view**
  - [ ] Botão "Criar Documento de Compra"
  - [ ] Redirecionar para PurchaseOrderDetailView

- [ ] **Testing - Auto Create**
  - [ ] Test: criar purchase order automático funciona
  - [ ] Test: linhas são criadas corretamente
  - [ ] Test: produtos não encontrados são sinalizados

---

## 14.6 Tratamento de Erros e Edge Cases

Tratar casos onde produtos não existem ou dados estão incorretos.

- [ ] **Listar produtos não encontrados**
  - [ ] Mostrar referências que não existem no sistema
  - [ ] Permitir criar produtos inline ou mapear manualmente

- [ ] **Validações**
  - [ ] Verificar se quantidades/preços são válidos
  - [ ] Alertar sobre valores atípicos

- [ ] **Testing - Error Handling**
  - [ ] Test: produtos não encontrados são listados
  - [ ] Test: validações funcionam

---

# 🚀 FASE 15: APP - RELATÓRIOS E DASHBOARD

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de relatórios e dashboard com KPIs principais
**📦 Dependências:** Fase 8 (Vendas), Fase 7 (Compras), Fase 9 (Financeiro), Fase 6 (Inventário)


## 14.7 Modelo EmailInboxConfig (Configuração de Email Input por Empresa)

Criar modelo para configurar contas de email que receberão PDFs automaticamente.

- [ ] **Criar modelo EmailInboxConfig**
  - [ ] Criar em `apps/purchases/models.py` ou `apps/core/models.py`
  - [ ] Herdar de AbstractBaseModel
  - [ ] Campo: company (ForeignKey para Company, **OBRIGATÓRIO**, on_delete=CASCADE)
  - [ ] Campo: name (CharField, descrição tipo "Scanner Compras Fornecedor X")
  - [ ] Campo: email_address (EmailField, email que vai receber os PDFs)
  - [ ] Campo: email_password (CharField, encriptado)
  - [ ] Campo: imap_server (CharField, default='imap.gmail.com')
  - [ ] Campo: imap_port (IntegerField, default=993)
  - [ ] Campo: use_ssl (BooleanField, default=True)
  - [ ] Campo: auto_process (BooleanField, default=True, se deve processar automaticamente)
  - [ ] Campo: default_supplier (ForeignKey para Contact, opcional, fornecedor padrão)
  - [ ] Campo: folder_to_monitor (CharField, default='INBOX', pasta IMAP a monitorar)
  - [ ] Campo: mark_as_read (BooleanField, default=True)
  - [ ] Campo: last_check (DateTimeField, nullable, último check de emails)
  - [ ] Campo: is_active (BooleanField, default=True)
  - [ ] Meta: unique_together = ['company', 'email_address']
  - [ ] Método: test_connection() - testa ligação IMAP
  - [ ] Método: get_unread_emails() - retorna lista de emails não lidos com PDFs

- [ ] **Validações importantes**
  - [ ] Validar que company não pode ser null (OBRIGATÓRIO!)
  - [ ] Validar formato de email
  - [ ] Validar credenciais antes de guardar (botão "Testar Conexão")

- [ ] **Criar migrations**
  - [ ] Executar makemigrations
  - [ ] Executar migrate

- [ ] **Registrar no Admin**
  - [ ] Criar EmailInboxConfigAdmin
  - [ ] list_display: company, name, email_address, auto_process, is_active, last_check
  - [ ] list_filter: company, is_active, auto_process
  - [ ] search_fields: name, email_address
  - [ ] Botão customizado "Testar Conexão" (chama test_connection())
  - [ ] Botão customizado "Processar Agora" (força check manual)
  - [ ] Fieldsets: Empresa, Configuração de Email (IMAP), Processamento, Status

- [ ] **Security - Encriptação de Password**
  - [ ] Usar django.contrib.auth.hashers ou cryptography.fernet
  - [ ] Encriptar email_password antes de guardar
  - [ ] Desencriptar apenas quando necessário (no Celery task)

- [ ] **Testing - EmailInboxConfig**
  - [ ] Test: criar config com company obrigatório funciona
  - [ ] Test: criar config sem company falha (ValidationError)
  - [ ] Test: test_connection() funciona com credenciais válidas
  - [ ] Test: test_connection() falha com credenciais inválidas
  - [ ] Test: get_unread_emails() retorna emails com PDFs
  - [ ] Test: duas empresas podem ter configs diferentes
  - [ ] Test: password é encriptado no save

---

## 14.8 Sistema de Monitoramento de Email Automático (Celery Task)

Criar Celery task que verifica emails periodicamente e processa PDFs.

- [ ] **Criar helper functions em apps/purchases/email_utils.py**
  - [ ] Função: connect_to_imap(config) - conecta ao servidor IMAP
  - [ ] Função: fetch_unread_emails_with_pdfs(mail, folder) - busca emails não lidos com PDFs
  - [ ] Função: download_pdf_from_email(email_message) - extrai PDF do anexo
  - [ ] Função: mark_email_as_processed(mail, email_id) - marca como lido/processado
  - [ ] Tratamento de erros robusto (conexão falha, timeout, etc.)

- [ ] **Criar Celery task periódica**
  - [ ] Criar `apps/purchases/tasks.py`
  - [ ] Task: `check_inbox_for_pdfs()` (roda periodicamente)
  - [ ] Lógica:
    1. Buscar todas as EmailInboxConfig ativas (is_active=True, auto_process=True)
    2. Para cada config:
       - Conectar ao IMAP
       - Buscar emails não lidos com PDFs
       - Para cada email com PDF:
         * Download do PDF
         * Processar via parse_purchase_lines() (já existe na tarefa 14.3)
         * Criar PurchaseOrder em DRAFT (tarefa 14.5)
         * Marcar email como lido
         * Registrar em log
       - Atualizar last_check
    3. Registrar estatísticas (quantos emails processados, quantos falharam)
    4. Enviar notificação em caso de erros

- [ ] **Configurar Celery Beat (agendamento)**
  - [ ] Configurar em `config/celery.py`
  - [ ] Schedule: rodar a cada 5 minutos (ajustável via SystemSetting)
  - [ ] Task: `check_inbox_for_pdfs.apply_async()`

- [ ] **Criar modelo EmailProcessingLog**
  - [ ] Campos: config (FK), email_from, email_subject, email_date, pdf_filename
  - [ ] Campos: status (SUCCESS, FAILED, PARTIAL), error_message
  - [ ] Campos: purchase_order (FK, nullable, se criou PO)
  - [ ] Campos: processed_at, processing_time_seconds
  - [ ] Para auditoria e debug

- [ ] **Registrar EmailProcessingLog no Admin**
  - [ ] Criar EmailProcessingLogAdmin
  - [ ] list_display: config, email_from, status, pdf_filename, purchase_order, processed_at
  - [ ] list_filter: status, config__company
  - [ ] search_fields: email_from, email_subject, pdf_filename

- [ ] **Criar SystemSetting para controlo**
  - [ ] Criar setting: `email_check_interval_minutes` (default: 5)
  - [ ] Criar setting: `email_processing_enabled` (ON/OFF global)
  - [ ] Criar setting: `email_notification_on_error` (default: True)

- [ ] **Testing - Email Monitoring**
  - [ ] Test: task conecta ao email e busca PDFs
  - [ ] Test: task processa PDF e cria PurchaseOrder
  - [ ] Test: task marca email como lido
  - [ ] Test: task regista logs corretamente
  - [ ] Test: task falha gracefully quando credenciais estão erradas
  - [ ] Test: task respeita auto_process=False
  - [ ] Test: task processa apenas emails da empresa correta (multi-company)
  - [ ] Test: Celery Beat schedule funciona (mock de tempo)

---

## 14.9 Views de Gestão de Email Inbox Config

Criar interface para configurar e monitorar emails.

- [ ] **Criar EmailInboxConfigListView**
  - [ ] Listar todas as configs da empresa ativa
  - [ ] Filtrar por company automaticamente (session['active_company'])
  - [ ] Mostrar: email, fornecedor default, status (ativo/inativo), último check, auto-process
  - [ ] Badges visuais: ✅ Ativo, ⏸️ Pausado, ❌ Erro
  - [ ] Link para editar, testar conexão, ver logs

- [ ] **Criar EmailInboxConfigCreateView**
  - [ ] Form com todos os campos
  - [ ] Campo company auto-preenchido com active_company (hidden + readonly)
  - [ ] Input de password tipo password (escondido)
  - [ ] Botão "Testar Conexão" AJAX (testa antes de guardar)
  - [ ] Validação: email único por empresa
  - [ ] Após criar, redirecionar para lista

- [ ] **Criar EmailInboxConfigUpdateView**
  - [ ] Mesmo form que Create
  - [ ] Campo company desabilitado (não pode mudar empresa)
  - [ ] Mostrar last_check e estatísticas
  - [ ] Botão "Processar Agora" (dispara task manualmente)

- [ ] **Criar EmailInboxConfigTestView (AJAX)**
  - [ ] Endpoint POST para testar conexão
  - [ ] Recebe: email, password, imap_server, imap_port
  - [ ] Tenta conectar via IMAP
  - [ ] Retorna JSON: {success: true/false, message: "...", email_count: X}
  - [ ] Se sucesso, mostra quantos emails não lidos existem

- [ ] **Criar EmailProcessingLogListView**
  - [ ] Listar logs da config selecionada
  - [ ] Filtros: status, período
  - [ ] Mostrar: email remetente, assunto, status, PO criada, erro
  - [ ] Link para ver PurchaseOrder criada

- [ ] **Criar templates**
  - [ ] `templates/purchases/email_inbox_config_list.html` (standalone)
  - [ ] `templates/purchases/email_inbox_config_form.html` (standalone, usado em create/update)
  - [ ] `templates/purchases/email_processing_logs.html` (standalone)

- [ ] **Configurar rotas**
  - [ ] `path('purchases/email-configs/', EmailInboxConfigListView, name='email_inbox_config_list')`
  - [ ] `path('purchases/email-configs/new/', EmailInboxConfigCreateView, name='email_inbox_config_create')`
  - [ ] `path('purchases/email-configs/<uuid:pk>/edit/', EmailInboxConfigUpdateView, name='email_inbox_config_update')`
  - [ ] `path('purchases/email-configs/test/', EmailInboxConfigTestView, name='email_inbox_config_test')` (AJAX)
  - [ ] `path('purchases/email-configs/<uuid:pk>/logs/', EmailProcessingLogListView, name='email_processing_logs')`

- [ ] **Adicionar ao menu de Compras**
  - [ ] Link "Configurar Emails" no dropdown de Compras
  - [ ] Badge com contagem de configs ativas

- [ ] **Testing - Email Config Views**
  - [ ] Test: criar config funciona
  - [ ] Test: company é obrigatório e auto-preenchido
  - [ ] Test: testar conexão via AJAX funciona
  - [ ] Test: editar config funciona (mas não permite mudar company)
  - [ ] Test: listar configs filtra por empresa ativa
  - [ ] Test: user de empresa A não vê configs de empresa B
  - [ ] Test: ver logs funciona
  - [ ] Test: botão "Processar Agora" dispara task

---

## 💡 INTEGRAÇÃO COM FASE 16 (OPCIONAL)

**Sugestão:** Adicionar também na **Fase 16 (Configurações)** uma tarefa:

### 16.9 Configuração Global de Email Input (UI Settings)

- [ ] **Adicionar ao SettingsIndexView**
  - [ ] Card "Email Automation" com link para EmailInboxConfigListView
  - [ ] Mostrar: quantas configs ativas, último processamento

- [ ] **Adicionar SystemSettings**
  - [ ] Setting: `email_check_interval_minutes`
  - [ ] Setting: `email_processing_enabled` (ON/OFF toggle)
  - [ ] Setting: `email_max_retries` (quantas tentativas em caso de erro)

---

## 📋 FLUXO COMPLETO - COMO FUNCIONA

```
1. USER CONFIG (Fase 16 ou Purchase Settings):
   └─ Cria EmailInboxConfig para cubicxscanner@gmail.com
   └─ Associa à Empresa A (company obrigatório!)
   └─ Define fornecedor padrão (opcional)
   └─ Ativa auto_process = True

2. CELERY TASK (roda a cada 5 min):
   └─ Busca EmailInboxConfig ativas
   └─ Conecta ao cubicxscanner@gmail.com (IMAP)
   └─ Busca emails não lidos com PDFs
   └─ Para cada email:
      ├─ Download PDF
      ├─ Extrai texto (PyPDF2)
      ├─ Parse referências/quantidades/preços (Tarefa 14.3)
      ├─ Cria PurchaseOrder DRAFT (Tarefa 14.5)
      ├─ Associa à Empresa A (via config.company)
      ├─ Marca email como lido
      └─ Regista em EmailProcessingLog

3. USER REVIEW (Purchase Orders):
   └─ Vê lista de POs em DRAFT
   └─ Revê dados extraídos
   └─ Confirma ou edita
   └─ Aprova PO → Stock movement automático
```

---

## ✅ CONFIRMAÇÕES IMPORTANTES

1. ✅ **Company é OBRIGATÓRIO** - EmailInboxConfig.company não pode ser null
2. ✅ **Multi-company funciona** - Cada empresa tem seus próprios emails configurados
3. ✅ **Emails ficam separados** - Empresa A não vê/processa emails da Empresa B
4. ✅ **Segurança** - Passwords encriptados
5. ✅ **Auditoria** - Todos os processamentos registados em EmailProcessingLog
6. ✅ **Flexibilidade** - Pode ter 1, 5, 10+ emails configurados por empresa
7. ✅ **Controlo** - Pode desativar globalmente ou por config

---

## 15.1 Criação da App 'reports'

Criar app Django para relatórios.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp reports apps/reports`
  - [ ] Adicionar 'apps.reports' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar `apps/reports/models.py` (se necessário para cache)
  - [ ] Criar `apps/reports/views.py`
  - [ ] Criar `apps/reports/urls.py`
  - [ ] Criar `apps/reports/services.py` (lógica de cálculos)

---

## 15.2 Dashboard Principal

Criar dashboard com KPIs principais do sistema.

- [ ] **Criar DashboardView**
  - [ ] KPIs: Vendas do Mês, Compras do Mês, Margem de Lucro, Stock Total
  - [ ] Gráfico: Vendas vs Compras (últimos 12 meses)
  - [ ] Gráfico: Top 10 Produtos Vendidos
  - [ ] Gráfico: Top 10 Clientes
  - [ ] Lista: Leads Pendentes, Vendas em Aberto, Compras a Receber
  - [ ] Alertas: Produtos com Stock Baixo, Faturas Vencidas

- [ ] **Criar template**
  - [ ] `templates/reports/dashboard.html`
  - [ ] Layout grid com cards de KPIs
  - [ ] Gráficos usando Chart.js ou similar
  - [ ] Filtro por período (último mês, últimos 3 meses, último ano)
  - [ ] Responsive para mobile

- [ ] **Configurar rota**
  - [ ] `path('reports/dashboard/', DashboardView, name='reports_dashboard')`

- [ ] **Testing - Dashboard**
  - [ ] Test: KPIs calculam corretamente
  - [ ] Test: gráficos renderizam
  - [ ] Test: filtros funcionam

---

## 15.3 Relatório de Vendas

Criar relatório detalhado de vendas.

- [ ] **Criar SalesReportView**
  - [ ] Filtros: Período, Cliente, Produto, Estado
  - [ ] Totais: Vendas, Custo, Margem, Quantidade
  - [ ] Tabela: Lista de vendas com detalhes
  - [ ] Exportar CSV/Excel
  - [ ] Gráfico: Vendas por mês

- [ ] **Criar template**
  - [ ] `templates/reports/sales_report.html`
  - [ ] Filtros sidebar
  - [ ] Tabela com paginação
  - [ ] Cards com totais

- [ ] **Configurar rota**
  - [ ] `path('reports/sales/', SalesReportView, name='sales_report')`

- [ ] **Testing - Sales Report**
  - [ ] Test: filtros funcionam
  - [ ] Test: totais calculam corretamente
  - [ ] Test: exportação funciona

---

## 15.4 Relatório de Compras

Criar relatório detalhado de compras.

- [ ] **Criar PurchasesReportView**
  - [ ] Filtros: Período, Fornecedor, Produto, Estado
  - [ ] Totais: Compras, Custo Médio por Produto
  - [ ] Tabela: Lista de compras com detalhes
  - [ ] Exportar CSV/Excel

- [ ] **Criar template**
  - [ ] `templates/reports/purchases_report.html`

- [ ] **Configurar rota**
  - [ ] `path('reports/purchases/', PurchasesReportView, name='purchases_report')`

- [ ] **Testing - Purchases Report**
  - [ ] Test: relatório gera corretamente
  - [ ] Test: exportação funciona

---

## 15.5 Relatório Financeiro

Criar relatório de perdas e ganhos.

- [ ] **Criar FinancialReportView**
  - [ ] Totais: Receitas, Despesas, Lucro Líquido
  - [ ] Filtro por período
  - [ ] Breakdown por categoria
  - [ ] Gráfico: Evolução mensal

- [ ] **Criar template**
  - [ ] `templates/reports/financial_report.html`

- [ ] **Configurar rota**
  - [ ] `path('reports/financial/', FinancialReportView, name='financial_report')`

- [ ] **Testing - Financial Report**
  - [ ] Test: cálculos de lucro corretos
  - [ ] Test: breakdown por categoria funciona

---

## 15.6 Relatório de Stock

Criar relatório de inventário.

- [ ] **Criar StockReportView**
  - [ ] Lista: Produtos com stock atual
  - [ ] Alertas: Produtos abaixo do mínimo
  - [ ] Valor total do stock
  - [ ] Filtro por categoria

- [ ] **Criar template**
  - [ ] `templates/reports/stock_report.html`

- [ ] **Configurar rota**
  - [ ] `path('reports/stock/', StockReportView, name='stock_report')`

- [ ] **Testing - Stock Report**
  - [ ] Test: stock atual correto
  - [ ] Test: alertas funcionam

---

# 🚀 FASE 16: APP - CONFIGURAÇÕES E PARÂMETROS

**⏱ Tempo estimado:** 3-4 dias
**🎯 Objetivo:** Criar sistema de configurações globais e parâmetros do sistema
**📦 Dependências:** Fase 3 (base models)

---

## 16.1 Criação da App 'settings'

Criar app Django para configurações.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp settings apps/settings`
  - [ ] Adicionar 'apps.settings' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar `apps/settings/models.py`
  - [ ] Criar `apps/settings/views.py`
  - [ ] Criar `apps/settings/forms.py`
  - [ ] Criar `apps/settings/urls.py`

---

## 16.2 Modelo SystemSetting

Criar modelo para parâmetros globais do sistema.

- [ ] **Criar modelo SystemSetting**
  - [ ] Campo: key (CharField, unique)
  - [ ] Campo: value (TextField, JSON)
  - [ ] Campo: description (TextField)
  - [ ] Campo: setting_type (STRING, NUMBER, BOOLEAN, JSON)
  - [ ] Método get_value() - parse value baseado em setting_type
  - [ ] Método set_value() - valida e guarda

- [ ] **Criar migrations**
  - [ ] Executar makemigrations
  - [ ] Executar migrate

- [ ] **Registrar no Admin**
  - [ ] Criar SystemSettingAdmin
  - [ ] list_display: key, value, description

- [ ] **Testing - SystemSetting**
  - [ ] Test: criar setting funciona
  - [ ] Test: get_value parse corretamente
  - [ ] Test: set_value valida

---

## 16.3 Modelo CompanyInfo

Criar modelo para informações da empresa.

- [ ] **Criar modelo CompanyInfo (Singleton)**
  - [ ] Campos: company_name, nif, address, city, postal_code, phone, email, website
  - [ ] Campo: logo (ImageField)
  - [ ] Campo: primary_color, secondary_color (para branding)
  - [ ] Campo: email_footer_text
  - [ ] Singleton pattern (apenas 1 registo)

- [ ] **Criar migrations**
  - [ ] Executar makemigrations
  - [ ] Executar migrate

- [ ] **Registrar no Admin**
  - [ ] Criar CompanyInfoAdmin

- [ ] **Testing - CompanyInfo**
  - [ ] Test: singleton funciona (não permite criar 2º registo)
  - [ ] Test: logo upload funciona

---

## 16.4 Configurações de Empresa (View)

Criar interface para editar informações da empresa.

- [ ] **Criar CompanyInfoUpdateView**
  - [ ] Form com todos os campos
  - [ ] Upload de logo
  - [ ] Color pickers para branding

- [ ] **Criar template**
  - [ ] `templates/settings/company_info.html`
  - [ ] Form com tabs: Info Básica, Branding, Email

- [ ] **Configurar rota**
  - [ ] `path('settings/company/', CompanyInfoUpdateView, name='company_settings')`

- [ ] **Testing - Company Settings**
  - [ ] Test: editar info funciona
  - [ ] Test: logo upload funciona
  - [ ] Test: cores são validadas

---

## 16.5 Configurações de Sistema (View)

Criar interface para editar parâmetros globais.

- [ ] **Criar SystemSettingsView**
  - [ ] Lista de todos os settings
  - [ ] Form inline para editar
  - [ ] Categorias: Geral, Vendas, Compras, Stock, Financeiro

- [ ] **Parâmetros padrão a criar**
  - [ ] `stock_alert_threshold` (nível mínimo de stock)
  - [ ] `default_tax_rate` (IVA padrão)
  - [ ] `currency` (moeda padrão)
  - [ ] `date_format` (formato de data)
  - [ ] `pagination_size` (items por página)
  - [ ] `allow_negative_stock` (permitir stock negativo)

- [ ] **Criar template**
  - [ ] `templates/settings/system_settings.html`
  - [ ] Tabs por categoria
  - [ ] Form para cada setting

- [ ] **Configurar rota**
  - [ ] `path('settings/system/', SystemSettingsView, name='system_settings')`

- [ ] **Testing - System Settings**
  - [ ] Test: editar settings funciona
  - [ ] Test: validações funcionam

---

## 16.6 Configurações de Email

Criar interface para configurar envio de emails.

- [ ] **Criar EmailSettingsView**
  - [ ] Form: SMTP host, port, username, password, use_tls
  - [ ] Botão "Testar Conexão"
  - [ ] Email de teste

- [ ] **Criar template**
  - [ ] `templates/settings/email_settings.html`

- [ ] **Configurar rota**
  - [ ] `path('settings/email/', EmailSettingsView, name='email_settings')`

- [ ] **Testing - Email Settings**
  - [ ] Test: guardar settings funciona
  - [ ] Test: teste de conexão funciona

---

## 16.7 Menu de Configurações

Criar menu principal de configurações.

- [ ] **Criar SettingsIndexView**
  - [ ] Cards: Empresa, Sistema, Email, Utilizadores, Backups
  - [ ] Links para cada secção

- [ ] **Criar template**
  - [ ] `templates/settings/index.html`
  - [ ] Grid de cards com ícones

- [ ] **Configurar rota**
  - [ ] `path('settings/', SettingsIndexView, name='settings_index')`

- [ ] **Testing - Settings Menu**
  - [ ] Test: menu renderiza
  - [ ] Test: links funcionam

---

## 16.8 Backup e Restore

Criar funcionalidade de backup da base de dados.

- [ ] **Criar BackupView**
  - [ ] Botão "Criar Backup"
  - [ ] Lista de backups existentes com data
  - [ ] Botão "Download" para cada backup
  - [ ] Botão "Restore" (com confirmação)

- [ ] **Criar template**
  - [ ] `templates/settings/backup.html`

- [ ] **Configurar rota**
  - [ ] `path('settings/backup/', BackupView, name='backup_settings')`

- [ ] **Testing - Backup**
  - [ ] Test: criar backup funciona
  - [ ] Test: download backup funciona
  - [ ] Test: restore funciona (em ambiente de test)

---

# 🚀 FASE 17: INTEGRAÇÃO FINAL E DEPLOYMENT

**⏱ Tempo estimado:** 3-4 dias
**🎯 Objetivo:** Integrar todos os módulos, testes finais e preparar para produção
**📦 Dependências:** Todas as fases anteriores

---

## 17.1 Testes de Integração

Testar integração entre todos os módulos.

- [ ] **Testar fluxo completo**
  - [ ] Criar cliente → Criar venda → Confirmar → Entregar → Faturar
  - [ ] Verificar stock é atualizado
  - [ ] Verificar transação financeira é criada

- [ ] **Testar fluxo de compras**
  - [ ] Upload PDF → Criar compra → Confirmar → Receber
  - [ ] Verificar stock é atualizado
  - [ ] Verificar transação financeira é criada

- [ ] **Testar ajustes de stock com perdas**
  - [ ] Criar ajuste → Verificar stock → Verificar transação financeira

---

## 17.2 Dashboard Principal Completo

Finalizar dashboard principal com todos os widgets.

- [ ] **Adicionar widgets**
  - [ ] Vendas do mês
  - [ ] Compras do mês
  - [ ] Lucro do mês
  - [ ] Alertas de stock
  - [ ] Últimas vendas
  - [ ] Top produtos

- [ ] **Adicionar gráficos**
  - [ ] Gráfico de vendas (últimos 6 meses)
  - [ ] Gráfico de lucro

---

## 17.3 Menu de Navegação Final

Criar menu de navegação completo.

- [ ] **Organizar menu**
  - [ ] Dashboard
  - [ ] Vendas (Listar, Criar, Relatórios)
  - [ ] Compras (Listar, Criar, Upload PDF, Relatórios)
  - [ ] Inventário (Produtos, Stock, Ajustes, Movimentações)
  - [ ] Contactos (Listar, Criar, Importar)
  - [ ] Financeiro (Dashboard, Transações, Balanço, P&L)
  - [ ] Marketing (Campanhas, Criar, Relatórios)
  - [ ] Configurações

---

## 17.4 Otimizações de Performance

Otimizar consultas e performance.

- [ ] **Adicionar select_related e prefetch_related**
  - [ ] Otimizar queries em views de listagem

- [ ] **Adicionar cache**
  - [ ] Cache de dashboard
  - [ ] Cache de relatórios

- [ ] **Adicionar índices**
  - [ ] Índices em campos de busca

---

## 17.5 Documentação

Criar documentação básica.

- [ ] **README.md**
  - [ ] Instruções de instalação
  - [ ] Configuração de .env
  - [ ] Como rodar o projeto

- [ ] **Documentação de API interna**
  - [ ] Documentar principais funções e models

---

## 17.6 Preparação para Produção

Configurar para ambiente de produção.

- [ ] **Settings de produção**
  - [ ] DEBUG = False
  - [ ] ALLOWED_HOSTS configurado
  - [ ] SECRET_KEY via .env

- [ ] **Configurar static files**
  - [ ] Executar collectstatic
  - [ ] Configurar servir static files

- [ ] **Configurar Gunicorn/uWSGI**
  - [ ] Instalar e configurar servidor WSGI

- [ ] **Configurar Nginx**
  - [ ] Configurar proxy reverso

---

# 🚀 FASE 18: TESTES AUTOMATIZADOS UI (PLAYWRIGHT)

**⏱ Tempo estimado:** 8-10 dias
**🎯 Objetivo:** Criar sistema de testes automatizados da interface do utilizador com Playwright, simulando ações humanas reais e gerando relatórios detalhados em PDF
**📦 Dependências:** Todas as fases anteriores (testa cada módulo implementado)

---

**📋 DESCRIÇÃO DA FASE:**

Esta fase implementa um sistema completo de testes automatizados que simula um utilizador real interagindo com a interface do sistema. O Playwright será usado para:

- **Simular ações humanas**: O rato move-se visualmente na tela, clica em botões, preenche formulários, navega entre páginas
- **Testes em qualquer ambiente**: Funciona tanto em produção quanto em staging
- **Interface DevTools**: Painel exclusivo para desenvolvedores executarem testes
- **Validação completa**: Cada ação é validada através de logs e verificações visuais
- **Relatórios dinâmicos**: Templates HTML que geram PDFs com resultados detalhados
- **Persistência de dados**: Todos os resultados guardados na base de dados
- **Testes granulares**: Testes individuais (criar, editar, apagar, pesquisar) e testes completos por módulo
- **Limpeza automática**: Dados de teste são criados e removidos automaticamente

**EXEMPLO DE FLUXO (Teste Criar Contacto):**
1. Playwright abre o browser e navega para /contacts/
2. Clica no botão "Novo Contacto" (movimento de rato visível)
3. Preenche formulário com dados únicos de teste (nome: "Test_Contact_20260208_143022")
4. Clica em "Guardar"
5. Verifica logs para confirmar sucesso (HTTP 200, redirect correto)
6. Volta à lista de contactos
7. Procura pelo nome único criado
8. Confirma que contacto aparece na lista
9. Clica no botão "Apagar"
10. Confirma eliminação
11. Verifica que contacto foi removido
12. Regista todos os passos e gera relatório PDF

---

## 18.1 Configuração Base e Infraestrutura de Testes

Criar estrutura base para testes automatizados com Playwright.

- [ ] **Instalar Playwright**
  - [ ] Adicionar playwright ao requirements.txt
  - [ ] Instalar browsers do Playwright
  - [ ] Configurar para modo headed (visível)

- [ ] **Criar app 'testing'**
  - [ ] Executar `python manage.py startapp testing apps/testing`
  - [ ] Adicionar 'apps.testing' ao INSTALLED_APPS
  - [ ] Criar estrutura de pastas: `apps/testing/playwright_tests/`

- [ ] **Modelo TestRun**
  - [ ] Campo: test_type (CREATE, UPDATE, DELETE, SEARCH, FULL)
  - [ ] Campo: module (CONTACTS, CRM, INVENTORY, etc.)
  - [ ] Campo: status (RUNNING, SUCCESS, FAILED, PARTIAL)
  - [ ] Campo: started_at, finished_at, duration
  - [ ] Campo: test_data (JSONField com dados usados)
  - [ ] Campo: steps_log (JSONField com log de cada passo)
  - [ ] Campo: screenshot_path (caminho para screenshots)
  - [ ] Campo: error_message (se falhar)
  - [ ] Campo: executed_by (FK User)

- [ ] **Modelo TestStep**
  - [ ] FK para TestRun
  - [ ] Campo: step_number (ordem)
  - [ ] Campo: action (NAVIGATE, CLICK, TYPE, VERIFY, etc.)
  - [ ] Campo: target (elemento ou URL)
  - [ ] Campo: expected_result
  - [ ] Campo: actual_result
  - [ ] Campo: status (SUCCESS, FAILED, SKIPPED)
  - [ ] Campo: screenshot (ImageField)
  - [ ] Campo: execution_time (duração do passo)

- [ ] **Modelo TestReportTemplate**
  - [ ] Campo: module (CONTACTS, CRM, etc.)
  - [ ] Campo: test_type (CREATE, FULL, etc.)
  - [ ] Campo: html_template (TextField com HTML do PDF)
  - [ ] Campo: css_styles (TextField com CSS)
  - [ ] Método render(test_run) - gera HTML final com dados

- [ ] **Configurações**
  - [ ] Criar settings para Playwright (headless=False, slowMo=500)
  - [ ] Configurar timeouts padrão
  - [ ] Configurar URLs base (staging vs production)

- [ ] **Migrations**
  - [ ] Executar makemigrations
  - [ ] Executar migrate

- [ ] **Testing - Models**
  - [ ] Test: criar TestRun funciona
  - [ ] Test: TestStep associa corretamente
  - [ ] Test: template renderiza HTML

---

## 18.2 Testes Automatizados - Módulo Contactos

Criar testes automatizados para todas as funcionalidades do módulo de contactos.

- [ ] **Script: test_contact_create.py**
  - [ ] Navegar para /contacts/
  - [ ] Clicar botão "Novo Contacto"
  - [ ] Preencher nome único (Test_Contact_[timestamp])
  - [ ] Preencher email, telefone, morada
  - [ ] Clicar "Guardar"
  - [ ] Verificar redirect para lista
  - [ ] Verificar mensagem de sucesso
  - [ ] Registar cada passo em TestStep

- [ ] **Script: test_contact_search.py**
  - [ ] Criar contacto de teste via API
  - [ ] Navegar para /contacts/
  - [ ] Preencher search box com nome do contacto
  - [ ] Verificar que contacto aparece
  - [ ] Verificar que outros não aparecem
  - [ ] Limpar search
  - [ ] Apagar contacto de teste

- [ ] **Script: test_contact_update.py**
  - [ ] Criar contacto de teste
  - [ ] Navegar para detalhe do contacto
  - [ ] Clicar "Editar"
  - [ ] Alterar nome, email, telefone
  - [ ] Guardar alterações
  - [ ] Verificar campos atualizados
  - [ ] Apagar contacto de teste

- [ ] **Script: test_contact_delete.py**
  - [ ] Criar contacto de teste
  - [ ] Navegar para lista
  - [ ] Procurar contacto
  - [ ] Clicar botão "Apagar"
  - [ ] Confirmar eliminação
  - [ ] Verificar que não aparece mais na lista

- [ ] **Script: test_contact_bulk_actions.py**
  - [ ] Criar 3 contactos de teste
  - [ ] Selecionar todos via checkboxes
  - [ ] Testar bulk archive
  - [ ] Verificar status archived
  - [ ] Testar bulk unarchive
  - [ ] Apagar contactos de teste

- [ ] **Script: test_contact_full.py**
  - [ ] Executar todos os testes acima em sequência
  - [ ] Gerar relatório consolidado

- [ ] **Template de Relatório**
  - [ ] Criar template HTML para relatórios de contactos
  - [ ] Incluir: título, data, duração, passos, screenshots, resultado

- [ ] **Interface DevTools**
  - [ ] Criar view TestContactView
  - [ ] Botões: "Teste Criar", "Teste Pesquisar", "Teste Editar", "Teste Apagar", "Teste Completo"
  - [ ] Mostrar status em tempo real (WebSocket ou polling)
  - [ ] Botão "Download PDF" após conclusão

- [ ] **Testing - Contact Tests**
  - [ ] Test: todos os scripts executam sem erros
  - [ ] Test: PDF é gerado corretamente

---

## 18.3 Testes Automatizados - Módulo CRM

Criar testes automatizados para gestão de leads e pipeline.

- [ ] **Script: test_lead_create.py**
  - [ ] Criar contacto de teste
  - [ ] Navegar para /crm/leads/
  - [ ] Clicar "Nova Lead"
  - [ ] Preencher campos (contact, title, value, stage)
  - [ ] Guardar lead
  - [ ] Verificar aparece na listagem

- [ ] **Script: test_lead_kanban.py**
  - [ ] Criar lead de teste
  - [ ] Navegar para /crm/pipeline/
  - [ ] Verificar lead aparece na coluna correta
  - [ ] Simular drag & drop para nova coluna
  - [ ] Verificar stage foi atualizado

- [ ] **Script: test_lead_convert.py**
  - [ ] Criar lead de teste
  - [ ] Navegar para detalhe da lead
  - [ ] Clicar "Converter em Venda"
  - [ ] Verificar SaleOrder criada
  - [ ] Verificar lead marcada como WON

- [ ] **Script: test_lead_full.py**
  - [ ] Executar todos os testes CRM
  - [ ] Gerar relatório consolidado

- [ ] **Template de Relatório CRM**
  - [ ] Template HTML específico para testes CRM

- [ ] **Interface DevTools para CRM**
  - [ ] View com botões de teste CRM
  - [ ] Download de relatórios

---

## 18.4 Testes Automatizados - Módulo Inventário

Criar testes automatizados para produtos e stock.

- [ ] **Script: test_product_create.py**
  - [ ] Navegar para /inventory/products/
  - [ ] Criar produto com código único
  - [ ] Preencher nome, preço, categoria
  - [ ] Guardar e verificar

- [ ] **Script: test_stock_movement.py**
  - [ ] Criar produto de teste
  - [ ] Criar movimento de entrada
  - [ ] Verificar stock atualizado
  - [ ] Criar movimento de saída
  - [ ] Verificar stock decrementado

- [ ] **Script: test_product_search.py**
  - [ ] Criar produto de teste
  - [ ] Pesquisar por código
  - [ ] Pesquisar por nome
  - [ ] Verificar filtros funcionam

- [ ] **Script: test_inventory_full.py**
  - [ ] Teste completo inventário

- [ ] **Template de Relatório Inventário**

- [ ] **Interface DevTools Inventário**

---

## 18.5 Testes Automatizados - Módulo Compras

Criar testes automatizados para ordens de compra.

- [ ] **Script: test_purchase_create.py**
  - [ ] Criar fornecedor de teste
  - [ ] Criar produto de teste
  - [ ] Navegar para /purchases/
  - [ ] Criar ordem de compra
  - [ ] Adicionar linhas
  - [ ] Guardar e verificar

- [ ] **Script: test_purchase_receive.py**
  - [ ] Criar compra de teste
  - [ ] Marcar como recebida
  - [ ] Verificar stock atualizado

- [ ] **Script: test_purchase_full.py**
  - [ ] Teste completo compras

- [ ] **Template de Relatório Compras**

- [ ] **Interface DevTools Compras**

---

## 18.6 Testes Automatizados - Módulo Vendas

Criar testes automatizados para ordens de venda e orçamentos.

- [ ] **Script: test_sale_create.py**
  - [ ] Criar cliente de teste
  - [ ] Criar produtos de teste
  - [ ] Navegar para /sales/
  - [ ] Criar venda/orçamento
  - [ ] Adicionar linhas
  - [ ] Calcular totais
  - [ ] Guardar e verificar

- [ ] **Script: test_sale_workflow.py**
  - [ ] Criar orçamento
  - [ ] Converter para encomenda
  - [ ] Marcar como entregue
  - [ ] Verificar stock
  - [ ] Gerar fatura

- [ ] **Script: test_sale_full.py**
  - [ ] Teste completo vendas

- [ ] **Template de Relatório Vendas**

- [ ] **Interface DevTools Vendas**

---

## 18.7 Testes Automatizados - Módulo Financeiro

Criar testes automatizados para gestão financeira.

- [ ] **Script: test_invoice_create.py**
  - [ ] Criar fatura de teste
  - [ ] Verificar valores calculados
  - [ ] Marcar como paga
  - [ ] Verificar transação criada

- [ ] **Script: test_financial_report.py**
  - [ ] Criar dados de teste (vendas, compras)
  - [ ] Gerar relatório financeiro
  - [ ] Verificar cálculos de lucro

- [ ] **Script: test_financial_full.py**
  - [ ] Teste completo financeiro

- [ ] **Template de Relatório Financeiro**

- [ ] **Interface DevTools Financeiro**

---

## 18.8 Testes Automatizados - Módulo BOM

Criar testes automatizados para receitas e configurador.

- [ ] **Script: test_bom_create.py**
  - [ ] Criar produto finalizado
  - [ ] Criar ingredientes
  - [ ] Criar BOM com linhas
  - [ ] Verificar cálculo de custos

- [ ] **Script: test_bom_configurator.py**
  - [ ] Navegar para configurador
  - [ ] Selecionar produto
  - [ ] Customizar (massa, recheio, cobertura)
  - [ ] Verificar preço atualizado
  - [ ] Adicionar ao orçamento

- [ ] **Script: test_bom_full.py**
  - [ ] Teste completo BOM

- [ ] **Template de Relatório BOM**

- [ ] **Interface DevTools BOM**

---

## 18.9 Testes Automatizados - Módulo Documentos

Criar testes automatizados para geração de PDFs.

- [ ] **Script: test_pdf_quotation.py**
  - [ ] Criar venda de teste
  - [ ] Gerar PDF de orçamento
  - [ ] Verificar PDF criado
  - [ ] Verificar conteúdo correto

- [ ] **Script: test_pdf_invoice.py**
  - [ ] Criar fatura de teste
  - [ ] Gerar PDF de fatura
  - [ ] Verificar dados corretos

- [ ] **Script: test_documents_full.py**
  - [ ] Teste completo documentos

- [ ] **Template de Relatório Documentos**

- [ ] **Interface DevTools Documentos**

---

## 18.10 Testes Automatizados - Módulo Marketing

Criar testes automatizados para campanhas.

- [ ] **Script: test_campaign_create.py**
  - [ ] Criar campanha de teste
  - [ ] Selecionar destinatários
  - [ ] Configurar mensagem
  - [ ] Verificar criação

- [ ] **Script: test_campaign_send.py**
  - [ ] Criar campanha
  - [ ] Simular envio (modo teste)
  - [ ] Verificar logs

- [ ] **Script: test_marketing_full.py**
  - [ ] Teste completo marketing

- [ ] **Template de Relatório Marketing**

- [ ] **Interface DevTools Marketing**

---

## 18.11 Testes Automatizados - Módulo Relatórios

Criar testes automatizados para dashboard e relatórios.

- [ ] **Script: test_dashboard.py**
  - [ ] Navegar para dashboard
  - [ ] Verificar KPIs carregam
  - [ ] Verificar gráficos renderizam
  - [ ] Testar filtros de período

- [ ] **Script: test_reports_generation.py**
  - [ ] Gerar relatório de vendas
  - [ ] Gerar relatório de compras
  - [ ] Verificar exportação CSV

- [ ] **Script: test_reports_full.py**
  - [ ] Teste completo relatórios

- [ ] **Template de Relatório**

- [ ] **Interface DevTools Relatórios**

---

## 18.12 Testes Automatizados - Módulo Configurações

Criar testes automatizados para configurações do sistema.

- [ ] **Script: test_company_settings.py**
  - [ ] Navegar para configurações
  - [ ] Alterar info da empresa
  - [ ] Upload de logo
  - [ ] Verificar alterações guardadas

- [ ] **Script: test_system_settings.py**
  - [ ] Alterar parâmetros do sistema
  - [ ] Verificar aplicação imediata

- [ ] **Script: test_settings_full.py**
  - [ ] Teste completo configurações

- [ ] **Template de Relatório Configurações**

- [ ] **Interface DevTools Configurações**

---

## 18.13 Interface Principal DevTools e Relatórios Globais

Criar interface centralizada para executar todos os testes.

- [ ] **View DevToolsTestingView**
  - [ ] Página principal em /devtools/testing/
  - [ ] Cards para cada módulo
  - [ ] Botão "Executar Teste Completo" (todos os módulos)
  - [ ] Histórico de testes executados
  - [ ] Status em tempo real

- [ ] **Sistema de Filas**
  - [ ] Usar Celery para executar testes em background
  - [ ] Task para cada tipo de teste
  - [ ] Progress tracking

- [ ] **Relatório Global**
  - [ ] Template para relatório de todos os módulos
  - [ ] Sumário executivo (X de Y testes passaram)
  - [ ] Breakdown por módulo
  - [ ] Screenshots de falhas
  - [ ] Gráfico de sucesso/falha

- [ ] **Download de Relatórios**
  - [ ] Endpoint para download de PDF individual
  - [ ] Endpoint para download de ZIP com todos os PDFs
  - [ ] Histórico de relatórios (últimos 30 dias)

- [ ] **Permissões**
  - [ ] Apenas superusers/admins acedem DevTools
  - [ ] Decorator @admin_required

- [ ] **Limpeza Automática**
  - [ ] Celery task para limpar dados de teste antigos
  - [ ] Limpar screenshots com mais de 30 dias
  - [ ] Manter apenas últimos 100 TestRuns por módulo

- [ ] **Configuração de Ambientes**
  - [ ] Selector: Staging vs Production
  - [ ] URLs base diferentes
  - [ ] Credenciais diferentes

- [ ] **Testing - DevTools**
  - [ ] Test: interface carrega
  - [ ] Test: executar teste completo funciona
  - [ ] Test: PDF global gera corretamente
  - [ ] Test: limpeza automática funciona

---

**FIM DO CHECKLIST**

---

## 📝 NOTAS IMPORTANTES

1. **Virtual Environment:** Sempre usar venv, nunca Docker
2. **Templates:** Todos standalone (sem herança), exceto base do sistema interno
3. **Tailwind CSS:** Sempre via CDN no header, nunca via NPM
4. **Rotas:** Uma tarefa = uma rota com todas as features dessa tarefa
5. **Website:** HTML copiado exatamente de https://v0-fuet-magico.vercel.app/
6. **PostgreSQL:** Versão 17+
7. **Stock:** Apenas entrada/saída, sem rotas complexas
8. **Perdas:** Sempre deduzir do lucro mensal quando marcado como perda
9. **BOM (Fase 10):** Sistema completo de receitas multi-nível com cálculo automático de custos em cascata
10. **Custos:** Incluem componentes + mão-de-obra (tempo * custo/hora)
11. **Conversões:** Sistema robusto de unidades (KG, G, L, ML, UN, SLICE, etc.)
12. **Recálculo:** Botão global para recalcular todos os custos quando preços mudam
13. **Testes Automatizados (Fase 18):** Playwright com modo headed (visível), simula utilizador real, gera relatórios PDF dinâmicos, todos os dados guardados na BD

---

## 🎯 PRÓXIMOS PASSOS

1. Começar pela Fase 1 (Setup)
2. Seguir sequencialmente as fases
3. Marcar progresso no `fuet_magico/progress.md` a partir da linha 110
4. Não avançar para próxima fase sem completar a anterior
5. Testar cada tarefa antes de marcar como concluída
6. **ATENÇÃO:** Fase 10 (BOM) é complexa - seguir ordem exata das tarefas para garantir dependências
7. **ATENÇÃO:** Fase 18 (Testes Automatizados) deve ser executada APÓS implementar cada módulo - usa Playwright para validar toda a UI

---

**Última atualização:** 08/02/2026
**Total de Tarefas:** 155
**Status:** Pronto para desenvolvimento ✅


Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process; .\venv\Scripts\Activate.ps1; python manage.py runserver 0.0.0.0:8000

---

## 3.14 Command Palette (Navegação Rápida) ✅

Barra de comandos estilo Odoo/VS Code para navegar entre rotas sem usar o menu.

- [x] **Implementação base**
  - [x] Overlay full-screen com `z-[99999]` e backdrop blur
  - [x] Input de pesquisa com ícone de lupa dourado
  - [x] Rodapé com hints de teclado (↑↓ navegar, ↵ abrir, Esc fechar)

- [x] **Mapa de rotas com palavras-chave em PT**
  - [x] Dashboard (`dashboard`, `início`, `painel`, `home`)
  - [x] CRM Pipeline (`crm`, `pipeline`, `kanban`, `leads`, `funil`)
  - [x] CRM Lista, Nova Lead, Configuração (Etapas, Tags, Motivos de Perda)
  - [x] CRM Atividades, Tipos de Atividade, Cadeias de Atividade
  - [x] Contactos (`contactos`, `clientes`, `empresas`)
  - [x] Perfil / Definições (`perfil`, `smtp`, `password`)
  - [x] Rotas Admin apenas para ADMIN/superuser (Admin Django, DevTools Logs)

- [x] **Comportamento de abertura**
  - [x] Qualquer tecla printável (fora de inputs) → abre e começa a filtrar
  - [x] `Ctrl+K` → abre/fecha a qualquer momento (inclusive dentro de inputs)
  - [x] `Esc` ou clique no backdrop → fecha

- [x] **Navegação por teclado**
  - [x] `↑` / `↓` → mover entre resultados (scroll automático)
  - [x] `Enter` → ir para rota selecionada (ou primeiro resultado)
  - [x] Clique num item → ir para a rota

- [x] **Pesquisa e resultados**
  - [x] Scoring: label > keywords/category > words
  - [x] Agrupamento por categoria com cabeçalho
  - [x] Highlight do termo pesquisado em `<mark>` com cor dourada
  - [x] Breadcrumb em cinzento (`CRM / Configuração / Etapas`)
  - [x] URL da rota mostrada à direita de cada resultado
  - [x] Mensagem "Nenhum resultado para X" quando sem matches

- [ ] **Melhorias futuras**
  - [x] Adicionar rotas de Gestão de Utilizadores quando implementado (ver 3.15)
  - [ ] Suporte a ações rápidas (ex: "Nova Lead", "Novo Contacto") sem navegar
  - [ ] Histórico de pesquisas recentes (localStorage)
  - [ ] Shortcut hint visível na navbar (`Ctrl+K`)

---

## 3.15 Gestão de Utilizadores (ADMIN only) ✅

Módulo para ADMIN criar, editar, desativar e gerir utilizadores do sistema.
Acessível via `/accounts/users/` — **apenas para role ADMIN ou superuser**.

- [x] **Model / URLs**
  - [x] Adicionar rotas em `apps/accounts/urls.py`:E outra coisa que eu quero fazer falta tipo esperar aqui uma coisa é no front-end já não alteraste nada ainda, né? Ou seja, continua com não está atualizado esta nova parte de que tu acabaste de fazer agora, não é? Se não tiver, podes atualizar, ok, para funcionar bem.
    ```python
    path('users/', views.user_list_view, name='user_list'),
    path('users/new/', views.user_create_view, name='user_create'),
    path('users/<uuid:user_id>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<uuid:user_id>/toggle-active/', views.user_toggle_active, name='user_toggle_active'),
    path('users/<uuid:user_id>/send-reset/', views.user_send_reset_email, name='user_send_reset'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    ```

- [x] **Views (`apps/accounts/views.py`)**
  - [x] `user_list_view` — lista todos os utilizadores da(s) empresa(s) do admin
    - [x] Filtros: role, ativo/inativo, empresa
    - [x] Pesquisa por nome/email
  - [x] `user_create_view` — criar novo utilizador
    - [x] Campos: nome, email, username, password, role, empresa(s), avatar, telemóvel
  - [x] `user_edit_view` — editar utilizador
    - [x] Campos editáveis: nome, email, role, empresas, avatar
    - [x] ADMIN não pode editar o próprio role/is_active (protecção)
  - [x] `user_toggle_active` — ativar/desativar utilizador (soft disable, AJAX)
  - [x] `user_send_reset_email` — envia link de reset por email (token seguro, 3 dias, uso único)
  - [x] `password_reset_confirm` — página pública para definir nova password via token

- [x] **Decorators / Permissões**
  - [x] Proteger todas as views com `@admin_required`
  - [x] Superuser tem acesso total independentemente do role

- [x] **Forms (`apps/accounts/forms.py`)**
  - [x] `UserCreateForm` — ModelForm com todos os campos + password1/password2
  - [x] `UserEditForm` — ModelForm sem username/password + is_active
  - [x] `SetNewPasswordForm` — Form simples para reset de password (mínimo 8 chars)

- [x] **Templates**
  - [x] `templates/accounts/user_list.html` — tabela com avatar, nome, email, role, estado
  - [x] `templates/accounts/user_create.html` — form de criação
  - [x] `templates/accounts/user_edit.html` — form de edição + card de reset de password
  - [x] `templates/accounts/password_reset_confirm.html` — página pública standalone
  - [x] `templates/accounts/password_reset_invalid.html` — página de erro de token inválido
  - [x] Badge colorido por role: ADMIN (dourado), MANAGER (azul), EMPLOYEE (cinzento)

- [x] **Avatar Dropdown (`base.html`)**
  - [x] Secção "Administração" visível para ADMIN/superuser
  - [x] Links: Utilizadores ✅, Empresas (em breve), Grupos (em breve)

- [x] **Command Palette**
  - [x] Rotas de utilizadores adicionadas ao mapa em `base.html` (Utilizadores + Novo Utilizador)
  - [x] Apenas visível para ADMIN/superuser (filtrado por `isAdmin`)

- [ ] **Testing**
  - [ ] Não-admin redireciona para 403/dashboard
  - [ ] ADMIN cria utilizador → aparece na lista
  - [ ] Desativar utilizador → não consegue fazer login
  - [ ] Editar role → reflete imediatamente na navbar do utilizador
  - [ ] Reset email: token expira após 3 dias / uso único

---

## 3.16 Gestão de Empresas (ADMIN only) ✅

Módulo para ADMIN criar, editar e gerir empresas do sistema.
Acessível via `/accounts/companies/` — **apenas para role ADMIN**.

- [x] **Model / URLs**
  - [x] Rotas em `apps/accounts/urls.py`:
    ```python
    path('companies/', views.company_list_view, name='company_list'),
    path('companies/new/', views.company_create_view, name='company_create'),
    path('companies/<uuid:pk>/edit/', views.company_edit_view, name='company_edit'),
    path('companies/<uuid:pk>/users/add/', views.company_user_add_view, name='company_user_add'),
    path('companies/<uuid:pk>/users/<int:user_id>/remove/', views.company_user_remove_view, name='company_user_remove'),
    path('companies/<uuid:pk>/users/search/', views.company_users_search_api, name='company_users_search'),
    ```

- [x] **Views (`apps/accounts/views.py`)**
  - [x] `company_list_view` — tabela de empresas com logo, nome, NIF, nº utilizadores, moeda
    - [x] Pesquisa por nome/NIF
    - [x] Bulk delete com checkboxes
    - [x] Clique na linha → abre edição
  - [x] `company_create_view` — criar nova empresa
  - [x] `company_edit_view` — editar empresa existente (redireciona para o próprio registo após guardar)
  - [x] `company_user_add_view` — adicionar utilizador à empresa (AJAX POST)
  - [x] `company_user_remove_view` — remover utilizador da empresa (AJAX POST)
  - [x] `company_users_search_api` — pesquisa utilizadores não pertencentes à empresa (AJAX GET)

- [x] **Forms**
  - [x] `CompanyCreateForm` — ModelForm com todos os campos da empresa

- [x] **Templates**
  - [x] `templates/accounts/company_list.html` — tabela + navbar de ações + bulk delete
  - [x] `templates/accounts/company_create.html` — form criação (logo + morada esq., campos dir., tabs Notas/WhatsApp)
  - [x] `templates/accounts/company_edit.html` — form edição igual ao create + tab Utilizadores
    - [x] Logo pré-preenchida
    - [x] Campos pré-preenchidos com dados da empresa
    - [x] Tab "Utilizadores": tabela de utilizadores da empresa + adicionar/remover AJAX
    - [x] Dropdown de pesquisa sai para fora da tabela (fora do overflow-hidden)
    - [x] Tab "WhatsApp": credenciais WhatsApp Business API com modal de ajuda
    - [x] Tab "Notas": editor Quill rich-text

- [x] **UX / Detalhe**
  - [x] Campo website: `type="text"` + `autoHttps()` no blur (aceita `www.cubix.pt`)
  - [x] Logo: upload com preview e crop 1:1 via canvas
  - [x] JSON dos utilizadores via `json_script` (não quebra atributos HTML)
  - [x] Alpine `x-data` separado do `x-show` para evitar erro "Cannot read .after"
  - [x] Quill usa `getElementById('company-edit-form')` — não apanha o form de logout do base.html
  - [x] Guardar redireciona para o próprio registo (não para a lista)

- [x] **Navbar (base.html)**
  - [x] Link "Empresas" adicionado na secção Administração do avatar dropdown

- [ ] **Futuro: integrar currency e language**
  - [ ] `currency` gravado na empresa — actualmente sem impacto funcional
  - [ ] Quando existirem módulos financeiros (Fase 8/9): usar `company.currency` para formatar valores em facturas, orçamentos, inventário
  - [ ] Criar modelo `Currency` com ISO 4217 (código, símbolo, nome) e ligar FK em `Company` — necessário quando houver suporte multi-moeda
  - [x] Campo `language` **removido** do modelo `Company` — não faz sentido na empresa interna; idioma pertence aos contactos

- [ ] **Testing**
  - [ ] Não-admin redireciona para 403
  - [ ] Criar empresa → aparece na lista
  - [ ] Editar empresa → dados actualizados, fica no registo
  - [ ] Adicionar utilizador → aparece na tab Utilizadores
  - [ ] Remover utilizador → desaparece da tab
  - [ ] Pesquisa de utilizadores não mostra os que já pertencem à empresa