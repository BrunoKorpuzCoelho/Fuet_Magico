# 🎨 Sistema de Ícones SVG Customizáveis

## 🎯 **CONCEITO**

O sistema de ícones do Fuet Mágico suporta **3 tipos diferentes** de ícones, dando total flexibilidade:

1. ✅ **FontAwesome** - Biblioteca de ícones (ex: `fa-phone`)
2. ✅ **Emoji** - Unicode emojis (ex: `📞`)
3. 🎨 **SVG Customizado** - **NOVO!** SVG inline com cor dinâmica via `currentColor`

---

## 🔧 **COMO FUNCIONA**

### **Prioridade de Renderização:**
```
1. icon_svg  → Se preenchido, usa SVG com icon_color
2. icon      → FontAwesome ou Emoji
3. fallback  → Emoji padrão do activity_type
```

### **Campos no Modelo:**
```python
class ActivityTemplate:
    # Opção 1 ou 2
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='FontAwesome (fa-phone) ou Emoji (📞)'
    )
    
    # Opção 3 (MELHOR!)
    icon_svg = models.TextField(
        blank=True,
        help_text='SVG inline com currentColor'
    )
    
    icon_color = models.CharField(
        max_length=7,
        default='#6366F1',
        help_text='Cor do ícone em hexadecimal'
    )
```

---

## 📝 **EXEMPLOS DE USO**

### **Opção 1: FontAwesome**
```python
template = ActivityTemplate.objects.create(
    name='Call Template',
    activity_type='CALL',
    icon='fa-phone',           # ← FontAwesome class
    icon_color='#10B981',       # ← Cor verde
)

# HTML gerado:
# <i class="fa-phone" style="font-size: 24px; color: #10B981;"></i>
```

### **Opção 2: Emoji**
```python
template = ActivityTemplate.objects.create(
    name='Email Template',
    activity_type='EMAIL',
    icon='📧',  # ← Emoji direto
)

# HTML gerado:
# <span style="font-size: 24px;">📧</span>
```

### **Opção 3: SVG Customizado** 🎨 **NOVO!**
```python
# SVG de um telefone customizado
phone_svg = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
</svg>
'''

template = ActivityTemplate.objects.create(
    name='Premium Call',
    activity_type='CALL',
    icon_svg=phone_svg,         # ← SVG inline
    icon_color='#FF5733',       # ← Cor vermelha
)

# HTML gerado:
# <span style="display: inline-block; width: 24px; height: 24px; color: #FF5733;">
#   <svg>...</svg>
# </span>
```

---

## 🎨 **VANTAGENS DO SVG**

### **1. Cores Dinâmicas com `currentColor`**
```html
<!-- SVG usa currentColor -->
<svg>
  <path fill="currentColor" d="..." />
</svg>

<!-- CSS aplica cor via color property -->
<span style="color: #FF5733;">
  <!-- SVG herda a cor #FF5733 automaticamente -->
</span>
```

### **2. Qualidade Perfeita em Qualquer Tamanho**
```python
# Pequeno (16px)
template.get_rendered_icon(size='16px')

# Médio (24px) - padrão
template.get_rendered_icon(size='24px')

# Grande (48px)
template.get_rendered_icon(size='48px')

# SVG escala sem perder qualidade!
```

### **3. Customização Total**
```python
# Ícone personalizado para empresa específica
custom_svg = '''
<svg viewBox="0 0 24 24">
  <path fill="currentColor" d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
  <text x="7" y="16" fill="white" font-size="10">FM</text>
</svg>
'''

company_template = ActivityTemplate.objects.create(
    name='Fuet Mágico VIP Call',
    icon_svg=custom_svg,
    icon_color='#6366F1',  # Brand color
)
```

---

## 🌈 **PALETA DE CORES SUGERIDA**

```python
# Cores por tipo de activity
ACTIVITY_COLORS = {
    'CALL': '#10B981',       # Verde - Success
    'EMAIL': '#3B82F6',      # Azul - Info
    'MEETING': '#8B5CF6',    # Roxo - Important
    'TODO': '#F59E0B',       # Laranja - Warning
    'WHATSAPP': '#22C55E',   # Verde WhatsApp
    'DOCUMENT': '#6366F1',   # Indigo - Neutral
    'SIGNATURE': '#EF4444',  # Vermelho - Urgent
}

# Criar template com cor sugerida
template = ActivityTemplate.objects.create(
    activity_type='CALL',
    icon_svg=call_svg,
    icon_color=ACTIVITY_COLORS['CALL'],
)
```

