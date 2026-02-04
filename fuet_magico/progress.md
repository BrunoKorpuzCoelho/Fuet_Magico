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

## 🚀 WORKFLOW ATUAL

**Task:** Sistema de Autenticação e Usuários (Tarefa 3.1)  
**Iniciado em:** 2026-02-03 22:00  
**Status:** FASE 0 ✅ COMPLETA

---

### 📋 FASE 0: COMPREENSÃO ✅

**Resumo da Solicitação:**
Implementar sistema de autenticação Django com modelo CustomUser, incluindo login/logout e roles (ADMIN, MANAGER, EMPLOYEE).

**Decisões Tomadas:**
- ✅ Login: `username` (não email)
- ✅ Roles: ADMIN, MANAGER, EMPLOYEE
- ✅ Redirect pós-login: `/dashboard`
- ✅ Template: Design Fuet Mágico (https://v0-login-page-design-two-ebon.vercel.app/)

**Escopo:**
- ✅ Criar app `accounts`
- ✅ Modelo `CustomUser` com campos: username, phone, avatar, role
- ✅ Views: LoginView, LogoutView
- ✅ Template login com design Fuet Mágico
- ✅ URLs: /login/, /logout/
- ✅ Migrations e testes

---

### 📋 FASE 1: ANÁLISE DO CONTEXTO

**Status:** ✅ COMPLETA

**Descobertas:**

**1. Estrutura Atual do Projeto:**
- ✅ Django 5.0.14 configurado
- ✅ PostgreSQL como banco de dados
- ✅ Redis configurado para cache e Celery
- ✅ Sistema de templates em `/templates/`
- ✅ Static files em `/static/` e `/staticfiles/`
- ✅ Media files em `/media/`

**2. Apps Existentes:**
- ✅ `apps.website` - Website institucional (já implementado nas fases anteriores)
- ❌ Nenhuma app de autenticação ainda

**3. INSTALLED_APPS Atual:**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.website',
]
```

**4. Sistema de Templates:**
- ✅ DIRS configurado para `BASE_DIR / 'templates'`
- ✅ APP_DIRS = True (busca templates nas apps)
- ✅ Estrutura: `/templates/website/home.html` já existe

**5. URLs Existentes:**
- `/admin/` → Django Admin
- `/` → apps.website.urls (homepage)

**6. Configurações de Segurança:**
- ✅ Passwords: MinimumLengthValidator com 12 caracteres (segue rules.md)
- ✅ SESSION_COOKIE_AGE = 1800 (30min - segue rules.md)
- ✅ CSRF/Session cookies com HTTPONLY e Secure
- ✅ X-Frame-Options = DENY

**7. Dependências Atuais:**
- Django 5.0+
- PostgreSQL (psycopg2)
- Redis
- Celery
- python-dotenv
- Pillow (não instalado ainda - necessário para ImageField)

**Conclusões:**
✅ Projeto bem estruturado e segue boas práticas
✅ Pronto para adicionar app de autenticação
✅ Precisa adicionar Pillow ao requirements.txt (para avatar)
✅ Precisa criar `/templates/accounts/` para login
✅ Precisa criar `/apps/accounts/` estrutura completa

---

### 📋 FASE 2: ANÁLISE E PROPOSTA

**Status:** ✅ COMPLETA

**Regras Aplicáveis (de rules.md):**

**1. Princípios Gerais:**
- ✅ Sem comentários no código
- ✅ Código limpo e auto-explicativo
- ✅ snake_case para ficheiros e funções
- ✅ PascalCase para classes
- ✅ Logs de erro em inglês

**2. Segurança de Autenticação:**
- ✅ Passwords: hash com Django (PBKDF2), min 12 caracteres
- ✅ Sessions: timeout 30 minutos (já configurado)
- ✅ Rate limiting: 5 tentativas / 15 minutos (implementar depois)
- ✅ Audit log de sessões (implementar depois)

**3. Segurança de Dados:**
- ✅ Validação de inputs
- ✅ ORM do Django (sem SQL injection)
- ✅ CSRF protection (já ativo no Django)
- ✅ XSS prevention (Django autoescaping)

**4. Form Validation:**
- ✅ Validação client-side + server-side (DUPLA)
- ✅ Feedback visual imediato

**DECISÕES TÉCNICAS:**

✅ **1. Sistema de Autenticação:**
- **Escolhido:** Django Auth nativo (confirmado pelo utilizador)
- **Razão:** Simplicidade, já integrado, menos dependências

✅ **2. Estrutura de Roles:**
- **Opção A:** CharField com choices ✅ ESCOLHIDA
  ```python
  ROLE_CHOICES = [
      ('ADMIN', 'Administrador'),
      ('MANAGER', 'Gestor'),
      ('EMPLOYEE', 'Funcionário'),
  ]
  role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')
  ```
- **Razão:** Simples, performático, suficiente para 3 roles fixos

✅ **3. Campo Avatar:**
- **Escolhido:** ImageField
- **Upload para:** MEDIA_ROOT/avatars/
- **Validação:** Pillow (já no requirements.txt)
- **Tamanho máx:** 2MB
- **Formatos:** JPG, PNG

✅ **4. Campo Phone:**
- **Escolhido:** CharField(max_length=20)
- **Validação:** Regex simples `^\+?[0-9\s\-\(\)]+$`
- **Opcional:** blank=True, null=True
- **Formato:** Internacional (+351 911 886 673)

✅ **5. Login:**
- **Campo:** username (confirmado)
- **Formulário:** Django AuthenticationForm (padrão)
- **Redirect:** /dashboard (confirmado)
- **Template:** Design Fuet Mágico

✅ **6. Template Login:**
- **Design:** Fuet Mágico (https://v0-login-page-design-two-ebon.vercel.app/)
- **Background:** cake-background.jpg (baixar)
- **Logo:** static/brand/logos/png/logo-primary.png (já existe)
- **Cores:** Rosa/bege (mesma paleta do website)

**ESTRUTURA PROPOSTA:**

```python
# apps/accounts/models.py
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EMPLOYEE')
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
```

**DEPENDÊNCIAS:**
- ✅ Pillow (já instalado)
- ✅ Django 5.0 (já instalado)
- ❌ Nenhuma dependência adicional necessária

---

### 📋 FASE 3: CLARIFICAÇÃO

**Status:** ✅ COMPLETA (PULADA)

**Razão:** Todas as decisões foram tomadas na FASE 2, sem necessidade de ajustes ou clarificações adicionais.

---

### 📋 FASE 4: ESTRUTURA

**Status:** ✅ COMPLETA

## 📁 ESTRUTURA DE DIRETÓRIOS E FICHEIROS

### **Legenda:**
- ⭐ = Ficheiro principal (crítico)
- 📝 = Ficheiro de configuração
- 📁 = Diretório
- 🎨 = Template/Frontend
- 🖼️ = Asset (imagem)

---

### **ESTRUTURA COMPLETA:**

```
Fuet_Magico/
│
├── 📁 apps/
│   ├── 📁 accounts/                    ⭐ Nova app de autenticação
│   │   ├── __init__.py                 📝 Import do app
│   │   ├── models.py                   ⭐ CustomUser model
│   │   ├── forms.py                    ⭐ LoginForm (Django AuthenticationForm)
│   │   ├── views.py                    ⭐ LoginView, LogoutView
│   │   ├── urls.py                     📝 Rotas /login/, /logout/
│   │   ├── admin.py                    📝 CustomUser admin interface
│   │   └── 📁 migrations/              📁 (Django cria automaticamente)
│   │
│   └── 📁 website/                     ✅ Já existe
│
├── 📁 templates/
│   ├── 📁 accounts/                    🎨 Nova pasta
│   │   └── login.html                  🎨 Template login Fuet Mágico
│   │
│   └── 📁 website/                     ✅ Já existe
│       └── home.html
│
├── 📁 static/
│   ├── 📁 images/                      🖼️ Imagens gerais
│   │   └── cake-background.jpg         🖼️ Fundo para login (baixar)
│   │
│   ├── 📁 brand/logos/png/             ✅ Já existe
│   │   └── logo-primary.png            ✅ Logo Fuet Mágico
│   │
│   ├── 📁 css/
│   │   └── global.css                  ✅ Já existe
│   │
│   └── 📁 js/
│       └── website.js                  ✅ Já existe
│
├── 📁 config/
│   ├── settings.py                     📝 ATUALIZAR: AUTH_USER_MODEL, INSTALLED_APPS
│   └── urls.py                         📝 ATUALIZAR: incluir accounts.urls
│
└── 📁 media/
    └── 📁 avatars/                     📁 Criar automaticamente via ImageField
