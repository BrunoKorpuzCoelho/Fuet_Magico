from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.core.models import AbstractBaseModel


class Warehouse(AbstractBaseModel):
    """Simple warehouse model — represents the storage location.
    
    Auto-created on setup, typically 1 per company.
    The person's warehouse is their home/business — no sub-locations needed.
    """

    name = models.CharField(
        max_length=128,
        verbose_name='Nome',
        help_text='Ex: Armazém Principal',
    )
    code = models.CharField(
        max_length=5,
        verbose_name='Código',
        help_text='Código curto, ex: WH',
    )
    address = models.TextField(
        blank=True,
        default='',
        verbose_name='Morada',
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='Armazém Padrão',
        help_text='Apenas 1 armazém pode ser padrão por empresa.',
    )

    # Multi-company
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='warehouses',
        verbose_name='Empresa',
        help_text='NULL = global (visível para todas).',
    )

    class Meta:
        verbose_name = 'Armazém'
        verbose_name_plural = 'Armazéns'
        ordering = ['-is_default', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['code', 'owner_company'],
                name='unique_warehouse_code_per_company',
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure only 1 default warehouse per company
        if self.is_default:
            Warehouse.objects.filter(
                owner_company=self.owner_company,
                is_default=True,
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class UoMCategory(AbstractBaseModel):
    """Groups related units of measure (e.g. Weight, Volume, Length)."""

    name = models.CharField(max_length=64, verbose_name='Nome')

    # Multi-company
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='uom_categories',
        verbose_name='Empresa',
        help_text='NULL = global (visível para todas).',
    )

    class Meta:
        verbose_name = 'Categoria de UdM'
        verbose_name_plural = 'Categorias de UdM'
        ordering = ['name']
        unique_together = ['name', 'owner_company']

    def __str__(self):
        return self.name


class UoM(AbstractBaseModel):
    """Unit of measure with conversion factor relative to the category reference unit."""

    UOM_TYPE_CHOICES = [
        ('reference', 'Referência'),
        ('bigger', 'Maior que a referência'),
        ('smaller', 'Menor que a referência'),
    ]

    name = models.CharField(max_length=64, verbose_name='Nome')
    symbol = models.CharField(max_length=16, verbose_name='Símbolo', help_text='Ex: kg, g, L, mL')
    category = models.ForeignKey(
        UoMCategory,
        on_delete=models.CASCADE,
        related_name='uoms',
        verbose_name='Categoria',
    )
    uom_type = models.CharField(
        max_length=16,
        choices=UOM_TYPE_CHOICES,
        default='reference',
        verbose_name='Tipo',
        help_text='Referência = unidade base da categoria.',
    )
    factor = models.DecimalField(
        max_digits=20,
        decimal_places=10,
        default=1,
        verbose_name='Factor',
        help_text='Quantas unidades de referência equivale 1 desta unidade. Ex: 1 kg = 1000 g → factor = 1000.',
    )
    rounding = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        default=0.01,
        verbose_name='Precisão de arredondamento',
        help_text='Precisão mínima para esta unidade.',
    )

    # Multi-company
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='uoms',
        verbose_name='Empresa',
        help_text='NULL = global (visível para todas).',
    )

    class Meta:
        verbose_name = 'Unidade de Medida'
        verbose_name_plural = 'Unidades de Medida'
        ordering = ['category', 'uom_type', 'name']
        unique_together = ['name', 'category', 'owner_company']

    def __str__(self):
        return f'{self.name} ({self.symbol})'

    def convert_to(self, qty, target_uom):
        """Convert qty from this UoM to target_uom.

        Both must belong to the same category.
        Formula: qty × self.factor / target.factor
        Example: 2 kg → g = 2 × 1000 / 1 = 2000 g
        """
        if self.category_id != target_uom.category_id:
            raise ValueError(
                f'Não é possível converter entre "{self.category}" e "{target_uom.category}". '
                f'As unidades devem pertencer à mesma categoria.'
            )
        if self.pk == target_uom.pk:
            return qty
        from decimal import Decimal
        return Decimal(str(qty)) * self.factor / target_uom.factor

    def convert_price_to(self, price, target_uom):
        """Convert a unit price from this UoM to target_uom.

        Example: 2 €/kg → 0.002 €/g
        Formula: price × target.factor / self.factor
        """
        from decimal import Decimal, ROUND_HALF_UP
        if self.category_id != target_uom.category_id:
            raise ValueError(
                f'Não é possível converter preço entre "{self.category}" e "{target_uom.category}".'
            )
        if self.pk == target_uom.pk:
            return Decimal(str(price or 0))
        return (Decimal(str(price or 0)) * target_uom.factor / self.factor).quantize(
            Decimal('0.0001'), rounding=ROUND_HALF_UP
        )