---

## 📦 **BIBLIOTECA DE SVGs PRONTOS**

### **Telefone (Call)**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
</svg>
```

### **Email**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
  <polyline points="22,6 12,13 2,6"/>
</svg>
```

### **Meeting (Calendário)**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
  <line x1="16" y1="2" x2="16" y2="6"/>
  <line x1="8" y1="2" x2="8" y2="6"/>
  <line x1="3" y1="10" x2="21" y2="10"/>
</svg>
```

### **Todo (Checkbox)**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M9 11l3 3L22 4"/>
  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>
</svg>
```

### **WhatsApp**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
</svg>
```

### **Document (Arquivo)**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
  <polyline points="14 2 14 8 20 8"/>
  <line x1="16" y1="13" x2="8" y2="13"/>
  <line x1="16" y1="17" x2="8" y2="17"/>
  <polyline points="10 9 9 9 8 9"/>
</svg>
```

### **Signature (Assinatura)**
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
</svg>
```

---

## 🛠️ **FERRAMENTAS PARA CRIAR SVGs**

### **1. Heroicons** (Recomendado!)
- URL: https://heroicons.com/
- Estilo: Outline (stroke) e Solid (fill)
- Licença: MIT (grátis para uso comercial)
- **Já usa `currentColor` por padrão!**

### **2. Feather Icons**
- URL: https://feathericons..com/
- Estilo: Outline apenas
- Super leves e limpos

### **3. Lucide Icons**
- URL: https://lucide.dev/
- Fork melhorado do Feather
- Mais ícones

### **4. Converter FontAwesome para SVG**
- Copiar SVG do site oficial
- Substituir cores fixas por `currentColor`

---

## 🎯 **EXEMPLO COMPLETO: Template com SVG**

```python
from apps.core.models import ActivityTemplate

# SVG do Heroicons (Phone icon)
phone_svg = '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" />
</svg>'''

# Criar template
template = ActivityTemplate.objects.create(
    name='VIP Client Call',
    activity_type='CALL',
    default_summary='Ligar para {{contact_name}} - VIP',
    due_days_offset=1,
    
    # SVG customizado com cor brand
    icon_svg=phone_svg,
    icon_color='#6366F1',  # Indigo-500
    
    decoration_type='success',
)

# Renderizar o ícone
html = template.get_rendered_icon(size='32px')
print(html)
# <span style="display: inline-block; width: 32px; height: 32px; color: #6366F1;">
#   <svg>...</svg>
# </span>
```

---

## 🎨 **USO EM TEMPLATES HTML**

```django
<!-- Template Django -->
<div class="activity-item">
    <!-- Renderizar ícone dinamicamente -->
    {{ template.get_rendered_icon|safe }}
    
    <span>{{ template.name }}</span>
</div>

<!-- OU com tamanho customizado -->
<div class="activity-card">
    {{ template.get_rendered_icon('48px')|safe }}
</div>

<!-- OU inline em Alpine.js -->
<div x-html="activityTemplate.icon_html"></div>
```

---

## 📊 **COMPARAÇÃO: 3 Opções**

| Tipo | Exemplo | Vantagens | Desvantagens |
|------|---------|-----------|--------------|
| **FontAwesome** | `fa-phone` | Biblioteca grande, fácil | Precisa importar CSS, limitado |
| **Emoji** | `📞` | Zero dependências, universal | Varia por OS, sem controle de cor |
| **SVG** | `<svg>...</svg>` | **Cor dinâmica, qualidade perfeita, customizável** | SVG inline pode ser grande |

**RECOMENDAÇÃO:** Use **SVG** para projetos profissionais! 🎨

---

## 🚀 **PRÓXIMO PASSO**

Agora que temos o sistema de ícones SVG, podemos:

1. ✅ Criar biblioteca de SVGs padrão
2. ✅ Adicionar no Django Admin interface para upload de SVG
3. ✅ Color picker no Admin para escolher cor
4. ✅ Preview do ícone em tempo real

**Feature EXCLUSIVA do Fuet Mágico!** Odoo não tem isso! 🏆

---

**Criado por:** GitHub Copilot  
**Data:** 17 de Fevereiro de 2026  
**Versão:** 1.0 - Sistema de Ícones SVG Customizáveis
