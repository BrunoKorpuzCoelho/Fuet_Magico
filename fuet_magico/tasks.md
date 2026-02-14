# 🎯 FUET MÁGICO - FULL STACK MANAGEMENT SYSTEM - DEVELOPMENT CHECKLIST

> **Stack:** Python 3.12+, Django 5.0+, Django ORM, PostgreSQL 17+, Redis, Celery, JavaScript Native, Tailwind CSS (via CDN)
> **Formato:** Checkboxes hierárquicos (Fase → Tarefa → Sub-tarefa)
> **Objetivo:** Sistema completo de gestão empresarial para Fuet Mágico - incluindo Vendas, Inventário, Compras, CRM, Financeiro, Marketing, Configurador de Produtos e Website Institucional. Desenvolvimento do zero - seguir todas as tasks = projeto funcionando ✅

---

## 📊 PROGRESSO GERAL

- **Fase 1:** 8/8 features (100%) - Setup Ambiente e Infraestrutura ✅ COMPLETA!
- **Fase 2:** 0/6 features (0%) - Frontend - Website Institucional (HTML Copy)
- **Fase 3:** 1/11 features (9%) - Backend - Estrutura Base Django
- **Fase 4:** 1/23 features (4%) - App: Contactos
- **Fase 5:** 0/7 features (0%) - App: CRM (Customer Relationship Management)
- **Fase 6:** 0/12 features (0%) - App: Inventário (Produtos e Stock)
- **Fase 7:** 0/10 features (0%) - App: Compras
- **Fase 8:** 0/12 features (0%) - App: Vendas
- **Fase 9:** 0/8 features (0%) - App: Financeiro
- **Fase 10:** 0/18 features (0%) - BOM (Bill of Materials) - Sistema de Receitas
- **Fase 11:** 0/8 features (0%) - Sistema de PDFs (Documentos)
- **Fase 12:** 0/6 features (0%) - App: Marketing e WhatsApp
- **Fase 13:** 0/6 features (0%) - Stock Management Avançado
- **Fase 14:** 0/6 features (0%) - PDF Scanning (Entrada de Compras)
- **Fase 15:** 0/6 features (0%) - App: Relatórios e Dashboard
- **Fase 16:** 0/8 features (0%) - App: Configurações e Parâmetros
- **Fase 17:** 0/6 features (0%) - Integração Final e Deployment
- **Fase 18:** 0/13 features (0%) - Testes Automatizados UI (Playwright)

**TOTAL:** 10/162 features (6.2%)

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

- [ ] **Configurar settings**
  - [ ] Adicionar EMAIL_BACKEND
  - [ ] Adicionar EMAIL_HOST, EMAIL_PORT
  - [ ] Adicionar EMAIL_HOST_USER, EMAIL_HOST_PASSWORD (via .env)
  - [ ] Adicionar DEFAULT_FROM_EMAIL

- [ ] **Criar templates de email**
  - [ ] Criar `templates/emails/base.html`
  - [ ] Criar template de teste

- [ ] **Criar helper function**
  - [ ] Criar `apps/core/utils.py`
  - [ ] Criar função `send_email_notification(to, subject, template, context)`

- [ ] **Testing - Email**
  - [ ] Test: enviar email de teste funciona
  - [ ] Test: template renderiza corretamente

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

- [ ] **Criar modelo ChatterMessage**
  - [ ] Criar em `apps/core/models.py`
  - [ ] Herdar de AbstractBaseModel
  - [ ] **GenericForeignKey (funciona com QUALQUER modelo - Lead, Contact, Sale, etc.):**
    ```python
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    ```
  - [ ] **Campos principais:**
    - [ ] author (ForeignKey CustomUser, on_delete=SET_NULL, nullable)
    - [ ] message_type (CharField, max_length=10, choices=[('EMAIL', 'Email'), ('NOTE', 'Nota Interna')])
    - [ ] subject (CharField, max_length=255, blank=True) - só para emails
    - [ ] body (TextField) - conteúdo da mensagem/nota
    - [ ] to_email (EmailField, blank=True, null=True) - destinatário
    - [ ] cc_emails (TextField, blank=True) - CC separados por vírgula
  - [ ] **Anexos:**
    - [ ] attachments (JSONField, default=list, blank=True)
      ```python
      # Exemplo:
      [
        {"filename": "fatura.pdf", "url": "/media/attachments/fatura.pdf"},
        {"filename": "foto.jpg", "url": "/media/attachments/foto.jpg"}
      ]
      ```
  - [ ] **Status:**
    - [ ] is_internal (BooleanField, default=False) - True = nota interna
    - [ ] sent_at (DateTimeField, null=True, blank=True) - quando enviado
  - [ ] **Meta:**
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
  - [ ] **Methods:**
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

- [ ] **Criar modelo ChatterActivity**
  - [ ] Criar em `apps/core/models.py`
  - [ ] Herdar de AbstractBaseModel
  - [ ] **GenericForeignKey:**
    ```python
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    ```
  - [ ] **Campos:**
    - [ ] user (ForeignKey CustomUser, on_delete=SET_NULL, null=True)
    - [ ] activity_type (CharField, max_length=20, choices=[...])
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
    - [ ] description (TextField) - texto legível: "mudou o estágio de New para Qualified"
    - [ ] details (JSONField, default=dict, blank=True)
      ```python
      # Exemplo:
      {
        "field": "stage",
        "old_value": "New",
        "new_value": "Qualified"
      }
      ```
  - [ ] **Meta:**
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
  - [ ] **Methods:**
    ```python
    def __str__(self):
        return f"{self.user} - {self.get_activity_type_display()} - {self.created_at}"
    ```

- [ ] **Criar migrations**
  - [ ] Executar `python manage.py makemigrations core`
  - [ ] Executar `python manage.py migrate`

- [ ] **Registrar no Admin**
  - [ ] ChatterMessageAdmin:
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
  - [ ] ChatterActivityAdmin:
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

- [ ] **Testing - Modelos**
  - [ ] Test: criar ChatterMessage EMAIL funciona
  - [ ] Test: criar ChatterMessage NOTE funciona
  - [ ] Test: GenericForeignKey funciona com Lead
  - [ ] Test: GenericForeignKey funciona com Contact
  - [ ] Test: criar ChatterActivity funciona
  - [ ] Test: attachments JSON guarda lista de ficheiros
  - [ ] Test: details JSON guarda mudanças de campos
  - [ ] Test: is_email e is_note properties funcionam

---

## 3.12.2 Template Tags Personalizados

Criar template tags para facilitar uso do chatter.

- [ ] **Criar pasta templatetags**
  - [ ] Criar `apps/core/templatetags/` (se não existir)
  - [ ] Criar `apps/core/templatetags/__init__.py` (vazio)

- [ ] **Criar chatter_tags.py**
  - [ ] Criar `apps/core/templatetags/chatter_tags.py`
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

- [ ] **Testing - Template Tags**
  - [ ] Test: content_type retorna string correta
  - [ ] Test: funciona com Lead → "crm.lead"
  - [ ] Test: funciona com Contact → "contacts.contact"
  - [ ] Test: funciona com Sale → "sales.saleorder"

---

## 3.12.3 ChatterMixin para Views (Auto-carregar dados)

Criar mixin Django para adicionar dados do chatter automaticamente nas DetailViews.

- [ ] **Criar ChatterMixin**
  - [ ] Criar em `apps/core/views.py`
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

- [ ] **Documentar uso**
  - [ ] Criar comentário explicativo no código
  - [ ] Exemplo de uso em docstring

- [ ] **Testing - ChatterMixin**
  - [ ] Test: mixin adiciona context['chatter_messages']
  - [ ] Test: mixin adiciona context['activities']
  - [ ] Test: mixin adiciona context['whatsapp_messages'] (vazio por agora)
  - [ ] Test: funciona com Lead
  - [ ] Test: funciona com Contact

---

## 3.12.4 Componente Chatter HTML (Template BASE - será substituído)

Criar template PLACEHOLDER que será substituído pelo teu design depois.

