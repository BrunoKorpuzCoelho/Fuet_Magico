import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from apps.core.models import AbstractBaseModel


class PaymentTerm(AbstractBaseModel):
    """Condições de pagamento para encomendas de compra.

    Exemplos: Pronto pagamento (0 dias), 30 dias, 60 dias, 30/60 dias.
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
        help_text='Seleccionada automaticamente em novas encomendas de compra.',
    )
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='payment_terms',
        verbose_name='Empresa',
    )

    class Meta:
        verbose_name = 'Condição de Pagamento'
        verbose_name_plural = 'Condições de Pagamento'
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


class PurchaseOrder(AbstractBaseModel):
    """Purchase order / procurement document.

    Lifecycle: DRAFT → CONFIRMED → RECEIVED (or CANCELLED at any point before RECEIVED).
    """

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Rascunho'
        CONFIRMED = 'confirmed', 'Confirmado'
        RECEIVED = 'received', 'Recebido'
        CANCELLED = 'cancelled', 'Cancelado'

    # ── Identification ───────────────────────────────────────────────
    order_number = models.CharField(
        max_length=32,
        unique=True,
        blank=True,
        verbose_name='Nº Encomenda',
        help_text='Auto-gerado ao gravar (ex: PO/2026/00001).',
    )

    # ── Supplier ─────────────────────────────────────────────────────
    supplier = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='purchase_orders',
        verbose_name='Fornecedor',
    )

    # ── Dates ────────────────────────────────────────────────────────
    order_date = models.DateField(
        default=timezone.localdate,
        verbose_name='Data da Encomenda',
    )
    expected_delivery_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data Prevista de Entrega',
    )

    # ── Status ───────────────────────────────────────────────────────
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='Estado',
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

    # ── Origin ───────────────────────────────────────────────────────
    origin = models.CharField(
        max_length=64,
        blank=True,
        default='',
        verbose_name='Origem',
        help_text='Referência externa (ex: SO/2026/00001).',
    )

    # ── Notes ────────────────────────────────────────────────────────
    notes = models.TextField(blank=True, default='', verbose_name='Notas')

    # ── Payment Terms ───────────────────────────────────────────────
    payment_terms = models.ForeignKey(
        'PaymentTerm',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchase_orders',
        verbose_name='Condições de Pagamento',
    )

    # ── Multi-company ────────────────────────────────────────────────
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='purchase_orders',
        verbose_name='Empresa',
        help_text='NULL = global (visível para todas as empresas).',
    )

    class Meta:
        verbose_name = 'Encomenda de Compra'
        verbose_name_plural = 'Encomendas de Compra'
        ordering = ['-order_date', '-created_at']

    def __str__(self):
        return self.order_number or f'PO-{str(self.id)[:8]}'

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    @classmethod
    def generate_order_number(cls):
        """Generate next sequential order number: PO/YYYY/NNNNN."""
        year = timezone.now().year
        prefix = f'PO/{year}/'
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


class PurchaseOrderLine(AbstractBaseModel):
    """Single product line within a PurchaseOrder."""

    purchase_order = models.ForeignKey(
        PurchaseOrder,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name='Encomenda',
    )
    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.PROTECT,
        related_name='purchase_order_lines',
        verbose_name='Produto',
    )
    uom = models.ForeignKey(
        'inventory.UoM',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='purchase_order_lines',
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
        verbose_name = 'Linha de Encomenda'
        verbose_name_plural = 'Linhas de Encomenda'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.product.name} × {self.quantity}'

    # ── Calculated properties ────────────────────────────────────────
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
        """Persist calculated values (if ever needed) and trigger order recalc."""
        self.purchase_order.recalculate_totals()
