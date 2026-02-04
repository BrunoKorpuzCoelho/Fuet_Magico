# 🎯 FUET MÁGICO - FULL STACK MANAGEMENT SYSTEM - DEVELOPMENT CHECKLIST

> **Stack:** Python 3.12+, Django 5.0+, Django ORM, PostgreSQL 17+, Redis, Celery, JavaScript Native, Tailwind CSS (via CDN)
> **Formato:** Checkboxes hierárquicos (Fase → Tarefa → Sub-tarefa)
> **Objetivo:** Sistema completo de gestão empresarial para Fuet Mágico - incluindo Vendas, Inventário, Compras, CRM, Financeiro, Marketing, Configurador de Produtos e Website Institucional. Desenvolvimento do zero - seguir todas as tasks = projeto funcionando ✅

---

## 📊 PROGRESSO GERAL

- **Fase 1:** 8/8 features (100%) - Setup Ambiente e Infraestrutura ✅ COMPLETA!
- **Fase 2:** 0/6 features (0%) - Frontend - Website Institucional (HTML Copy)
- **Fase 3:** 0/10 features (0%) - Backend - Estrutura Base Django
- **Fase 4:** 0/8 features (0%) - App: Contactos (CRM)
- **Fase 5:** 0/12 features (0%) - App: Inventário (Produtos e Stock)
- **Fase 6:** 0/10 features (0%) - App: Compras
- **Fase 7:** 0/12 features (0%) - App: Vendas
- **Fase 8:** 0/8 features (0%) - App: Financeiro
- **Fase 9:** 0/18 features (0%) - BOM (Bill of Materials) - Sistema de Receitas
- **Fase 10:** 0/8 features (0%) - Sistema de PDFs (Documentos)
- **Fase 11:** 0/6 features (0%) - App: Marketing e WhatsApp
- **Fase 12:** 0/6 features (0%) - Stock Management Avançado
- **Fase 13:** 0/6 features (0%) - PDF Scanning (Entrada de Compras)
- **Fase 14:** 0/6 features (0%) - Integração Final e Deployment

**TOTAL:** 8/122 features (6.6%)

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

- [ ] **Criar app 'accounts'**
  - [ ] Executar `python manage.py startapp accounts apps/accounts`
  - [ ] Adicionar 'apps.accounts' ao INSTALLED_APPS

- [ ] **Criar modelo CustomUser**
  - [ ] Estender AbstractUser em `apps/accounts/models.py`
  - [ ] Adicionar campos: phone, avatar, role (ADMIN, MANAGER, EMPLOYEE)
  - [ ] Adicionar AUTH_USER_MODEL = 'accounts.CustomUser' no settings

- [ ] **Criar forms e views**
  - [ ] Criar LoginView, LogoutView
  - [ ] Criar template de login standalone

- [ ] **Configurar URLs**
  - [ ] Criar `apps/accounts/urls.py`
  - [ ] Adicionar rotas: /login/, /logout/
  - [ ] Incluir no config/urls.py

- [ ] **Testing - Autenticação**
  - [ ] Test: makemigrations e migrate sem erros
  - [ ] Test: criar superuser funciona
  - [ ] Test: login e logout funcionam

---

## 3.2 Django Admin Customização

Configurar Django Admin para gestão.

- [ ] **Customizar Admin**
  - [ ] Configurar admin.site.site_header = 'Fuet Mágico Admin'
  - [ ] Configurar admin.site.site_title = 'Fuet Mágico'
  - [ ] Configurar admin.site.index_title = 'Gestão'

- [ ] **Registrar CustomUser no admin**
  - [ ] Criar UserAdmin em `apps/accounts/admin.py`
  - [ ] Configurar list_display, search_fields, list_filter

- [ ] **Testing - Admin**
  - [ ] Test: acessar /admin/ funciona
  - [ ] Test: login com superuser funciona
  - [ ] Test: visualizar usuários no admin

---

## 3.3 Middleware e Permissions

Criar middleware para controlo de acesso.

- [ ] **Criar middleware de autenticação**
  - [ ] Criar `apps/accounts/middleware.py`
  - [ ] Verificar se usuário está autenticado em rotas protegidas
  - [ ] Adicionar ao MIDDLEWARE no settings