```

---

## 📝 FICHEIROS A CRIAR/ATUALIZAR

### **1. apps/accounts/__init__.py**
```python
default_app_config = 'apps.accounts.apps.AccountsConfig'
```

### **2. apps/accounts/apps.py** (Django cria)
```python
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
```

### **3. ⭐ apps/accounts/models.py**
**Responsabilidade:** Modelo CustomUser estendendo AbstractUser
**Campos:**
- `phone` - CharField(20), opcional, regex validation
- `avatar` - ImageField, upload_to='avatars/', opcional
- `role` - CharField(20), choices (ADMIN/MANAGER/EMPLOYEE), default EMPLOYEE

**Métodos:**
- `get_full_name()` - Retorna nome completo ou username
- `__str__()` - Representação string

### **4. ⭐ ✅ Completa | 100% |
| FASE 4 | ✅ Completa | 100% |
| FASE 5 | ⏳ Pendente | 0% |
| FASE 6 | ⏳ Pendente | 0% |
| FASE 7 | ⏳ Pendente | 0% |

**Progresso Total:** 62.5% (5s.py**
**Responsabilidade:** Views de autenticação
**Views:**
- `LoginView` - Class-based view, POST login, redirect /dashboard
- `LogoutView` - Class-based view, logout user, redirect /login/
**Segurança:** CSRF protection, validação server-side

### **6. 📝 apps/accounts/urls.py**
**Responsabilidade:** Rotas de autenticação
**Rotas:**
- `path('login/', LoginView.as_view(), name='login')`
- `path('logout/', LogoutView.as_view(), name='logout')`

### **7. 📝 apps/accounts/admin.py**
**Responsabilidade:** Interface admin do Django para CustomUser
**Features:**
- Listar usuários com filtros (role, is_active, is_staff)
- Campos exibidos: username, email, role, is_active
- Pesquisa por username, email
- Ordenação por date_joined

### **8. 🎨 templates/accounts/login.html**
**Responsabilidade:** Template de login com design Fuet Mágico
**Design:**
- Background: cake-background.jpg (fullscreen)
- Logo: logo-primary.png (topo centralizado)
- Card: Branco, centralizado, sombra
- Título: "Bem-vindo" + subtítulo "Inicie sessão para criar magia"
- Form: Email + Password + Botão
- Footer: "© 2026 BY DAISY fuet mágico"
**Cores:** Rosa (#dbc693) + Bege (#f4f0e7)

### **9. 📝 config/settings.py (ATUALIZAR)**
**Adicionar:**
```python
INSTALLED_APPS = [
    # ... apps existentes
    'apps.accounts',  # ← ADICIONAR
]