- [ ] **Criar template base**
  - [ ] Criar `templates/components/chatter.html`
  - [ ] **NOTA IMPORTANTE:** Este é um template BASE mínimo!
    - Será **SUBSTITUÍDO** quando tiveres o teu design pronto
    - Serve apenas para ter estrutura funcional desde já
    - Usa Alpine.js conforme tua stack

- [ ] **Estrutura mínima (PLACEHOLDER):**
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

- [ ] **Incluir Alpine.js no base.html** (se ainda não tiver)
  - [ ] Adicionar no `<head>` de `templates/base.html`:
    ```html
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    ```

- [ ] **Testing - Template**
  - [ ] Test: template renderiza sem erros
  - [ ] Test: tabs funcionam ao clicar
  - [ ] Test: toggle EMAIL/NOTE funciona
  - [ ] Test: Alpine.js x-data inicializa
  - [ ] Test: funções placeholder mostram alert

---

## 3.12.5 Views Placeholder (APIs REST)

Criar endpoints REST com lógica PLACEHOLDER (print apenas).

- [ ] **Criar view para mensagens/notas**
  - [ ] Criar em `apps/core/views.py`
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

- [ ] **Criar view para WhatsApp**
  - [ ] Criar em `apps/core/views.py`
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

- [ ] **Configurar rotas**
  - [ ] Adicionar em `config/urls.py`:
    ```python
    from apps.core.views import chatter_create_message, chatter_send_whatsapp
    
    urlpatterns = [
        # ... outras rotas
        
        # Chatter APIs (PLACEHOLDERS)
        path('api/chatter/message/', chatter_create_message, name='chatter_create_message'),
        path('api/chatter/whatsapp/', chatter_send_whatsapp, name='chatter_send_whatsapp'),
    ]
    ```

- [ ] **Testing - APIs**
  - [ ] Test: POST /api/chatter/message/ retorna success
  - [ ] Test: POST /api/chatter/whatsapp/ retorna success
  - [ ] Test: print aparece no console
  - [ ] Test: user não autenticado retorna 403

---

## 3.12.6 Documentação e Notas para o Futuro

Criar documentação para lembrar o que falta implementar.

