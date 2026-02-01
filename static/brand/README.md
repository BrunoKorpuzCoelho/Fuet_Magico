# Brand Assets - Guia de Utilização

Este documento explica quando e como utilizar cada tipo de ficheiro de marca disponível nesta pasta.

---

## 📁 Estrutura de Ficheiros

```
brand/
├── logos/
│   ├── vector/         → Ficheiro original vetorizado (.ai)
│   ├── png/            → Logos PNG para web
│   ├── png-hd/         → Logos PNG alta resolução
│   └── jpg/            → Logos JPG comprimidos
└── watermarks/
    ├── white/          → Marcas d'água brancas
    ├── color/          → Marcas d'água a cores
    └── black/          → Marcas d'água pretas
```

---

## 🎨 Tipos de Ficheiros

### 1. **Vector (.ai) - Adobe Illustrator**

**O que é:** Ficheiro **vetorizado** criado no Adobe Illustrator. É o ficheiro ORIGINAL de onde todos os outros formatos são exportados.

**Características:**
- ✅ **Escalável infinitamente** sem perder qualidade
- ✅ Pode ser redimensionado para qualquer tamanho (desde cartão de visita até outdoor)
- ✅ Editável (pode alterar cores, formas, textos)
- ✅ Qualidade perfeita para impressão profissional
- ❌ Precisa de Adobe Illustrator ou software compatível para abrir
- ❌ Não funciona diretamente em websites

**Quando usar:**
- Enviar para gráficas/impressoras profissionais
- Criar novos materiais de marca (banners, outdoors, flyers)
- Redimensionar logos para qualquer tamanho
- Alterar cores ou fazer adaptações da marca
- **NUNCA apagar este ficheiro** - é o ficheiro MASTER da marca

**Exemplo prático:**
- Cliente pede logo para imprimir num outdoor de 3x2 metros → usar .ai
- Gráfica pede ficheiro para imprimir cartões de visita → usar .ai
- Precisas de alterar a cor do logo → usar .ai

---

### 2. **PNG (Portable Network Graphics)**

**O que é:** Formato de imagem digital com **fundo transparente**.

**Características:**
- ✅ Fundo transparente (permite sobrepor em qualquer cor)
- ✅ Boa qualidade visual
- ✅ Funciona em todos os browsers e dispositivos
- ✅ Tamanho médio de ficheiro (56-82 KB)
- ✅ Suporta transparência (melhor que JPG)
- ❌ Não é vetorizado (perde qualidade se aumentar muito)

**Quando usar:**
- Website (favicon, logos no header/footer)
- Redes sociais (perfil, posts)
- Apresentações PowerPoint/Google Slides
- Documentos digitais (Word, PDF)
- Emails marketing
- Assinaturas de email

**Exemplo prático:**
- Colocar logo no topo do website → usar PNG
- Adicionar logo a um post de Instagram → usar PNG
- Inserir logo numa apresentação → usar PNG

---

### 3. **PNG-HD (Alta Resolução)**

**O que é:** PNG com **maior resolução** e qualidade superior.

**Características:**
- ✅ Fundo transparente
- ✅ **Alta resolução** (426-617 KB - 5x maior que PNG normal)
- ✅ Qualidade superior para impressões
- ✅ Mantém detalhes em tamanhos médios
- ❌ Ficheiros maiores (carrega mais lento)
- ❌ Não é vetorizado

**Quando usar:**
- Impressões em **alta qualidade** (flyers, posters A4/A3)
- Materiais promocionais físicos
- Mockups de produtos
- Casos onde PNG normal fica pixelizado
- Banners digitais grandes
- **NÃO usar no website** (muito pesado, usa PNG normal)

**Exemplo prático:**
- Imprimir flyer A4 numa impressora a cores → usar PNG-HD
- Criar mockup de uma t-shirt → usar PNG-HD
- Poster para loja → usar PNG-HD (ou melhor ainda, .ai)

---

### 4. **JPG (JPEG - Joint Photographic Experts Group)**

**O que é:** Formato **comprimido** para imagens, sem transparência.

**Características:**
- ✅ Tamanho pequeno de ficheiro (182-312 KB)
- ✅ Carrega rápido
- ✅ Compatível com tudo
- ❌ **SEM transparência** (fundo branco)
- ❌ Perde qualidade com compressão
- ❌ Não recomendado para logos (usar PNG)