class Category(AbstractBaseModel):
    """Product category with optional hierarchy (subcategories via parent FK)."""

    name = models.CharField(max_length=128, verbose_name='Nome')
    description = models.TextField(blank=True, default='', verbose_name='Descrição')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Categoria Pai',
        help_text='Deixe vazio para categoria de topo.',
    )

    # Multi-company
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='inventory_categories',
        verbose_name='Empresa',
        help_text='Empresa proprietária. NULL = global (visível para todas).',
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']
        unique_together = ['name', 'parent', 'owner_company']

    def __str__(self):
        if self.parent:
            return f'{self.parent.name} / {self.name}'
        return self.name


def product_image_path(instance, filename):
    """Upload path: media/products/<uuid>/<filename>"""
    return f'products/{instance.pk}/{filename}'


class Product(AbstractBaseModel):
    """Product with pricing, UoM, and supplier info."""

    PRODUCT_TYPE_CHOICES = [
        ('storable', 'Armazenável'),
        ('consumable', 'Consumível'),
        ('service', 'Serviço'),
    ]

    # ── Identificação ────────────────────────────────────────────────
    name = models.CharField(max_length=255, verbose_name='Nome')
    internal_reference = models.CharField(
        max_length=64,
        blank=True,
        default='',
        verbose_name='Referência Interna',
        help_text='Código único do produto (ex: FM-001).',
    )
    reference = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Referência',
        help_text='Campo de texto livre.',
    )
    barcode = models.CharField(
        max_length=64,
        blank=True,
        default='',
        verbose_name='Código de Barras',
        help_text='EAN-13, UPC, etc.',
    )
    description = models.TextField(blank=True, default='', verbose_name='Descrição')
    image = models.ImageField(
        upload_to=product_image_path,
        blank=True,
        null=True,
        verbose_name='Imagem',
    )

    # ── Classificação ────────────────────────────────────────────────
    product_type = models.CharField(
        max_length=16,
        choices=PRODUCT_TYPE_CHOICES,
        default='storable',
        verbose_name='Tipo de Produto',
        help_text='Armazenável = com stock. Consumível = sem controlo. Serviço = sem stock.',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Categoria',
    )

    # ── Unidades de Medida ───────────────────────────────────────────
    uom = models.ForeignKey(
        UoM,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Unidade de Medida',
        help_text='UdM principal (stock e venda). Stock, cost_price e sale_price são sempre nesta unidade.',
    )
    uom_purchase = models.ForeignKey(
        UoM,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products_purchase',
        verbose_name='UdM de Compra',
        help_text='UdM usada nas compras (pode diferir). Ex: compra em caixas, vende à unidade.',
    )

    # ── Preços ───────────────────────────────────────────────────────
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Preço de Venda',
        help_text='Preço de venda em € por unidade de stock (UdM principal).',
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Preço de Custo',
        help_text='Custo unitário em € por unidade de stock (UdM principal).',
    )
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=23,
        verbose_name='Taxa IVA (%)',
        help_text='Percentagem de IVA aplicável.',
    )

    # ── Compras ──────────────────────────────────────────────────────
    supplier = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supplied_products',
        verbose_name='Fornecedor',
        help_text='Fornecedor principal deste produto.',
    )

    # ── Multi-company ────────────────────────────────────────────────
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Empresa',
        help_text='NULL = global (visível para todas).',
    )

    # ── Stock ─────────────────────────────────────────────────────────
    min_stock = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0,
        verbose_name='Stock Mínimo',
        help_text='Alerta quando o stock em mão cair abaixo deste valor.',
    )
    is_manufactured = models.BooleanField(
        default=False,
        verbose_name='Produto de Fabrico (BOM)',
        help_text='Indica que este produto é produzido internamente a partir de uma Receita (BOM).',
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['internal_reference', 'owner_company'],
                name='unique_product_internal_ref_per_company',
                condition=models.Q(internal_reference__gt=''),
            ),
            models.UniqueConstraint(
                fields=['barcode', 'owner_company'],
                name='unique_product_barcode_per_company',
                condition=models.Q(barcode__gt=''),
            ),
        ]

    def __str__(self):
        if self.internal_reference:
            return f'[{self.internal_reference}] {self.name}'
        return self.name

    def get_profit_margin(self):
        """Return profit margin as percentage. None if cost is 0."""
        if not self.cost_price:
            return None
        return ((self.sale_price - self.cost_price) / self.cost_price) * 100

    def get_profit_margin_pct(self):
        """Return margin as % of sale price (e.g. 38.5). None if sale_price is 0."""
        if not self.sale_price:
            return None
        return float((self.sale_price - self.cost_price) / self.sale_price * 100)

    def get_sale_price_with_tax(self):
        """Return sale price including IVA."""
        from decimal import Decimal
        return self.sale_price * (1 + self.tax_rate / Decimal('100'))

    def get_on_hand_quantity(self, warehouse=None):
        """Total quantity currently in stock (from validated movements)."""
        from django.db.models import Sum
        qs = StockQuant.objects.filter(product=self)
        if warehouse:
            qs = qs.filter(warehouse=warehouse)
        return float(qs.aggregate(total=Sum('quantity'))['total'] or 0)

    def get_incoming_quantity(self, warehouse=None):
        """Quantity on pending (draft) receipt movements."""
        from django.db.models import Sum
        qs = StockMovementLine.objects.filter(
            product=self,
            stock_movement__movement_type='receipt',
            stock_movement__state='draft',
        )
        if warehouse:
            qs = qs.filter(stock_movement__warehouse=warehouse)
        return float(qs.aggregate(total=Sum('quantity'))['total'] or 0)

    def get_outgoing_quantity(self, warehouse=None):
        """Quantity on pending (draft) delivery movements."""
        from django.db.models import Sum
        qs = StockMovementLine.objects.filter(
            product=self,
            stock_movement__movement_type='delivery',
            stock_movement__state='draft',
        )
        if warehouse:
            qs = qs.filter(stock_movement__warehouse=warehouse)
        return float(qs.aggregate(total=Sum('quantity'))['total'] or 0)

    def get_forecasted_quantity(self, warehouse=None):
        """Forecast = on_hand + incoming - outgoing."""
        return (
            self.get_on_hand_quantity(warehouse)
            + self.get_incoming_quantity(warehouse)
            - self.get_outgoing_quantity(warehouse)
        )

    def get_stock_value(self, warehouse=None):
        """Value of current stock = on_hand × cost_price."""
        return self.get_on_hand_quantity(warehouse) * float(self.cost_price)


