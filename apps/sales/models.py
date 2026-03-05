import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from apps.core.models import AbstractBaseModel


class PaymentTerm(AbstractBaseModel):
    """Condições de pagamento para vendas.

    Exemplos: Pronto pagamento (0 dias), 30 dias, 60 dias.
    """

    name = models.CharField(
        max_length=100,
        verbose_name='Nome',
        help_text='Ex: Pronto pagamento, 30 dias, 30/60 dias',
    )
    days = models.PositiveIntegerField(
        default=0,
        verbose_name='Dias',
        help_text='Número de dias para pagamento (0 = pronto pagamento)',
    )
    description = models.TextField(
        blank=True,
        default='',
        verbose_name='Descrição',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='Padrão',
        help_text='Seleccionada automaticamente em novas vendas.',
    )
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sales_payment_terms',
        verbose_name='Empresa',
    )

    class Meta:
        verbose_name = 'Condição de Pagamento (Venda)'
        verbose_name_plural = 'Condições de Pagamento (Vendas)'
        ordering = ['-is_default', 'days', 'name']

    def save(self, *args, **kwargs):
        # Only one default per company — clear others before saving
        if self.is_default:
            PaymentTerm.objects.filter(
                owner_company=self.owner_company,
                is_default=True,
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SaleOrder(AbstractBaseModel):
    """Sale order / quotation / invoice document.

    Lifecycle: DRAFT → CONFIRMED → DELIVERED / INVOICED (or CANCELLED at any point before INVOICED).
    """

    class Status(models.TextChoices):
        DRAFT     = 'draft',     'Rascunho'
        CONFIRMED = 'confirmed', 'Confirmado'
        DELIVERED = 'delivered', 'Entregue'
        INVOICED  = 'invoiced',  'Faturado'
        CANCELLED = 'cancelled', 'Cancelado'

    class DocumentType(models.TextChoices):
        QUOTATION = 'quotation', 'Orçamento'
        ORDER     = 'order',     'Encomenda'
        INVOICE   = 'invoice',   'Fatura'   # reservado para faturas futuras

    class PaymentStatus(models.TextChoices):
        UNPAID  = 'unpaid',  'Não Pago'
        PARTIAL = 'partial', 'Parcial'
        PAID    = 'paid',    'Pago'

    # ── Identification ───────────────────────────────────────
    order_number = models.CharField(
        max_length=32,
        unique=True,
        blank=True,
        verbose_name='Nº Venda',
        help_text='Auto-gerado ao gravar (ex: SO/2026/00001).',
    )

    # ── Client ─────────────────────────────────────────────
    client = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='sale_orders',
        verbose_name='Cliente',
    )

    # ── Document type ────────────────────────────────────
    document_type = models.CharField(
        max_length=16,
        choices=DocumentType.choices,
        default=DocumentType.QUOTATION,  # auto: DRAFT=Orçamento, CONFIRMED=Encomenda
        verbose_name='Tipo de Documento',
    )

    # ── Dates ──────────────────────────────────────────
    order_date = models.DateField(
        default=timezone.localdate,
        verbose_name='Data',
    )
    delivery_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Entrega',
    )

    # ── Status ───────────────────────────────────────────
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Estado',
    )
    payment_status = models.CharField(
        max_length=16,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID,
        verbose_name='Estado Pagamento',
    )

    # ── Totals (denormalised, recalculated on line save/delete) ──────
    subtotal = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal('0.00'),
        verbose_name='Subtotal (s/ IVA)',
    )
    tax = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal('0.00'),
        verbose_name='IVA',
    )
    total = models.DecimalField(
        max_digits=14, decimal_places=2, default=Decimal('0.00'),
        verbose_name='Total (c/ IVA)',
    )

    # ── Notes ────────────────────────────────────────────
    notes = models.TextField(blank=True, default='', verbose_name='Notas')
    # ── Payment Terms ────────────────────────────────────────
    payment_terms = models.ForeignKey(
        'sales.PaymentTerm',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sale_orders',
        verbose_name='Condição de Pagamento',
    )
    # ── Multi-company ────────────────────────────────────
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sale_orders',
        verbose_name='Empresa',
        help_text='NULL = global (visível para todas as empresas).',
    )

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-order_date', '-created_at']

    def __str__(self):
        return self.order_number or f'SO-{str(self.id)[:8]}'

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    @classmethod
    def generate_order_number(cls):
        """Generate next sequential order number: SO/YYYY/NNNNN."""
        year = timezone.now().year
        prefix = f'SO/{year}/'
        last = (
            cls.objects
            .filter(order_number__startswith=prefix)
            .order_by('-order_number')
            .values_list('order_number', flat=True)
            .first()
        )
        if last:
            try:
                seq = int(last.split('/')[-1]) + 1
            except (ValueError, IndexError):
                seq = 1
        else:
            seq = 1
        return f'{prefix}{seq:05d}'

    def recalculate_totals(self):
        """Recalculate subtotal, tax and total from lines."""
        lines = self.lines.all()
        sub = sum(ln.line_total for ln in lines)
        vat = sum(ln.line_vat for ln in lines)
        self.subtotal = sub
        self.tax = vat
        self.total = sub + vat
        self.save(update_fields=['subtotal', 'tax', 'total'])

    @property
    def is_editable(self):
        return self.status == self.Status.DRAFT


class SaleOrderLine(AbstractBaseModel):
    """Single product line within a SaleOrder."""

    sale_order = models.ForeignKey(
        SaleOrder,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name='Venda',
    )
    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.PROTECT,
        related_name='sale_order_lines',
        verbose_name='Produto',
    )
    uom = models.ForeignKey(
        'inventory.UoM',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='sale_order_lines',
        verbose_name='Unidade',
    )
    quantity = models.DecimalField(
        max_digits=14, decimal_places=4, default=Decimal('1.0000'),
        verbose_name='Quantidade',
    )
    unit_price = models.DecimalField(
        max_digits=14, decimal_places=4, default=Decimal('0.0000'),
        verbose_name='Preço Unitário',
    )
    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.00'),
        verbose_name='IVA (%)',
    )
    discount_pct = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.00'),
        verbose_name='Desconto (%)',
        help_text='Percentagem de desconto aplicada ao preço unitário (0–100).',
    )
    notes = models.CharField(max_length=255, blank=True, default='', verbose_name='Notas')

    class Meta:
        verbose_name = 'Linha de Venda'
        verbose_name_plural = 'Linhas de Venda'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.product.name} × {self.quantity}'

    # ── Calculated properties ──────────────────────────────────
    @property
    def line_total(self):
        """Subtotal without VAT, after line discount."""
        return (self.quantity * self.unit_price * (1 - self.discount_pct / 100)).quantize(Decimal('0.01'))

    @property
    def line_vat(self):
        """VAT amount for this line (applied on the already-discounted net)."""
        return (self.line_total * self.tax_rate / 100).quantize(Decimal('0.01'))

    @property
    def line_total_with_vat(self):
        return self.line_total + self.line_vat

    def calculate_line_total(self):
        """Trigger order recalc."""
        self.sale_order.recalculate_totals()