- [ ] **Criar decorators**
  - [ ] Criar `@login_required_custom`
  - [ ] Criar `@role_required(role='ADMIN')`

- [ ] **Testing - Middleware**
  - [ ] Test: rotas protegidas redirecionam para login
  - [ ] Test: decorators funcionam corretamente

---

## 3.4 Modelos Base (Abstract Models)

Criar modelos abstratos para reutilização.

- [ ] **Criar BaseModel**
  - [ ] Criar `apps/core/` (app helper)
  - [ ] Criar `apps/core/models.py`
  - [ ] Criar AbstractBaseModel com: id (UUID), created_at, updated_at, is_active

- [ ] **Adicionar ao INSTALLED_APPS**
  - [ ] Adicionar 'apps.core'

- [ ] **Testing - Base Models**
  - [ ] Test: outros models podem herdar de BaseModel

---

## 3.5 Configuração de Media Files

Configurar upload e servir arquivos de media.

- [ ] **Configurar settings**
  - [ ] Verificar MEDIA_URL = '/media/'
  - [ ] Verificar MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

- [ ] **Configurar URLs para desenvolvimento**
  - [ ] Adicionar static serve de media em `config/urls.py`
  - [ ] Adicionar `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`

- [ ] **Testing - Media**
  - [ ] Test: upload de arquivo via admin funciona
  - [ ] Test: acessar arquivo em /media/ funciona

---

## 3.6 Templates Base e Estrutura

Criar templates base para o sistema interno (não website).

- [ ] **Criar base template**
  - [ ] Criar `templates/base.html` (sistema interno)
  - [ ] Incluir Tailwind CSS via CDN
  - [ ] Criar navbar com menu
  - [ ] Criar sidebar (se necessário)
  - [ ] Criar footer

- [ ] **Criar templates de componentes**
  - [ ] Criar `templates/components/navbar.html`
  - [ ] Criar `templates/components/messages.html` (Django messages)

- [ ] **Testing - Templates Base**
  - [ ] Test: base.html renderiza corretamente
  - [ ] Test: herança de templates funciona

---

## 3.7 Dashboard Principal

Criar dashboard principal do sistema.

- [ ] **Criar app 'dashboard'**
  - [ ] Executar `python manage.py startapp dashboard apps/dashboard`
  - [ ] Adicionar ao INSTALLED_APPS

- [ ] **Criar view e template**
  - [ ] Criar `dashboard_view` em views.py
  - [ ] Criar template `dashboard/index.html` (standalone)
  - [ ] Mostrar resumo: vendas, compras, stock, clientes

- [ ] **Configurar rota**
  - [ ] Criar urls.py: `path('dashboard/', dashboard_view, name='dashboard')`
  - [ ] Incluir no config/urls.py

- [ ] **Testing - Dashboard**
  - [ ] Test: acessar /dashboard/ funciona
  - [ ] Test: usuário não autenticado é redirecionado

---

## 3.8 Sistema de Logs e Auditoria

Criar sistema para logging de ações.

- [ ] **Criar modelo AuditLog**
  - [ ] Criar em `apps/core/models.py`
  - [ ] Campos: user, action, model_name, object_id, timestamp, details (JSON)

- [ ] **Criar signals**
  - [ ] Criar signals para log automático em save/delete
  - [ ] Registrar signals

- [ ] **Registrar no Admin**
  - [ ] Criar AuditLogAdmin
  - [ ] Configurar list_display, search, filters

- [ ] **Testing - Audit Log**
  - [ ] Test: criar objeto gera log
  - [ ] Test: visualizar logs no admin

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

## 3.10 Gestão de Configurações Globais

Criar sistema para configurações do sistema.

- [ ] **Criar modelo Settings**
  - [ ] Criar em `apps/core/models.py`
  - [ ] Campos: key (unique), value (JSON), description

- [ ] **Criar view de configurações**
  - [ ] Criar view para listar/editar settings
  - [ ] Restringir acesso (apenas ADMIN)

- [ ] **Registrar no Admin**
  - [ ] Criar SettingsAdmin com inline editing

- [ ] **Testing - Settings**
  - [ ] Test: criar configuração funciona
  - [ ] Test: ler configuração via API interna

---

# 🚀 FASE 4: APP - CONTACTOS (CRM)