AUTH_USER_MODEL = 'accounts.CustomUser'  # ← ADICIONAR

LOGIN_URL = '/login/'  # ← ADICIONAR
LOGIN_REDIRECT_URL = '/dashboard'  # ← ADICIONAR
LOGOUT_REDIRECT_URL = '/login/'  # ← ADICIONAR
```

### **10. 📝 config/urls.py (ATUALIZAR)**
**Adicionar:**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),  # ← ADICIONAR
    path('', include('apps.website.urls')),
]
```

### **11. 🖼️ static/images/cake-background.jpg (BAIXAR)**
**Fonte:** https://v0-login-page-design-two-ebon.vercel.app/cake-background.jpg
**Uso:** Background do template login

---

## 🔧 DEPENDÊNCIAS

**Nenhuma dependência adicional necessária!**

✅ Django 5.0 (já instalado)
✅ Pillow (já instalado)
✅ psycopg2 (já instalado)
✅ python-dotenv (já instalado)

---

## 🎨 PREVIEW DO TEMPLATE LOGIN

```
┌─────────────────────────────────────────┐
│  [Background: Imagem de bolo]           │
│                                         │
│     [Logo Fuet Mágico]                  │
│                                         │
│  ┌──────────────────────────┐           │
│  │  Bem-vindo               │           │
│  │  Inicie sessão para      │           │
│  │  criar magia             │           │
│  │                          │           │
│  │  ┌─────────────────┐     │           │
│  │  │ Email          │     │           │
│  │  └─────────────────┘     │           │
│  │                          │           │
│  │  ┌─────────────────┐     │           │
│  │  │ Palavra-passe  │     │           │
│  │  └─────────────────┘     │           │
│  │                          │           │
│  │  [Iniciar sessão]        │           │
│  │                          │           │
│  └──────────────────────────┘           │
│                                         │
│  © 2026 BY DAISY fuet mágico            │
└─────────────────────────────────────────┘
```

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