- [ ] **Criar TODO.md**
  - [ ] Criar `docs/chatter_todo.md`
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
  - [ ] Criar design visual no CRM
  - [ ] Usar PROMPT do VS Code para componentizar
  - [ ] Substituir templates/components/chatter.html
  
  ### 2. Implementar Lógica de Emails (Tarefa 3.9)
  - [ ] Configurar SMTP
  - [ ] Implementar função real em chatter_create_message()
  - [ ] Criar ChatterMessage na BD
  - [ ] Enviar email via Django send_mail()
  - [ ] Criar ChatterActivity automaticamente
  
  ### 3. Implementar WhatsApp (Fase 12)
  - [ ] Setup Meta WhatsApp API
  - [ ] Criar modelo WhatsAppMessage
  - [ ] Implementar função real em chatter_send_whatsapp()
  - [ ] Webhook para receber mensagens
  - [ ] Processar mensagens via Celery
  
  ### 4. Auto-logging de Atividades (Signals)
  - [ ] Criar signals para detetar mudanças
  - [ ] Criar ChatterActivity automaticamente
  - [ ] Middleware para capturar user atual
  
  ### 5. Anexos
  - [ ] Upload de ficheiros
  - [ ] Guardar em media/
  - [ ] Adicionar URL ao attachments JSON
  ```

- [ ] **Adicionar comentários no código**
  - [ ] Comentar funções placeholder com TODO
  - [ ] Explicar que será implementado depois

- [ ] **Testing - Documentação**
  - [ ] Test: TODO.md existe e está completo
  - [ ] Test: comentários TODO estão no código

---

## 3.12.7 Testing Completo

Testar tudo o que foi implementado.

- [ ] **Testes de Modelos**
  - [ ] Test: criar ChatterMessage tipo EMAIL
  - [ ] Test: criar ChatterMessage tipo NOTE
  - [ ] Test: GenericForeignKey funciona com Lead
  - [ ] Test: GenericForeignKey funciona com Contact
  - [ ] Test: criar ChatterActivity
  - [ ] Test: attachments JSON funciona
  - [ ] Test: visualizar no Admin

- [ ] **Testes de Template Tags**
  - [ ] Test: {{ object|content_type }} retorna string correta

- [ ] **Testes de ChatterMixin**
  - [ ] Test: incluir mixin em view adiciona context
  - [ ] Test: context['chatter_messages'] existe
  - [ ] Test: context['activities'] existe

- [ ] **Testes de Template**
  - [ ] Test: incluir chatter.html funciona
  - [ ] Test: tabs renderizam
  - [ ] Test: Alpine.js inicializa
  - [ ] Test: clicar em tabs troca conteúdo

- [ ] **Testes de APIs**
  - [ ] Test: chamar /api/chatter/message/ mostra print
  - [ ] Test: chamar /api/chatter/whatsapp/ mostra print
  - [ ] Test: alert aparece ao usar funções

- [ ] **Teste de Integração**
  - [ ] Test: criar Lead → abrir detalhe → chatter aparece
  - [ ] Test: incluir ChatterMixin em LeadDetailView
  - [ ] Test: template funciona sem erros


## 3.12.8 Sistema de Menções (@username) em Notas

Permitir mencionar outros utilizadores em notas e criar notificações automáticas.

- [ ] **Atualizar modelo ChatterMessage**
  - [ ] Adicionar campo `mentioned_users` em `apps/core/models.py`:
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
  - [ ] Criar migration:
    ```bash
    python manage.py makemigrations core
    python manage.py migrate
    ```

- [ ] **Criar helper function para parse de menções**
  - [ ] Criar `apps/core/utils.py` (se não existir)
  - [ ] Função `extract_mentions(text)`:
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

- [ ] **Atualizar view chatter_create_message**
  - [ ] Modificar `apps/core/views.py`:
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

- [ ] **Testing - Menções**
  - [ ] Test: criar nota com @joao cria menção
  - [ ] Test: mentioned_users contém user correto
  - [ ] Test: notificação é criada para mencionado
  - [ ] Test: não cria notificação para autor

---

## 3.12.9 Modelo de Notificações

Criar modelo para notificações internas do sistema.

- [ ] **Criar modelo Notification**
  - [ ] Criar em `apps/core/models.py`:
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

- [ ] **Criar migrations**
  - [ ] `python manage.py makemigrations core`
  - [ ] `python manage.py migrate`

- [ ] **Registrar no Admin**
  - [ ] Criar NotificationAdmin:
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

- [ ] **Testing - Notification Model**
  - [ ] Test: criar notificação funciona
  - [ ] Test: mark_as_read() atualiza is_read e read_at
  - [ ] Test: GenericForeignKey funciona
  - [ ] Test: ordenação por -created_at

---

## 3.12.10 API de Notificações

Criar endpoints REST para obter e marcar notificações.

- [ ] **Criar view para listar notificações**
  - [ ] Criar em `apps/core/views.py`:
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

- [ ] **Criar view para marcar como lido**
  - [ ] Criar em `apps/core/views.py`:
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

- [ ] **Criar view para marcar TODAS como lidas**
  - [ ] Criar em `apps/core/views.py`:
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

- [ ] **Configurar rotas**
  - [ ] Adicionar em `config/urls.py`:
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

- [ ] **Testing - APIs**
  - [ ] Test: GET /api/notifications/ retorna lista
  - [ ] Test: unread_count está correto
  - [ ] Test: POST mark-read funciona
  - [ ] Test: POST mark-all-read funciona

---

## 3.12.11 Badge de Notificações no Navbar

Atualizar navbar para mostrar contador de notificações não lidas.

- [ ] **Atualizar base.html (navbar)**
  - [ ] Modificar `templates/base.html`:
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

- [ ] **Testing - Badge**
  - [ ] Test: badge mostra contador correto
  - [ ] Test: clicar abre dropdown
  - [ ] Test: clicar em notificação marca como lida
  - [ ] Test: "Marcar todas" funciona
  - [ ] Test: polling atualiza a cada 30s

---

## 3.12.12 Autocomplete de Menções (@) no Chatter

Criar dropdown de autocomplete quando digitar @ no textarea.

- [ ] **Criar API para buscar users**
  - [ ] Criar em `apps/core/views.py`:
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

- [ ] **Configurar rota**
  - [ ] Adicionar em `config/urls.py`:
    ```python
    path('api/users/search/', users_search_api, name='users_search'),
    ```

- [ ] **Adicionar JavaScript autocomplete no chatter**
  - [ ] Atualizar `templates/components/chatter.html`:
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

- [ ] **Testing - Autocomplete**
  - [ ] Test: digitar @ abre dropdown
  - [ ] Test: digitar @joa filtra users
  - [ ] Test: clicar em user insere @username
  - [ ] Test: API retorna users corretos

---

## 3.12.13 Testing Completo (Menções + Notificações)

Testar todo o sistema de menções e notificações.

- [ ] **Testes de Menções**
  - [ ] Test: criar nota com @joao
  - [ ] Test: mentioned_users contém user correto
  - [ ] Test: parse extrai múltiplos @mentions
  - [ ] Test: autocomplete funciona

- [ ] **Testes de Notificações**
  - [ ] Test: notificação criada quando mencionado
  - [ ] Test: badge mostra contador correto
  - [ ] Test: clicar marca como lida
  - [ ] Test: "Marcar todas" funciona
  - [ ] Test: não cria notificação para autor

- [ ] **Teste de Integração**
  - [ ] Test: João menciona Maria em nota
  - [ ] Test: Maria recebe notificação
  - [ ] Test: Badge de Maria atualiza
  - [ ] Test: Maria clica e vê notificação
  - [ ] Test: Maria marca como lida
  - [ ] Test: Badge decrementa

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

## 5.1 Criação da App 'crm'

Criar app Django para gestão de CRM.

- [x] **Criar app**
  - [x] Executar `python manage.py startapp crm apps/crm`
  - [x] Adicionar 'apps.crm' ao INSTALLED_APPS

- [x] **Criar estrutura de arquivos**
  - [x] Criar `apps/crm/models.py`
  - [x] Criar `apps/crm/views.py`
  - [x] Criar `apps/crm/forms.py`
  - [x] Criar `apps/crm/urls.py`

---

## 5.2 Modelo CRMStage (Estágios do Pipeline)

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
  - [ ] CRMStageCreateView
  - [ ] CRMStageUpdateView
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

## 5.3 Modelo Lead

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
  - [ ] Filtrar por owner_company na LeadListView usando filter_by_company()
  - [ ] Auto-preencher owner_company na create view com get_active_company()

- [x] **Validações e constraints**
  - [x] Validar: estimated_value >= 0
  - [x] Validar: probability entre 0-100
  - [x] Validar: lost_reason obrigatório se stage=LOST
  - [ ] Auto-definir probability baseado no stage (NEW=10%, QUALIFIED=25%, PROPOSAL=50%, NEGOTIATION=75%)

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

## 5.4 Modelo Activity (Atividades/Tarefas)

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

- [ ] **CRUD Views para Activity**
  - [ ] ActivityCreateView (modal dentro de lead_detail)
  - [ ] ActivityUpdateView (modal)
  - [ ] ActivityMarkDoneView (abre modal para pedir feedback)
  - [ ] Templates: `templates/crm/activity_form_modal.html`, `activity_done_modal.html`
  - [ ] Rotas: `/crm/activities/create/`, `/crm/activities/<pk>/done/`, etc.

- [ ] **Timeline de Activities dentro de Lead**
  - [ ] Adicionar seção "Activities" no lead_detail.html
  - [ ] Mostrar activities ordenadas por due_date
  - [ ] Ícones diferentes por activity_type (📧 email, 📞 call, ✅ todo, 💬 whatsapp)
  - [ ] Cores baseadas em status (verde/amarelo/vermelho)
  - [ ] Botão "Schedule Activity" abre modal
  - [ ] Checkbox para marcar como done (abre modal de feedback)

- [x] **Testing - Activity Model**
  - [x] Test: criar activity funciona
  - [x] Test: is_overdue funciona corretamente
  - [x] Test: status_color retorna cor correta
  - [x] Test: feedback obrigatório ao marcar done
  - [x] Test: done_date auto-preenchido

---

## 5.5 Views de Listagem de Leads

Criar view para listar leads com filtros por estágio, responsável e período.

- [ ] **Criar LeadListView**
  - [ ] Implementar paginação (50 por página)
  - [ ] Implementar busca por title/contact/description
  - [ ] Implementar filtro por stage (NEW, QUALIFIED, PROPOSAL, etc.)
  - [ ] Implementar filtro por assigned_to (ver só as minhas vs todas)
  - [ ] Implementar filtro por período (created_at range)
  - [ ] Ordenação por estimated_value, probability, expected_close_date

- [ ] **Criar template**
  - [ ] Criar `templates/crm/lead_list.html`
  - [ ] Tabela com: checkbox, title, contact, stage badge, value, probability bar, assigned_to, actions
  - [ ] Filtros sidebar: Stage, Responsável, Período
  - [ ] Botão "Nova Lead"
  - [ ] Sistema de seleção múltipla com checkboxes
  - [ ] Bulk actions: Mudar Stage, Atribuir Responsável, Arquivar
  - [ ] Cards com KPIs: Total Leads, Valor Total Pipeline, Taxa de Conversão, Leads Este Mês

- [ ] **Configurar rota**
  - [ ] `path('crm/leads/', LeadListView, name='lead_list')`
  - [ ] Incluir urls no config/urls.py

- [ ] **Testing - Lead List**
  - [ ] Test: lista mostra leads do user
  - [ ] Test: filtros funcionam
  - [ ] Test: busca funciona
  - [ ] Test: KPIs calculam corretamente

---

## 5.6 Views de Criação de Lead

Criar formulário para criar nova lead.

- [ ] **Criar LeadForm**
  - [ ] Campos: contact (select com autocomplete), title, description, estimated_value, stage, source, expected_close_date, assigned_to
  - [ ] Validação: contact obrigatório
  - [ ] Validação: estimated_value >= 0
  - [ ] Option: criar novo contact inline (modal)

- [ ] **Criar LeadCreateView**
  - [ ] Form com todos os campos
  - [ ] Auto-preencher assigned_to com user atual
  - [ ] Auto-preencher stage com NEW
  - [ ] Redirect para lead_detail após criar

- [ ] **Criar template**
  - [ ] Criar `templates/crm/lead_create.html`
  - [ ] Form layout com Tailwind
  - [ ] Botão "Guardar" e "Guardar e Criar Novo"
  - [ ] Botão "Cancelar" (volta para lista)
  - [ ] Select de contact com search (Alpine.js)

- [ ] **Configurar rota**
  - [ ] `path('crm/leads/create/', LeadCreateView, name='lead_create')`

- [ ] **Testing - Lead Create**
  - [ ] Test: criar lead funciona
  - [ ] Test: validações funcionam
  - [ ] Test: assigned_to default = user atual

---

## 5.7 Views de Edição e Detalhes

Criar views para editar e visualizar detalhes de lead.

- [ ] **Criar LeadDetailView**
  - [ ] Mostrar todos os campos da lead
  - [ ] Mostrar histórico de mudanças (via AuditLog)
  - [ ] **Seção Activities/Chatter** (estilo Odoo):
    - [ ] Botão "Schedule Activity" (abre modal ActivityCreateView)
    - [ ] Timeline vertical com todas as activities ordenadas por due_date
    - [ ] Cada activity mostra:
      - [ ] Ícone por tipo (📧 EMAIL, 📞 CALL, ✅ TODO, 💬 WHATSAPP, 📄 DOCUMENT, ✍️ SIGNATURE)
      - [ ] Summary (título da activity)
      - [ ] Due date formatada (ex: "Feb 16" ou "Today" ou "Yesterday")
      - [ ] Cor do border baseada em status (verde/amarelo/vermelho)
      - [ ] Avatar do assigned_to
      - [ ] Botões: "Mark Done" (abre modal feedback) | "Edit"
    - [ ] Se activity is_done=True, mostrar com opacidade reduzida e ícone ✅
    - [ ] Feedback da activity (se done) em texto cinza abaixo do summary
  - [ ] Smart buttons: Vendas Geradas (se convertida), Documentos, Atividades Pendentes
  - [ ] Timeline de eventos (AuditLog)

- [ ] **Criar LeadUpdateView**
  - [ ] Form igual ao create
  - [ ] Permitir mudar stage (dropdown com stages do CRMStage)
  - [ ] Se mudar para stage com is_won_stage=True, sugerir criar venda
  - [ ] Se mudar para LOST, campo lost_reason obrigatório (modal)

- [ ] **Criar templates**
  - [ ] `templates/crm/lead_detail.html` (view mode)
    - [ ] Layout 2 colunas: Info principal (esquerda) + Activities/Chatter (direita)
  - [ ] `templates/crm/lead_edit.html` (edit mode)
  - [ ] `templates/crm/components/activity_timeline.html` (component reutilizável)
  - [ ] Layout com tabs: Geral, Histórico, Atividades (mobile)

- [ ] **Configurar rotas**
  - [ ] `path('crm/leads/<uuid:pk>/', LeadDetailView, name='lead_detail')`
  - [ ] `path('crm/leads/<uuid:pk>/edit/', LeadUpdateView, name='lead_edit')`

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

**⏳ PENDENTE:**
- ⏳ Modal lost_reason para stage "Lost" (drag para Lost pede motivo)
- ⏳ Botão "+" funcional para criar lead no stage
- ⏳ Lead detail view (click no card)
- ⏳ Filtros avançados (assigned_to, priority, date range, tags, source)
- ⏳ Progress bar dividida em 3 cores (verde/amarelo/vermelho) no header
- ⏳ Activity icons baseados em activities reais do banco
- ⏳ Sistema de tags customizáveis (JSONField)
- ⏳ Lead list view alternativa (`/crm/sales/`)
- ⏳ Mobile responsive otimizado (accordion/tabs)
- ⏳ Testes automatizados
- ⏳ Empty state nas colunas vazias
- ⏳ Prioridade stars corrigida (HIGH=3, MEDIUM=2, LOW=1)
- ⏳ Animação visual de sucesso ao arrastar

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
  - [x] Botão "+" no canto superior direito (existe, mas ainda não funcional - links to #)

- [x] **Container de Cards**
  - [x] Área scrollável verticalmente com altura dinâmica via JS
  - [x] Padding: px-1
  - [x] Background: bg-gray-800 dark:bg-gray-800
  - [x] Cards empilhados com gap space-y-2
  - [ ] Empty state: "Nenhuma oportunidade neste estágio" - TODO

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
  - [ ] **TODO FUTURO:** Implementar barra dividida em 3 cores com tooltips no header (opcional)

**Alternativa opcional (comentar no código):**
Progress bar baseada em `probability` média do stage (mais simples, menos específico):
- [ ] Calcular avg_probability do stage
- [ ] Barra única com fill de avg_probability% (cor do stage)

### 5.9.3 Lead Cards (Design Odoo-like)

- [x] **Layout do Card (Design compacto)**
  - [x] Container: bg-gray-800 dark:bg-gray-800, rounded-lg, shadow-sm, p-3
  - [x] Border com cores baseadas em routing (amarelo/vermelho para warning/overdue)
  - [x] Hover: border-gray-600, cursor-pointer
  - [ ] Click: abre lead_detail_view (modal ou página) - TODO

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

- [x] **Linha 5: Tags (Source Badge)**
  - [x] Badge de source renderizado com cores diferentes:
    - [x] WEBSITE: blue, REFERRAL: green, SOCIAL_MEDIA: purple, etc.
  - [x] Formato: px-2, py-0.5, rounded-full, text-xs
  - [ ] **TODO:** Implementar sistema de tags customizáveis (JSONField)

- [x] **Linha 6: Activity Icons**
  - [x] Ícone de telefone (phone) exibido estaticamente
  - [ ] **TODO:** Buscar activities reais do banco e renderizar dinamicamente
  - [ ] **TODO:** Cores baseadas em status (done/overdue/pending)

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
  - [ ] Modal lost_reason para stage "Lost" (quando drag para Lost)
  - [ ] Animação visual de sucesso/erro no drag

### 5.9.5 Totais e KPIs por Coluna

- [x] **Calcular totais no backend (LeadPipelineView):**
  - [x] Total value (soma de estimated_value) calculado
  - [x] Count de leads calculado
  - [x] Routing calculations (is_overdue, is_warning) implementado nos cards
  - [x] Dados passados no context como `pipeline_data`
  - [ ] **TODO:** Calcular avg_probability (não usado atualmente)
  - [ ] **TODO:** Calcular verde/amarelo/vermelho aggregated para progress bar dividida

- [x] **Renderizar no header:**
  - [x] Contador: badge com `(count)` mostrado na collapsed view
  - [x] Total: `{{ total_value|short_value }}` com formatação K/M/B
  - [x] Progress bar: barra simples colorida (não dividida em 3 seções)
  - [ ] **TODO:** Progress bar dividida em 3 cores proporcionais (verde/amarelo/vermelho)
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

- [ ] **Renderizar no header:**
  - [ ] Contador: badge pequeno `({{ count }})`
  - [ ] Total: `R$ {{ total_value|floatformat:2 }}`
  - [ ] Progress bar: 3 seções com widths proporcionais

### 5.9.6 Filtros e Search (Barra Superior)

- [x] **Barra de Filtros no Topo do Pipeline**
  - [x] Search bar implementada (idêntica ao app contacts)
  - [x] Layout com botão "Novo" (links to # - TODO)
  - [x] View toggle (Kanban/List) implementado (List links to # - TODO)
  - [ ] Logo "Pipeline" + badge total - não implementado
  - [ ] Linha de filtros inline - não implementada

- [x] **Filtros implementados:**
  - [x] **Search bar**: busca por `lead.title` (field selector com dropdown)
  - [ ] Outros campos de busca: contact, source, assigned_to, priority, description - TODO
  - [ ] **Dropdown "Assigned to"** - não implementado
  - [ ] **Dropdown "Priority"** - não implementado
  - [ ] **Date Range Picker** - não implementado
  - [ ] **Dropdown "Tags"** - não implementado
  - [ ] **Dropdown "Source"** - não implementado

- [ ] **Implementação de Filtros:** - não implementado (apenas search básica)
- [ ] **Botão "Clear Filters"** - não implementado

### 5.9.7 Mobile Responsive

**STATUS: NÃO IMPLEMENTADO - Layout atual responsivo básico com Tailwind, mas não otimizado para mobile**

- [x] **Desktop (>1024px):** Colunas lado a lado com scroll horizontal - FUNCIONA
  - [x] Smooth scroll funciona naturalmente
  - [ ] TODO: Ajustar para garantir 4 colunas visíveis

- [ ] **Tablet (768-1024px):** 2-3 colunas visíveis - não testado/otimizado
- [ ] **Mobile (<768px):** Layout vertical ou tabs - não implementado
  - [ ] **Opção 1 - Accordion:**
    - [ ] Cada stage é um collapsible panel
    - [ ] Click no header expande a coluna, mostra cards
    - [ ] Só 1 coluna expandida por vez
  - [ ] **Opção 2 - Tabs horizontais:**
    - [ ] Tabs com nome dos stages no topo
    - [ ] Swipe entre tabs (mobile-friendly)
    - [ ] Cada tab mostra cards daquele stage
  - [ ] **Drag & drop desabilitado no mobile** (difícil de usar)
    - [ ] Substituir por botão "Mover para..." dentro do card
    - [ ] Abre dropdown com lista de stages
    - [ ] Selecionar novo stage → chama mesmo endpoint change-stage

### 5.9.8 Navegação e URLs

- [x] **Atualizar crm_navbar.html:**
  - [x] Link "CRM" → `/crm/` (pipeline view, DEFAULT) - **Destacado como ativo**
  - [ ] Link "Sales" → `/crm/sales/` (lista tabular de leads) - **Links to # atualmente**
  - [ ] Link "Reporting" → `/crm/reporting/` (dashboards) - **Desabilitado**
  - [x] Dropdown "Configuração" → Etapas, Categorias, etc. - **Implementado**

- [ ] **Criar Lead List View alternativa (task 5.5):**
  - [ ] URL: `/crm/sales/` (lista tradicional tabular) - **TODO**
  - [ ] Para users que preferem tabelas
  - [ ] Botão "Ver Pipeline" switch para `/crm/`

### 5.9.9 Templates Necessários

- [x] **templates/crm/lead_pipeline.html**: Layout principal do Kanban - **CRIADO**
  - [x] Loop por `pipeline_data`
  - [x] Renderiza colunas com headers colapsáveis (Alpine.js)
  - [x] Renderiza cards com todos os campos principais
  - [x] Search bar idêntica ao app contacts
  - [x] CSS inline para layout flex, scroll, altura dinâmica
  - [x] JS para calcular altura do pipeline dinamicamente
  - [x] SortableJS CDN carregado (não wired ainda)

- [ ] **templates/crm/components/lead_card.html**: Card individual (partial) - **NÃO CRIADO**
  - [ ] TODO: Extrair card para component reusável
  - [ ] Renderizar colunas com headers coloridos
  - [ ] Incluir `lead_card.html` para cada lead
  - [ ] Script Sortable.js para drag & drop

- [ ] **templates/crm/partials/lead_card.html**: Card individual (include)
- [ ] **templates/crm/components/lead_card.html**: Card individual (partial) - **NÃO CRIADO**
  - [ ] TODO: Extrair card para component reusável
  - [ ] Recebe context: `lead` object
  - [ ] Renderiza: title, value, contact, priority stars, tags, activity icons, assigned_to
  - [ ] Data attributes: `data-lead-id="{{ lead.id }}"` (para Sortable.js)

- [ ] **templates/crm/lost_reason_modal.html**: Modal para lost_reason - **NÃO CRIADO**
  - [ ] Form com textarea
  - [ ] Botões: Cancelar, Confirmar
  - [ ] Alpine.js para controlar visibilidade

- [ ] **templates/crm/pipeline_filters.html**: Barra de filtros (include) - **NÃO CRIADO**
  - [ ] Opcional: modularizar filtros em partial

### 5.9.10 Testing - Pipeline View

**STATUS: TESTES NÃO IMPLEMENTADOS - View funcional criada mas sem cobertura de testes**

- [ ] **Test: pipeline view carrega todas as colunas dinamicamente**
  - Criar 5 stages, verificar 5 colunas renderizadas
  - Verificar ordem por sequence

- [ ] **Test: totais calculados corretamente**
  - Criar 3 leads no stage "New": R$ 1.000, R$ 2.000, R$ 3.000
  - Verificar header mostra "R$ 6.000,00"

- [ ] **Test: progress bar renderiza cores baseado em routing**
  - Stage com routing_in_days=7
  - Lead A: 3 dias no stage (verde)
  - Lead B: 7 dias no stage (amarelo)
  - Lead C: 10 dias no stage (vermelho)
  - Verificar progress bar: 33% verde, 33% amarelo, 33% vermelho

- [ ] **Test: drag-and-drop atualiza stage da lead**
  - Simular drag de lead do stage "New" para "Qualified"
  - Verificar lead.stage mudou
  - Verificar lead.stage_updated_at atualizado
  - Verificar lead.probability auto-atualizada

- [ ] **Test: modal lost_reason aparece ao drag para Lost**
  - Drag card para stage "Lost"
  - Verificar modal aparece
  - Verificar lost_reason obrigatório
  - Simular cancelamento: card volta para coluna original

- [ ] **Test: priority stars renderizam corretamente**
  - Lead LOW: 1 estrela preenchida, 2 vazias
  - Lead MEDIUM: 2 estrelas preenchidas, 1 vazia
  - Lead HIGH: 3 estrelas preenchidas

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

- [ ] **Test: mobile responsive mostra accordion ou tabs**
  - Viewport <768px
  - Verificar colunas viram accordion/tabs
  - Verificar drag & drop desabilitado

- [ ] **Test: fold_by_default colapsa colunas**
  - Stage com fold_by_default=True
  - Verificar coluna aparece colapsada (só header)
  - Click no botão "Expand" → mostra cards

- [ ] **Test: botão "+" no header cria lead direto no stage**
  - Click no "+" do stage "Qualified"
  - Verificar form abre com stage pré-selecionado

---

## 5.10 Generate Leads (Geração Automática Baseada em Histórico)

Criar funcionalidade para gerar leads automaticamente baseado em dados históricos (ex: aniversários do ano passado).

**CONTEXTO:** 
- No Odoo, há uma feature "Generate Leads" no pipeline
- Exemplo: se em Fevereiro 2025 houve 30 bolos de aniversário, o sistema pode sugerir leads para Fevereiro 2026 para os mesmos clientes
- Ideia: automatizar follow-up de vendas recorrentes (aniversários, eventos sazonais, etc.)

- [ ] **Criar LeadGenerateView**
  - [ ] Botão "Generate Leads" no topo do pipeline (lead_kanban.html)
  - [ ] Modal com opções:
    - [ ] Período histórico: "Mesmo mês do ano passado" (default), "Últimos X meses", "Custom range"
    - [ ] Filtro de produtos: apenas produtos com categoria "Aniversário" ou tag específica
    - [ ] Filtro de clientes: apenas clientes com vendas no período histórico
    - [ ] Preview: "Encontrados X clientes com Y vendas no período selecionado"
  - [ ] Botão "Gerar Leads" executa a lógica

- [ ] **Lógica de Geração**
  - [ ] Buscar vendas (SaleOrder) no período histórico selecionado
  - [ ] Agrupar por contact (cliente)
  - [ ] Para cada contact:
    - [ ] Criar Lead com:
      - [ ] title = "Follow-up: Aniversário {ano_atual}" (ou template customizável)
      - [ ] contact = contact da venda histórica
      - [ ] estimated_value = média/soma das vendas anteriores
      - [ ] stage = primeiro CRMStage (NEW)
      - [ ] source = "GENERATED"
      - [ ] assigned_to = mesmo responsável da última venda (ou user atual)
      - [ ] tags = ['generated', 'birthday'] (ou baseado em filtros)
    - [ ] Criar Activity automática:
      - [ ] activity_type = EMAIL ou WHATSAPP (configurável)
      - [ ] summary = "Contactar cliente para promoção aniversário"
      - [ ] due_date = hoje + X dias (configurável, ex: 7 dias)
      - [ ] assigned_to = responsável da lead
  - [ ] Evitar duplicados: não criar lead se já existe lead ativa para o mesmo contact no mesmo período

- [ ] **Template Modal**
  - [ ] `templates/crm/generate_leads_modal.html`
  - [ ] Form com:
    - [ ] Select período histórico (dropdown)
    - [ ] Date pickers para custom range
    - [ ] Checkboxes para filtros (produtos, categorias)
    - [ ] Preview dinâmico (AJAX) mostrando quantos leads serão geradas
  - [ ] Botão "Gerar X Leads" (X = contagem do preview)
  - [ ] Botão "Cancelar"

- [ ] **Endpoint AJAX**
  - [ ] GET `crm/leads/generate/preview/` (recebe filtros, retorna contagem)
  - [ ] POST `crm/leads/generate/` (executa geração, retorna leads criadas)
  - [ ] Response JSON: {success: true, leads_created: 15, message: "15 leads geradas com sucesso"}

- [ ] **Configurar rotas**
  - [ ] `path('crm/leads/generate/preview/', LeadGeneratePreviewView, name='lead_generate_preview')`
  - [ ] `path('crm/leads/generate/', LeadGenerateView, name='lead_generate')`

- [ ] **Notificação e Feedback**
  - [ ] Após geração, mostrar toast: "✅ X leads geradas com sucesso"
  - [ ] Redirecionar para pipeline com filtro "source=GENERATED"
  - [ ] Enviar notificação para users atribuídos (opcional)

- [ ] **Testing - Generate Leads**
  - [ ] Test: preview conta vendas históricas corretamente
  - [ ] Test: geração cria leads com dados corretos
  - [ ] Test: não cria duplicados para mesmo contact
  - [ ] Test: cria activities automáticas
  - [ ] Test: filtros de período funcionam
  - [ ] Test: assigned_to herda da última venda


Task 5.9 PRIMEIRO - Pipeline/Kanban (a view principal que tu queres!)

Colunas por stage (New, Qualified, Proposition, Won)
Drag & drop para mover leads entre stages
Cards com info básica (title, valor, contacto)
Botão "+" em cada coluna para criar lead naquele stage
Task 5.6 - LeadCreateView (modal simples para criar lead do pipeline)

Task 5.7 - LeadDetailView (modal/sidebar ao clicar no card)

Task 5.5 - LeadListView (view alternativa, não default)

Task 5.8 - LeadUpdateView (editar lead)

no final ver o que falta e im-plementar
---

## 4.16 Template Base de Smart Buttons (Relações Modulares)

Criar template base reutilizável para vistas de smart buttons que mostram relações entre módulos (ex: CRM, Vendas, Compras, Faturas associadas a um Contacto).

**CONTEXTO:**
- Smart buttons são os botões coloridos que mostram contagens (ex: "CRM 3", "Vendas 12")
- Ao clicar num smart button:
  - Se houver 1 registo → redireciona direto para o formulário de detalhe
  - Se houver múltiplos → mostra vista de lista para o user escolher

**OBJETIVO:** Criar template base que pode ser herdado por todas as vistas de smart buttons, evitando duplicação de código HTML/CSS e mantendo UI consistente.

- [ ] **Criar template base**
  - [ ] Criar `templates/components/smart_button_list_base.html`
  - [ ] Estrutura com blocks Django para herança:
    - [ ] `{% block title %}` - Título da página (ex: "Leads CRM - Alexandra Brito")
    - [ ] `{% block breadcrumbs %}` - Opcional para navegação
    - [ ] `{% block table_headers %}` - Cabeçalhos das colunas da tabela
    - [ ] `{% block table_rows %}` - Linhas dos dados (loop dos registos)
    - [ ] `{% block empty_state %}` - Mensagem quando não há dados
    - [ ] `{% block actions %}` - Botões de ação (ex: "Criar Novo")
  - [ ] Estrutura CSS/Tailwind consistente:
    - [ ] Header com título e botão voltar
    - [ ] Tabela responsiva com dark mode
    - [ ] Estados: loading, empty, populated
    - [ ] Hover effects nas linhas (cursor pointer)
    - [ ] Links clicáveis para cada registo

- [ ] **Criar documentação de uso**
  - [ ] Adicionar comentários no template explicando como herdar
  - [ ] Exemplo de uso no topo do arquivo
  - [ ] Listar todos os blocks obrigatórios vs opcionais

- [ ] **Criar template de exemplo**
  - [ ] Criar `templates/contacts/smart_button_example.html` (referência)
  - [ ] Demonstrar herança do base
  - [ ] Mostrar como override de cada block
  - [ ] Exemplo completo funcional com dados mockados

- [ ] **Testing - Smart Button Base Template**
  - [ ] Test: template compila sem erros
  - [ ] Test: herança funciona (extends/block)
  - [ ] Test: todos os blocks podem ser overridden
  - [ ] Test: CSS responsivo funciona em mobile/desktop
  - [ ] Test: dark mode funciona

**NOTA:** Este template será usado nas tarefas seguintes para criar vistas de:
- Contactos ↔ CRM leads
- Contactos ↔ Vendas
- Contactos ↔ Compras
- Contactos ↔ Faturas
- Vendas ↔ Faturas
- Vendas ↔ CRM leads
- Produtos ↔ BOMs
- E outras relações modulares

---

## 4.17 Relações e Smart Buttons - Módulo Contactos

**OBJETIVO:** Documentar todas as relações FK que módulos futuros terão com Contactos + criar smart buttons bidirecionais + vistas de listagem.

**ARQUITETURA:** Opção 3 (Foreign Keys Diretas) - cada tabela nova (Vendas, CRM, Compras) terá campo `contact_id` apontando para Contact.

- [ ] **Relações FK Recebidas (outros módulos → Contact)**
  - [ ] **CRM/Leads** (Fase futura):
    - [ ] Modelo `Lead` terá campo `contact = ForeignKey(Contact, on_delete=CASCADE, related_name='leads')`
    - [ ] Smart button: "CRM" no formulário de Contact (contador dinâmico)
    - [ ] Vista: `contact_crm_list(contact_id)` usando template base (herda `smart_button_list_base.html`)
    - [ ] Rota: `/contacts/<uuid:pk>/crm/`
    - [ ] Colunas tabela: Referência, Estado, Valor Estimado, Data Criação
    - [ ] Se 1 lead → redireciona para `lead_detail(pk)`
    - [ ] Se múltiplas → mostra lista clicável
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

# 🚀 FASE 6: APP - INVENTÁRIO (PRODUTOS E STOCK)

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de gestão de produtos e stock básico
**📦 Dependências:** Fase 3 (base models), Fase 4 (contacts para suppliers)

---

## 6.1 Criação da App 'inventory'

Criar app Django para gestão de inventário.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp inventory apps/inventory`
  - [ ] Adicionar 'apps.inventory' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar models.py, views.py, forms.py, urls.py

