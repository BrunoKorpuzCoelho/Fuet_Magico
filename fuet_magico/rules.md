# 🔒 CUBIX ERP - REGRAS DE DESENVOLVIMENTO E SEGURANÇA

> **Última atualização:** 25 de Novembro de 2025  
> **Versão:** 3.1  
> **Ambiente:** Multi-tenant + AI-First + Event-Driven

---

## 📋 ÍNDICE

1. [Regras Gerais de Código](#regras-gerais-de-código)
2. [Regras de Backend](#regras-de-backend)
3. [Regras de Frontend](#regras-de-frontend)
4. [Regras de IA](#regras-de-ia)
5. [Regras de Segurança Geral](#regras-de-segurança-geral)
6. [Regras de Base de Dados](#regras-de-base-de-dados)
7. [Regras de API](#regras-de-api)
8. [Regras de Deploy](#regras-de-deploy)

---

É obrigatório ver todas as regras, mesmo que não se adequem à necessidade de termos que as ver, para entendermos o contexto das regras inteiras, ok? Portanto, em vez de ver só as regras de back-end, portanto, a data de back-end, eu quero que você leia-as todas, inclusive as de segurança, que são as mais importantes, que é para não recebermos ataques de desnecessidade de segurança.

---

## 🎯 REGRAS GERAIS DE CÓDIGO

### **Princípios Fundamentais**

1. **Sem comentários no código** - código deve ser auto-explicativo
2. **Sem testes** - fazemos depois aqui e mesmo sem nenhum teste 
3. **Sem documentação inline** - fazemos depois
4. **Sem migrações** - faço depois
5. **Controllers apenas para rotas** - lógica de negócio fica em `services.py` (ver `python\modules\tenants`)
6. **Estrutura clean code** - código limpo, legível e manutenível
7. **1 tabela por ficheiro** - igual Odoo, depois importar no `__init__.py` do models e depois no `__init__.py` do modules
8. **Campos do BaseModel** - sempre verificar campos herdados antes de criar novos
9. **Nunca atualizar tarefas sem autorização** - aguardar aprovação do utilizador
10. **Todos os logs de erro/raise user error/ ou outros que criamos** - Sempre em ingles  

### **Nomenclatura**

- **Ficheiros:** snake_case (`user_service.py`, `auth_controller.py`)
- **Classes:** PascalCase (`UserService`, `AuthController`)
- **Funções/Métodos:** snake_case (`get_user_by_id`, `validate_token`)
- **Constantes:** UPPER_SNAKE_CASE (`MAX_RETRY_ATTEMPTS`, `DEFAULT_TTL_DAYS`)
- **Variáveis privadas:** Prefixo `_` (`_internal_cache`, `_validate_input`)

### **Estrutura de Módulos**

```
python/modules/nome_modulo/
├── __init__.py           # Imports do módulo
├── models/               # 1 ficheiro por modelo
│   ├── __init__.py
│   └── modelo.py
├── services/             # Lógica de negócio
│   ├── __init__.py
│   └── modelo_service.py
├── controllers.py        # APENAS rotas HTTP
└── utils.py             # Utilitários do módulo (se necessário)
```

---

## 🔐 REGRAS DE BACKEND

### **Segurança de Autenticação**

1. **JWT Tokens:**

   - Expiração máxima de 24h
   - Secret key NUNCA no código - usar `.env`
   - Refresh tokens com expiração de 7 dias
   - Invalidar tokens em logout
   - Rotação automática de secrets (a cada 90 dias)

2. **Passwords:**

   - Hash com bcrypt (nunca MD5/SHA1)
   - Salt individual por password
   - Mínimo 12 caracteres
   - Força obrigatória: maiúsculas + minúsculas + números + especiais
   - Histórico de 5 passwords (não permitir reutilização)
   - Rate limiting em login: 5 tentativas / 15 minutos

3. **Sessions:**
   - Timeout de inatividade: 30 minutos
   - Renovação automática em atividade
   - Binding ao IP e User-Agent
   - Logout forçado em mudança de IP (opcional por tenant)
   - Logs de todas as sessões iniciadas/terminadas

### **Segurança de Autorização**

4. **RBAC (Role-Based Access Control):**

   - Verificar permissões em TODOS os endpoints (exceto públicos)
   - Usar decorators: `@require_permission('module.action')`
   - Princípio do menor privilégio (deny by default)
   - Permissões granulares por campo (read/write separados)
   - Audit log de tentativas de acesso negado

5. **Multi-Tenant Isolation:**

   - SEMPRE verificar `tenant_id` em queries
   - Context automático: `TenantContext.get_current()`
   - NUNCA permitir cross-tenant queries sem autorização explícita
   - Validar tenant_id em TODAS as operações de escrita
   - Analytics cross-tenant apenas com flag específica

6. **Field-Level Security:**
   - Campos sensíveis (`password`, `ssn`, `credit_card`) → encriptação AES-256
   - Mascaramento em logs (`****1234` para cartões)
   - Redação automática em exports (GDPR compliant)
   - Campos financeiros com precisão decimal (nunca float)

### **Segurança de Dados**

7. **Input Validation:**

   - Validar TODOS os inputs de utilizador
   - Sanitização antes de usar em queries
   - Whitelist de caracteres permitidos (não blacklist)
   - Limits de tamanho (strings, uploads, JSON)
   - Rejeitar inputs com caracteres de controle

8. **SQL Injection Prevention:**

   - SEMPRE usar ORM (SQLAlchemy)
   - NUNCA concatenar strings em queries
   - Usar `bindparam()` para valores dinâmicos
   - Sanitização em Query Tracking (`query_tracking.py`)
   - Audit de queries raw (sistema deve alertar)

9. **XSS Prevention:**

   - Escape automático em templates (Jinja2 autoescaping ON)
   - Validar HTML em rich text editors
   - CSP (Content Security Policy) headers
   - Sanitização de JSON antes de render

10. **CSRF Prevention:**
    - Token CSRF em TODOS os forms
    - Validação de Origin/Referer headers
    - SameSite=Strict em cookies
    - Rate limiting em endpoints críticos

### **Segurança de APIs Internas**

11. **Event System:**

    - Validar schema de eventos antes de emit
    - Rate limiting por evento (anti-spam)
    - Anonimização de PII antes de persistir (GDPR)
    - TTL automático por tipo de evento
    - Audit de eventos críticos (ERROR, SECURITY)

12. **Background Jobs (Celery):**

    - Timeout máximo de 5 minutos (configurável)
    - Retry exponencial com max 3 tentativas
    - Dead Letter Queue (DLQ) para falhas persistentes
    - Logging estruturado de falhas
    - Monitoring de worker health

13. **Webhooks:**
    - HMAC signature obrigatório
    - Timestamp validation (±5min window)
    - Rate limiting por webhook (10/min)
    - Retry automático com backoff
    - Audit de deliveries falhadas

### **Logging e Monitoring**

14. **Audit Trail:**

    - Log de TODAS as ações críticas (create, update, delete)
    - Metadata: user_id, tenant_id, IP, timestamp, action
    - Discriminator: HUMAN vs AI Agent
    - Retention: 1 ano (configurável por tenant)
    - Logs imutáveis (append-only)

15. **Error Handling:**

    - NUNCA expor stack traces para utilizador
    - Logs detalhados apenas em ficheiros
    - Mensagens genéricas para cliente (`Internal Server Error`)
    - Alertas automáticos para erros críticos
    - Correlação de erros por `request_id`

16. **Performance Monitoring:**
    - Slow query detection (>1000ms)
    - N+1 query detection automática
    - Connection pool monitoring
    - Memory leak detection
    - Alertas em anomalias (Event Analyzer)

### **Segurança de Dependências**

17. **Third-Party Libraries:**
    - Audit regular com `pip-audit` ou `safety`
    - Pin de versões em `requirements.txt`
    - Scanning automático em CI/CD
    - Proibir bibliotecas sem manutenção (>1 ano)
    - Review de novas dependências (justificar necessidade)

### **Rate Limiting**

18. **API Rate Limits:**
    - Por IP: 100 requests/minuto
    - Por utilizador: 1000 requests/hora
    - Por tenant: 10,000 requests/hora
    - Endpoints críticos: limites personalizados
    - Headers informativos: `X-RateLimit-*`

---

## 🌐 REGRAS DE FRONTEND

### **Segurança de Input**

19. **Form Validation:**

    - Validação client-side + server-side (DUPLA)
    - Feedback visual imediato (sem submit)
    - Mensagens de erro claras
    - Desabilitar submit em formulário inválido
    - Limitar tamanho de campos (max length)

20. **File Uploads:**
    - Validar extensão E mimetype
    - Whitelist de tipos permitidos
    - Limite de tamanho: 10MB (configurável)
    - Scan antivírus (ClamAV) em uploads
    - Armazenar FORA da webroot
    - Gerar nomes aleatórios (nunca usar nome original)

### **Segurança de Autenticação**

21. **Gestão de Tokens:**

    - Tokens em `httpOnly` cookies (não localStorage)
    - Refresh automático antes de expirar
    - Limpar tokens em logout
    - Redirect para login em 401
    - Não enviar tokens em URLs (usar headers)

22. **Session Handling:**
    - Auto-logout após inatividade (30min)
    - Warning 5 minutos antes de expirar
    - Renovação em atividade do utilizador
    - Limpar dados sensíveis em logout

### **Segurança de Dados**

23. **Dados Sensíveis:**

    - NUNCA armazenar passwords no frontend
    - Mascaramento de campos sensíveis (\*\*\*\*1234)
    - Limpar formulários após submit
    - Evitar console.log com dados sensíveis
    - Redação automática em screenshots (se aplicável)

24. **XSS Prevention:**
    - Escapar HTML em user-generated content
    - Usar `textContent` em vez de `innerHTML` (quando possível)
    - Sanitizar rich text com DOMPurify
    - CSP meta tags em index.html
    - Validar JSON antes de processar

### **Segurança de Comunicação**

25. **HTTPS Only:**

    - Forçar HTTPS em produção
    - HSTS headers (max-age=31536000)
    - Upgrade insecure requests automático
    - Alertar em certificados inválidos

26. **CORS:**

    - Whitelist de origens permitidas
    - Credentials apenas para domínios autorizados
    - Validar preflight requests
    - Logs de tentativas cross-origin bloqueadas

27. **WebSockets:**
    - Autenticação obrigatória na conexão
    - Validar JWT antes de permitir subscriptions
    - Rate limiting por conexão
    - Heartbeat para detectar conexões mortas
    - Desconectar automaticamente após 1h

### **Performance e Segurança**

28. **Code Splitting:**

    - Lazy loading de rotas
    - Componentes críticos em bundle principal
    - Chunks otimizados (<250KB)
    - Preload de rotas prováveis

29. **Caching:**

    - Cache de assets com hash (cache-busting)
    - Invalidação automática em deploy
    - Service Worker para offline (se aplicável)
    - Cache de APIs com TTL curto (5min)

30. **Error Boundaries:**
    - Catch de erros React globalmente
    - Fallback UI amigável
    - Logging de erros para backend
    - Não expor detalhes técnicos

---

## 🤖 REGRAS DE IA

### **Segurança de Modelos**

31. **Model Isolation:**

    - IA Local (Ollama) → dados do tenant apenas
    - IA Central (Llama) → dados anonimizados
    - Separação física de modelos (containers)
    - Validar tenant_id antes de processar
    - Logs de acesso a modelos

32. **Prompt Injection Prevention:**

    - Sanitização de inputs do utilizador
    - Templates de prompts fixos (não concatenar direto)
    - Validação de outputs (não executar código gerado sem review)
    - Rate limiting por utilizador (10 requests/min)
    - Timeout de inferência (30s max)

33. **Data Privacy:**
    - Anonimização obrigatória antes de enviar para IA Central
    - Hash SHA-256 com salt por empresa
    - Redação de PII (emails, phones, SSN, etc)
    - Logs de dados enviados para IA
    - Right to Erasure (GDPR) aplicável a treino

### **Segurança de Agentes**

34. **AI Agent Permissions:**

    - Princípio do menor privilégio
    - Permissões explícitas por ação (`ai_agent_permissions`)
    - Rate limiting por agente (100 ações/hora)
    - Audit trail com `reasoning` e `decision_process`
    - Aprovação humana obrigatória para ações críticas (High Risk)

35. **Explainability:**

    - Logs detalhados de decisões (SHAP/LIME se aplicável)
    - Confidence score em todas as ações
    - Risk score calculado automaticamente
    - Metadata JSON com contexto completo
    - UI para visualizar reasoning (Audit Dashboard)

36. **Autonomy Levels:**
    - **Level 1 (Supervised):** Todas as ações requerem aprovação
    - **Level 2 (Semi-Autonomous):** Ações low-risk automáticas
    - **Level 3 (Autonomous):** Todas exceto critical automáticas
    - Configurável por tenant e por agente
    - Downgrade automático em caso de erros frequentes

### **Segurança de Treino**

37. **Model Training:**

    - Apenas IA Central treina (não local)
    - Dados de treino anonimizados
    - Audit de datasets usados
    - Versionamento de modelos (rollback se necessário)
    - A/B testing antes de deploy

38. **Bias Prevention:**
    - Validação de datasets por diversidade
    - Métricas de fairness (disparate impact, etc)
    - Review humano de outputs suspeitos
    - Feedback loop para correção de bias
    - Logs de decisões enviesadas detectadas

### **Segurança de Integração**

39. **Event Analyzer:**

    - Processar apenas eventos dos últimos 30 dias (privacy)
    - Sampling configurável (10% em prod, 100% em dev)
    - Timeout de análise: 5 minutos
    - Fallback em caso de falha (não bloquear sistema)
    - Alertas apenas para severidade >= WARNING

40. **ML Predictor:**

    - Features baseadas apenas em eventos anonimizados
    - Re-treino automático a cada 7 dias
    - Validação de accuracy antes de usar (>80%)
    - Fallback para heurísticas se ML falhar
    - Logs de previsões erradas para correção

41. **Business Logic Analyzer:**
    - AST parsing sem execução de código
    - Análise apenas em ficheiros do projeto (não libs)
    - Detecção de dead code, N+1, security flaws
    - Reports semanais (não real-time)
    - Whitelist de métodos "não usados" permitidos

### **Segurança de Chat IA**

42. **IA Conversacional:**

    - Context window limitado (últimas 10 mensagens)
    - Filtragem de conteúdo inapropriado
    - Rate limiting: 20 mensagens/hora
    - Timeout de resposta: 15s
    - Logging de conversas (GDPR compliant)

43. **TODO Adaptativo:**
    - Níveis de complexidade validados (LOW/MEDIUM/HIGH)
    - Estimativas realistas (não prometer prazos impossíveis)
    - Escalação para GPU central se >30min
    - Progress tracking com WebSocket real-time
    - Cancellation pelo utilizador permitida

---

## 🔒 REGRAS DE SEGURANÇA GERAL

### **Infrastructure**

44. **Secrets Management:**

    - NUNCA commitar secrets no Git
    - Usar `.env` local (ignorado pelo Git)
    - Secrets Manager em produção (AWS Secrets, Vault)
    - Rotação automática de secrets críticos (DB, JWT)
    - Audit de acesso a secrets

45. **Environment Variables:**

    - Diferentes `.env` por ambiente (dev/staging/prod)
    - Validação de variáveis obrigatórias no startup
    - Logs NÃO devem conter valores de `.env`
    - Backup de secrets em múltiplas localizações

46. **Firewall & Network:**

    - Apenas portas necessárias abertas (80, 443, 22)
    - PostgreSQL e Redis apenas localhost
    - Fail2ban em SSH (proteção brute-force)
    - VPN obrigatória para acesso admin

47. **SSL/TLS:**
    - Certificados Let's Encrypt (renovação automática)
    - TLS 1.3 mínimo (desabilitar 1.0 e 1.1)
    - Strong ciphers apenas (AES-256)
    - HSTS headers (força HTTPS)

### **Compliance**

48. **GDPR:**

    - Right to Access: API para export de dados
    - Right to Erasure: Deleção completa (hard delete)
    - Right to Portability: Export em JSON/CSV
    - Data Processing Agreements com terceiros
    - DPO designado (se aplicável)

49. **Data Retention:**

    - TTL automático por tipo de dado:
      - QUERY: 30 dias
      - ERROR: 90 dias
      - ACTION: 180 dias
      - USER_BEHAVIOR: 60 dias
    - Agregações antes de deletar (para analytics)
    - Configurável por tenant

50. **Audit Requirements:**
    - Logs imutáveis (append-only tables)
    - Retention de 1 ano mínimo
    - Export de audit logs para compliance
    - Alertas em eventos suspeitos
    - Review regular de acessos privilegiados

---

## 🗄️ REGRAS DE BASE DE DADOS

### **Segurança de Acesso**

51. **Credentials:**

    - User separado por ambiente (dev/prod)
    - Password forte (20+ caracteres)
    - Rotação a cada 90 dias
    - Least privilege (apenas schemas necessários)

52. **Connection Pooling:**

    - Pool size otimizado (workers \* 2 + 1)
    - Max overflow limitado (evitar esgotar conexões)
    - Timeout de aquisição: 30s
    - Health checks a cada 30s
    - Logs de pool exhaustion

53. **Read Replicas:**
    - Routing automático (read→replica, write→master)
    - Health monitoring contínuo
    - Failover automático se lag >10s
    - Validação de data consistency
    - ML-based replica selection

### **Performance e Segurança**

54. **Indexes:**

    - GIN indexes para JSONB
    - B-tree para foreign keys
    - Partial indexes para queries frequentes
    - Análise de slow queries (>1000ms)
    - Reindex automático semanal

55. **Backups:**

    - Backup diário às 3AM
    - Rotação de 7 dias (mínimo)
    - Compressão gzip automática
    - Validação de integridade após backup
    - Restore testado mensalmente
    - Encryption at rest (AES-256)

56. **Row-Level Security (RLS):**

    - Políticas PostgreSQL por tenant
    - Isolamento automático em queries
    - Bypass apenas para superuser
    - Audit de tentativas de bypass
    - Performance testing de policies

57. **Encryption:**
    - Encryption at rest (LUKS ou AWS EBS)
    - Encryption in transit (SSL/TLS)
    - Field-level encryption para dados sensíveis
    - Key management com rotation

---

## 🌍 REGRAS DE API

### **Design**

58. **RESTful Principles:**

    - Endpoints em plural (`/users`, `/invoices`)
    - HTTP methods corretos (GET/POST/PUT/DELETE/PATCH)
    - Status codes apropriados (200, 201, 400, 401, 403, 404, 500)
    - Paginação obrigatória para listas (default 50)
    - Versionamento em URL (`/api/v1/users`)

59. **Request/Response:**

    - Content-Type: `application/json`
    - UTF-8 encoding obrigatório
    - GZIP compression para >1KB
    - Request ID em headers (`X-Request-ID`)
    - Rate limit headers (`X-RateLimit-*`)

60. **Error Handling:**
    - JSON estruturado:
      ```json
      {
        "error": {
          "code": "INVALID_INPUT",
          "message": "Email is required",
          "field": "email",
          "request_id": "abc123"
        }
      }
      ```
    - NUNCA expor stack traces
    - Logs detalhados no servidor
    - Mensagens i18n (múltiplos idiomas)

### **Autenticação**

61. **API Keys:**

    - JWT em header: `Authorization: Bearer <token>`
    - Validação em TODOS os endpoints (exceto públicos)
    - Expiration obrigatória (24h max)
    - Refresh tokens para renovação
    - Revogação imediata em logout

62. **OAuth2 (Future):**
    - Authorization Code Flow para terceiros
    - Scopes granulares por recurso
    - Consent screen obrigatório
    - Audit de aplicações autorizadas

### **Rate Limiting**

63. **Limites por Endpoint:**
    - `/api/v1/auth/login`: 5/15min (anti brute-force)
    - `/api/v1/events`: 100/min
    - `/api/v1/search`: 50/min
    - Outros: 100/min (default)
    - Admin bypass se necessário

---

## 🚀 REGRAS DE DEPLOY

### **CI/CD**

64. **Pre-Deploy Checks:**

    - Tests devem passar (quando implementados)
    - Linting sem erros (flake8, pylint)
    - Security scan (pip-audit, bandit)
    - Migrations validadas
    - Rollback plan documentado

65. **Deploy Strategy:**

    - Blue-Green deployment (zero downtime)
    - Canary releases para features críticas (10% → 50% → 100%)
    - Health checks antes de switch
    - Rollback automático em falha
    - Alertas em Discord/Slack

66. **Environment Separation:**
    - Dev → Staging → Production
    - Dados de produção NUNCA em dev
    - Secrets diferentes por ambiente
    - Access control por ambiente
    - Monitoring separado

### **Monitoring**

67. **Metrics:**

    - Uptime: 99.9% SLA
    - Response time: <500ms p95
    - Error rate: <0.1%
    - CPU/Memory/Disk tracking
    - Database connections/queries

68. **Alerting:**

    - Downtime: Alerta imediato
    - High error rate (>1%): 5 min
    - Slow queries (>5s): 15 min
    - Pool exhaustion: Imediato
    - Security events: Imediato

69. **Incident Response:**
    - On-call rotation (se aplicável)
    - Runbooks para incidentes comuns
    - Post-mortem obrigatório para outages
    - RCA (Root Cause Analysis) documentada
    - Action items para prevenir recorrência

---

## 📚 RESUMO DE PRIORIDADES

### **Crítico (Nunca Ignorar):**

- Multi-tenant isolation (tenant_id)
- SQL injection prevention (ORM only)
- Authentication/Authorization (JWT + RBAC)
- Secrets management (nunca no código)
- Audit logging (ações críticas)
- GDPR compliance (data privacy)

### **Importante (Seguir Sempre):**

- Input validation (client + server)
- Rate limiting (APIs críticas)
- Error handling (não expor detalhes)
- Performance monitoring (slow queries)
- Backup automático (1x dia)

### **Recomendado (Quando Possível):**

- Code review antes de merge
- Security scanning (CI/CD)
- Load testing antes de prod
- Documentation updates
- Refactoring regular

---

## 🔄 EVOLUÇÃO DESTE DOCUMENTO

Este ficheiro deve ser atualizado sempre que:

- Novas vulnerabilidades forem descobertas
- Compliance requirements mudarem
- Novas features de segurança forem adicionadas
- Post-mortems revelarem gaps

**Responsável:** Bruno Coelho  
**Review:** Trimestral (Março, Junho, Setembro, Dezembro)

---

**💡 NOTA FINAL:** Estas regras existem para proteger os dados dos nossos clientes. Segurança não é opcional - é responsabilidade de TODOS os desenvolvedores. Em caso de dúvida, SEMPRE perguntar antes de implementar.