class StockMovement(AbstractBaseModel):
    """Central inventory document — records stock receipts, deliveries, and adjustments.

    Created automatically by Purchases/Sales or manually for adjustments.
    Lifecycle: draft → done (validates stock) or draft → cancelled.
    """

    MOVEMENT_TYPE_CHOICES = [
        ('receipt', 'Receção'),
        ('delivery', 'Expedição'),
        ('adjustment', 'Ajuste'),
        ('scrap', 'Sucata'),
    ]

    SCRAP_REASON_CHOICES = [
        ('damage',  'Avaria'),
        ('expiry',  'Validade expirada'),
        ('breakage','Quebra'),
        ('quality', 'Controlo de qualidade'),
        ('other',   'Outro'),
    ]

    ADJUSTMENT_DIRECTION_CHOICES = [
        ('in', 'Entrada (adiciona stock)'),
        ('out', 'Saída (remove stock)'),
    ]

    STATE_CHOICES = [
        ('draft', 'Rascunho'),
        ('done', 'Validado'),
        ('cancelled', 'Cancelado'),
    ]

    REFERENCE_PREFIXES = {
        'receipt':    'WH/IN/',
        'delivery':   'WH/OUT/',
        'adjustment': 'ADJ/',
        'scrap':      'SCRAP/',
    }
    # Maps movement_type → DocumentSequence code
    SEQUENCE_CODES = {
        'receipt':    'WH_IN',
        'delivery':   'WH_OUT',
        'adjustment': 'WH_ADJ',
        'scrap':      'WH_SCRAP',
    }
    reference = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Referência',
        help_text='Auto-gerado: WH/IN/00001, WH/OUT/00001, ADJ/00001',
    )
    movement_type = models.CharField(
        max_length=16,
        choices=MOVEMENT_TYPE_CHOICES,
        verbose_name='Tipo de Movimento',
    )
    scrap_reason = models.CharField(
        max_length=16,
        choices=SCRAP_REASON_CHOICES,
        null=True,
        blank=True,
        verbose_name='Motivo de Sucata',
        help_text='Apenas para movimentos de sucata.',
    )
    adjustment_direction = models.CharField(
        max_length=3,
        choices=ADJUSTMENT_DIRECTION_CHOICES,
        null=True,
        blank=True,
        verbose_name='Direção do Ajuste',
        help_text='Apenas para ajustes: Entrada adiciona stock, Saída remove stock.',
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name='stock_movements',
        verbose_name='Armazém',
    )
    partner = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements',
        verbose_name='Parceiro',
        help_text='Fornecedor (receção) ou cliente (expedição).',
    )
    state = models.CharField(
        max_length=16,
        choices=STATE_CHOICES,
        default='draft',
        verbose_name='Estado',
    )
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Data do Movimento',
    )
    origin = models.CharField(
        max_length=64,
        blank=True,
        default='',
        verbose_name='Origem',
        help_text='Referência ao documento de origem (ex: PO-00001).',
    )
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name='Notas',
    )
    global_discount_pct = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        verbose_name='Desconto Global (%)',
        help_text='Desconto aplicado ao valor total antes do IVA.',
    )
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_movements',
        verbose_name='Responsável',
    )

    # Multi-company
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='stock_movements',
        verbose_name='Empresa',
        help_text='NULL = global (visível para todas).',
    )

    class Meta:
        verbose_name = 'Movimento de Stock'
        verbose_name_plural = 'Movimentos de Stock'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return self.reference

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_reference()
        super().save(*args, **kwargs)

    def generate_reference(self):
        """Generate next sequential reference using DocumentSequence (atomic).

        Delegates to ``DocumentSequence.get_for()`` + ``next_reference()`` so
        that concurrent requests never produce duplicate references and deleted
        documents never recycle their numbers.

        Format: WH/IN/00001, WH/OUT/00001, ADJ/00001
        """
        from apps.core.models import DocumentSequence
        code = self.SEQUENCE_CODES[self.movement_type]
        seq = DocumentSequence.get_for(code, self.owner_company)
        return seq.next_reference()

    def action_validate(self):
        """Validate the movement — changes state to 'done', updates stock, and
        maintains the Weighted Average Cost (CMVMC — Custo Médio Ponderado) per product.

        CMVMC logic:
          • Receipt / Adjustment-IN:
              new_avg = (on_hand_qty × old_avg + incoming_qty × unit_price)
                        / (on_hand_qty + incoming_qty)
              → updates Product.cost_price (running average)
              → stores new_avg in line.cost_price_at_move

          • Delivery / Adjustment-OUT:
              cost used = current Product.cost_price (the running average)
              → stores it in line.cost_price_at_move  (cost of goods sold)
              → Product.cost_price is unchanged (average stays the same)

        Quantities and prices on movement lines may use any compatible UoM.
        Stock (StockQuant) and weighted-average cost are always normalised to
        product.uom via convert_to / unit_price_to_product_uom.
        """
        from decimal import Decimal, ROUND_HALF_UP
        from apps.inventory.uom_utils import quantity_to_product_uom, unit_price_to_product_uom
        if self.state != 'draft':
            raise ValidationError('Apenas movimentos em rascunho podem ser validados.')

        is_in = (
            self.movement_type == 'receipt'
            or (self.movement_type == 'adjustment' and self.adjustment_direction == 'in')
        )
        is_out = (
            self.movement_type == 'delivery'
            or self.movement_type == 'scrap'
            or (self.movement_type == 'adjustment' and self.adjustment_direction == 'out')
        )

        # ── Pre-validation: check sufficient stock for all out-lines ─────
        # For manufactured products (is_manufactured=True with a BOM), stock is
        # checked against BOM components instead of the finished product itself.
        # The movement line keeps the finished product (for delivery notes / guia
        # de remessa), but the actual stock deduction targets the components.
        if is_out:
            shortages = []
            for line in self.lines.select_related('product', 'product__uom', 'uom'):
                product = line.product
                qty_needed = quantity_to_product_uom(line.quantity, line.uom, product)
                bom = getattr(product, 'bom', None)
                if product.is_manufactured and bom and bom.qty_produced:
                    # Check each component (quantities normalised to component.uom)
                    multiplier = qty_needed / Decimal(str(bom.qty_produced))
                    for bom_line in bom.lines.select_related('component', 'component__uom', 'uom').all():
                        comp = bom_line.component
                        raw_comp_qty = Decimal(str(bom_line.quantity)) * multiplier
                        line_uom = bom_line.uom or comp.uom
                        try:
                            comp_qty_needed = line_uom.convert_to(raw_comp_qty, comp.uom)
                        except ValueError:
                            comp_qty_needed = raw_comp_qty
                        comp_qty_needed = comp_qty_needed.quantize(Decimal('0.0001'))
                        available = Decimal(str(comp.get_on_hand_quantity()))
                        if available < comp_qty_needed:
                            shortages.append(
                                f'{comp.name} (componente de {product.name}): '
                                f'disponível {available:f} {comp.uom.symbol}, '
                                f'necessário {comp_qty_needed:f} {comp.uom.symbol}'
                            )
                else:
                    available = Decimal(str(product.get_on_hand_quantity()))
                    if available < qty_needed:
                        shortages.append(
                            f'{product.name}: disponível {available:f} {product.uom.symbol}, '
                            f'necessário {qty_needed:f} {product.uom.symbol}'
                        )
            if shortages:
                raise ValidationError(
                    'Stock insuficiente para validar este movimento:\n'
                    + '\n'.join(f'• {s}' for s in shortages)
                )

        lines_to_save = []
        products_to_save = []

        for line in self.lines.select_related('product', 'product__uom', 'uom'):
            qty = quantity_to_product_uom(line.quantity, line.uom, line.product).copy_abs()
            product = line.product
            current_cost = Decimal(str(product.cost_price or 0))

            if is_in:
                # ── Weighted Average Cost recalculation (all in product.uom) ──
                current_qty = Decimal(str(product.get_on_hand_quantity()))
                line_cost = (
                    unit_price_to_product_uom(line.unit_price, line.uom, product)
                    if line.unit_price else current_cost
                )

                current_value = current_qty * current_cost
                new_total_qty = current_qty + qty
                new_total_value = current_value + qty * line_cost

                new_avg = (
                    (new_total_value / new_total_qty).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
                    if new_total_qty > 0
                    else line_cost
                )

                line.cost_price_at_move = new_avg
                product.cost_price = new_avg
                products_to_save.append(product)

                StockQuant.update_quantity(product, self.warehouse, qty, 'add')

            elif is_out:
                bom = getattr(product, 'bom', None)
                if product.is_manufactured and bom and bom.qty_produced:
                    multiplier = qty / Decimal(str(bom.qty_produced))
                    line.cost_price_at_move = Decimal(str(product.cost_price or 0))
                    for bom_line in bom.lines.select_related('component', 'component__uom', 'uom').all():
                        comp = bom_line.component
                        raw_comp_qty = Decimal(str(bom_line.quantity)) * multiplier
                        line_uom = bom_line.uom or comp.uom
                        try:
                            comp_qty = line_uom.convert_to(raw_comp_qty, comp.uom)
                        except ValueError:
                            comp_qty = raw_comp_qty
                        comp_qty = comp_qty.quantize(Decimal('0.0001'))
                        StockQuant.update_quantity(comp, self.warehouse, comp_qty, 'subtract')
                else:
                    line.cost_price_at_move = current_cost
                    StockQuant.update_quantity(product, self.warehouse, qty, 'subtract')

            lines_to_save.append(line)

        # Bulk-save lines and products
        if lines_to_save:
            StockMovementLine.objects.bulk_update(lines_to_save, ['cost_price_at_move'])
        for p in products_to_save:
            p.save(update_fields=['cost_price'])

        self.state = 'done'
        self.save()

    def action_cancel(self):
        """Cancel the movement.

        - Draft  → simply marks as cancelled (no stock was ever touched).
        - Done   → reverses the stock quantities (undoes the validation).
          Note: the weighted-average cost_price on the product is NOT re-calculated
          on reversal — this is a known simplification acceptable for this use-case.
        """
        if self.state == 'cancelled':
            raise ValidationError('O movimento já está cancelado.')

        if self.state == 'done':
            # Reverse stock: opposite of what action_validate did
            is_in = (
                self.movement_type == 'receipt'
                or (self.movement_type == 'adjustment' and self.adjustment_direction == 'in')
            )
            is_out = (
                self.movement_type == 'delivery'
                or self.movement_type == 'scrap'
                or (self.movement_type == 'adjustment' and self.adjustment_direction == 'out')
            )
            from decimal import Decimal
            from apps.inventory.uom_utils import quantity_to_product_uom
            for line in self.lines.select_related('product', 'product__uom', 'uom'):
                qty = abs(quantity_to_product_uom(line.quantity, line.uom, line.product))
                if is_in:
                    StockQuant.update_quantity(line.product, self.warehouse, qty, 'subtract')
                elif is_out:
                    StockQuant.update_quantity(line.product, self.warehouse, qty, 'add')

        self.state = 'cancelled'
        self.save()

    @property
    def total_value(self):
        """Sum of line_total (after discount, excl. VAT) across all movement lines."""
        from decimal import Decimal
        return sum((line.line_total for line in self.lines.all()), Decimal('0.00'))