---

## 6.2 Modelo Category

Criar categorias para produtos.

- [ ] **Criar modelo Category**
  - [ ] Herdar de BaseModel
  - [ ] Campos: name, description, parent (self FK para subcategorias)
  - [ ] Campo: **owner_company** (FK para Company, null=True, blank=True) - NULL=global, com valor=privado
  - [ ] Método __str__
  - [ ] Filtrar por owner_company na CategoryListView usando filter_by_company()
  - [ ] Auto-preencher owner_company na create view com get_active_company()

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar CategoryAdmin com list_display

- [ ] **Testing - Category**
  - [ ] Test: criar categoria funciona
  - [ ] Test: hierarquia de categorias funciona

---

## 6.3 Modelo Product

Criar modelo de produtos.

- [ ] **Criar modelo Product**
  - [ ] Herdar de BaseModel
  - [ ] Campos: code (único), name, description, category (FK)
  - [ ] Campos: unit_type (KG, UN, L, etc.)
  - [ ] Campos: cost_price, sale_price, tax_rate
  - [ ] Campos: image (ImageField)
  - [ ] Campos: supplier (FK para Contact)
  - [ ] Campo: **owner_company** (FK para Company, null=True, blank=True) - NULL=global, com valor=privado
  - [ ] Método __str__, método get_profit_margin()
  - [ ] Filtrar por owner_company na ProductListView usando filter_by_company()
  - [ ] Auto-preencher owner_company na create view com get_active_company()

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar ProductAdmin
  - [ ] list_display: code, name, category, cost_price, sale_price
  - [ ] search_fields, list_filter

