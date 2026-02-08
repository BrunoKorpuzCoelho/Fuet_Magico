# 🚀 FUET MÁGICO - DEPLOYMENT GUIDE

> **Última atualização:** 08/02/2026  
> **Versão:** 1.0  
> **Stack:** Django 5.0, PostgreSQL 17, Redis, Celery

---

## 📋 PRÉ-REQUISITOS

Antes de começar, certifica-te que tens instalado:
- ✅ Python 3.12+
- ✅ PostgreSQL 17+
- ✅ Redis (via WSL ou Windows)
- ✅ Git

---

## 🗄️ 1. CONFIGURAÇÃO DA BASE DE DADOS

### **1.1. Criar Base de Dados PostgreSQL**

```sql
-- Conectar ao PostgreSQL como superuser
psql -U postgres

-- Criar database
CREATE DATABASE fuet_magico_db;

-- Criar user
CREATE USER cubix WITH PASSWORD 'cubix123';

-- Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE fuet_magico_db TO cubix;

-- Conectar à database e conceder schema permissions
\c fuet_magico_db
GRANT ALL ON SCHEMA public TO cubix;

-- Sair
\q
```

### **1.2. Configurar Variáveis de Ambiente**

Criar/editar arquivo `.env` na raiz do projeto:

```bash
# Database
DATABASE_URL=postgresql://cubix:cubix123@localhost:5432/fuet_magico_db

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_MAX_CONNECTIONS=10

# Django
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,cubixtest.pt,www.cubixtest.pt

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

## 🔧 2. MIGRAÇÕES E ESTRUTURA DE TABELAS

### **2.1. Executar Migrations**

```bash
# Verificar migrations pendentes
python manage.py showmigrations

# Criar migrations (se houver alterações nos models)
python manage.py makemigrations

# Aplicar todas as migrations
python manage.py migrate

# Verificar se tudo foi aplicado
python manage.py showmigrations
```

**Saída esperada:**
```
accounts
 [X] 0001_initial
 [X] 0002_customuser_companies_customuser_default_company
contacts
 [X] 0001_initial
 [X] 0002_contact_country_contact_district_contact_language_and_more
 [X] 0003_contacttag_remove_contact_tags_contact_tags
core
 [X] 0001_initial
 [X] 0002_errorlog
 [X] 0003_company
dashboard
 [X] 0001_initial
```

---

## 🏢 3. CRIAR DADOS DEFAULT (SEEDS)

> **💡 Sobre Grupos/Roles:**  
> O sistema usa **3 roles fixas**: ADMIN, MANAGER, EMPLOYEE  
> Estas roles **já existem automaticamente** como choices do campo `role` no modelo CustomUser.  
> **Não são Django Groups** - são valores fixos no código, não precisam de seed.

### **3.1. Criar Company Default**

```bash
python manage.py create_default_company
```

**O que cria:**
- ✅ Empresa: "Fuet Mágico"
- ✅ Nome Legal: "Fuet Mágico, Lda."
- ✅ Moeda: EUR
- ✅ Língua: pt_PT
- ✅ País: Portugal

**Saída esperada:**
```
Successfully created default company: Fuet Mágico (ID: d14231df-6335-4659-bb17-d97cf6d53029)
You can now configure additional details in Django Admin.
```

### **3.2. Criar Users Default**

```bash
python manage.py create_default_users
```

**O que cria:**
- ✅ **Admin User:**
  - Username: `cubix`
  - Password: `cubix123`
  - Email: admin@fuetmagico.pt
  - Role: Administrator (superuser)
  - Acesso total ao sistema

- ✅ **Manager User:**
  - Username: `daisy`
  - Password: `torres`
  - Email: manager@fuetmagico.pt
  - Role: Manager (staff)
  - Acesso ao Django Admin

**Saída esperada:**
```
============================================================
DEFAULT USERS CREATED SUCCESSFULLY
============================================================
  • Admin: cubix
  • Manager: daisy
============================================================

⚠️  IMPORTANT: Change these passwords in production!
```

> **💡 Nota sobre Grupos/Roles:**  
> Os "grupos" (ADMIN, MANAGER, EMPLOYEE) **já existem automaticamente** no sistema.  
> São choices fixas do campo `role` no modelo CustomUser - não precisam de seed separada.

### **3.3. Personalizar Users Default (Opcional)**

```bash
# Criar com usernames/passwords customizados
python manage.py create_default_users \
  --admin-username=seuadmin \
  --admin-password=SuaSenhaSegura123! \
  --manager-username=seugert \
  --manager-password=OutraSenhaSegura456!
```

---

## 📂 4. ARQUIVOS ESTÁTICOS E MEDIA

### **4.1. Coletar Static Files**

```bash
# Coletar todos os arquivos estáticos
python manage.py collectstatic --noinput

# Verificar criação
ls -la staticfiles/
```

### **4.2. Criar Diretórios Media**

```bash
# Criar estruturas de pastas
mkdir -p media/documents
mkdir -p media/products
mkdir -p media/uploads
mkdir -p media/companies/logos
mkdir -p media/avatars
```

---

## 🔄 5. CELERY (OPCIONAL - SE USAR TASKS ASSÍNCRONAS)

### **5.1. Iniciar Redis**

```bash
# WSL Ubuntu
sudo service redis-server start