class StockMovementLine(AbstractBaseModel):
    """A single product line within a StockMovement.

    Each movement document can have multiple lines, one per product.
    The uom is inherited from the product if not explicitly set.
    """

    stock_movement = models.ForeignKey(
        StockMovement,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name='Movimento',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='movement_lines',
        verbose_name='Produto',
    )
    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        verbose_name='Quantidade',
        help_text='Quantidade movida nesta linha. Usa decimais para sub-unidades (ex: 0.250 = 250 g de 1 kg).',
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Preço Unitário',
        help_text='Custo unitário (receção) ou preço de venda (expedição).',
    )
    cost_price_at_move = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name='Custo Médio no Momento',
        help_text=(
            'Custo Médio Ponderado (CMVMC) do produto no instante em que este '
            'movimento foi validado. Preenchido automaticamente. Imutável após validação.'
        ),
    )
    uom = models.ForeignKey(
        UoM,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movement_lines',
        verbose_name='Unidade de Medida',
        help_text='Herdado do produto se não definido.',
    )
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Taxa IVA (%)',
        help_text='Copiado do produto aquando da criação da linha.',
    )
    discount_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Desconto (%)',
        help_text='Percentagem de desconto copiada da linha de venda/compra (0–100).',
    )

    class Meta:
        verbose_name = 'Linha de Movimento'
        verbose_name_plural = 'Linhas de Movimento'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.stock_movement.reference} — {self.product.name} ({self.quantity})'

    def save(self, *args, **kwargs):
        # Inherit uom from product if not set
        if not self.uom_id and self.product_id:
            movement = getattr(self, 'stock_movement', None)
            if movement and movement.movement_type == 'receipt' and self.product.uom_purchase_id:
                self.uom = self.product.uom_purchase
            else:
                self.uom = self.product.uom
        # Copy tax_rate from product on first save
        if not self.pk and self.product_id and not self.tax_rate:
            self.tax_rate = self.product.tax_rate
        super().save(*args, **kwargs)

    def quantity_in_product_uom(self):
        from apps.inventory.uom_utils import quantity_to_product_uom
        return quantity_to_product_uom(self.quantity, self.uom, self.product)

    def unit_price_in_product_uom(self):
        from apps.inventory.uom_utils import unit_price_to_product_uom
        return unit_price_to_product_uom(self.unit_price, self.uom, self.product)

    @property
    def line_total(self):
        """Total value for this line: quantity × unit_price × (1 - discount) excl. VAT."""
        from decimal import Decimal
        return (
            Decimal(str(self.quantity))
            * Decimal(str(self.unit_price))
            * (1 - Decimal(str(self.discount_pct)) / 100)
        ).quantize(Decimal('0.01'))

    @property
    def tax_amount(self):
        """VAT amount for this line."""
        from decimal import Decimal
        return (self.line_total * Decimal(str(self.tax_rate)) / Decimal('100')).quantize(Decimal('0.01'))

    @property
    def line_total_with_tax(self):
        """Total value for this line including VAT."""
        return self.line_total + self.tax_amount