- [ ] **Testing - Product**
  - [ ] Test: criar produto via admin funciona
  - [ ] Test: upload de imagem funciona
  - [ ] Test: cálculo de margem funciona

---

## 6.4 Modelo StockMovement

Criar modelo para movimentações de stock (entrada/saída).

- [ ] **Criar modelo StockMovement**
  - [ ] Herdar de BaseModel
  - [ ] Campos: product (FK), quantity, movement_type (IN, OUT, ADJUSTMENT)
  - [ ] Campos: reference_doc (opcional, para compras/vendas)
  - [ ] Campos: reason, user (FK), timestamp
  - [ ] Campo: **owner_company** (FK para Company, null=True, blank=True) - Herdar de product.owner_company
  - [ ] Método __str__

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar StockMovementAdmin
  - [ ] Apenas visualização (não edição)

- [ ] **Testing - StockMovement**
  - [ ] Test: criar movimentação funciona
  - [ ] Test: histórico é registrado

---

## 6.5 Modelo Stock (Saldo Atual)

Criar modelo para stock atual de cada produto.

- [ ] **Criar modelo Stock**
  - [ ] Campos: product (OneToOne), quantity, last_updated
  - [ ] Campo: **owner_company** (FK para Company, null=True, blank=True) - Herdar de product.owner_company
  - [ ] Método update_stock(quantity, movement_type)