**⏱ Tempo estimado:** 3-4 dias
**🎯 Objetivo:** Criar sistema de gestão de clientes e contactos
**📦 Dependências:** Fase 3 (base models e autenticação)

---

## 4.1 Criação da App 'contacts'

Criar app Django para gestão de contactos.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp contacts apps/contacts`
  - [ ] Adicionar 'apps.contacts' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar `apps/contacts/models.py`
  - [ ] Criar `apps/contacts/views.py`
  - [ ] Criar `apps/contacts/forms.py`
  - [ ] Criar `apps/contacts/urls.py`

---

## 4.2 Modelo Contact

Criar modelo para clientes/contactos.

- [ ] **Criar modelo Contact**
  - [ ] Herdar de BaseModel
  - [ ] Campos: name, email, phone, whatsapp, address, city, postal_code, nif, notes
  - [ ] Campos: contact_type (CLIENT, SUPPLIER, BOTH)
  - [ ] Campos: tags (JSONField para categorização)
  - [ ] Método __str__

- [ ] **Criar migrations**
  - [ ] Executar makemigrations
  - [ ] Executar migrate

- [ ] **Registrar no Admin**
  - [ ] Criar ContactAdmin
  - [ ] Configurar list_display, search_fields, list_filter

- [ ] **Testing - Contact Model**
  - [ ] Test: criar contact via admin funciona
  - [ ] Test: todos os campos salvam corretamente

---

## 4.3 Views de Listagem de Contactos

Criar view para listar todos os contactos.

- [ ] **Criar ContactListView**
  - [ ] Criar view em `apps/contacts/views.py`
  - [ ] Implementar paginação (25 por página)
  - [ ] Implementar busca por nome/email/phone
  - [ ] Implementar filtro por contact_type

- [ ] **Criar template**
  - [ ] Criar `templates/contacts/list.html` (standalone)
  - [ ] Tabela com: name, email, phone, contact_type, actions
  - [ ] Barra de busca
  - [ ] Botão "Novo Contacto"

- [ ] **Configurar rota**
  - [ ] Adicionar `path('contacts/', ContactListView, name='contact_list')`
  - [ ] Incluir urls no config/urls.py

- [ ] **Testing - Contact List**
  - [ ] Test: acessar /contacts/ mostra lista
  - [ ] Test: busca funciona
  - [ ] Test: paginação funciona

---

## 4.4 Views de Criação de Contacto

Criar view para adicionar novo contacto.

- [ ] **Criar ContactCreateView**
  - [ ] Criar view para criar contacto
  - [ ] Validar email único
  - [ ] Validar phone/whatsapp formato

- [ ] **Criar form**
  - [ ] Criar ContactForm em forms.py
  - [ ] Validações customizadas

- [ ] **Criar template**
  - [ ] Criar `templates/contacts/create.html` (standalone)
  - [ ] Formulário com todos os campos
  - [ ] Validação JavaScript básica

- [ ] **Configurar rota**
  - [ ] Adicionar `path('contacts/new/', ContactCreateView, name='contact_create')`

- [ ] **Testing - Contact Create**
  - [ ] Test: criar contacto funciona
  - [ ] Test: validações funcionam
  - [ ] Test: redirecionamento após criação

---

## 4.5 Views de Edição e Detalhes

Criar views para editar e visualizar contacto.

- [ ] **Criar ContactDetailView**
  - [ ] Mostrar todas as informações do contacto
  - [ ] Mostrar histórico de vendas/compras relacionadas

- [ ] **Criar ContactUpdateView**
  - [ ] Formulário pré-preenchido
  - [ ] Validações

- [ ] **Criar templates**
  - [ ] `templates/contacts/detail.html` (standalone)
  - [ ] `templates/contacts/update.html` (standalone)

- [ ] **Configurar rotas**
  - [ ] `path('contacts/<uuid:pk>/', ContactDetailView, name='contact_detail')`
  - [ ] `path('contacts/<uuid:pk>/edit/', ContactUpdateView, name='contact_update')`

- [ ] **Testing - Contact Edit/Detail**
  - [ ] Test: visualizar detalhes funciona
  - [ ] Test: editar contacto funciona

---

## 4.6 Soft Delete de Contactos

Implementar soft delete (is_active=False) em vez de deletar.

- [ ] **Criar ContactDeleteView**
  - [ ] Marcar is_active=False
  - [ ] Confirmação antes de deletar

- [ ] **Atualizar queryset**
  - [ ] Filtrar is_active=True por padrão nas views

- [ ] **Criar template de confirmação**
  - [ ] `templates/contacts/confirm_delete.html` (standalone)

- [ ] **Configurar rota**
  - [ ] `path('contacts/<uuid:pk>/delete/', ContactDeleteView, name='contact_delete')`

- [ ] **Testing - Contact Delete**
  - [ ] Test: soft delete funciona
  - [ ] Test: contacto não aparece mais na lista
  - [ ] Test: ainda existe no banco (is_active=False)

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

# 🚀 FASE 5: APP - INVENTÁRIO (PRODUTOS E STOCK)

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de gestão de produtos e stock básico
**📦 Dependências:** Fase 3 (base models), Fase 4 (contacts para suppliers)

---

## 5.1 Criação da App 'inventory'

Criar app Django para gestão de inventário.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp inventory apps/inventory`
  - [ ] Adicionar 'apps.inventory' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar models.py, views.py, forms.py, urls.py

