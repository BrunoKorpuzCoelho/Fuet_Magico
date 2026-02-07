# Default Avatar Images

Esta pasta contém imagens SVG de avatar padrão para diferentes tipos de contactos no sistema Fuet Mágico.

## 📁 Estrutura de Ficheiros

### Avatares por Categoria de Contacto
- **`default-person.svg`** - Avatar padrão para contactos do tipo PESSOA
  - Ícone: Silhueta de pessoa
  - Uso: `contact.contact_category == 'PERSON'`

- **`default-company.svg`** - Avatar padrão para contactos do tipo EMPRESA
  - Ícone: Edifício com janelas
  - Uso: `contact.contact_category == 'COMPANY'`

### Avatares por Tipo de Contacto
- **`default-client.svg`** - Avatar padrão para CLIENTES
  - Ícone: Saco de compras
  - Uso: `contact.contact_type == 'CLIENT'`

- **`default-supplier.svg`** - Avatar padrão para FORNECEDORES
  - Ícone: Caixa de entrega
  - Uso: `contact.contact_type == 'SUPPLIER'`

### Avatares por Função (Futuro)
- **`default-billing.svg`** - Avatar para contactos de faturação
  - Ícone: Documento/fatura com símbolo €
  - Uso futuro: Quando implementar contactos de faturação

- **`default-shipping.svg`** - Avatar para contactos de entrega
  - Ícone: Camião de entregas
  - Uso futuro: Quando implementar contactos de entrega

- **`default-other.svg`** - Avatar genérico para outros tipos
  - Ícone: Livro de contactos
  - Uso: Fallback genérico

## 🎨 Design System

Todas as imagens seguem o design system do projeto:

### Cores Utilizadas
- **Dourado primário**: `#dbc693`
- **Dourado escuro**: `#c9b580`
- **Background**: `#1f2937` (gray-800)
- **Detalhes**: `#4b5563` (gray-600), `#9ca3af` (gray-400)

### Especificações Técnicas
- **Formato**: SVG (vetorial, escalável)
- **Dimensões**: 120x120px (viewBox)
- **Forma**: Círculo de fundo + ícone centrado
- **Otimização**: Código SVG limpo e minimalista

## 💡 Como Usar

### Em Templates Django
```django
{% if contact.avatar %}
    <img src="{{ contact.avatar.url }}" alt="{{ contact.name }}">
{% elif contact.contact_category == 'PERSON' %}
    <img src="{% static 'images/avatars/defaults/default-person.svg' %}" alt="Person">
{% elif contact.contact_category == 'COMPANY' %}
    <img src="{% static 'images/avatars/defaults/default-company.svg' %}" alt="Company">
{% else %}
    <img src="{% static 'images/avatars/defaults/default-other.svg' %}" alt="Contact">
{% endif %}
```

### Em Python (Model Method)
```python
# apps/contacts/models.py
class Contact(AbstractBaseModel):
    # ... campos existentes ...
    
    def get_avatar_url(self):
        """Retorna URL do avatar (upload ou default)"""
        if self.avatar:
            return self.avatar.url
        
        # Default baseado na categoria
        if self.contact_category == 'PERSON':
            return '/static/images/avatars/defaults/default-person.svg'
        elif self.contact_category == 'COMPANY':
            return '/static/images/avatars/defaults/default-company.svg'
        
        # Default baseado no tipo
        if self.contact_type == 'CLIENT':
            return '/static/images/avatars/defaults/default-client.svg'
        elif self.contact_type == 'SUPPLIER':
            return '/static/images/avatars/defaults/default-supplier.svg'
        
        # Fallback genérico
        return '/static/images/avatars/defaults/default-other.svg'
```

### Em JavaScript
```javascript
function getContactAvatar(contact) {
    if (contact.avatar) {
        return contact.avatar;
    }
    
    const defaults = {
        'PERSON': '/static/images/avatars/defaults/default-person.svg',
        'COMPANY': '/static/images/avatars/defaults/default-company.svg',
        'CLIENT': '/static/images/avatars/defaults/default-client.svg',
        'SUPPLIER': '/static/images/avatars/defaults/default-supplier.svg',
    };
    
    return defaults[contact.contact_category] 
        || defaults[contact.contact_type] 
        || '/static/images/avatars/defaults/default-other.svg';
}
```

## 🔄 Prioridade de Seleção

Ordem recomendada para escolher o avatar:
1. **Avatar custom** (se o contacto fez upload)
2. **Categoria** (PERSON vs COMPANY)
3. **Tipo** (CLIENT vs SUPPLIER vs BOTH)
4. **Fallback** (default-other.svg)

## 📝 Notas
- Imagens SVG ocupam ~1-2KB cada (muito leve!)
- Escaláveis sem perda de qualidade
- Podem ser coloridas dinamicamente via CSS se necessário
- Background circular garante consistência visual