- [ ] **Criar signal para atualização automática**
  - [ ] Signal post_save de StockMovement atualiza Stock
  - [ ] Entrada: quantity += quantidade
  - [ ] Saída: quantity -= quantidade

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Testing - Stock**
  - [ ] Test: criar StockMovement atualiza Stock automaticamente
  - [ ] Test: saldo é calculado corretamente

---

## 6.6 Views de Listagem de Produtos

Criar views para listar produtos.

- [ ] **Criar ProductListView**
  - [ ] Listar todos os produtos
  - [ ] Busca por code/name
  - [ ] Filtro por categoria
  - [ ] Mostrar stock atual

- [ ] **Criar template**
  - [ ] `templates/inventory/product_list.html` (standalone)
  - [ ] Tabela com: code, name, category, cost, sale, stock, actions

- [ ] **Configurar rota**
  - [ ] `path('inventory/products/', ProductListView, name='product_list')`

- [ ] **Testing - Product List**
  - [ ] Test: listar produtos funciona
  - [ ] Test: busca funciona
  - [ ] Test: stock é exibido

---

## 6.7 Views de Criação/Edição de Produtos

Criar views para CRUD de produtos.

- [ ] **Criar ProductCreateView**
  - [ ] Form com todos os campos
  - [ ] Upload de imagem

