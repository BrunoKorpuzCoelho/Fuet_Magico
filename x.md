# 🔒 TEMPLATE - CYBERSECURITY & SECURITY RULES

> **Last Updated:** [Data Atual]  
> **Version:** 1.0  
> **Project Type:** [Frontend / Backend / Full-Stack / AI / Mobile / API / etc]  
> **Stack:** [Tecnologias específicas - ex: Django, Vue.js, PostgreSQL, Redis, etc]

---

## ⚠️ MANDATORY READING NOTICE

**THIS ENTIRE DOCUMENT MUST BE READ IN FULL.**

É obrigatório rever TODAS as regras de segurança neste documento, mesmo aquelas que podem não se aplicar imediatamente à tua tarefa atual. Compreender o contexto completo de segurança é crítico para prevenir vulnerabilidades e ataques. Segurança não é opcional - é responsabilidade de TODOS os desenvolvedores neste projeto.

**NÃO saltes secções.** Mesmo que estejas a trabalhar apenas em backend, deves compreender a segurança frontend. Mesmo que não estejas a implementar features de IA agora, deves conhecer os princípios de segurança de IA. Esta compreensão holística previne lacunas de segurança nos pontos de integração.

---

## 📋 TABLE OF CONTENTS

1. [Authentication & Session Security](#1-authentication--session-security)
2. [Authorization & Access Control](#2-authorization--access-control)
3. [Data Protection & Encryption](#3-data-protection--encryption)
4. [Input Validation & Injection Prevention](#4-input-validation--injection-prevention)
5. [API Security](#5-api-security)
6. [Frontend Security](#6-frontend-security)
7. [Backend Security (Django Specific)](#7-backend-security-django-specific)
8. [Database Security](#8-database-security)
9. [Multi-Tenant Isolation](#9-multi-tenant-isolation)
10. [AI Security & Model Protection](#10-ai-security--model-protection)
11. [Mobile Security](#11-mobile-security)
12. [Infrastructure & Network Security](#12-infrastructure--network-security)
13. [Secrets Management](#13-secrets-management)
14. [File Upload & Storage Security](#14-file-upload--storage-security)
15. [Third-Party Integrations](#15-third-party-integrations)
16. [Logging, Monitoring & Incident Response](#16-logging-monitoring--incident-response)
17. [Compliance & Privacy (GDPR, HIPAA, etc)](#17-compliance--privacy)
18. [Security Testing & Auditing](#18-security-testing--auditing)
19. [Deployment & CI/CD Security](#19-deployment--cicd-security)
20. [Disaster Recovery & Business Continuity](#20-disaster-recovery--business-continuity)
21. [Supply Chain Security](#21-supply-chain-security)
22. [Social Engineering & Human Factors](#22-social-engineering--human-factors)
23. [API Versioning & Deprecation Security](#23-api-versioning--deprecation-security)
24. [WebSocket Security](#24-websocket-security)
25. [GraphQL Security](#25-graphql-security)
26. [Service Mesh & Microservices Security](#26-service-mesh--microservices-security)
27. [Cryptojacking Prevention](#27-cryptojacking-prevention)
28. [Zero Trust Architecture](#28-zero-trust-architecture)
29. [Error Handling & Information Disclosure](#29-error-handling--information-disclosure)
30. [Advanced Threat Protection](#30-advanced-threat-protection)

---

## 1. AUTHENTICATION & SESSION SECURITY

### **JWT Token Security**

**Rule 1.1 - Token Expiration**

- Token de acesso (Access Token): máximo **1 hora** de expiração
- Token de atualização (Refresh Token): máximo **7 dias**
- Tokens curtos minimizam janela de exposição
- Implementar rotação de tokens no refresh
- Tokens devem expirar automaticamente no servidor

**Rule 1.2 - Secret Key Management**

- Chaves secretas JWT NUNCA no código fonte
- Armazenar em ficheiro `.env` (excluído do Git)
- Usar secrets diferentes por ambiente (dev/staging/prod)
- Rotação automática de secrets a cada **90 dias**
- Alertas em caso de falha na rotação
- Complexidade mínima: 256 bits (32 caracteres aleatórios)

**Rule 1.3 - Token Invalidation**

- Invalidar todos os tokens no logout
- Implementar lista de revogação (blacklist/revocation list)
- Armazenar tokens revogados até expiração natural
- Limpar lista de revogação de tokens expirados diariamente
- Invalidar todos os tokens do utilizador em mudança de password
- Invalidar tokens em alterações críticas (email, 2FA, etc)

**Rule 1.4 - Token Security Headers**

- Armazenar tokens em cookies `httpOnly` (NUNCA em localStorage)
- Flag `Secure` ativada (HTTPS obrigatório)
- `SameSite=Strict` para prevenir CSRF
- Incluir token anti-CSRF para operações sensíveis
- NUNCA transmitir tokens em parâmetros URL
- Header `Authorization: Bearer` apenas em HTTPS

**Rule 1.5 - Token Claims Validation**

- Validar `iss` (issuer) em todos os tokens
- Validar `aud` (audience) corresponde à aplicação
- Validar `exp` (expiration) antes de aceitar token
- Validar `nbf` (not before) se presente
- Rejeitar tokens com claims modificados
- Verificar assinatura digital do token

### **Password Security**

**Rule 1.6 - Password Hashing**

- Usar **bcrypt** ou **Argon2** para hashing (NUNCA MD5, SHA1, SHA256 simples)
- Salt individual por password (automático com bcrypt/Argon2)
- Custo mínimo bcrypt: **12** (ajustar conforme hardware)
- Argon2: usar configurações recomendadas OWASP
- NUNCA armazenar passwords em texto plano, mesmo temporariamente
- Opcional: hash adicional no client-side antes de transmissão

**Rule 1.7 - Password Policy**

- Comprimento mínimo: **12 caracteres** (recomendado: 16+)
- Complexidade obrigatória:
  - Mínimo 1 letra maiúscula
  - Mínimo 1 letra minúscula
  - Mínimo 1 número
  - Mínimo 1 caractere especial
- Verificar contra listas de passwords comuns (HaveIBeenPwned API)
- Rejeitar passwords que contenham username ou email
- Não forçar mudanças periódicas (recomendação NIST atual)

**Rule 1.8 - Password History**

- Manter histórico das últimas **5 passwords**
- Prevenir reutilização de passwords do histórico
- Armazenar hashes, NUNCA texto plano
- Limpar histórico em eliminação de conta
- Configurável por tenant (alguns podem requerer 10+)

**Rule 1.9 - Brute Force Protection**

- Rate limiting: **5 tentativas por 15 minutos** por IP
- Delays progressivos: 1s, 2s, 4s, 8s, 16s entre tentativas
- Bloqueio de conta após **10 tentativas falhadas**
- CAPTCHA após **3 tentativas falhadas**
- Alertar equipa de segurança em bloqueios repetidos
- Log de todas as tentativas falhadas com IP, timestamp, username

**Rule 1.10 - Multi-Factor Authentication (MFA)**

- MFA obrigatório para contas admin/privilegiadas
- Suporte a TOTP (Time-based One-Time Password)
- Suporte a SMS backup (apenas como fallback)
- Códigos de recuperação (8-10 códigos de uso único)
- Possibilidade de usar chaves de segurança (FIDO2/WebAuthn)
- Não permitir desativação de MFA por utilizadores normais (apenas admin)

### **Session Management**

**Rule 1.11 - Session Timeout**

- Timeout de inatividade: **30 minutos**
- Duração máxima de sessão: **24 horas** (forçar re-autenticação)
- Renovação automática em atividade do utilizador
- Aviso 5 minutos antes do timeout
- Configurável por tenant (alguns podem requerer mais restritivo)

**Rule 1.12 - Session Binding**

- Vincular sessão a endereço IP (opcional, configurável)
- Vincular sessão a User-Agent string
- Detetar e alertar tentativas de hijacking
- Opcional: forçar logout em mudança de IP (tenants high-security)
- Log de todos os bindings e validações

**Rule 1.13 - Session Audit Trail**

- Log de todos os inícios de sessão (login events)
- Log de todos os términos de sessão (logout events)
- Log de timeouts de sessão
- Registar IP, device info, localização (se disponível)
- Rastrear sessões concorrentes por utilizador
- Permitir utilizadores verem e revogarem sessões ativas

**Rule 1.14 - Multi-Device Sessions**

- Permitir múltiplas sessões concorrentes por utilizador
- Mostrar sessões ativas no perfil do utilizador
- Funcionalidade "logout de todos os dispositivos"
- Alertar utilizador em login de novo dispositivo
- Limite máximo de sessões concorrentes: **5 por utilizador**

**Rule 1.15 - OAuth 2.0 / OpenID Connect**

- Implementar OAuth 2.0 corretamente (Authorization Code Flow)
- Usar PKCE (Proof Key for Code Exchange) sempre
- Validar redirect_uri rigorosamente (whitelist exata)
- Não expor client_secret em aplicações públicas
- Usar state parameter para prevenir CSRF
- Implementar nonce em OpenID Connect

---

## 2. AUTHORIZATION & ACCESS CONTROL

### **Role-Based Access Control (RBAC)**

**Rule 2.1 - Permission Verification**

- Verificar permissões em **TODOS os endpoints** (exceto explicitamente públicos)
- Usar decorator pattern: `@require_permission('module.action')`
- Implementar verificação na camada controller E service (defesa em profundidade)
- Sem mecanismos de bypass em produção
- Log de todas as negações de permissão para auditoria

**Rule 2.2 - Principle of Least Privilege**

- **Negar por defeito** - conceder permissões explicitamente
- Utilizadores recebem permissões mínimas necessárias
- Escalação temporária de privilégios deve ser logged e time-limited
- Rever e revogar permissões não utilizadas trimestralmente
- Acesso admin requer passo de autenticação separado

**Rule 2.3 - Granular Permissions**

- Separar permissões READ e WRITE por recurso
- Permissões ao nível de campo para dados sensíveis
- Formato de permissão: `module.resource.action` (ex: `sales.invoice.create`)
- Suporte a wildcards: `sales.*` (usar com cautela)
- Permissões hierárquicas: parent implica children

**Rule 2.4 - Permission Audit**

- Log de todas as verificações de permissão (ALLOW e DENY)
- Incluir contexto: user_id, tenant_id, resource, action, IP
- Alertar em negações repetidas (potencial ataque)
- Revisão mensal de tentativas de acesso negadas
- Deteção automática de tentativas de escalação de privilégios

**Rule 2.5 - Django Groups & Permissions (Backend)**

- Usar Django Groups para organizar permissões
- Nunca atribuir permissões diretamente a utilizadores (usar grupos)
- Grupos pré-definidos: Admin, Manager, User, Guest
- Sincronizar permissões Django com sistema RBAC custom
- Migrar permissões em alterações de schema
- Documentar cada grupo e suas permissões

**Rule 2.6 - Django Admin Security**

- Django Admin APENAS acessível a superusers
- URL do admin customizado (não usar `/admin/`)
- MFA obrigatório para acesso ao Django Admin
- IP whitelist para acesso ao admin (opcional)
- Log de todas as ações no Django Admin
- Desativar admin em produção se não necessário

### **Field-Level Security**

**Rule 2.7 - Sensitive Field Protection**

- Identificar campos sensíveis: password, SSN, credit_card, salary, medical_data
- Encriptar campos sensíveis at rest (AES-256)
- Mascarar dados sensíveis em logs: `****1234` para cartões
- Redação de campos sensíveis em exports (configurável)
- Permissões separadas para visualização vs edição de campos sensíveis

**Rule 2.8 - Data Redaction**

- Redação automática em audit logs
- Regras de redação configuráveis por tenant
- Redação em mensagens de erro e stack traces
- Export GDPR-compliant (excluir sensíveis a menos que explicitamente pedido)
- Revelação parcial com multi-factor authentication

### **AI Agent Permissions**

**Rule 2.9 - AI Agent Authorization**

- Agentes IA requerem permissões explícitas (tabela `ai_agent_permissions`)
- Princípio de menor privilégio aplica-se a agentes IA
- Rate limiting por agente: **100 ações/hora**
- Aprovação humana obrigatória para ações HIGH RISK
- Audit trail inclui raciocínio e processo de decisão da IA

**Rule 2.10 - AI Autonomy Levels**

- **Nível 1 (Supervisionado):** Todas as ações requerem aprovação humana
- **Nível 2 (Semi-Autónomo):** Ações baixo risco automáticas, outras precisam aprovação
- **Nível 3 (Autónomo):** Todas as ações automáticas exceto CRÍTICAS
- Configurável por tenant e por agente
- Downgrade automático em erros repetidos (>5 falhas → Nível 1)

**Rule 2.11 - AI Action Validation**

- Validar ações geradas por IA antes de execução
- Score de risco para todas as ações IA (LOW/MEDIUM/HIGH/CRITICAL)
- Threshold de confiança: mínimo **80%** para ações autónomas
- Mecanismo de rollback para ações IA
- Override humano possível para todas as decisões IA

---

## 3. DATA PROTECTION & ENCRYPTION

### **Encryption at Rest**

**Rule 3.1 - Database Encryption**

- Encriptação completa da base de dados usando **AES-256**
- Encriptar volumes de disco (LUKS para Linux, BitLocker para Windows)
- Cloud providers: usar encriptação nativa (AWS EBS, Azure Disk Encryption)
- Chaves de encriptação separadas por tenant (feature enterprise)
- Rotação de chaves a cada **180 dias**

**Rule 3.2 - Field-Level Encryption**

- Encriptar campos específicos sensíveis (além de DB encryption)
- Usar `django-encrypted-model-fields` ou similar
- Chaves armazenadas em secrets manager (nunca em código)
- Encriptar antes de escrever, desencriptar ao ler
- Índices não podem usar campos encriptados diretamente

**Rule 3.3 - File Encryption**

- Encriptar ficheiros sensíveis antes de armazenar
- Formato recomendado: AES-256-GCM
- Chaves únicas por ficheiro (ou por tenant)
- Metadados de encriptação armazenados separadamente
- Desencriptar apenas quando necessário (just-in-time)

### **Encryption in Transit**

**Rule 3.4 - HTTPS Everywhere**

- **HTTPS obrigatório** em todos os ambientes (incluindo dev)
- TLS 1.2 mínimo (TLS 1.3 recomendado)
- Certificados válidos e não expirados
- HSTS (HTTP Strict Transport Security) ativado
- Redirect automático HTTP → HTTPS
- Desativar TLS 1.0 e 1.1 completamente

**Rule 3.5 - Certificate Management**

- Certificados Let's Encrypt com renovação automática
- Ou certificados comerciais de CA confiável
- Monitorizar expiração de certificados (alertas 30 dias antes)
- Usar wildcard certificates ou SANs para subdomínios
- Certificate pinning em apps móveis (opcional)

**Rule 3.6 - Internal Communications**

- Comunicações inter-serviços também em TLS
- Mutual TLS (mTLS) para serviços críticos
- Encriptar mensagens de queue (Redis, RabbitMQ)
- VPN para acesso a recursos internos
- Nunca transmitir dados sensíveis em plaintext

### **Key Management**

**Rule 3.7 - Key Storage**

- NUNCA armazenar chaves no código fonte
- Usar secrets manager (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault)
- Chaves em `.env` ficheiro (dev local apenas)
- Diferentes chaves por ambiente
- Acesso a chaves limitado (least privilege)

**Rule 3.8 - Key Rotation**

- Rotação automática de chaves a cada **180 dias**
- Re-encriptação de dados com nova chave
- Manter chave antiga até re-encriptação completa
- Log de todas as rotações de chaves
- Testar processo de rotação regularmente

**Rule 3.9 - Key Backup & Recovery**

- Backup seguro de master keys
- Armazenar em localização física separada
- Processo de recuperação de chaves documentado
- Testar recuperação anualmente
- Multi-person control para acesso a backups de chaves

---

## 4. INPUT VALIDATION & INJECTION PREVENTION

### **General Input Validation**

**Rule 4.1 - Server-Side Validation**

- **SEMPRE validar no servidor** (client-side é apenas UX)
- Validar tipo, formato, comprimento, range
- Whitelist > Blacklist (aceitar apenas o esperado)
- Rejeitar input inválido com mensagem clara
- Log de tentativas de input malicioso

**Rule 4.2 - Data Type Validation**

- Usar type hints em Python (`str`, `int`, `datetime`, etc)
- Validação com Pydantic para APIs
- Django forms/serializers para validação
- Rejeitar tipos inesperados
- Conversão segura de tipos

**Rule 4.3 - Length & Range Validation**

- Definir comprimento máximo para todos os inputs
- Validar ranges numéricos
- Prevenir DoS por inputs enormes
- Validar tamanho de ficheiros upload
- Limitar número de elementos em arrays/listas

**Rule 4.4 - Format Validation**

- Regex para formatos específicos (email, telefone, zip code, etc)
- Validar estrutura de JSON/XML
- Rejeitar caracteres especiais onde não esperados
- Validar encoding (UTF-8 apenas, normalmente)
- Normalização de input (trim, lowercase, etc)

### **SQL Injection Prevention**

**Rule 4.5 - ORM Only (Django)**

- **SEMPRE usar Django ORM** (NUNCA raw SQL concatenado)
- Se raw SQL necessário: usar `.raw()` com parâmetros
- Ou usar `.execute()` com placeholders `%s`
- NUNCA concatenar strings em queries SQL
- Escapar input mesmo quando usando ORM (paranoia)

**Rule 4.6 - Query Parameterization**

- Usar placeholders em queries: `WHERE id = %s`
- NUNCA f-strings ou formatação direta em SQL
- Django ORM já faz isto automaticamente
- Validar tipos antes de passar para query
- Log de queries suspeitas

**Rule 4.7 - Stored Procedures Security**

- Se usar stored procedures: validar inputs
- Não confiar em stored procedures para validação apenas
- Aplicar princípio de menor privilégio a DB users
- Auditar stored procedures regularmente

### **NoSQL Injection Prevention**

**Rule 4.8 - NoSQL Query Safety**

- NUNCA construir queries NoSQL com concatenação
- Usar métodos seguros da library (ex: `find({})` vs `eval()`)
- Validar tipos antes de usar em queries
- Sanitizar input JSON
- Rejeitar operadores MongoDB em input (`$where`, `$regex`, etc)

**Rule 4.9 - MongoDB Specific**

- Desativar `mapReduce` se não necessário
- Usar `$expr` com cuidado
- Validar regex patterns de utilizadores
- Rate limiting em queries complexas

### **Command Injection Prevention**

**Rule 4.10 - Avoid System Commands**

- **NUNCA executar comandos do sistema com input do utilizador**
- Usar bibliotecas Python em vez de shell commands
- Se inevitável: usar `subprocess` com lista de args (não string)
- Whitelist de comandos permitidos
- Sanitização extrema de argumentos

**Rule 4.11 - Shell Injection**

- NUNCA usar `os.system()` ou `shell=True` em subprocess
- Escapar todos os caracteres especiais shell
- Validar paths de ficheiros rigorosamente
- Usar bibliotecas específicas (ex: `PIL` para imagens vs `imagemagick`)

### **XSS Prevention (Frontend)**

**Rule 4.12 - Output Encoding**

- Escapar HTML em todos os outputs
- Vue.js faz isto por defeito com `{{ }}` (usar `v-text` em vez de `v-html`)
- Apenas usar `v-html` com conteúdo 100% confiável
- Sanitizar HTML com biblioteca (DOMPurify)
- Encoding específico por contexto (HTML, JS, URL, CSS)

**Rule 4.13 - Content Security Policy (CSP)**

- Header CSP configurado restritivamente
- `default-src 'self'`
- `script-src 'self'` (sem `'unsafe-inline'` ou `'unsafe-eval'`)
- `style-src 'self'` (permitir `'unsafe-inline'` só se necessário)
- `img-src 'self' data: https:`
- Reportar violações CSP para monitorização

**Rule 4.14 - DOM-based XSS Prevention**

- NUNCA usar `innerHTML` com dados não confiáveis
- Evitar `eval()`, `Function()`, `setTimeout(string)`
- Sanitizar URLs antes de usar em `location.href`
- Validar e sanitizar query parameters
- Usar `textContent` em vez de `innerHTML`

### **LDAP/XML Injection Prevention**

**Rule 4.15 - LDAP Injection**

- Escapar caracteres especiais LDAP: `*()\ /`
- Usar bibliotecas que fazem escaping automático
- Validar input antes de usar em queries LDAP
- Whitelist de caracteres permitidos

**Rule 4.16 - XML Injection (XXE)**

- Desativar entidades externas em parsers XML
- Usar `defusedxml` em Python
- Validar estrutura XML rigorosamente
- Limitar tamanho de XML processado
- NUNCA processar XML de fontes não confiáveis sem validação

---

## 5. API SECURITY

### **API Authentication**

**Rule 5.1 - API Key Management**

- API keys únicas por cliente/aplicação
- NUNCA reutilizar API keys
- Armazenar hashes de API keys (não plaintext)
- Rotação de API keys a cada **90 dias**
- Revogar keys comprometidas imediatamente

**Rule 5.2 - API Key Transmission**

- API keys em header `Authorization: Bearer <key>`
- NUNCA em URL query parameters
- NUNCA em request body (a menos que POST para criar key)
- HTTPS obrigatório
- Rate limiting por API key

**Rule 5.3 - OAuth for API Access**

- Preferir OAuth 2.0 em vez de API keys
- Scopes granulares (read, write, admin)
- Tokens de curta duração
- Refresh tokens para renovação
- Revogar tokens em logout

### **API Rate Limiting**

**Rule 5.4 - Global Rate Limiting**

- Rate limit global: **100 requests/minuto** (ajustar conforme necessário)
- Por IP, por utilizador, ou por API key
- Usar Redis para contadores distribuídos
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- Retornar HTTP 429 quando limite excedido

**Rule 5.5 - Endpoint-Specific Rate Limiting**

- Endpoints sensíveis: **10 requests/minuto**
- Login endpoint: **5 tentativas/15 minutos**
- Search endpoints: **30 requests/minuto**
- Bulk operations: **5 requests/hora**
- Configurável por tenant

**Rule 5.6 - Rate Limit Bypass Protection**

- Rate limiting também por IP (além de user/key)
- Detetar e bloquear distributed attacks
- CAPTCHA em limite excedido repetidamente
- Alertar equipa em ataques de grande escala
- Whitelist de IPs confiáveis (com cautela)

### **API Input/Output**

**Rule 5.7 - Request Validation**

- Validar Content-Type header
- Validar tamanho do request body (max 10MB por defeito)
- Schema validation com Pydantic/Marshmallow
- Rejeitar campos extras não esperados
- Validar tipos de dados rigorosamente

**Rule 5.8 - Response Security**

- NUNCA expor stack traces em produção
- Mensagens de erro genéricas para utilizadores
- Log detalhado apenas em servidor
- Remover headers sensíveis (`X-Powered-By`, `Server`)
- Adicionar security headers (CSP, X-Frame-Options, etc)

**Rule 5.9 - API Versioning**

- Versionar APIs: `/api/v1/`, `/api/v2/`
- Manter retrocompatibilidade por **1 ano**
- Deprecation warnings nas versões antigas
- Documentar breaking changes claramente
- Forçar upgrade eventualmente (após aviso)

### **API Documentation Security**

**Rule 5.10 - Swagger/OpenAPI Security**

- Documentação automática com Swagger/OpenAPI
- **Desativar Swagger em produção** (ou proteger com autenticação)
- Não expor endpoints internos/debug
- Exemplos sem dados sensíveis reais
- Schemas de segurança documentados (JWT, OAuth, etc)

**Rule 5.11 - API Documentation Access**

- Documentação apenas acessível a utilizadores autenticados
- Ou endpoint público com informação limitada
- Nunca expor configurações internas
- Redaction de secrets em exemplos
- Versão pública vs versão interna da documentação

### **CORS Configuration**

**Rule 5.12 - CORS Policy**

- CORS configurado restritivamente
- Whitelist explícita de origens permitidas
- NUNCA usar `Access-Control-Allow-Origin: *` em produção
- `Access-Control-Allow-Credentials: true` apenas quando necessário
- Validar Origin header no servidor

**Rule 5.13 - Preflight Requests**

- Responder corretamente a OPTIONS requests
- Configurar `Access-Control-Allow-Methods` restritivamente
- `Access-Control-Allow-Headers` apenas para headers necessários
- `Access-Control-Max-Age` para cache de preflight (ex: 86400)

---

## 6. FRONTEND SECURITY

### **Client-Side Security**

**Rule 6.1 - Sensitive Data in Frontend**

- **NUNCA armazenar dados sensíveis em localStorage**
- NUNCA armazenar tokens em localStorage (usar httpOnly cookies)
- Limpar dados sensíveis da memória após uso
- Não armazenar passwords mesmo que hasheadas
- Session storage preferível a localStorage (limpa ao fechar browser)

**Rule 6.2 - Client-Side Validation**

- Validação client-side é apenas para UX
- NUNCA confiar apenas em validação client-side
- Sempre re-validar no servidor
- Mensagens de erro claras mas sem detalhes sensíveis
- Feedback instantâneo ao utilizador

**Rule 6.3 - Third-Party Scripts**

- Minimizar uso de scripts third-party
- Usar Subresource Integrity (SRI) para CDN scripts
- `<script src="..." integrity="sha384-..." crossorigin="anonymous">`
- Auditar scripts third-party regularmente
- CSP para controlar fontes de scripts permitidas

**Rule 6.4 - Frontend Build Security**

- Minificar e obfuscar código JavaScript
- Remover source maps em produção
- Webpack/Vite com configuração de produção segura
- Tree shaking para remover código não usado
- Verificar dependencies com `npm audit` ou `yarn audit`

### **Vue.js Specific Security**

**Rule 6.5 - Vue.js XSS Prevention**

- Usar `{{ }}` ou `v-text` para output (escapa automaticamente)
- **EVITAR `v-html`** a todo custo
- Se `v-html` necessário: sanitizar com DOMPurify primeiro
- Nunca usar `v-html` com input do utilizador
- `v-bind:href` com URLs validadas apenas

**Rule 6.6 - Vue.js Lifecycle Security**

- Limpar event listeners em `beforeUnmount`
- Cancelar timers/intervals em `beforeUnmount`
- Limpar subscriptions WebSocket/SSE
- Evitar memory leaks
- Não armazenar dados sensíveis em `this.$root` ou `this.$parent`

**Rule 6.7 - Vue Router Security**

- Guards de navegação para autenticação
- `beforeEach` para verificar permissões
- Redirect para login se não autenticado
- Validar parâmetros de rota
- Prevenir navigation timing attacks

**Rule 6.8 - Vuex/Pinia Security**

- NUNCA armazenar tokens/passwords no Vuex/Pinia
- Limpar state em logout
- Não persistir state sensível em localStorage
- Mutations/Actions com validação
- Módulos separados por contexto de segurança

### **Single Page Application (SPA) Security**

**Rule 6.9 - SPA Authentication Flow**

- Token refresh automático antes de expirar
- Redirect para login em 401 Unauthorized
- Proteção de rotas com guards
- Estado de autenticação global (Vuex/Pinia)
- Deep linking seguro (não expor estado sensível na URL)

**Rule 6.10 - Client-Side Routing**

- NUNCA confiar em client-side routing para segurança
- Backend deve validar todas as permissões
- Frontend routing é apenas UX
- Proteger rotas de admin no frontend (mas sempre validar backend)
- Prevenir acesso direto por URL manipulation

---

## 7. BACKEND SECURITY (DJANGO SPECIFIC)

### **Django Settings Security**

**Rule 7.1 - DEBUG Mode**

- **DEBUG = False em produção** (CRÍTICO)
- DEBUG = True apenas em desenvolvimento local
- NUNCA commitar DEBUG = True
- CI/CD deve verificar DEBUG = False antes de deploy
- Logs detalhados em vez de DEBUG mode

**Rule 7.2 - SECRET_KEY**

- SECRET_KEY em `.env`, NUNCA no código
- SECRET_KEY diferente por ambiente
- Comprimento mínimo 50 caracteres aleatórios
- Rotação a cada **180 dias**
- Gerar com `django.core.management.utils.get_random_secret_key()`

**Rule 7.3 - ALLOWED_HOSTS**

- ALLOWED_HOSTS configurado explicitamente
- NUNCA usar `['*']` em produção
- Lista exata de domínios permitidos
- Incluir subdomínios se necessário
- Validar host header em middleware

**Rule 7.4 - CSRF Protection**

- `django.middleware.csrf.CsrfViewMiddleware` ativado
- CSRF token em todos os forms
- `@csrf_protect` em views específicas
- `@csrf_exempt` apenas quando absolutamente necessário (e documentar porquê)
- CSRF cookie com `Secure` e `SameSite`

**Rule 7.5 - SECURE Settings**

- `SECURE_SSL_REDIRECT = True` (redirect HTTP → HTTPS)
- `SESSION_COOKIE_SECURE = True`
- `CSRF_COOKIE_SECURE = True`
- `SECURE_HSTS_SECONDS = 31536000` (1 ano)
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- `SECURE_HSTS_PRELOAD = True`
- `SECURE_CONTENT_TYPE_NOSNIFF = True`
- `SECURE_BROWSER_XSS_FILTER = True`
- `X_FRAME_OPTIONS = 'DENY'` ou `'SAMEORIGIN'`

### **Django ORM Security**

**Rule 7.6 - ORM Usage**

- **SEMPRE usar Django ORM** para queries
- NUNCA concatenar strings em raw SQL
- Usar `.filter(id=user_input)` não `.raw(f"SELECT * WHERE id={user_input}")`
- Se raw SQL necessário: `.raw('SELECT * WHERE id = %s', [user_input])`
- Ou `.execute()` com placeholders

**Rule 7.7 - Query Optimization**

- Usar `select_related()` e `prefetch_related()` para evitar N+1
- Índices em campos frequentemente consultados
- `only()` e `defer()` para carregar apenas campos necessários
- EXPLAIN queries lentas
- Rate limiting em queries pesadas

**Rule 7.8 - Model Validation**

- Validação em `clean()` methods
- Constraints de base de dados (unique, check, etc)
- Validação de tipos com model fields
- Custom validators para regras complexas
- Não confiar apenas em validação de forms

### **Django Middleware Security**

**Rule 7.9 - Security Middleware**

- `SecurityMiddleware` ativado (primeiro na lista)
- `SessionMiddleware` ativado
- `CsrfViewMiddleware` ativado
- `AuthenticationMiddleware` ativado
- `XFrameOptionsMiddleware` ativado
- Custom middleware para logging de segurança

**Rule 7.10 - Custom Middleware**

- Middleware de tenant isolation (multi-tenant)
- Middleware de rate limiting
- Middleware de audit logging
- Validar ordem de middleware (ordem importa)
- Testar middleware em desenvolvimento

### **Django Authentication**

**Rule 7.11 - User Model**

- Usar AbstractBaseUser ou AbstractUser
- NUNCA usar User model default do Django diretamente em produção
- Custom User model com campos adicionais
- Email como username (opcional, mas recomendado)
- Soft delete de utilizadores (manter audit trail)

**Rule 7.12 - Password Validators**

- `AUTH_PASSWORD_VALIDATORS` configurado:
  - `UserAttributeSimilarityValidator`
  - `MinimumLengthValidator` (min 12)
  - `CommonPasswordValidator`
  - `NumericPasswordValidator`
- Custom validators se necessário
- Feedback claro ao utilizador

**Rule 7.13 - Permission System**

- Usar Django permissions integradas
- Custom permissions quando necessário
- Grupos para organizar permissões
- NUNCA atribuir permissões diretamente a utilizadores (usar grupos)
- Sincronizar permissões em migrações

### **Django Admin Security**

**Rule 7.14 - Admin Site Protection**

- URL do admin customizado (não `/admin/`)
- Admin apenas acessível a superusers
- MFA obrigatório para acesso ao admin
- IP whitelist (opcional)
- HTTPS obrigatório
- Desativar admin em produção se não usado

**Rule 7.15 - Admin Actions Security**

- Validar ações em massa
- Confirmação para ações destrutivas
- Log de todas as ações de admin
- Limitar ações disponíveis por grupo
- Não permitir ações perigosas sem MFA

### **Django REST Framework Security**

**Rule 7.16 - DRF Authentication**

- `DEFAULT_AUTHENTICATION_CLASSES` configurado
- JWT authentication recomendado
- Session authentication apenas para browsable API (dev)
- Múltiplos authentication backends possíveis
- Fallback para anonymous user se configurado

**Rule 7.17 - DRF Permissions**

- `DEFAULT_PERMISSION_CLASSES` configurado
- NUNCA usar `AllowAny` em produção (exceto endpoints públicos explícitos)
- `IsAuthenticated` como mínimo
- Custom permissions para lógica complexa
- Permissions granulares por viewset/action

**Rule 7.18 - DRF Throttling**

- `DEFAULT_THROTTLE_CLASSES` configurado
- `AnonRateThrottle` e `UserRateThrottle`
- Rates por endpoint (ex: login mais restritivo)
- Throttling por IP e por utilizador
- Custom throttle classes se necessário

**Rule 7.19 - DRF Serializer Security**

- Validação em serializers
- `read_only_fields` para campos que não devem ser editáveis
- `write_only_fields` para campos sensíveis (ex: password)
- NUNCA expor campos sensíveis inadvertidamente
- Serializers diferentes para read vs write

---

## 8. DATABASE SECURITY

### **Database Access Control**

**Rule 8.1 - Database Users**

- User diferente por aplicação/serviço
- Princípio de menor privilégio
- User de aplicação: APENAS SELECT, INSERT, UPDATE, DELETE (não DROP, CREATE)
- User de admin: acesso completo (usar raramente)
- User de backup: apenas SELECT
- User de migração: DDL rights (CREATE, ALTER, DROP)

**Rule 8.2 - Database Authentication**

- Passwords fortes para database users
- NUNCA usar user 'root' ou 'postgres' em aplicação
- Autenticação via certificados (opcional)
- Renovação de passwords a cada **90 dias**
- Armazenar credentials em secrets manager

**Rule 8.3 - Connection Security**

- Conexões via SSL/TLS
- Certificados validados
- Conexões apenas de IPs whitelisted
- Firewall configurado (apenas portas necessárias)
- VPN para acesso externo ao database

### **PostgreSQL Specific**

**Rule 8.4 - PostgreSQL Configuration**

- `pg_hba.conf` configurado restritivamente
- SSL mode: `require` ou `verify-full`
- `listen_addresses` apenas para IPs necessários (não `*`)
- `max_connections` limitado (prevenir DoS)
- Logs de conexões e queries (para auditoria)

**Rule 8.5 - PostgreSQL Roles & Permissions**

- Usar ROLES em vez de USERS diretos
- GRANT mínimo necessário
- REVOKE permissões não usadas
- Schemas separados para multi-tenancy (opcional)
- Row-level security (RLS) para isolamento tenant

**Rule 8.6 - PostgreSQL Extensions**

- Apenas instalar extensões necessárias
- Auditar extensões third-party
- Atualizar extensões regularmente
- Desativar extensões não usadas
- Documentar porquê cada extensão é necessária

### **Database Backups**

**Rule 8.7 - Backup Frequency**

- Backups automáticos **diários**
- Backups incrementais (se possível)
- Backups antes de migrações major
- Testar backups mensalmente (restore test)
- Retenção: **30 dias** (ajustar conforme compliance)

**Rule 8.8 - Backup Security**

- Encriptar backups (AES-256)
- Armazenar em localização geograficamente separada
- Acesso a backups limitado (MFA obrigatório)
- Logs de acesso a backups
- Validar integridade de backups

**Rule 8.9 - Backup Restoration**

- Processo de restauro documentado
- Testar restauro em ambiente staging
- RTO (Recovery Time Objective): **< 4 horas**
- RPO (Recovery Point Objective): **< 24 horas**
- Equipa treinada em procedimento de disaster recovery

### **Database Monitoring**

**Rule 8.10 - Query Monitoring**

- Log de queries lentas (> 1 segundo)
- Análise de query performance semanal
- Índices para queries frequentes
- EXPLAIN queries problemáticas
- Alertas em queries excepcionalmente lentas

**Rule 8.11 - Connection Monitoring**

- Monitorizar número de conexões ativas
- Alertas em picos de conexões
- Connection pooling (PgBouncer, Django DB pool)
- Timeout de conexões idle
- Logs de conexões rejeitadas

---

## 9. MULTI-TENANT ISOLATION

### **Tenant Data Isolation**

**Rule 9.1 - Tenant ID Verification**

- **SEMPRE verificar tenant_id em TODAS as queries**
- Middleware de tenant injection
- Queries automáticas com `filter(tenant_id=current_tenant)`
- NUNCA confiar em tenant_id do frontend
- Validação em múltiplas camadas (middleware, ORM, service)

**Rule 9.2 - Tenant-Specific Resources**

- Isolation de ficheiros por tenant
- Subdomínios por tenant (opcional): `tenant1.app.com`
- Databases separadas por tenant (opcional, enterprise)
- Schemas PostgreSQL separados por tenant (alternativa)
- Rate limiting por tenant

**Rule 9.3 - Cross-Tenant Data Leakage**

- Prevenir queries cross-tenant
- Testar com tentativas de acesso cross-tenant
- Audit logs para detetar acessos suspeitos
- Alerts em tentativas cross-tenant
- Pentest focado em multi-tenancy

**Rule 9.4 - Shared Resources**

- Identificar recursos shared (ex: user authentication)
- Documentar o que é shared vs isolado
- Validação rigorosa em recursos shared
- Evitar leakage via recursos shared
- Caching isolado por tenant

### **Tenant Management**

**Rule 9.5 - Tenant Provisioning**

- Processo automático de criação de tenant
- Validação de domínio/subdomain único
- Setup de permissões default
- Logs de criação de tenants
- Trial period configurável

**Rule 9.6 - Tenant Suspension/Deletion**

- Soft delete de tenants (manter dados por período)
- Hard delete após período de retenção (GDPR compliance)
- Notificação antes de deletion
- Backup antes de delete
- Restore possível dentro de período

---

## 10. AI SECURITY & MODEL PROTECTION

### **AI Model Security**

**Rule 10.1 - Model Access Control**

- Modelos IA apenas acessíveis via API autenticada
- Rate limiting em chamadas ao modelo (100/hora por user)
- Logs de todas as inferências
- Versionamento de modelos
- Rollback rápido em caso de modelo comprometido

**Rule 10.2 - Model Confidentiality**

- Modelos proprietários encriptados at rest
- Acesso ao modelo limitado (least privilege)
- Não expor pesos do modelo publicamente
- API inference apenas (não dar modelo aos users)
- Proteção contra model stealing attacks

**Rule 10.3 - Training Data Security**

- Dados de treino encriptados at rest
- Acesso a dados de treino restrito
- Anonimização de dados sensíveis antes de treino
- GDPR compliance em dados de treino
- Logs de acesso a training datasets

**Rule 10.4 - Model Versioning & Rollback**

- Versionamento de modelos (v1, v2, etc)
- Rollback rápido para versão anterior
- Testes em staging antes de deploy de novo modelo
- A/B testing de modelos
- Monitorização de performance pós-deploy

### **Prompt Injection Prevention**

**Rule 10.5 - Input Sanitization for AI**

- Sanitizar prompts de utilizadores
- Remover/escapar comandos especiais
- Validar comprimento de prompts
- Rejeitar prompts maliciosos (patterns conhecidos)
- Rate limiting em prompts

**Rule 10.6 - Prompt Engineering Security**

- System prompts protegidos (não editáveis por utilizadores)
- Separação clara entre system prompt e user input
- Validação de output do modelo
- Filtragem de respostas inadequadas
- Logs de prompts e respostas para auditoria

**Rule 10.7 - Jailbreak Prevention**

- Deteção de tentativas de jailbreak
- Blacklist de patterns conhecidos de jailbreak
- Rate limiting agressivo em tentativas de jailbreak
- Bloqueio de utilizadores que tentam jailbreak repetidamente
- Logs e alertas de tentativas de jailbreak

### **AI Output Validation**

**Rule 10.8 - Output Content Filtering**

- Filtrar conteúdo sensível/inadequado em outputs IA
- Validar que output está dentro de scope esperado
- Rejeitar outputs com informação sensível (ex: números de cartão)
- Classificação de risco de outputs
- Human-in-the-loop para outputs HIGH RISK

**Rule 10.9 - Bias & Fairness Monitoring**

- Monitorizar outputs para bias
- Métricas de fairness
- Alertas em desvios de fairness
- Re-treino de modelos enviesados
- Documentação de limitações conhecidas

**Rule 10.10 - Hallucination Detection**

- Validação de factos quando possível
- Confidence scores em outputs
- Disclaim que IA pode errar
- Fact-checking automático (quando aplicável)
- Feedback loop para melhorar modelo

### **AI Agent Security**

**Rule 10.11 - Agent Permissions (ver também Rule 2.9-2.11)**

- Agentes IA com permissões explícitas
- Autonomy levels configuráveis
- Approval humana para HIGH RISK actions
- Rollback de ações IA
- Audit trail completo de decisões

**Rule 10.12 - Agent Rate Limiting**

- Limite de ações por hora por agente
- Cooling period após erros
- Downgrade de autonomy em falhas repetidas
- Alertas em atividade anormal
- Circuit breaker pattern

---

## 11. MOBILE SECURITY

### **Mobile App Security**

**Rule 11.1 - Secure Storage (Mobile)**

- NUNCA armazenar tokens em SharedPreferences/UserDefaults plaintext
- Usar Keychain (iOS) ou Keystore (Android)
- Encriptar dados sensíveis localmente
- Limpar dados em logout
- Ofuscar código (ProGuard, R8)

**Rule 11.2 - Certificate Pinning**

- Implementar certificate pinning
- Prevenir man-in-the-middle attacks
- Pins com backup (múltiplos certificados)
- Atualizar pins em app updates
- Fallback seguro se pinning falhar

**Rule 11.3 - Jailbreak/Root Detection**

- Detetar dispositivos jailbroken/rooted
- Aviso ao utilizador (não bloquear necessariamente)
- Funcionalidades sensíveis bloqueadas em dispositivos comprometidos
- Logs de deteção
- Bypass detection também implementado (defense in depth)

**Rule 11.4 - Mobile API Security**

- Autenticação em todas as chamadas API
- Refresh token automático
- Timeout de sessão
- Biometric authentication (opcional)
- Deep link validation

---

## 12. INFRASTRUCTURE & NETWORK SECURITY

### **Network Security**

**Rule 12.1 - Firewall Configuration**

- Firewall ativado em todos os servidores
- Apenas portas necessárias abertas (80, 443, 22)
- SSH apenas de IPs whitelisted
- Rate limiting em firewall
- Logs de tentativas de conexão bloqueadas

**Rule 12.2 - DDoS Protection**

- Cloudflare ou similar para proteção DDoS
- Rate limiting agressivo
- IP blacklisting automático
- Geographic blocking se necessário
- Scaling automático sob ataque

**Rule 12.3 - VPN for Internal Access**

- VPN obrigatório para acesso a recursos internos
- MFA em VPN
- Logs de conexões VPN
- Desconexão automática após inatividade
- Split tunneling desativado

### **Server Hardening**

**Rule 12.4 - OS Security**

- Sistema operacional atualizado (patches de segurança)
- Serviços desnecessários desativados
- Fail2ban ou similar para proteção brute force
- SELinux/AppArmor ativado
- Logs centralizados

**Rule 12.5 - SSH Security**

- SSH key-based authentication (não passwords)
- Root login desativado
- Port knocking ou port não-standard (opcional)
- Fail2ban para tentativas falhadas
- Logs de todas as sessões SSH

**Rule 12.6 - Container Security**

- Imagens Docker de fontes confiáveis
- Scan de vulnerabilidades em imagens (Trivy, Clair)
- Non-root user em containers
- Read-only filesystem quando possível
- Secrets em runtime (não em imagem)

### **Cloud Security**

**Rule 12.7 - Cloud IAM**

- Princípio de menor privilégio
- MFA obrigatório
- Roles específicos por função
- Rotação de access keys
- Audit logs de ações IAM

**Rule 12.8 - Cloud Network**

- VPC isolada por ambiente
- Security groups restritivos
- NACLs para defesa em profundidade
- VPC peering apenas quando necessário
- VPN ou Direct Connect para on-premise

**Rule 12.9 - Cloud Storage**

- Buckets S3 com ACLs restritivas (não public)
- Encryption at rest ativada
- Versioning ativado
- Lifecycle policies para data retention
- Logs de acesso a buckets

---

## 13. SECRETS MANAGEMENT

### **Secret Storage**

**Rule 13.1 - Environment Variables**

- Secrets em `.env` ficheiro (dev local)
- `.env` excluído do Git (`.gitignore`)
- Diferentes `.env` por ambiente
- NUNCA commitar secrets
- Template `.env.example` com placeholders

**Rule 13.2 - Secrets Manager**

- Usar secrets manager em produção (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault)
- Secrets injetados em runtime
- Rotação automática de secrets
- Audit logs de acesso a secrets
- Encryption at rest no secrets manager

**Rule 13.3 - CI/CD Secrets**

- Secrets em GitHub Secrets, GitLab CI/CD Variables
- NUNCA em código ou logs
- Masked em outputs de CI/CD
- Rotação após mudança de equipa
- Scoped por ambiente

### **Secret Rotation**

**Rule 13.4 - Rotation Schedule**

- Database passwords: **90 dias**
- API keys: **90 dias**
- Encryption keys: **180 dias**
- JWT secrets: **90 dias**
- Alertas antes de expiração

**Rule 13.5 - Rotation Process**

- Automático quando possível
- Zero-downtime rotation
- Rollback plan
- Validação pós-rotação
- Logs de rotações

---

## 14. FILE UPLOAD & STORAGE SECURITY

### **File Upload Validation**

**Rule 14.1 - File Type Validation**

- Whitelist de extensões permitidas
- Validar MIME type (não confiar apenas em extensão)
- Validar magic bytes (file signature)
- Rejeitar executáveis (.exe, .sh, .bat, etc)
- Validação server-side (não apenas client-side)

**Rule 14.2 - File Size Limits**

- Limite de tamanho por ficheiro (ex: 10MB)
- Limite total de uploads por utilizador
- Validação antes de processar
- Rejeitar ficheiros vazios
- Prevenir DoS por uploads grandes

**Rule 14.3 - Filename Sanitization**

- Sanitizar nomes de ficheiros
- Remover caracteres especiais
- Prevenir path traversal (`../`, etc)
- Gerar nomes únicos (UUID)
- NUNCA usar filename do utilizador diretamente

### **File Storage**

**Rule 14.4 - Storage Location**

- Ficheiros fora de webroot
- Acesso via aplicação (não direto)
- URLs assinadas com expiração
- Isolamento por tenant
- Backups de ficheiros

**Rule 14.5 - Malware Scanning**

- Scan antivírus em uploads
- Quarentena de ficheiros suspeitos
- Integração com ClamAV ou similar
- Alertas em malware detetado
- Bloqueio de utilizadores que fazem upload de malware repetidamente

---

## 15. THIRD-PARTY INTEGRATIONS

### **API Integration Security**

**Rule 15.1 - Third-Party API Keys**

- API keys em secrets manager
- NUNCA no código
- Diferentes keys por ambiente
- Rotação regular
- Revogação imediata se comprometidas

**Rule 15.2 - Webhook Security**

- Validar signatures de webhooks
- HTTPS obrigatório para webhooks
- Verificar IP source (whitelist)
- Rate limiting em webhook endpoints
- Logs de webhooks recebidos

**Rule 15.3 - OAuth Integration**

- Validar redirect_uri rigorosamente
- Usar state parameter (anti-CSRF)
- Validar scopes recebidos
- Revogar tokens não usados
- Logs de autorizações OAuth

---

## 16. LOGGING, MONITORING & INCIDENT RESPONSE

### **Security Logging**

**Rule 16.1 - Event Logging**

- Log de todos os eventos de segurança:
  - Login/logout
  - Alterações de permissões
  - Acessos a dados sensíveis
  - Ações administrativas
  - Tentativas falhadas de autenticação
  - Violações de rate limiting

**Rule 16.2 - Log Content**

- Incluir: timestamp, user_id, IP, action, resource, result
- NUNCA logar passwords ou tokens
- Redact dados sensíveis automaticamente
- Structured logging (JSON)
- Correlation IDs para rastreamento

**Rule 16.3 - Log Storage & Retention**

- Logs imutáveis (write-only)
- Centralizados (ELK, Splunk, CloudWatch, etc)
- Encriptados at rest
- Retenção: **90 dias** (ou conforme compliance)
- Backups de logs críticos

**Rule 16.4 - Log Monitoring**

- Alertas em eventos críticos
- Dashboard de segurança
- Análise automática de anomalias
- SIEM (Security Information and Event Management)
- Response playbooks

### **Incident Response**

**Rule 16.5 - Incident Detection**

- Monitorização 24/7
- Alertas automáticos
- Threshold-based alerts
- Anomaly detection
- User behavior analytics

**Rule 16.6 - Incident Response Plan**

- Plano documentado
- Equipa designada
- Procedimentos de contenção
- Comunicação com stakeholders
- Post-mortem obrigatório

**Rule 16.7 - Breach Notification**

- Notificação em < 72h (GDPR)
- Template de comunicação
- Contacto com autoridades (CNPD, etc)
- Transparência com utilizadores afetados
- Documentação completa do incidente

---

## 17. COMPLIANCE & PRIVACY

### **GDPR Compliance**

**Rule 17.1 - Data Subject Rights**

- Right to access (export de dados)
- Right to rectification (editar dados)
- Right to erasure (apagar conta)
- Right to data portability (export em formato standard)
- Right to object (opt-out de processamento)
- Implementar todos os direitos em self-service

**Rule 17.2 - Consent Management**

- Consentimento explícito para processamento
- Opt-in (não opt-out)
- Granular (por tipo de processamento)
- Revogável a qualquer momento
- Logs de consentimentos

**Rule 17.3 - Data Minimization**

- Coletar apenas dados necessários
- Evitar "nice to have" data
- Revisão regular de dados coletados
- Eliminar dados desnecessários
- Privacy by design

**Rule 17.4 - Data Retention**

- Políticas de retenção documentadas
- Eliminação automática após período
- Legal holds sobrepõem auto-delete
- Documentar justificação de retenção
- Revisão anual de políticas

### **Other Compliance**

**Rule 17.5 - HIPAA (se aplicável)**

- Encryption of PHI (Protected Health Information)
- Access controls rigorosos
- Audit logs completos
- Business Associate Agreements (BAA)
- Security risk assessments anuais

**Rule 17.6 - PCI-DSS (se aplicável)**

- Nunca armazenar dados completos de cartão
- Tokenização via payment gateway
- SAQ (Self-Assessment Questionnaire) anual
- Network segmentation
- Quarterly vulnerability scans

---

## 18. SECURITY TESTING & AUDITING

### **Testing**

**Rule 18.1 - Penetration Testing**

- Pentest externo anual
- Scope: todas as aplicações public-facing
- Testar auth, authz, injection flaws
- Documentar findings e remediação
- Retest após fixes

**Rule 18.2 - Vulnerability Scanning**

- Scan automático semanal
- Scan de dependencies (`pip-audit`, `safety`, `npm audit`)
- Scan de container images
- Scan de infraestrutura
- Remediar HIGH/CRITICAL em **7 dias**

**Rule 18.3 - Code Security Review**

- Review de segurança para features críticas
- Static analysis tools (Bandit, SonarQube, ESLint)
- Review manual para mudanças de auth/authz
- Checklist OWASP Top 10
- Documentar findings

### **Auditing**

**Rule 18.4 - Access Audit**

- Review trimestral de permissões
- Remover acesso de utilizadores inativos (90+ dias)
- Rever acessos privilegiados
- Validar least privilege
- Documentar findings e ações

**Rule 18.5 - Dependency Audit**

- Scan de vulnerabilidades em dependencies
- CI/CD pipeline com dependency check
- Bloquear builds com vulnerabilidades HIGH/CRITICAL
- Update regular de dependencies
- Documentar dependências vulneráveis conhecidas (com mitigação)

---

## 19. DEPLOYMENT & CI/CD SECURITY

### **CI/CD Pipeline**

**Rule 19.1 - Secure Build**

- Build environment isolado
- Sem secrets em logs
- Secrets injetados em runtime
- Assinatura de artifacts
- Artifacts imutáveis

**Rule 19.2 - Pre-Deployment Checks**

- Todos os testes passam
- Security scans (SAST, dependency scan)
- Linting sem erros
- Sem vulnerabilidades HIGH/CRITICAL
- Rollback plan documentado

**Rule 19.3 - Deployment Strategy**

- Blue-green deployment (zero downtime)
- Canary releases para features críticas
- Health checks antes de switch
- Rollback automático em falha
- Notificações de deploy

### **Environment Security**

**Rule 19.4 - Environment Separation**

- Ambientes separados: dev/staging/prod
- NUNCA usar dados de prod em dev/staging
- Secrets diferentes por ambiente
- Access control por ambiente
- Isolamento de rede

**Rule 19.5 - Production Access**

- Acesso limitado (need-to-know)
- MFA obrigatório
- VPN obrigatório
- Audit de todos os acessos
- Acesso time-limited

---

## 20. DISASTER RECOVERY & BUSINESS CONTINUITY

### **Backup & Recovery**

**Rule 20.1 - Backup Strategy**

- Backups diários automáticos
- Backups incrementais
- Backup antes de migrações major
- Testar restore mensalmente
- Retenção: **30 dias** (mínimo)

**Rule 20.2 - Recovery Objectives**

- RTO (Recovery Time Objective): **< 4 horas**
- RPO (Recovery Point Objective): **< 24 horas**
- Documentar procedimentos de restore
- Equipa treinada
- Testar disaster recovery anualmente

**Rule 20.3 - High Availability**

- Load balancing
- Auto-scaling
- Multi-region deployment (opcional)
- Database replication
- Failover automático

---

## 21. SUPPLY CHAIN SECURITY

### **Dependency Management**

**Rule 21.1 - Package Integrity Verification**

- Verificar checksums/hashes de packages
- Usar lockfiles com hashes (`package-lock.json`, `poetry.lock`)
- `pip install --require-hashes` para Python
- Verificar assinaturas de packages quando disponíveis
- NUNCA instalar packages sem verificação

**Rule 21.2 - Typosquatting Prevention**

- Verificar nomes de packages cuidadosamente
- Usar listas aprovadas de packages críticos
- Automated scanning para typosquatting
- Review manual de novos packages
- Monitorizar PyPI/npm para packages suspeitos

**Rule 21.3 - Dependency Poisoning Protection**

- Private package registry/mirror para packages aprovados
- Scan de malware em dependencies
- Code review de packages críticos
- Pin de versões exatas (não ranges tipo `^` ou `~`)
- Alertas em mudanças de dependencies

**Rule 21.4 - Software Bill of Materials (SBOM)**

- Gerar SBOM de todas as aplicações
- Tracking completo de dependencies
- Incluir transitive dependencies
- Update SBOM em cada release
- Usar formato standard (SPDX, CycloneDX)

**Rule 21.5 - Dependency Updates**

- Update regular de dependencies (mensal)
- Priorizar security updates (dentro de 7 dias)
- Testar updates em staging primeiro
- Automated dependency update PRs (Dependabot, Renovate)
- Documentar decision de não atualizar (com justificação)

### **Build Pipeline Security**

**Rule 21.6 - Build Reproducibility**

- Builds determinísticos
- Lockfiles versionados
- Build environment imutável
- Cached dependencies verificados
- Assinatura de build artifacts

**Rule 21.7 - Artifact Verification**

- Assinatura digital de artifacts
- Verificação antes de deploy
- Chain of custody documentada
- Artifact registry seguro
- Imutabilidade de artifacts

---

## 22. SOCIAL ENGINEERING & HUMAN FACTORS

### **Security Awareness**

**Rule 22.1 - Security Training**

- Treino de segurança obrigatório (anual mínimo)
- Phishing simulation tests (trimestrais)
- Awareness de social engineering tactics
- Reporting de incidentes suspeitos
- Consequências de violações comunicadas

**Rule 22.2 - Phishing Prevention**

- Email authentication (SPF, DKIM, DMARC)
- Link scanning automático
- Avisos em emails externos
- Verificação de remetentes suspeitos
- Nunca clicar em links de emails não solicitados

**Rule 22.3 - Insider Threat Mitigation**

- Separation of duties para operações críticas
- Dual approval para mudanças sensíveis
- Monitoring de comportamentos anómalos
- Background checks para posições sensíveis
- Exit interviews e handover procedures

### **Access Management Lifecycle**

**Rule 22.4 - Onboarding Security**

- Security training no primeiro dia
- Princípio de least privilege desde início
- MFA configurado antes de acesso
- Assinatura de políticas de segurança
- Equipment security (encryption, screen lock, etc)

**Rule 22.5 - Offboarding Process**

- Checklist de offboarding obrigatória
- Revogação imediata de todos os acessos
- Coleta de hardware/tokens
- Rotação de shared secrets conhecidos
- Exit interview sobre security knowledge

**Rule 22.6 - Periodic Access Review**

- Review de acessos a cada **90 dias**
- Remover acessos não usados (90+ dias)
- Validar necessidade de privilégios
- Documentar justificações
- Automated alerts para reviews overdue

---

## 23. API VERSIONING & DEPRECATION SECURITY

### **API Lifecycle Management**

**Rule 23.1 - Version Security Parity**

- Todas as versões ativas mantêm mesmo nível de segurança
- Security patches aplicados a TODAS as versões suportadas
- NUNCA deixar versões antigas vulneráveis
- Monitorização de segurança por versão
- Documentar status de segurança por versão

**Rule 23.2 - Deprecation Process**

- Aviso prévio de **6 meses** para deprecation
- Comunicação clara de timeline
- Migration guides detalhados
- Support durante período de transição
- Telemetry de uso de versões antigas

**Rule 23.3 - Version Sunset**

- Hard shutdown de versões inseguras
- Redirect para documentação de upgrade
- Logs de tentativas de uso de versões antigas
- Comunicação final antes de shutdown
- Rollback plan se necessário

**Rule 23.4 - Breaking Changes Management**

- Breaking changes apenas em major versions
- Compatibilidade backward quando possível
- Feature flags para transições graduais
- Documentação completa de mudanças
- Testes de compatibilidade

---

## 24. WEBSOCKET SECURITY

### **WebSocket Connection Security**

**Rule 24.1 - WSS (WebSocket Secure)**

- **SEMPRE usar WSS** (WebSocket over TLS)
- NUNCA WS em produção
- Mesmos certificados que HTTPS
- Validar certificados no cliente
- Pinning opcional para mobile

**Rule 24.2 - WebSocket Authentication**

- Autenticação na conexão inicial
- Token JWT no handshake
- Revalidação periódica durante conexão
- Timeout de conexão (ex: 1 hora)
- Reconnection com novo token

**Rule 24.3 - Origin Validation**

- Validar `Origin` header rigorosamente
- Whitelist de origins permitidas
- Rejeitar origins desconhecidos
- Logs de tentativas de origins inválidos
- CSRF protection via Origin check

**Rule 24.4 - Message Security**

- Rate limiting de mensagens (ex: 100/minuto)
- Validação de mensagens recebidas
- Size limits de mensagens (ex: 1MB)
- Sanitização de conteúdo
- Encryption adicional se dados sensíveis

**Rule 24.5 - Connection Management**

- Limit de conexões simultâneas por utilizador
- Cleanup de conexões inativas (timeout)
- Resource limits por conexão
- Graceful shutdown
- Logs de conexões e desconexões

---

## 25. GRAPHQL SECURITY

### **Query Security**

**Rule 25.1 - Query Depth Limiting**

- Limite máximo de depth (ex: 7 níveis)
- Prevenir queries infinitamente nested
- Reject queries que excedem limite
- Configurável por tipo
- Logging de queries rejeitadas

**Rule 25.2 - Query Complexity Analysis**

- Calcular custo de queries antes de executar
- Limite de complexidade (ex: 1000 pontos)
- Custo por field configurável
- Reject queries muito complexas
- Throttling baseado em complexidade

**Rule 25.3 - Introspection Control**

- **Introspection DESATIVADO em produção**
- Apenas ativo em dev/staging
- Introspection apenas para utilizadores autenticados (se necessário em prod)
- Documentação separada do introspection
- Monitorizar uso de introspection

**Rule 25.4 - Batching Attacks Prevention**

- Limite de queries em batch (ex: 10)
- Rate limiting de batch requests
- Análise de complexidade em batches
- Timeout por batch
- Logs de batches grandes

### **GraphQL-Specific Attacks**

**Rule 25.5 - Field Duplication Attack**

- Detectar duplicação massiva de fields
- Limite de field repetitions
- Normalização de queries
- Reject queries com duplication excessiva
- Alertas de tentativas de ataque

**Rule 25.6 - Circular Query Prevention**

- Detectar referências circulares
- Prevenir queries que causam loops
- Análise estática de queries
- Timeout de execução (ex: 30s)
- Error handling adequado

**Rule 25.7 - N+1 Query Prevention**

- Usar DataLoader ou similar
- Batching de database queries
- Caching agressivo
- Monitoring de query patterns
- Otimização contínua

---

## 26. SERVICE MESH & MICROSERVICES SECURITY

### **Service-to-Service Communication**

**Rule 26.1 - Mutual TLS (mTLS)**

- mTLS entre todos os serviços
- Certificados por serviço
- Rotação automática de certificados
- Validação bidirecional
- Rejeitar conexões não-mTLS

**Rule 26.2 - Service Authentication**

- Service identity único por serviço
- Service accounts com least privilege
- JWT para service-to-service auth
- Validar service identity em cada request
- Revogação de service credentials

**Rule 26.3 - Service Authorization**

- Policy-based access control
- Whitelist de serviços permitidos por endpoint
- Granular permissions entre serviços
- Audit de comunicação inter-service
- Deny by default

### **API Gateway Security**

**Rule 26.4 - Gateway as Security Perimeter**

- Autenticação centralizada no gateway
- Rate limiting no gateway
- Request validation no gateway
- Logging centralizado
- WAF no gateway

**Rule 26.5 - Backend for Frontend (BFF)**

- BFF por tipo de cliente (web, mobile, etc)
- Isolamento de lógica de cliente
- Security policies específicas
- Transformação de responses
- Agregação segura

### **Resilience & Fault Tolerance**

**Rule 26.6 - Circuit Breakers**

- Circuit breaker em chamadas externas
- Fail fast em serviços degradados
- Fallback strategies
- Health checks contínuos
- Automatic recovery

**Rule 26.7 - Distributed Tracing**

- Tracing de todas as requests
- Correlation IDs propagados
- Performance monitoring
- Security event tracking
- Audit trail distribuído

---

## 27. CRYPTOJACKING PREVENTION

### **Resource Monitoring**

**Rule 27.1 - Resource Usage Monitoring**

- Monitoring de CPU/memory em tempo real
- Alertas em spikes anómalos
- Baseline de uso normal estabelecido
- Automated response a anomalias
- Dashboard de resource usage

**Rule 27.2 - Container Resource Limits**

- CPU limits em containers
- Memory limits em containers
- Resource quotas por namespace (Kubernetes)
- OOMKill policies
- Prevenção de noisy neighbors

**Rule 27.3 - Browser Mining Detection**

- Blocklist de mining scripts conhecidos
- CSP para prevenir mining scripts
- Browser extension detection (opcional)
- Network monitoring para mining pools
- User alerts se detetado

### **Infrastructure Protection**

**Rule 27.4 - Process Whitelisting**

- Whitelist de processos permitidos
- Block de processos desconhecidos
- Automated termination de miners
- Logs de tentativas
- Rootkit detection

**Rule 27.5 - Network Traffic Analysis**

- Monitoring de outbound connections
- Blocklist de mining pool IPs/domains
- Anomaly detection em traffic patterns
- Firewall rules para mining ports
- DNS filtering

---

## 28. ZERO TRUST ARCHITECTURE

### **Core Principles**

**Rule 28.1 - Never Trust, Always Verify**

- Autenticação em TODOS os acessos
- NUNCA confiar em network location
- Verificação contínua de identidade
- Re-autenticação periódica
- Context-aware access control

**Rule 28.2 - Micro-Segmentation**

- Segmentação granular de rede
- Firewalls entre cada segmento
- Policies por workload
- Isolamento de aplicações críticas
- Software-defined perimeter

**Rule 28.3 - Least Privilege Access**

- Just-in-time (JIT) access
- Just-enough-access (JEA)
- Time-limited permissions
- Privilege elevation apenas quando necessário
- Automated privilege revocation

**Rule 28.4 - Assume Breach**

- Design assumindo que breach já ocorreu
- Lateral movement prevention
- Segmentation para conter breaches
- Monitoring para detectar movement
- Rapid response procedures

### **Continuous Verification**

**Rule 28.5 - Device Posture Verification**

- Verificar device compliance
- Antivirus/EDR ativo
- Patches atualizados
- Encryption ativada
- Deny access a devices não-compliant

**Rule 28.6 - User Behavior Analytics**

- Baseline de comportamento normal
- Anomaly detection
- Risk scoring dinâmico
- Adaptive authentication
- Automated response a anomalias

**Rule 28.7 - Continuous Monitoring**

- Logs de TODOS os acessos
- Real-time analysis
- Correlation de eventos
- Threat intelligence integration
- SOAR (Security Orchestration and Automation)

---

## 29. ERROR HANDLING & INFORMATION DISCLOSURE

### **Error Response Security**

**Rule 29.1 - Generic Error Messages**

- Mensagens genéricas para utilizadores
- "An error occurred" em vez de detalhes técnicos
- NUNCA expor stack traces
- NUNCA expor database errors
- NUNCA expor file paths ou estrutura interna

**Rule 29.2 - HTTP Status Codes**

- Usar status codes apropriados mas genéricos
- 401 para authentication errors (não "invalid password")
- 403 para authorization (não "user X cannot access Y")
- 404 para recursos inexistentes (não revelar se existe)
- 500 para erros internos (sem detalhes)

**Rule 29.3 - Error Logging**

- Logs detalhados INTERNAMENTE
- Include stack traces em logs internos
- Include context e request data
- **NUNCA logar passwords, tokens, ou PII**
- Centralized logging com acesso restrito

**Rule 29.4 - Debug Information**

- Debug endpoints DESATIVADOS em produção
- Source maps desativados em produção
- Verbose logging apenas em dev
- Stack traces apenas em logs internos
- NUNCA retornar queries SQL em errors

### **Timing & Side-Channel Attacks**

**Rule 29.5 - Constant-Time Comparisons**

- Usar constant-time comparison para secrets
- `hmac.compare_digest()` em Python
- `crypto.timingSafeEqual()` em Node.js
- Prevenir timing attacks em password checks
- Prevenir timing attacks em token validation

**Rule 29.6 - Response Time Normalization**

- Adicionar delay aleatório em operações sensíveis
- Login failure: mesmo tempo que success
- User enumeration prevention
- Rate limiting adicional
- Jitter em responses

**Rule 29.7 - Error Handling Consistency**

- Mesmo tipo de error para diferentes falhas
- "Invalid credentials" para username ou password errados
- Não revelar qual campo está errado
- Tempo de resposta consistente
- Prevenir information disclosure via errors

---

## 30. ADVANCED THREAT PROTECTION

### **Runtime Application Self-Protection (RASP)**

**Rule 30.1 - Runtime Protection**

- RASP agent em produção (opcional mas recomendado)
- Detecção de ataques em runtime
- Automated blocking de ataques
- Zero-day protection
- Real-time alerts

**Rule 30.2 - Web Application Firewall (WAF)**

- WAF em todas as aplicações public-facing
- OWASP Core Rule Set ativado
- Custom rules para aplicação
- Virtual patching para vulnerabilities conhecidas
- Logs e alerts de WAF

### **Advanced Monitoring**

**Rule 30.3 - Threat Intelligence Integration**

- Feeds de threat intelligence
- IP reputation checking
- Known malicious actor blocking
- IOC (Indicators of Compromise) matching
- Automated response a threats conhecidas

**Rule 30.4 - User Entity Behavior Analytics (UEBA)**

- Behavioral baselines por utilizador
- Anomaly detection
- Risk scoring
- Privilege escalation detection
- Account takeover detection

**Rule 30.5 - Deception Technology**

- Honeypots em rede interna
- Honey tokens em aplicação
- Canary files/databases
- Early warning system
- Attacker profiling

---

---

## 📊 SECURITY RULES MATRIX - APLICABILIDADE POR TIPO DE PROJETO

Esta matriz indica quais regras são **obrigatórias** para cada tipo de projeto.

### **Legenda:**
- ✅ **OBRIGATÓRIO** - Deve ser implementado
- ⚠️ **RECOMENDADO** - Fortemente recomendado mas pode ser opcional
- ➖ **NÃO APLICÁVEL** - Não se aplica a este tipo de projeto
- 🔴 **CRÍTICO** - Extremamente crítico, violação grave se não implementado

---

### **FRONTEND ONLY (Vue.js, React, etc)**

| Categoria | Regras | Status |
|-----------|--------|--------|
| **1. Authentication** | 1.1, 1.4 | ⚠️ |
| **1. Authentication** | 1.2, 1.3, 1.5-1.15 | ➖ |
| **2. Authorization** | 2.1-2.4 | ⚠️ |
| **2. Authorization** | 2.5-2.11 | ➖ |
| **3. Encryption** | 3.4-3.6 | ✅ |
| **3. Encryption** | 3.1-3.3, 3.7-3.9 | ➖ |
| **4. Input Validation** | 4.1-4.4, 4.12-4.14 | 🔴 |
| **4. Input Validation** | 4.5-4.11, 4.15-4.16 | ➖ |
| **5. API Security** | 5.1-5.3, 5.7, 5.12-5.13 | ✅ |
| **5. API Security** | 5.4-5.6, 5.8-5.11 | ➖ |
| **6. Frontend Security** | 6.1-6.10 | 🔴 |
| **7. Django Backend** | Todas | ➖ |
| **8. Database** | Todas | ➖ |
| **9. Multi-Tenant** | 9.1 (se aplicável) | ⚠️ |
| **10. AI Security** | Todas | ➖ |
| **11. Mobile** | Todas | ➖ |
| **12. Infrastructure** | 12.1, 12.2 | ⚠️ |
| **13. Secrets** | 13.1, 13.3 | ✅ |
| **14. File Upload** | 14.1-14.3 (client-side) | ⚠️ |
| **15. Third-Party** | 15.1, 15.3 | ⚠️ |
| **16. Logging** | 16.1-16.2 (client-side) | ⚠️ |
| **17. Compliance** | 17.1-17.4 | ✅ |
| **18. Testing** | 18.1, 18.3 | ⚠️ |
| **19. CI/CD** | 19.1-19.3 | ✅ |
| **20. Disaster Recovery** | Todas | ➖ |

**Regras CRÍTICAS para Frontend:**
- 4.1-4.4, 4.12-4.14 (XSS Prevention)
- 6.1-6.10 (Frontend Security)
- 3.4 (HTTPS)
- 17.1-17.4 (GDPR)

---

### **BACKEND ONLY (Django API)**

| Categoria | Regras | Status |
|-----------|--------|--------|
| **1. Authentication** | 1.1-1.15 | 🔴 |
| **2. Authorization** | 2.1-2.11 | 🔴 |
| **3. Encryption** | 3.1-3.9 | ✅ |
| **4. Input Validation** | 4.1-4.11, 4.15-4.16 | 🔴 |
| **4. Input Validation** | 4.12-4.14 | ⚠️ |
| **5. API Security** | 5.1-5.13 | 🔴 |
| **6. Frontend Security** | Todas | ➖ |
| **7. Django Backend** | 7.1-7.19 | 🔴 |
| **8. Database** | 8.1-8.11 | 🔴 |
| **9. Multi-Tenant** | 9.1-9.6 (se multi-tenant) | 🔴 |
| **10. AI Security** | 10.1-10.12 (se usar IA) | ✅ |
| **11. Mobile** | Todas | ➖ |
| **12. Infrastructure** | 12.1-12.9 | ✅ |
| **13. Secrets** | 13.1-13.5 | 🔴 |
| **14. File Upload** | 14.1-14.5 | ✅ |
| **15. Third-Party** | 15.1-15.3 | ✅ |
| **16. Logging** | 16.1-16.7 | 🔴 |
| **17. Compliance** | 17.1-17.6 | 🔴 |
| **18. Testing** | 18.1-18.5 | ✅ |
| **19. CI/CD** | 19.1-19.5 | ✅ |
| **20. Disaster Recovery** | 20.1-20.3 | ✅ |

**Regras CRÍTICAS para Backend Django:**
- 7.1 (DEBUG = False) 🔴
- 7.2 (SECRET_KEY) 🔴
- 7.5 (SECURE Settings) 🔴
- 7.6 (ORM Usage - SQL Injection Prevention) 🔴
- 7.14-7.15 (Django Admin Security) 🔴
- 7.16-7.19 (DRF Security) 🔴
- 1.1-1.15 (Authentication completa) 🔴
- 2.1-2.4 (RBAC) 🔴
- 8.1-8.3 (Database Access Control) 🔴
- 9.1 (Tenant ID Verification se multi-tenant) 🔴
- 13.1-13.2 (Secrets Management) 🔴
- 16.1-16.4 (Security Logging) 🔴
- 17.1-17.4 (GDPR Compliance) 🔴

---

### **FULL-STACK (Django + Vue.js)**

| Categoria | Regras | Status |
|-----------|--------|--------|
| **Todas as categorias** | Todas | 🔴/✅ |

**Combinar regras de Frontend + Backend:**
- Todas as regras CRÍTICAS de Backend
- Todas as regras CRÍTICAS de Frontend
- Atenção especial a integração (CORS, CSRF, etc)

---

### **AI-POWERED APPLICATION (Django + IA)**

| Categoria | Regras | Status |
|-----------|--------|--------|
| **Todas de Backend** | Todas | 🔴 |
| **10. AI Security** | 10.1-10.12 | 🔴 |

**Regras ADICIONAIS CRÍTICAS para IA:**
- 10.1-10.4 (Model Security) 🔴
- 10.5-10.7 (Prompt Injection Prevention) 🔴
- 10.8-10.10 (Output Validation) 🔴
- 10.11-10.12 (AI Agent Security) 🔴
- 2.9-2.11 (AI Agent Permissions) 🔴
- Rate limiting agressivo em AI endpoints
- Human-in-the-loop para decisões críticas

---

### **MOBILE APP (iOS/Android + Django Backend)**

| Categoria | Regras | Status |
|-----------|--------|--------|
| **Todas de Backend** | Todas | 🔴 |
| **11. Mobile Security** | 11.1-11.4 | 🔴 |
| **1. Authentication** | 1.1-1.15 | 🔴 |
| **5. API Security** | 5.1-5.13 | 🔴 |

**Regras ADICIONAIS CRÍTICAS para Mobile:**
- 11.1 (Secure Storage) 🔴
- 11.2 (Certificate Pinning) 🔴
- 11.3 (Jailbreak/Root Detection) ⚠️
- 11.4 (Mobile API Security) 🔴
- Deep link validation
- Biometric authentication
- App obfuscation

---

### **API ONLY (Microservice/REST API)**

| Categoria | Regras | Status |
|-----------|--------|--------|
| **1. Authentication** | 1.1-1.5, 1.10 | 🔴 |
| **2. Authorization** | 2.1-2.4 | 🔴 |
| **3. Encryption** | 3.1-3.9 | ✅ |
| **4. Input Validation** | 4.1-4.11 | 🔴 |
| **5. API Security** | 5.1-5.13 | 🔴 |
| **7. Django Backend** | 7.1-7.19 | 🔴 |
| **8. Database** | 8.1-8.11 | 🔴 |
| **13. Secrets** | 13.1-13.5 | 🔴 |
| **15. Third-Party** | 15.1-15.3 | ✅ |
| **16. Logging** | 16.1-16.7 | 🔴 |
| **18. Testing** | 18.1-18.5 | ✅ |
| **19. CI/CD** | 19.1-19.5 | ✅ |

**Regras CRÍTICAS para API:**
- 5.1-5.6 (Authentication & Rate Limiting) 🔴
- 5.7-5.9 (Request/Response Security) 🔴
- 7.16-7.19 (Django REST Framework) 🔴
- 4.1-4.11 (Input Validation & Injection Prevention) 🔴
- Documentação segura (Swagger com autenticação)

---

### **MULTI-TENANT SaaS (Django + Vue.js + Multi-Tenancy)**

| Categoria | Regras | Status |
|-----------|--------|--------|
| **Todas de Full-Stack** | Todas | 🔴 |
| **9. Multi-Tenant** | 9.1-9.6 | 🔴 |
| **8. Database** | 8.5 (PostgreSQL RLS) | 🔴 |

**Regras ADICIONAIS CRÍTICAS para Multi-Tenant:**
- 9.1 (Tenant ID Verification) 🔴🔴🔴
- 9.3 (Cross-Tenant Leakage Prevention) 🔴
- 9.4 (Shared Resources Isolation) 🔴
- Database schemas separados ou RLS
- Testes específicos de isolamento
- Pentest focado em multi-tenancy

---

## 🎯 RESUMO DE PRIORIDADES

### **CRÍTICO (🔴) - NUNCA IGNORAR:**

1. **Multi-tenant isolation (se aplicável)** - Rule 9.1
2. **SQL injection prevention** - Rule 7.6
3. **Django DEBUG = False em produção** - Rule 7.1
4. **Django SECRET_KEY seguro** - Rule 7.2
5. **Django SECURE settings** - Rule 7.5
6. **Authentication & Authorization** - Rules 1.x, 2.x
7. **Secrets management** - Rules 13.1-13.2
8. **HTTPS everywhere** - Rule 3.4
9. **Input validation server-side** - Rule 4.1
10. **XSS prevention (frontend)** - Rules 4.12-4.14, 6.5
11. **Audit logging** - Rules 16.1-16.4
12. **GDPR compliance** - Rules 17.1-17.4

### **HIGH PRIORITY (✅) - SEMPRE SEGUIR:**

13. **Rate limiting** - Rules 5.4-5.6
14. **Password security** - Rules 1.6-1.8
15. **Database security** - Rules 8.1-8.3
16. **File upload validation** - Rules 14.1-14.5
17. **CI/CD security** - Rules 19.1-19.3
18. **Backups automáticos** - Rule 20.1
19. **Django ORM security** - Rule 7.6-7.8
20. **Django Admin security** - Rules 7.14-7.15

### **RECOMMENDED (⚠️) - QUANDO POSSÍVEL:**

21. **Penetration testing** - Rule 18.1
22. **MFA** - Rule 1.10
23. **Certificate pinning (mobile)** - Rule 11.2
24. **AI security (se usar IA)** - Rules 10.x
25. **Code reviews de segurança** - Rule 18.3
26. **Supply chain security** - Rules 21.x (IMPORTANTE!)
27. **Zero Trust principles** - Rules 28.x
28. **WebSocket security (se usar)** - Rules 24.x
29. **GraphQL security (se usar)** - Rules 25.x
30. **Error handling security** - Rules 29.x

---

## 🔄 DOCUMENT MAINTENANCE

Este documento deve ser atualizado quando:

- Novas vulnerabilidades são descobertas
- Requisitos de compliance mudam
- Novas features de segurança são adicionadas
- Post-mortems revelam gaps de segurança
- Stack tecnológica muda
- Mudanças regulatórias ocorrem

**Owner:** [Nome do Responsável]  
**Review Schedule:** Trimestral (Março, Junho, Setembro, Dezembro)  
**Last Review:** [Data]  
**Next Review:** [Data]

---

## 📝 NOTAS FINAIS

**Segurança é responsabilidade de todos.** Estas regras existem para proteger os dados dos clientes e o negócio. Em caso de dúvida:

1. **Perguntar antes de implementar** - Não adivinhar em questões de segurança
2. **Default para seguro** - Escolher a opção mais segura
3. **Documentar decisões** - Explicar trade-offs de segurança
4. **Reportar preocupações** - Falar sobre potenciais vulnerabilidades
5. **Manter-se informado** - Continuar a aprender sobre ameaças de segurança

**Lembrar:** Uma única falha de segurança pode comprometer todas as outras proteções. Levar estas regras a sério.

---

**🛡️ Segurança não é opcional. É obrigatória.**