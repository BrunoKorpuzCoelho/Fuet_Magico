# -*- coding: utf-8 -*-
"""
Seed: Document Layout Styles + Table Styles
Cria 7 Layout Styles e 7 Table Styles para o sistema de Document Layout.

Uso:
    python manage.py shell -c "exec(open('scripts/seed_document_styles.py', encoding='utf-8').read())"
"""

from apps.documents.models import LayoutStyle, TableStyle


# ═══════════════════════════════════════════════════════════════════════════════
#  LAYOUT STYLES  (header + footer HTML)
#  Placeholders: {{ company_name }}, {{ company_logo }}, {{ company_address }},
#                {{ company_phone }}, {{ company_email }}, {{ company_website }},
#                {{ primary_color }}, {{ secondary_color }}, {{ tagline }},
#                {{ footer_text }}, {{ tax_id }}, {{ company_initials }}
# ═══════════════════════════════════════════════════════════════════════════════

LAYOUT_STYLES = [

    # ── 1. CLEAN ─────────────────────────────────────────────────────────────
    {
        'name': 'Clean',
        'slug': 'clean',
        'sort_order': 1,
        'description': 'Minimalista. Logo à esquerda, dados à direita, muito espaço em branco. Sem fundos coloridos. Ideal para quem quer sobriedade.',
        'header_html': '''<div style="padding: 20px 28px 14px; display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid #e5e7eb; font-family: {{ font }}, sans-serif;">
    <div style="display: flex; align-items: center; gap: 10px;">
        {% if company_logo %}
        <img src="{{ company_logo }}" alt="{{ company_name }}" style="height: 36px; width: auto;">
        {% else %}
        <div style="width: 36px; height: 36px; background: {{ primary_color }}; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 900; font-size: 14px;">{{ company_initials }}</div>
        {% endif %}
        <span style="font-size: 16px; font-weight: 700; color: {{ secondary_color }};">{{ company_name }}</span>
    </div>
    <div style="text-align: right; font-size: 10px; color: #6b7280; line-height: 1.6;">
        {{ company_address }}<br>
        {{ company_phone }}
    </div>
</div>''',
        'footer_html': '''<div style="border-top: 1px solid #e5e7eb; padding: 10px 28px; text-align: center; font-size: 9px; color: #9ca3af; font-family: {{ font }}, sans-serif;">
    {{ company_phone }} · {{ company_email }} · {{ company_website }} · {{ footer_text }}
</div>''',
    },

    # ── 2. BOLD ──────────────────────────────────────────────────────────────
    {
        'name': 'Bold',
        'slug': 'bold',
        'sort_order': 2,
        'description': 'Impactante. Barras escuras no topo e fundo, logo e nome à esquerda, dados da empresa à direita. Presença forte da marca.',
        'header_html': '''<div style="background: {{ secondary_color }}; padding: 18px 28px; display: flex; justify-content: space-between; align-items: center; font-family: {{ font }}, sans-serif;">
    <div style="display: flex; align-items: center; gap: 12px;">
        {% if company_logo %}
        <img src="{{ company_logo }}" alt="{{ company_name }}" style="height: 42px; width: auto;">
        {% else %}
        <div style="width: 42px; height: 42px; background: {{ primary_color }}; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 900; font-size: 17px;">{{ company_initials }}</div>
        {% endif %}
        <span style="font-size: 18px; font-weight: 900; color: #ffffff;">{{ company_name }}</span>
    </div>
    <div style="text-align: right; font-size: 10px; color: #9ca3af; line-height: 1.6;">
        {{ company_address }}<br>
        {{ company_phone }}
    </div>
</div>''',
        'footer_html': '''<div style="background: {{ secondary_color }}; padding: 10px 28px; text-align: center; font-size: 9px; color: #9ca3af; font-family: {{ font }}, sans-serif;">
    {{ company_phone }} · {{ company_email }} · {{ company_website }} · {{ footer_text }}
</div>''',
    },

    # ── 3. STRIPE ────────────────────────────────────────────────────────────
    {
        'name': 'Stripe',
        'slug': 'stripe',
        'sort_order': 3,
        'description': 'Subtil. Faixa lateral colorida de 5px à esquerda. Toque profissional discreto, sem exagerar na cor.',
        'header_html': '''<div style="padding: 18px 28px 14px 36px; border-left: 5px solid {{ primary_color }}; display: flex; justify-content: space-between; align-items: flex-start; font-family: {{ font }}, sans-serif;">
    <div style="display: flex; align-items: center; gap: 10px;">
        {% if company_logo %}
        <img src="{{ company_logo }}" alt="{{ company_name }}" style="height: 34px; width: auto;">
        {% else %}
        <div style="width: 34px; height: 34px; background: {{ primary_color }}; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 900; font-size: 14px;">{{ company_initials }}</div>
        {% endif %}
        <span style="font-size: 15px; font-weight: 700; color: {{ secondary_color }};">{{ company_name }}</span>
    </div>
    <div style="text-align: right; font-size: 10px; color: #6b7280; line-height: 1.6;">
        {{ company_address }}<br>
        {{ company_phone }}
    </div>
</div>''',
        'footer_html': '''<div style="border-left: 5px solid {{ primary_color }}; padding: 10px 28px 10px 36px; font-size: 9px; color: #9ca3af; font-family: {{ font }}, sans-serif;">
    {{ company_phone }} · {{ company_email }} · {{ company_website }}
</div>''',
    },

    # ── 4. FRAME ─────────────────────────────────────────────────────────────
    {
        'name': 'Frame',
        'slug': 'frame',
        'sort_order': 4,
        'description': 'Clássico e formal. Bordas finas douradas formam moldura. Logo centrado dentro da moldura. Elegância tradicional.',
        'header_html': '''<div style="margin: 14px 20px 0; border: 2px solid {{ primary_color }}; border-bottom: none; border-radius: 8px 8px 0 0; padding: 16px 20px; text-align: center; font-family: {{ font }}, sans-serif;">
    {% if company_logo %}
    <img src="{{ company_logo }}" alt="{{ company_name }}" style="height: 36px; width: auto; margin-bottom: 4px;">
    {% else %}
    <div style="width: 36px; height: 36px; background: {{ primary_color }}; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; color: #fff; font-weight: 900; font-size: 14px; margin-bottom: 4px;">{{ company_initials }}</div>
    {% endif %}
    <span style="font-size: 15px; font-weight: 700; color: {{ secondary_color }}; display: block;">{{ company_name }}</span>
    <div style="font-size: 10px; color: #6b7280; margin-top: 2px;">{{ company_address }}</div>
</div>''',
        'footer_html': '''<div style="margin: 0 20px 14px; border: 2px solid {{ primary_color }}; border-top: none; border-radius: 0 0 8px 8px; padding: 10px 20px; text-align: center; font-size: 9px; color: #9ca3af; font-family: {{ font }}, sans-serif;">
    {{ company_phone }} · {{ company_email }} · {{ company_website }}
</div>''',
    },

    # ── 5. SPLIT ─────────────────────────────────────────────────────────────
    {
        'name': 'Split',
        'slug': 'split',
        'sort_order': 5,
        'description': 'Header dividido ao meio — metade esquerda com fundo escuro e logo, metade direita limpa com dados. Moderno e assimétrico.',
        'header_html': '''<div style="display: flex; min-height: 70px; font-family: {{ font }}, sans-serif;">
    <div style="flex: 1; background: {{ secondary_color }}; display: flex; align-items: center; justify-content: center; gap: 10px; padding: 14px;">
        {% if company_logo %}
        <img src="{{ company_logo }}" alt="{{ company_name }}" style="height: 34px; width: auto;">
        {% else %}
        <div style="width: 34px; height: 34px; background: {{ primary_color }}; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 900; font-size: 14px;">{{ company_initials }}</div>
        {% endif %}
        <span style="color: #fff; font-size: 15px; font-weight: 700;">{{ company_name }}</span>
    </div>
    <div style="flex: 1; display: flex; align-items: center; justify-content: flex-end; padding: 14px 20px;">
        <div style="text-align: right; font-size: 10px; color: #6b7280; line-height: 1.6;">
            {{ company_address }}<br>
            {{ company_phone }}
        </div>
    </div>
</div>''',
        'footer_html': '''<div style="display: flex; font-family: {{ font }}, sans-serif;">
    <div style="flex: 1; background: {{ secondary_color }}; padding: 8px 14px; font-size: 9px; color: {{ primary_color }};">{{ company_website }}</div>
    <div style="flex: 1; padding: 8px 14px; text-align: right; font-size: 9px; color: #9ca3af;">{{ footer_text }}</div>
</div>''',
    },

    # ── 6. ARC ────────────────────────────────────────────────────────────────
    {
        'name': 'Arc',
        'slug': 'arc',
        'sort_order': 6,
        'description': 'Orgânico. Gradiente dourado no header com curva suave na base. Visual moderno, elegante e não-agressivo.',
        'header_html': '''<div style="position: relative; padding: 20px 28px 30px; text-align: center; overflow: hidden; font-family: {{ font }}, sans-serif;">
    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(135deg, {{ primary_color }}, #c4a96e); z-index: 0;"></div>
    <div style="position: absolute; bottom: 0; left: -10%; width: 120%; height: 30px; background: white; border-radius: 50% 50% 0 0; z-index: 1;"></div>
    <div style="position: relative; z-index: 2;">
        {% if company_logo %}
        <img src="{{ company_logo }}" alt="{{ company_name }}" style="height: 38px; width: auto; margin-bottom: 4px;">
        {% else %}
        <div style="width: 38px; height: 38px; background: rgba(255,255,255,0.25); border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; color: #fff; font-weight: 900; font-size: 16px; margin-bottom: 4px;">{{ company_initials }}</div>
        {% endif %}
        <span style="font-size: 16px; font-weight: 700; color: #fff; display: block;">{{ company_name }}</span>
        <div style="font-size: 10px; color: rgba(255,255,255,0.75); margin-top: 2px;">{{ company_address }}</div>
    </div>
</div>''',
        'footer_html': '''<div style="position: relative; padding: 24px 28px 10px; text-align: center; font-size: 9px; color: #9ca3af; overflow: hidden; font-family: {{ font }}, sans-serif;">
    <div style="position: absolute; top: 0; left: -10%; width: 120%; height: 20px; background: {{ primary_color }}; border-radius: 0 0 50% 50%; opacity: 0.3;"></div>
    {{ company_phone }} · {{ company_email }} · {{ company_website }}
</div>''',
    },

    # ── 7. EDGE ──────────────────────────────────────────────────────────────
    {
        'name': 'Edge',
        'slug': 'edge',
        'sort_order': 7,
        'description': 'Técnico. Triângulos e linhas geométricas angulares nos cantos. Gradientes lineares. Sharp e contemporâneo.',
        'header_html': '''<div style="position: relative; padding: 18px 28px; display: flex; justify-content: space-between; align-items: flex-start; overflow: hidden; font-family: {{ font }}, sans-serif;">
    <div style="position: absolute; top: 0; left: 0; width: 0; height: 0; border-style: solid; border-width: 60px 120px 0 0; border-color: {{ primary_color }} transparent transparent transparent;"></div>
    <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, {{ primary_color }}, transparent 70%);"></div>
    <div style="display: flex; align-items: center; gap: 10px; position: relative; z-index: 1;">
        {% if company_logo %}
        <img src="{{ company_logo }}" alt="{{ company_name }}" style="height: 32px; width: auto;">
        {% else %}
        <div style="width: 32px; height: 32px; background: {{ secondary_color }}; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: {{ primary_color }}; font-weight: 900; font-size: 13px;">{{ company_initials }}</div>
        {% endif %}
        <span style="font-size: 15px; font-weight: 700; color: {{ secondary_color }};">{{ company_name }}</span>
    </div>
    <div style="text-align: right; font-size: 10px; color: #6b7280; line-height: 1.6;">
        {{ company_address }}<br>
        {{ company_phone }}
    </div>
</div>''',
        'footer_html': '''<div style="position: relative; padding: 10px 28px; font-size: 9px; color: #9ca3af; text-align: right; overflow: hidden; font-family: {{ font }}, sans-serif;">
    <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, transparent 30%, {{ primary_color }});"></div>
    <div style="position: absolute; bottom: 0; right: 0; width: 0; height: 0; border-style: solid; border-width: 0 0 40px 80px; border-color: transparent transparent {{ primary_color }} transparent; opacity: 0.2;"></div>
    {{ company_phone }} · {{ company_email }} · {{ company_website }} · {{ footer_text }}
</div>''',
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
#  TABLE STYLES  (CSS + HTML templates)
#  Placeholders: {{ primary_color }}, {{ secondary_color }}
# ═══════════════════════════════════════════════════════════════════════════════

TABLE_STYLES = [

    # ── 1. MINIMAL ───────────────────────────────────────────────────────────
    {
        'name': 'Minimal',
        'slug': 'minimal',
        'sort_order': 1,
        'description': 'Sem bordas externas. Apenas separadores horizontais subtis entre linhas. O mais discreto.',
        'css_styles': '''table { width: 100%; border-collapse: collapse; font-size: 11px; }
th { font-weight: 700; padding: 8px; text-align: left; border-bottom: 1px solid #d1d5db; color: {{ secondary_color }}; }
td { padding: 8px; border-bottom: 1px solid #f3f4f6; color: #374151; }
th:last-child, td:last-child { text-align: right; }''',
        'header_row_html': '<tr><th>Descrição</th><th>Qtd</th><th>Preço Unit.</th><th>IVA</th><th>Total</th></tr>',
        'data_row_html': '<tr><td>{{ description }}</td><td>{{ quantity }}</td><td>{{ unit_price }}</td><td>{{ tax_rate }}</td><td>{{ total }}</td></tr>',
        'totals_row_html': '''<div style="width: 200px; margin-left: auto; margin-top: 14px; font-size: 11px; color: #374151;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr><td style="padding: 4px 0;">Subtotal</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ subtotal }}</td></tr>
        <tr><td style="padding: 4px 0;">IVA {{ tax_rate }}</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ tax_amount }}</td></tr>
        <tr><td style="border-top: 2px solid {{ secondary_color }}; padding-top: 6px; font-weight: 700; font-size: 12px;">Total</td><td style="border-top: 2px solid {{ secondary_color }}; padding-top: 6px; text-align: right; font-weight: 700; font-size: 12px;">{{ total }}</td></tr>
    </table>
</div>''',
    },

    # ── 2. GRID ──────────────────────────────────────────────────────────────
    {
        'name': 'Grid',
        'slug': 'grid',
        'sort_order': 2,
        'description': 'Bordas completas em todas as células. Header com fundo escuro e texto branco. Máxima estrutura visual.',
        'css_styles': '''table { width: 100%; border-collapse: collapse; font-size: 11px; border: 1px solid #d1d5db; }
th { background: {{ secondary_color }}; color: #fff; padding: 8px; text-align: left; border: 1px solid #374151; }
td { padding: 8px; border: 1px solid #d1d5db; color: #374151; }
th:last-child, td:last-child { text-align: right; }''',
        'header_row_html': '<tr><th>Descrição</th><th>Qtd</th><th>Preço Unit.</th><th>IVA</th><th>Total</th></tr>',
        'data_row_html': '<tr><td>{{ description }}</td><td>{{ quantity }}</td><td>{{ unit_price }}</td><td>{{ tax_rate }}</td><td>{{ total }}</td></tr>',
        'totals_row_html': '''<div style="width: 200px; margin-left: auto; margin-top: 14px; font-size: 11px; color: #374151;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr><td style="padding: 4px 0;">Subtotal</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ subtotal }}</td></tr>
        <tr><td style="padding: 4px 0;">IVA {{ tax_rate }}</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ tax_amount }}</td></tr>
        <tr><td style="border-top: 2px solid {{ secondary_color }}; padding-top: 6px; font-weight: 700; font-size: 12px;">Total</td><td style="border-top: 2px solid {{ secondary_color }}; padding-top: 6px; text-align: right; font-weight: 700; font-size: 12px;">{{ total }}</td></tr>
    </table>
</div>''',
    },

    # ── 3. ACCENT ────────────────────────────────────────────────────────────
    {
        'name': 'Accent',
        'slug': 'accent',
        'sort_order': 3,
        'description': 'Sem bordas verticais. Header sublinhado com a cor principal. Linhas pares com fundo levemente colorido.',
        'css_styles': '''table { width: 100%; border-collapse: collapse; font-size: 11px; }
th { padding: 8px; text-align: left; color: {{ secondary_color }}; font-weight: 700; border-bottom: 3px solid {{ primary_color }}; }
td { padding: 8px; color: #374151; border-bottom: 1px solid #e5e7eb; }
tr:nth-child(even) td { background: rgba(219, 198, 147, 0.07); }
th:last-child, td:last-child { text-align: right; }''',
        'header_row_html': '<tr><th>Descrição</th><th>Qtd</th><th>Preço Unit.</th><th>IVA</th><th>Total</th></tr>',
        'data_row_html': '<tr><td>{{ description }}</td><td>{{ quantity }}</td><td>{{ unit_price }}</td><td>{{ tax_rate }}</td><td>{{ total }}</td></tr>',
        'totals_row_html': '''<div style="width: 200px; margin-left: auto; margin-top: 14px; font-size: 11px; color: #374151;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr><td style="padding: 4px 0;">Subtotal</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ subtotal }}</td></tr>
        <tr><td style="padding: 4px 0;">IVA {{ tax_rate }}</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ tax_amount }}</td></tr>
        <tr><td style="border-top: 2px solid {{ primary_color }}; padding-top: 6px; font-weight: 700; font-size: 12px;">Total</td><td style="border-top: 2px solid {{ primary_color }}; padding-top: 6px; text-align: right; font-weight: 700; font-size: 12px;">{{ total }}</td></tr>
    </table>
</div>''',
    },

    # ── 4. ZEBRA ─────────────────────────────────────────────────────────────
    {
        'name': 'Zebra',
        'slug': 'zebra',
        'sort_order': 4,
        'description': 'Linhas alternadas cinza/branco sem bordas entre elas. A cor faz a separação. Header com borda inferior grossa.',
        'css_styles': '''table { width: 100%; border-collapse: collapse; font-size: 11px; }
th { padding: 8px; text-align: left; color: {{ secondary_color }}; font-weight: 700; border-bottom: 2px solid {{ secondary_color }}; }
td { padding: 8px; color: #374151; }
tbody tr:nth-child(odd) td { background: #f9fafb; }
tbody tr:nth-child(even) td { background: #fff; }
th:last-child, td:last-child { text-align: right; }''',
        'header_row_html': '<tr><th>Descrição</th><th>Qtd</th><th>Preço Unit.</th><th>IVA</th><th>Total</th></tr>',
        'data_row_html': '<tr><td>{{ description }}</td><td>{{ quantity }}</td><td>{{ unit_price }}</td><td>{{ tax_rate }}</td><td>{{ total }}</td></tr>',
        'totals_row_html': '''<div style="width: 200px; margin-left: auto; margin-top: 14px; font-size: 11px; color: #374151;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr><td style="padding: 4px 0;">Subtotal</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ subtotal }}</td></tr>
        <tr><td style="padding: 4px 0;">IVA {{ tax_rate }}</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ tax_amount }}</td></tr>
        <tr><td style="border-top: 2px solid {{ secondary_color }}; padding-top: 6px; font-weight: 700; font-size: 12px;">Total</td><td style="border-top: 2px solid {{ secondary_color }}; padding-top: 6px; text-align: right; font-weight: 700; font-size: 12px;">{{ total }}</td></tr>
    </table>
</div>''',
    },

    # ── 5. COMPACT ───────────────────────────────────────────────────────────
    {
        'name': 'Compact',
        'slug': 'compact',
        'sort_order': 5,
        'description': 'Padding reduzido, fonte menor. Header com fundo escuro. Ideal para documentos com muitas linhas que precisam caber numa página.',
        'css_styles': '''table { width: 100%; border-collapse: collapse; font-size: 10px; }
th { padding: 4px 6px; text-align: left; color: #fff; font-weight: 700; background: #374151; }
td { padding: 4px 6px; color: #374151; border-bottom: 1px solid #e5e7eb; }
th:last-child, td:last-child { text-align: right; }''',
        'header_row_html': '<tr><th>Descrição</th><th>Qtd</th><th>Preço Unit.</th><th>IVA</th><th>Total</th></tr>',
        'data_row_html': '<tr><td>{{ description }}</td><td>{{ quantity }}</td><td>{{ unit_price }}</td><td>{{ tax_rate }}</td><td>{{ total }}</td></tr>',
        'totals_row_html': '''<div style="width: 200px; margin-left: auto; margin-top: 14px; font-size: 10px; color: #374151;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr><td style="padding: 4px 0;">Subtotal</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ subtotal }}</td></tr>
        <tr><td style="padding: 4px 0;">IVA {{ tax_rate }}</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ tax_amount }}</td></tr>
        <tr><td style="border-top: 1px solid #374151; padding-top: 6px; font-weight: 700; font-size: 11px;">Total</td><td style="border-top: 1px solid #374151; padding-top: 6px; text-align: right; font-weight: 700; font-size: 11px;">{{ total }}</td></tr>
    </table>
</div>''',
    },

    # ── 6. CARD ──────────────────────────────────────────────────────────────
    {
        'name': 'Card',
        'slug': 'card',
        'sort_order': 6,
        'description': 'Cada linha como "cartão" com bordas arredondadas e sombra subtil. Espaçamento entre linhas. Header em uppercase.',
        'css_styles': '''table { width: 100%; border-collapse: separate; border-spacing: 0 8px; font-size: 11px; }
th { padding: 8px 12px; text-align: left; color: #6b7280; font-weight: 600; text-transform: uppercase; font-size: 9px; letter-spacing: 0.5px; }
td { padding: 10px 12px; color: #374151; background: #fff; border-top: 1px solid #e5e7eb; border-bottom: 1px solid #e5e7eb; }
td:first-child { border-left: 1px solid #e5e7eb; border-radius: 8px 0 0 8px; }
td:last-child { border-right: 1px solid #e5e7eb; border-radius: 0 8px 8px 0; text-align: right; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
th:last-child { text-align: right; }''',
        'header_row_html': '<tr><th>Descrição</th><th>Qtd</th><th>Preço Unit.</th><th>IVA</th><th>Total</th></tr>',
        'data_row_html': '<tr><td>{{ description }}</td><td>{{ quantity }}</td><td>{{ unit_price }}</td><td>{{ tax_rate }}</td><td>{{ total }}</td></tr>',
        'totals_row_html': '''<div style="width: 200px; margin-left: auto; margin-top: 14px; font-size: 11px; color: #374151;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr><td style="padding: 4px 0;">Subtotal</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ subtotal }}</td></tr>
        <tr><td style="padding: 4px 0;">IVA {{ tax_rate }}</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ tax_amount }}</td></tr>
        <tr><td style="border-top: 2px solid #e5e7eb; padding-top: 6px; font-weight: 700; font-size: 12px;">Total</td><td style="border-top: 2px solid #e5e7eb; padding-top: 6px; text-align: right; font-weight: 700; font-size: 12px;">{{ total }}</td></tr>
    </table>
</div>''',
    },

    # ── 7. FLAT ──────────────────────────────────────────────────────────────
    {
        'name': 'Flat',
        'slug': 'flat',
        'sort_order': 7,
        'description': 'Zero linhas, zero bordas. Apenas texto alinhado em colunas. A versão mais invisível — foca-se 100% nos dados.',
        'css_styles': '''table { width: 100%; border-collapse: collapse; font-size: 11px; }
th { font-weight: 700; padding: 8px; text-align: left; color: {{ secondary_color }}; }
td { padding: 8px; color: #374151; }
th:last-child, td:last-child { text-align: right; }''',
        'header_row_html': '<tr><th>Descrição</th><th>Qtd</th><th>Preço Unit.</th><th>IVA</th><th>Total</th></tr>',
        'data_row_html': '<tr><td>{{ description }}</td><td>{{ quantity }}</td><td>{{ unit_price }}</td><td>{{ tax_rate }}</td><td>{{ total }}</td></tr>',
        'totals_row_html': '''<div style="width: 200px; margin-left: auto; margin-top: 14px; font-size: 11px; color: #374151;">
    <table style="width: 100%; border-collapse: collapse;">
        <tr><td style="padding: 4px 0;">Subtotal</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ subtotal }}</td></tr>
        <tr><td style="padding: 4px 0;">IVA {{ tax_rate }}</td><td style="padding: 4px 0; text-align: right; font-weight: 600;">{{ tax_amount }}</td></tr>
        <tr><td style="border-top: 2px solid {{ secondary_color }}; padding-top: 6px; font-weight: 700; font-size: 12px;">Total</td><td style="border-top: 2px solid {{ secondary_color }}; padding-top: 6px; text-align: right; font-weight: 700; font-size: 12px;">{{ total }}</td></tr>
    </table>
</div>''',
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
#  EXECUÇÃO
# ═══════════════════════════════════════════════════════════════════════════════

print('=' * 60)
print('  Seed: Document Layout & Table Styles')
print('=' * 60)

# ── Layout Styles ────────────────────────────────────────────────────────────
created_ls = 0
updated_ls = 0
for data in LAYOUT_STYLES:
    obj, created = LayoutStyle.objects.update_or_create(
        slug=data['slug'],
        defaults=data,
    )
    if created:
        created_ls += 1
        print(f'  ✅ Layout criado: {obj.name}')
    else:
        updated_ls += 1
        print(f'  🔄 Layout atualizado: {obj.name}')

print(f'\n  Layout Styles: {created_ls} criados, {updated_ls} atualizados')

# ── Table Styles ─────────────────────────────────────────────────────────────
created_ts = 0
updated_ts = 0
for data in TABLE_STYLES:
    obj, created = TableStyle.objects.update_or_create(
        slug=data['slug'],
        defaults=data,
    )
    if created:
        created_ts += 1
        print(f'  ✅ Tabela criada: {obj.name}')
    else:
        updated_ts += 1
        print(f'  🔄 Tabela atualizada: {obj.name}')

print(f'\n  Table Styles: {created_ts} criados, {updated_ts} atualizados')
print('=' * 60)
print('  ✅ Seed completo!')
print('=' * 60)