# Verificar
redis-cli ping
# Output esperado: PONG
```

### **5.2. Iniciar Celery Worker**

```bash
# Em terminal separado
celery -A config worker --loglevel=info --pool=solo
```

### **5.3. Iniciar Celery Beat (Tarefas Agendadas)**

```bash
# Em terminal separado
celery -A config beat --loglevel=info
```

---

## 🧪 6. VERIFICAÇÃO FINAL

### **6.1. Testar Servidor Django**

```bash
python manage.py runserver 0.0.0.0:8000
```

Acessar: http://localhost:8000

### **6.2. Checklist de Testes**

- [ ] **Homepage:** http://localhost:8000/ (deve mostrar website)
- [ ] **Admin:** http://localhost:8000/admin/ 
  - [ ] Login com `cubix / cubix123`
  - [ ] Verificar Company "Fuet Mágico" existe
  - [ ] Verificar 2 users (cubix, daisy)
- [ ] **Dashboard:** http://localhost:8000/dashboard/
  - [ ] Login redireciona para dashboard
  - [ ] Smart buttons mostram contadores
- [ ] **Contactos:** http://localhost:8000/contacts/
  - [ ] Lista vazia (normal em fresh install)
  - [ ] Botão "Novo Contacto" funciona
- [ ] **Logs do Sistema:** http://localhost:8000/devtools/logs/application/
  - [ ] Dropdown DevTools no navbar
  - [ ] Logs aparecem em tempo real

---

## 🔐 7. SEGURANÇA - PRODUÇÃO

### **7.1. Alterar Passwords Default**

```bash
# Acessar Django shell
python manage.py shell

# Alterar password do admin (cubix)
from django.contrib.auth import get_user_model
User = get_user_model()
admin = User.objects.get(username='cubix')
admin.set_password('NovaSenhaSegura123!')
admin.save()

# Alterar password do manager (daisy)
manager = User.objects.get(username='daisy')
manager.set_password('OutraSenhaSegura456!')
manager.save()
```

### **7.2. Configurar .env para Produção**

```bash
# .env (PRODUÇÃO)
DEBUG=False
SECRET_KEY=generate-new-secret-key-here
ALLOWED_HOSTS=fuetmagico.pt,www.fuetmagico.pt

# Database (usar SSL)
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require

# Redis (usar senha)
REDIS_URL=redis://:senha@host:6379/0
```

### **7.3. Gerar Nova SECRET_KEY**

```bash
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 📝 8. COMANDOS ÚTEIS DE MANUTENÇÃO

### **8.1. Backup Database**

```bash
# PostgreSQL dump
pg_dump -U cubix -d fuet_magico_db -F c -f backup_$(date +%Y%m%d).dump

# Restaurar backup
pg_restore -U cubix -d fuet_magico_db -c backup_20260208.dump
```

### **8.2. Limpar Logs Antigos**

```bash
# Limpar logs com mais de 30 dias
find logs/ -name "*.log" -mtime +30 -delete
```

### **8.3. Verificar Estado Geral**

```bash
# Ver migrations pendentes
python manage.py showmigrations | grep "\[ \]"

# Check do sistema
python manage.py check

# Verificar configurações
python manage.py diffsettings
```

---

## 🆘 9. TROUBLESHOOTING

### **Erro: "database does not exist"**
```bash
# Criar database manualmente
createdb -U postgres fuet_magico_db
```

### **Erro: "relation does not exist"**
```bash
# Limpar migrations e recriar
python manage.py migrate --fake-initial
```

### **Erro: "Company matching query does not exist"**
```bash
# Executar create_default_company
python manage.py create_default_company
```

### **Redis não conecta (Windows)**
```bash
# Iniciar Redis via WSL
wsl
sudo service redis-server start
```

---

## 🔄 10. ATUALIZAÇÕES FUTURAS

### **Quando adicionar novos models/apps:**

1. Criar migrations:
   ```bash
   python manage.py makemigrations nome_do_app
   ```

2. Aplicar migrations:
   ```bash
   python manage.py migrate nome_do_app
   ```

3. Se criar seeds/fixtures:
   ```bash
   python manage.py loaddata nome_do_app/fixtures/data.json
   ```

### **Quando adicionar novos comandos de seed:**

- Documentar aqui na secção 3 (Criar Dados Default)
- Adicionar ao checklist de deployment
- Testar em fresh install

---

## 📞 SUPORTE

**Problemas?** Verificar:
1. Logs do Django: `logs/django.log`
2. Logs de erro: `/devtools/logs/error/`
3. Console do terminal onde runserver está ativo

**Comandos de diagnóstico:**
```bash
python manage.py check
python manage.py showmigrations
python manage.py dbshell  # Acesso direto ao PostgreSQL
```

---

## ✅ CHECKLIST COMPLETO DE DEPLOYMENT

- [ ] PostgreSQL database criada
- [ ] Arquivo .env configurado
- [ ] Migrations aplicadas (`migrate`)
- [ ] Company default criada (`create_default_company`)
- [ ] Users default criados (`create_default_users`)
- [ ] Static files coletados (`collectstatic`)
- [ ] Diretórios media criados
- [ ] Redis iniciado (se usar Celery)
- [ ] Servidor Django funciona (`runserver`)
- [ ] Login admin funciona
- [ ] Dashboard acessível
- [ ] Passwords alterados (produção)

---

**Status:** ✅ Sistema pronto para usar!  
**Próximos passos:** Criar contactos, configurar empresa, adicionar produtos...