---

## 5.2 Modelo Category

Criar categorias para produtos.

- [ ] **Criar modelo Category**
  - [ ] Herdar de BaseModel
  - [ ] Campos: name, description, parent (self FK para subcategorias)
  - [ ] Método __str__

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar CategoryAdmin com list_display

- [ ] **Testing - Category**
  - [ ] Test: criar categoria funciona
  - [ ] Test: hierarquia de categorias funciona

---

## 5.3 Modelo Product

Criar modelo de produtos.

- [ ] **Criar modelo Product**
  - [ ] Herdar de BaseModel
  - [ ] Campos: code (único), name, description, category (FK)
  - [ ] Campos: unit_type (KG, UN, L, etc.)
  - [ ] Campos: cost_price, sale_price, tax_rate
  - [ ] Campos: image (ImageField)
  - [ ] Campos: supplier (FK para Contact)
  - [ ] Método __str__, método get_profit_margin()

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

## 5.4 Modelo StockMovement

Criar modelo para movimentações de stock (entrada/saída).

- [ ] **Criar modelo StockMovement**
  - [ ] Herdar de BaseModel
  - [ ] Campos: product (FK), quantity, movement_type (IN, OUT, ADJUSTMENT)
  - [ ] Campos: reference_doc (opcional, para compras/vendas)
  - [ ] Campos: reason, user (FK), timestamp
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

## 5.5 Modelo Stock (Saldo Atual)

Criar modelo para stock atual de cada produto.

- [ ] **Criar modelo Stock**
  - [ ] Campos: product (OneToOne), quantity, last_updated
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

## 5.6 Views de Listagem de Produtos

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

## 5.7 Views de Criação/Edição de Produtos

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

## 5.8 View de Stock Atual

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

## 5.9 Ajustes de Stock Manual

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

## 5.10 Relatório de Movimentações de Stock

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

## 5.11 Alertas de Stock Mínimo

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

## 5.12 Importação de Produtos (CSV)

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

# 🚀 FASE 6: APP - COMPRAS

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de gestão de compras e documentos de compra
**📦 Dependências:** Fase 4 (contacts), Fase 5 (inventory/products)

---

## 6.1 Criação da App 'purchases'