class StockQuant(AbstractBaseModel):
    """Current on-hand stock for a product in a warehouse.

    One record per (product, warehouse) pair — enforced by unique_together.
    Created automatically on first stock movement; updated on every validation.
    Negative quantities are prevented by action_validate() before any subtraction.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='quants',
        verbose_name='Produto',
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='quants',
        verbose_name='Armazém',
    )
    quantity = models.DecimalField(
        max_digits=14,
        decimal_places=3,
        default=0,
        verbose_name='Quantidade em Mão',
        help_text='Quantidade física actual neste armazém.',
    )

    class Meta:
        verbose_name = 'Stock Actual'
        verbose_name_plural = 'Stock Actual'
        ordering = ['product__name', 'warehouse__name']
        unique_together = [('product', 'warehouse')]

    def __str__(self):
        return f'{self.product.name} @ {self.warehouse.name}: {self.quantity}'

    @classmethod
    def get_on_hand(cls, product, warehouse=None):
        """Return current on-hand quantity for a product.

        If warehouse is given, returns quantity for that specific warehouse.
        If warehouse is None, returns the total across all warehouses.
        Returns Decimal('0') if no quant record exists yet.
        """
        from decimal import Decimal
        if warehouse is not None:
            try:
                return cls.objects.get(product=product, warehouse=warehouse).quantity
            except cls.DoesNotExist:
                return Decimal('0')
        total = cls.objects.filter(product=product).aggregate(
            total=models.Sum('quantity', output_field=models.DecimalField())
        )['total']
        return total or Decimal('0')

    @classmethod
    def update_quantity(cls, product, warehouse, qty, mode='add'):
        """Add or subtract qty from the stock quant for product/warehouse.

        Uses get_or_create so no quant record needs to exist beforehand.
        mode='add'      → quantity += qty
        mode='subtract' → quantity -= qty  (stock check done in action_validate before calling this)
        """
        from decimal import Decimal
        quant, _ = cls.objects.get_or_create(
            product=product,
            warehouse=warehouse,
            defaults={'quantity': Decimal('0')},
        )
        if mode == 'add':
            quant.quantity += Decimal(str(qty))
        elif mode == 'subtract':
            quant.quantity -= Decimal(str(qty))
        else:
            raise ValueError(f"mode deve ser 'add' ou 'subtract', não '{mode}'.")
        quant.save()
        return quant


class ProductSupplierInfo(AbstractBaseModel):
    """Purchase information for a product from a specific supplier.

    Multiple suppliers can be recorded per product, ordered by sequence.
    The supplier with the lowest sequence (and/or is_preferred=True) is used
    first when auto-generating purchase orders.

    supplier_product_code is the code this supplier uses for this product in
    their invoices/catalogs.  Used in Phase 14 (PDF scanning) as a fallback
    matcher when Product.internal_reference doesn\'t match directly.

    Matching logic (Phase 14):
        1. Try Product.internal_reference  == code on invoice line
        2. Try ProductSupplierInfo where supplier == invoice supplier
           AND supplier_product_code == code on invoice line
        3. If price changed -> auto-update this record + Product.cost_price
    """

    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='supplier_infos',
        verbose_name='Produto',
    )
    supplier = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.CASCADE,
        related_name='product_supplier_infos',
        verbose_name='Fornecedor',
    )
    sequence = models.PositiveSmallIntegerField(
        default=10,
        verbose_name='Sequência',
        help_text='Prioridade de compra. Menor número = mais prioritário.',
    )
    supplier_product_code = models.CharField(
        max_length=64,
        blank=True,
        default='',
        verbose_name='Cód. Fornecedor',
        help_text=(
            'Código que o fornecedor usa para este produto nas suas faturas/catálogo. '
            'Usado para matching automático na leitura de PDFs (Fase 14).'
        ),
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=0,
        verbose_name='Preço de Compra',
        help_text='Preço unitário na UdM de compra do produto. Atualizado automaticamente ao receber faturas.',
    )
    min_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=1,
        verbose_name='Qtd. Mínima',
        help_text='Quantidade mínima de encomenda neste fornecedor.',
    )
    lead_time = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Prazo (dias)',
        help_text='Prazo de entrega em dias úteis.',
    )
    is_preferred = models.BooleanField(
        default=False,
        verbose_name='Preferido',
        help_text='Atalho: assinala este como o fornecedor preferido independentemente da sequência.',
    )
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='product_supplier_infos',
        verbose_name='Empresa',
    )

    class Meta:
        verbose_name = 'Info Fornecedor'
        verbose_name_plural = 'Info Fornecedores'
        ordering = ['sequence', '-is_preferred', 'price']
        unique_together = [('product', 'supplier')]

    def __str__(self):
        return f'{self.supplier.name} → {self.product.name} ({self.price})'

    @classmethod
    def get_best_supplier(cls, product):
        """Return the best (supplier, price) for a product.

        Preferred supplier wins; otherwise the one with the lowest sequence;
        tie-broken by cheapest price.
        Returns None if no supplier_infos exist.
        """
        qs = cls.objects.filter(product=product, is_active=True).order_by(
            '-is_preferred', 'sequence', 'price'
        ).select_related('supplier').first()
        if qs is None:
            return None
        return (qs.supplier, qs.price)

    @classmethod
    def find_by_supplier_code(cls, supplier, code):
        """Lookup used by PDF scanning (Phase 14).

        Given a supplier Contact and a code from their invoice,
        return the matching ProductSupplierInfo or None.
        """
        if not code:
            return None
        return cls.objects.filter(
            supplier=supplier,
            supplier_product_code__iexact=code.strip(),
            is_active=True,
        ).select_related('product').first()


# ---------------------------------------------------------------------------
# Purchase List (Lista de Compras)
# ---------------------------------------------------------------------------

class PurchaseList(AbstractBaseModel):
    """Shopping list header.

    Can be created manually or auto-generated from min_stock levels.
    Each list has N lines (PurchaseListLine) representing products to buy.
    """

    STATE_CHOICES = [
        ('draft',     'Rascunho'),
        ('confirmed', 'Confirmada'),
        ('done',      'Concluída'),
        ('cancelled', 'Cancelada'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Nome',
        help_text='Ex: Compras Semana 10 — gerado automaticamente se deixado em branco.',
    )
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default='draft',
        verbose_name='Estado',
    )
    date = models.DateField(
        default=timezone.localdate,
        verbose_name='Data Prevista',
        help_text='Data prevista para a compra.',
    )
    supplier = models.ForeignKey(
        'contacts.Contact',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchase_lists',
        verbose_name='Fornecedor',
        help_text='Local / fornecedor onde vai ser feita a compra.',
    )
    warehouse = models.ForeignKey(
        'Warehouse',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchase_lists',
        verbose_name='Armazém',
        help_text='Armazém de destino dos produtos comprados.',
    )
    reference = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Referência Externa',
    )
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name='Notas',
    )
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='purchase_lists',
        verbose_name='Empresa',
    )

    class Meta:
        verbose_name = 'Lista de Compras'
        verbose_name_plural = 'Listas de Compras'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return self.name or f'Lista #{self.pk}'

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.generate_name()
        super().save(*args, **kwargs)

    def generate_name(self):
        from django.utils.formats import date_format
        d = self.date or timezone.localdate()
        return f'Compras {date_format(d, "d/m/Y")}'

    # ------------------------------------------------------------------
    # Calculated totals (computed from lines at runtime)
    # ------------------------------------------------------------------

    @property
    def subtotal(self):
        """Sum of all line totals (excl. VAT)."""
        return sum(line.line_total for line in self.lines.all())

    @property
    def vat_amount(self):
        """Sum of all line VAT amounts."""
        return sum(line.line_vat for line in self.lines.all())

    @property
    def total(self):
        """Grand total including VAT."""
        return self.subtotal + self.vat_amount


class PurchaseListLine(AbstractBaseModel):
    """One product line inside a PurchaseList."""

    purchase_list = models.ForeignKey(
        PurchaseList,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name='Lista de Compras',
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.PROTECT,
        related_name='purchase_list_lines',
        verbose_name='Produto',
    )
    uom = models.ForeignKey(
        'UoM',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchase_list_lines',
        verbose_name='Unidade de Medida',
        help_text='Preenchida automaticamente a partir do produto; editável para comprar noutra unidade.',
    )
    # Stock snapshot at time of creation/generation (read-only after save)
    qty_on_hand = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        default=0,
        verbose_name='Stock Actual',
        help_text='Valor gravado no momento de criação/geração da linha.',
    )
    qty_needed = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        default=0,
        verbose_name='Qtd. Necessária',
        help_text='Stock mínimo alvo gravado no momento da geração.',
    )
    qty_to_buy = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        default=0,
        verbose_name='Qtd. a Comprar',
        help_text='Sugerida automaticamente; editável pelo utilizador.',
    )
    purchase_price = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        default=0,
        verbose_name='Preço de Compra',
        help_text='Preço unitário sem IVA.',
    )
    qty_purchased = models.DecimalField(
        max_digits=14,
        decimal_places=4,
        default=0,
        verbose_name='Qtd. Adquirida',
        help_text='Quantidade já colocada no carrinho / recebida no ponto de venda.',
    )
    vat_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name='Taxa IVA (%)',
        help_text='Ex: 23.00 para 23%.',
    )
    notes = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Notas',
    )

    class Meta:
        verbose_name = 'Linha de Lista de Compras'
        verbose_name_plural = 'Linhas de Lista de Compras'
        ordering = ['id']

    def __str__(self):
        return f'{self.product.name} × {self.qty_to_buy}'

    def save(self, *args, **kwargs):
        # Auto-fill uom from product if not set
        if not self.uom_id and self.product_id:
            self.uom = self.product.uom
        super().save(*args, **kwargs)

    # ------------------------------------------------------------------
    # Calculated properties
    # ------------------------------------------------------------------

    @property
    def line_total(self):
        """Total sem IVA: qty_to_buy × purchase_price."""
        return float(self.qty_to_buy) * float(self.purchase_price)

    @property
    def line_vat(self):
        """Valor do IVA desta linha."""
        return self.line_total * float(self.vat_rate) / 100

    @property
    def line_total_with_vat(self):
        """Total com IVA."""
        return self.line_total + self.line_vat