**Quando usar:**
- Situações onde **não tens suporte para PNG**
- Precises de **ficheiros mais leves**
- Enviar por email com limitações de tamanho
- Plataformas antigas que não aceitam PNG
- **RARAMENTE** - prefere sempre PNG quando possível

**Exemplo prático:**
- Sistema antigo só aceita JPG → usar JPG
- Email com limite de 1MB → usar JPG
- **Na maioria dos casos: NÃO USAR** (PNG é melhor)

---

## 💧 Marcas d'Água (Watermarks)

As marcas d'água são versões **semi-transparentes** do logo para proteger documentos.

### Tipos de Marcas d'Água

| Tipo | Quando Usar | Exemplo Prático |
|------|-------------|-----------------|
| **White (Branco)** | Documentos com **fundo escuro** | PDF com fundo preto, apresentações dark mode |
| **Color (Cores)** | Documentos com **fundo claro** | Orçamentos, faturas, propostas em branco |
| **Black (Preto)** | Documentos com **fundo branco** puro | Contratos, documentos oficiais, certificados |

**Quando usar marcas d'água:**
- Faturas e orçamentos (proteger documentos)
- Propostas comerciais
- Relatórios financeiros
- Certificados
- Documentos gerados automaticamente em PDF
- Proteger imagens de produtos antes da venda

**Como usar no código:**
```python
# Exemplo: Adicionar marca d'água a PDF
watermark_path = 'static/brand/watermarks/color/watermark-logo-primary.png'
```

---

## 🎯 Resumo Rápido: Qual Usar?

| Situação | Ficheiro Recomendado | Porquê |
|----------|---------------------|---------|
| Website (header, footer) | **PNG** | Transparente, leve, rápido |
| Redes sociais | **PNG** | Transparente, boa qualidade |
| Email marketing | **PNG** | Compatível, boa qualidade |
| Impressão profissional | **.AI** | Vetorizado, qualidade infinita |
| Flyer/Poster A4 | **PNG-HD** ou **.AI** | Alta resolução |
| Outdoor/Banner grande | **.AI** | Única opção com qualidade |
| Editar o logo | **.AI** | Formato editável |
| PDF (marca d'água) | **Watermark** | Proteger documentos |
| Sistema antigo | **JPG** | Última opção |

---

## ⚠️ Regras Importantes

1. **NUNCA apagar o ficheiro .ai** - é o ficheiro original da marca
2. **Website sempre PNG** (não PNG-HD, é muito pesado)
3. **Impressão profissional sempre .ai** (gráficas pedem vetorizado)
4. **JPG é última opção** - só se não houver alternativa
5. **Marcas d'água para PDFs** - proteger documentos oficiais

---

## 📋 Ficheiros Disponíveis

### Logos (4 variações)
- `logo-primary` - Logo principal completo
- `logo-secondary` - Logo alternativo
- `logo-sub-brand` - Logo de sub-marca
- `logo-icon` - Ícone/favicon

### Formatos disponíveis por logo
- ✅ Vector (.ai)
- ✅ PNG (web)
- ✅ PNG-HD (impressão)
- ✅ JPG (compatibilidade)

### Marcas d'água (3 cores x 4 logos)
- ✅ Branco (fundo escuro)
- ✅ Cores (fundo claro)
- ✅ Preto (fundo branco)

---

## 🚀 Exemplos de Código

### Django Template (Website)
```html
<!-- Logo no header -->
<img src="{% static 'brand/logos/png/logo-primary.png' %}" alt="Fuet Mágico">

<!-- Favicon -->
<link rel="icon" type="image/png" href="{% static 'brand/logos/png/logo-icon.png' %}">
```

### Python (Gerar PDF com marca d'água)
```python
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Adicionar marca d'água
watermark = 'static/brand/watermarks/color/watermark-logo-primary.png'
c.drawImage(watermark, x=100, y=100, width=400, height=400, mask='auto')
```

---

## 📞 Suporte

Se precisares de:
- **Novos formatos** → exportar a partir do ficheiro .ai
- **Alterar cores** → editar o ficheiro .ai no Adobe Illustrator
- **Novos tamanhos** → usar o ficheiro .ai (vetorizado, escala infinita)

**Ficheiro Master:** `static/brand/logos/vector/fuet-magico-logo.ai`

---

**Última atualização:** Fevereiro 2026