Criar app Django para gestão de compras.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp purchases apps/purchases`
  - [ ] Adicionar 'apps.purchases' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar models.py, views.py, forms.py, urls.py

---

## 6.2 Modelo PurchaseOrder

Criar modelo de encomenda/documento de compra.

- [ ] **Criar modelo PurchaseOrder**
  - [ ] Herdar de BaseModel
  - [ ] Campos: order_number (único, auto-gerado), supplier (FK Contact)
  - [ ] Campos: order_date, expected_delivery_date
  - [ ] Campos: status (DRAFT, CONFIRMED, RECEIVED, CANCELLED)
  - [ ] Campos: subtotal, tax, total (calculados)
  - [ ] Campos: notes
  - [ ] Método __str__, método generate_order_number()

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar PurchaseOrderAdmin
  - [ ] list_display: order_number, supplier, order_date, status, total

- [ ] **Testing - PurchaseOrder**
  - [ ] Test: criar purchase order funciona
  - [ ] Test: order_number é gerado automaticamente

---

## 6.3 Modelo PurchaseOrderLine

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

## 6.4 Views de Listagem de Compras

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

## 6.5 Views de Criação de Compra

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

## 6.6 Views de Edição e Detalhes

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

## 6.7 Confirmação de Compra

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

## 6.8 Receção de Compra (Entrada de Stock)

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

## 6.9 Cancelamento de Compra

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

## 6.10 Relatórios de Compras

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

# 🚀 FASE 7: APP - VENDAS

**⏱ Tempo estimado:** 5-6 dias
**🎯 Objetivo:** Criar sistema de vendas, orçamentos, encomendas e faturas
**📦 Dependências:** Fase 4 (contacts/clients), Fase 5 (inventory), Fase 6 (estrutura similar)

---

## 7.1 Criação da App 'sales'

Criar app Django para gestão de vendas.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp sales apps/sales`
  - [ ] Adicionar 'apps.sales' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar models.py, views.py, forms.py, urls.py

---

## 7.2 Modelo SaleOrder

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
  - [ ] Método __str__, método generate_order_number()

- [ ] **Criar migrations**
  - [ ] makemigrations e migrate

- [ ] **Registrar no Admin**
  - [ ] Criar SaleOrderAdmin
  - [ ] list_display: order_number, client, order_date, document_type, status, total

- [ ] **Testing - SaleOrder**
  - [ ] Test: criar sale order funciona
  - [ ] Test: order_number é gerado

---

## 7.3 Modelo SaleOrderLine

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

## 7.4 Views de Listagem de Vendas

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

## 7.5 Views de Criação de Venda/Orçamento

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

## 7.6 Views de Edição e Detalhes

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

## 7.7 Confirmação de Venda

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

## 7.8 Entrega de Venda (Saída de Stock)

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

## 7.9 Faturação de Venda

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

## 7.10 Cancelamento de Venda

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

## 7.11 Envio de Documentos por Email

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

## 7.12 Relatórios de Vendas

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

# 🚀 FASE 8: APP - FINANCEIRO

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de gestão financeira, balanços, perdas e ganhos
**📦 Dependências:** Fase 6 (compras), Fase 7 (vendas)

---

## 8.1 Criação da App 'finance'

Criar app Django para gestão financeira.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp finance apps/finance`
  - [ ] Adicionar 'apps.finance' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar models.py, views.py, urls.py

---

## 8.2 Modelo Transaction

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

## 8.3 Signal para Criar Transações Automáticas

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

## 8.4 View de Extrato Financeiro

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

## 8.5 Balanço Mensal

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

## 8.6 Relatório de Perdas e Ganhos

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

## 8.7 Dashboard Financeiro

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

## 8.8 Exportação de Relatórios Financeiros

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

# 🚀 FASE 9: BOM (BILL OF MATERIALS) - SISTEMA DE RECEITAS E CONFIGURADOR DE BOLOS

**⏱ Tempo estimado:** 6-8 dias
**🎯 Objetivo:** Criar sistema robusto de BOM multi-nível com cálculo automático de custos em cascata, gestão de componentes, unidades de medida, conversões e custos de mão-de-obra
**📦 Dependências:** Fase 5 (inventory/products) - Product model DEVE já existir

---

## 9.1 Criação da App 'bom'

Criar app Django para gestão de Bill of Materials (Receitas).

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp bom apps/bom`
  - [ ] Adicionar 'apps.bom' ao INSTALLED_APPS

- [ ] **Criar estrutura de arquivos**
  - [ ] Criar models.py, views.py, forms.py, urls.py, utils.py

---

## 9.2 Atualização do Modelo Product (Fase 5)

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

## 9.3 Modelo UnitOfMeasure (Unidades de Medida)

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

## 9.4 Modelo UnitConversion (Conversões entre Unidades)

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

## 9.5 Modelo ProductBOM (Receita/Lista de Materiais)

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

## 9.6 Modelo ProductBOMLine (Componentes da Receita)

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

## 9.7 Lógica de Cálculo de Custos em Cascata (RECURSIVA)

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