- [ ] **Criar ProductUpdateView**
  - [ ] Form pré-preenchido
  - [ ] Substituir imagem

- [ ] **Criar ProductDetailView**
  - [ ] Mostrar todas as informações
  - [ ] Mostrar histórico de stock

- [ ] **Criar templates**
  - [ ] `templates/inventory/product_create.html` (standalone)
  - [ ] `templates/inventory/product_update.html` (standalone)
  - [ ] `templates/inventory/product_detail.html` (standalone)

- [ ] **Configurar rotas**
  - [ ] `/inventory/products/new/`
  - [ ] `/inventory/products/<uuid:pk>/edit/`
  - [ ] `/inventory/products/<uuid:pk>/`

- [ ] **Testing - Product CRUD**
  - [ ] Test: criar produto funciona
  - [ ] Test: editar produto funciona
  - [ ] Test: visualizar detalhes funciona

---

## 6.8 View de Stock Atual

Criar view para visualizar stock de todos os produtos.

- [ ] **Criar StockListView**
  - [ ] Listar todos os produtos com stock
  - [ ] Mostrar: product, quantity, last_updated
  - [ ] Filtro por categoria
  - [ ] Destacar produtos com stock baixo (configurável)

- [ ] **Criar template**
  - [ ] `templates/inventory/stock_list.html` (standalone)
  - [ ] Tabela com alertas visuais

- [ ] **Configurar rota**
  - [ ] `path('inventory/stock/', StockListView, name='stock_list')`

- [ ] **Testing - Stock List**
  - [ ] Test: visualizar stock funciona
  - [ ] Test: alertas de stock baixo aparecem

---

## 6.9 Ajustes de Stock Manual

Criar view para ajustes manuais de stock.

- [ ] **Criar StockAdjustmentView**
  - [ ] Form: product, quantity, reason, is_loss (checkbox)
  - [ ] Se is_loss=True, registrar perda financeira

- [ ] **Criar template**
  - [ ] `templates/inventory/stock_adjustment.html` (standalone)
  - [ ] Form com validações

- [ ] **Criar StockMovement ao salvar**
  - [ ] movement_type = ADJUSTMENT
  - [ ] Registrar reason

- [ ] **Configurar rota**
  - [ ] `path('inventory/stock/adjust/', StockAdjustmentView, name='stock_adjustment')`

- [ ] **Testing - Stock Adjustment**
  - [ ] Test: ajuste de stock funciona
  - [ ] Test: stock é atualizado
  - [ ] Test: perda é registrada se marcado

---

## 6.10 Relatório de Movimentações de Stock

Criar view para histórico de movimentações.

- [ ] **Criar StockMovementListView**
  - [ ] Listar todas as movimentações
  - [ ] Filtros: data, produto, tipo de movimento
  - [ ] Paginação

- [ ] **Criar template**
  - [ ] `templates/inventory/stock_movements.html` (standalone)
  - [ ] Tabela com: data, produto, tipo, quantidade, user, reason

- [ ] **Configurar rota**
  - [ ] `path('inventory/movements/', StockMovementListView, name='stock_movements')`

- [ ] **Testing - Stock Movements**
  - [ ] Test: visualizar histórico funciona
  - [ ] Test: filtros funcionam

---

## 6.11 Alertas de Stock Mínimo

Implementar sistema de alertas de stock baixo.

- [ ] **Adicionar campo min_stock em Product**
  - [ ] Criar migration para adicionar campo

- [ ] **Criar view de alertas**
  - [ ] Listar produtos com stock < min_stock
  - [ ] Destacar em vermelho

- [ ] **Adicionar no Dashboard**
  - [ ] Widget com contagem de produtos com stock baixo

- [ ] **Testing - Stock Alerts**
  - [ ] Test: produtos com stock baixo aparecem em alerta
  - [ ] Test: dashboard mostra contagem

---

## 6.12 Importação de Produtos (CSV)

Permitir importar produtos via CSV.

- [ ] **Criar ProductImportView**
  - [ ] Upload CSV
  - [ ] Validar estrutura
  - [ ] Criar produtos em batch

- [ ] **Criar template**
  - [ ] `templates/inventory/product_import.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('inventory/products/import/', ProductImportView, name='product_import')`

- [ ] **Testing - Product Import**
  - [ ] Test: importar CSV funciona
  - [ ] Test: validações funcionam

---

## 6.13 Relações e Smart Buttons - Módulo Produtos

**OBJETIVO:** Documentar todas as relações FK que Produtos terão com outros módulos + criar smart buttons bidirecionais + vistas de listagem.

- [ ] **Relações FK Recebidas (outros módulos → Product)**
  - [ ] **Vendas** (Fase 7):
    - [ ] Modelo `SaleOrderLine` terá campo `product = ForeignKey(Product, on_delete=PROTECT, related_name='sale_lines')`
    - [ ] Smart button: "Vendas" no formulário de Product (contador de quantas vendas incluíram este produto)
    - [ ] Vista: `product_sales_list(product_id)` usando template base
    - [ ] Rota: `/products/<uuid:pk>/sales/`
    - [ ] Colunas tabela: Nº Venda, Cliente, Data, Quantidade Vendida, Total Linha
    - [ ] Se 1 venda → redireciona para `sale_detail(pk)`
    - [ ] Se múltiplas → mostra lista clicável
  - [ ] **Compras** (Fase 6):
    - [ ] Modelo `PurchaseOrderLine` terá campo `product = ForeignKey(Product, on_delete=PROTECT, related_name='purchase_lines')`
    - [ ] Smart button: "Compras" no formulário de Product
    - [ ] Vista: `product_purchases_list(product_id)` usando template base
    - [ ] Rota: `/products/<uuid:pk>/purchases/`
    - [ ] Colunas tabela: Nº Compra, Fornecedor, Data, Quantidade Comprada, Custo Unitário
    - [ ] Se 1 compra → redireciona para `purchase_detail(pk)`
    - [ ] Se múltiplas → mostra lista clicável
  - [ ] **Movimentos Stock** (Fase 5 - mesma fase):
    - [ ] Modelo `StockMovement` já tem campo `product = ForeignKey(Product, on_delete=CASCADE, related_name='stock_movements')`
    - [ ] Smart button: "Movimentos" no formulário de Product
    - [ ] Vista: `product_movements_list(product_id)` usando template base
    - [ ] Rota: `/products/<uuid:pk>/movements/`
    - [ ] Colunas tabela: Data, Tipo (IN/OUT/ADJUSTMENT), Quantidade, Referência Doc, User
    - [ ] Sempre mostra lista (mesmo se 1 movimento)
  - [ ] **BOMs (Bill of Materials)** (Fase 9):
    - [ ] **Relação BIDIRECIONAL MAS ASSIMÉTRICA:**
      - [ ] Modelo `BOM` terá campo `product = ForeignKey(Product, on_delete=CASCADE, related_name='bom')` (produto finalizado que TEM uma BOM)
      - [ ] Modelo `BOMLine` terá campo `component = ForeignKey(Product, on_delete=PROTECT, related_name='used_in_boms')` (ingrediente usado EM outras BOMs)
    - [ ] Smart button "BOM" no formulário de Product:
      - [ ] Se `product.bom.exists()` → mostrar botão "BOM (1)" que vai direto para `bom_detail(bom_id)`
      - [ ] Se não tem BOM → botão fica disabled com "BOM (0)" ou oculto
    - [ ] Smart button "Usado em BOMs" NO formulário de Product:
      - [ ] **EXCEÇÃO:** NÃO criar este botão! (seria "Usado em 50 bolos" - info demasiada)
      - [ ] Razão: Um ingrediente como "Farinha" pode estar em 50+ BOMs, não faz sentido mostrar
    - [ ] Vista dentro da BOM:
      - [ ] Ao abrir `bom_detail(bom_id)`, mostra tabela de ingredientes (BOMLines)
      - [ ] Cada linha tem link para `product_detail(component_id)` do ingrediente
      - [ ] Mas ingrediente NÃO tem botão "Ver BOMs onde sou usado"