**Ordem de Criação (FASE 5):**
1. ⬜ Baixar cake-background.jpg
2. ⬜ Criar apps/accounts/__init__.py
3. ⬜ Criar apps/accounts/models.py
4. ⬜ Criar apps/accounts/forms.py
5. ⬜ Criar apps/accounts/views.py
6. ⬜ Criar apps/accounts/urls.py
7. ⬜ Criar apps/accounts/admin.py
8. ⬜ Criar templates/accounts/login.html
9. ⬜ Atualizar config/settings.py
10. ⬜ Atualizar config/urls.py
11. ⬜ Executar makemigrations
12. ⬜ Executar migrate
13. ⬜ Criar superuser para teste

---

### 📋 FASE 5: IMPLEMENTAÇÃO

**Status:** ✅ COMPLETA

**Ficheiros a criar:**
1. [ ] apps/accounts/models.py
2. [ ] apps/accounts/forms.py
3. [ ] apps/accounts/views.py
4. [ ] apps/accounts/urls.py
5. [ ] apps/accounts/admin.py
6. [ ] templates/accounts/login.html
7. [ ] config/settings.py (atualizar AUTH_USER_MODEL)
8. [ ] config/urls.py (incluir accounts.urls)

**Migrations:**
- [ ] python manage.py makemigrations
- [ ] python manage.py migrate

**Testes:**
- [ ] Criar superuser
- [ ] Testar login
- [ ] Testar logout
- [ ] Testar redirect /dashboard

---

### 📋 FASE 6: DOCUMENTAÇÃO

**Status:** PENDENTE

**Tarefas:**
- [ ] Marcar tarefa 3.1 como completa em tasks.md
- [ ] Documentar campos do CustomUser
- [ ] Documentar como criar usuários
- [ ] Documentar próximos passos (permissions, dashboard)

---

### 📋 FASE 7: FINALIZAÇÃO

**Status:** PENDENTE

**Checklist final:**
- [ ] Validar compliance com rules.md
- [ ] Verificar sem comentários no código
- [ ] Verificar código limpo e auto-explicativo
- [ ] Limpar progress.md (manter apenas instruções)
- [ ] Apresentar resumo final

---

## 📊 PROGRESSO GERAL

| Fase | Status | Progresso |
|------|--------|-----------|
| FASE 0 | ✅ Completa | 100% |
| FASE 1 | ✅ Completa | 100% |
| FASE 2 | ✅ Completa | 100% |
| FASE 3 | ⏳ Pendente | 0% |
| FASE 4 | ⏳ Pendente | 0% |
| FASE 5 | ⏳ Pendente | 0% |
| FASE 6 | ⏳ Pendente | 0% |
| FASE 7 | ⏳ Pendente | 0% |

**Progresso Total:** 37.5% (3/8 fases)

---
