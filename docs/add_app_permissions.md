# Como Adicionar Permissões a uma Nova App ou Modelo

Guia passo a passo para registar uma nova aplicação (ex: Vendas) e os seus modelos no sistema de permissões.

---

## Contexto

O sistema de permissões tem dois registos em `apps/accounts/models.py`:

| Registo | Para quê |
|---|---|
| `APP_REGISTRY` | Controla se o tile aparece no dashboard e define o nível geral (user/manager/admin) |
| `APP_MODELS_REGISTRY` | Controla as permissões CRUD por tabela (Ver / Criar / Editar / Apagar) |

---

## Passo 1 — Criar a app Django (se ainda não existir)

```bash
python manage.py startapp sales
```

Registar em `config/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'apps.sales',
]
```

---

## Passo 2 — Criar os modelos

Em `apps/sales/models.py`, criar os modelos normalmente. O Django gera as 4 permissões CRUD automaticamente na próxima migração.

```python
from apps.core.models import AbstractBaseModel

class SaleOrder(AbstractBaseModel):
    # campos...
    class Meta:
        verbose_name = 'Encomenda de Venda'
        verbose_name_plural = 'Encomendas de Venda'

class SaleOrderLine(AbstractBaseModel):
    # campos...
    class Meta:
        verbose_name = 'Linha de Encomenda'
        verbose_name_plural = 'Linhas de Encomenda'
```

---

## Passo 3 — Correr as migrações

```bash
python manage.py makemigrations sales
python manage.py migrate
```

Após o `migrate`, o Django insere automaticamente na tabela `auth_permission`:
```
sales | saleorder     | Can view sale order
sales | saleorder     | Can add sale order
sales | saleorder     | Can change sale order
sales | saleorder     | Can delete sale order
sales | saleorderline | Can view sale order line
...
```

---

## Passo 4 — Registar no `APP_REGISTRY`

Em `apps/accounts/models.py`, adicionar o slug da nova app à lista:

```python
APP_REGISTRY = [
    ('crm',       'CRM / Leads & Pipeline'),
    ('contacts',  'Contactos'),
    ...
    ('sales',     'Vendas'),          # ← adicionar aqui
]
```

Isto faz aparecer o tile "Vendas" no dashboard (filtrado por AppRole) e adiciona a linha no selector de permissões de aplicação no perfil do utilizador.

---

## Passo 5 — Registar os modelos no `APP_MODELS_REGISTRY`

No mesmo ficheiro, adicionar uma entrada no dicionário:

```python
APP_MODELS_REGISTRY = {
    'crm': [...],
    'contacts': [...],

    'sales': [                                           # ← adicionar aqui
        # formato: (app_label, model_name, nome display)
        # app_label  = nome da app Django (pasta em apps/)
        # model_name = nome do modelo em MINÚSCULAS (como fica na auth_permission)
        ('sales', 'saleorder',     'Encomendas de Venda'),
        ('sales', 'saleorderline', 'Linhas de Encomenda'),
    ],
}
```

**Regra para o `model_name`**: é sempre o nome da classe em minúsculas sem espaços.
- `SaleOrder` → `saleorder`
- `SaleOrderLine` → `saleorderline`
- `CRMStage` → `crmstage`

Para confirmar o nome exacto que o Django usa:

```bash
python manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.filter(app_label='sales').values('model')
```

---

## Passo 6 — Registar o tile no dashboard

Em `apps/dashboard/views.py`, adicionar à lista `_APP_TILES`:

```python
_APP_TILES = [
    ...
    {'slug': 'sales', 'name': 'Vendas', 'icon': '💰', 'url_name': 'sales:index'},
    # ou se a URL ainda não existir:
    {'slug': 'sales', 'name': 'Vendas', 'icon': '💰', 'url_name': None, 'url': '#'},
]
```

---

## Passo 7 — Proteger as views com os decorators

Nas views da nova app, usar os helpers de `apps.accounts.decorators`:

```python
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import require_app_role, has_app_access

# Nível mínimo para entrar na app
@login_required
@require_app_role('sales', min_level='user')
def sale_order_list(request):
    # Filtrar por owner se for 'user', mostrar todos se for 'manager'/'admin'
    from apps.accounts.decorators import get_app_role
    company_id = request.session.get('active_company_id')
    level = get_app_role(request.user, 'sales', company_id)

    if level == 'user':
        orders = SaleOrder.objects.filter(owner=request.user)
    else:
        orders = SaleOrder.objects.all()
    ...

# Configurações — só manager e acima
@login_required
@require_app_role('sales', min_level='manager')
def sales_settings(request):
    ...
```

Nos templates, para ocultar botões:

```html
<!-- Só mostra "Criar" se o utilizador tiver permissão add_saleorder -->
{% if perms.sales.add_saleorder %}
<a href="{% url 'sales:create' %}">Nova Encomenda</a>
{% endif %}

<!-- Só mostra "Apagar" se tiver permissão delete_saleorder -->
{% if perms.sales.delete_saleorder %}
<button>Apagar</button>
{% endif %}
```

---

## Checklist resumida

```
[ ] 1. Criar app Django + registar em INSTALLED_APPS
[ ] 2. Criar modelos com class Meta adequada
[ ] 3. makemigrations + migrate
[ ] 4. Adicionar slug a APP_REGISTRY        (accounts/models.py)
[ ] 5. Adicionar modelos a APP_MODELS_REGISTRY  (accounts/models.py)
[ ] 6. Adicionar tile a _APP_TILES          (dashboard/views.py)
[ ] 7. Decorar views com @require_app_role
[ ] 8. Usar {% if perms.app.action_model %} nos templates
```