- [ ] **Método Helper para Contadores**
  - [ ] Adicionar método `Product.get_stats()` no modelo Product:
    ```python
    def get_stats(self):
        from django.db.models import Sum, Count
        return {
            'sales_count': self.sale_lines.values('sale_order').distinct().count(),
            'purchases_count': self.purchase_lines.values('purchase_order').distinct().count(),
            'movements_count': self.stock_movements.count(),
            'has_bom': self.bom.exists(),
            'total_sold': self.sale_lines.aggregate(Sum('quantity'))['quantity__sum'] or 0,
            'current_stock': self.current_stock or 0,  # campo direto no Product
        }
    ```
  - [ ] No template do formulário Product, chamar `product.get_stats` para popular os smart buttons

- [ ] **Testing - Product Relations**
  - [ ] Test: `product.get_stats()` retorna contadores corretos
  - [ ] Test: smart button Vendas conta distintas vendas (não linhas)
  - [ ] Test: smart button Compras conta distintas compras
  - [ ] Test: smart button BOM só aparece se produto TEM bom
  - [ ] Test: ingrediente NÃO mostra botão "Usado em BOMs"
  - [ ] Test: vistas usam template base corretamente

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

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de geração de PDFs para documentos (orçamentos, faturas, etc.)
**📦 Dependências:** Fase 7 (compras), Fase 8 (vendas)

---

## 11.1 Criação da App 'documents'

Criar app Django para geração de PDFs.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp documents apps/documents`
  - [ ] Adicionar 'apps.documents' ao INSTALLED_APPS

---

## 11.2 Template Base para PDFs

Criar template base HTML para PDFs.

- [ ] **Criar template base**
  - [ ] Criar `templates/documents/pdf_base.html`
  - [ ] Definir header fixo (logo, empresa)
  - [ ] Definir footer fixo (página, termos)
  - [ ] Área de conteúdo variável

- [ ] **Estilização**
  - [ ] CSS inline para PDF
  - [ ] Garantir compatibilidade com ReportLab

---

## 11.3 Template para Orçamento PDF

Criar template específico para orçamentos.

- [ ] **Criar template**
  - [ ] Criar `templates/documents/pdf_quotation.html`
  - [ ] Header: dados da empresa
  - [ ] Dados do cliente
  - [ ] Tabela de produtos/serviços
  - [ ] Totais e condições

---

## 11.4 Template para Fatura PDF

Criar template específico para faturas.

- [ ] **Criar template**
  - [ ] Criar `templates/documents/pdf_invoice.html`
  - [ ] Similar ao orçamento
  - [ ] Adicionar informações fiscais
  - [ ] Condições de pagamento

---

## 11.5 Função de Geração de PDF

Criar função utilitária para gerar PDFs.

- [ ] **Criar utils**
  - [ ] Criar `apps/documents/utils.py`
  - [ ] Função `generate_pdf(template, context, filename)`
  - [ ] Usar ReportLab para conversão HTML → PDF
  - [ ] Salvar em /media/documents/

- [ ] **Testing - PDF Generation**
  - [ ] Test: gerar PDF funciona
  - [ ] Test: PDF é salvo corretamente

---

## 11.6 Views de Geração de PDF para Vendas

Integrar geração de PDF nas vendas.

- [ ] **Criar SaleOrderPDFView**
  - [ ] Gerar PDF de orçamento/fatura
  - [ ] Retornar PDF para download ou visualização

- [ ] **Adicionar links nos templates**
  - [ ] Link "Download PDF" no SaleOrderDetailView
  - [ ] Link "Visualizar PDF" (abrir em nova aba)

- [ ] **Configurar rota**
  - [ ] `path('sales/<uuid:pk>/pdf/', SaleOrderPDFView, name='sale_pdf')`

- [ ] **Testing - Sale PDF**
  - [ ] Test: gerar PDF de orçamento funciona
  - [ ] Test: gerar PDF de fatura funciona
  - [ ] Test: PDF contém todos os dados

---

## 11.7 Views de Geração de PDF para Compras

Integrar geração de PDF nas compras.

- [ ] **Criar PurchaseOrderPDFView**
  - [ ] Gerar PDF de encomenda de compra

- [ ] **Adicionar link no template**
  - [ ] Link no PurchaseOrderDetailView

- [ ] **Configurar rota**
  - [ ] `path('purchases/<uuid:pk>/pdf/', PurchaseOrderPDFView, name='purchase_pdf')`

- [ ] **Testing - Purchase PDF**
  - [ ] Test: gerar PDF de compra funciona

---

## 11.8 Personalização de Templates de PDF

Permitir customizar templates via admin.

- [ ] **Criar modelo PDFTemplate**
  - [ ] Campos: name, template_type (QUOTATION, INVOICE, PURCHASE)
  - [ ] Campos: header_html, footer_html
  - [ ] Campo: is_default

- [ ] **Registrar no Admin**
  - [ ] Criar PDFTemplateAdmin

- [ ] **Atualizar generate_pdf**
  - [ ] Usar PDFTemplate customizado se existir

- [ ] **Testing - Custom Templates**
  - [ ] Test: customizar template funciona
  - [ ] Test: PDF usa template customizado

---

# 🚀 FASE 12: APP - MARKETING E WHATSAPP

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de marketing e integração WhatsApp
**📦 Dependências:** Fase 4 (contacts), Fase 11 (PDFs)

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
**🎯 Objetivo:** Implementar funcionalidades avançadas de stock (ajustes com motivos, perdas fiscais)
**📦 Dependências:** Fase 6 (inventory), Fase 9 (finance)

---

## 13.1 Modelo StockAdjustmentReason

Criar modelo para motivos de ajuste.

- [ ] **Criar modelo**
  - [ ] Campos: name, is_loss, description
  - [ ] Ex: "Quebra", "Vencimento", "Erro de contagem"

- [ ] **Registrar no Admin**
  - [ ] Criar StockAdjustmentReasonAdmin

---

## 13.2 Atualizar StockMovement com Reason

Adicionar campo reason ao StockMovement.

- [ ] **Criar migration**
  - [ ] Adicionar campo reason (FK para StockAdjustmentReason)
  - [ ] Adicionar campo is_loss (Boolean)

- [ ] **Atualizar forms e views**
  - [ ] Incluir seleção de reason em ajustes

---

## 13.3 Integração com Financeiro para Perdas

Quando ajuste é perda, deduzir no lucro.

- [ ] **Atualizar signal de StockMovement**
  - [ ] Se is_loss=True, criar Transaction (LOSS)
  - [ ] amount = product.cost_price * quantity

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

Criar view de histórico completo de stock.

- [ ] **Criar ProductStockHistoryView**
  - [ ] Listar todas as movimentações de um produto
  - [ ] Mostrar saldo após cada movimentação

- [ ] **Criar template**
  - [ ] `templates/inventory/product_stock_history.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('inventory/products/<uuid:pk>/stock-history/', ProductStockHistoryView, name='product_stock_history')`

- [ ] **Testing - Stock History**
  - [ ] Test: histórico mostra todas as movimentações

---

## 13.6 Alertas e Notificações de Stock

Criar sistema de alertas de stock baixo.

- [ ] **Criar Celery task periódica**
  - [ ] Task que roda diariamente
  - [ ] Verificar produtos com stock < min_stock
  - [ ] Enviar email/notificação para admins

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