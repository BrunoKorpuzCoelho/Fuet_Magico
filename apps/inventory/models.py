from django.db import models
from django.core.exceptions import ValidationError
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
        help_text='UdM principal (stock e venda).',
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
        help_text='Preço de venda em €.',
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Preço de Custo',
        help_text='Custo unitário em €.',
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

    def get_sale_price_with_tax(self):
        """Return sale price including IVA."""
        from decimal import Decimal
        return self.sale_price * (1 + self.tax_rate / Decimal('100'))
