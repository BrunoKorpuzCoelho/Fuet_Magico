import uuid
from django.db import models
from django.conf import settings
from apps.core.models import AbstractBaseModel


class LayoutStyle(AbstractBaseModel):
    """
    Estilo de envelope do documento (header + footer).
    Cada estilo define um visual diferente para o cabeçalho e rodapé do PDF.
    Ex: Clean, Bold, Stripe, Frame, Split, Arc, Edge.
    """

    name = models.CharField(
        max_length=100, unique=True,
        verbose_name='Nome',
    )
    slug = models.SlugField(
        max_length=100, unique=True,
        verbose_name='Slug',
    )
    description = models.TextField(
        blank=True, default='',
        verbose_name='Descrição',
    )
    header_html = models.TextField(
        verbose_name='HTML do Header',
        help_text='HTML do cabeçalho do documento. Usa placeholders Django template.',
    )
    footer_html = models.TextField(
        verbose_name='HTML do Footer',
        help_text='HTML do rodapé do documento. Usa placeholders Django template.',
    )
    preview_image = models.ImageField(
        upload_to='documents/previews/layouts/',
        blank=True, default='',
        verbose_name='Imagem de Pré-visualização',
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name='Ordem',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='layout_styles_created',
        verbose_name='Criado por',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='layout_styles_updated',
        verbose_name='Atualizado por',
    )

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Estilo de Layout'
        verbose_name_plural = 'Estilos de Layout'

    def __str__(self):
        return self.name


class TableStyle(AbstractBaseModel):
    """
    Estilo de tabela de dados do documento.
    Define como as linhas de items (produtos, serviços) aparecem no corpo do PDF.
    Ex: Minimal, Grid, Accent, Zebra, Compact, Card, Flat.
    """

    name = models.CharField(
        max_length=100, unique=True,
        verbose_name='Nome',
    )
    slug = models.SlugField(
        max_length=100, unique=True,
        verbose_name='Slug',
    )
    description = models.TextField(
        blank=True, default='',
        verbose_name='Descrição',
    )
    css_styles = models.TextField(
        verbose_name='CSS da Tabela',
        help_text='CSS inline para estilizar a tabela de dados.',
    )
    header_row_html = models.TextField(
        blank=True, default='',
        verbose_name='HTML do Header da Tabela',
        help_text='HTML template da row de cabeçalho (th).',
    )
    data_row_html = models.TextField(
        blank=True, default='',
        verbose_name='HTML de cada Row de Dados',
        help_text='HTML template de cada linha de dados (td).',
    )
    totals_row_html = models.TextField(
        blank=True, default='',
        verbose_name='HTML da Row de Totais',
        help_text='HTML template do bloco de totais (subtotal, IVA, total).',
    )
    preview_image = models.ImageField(
        upload_to='documents/previews/tables/',
        blank=True, default='',
        verbose_name='Imagem de Pré-visualização',
    )
    sort_order = models.IntegerField(
        default=0,
        verbose_name='Ordem',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='table_styles_created',
        verbose_name='Criado por',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='table_styles_updated',
        verbose_name='Atualizado por',
    )

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Estilo de Tabela'
        verbose_name_plural = 'Estilos de Tabela'

    def __str__(self):
        return self.name


class DocumentLayout(AbstractBaseModel):
    """
    Configuração ativa do layout de documentos por empresa.
    Cada empresa tem 1 DocumentLayout que combina LayoutStyle + TableStyle + cores + fonte.
    Os dados da empresa (logo, morada) vêm da tabela Company via FK.
    """

    PAPER_A4 = 'A4'
    PAPER_US_LETTER = 'US_LETTER'
    PAPER_CHOICES = [
        (PAPER_A4, 'A4'),
        (PAPER_US_LETTER, 'US Letter'),
    ]

    company = models.OneToOneField(
        'core.Company',
        on_delete=models.CASCADE,
        related_name='document_layout',
        verbose_name='Empresa',
    )
    layout_style = models.ForeignKey(
        LayoutStyle,
        on_delete=models.PROTECT,
        related_name='document_layouts',
        verbose_name='Estilo de Layout',
    )
    table_style = models.ForeignKey(
        TableStyle,
        on_delete=models.PROTECT,
        related_name='document_layouts',
        verbose_name='Estilo de Tabela',
    )
    font = models.CharField(
        max_length=100, default='Lato',
        verbose_name='Fonte',
    )
    primary_color = models.CharField(
        max_length=7, default='#dbc693',
        verbose_name='Cor Principal',
        help_text='Cor HEX para headers e destaques.',
    )
    secondary_color = models.CharField(
        max_length=7, default='#1f2937',
        verbose_name='Cor Secundária',
        help_text='Cor HEX para texto e borders.',
    )
    tagline = models.CharField(
        max_length=255, blank=True, default='',
        verbose_name='Slogan',
    )
    footer_text = models.TextField(
        blank=True, default='',
        verbose_name='Texto do Rodapé',
        help_text='Texto livre: telefone, email, website.',
    )
    paper_format = models.CharField(
        max_length=20, choices=PAPER_CHOICES, default=PAPER_A4,
        verbose_name='Formato do Papel',
    )
    tax_id = models.CharField(
        max_length=50, blank=True, default='',
        verbose_name='NIF / CNPJ',
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='document_layouts_created',
        verbose_name='Criado por',
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='document_layouts_updated',
        verbose_name='Atualizado por',
    )

    class Meta:
        verbose_name = 'Layout de Documento'
        verbose_name_plural = 'Layouts de Documento'

    def __str__(self):
        return f'Layout de {self.company.name}'

    def get_context(self):
        """
        Retorna dict completo para renderização de documentos.
        Combina dados da Company + configurações deste layout.
        """
        company = self.company
        ctx = {
            'company_name': company.name,
            'company_legal_name': getattr(company, 'legal_name', '') or company.name,
            'company_vat': getattr(company, 'vat', '') or '',
            'company_address': self._build_address(company),
            'company_phone': getattr(company, 'phone', '') or '',
            'company_email': getattr(company, 'email', '') or '',
            'company_website': getattr(company, 'website', '') or '',
            'company_logo': company.logo.url if hasattr(company, 'logo') and company.logo else '',
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'font': self.font,
            'tagline': self.tagline,
            'footer_text': self.footer_text,
            'paper_format': self.paper_format,
            'tax_id': self.tax_id or getattr(company, 'vat', ''),
        }
        return ctx

    @staticmethod
    def _build_address(company):
        """Monta morada formatada a partir dos campos da Company."""
        parts = []
        for field in ['street', 'street2', 'city', 'state', 'zip_code', 'country']:
            val = getattr(company, field, None)
            if val:
                parts.append(str(val))
        return ', '.join(parts) if parts else ''