## 9.8 Sistema de Recálculo Global de Custos

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

## 9.9 Views de Gestão de BOM - Listagem

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

## 9.10 Views de Gestão de BOM - Criação

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

## 9.11 Views de Gestão de BOM - Edição e Detalhes

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

## 9.12 Ação de Recálculo Individual

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

## 9.13 Integração com Vendas - Venda por Fatias

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

## 9.14 Relatório de Análise de Custos

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

## 9.15 Interface de Configurador de Bolos (UI Específica)

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

## 9.16 Validações e Regras de Negócio

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

## 9.17 Documentação e Ajuda

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

## 9.18 Testes Integrados e Casos de Uso

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

# 🚀 FASE 10: SISTEMA DE PDFs (DOCUMENTOS)

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de geração de PDFs para documentos (orçamentos, faturas, etc.)
**📦 Dependências:** Fase 6 (compras), Fase 7 (vendas)

---

## 10.1 Criação da App 'documents'

Criar app Django para geração de PDFs.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp documents apps/documents`
  - [ ] Adicionar 'apps.documents' ao INSTALLED_APPS

---

## 10.2 Template Base para PDFs

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

## 10.3 Template para Orçamento PDF

Criar template específico para orçamentos.

- [ ] **Criar template**
  - [ ] Criar `templates/documents/pdf_quotation.html`
  - [ ] Header: dados da empresa
  - [ ] Dados do cliente
  - [ ] Tabela de produtos/serviços
  - [ ] Totais e condições

---

## 10.4 Template para Fatura PDF

Criar template específico para faturas.

- [ ] **Criar template**
  - [ ] Criar `templates/documents/pdf_invoice.html`
  - [ ] Similar ao orçamento
  - [ ] Adicionar informações fiscais
  - [ ] Condições de pagamento

---

## 10.5 Função de Geração de PDF

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

## 10.6 Views de Geração de PDF para Vendas

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

## 10.7 Views de Geração de PDF para Compras

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

## 10.8 Personalização de Templates de PDF

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

# 🚀 FASE 11: APP - MARKETING E WHATSAPP

**⏱ Tempo estimado:** 4-5 dias
**🎯 Objetivo:** Criar sistema de marketing e integração WhatsApp
**📦 Dependências:** Fase 4 (contacts), Fase 10 (PDFs)

---

## 11.1 Criação da App 'marketing'

Criar app Django para marketing.

- [ ] **Criar app**
  - [ ] Executar `python manage.py startapp marketing apps/marketing`
  - [ ] Adicionar 'apps.marketing' ao INSTALLED_APPS

---

## 11.2 Configuração de API WhatsApp

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

---

## 11.3 Modelo Campaign

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

## 11.4 Seleção de Destinatários

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

## 11.5 Criação e Envio de Campanha WhatsApp

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

## 11.6 Relatórios de Campanhas

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

# 🚀 FASE 12: STOCK MANAGEMENT AVANÇADO

**⏱ Tempo estimado:** 3-4 dias
**🎯 Objetivo:** Implementar funcionalidades avançadas de stock (ajustes com motivos, perdas fiscais)
**📦 Dependências:** Fase 5 (inventory), Fase 8 (finance)

---

## 12.1 Modelo StockAdjustmentReason

Criar modelo para motivos de ajuste.

- [ ] **Criar modelo**
  - [ ] Campos: name, is_loss, description
  - [ ] Ex: "Quebra", "Vencimento", "Erro de contagem"

- [ ] **Registrar no Admin**
  - [ ] Criar StockAdjustmentReasonAdmin

---

## 12.2 Atualizar StockMovement com Reason

Adicionar campo reason ao StockMovement.

- [ ] **Criar migration**
  - [ ] Adicionar campo reason (FK para StockAdjustmentReason)
  - [ ] Adicionar campo is_loss (Boolean)

- [ ] **Atualizar forms e views**
  - [ ] Incluir seleção de reason em ajustes

---

## 12.3 Integração com Financeiro para Perdas

Quando ajuste é perda, deduzir no lucro.

- [ ] **Atualizar signal de StockMovement**
  - [ ] Se is_loss=True, criar Transaction (LOSS)
  - [ ] amount = product.cost_price * quantity

- [ ] **Testing - Loss Integration**
  - [ ] Test: ajuste com perda cria transação financeira
  - [ ] Test: perda aparece no balanço mensal

---

## 12.4 Relatório de Perdas

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

## 12.5 Histórico de Stock por Produto

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

## 12.6 Alertas e Notificações de Stock

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

# 🚀 FASE 13: PDF SCANNING (ENTRADA DE COMPRAS)

**⏱ Tempo estimado:** 5-6 dias
**🎯 Objetivo:** Implementar scanning de PDFs para criar documentos de compra automaticamente
**📦 Dependências:** Fase 5 (inventory), Fase 6 (purchases)

---

## 13.1 Análise de PDFs de Fornecedores

Analisar estrutura dos PDFs recebidos.

- [ ] **Coletar amostras**
  - [ ] Obter PDFs exemplo dos fornecedores
  - [ ] Identificar padrões: referência, quantidade, preço

- [ ] **Documentar estrutura**
  - [ ] Criar documento com regras de parsing

---

## 13.2 Configuração de Parser de PDF

Instalar e configurar biblioteca de parsing.

- [ ] **Instalar dependências**
  - [ ] Adicionar PyPDF2 ou pdfplumber ao requirements.txt
  - [ ] pip install

- [ ] **Criar helper functions**
  - [ ] Criar `apps/purchases/pdf_parser.py`
  - [ ] Função `extract_text_from_pdf(pdf_file)`

---

## 13.3 Lógica de Extração de Dados

Criar lógica para extrair referências, quantidades e preços.

- [ ] **Criar função de parsing**
  - [ ] Função `parse_purchase_lines(text)`
  - [ ] Usar regex para identificar padrões
  - [ ] Retornar lista de dicionários: {reference, quantity, price}

- [ ] **Testing - Parser**
  - [ ] Test: parser extrai dados de PDF exemplo
  - [ ] Test: tratar erros de formato

---

## 13.4 View de Upload de PDF

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

## 13.5 Criação Automática de PurchaseOrder

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

## 13.6 Tratamento de Erros e Edge Cases

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

# 🚀 FASE 14: INTEGRAÇÃO FINAL E DEPLOYMENT

**⏱ Tempo estimado:** 3-4 dias
**🎯 Objetivo:** Integrar todos os módulos, testes finais e preparar para produção
**📦 Dependências:** Todas as fases anteriores

---

## 14.1 Testes de Integração

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

## 14.2 Dashboard Principal Completo

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

## 14.3 Menu de Navegação Final

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

## 14.4 Otimizações de Performance

Otimizar consultas e performance.

- [ ] **Adicionar select_related e prefetch_related**
  - [ ] Otimizar queries em views de listagem

- [ ] **Adicionar cache**
  - [ ] Cache de dashboard
  - [ ] Cache de relatórios

- [ ] **Adicionar índices**
  - [ ] Índices em campos de busca

---

## 14.5 Documentação

Criar documentação básica.

- [ ] **README.md**
  - [ ] Instruções de instalação
  - [ ] Configuração de .env
  - [ ] Como rodar o projeto

- [ ] **Documentação de API interna**
  - [ ] Documentar principais funções e models

---

## 14.6 Preparação para Produção

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
9. **BOM (Fase 9):** Sistema completo de receitas multi-nível com cálculo automático de custos em cascata
10. **Custos:** Incluem componentes + mão-de-obra (tempo * custo/hora)
11. **Conversões:** Sistema robusto de unidades (KG, G, L, ML, UN, SLICE, etc.)
12. **Recálculo:** Botão global para recalcular todos os custos quando preços mudam

---

## 🎯 PRÓXIMOS PASSOS

1. Começar pela Fase 1 (Setup)
2. Seguir sequencialmente as fases
3. Marcar progresso no `fuet_magico/progress.md` a partir da linha 110
4. Não avançar para próxima fase sem completar a anterior
5. Testar cada tarefa antes de marcar como concluída
6. **ATENÇÃO:** Fase 9 (BOM) é complexa - seguir ordem exata das tarefas para garantir dependências

---

**Última atualização:** 01/02/2026
**Total de Tarefas:** 122
**Status:** Pronto para desenvolvimento ✅


Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process; .\venv\Scripts\Activate.ps1; python manage.py runserver 0.0.0.0:8000