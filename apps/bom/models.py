from decimal import Decimal
from django.db import models
from apps.core.models import AbstractBaseModel


class ProductBOM(AbstractBaseModel):
    """
    Bill of Materials — Receita de um produto manufaturado.

    Define quais ingredientes/componentes são necessários para produzir
    uma determinada quantidade do produto final (qty_produced).

    Exemplo:
        product       = "Bolo de Chocolate - Fatia"
        qty_produced  = 12  (a receita produz 12 fatias)
        uom           = Fatia
        labor_cost    = 5.00 €  (custo de mão-de-obra por produção)
        lines         = [Farinha 500g, Açúcar 300g, Ovos 3un, ...]
    """

    product = models.OneToOneField(
        'inventory.Product',
        on_delete=models.CASCADE,
        related_name='bom',
        verbose_name='Produto',
        help_text='Produto acabado que esta receita produz.',
    )
    internal_reference = models.CharField(
        max_length=64,
        blank=True,
        default='',
        verbose_name='Referência Interna',
        help_text='Código único desta receita (ex: BOM-001).',
    )
    qty_produced = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        default=Decimal('1'),
        verbose_name='Quantidade Produzida',
        help_text='Quantidade do produto final produzida por uma execução desta receita. Ex: 12 fatias.',
    )
    uom = models.ForeignKey(
        'inventory.UoM',
        on_delete=models.PROTECT,
        related_name='boms',
        verbose_name='UdM do Produto',
        help_text='Unidade de medida do produto final. Ex: Fatia, Unidade, kg.',
    )
    labor_cost = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        default=Decimal('0'),
        verbose_name='Custo de Mão-de-obra (€)',
        help_text='Custo de mão-de-obra por execução completa desta receita (não por unidade).',
    )
    notes = models.TextField(
        blank=True,
        default='',
        verbose_name='Notas',
        help_text='Instruções de preparação, anotações, etc.',
    )
    owner_company = models.ForeignKey(
        'core.Company',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='boms',
        verbose_name='Empresa',
        help_text='NULL = global.',
    )

    class Meta:
        verbose_name = 'Receita (BOM)'
        verbose_name_plural = 'Receitas (BOM)'
        ordering = ['product__name']
        constraints = [
            models.UniqueConstraint(
                condition=models.Q(internal_reference__gt=''),
                fields=('internal_reference', 'owner_company'),
                name='unique_bom_internal_ref_per_company',
            ),
        ]

    def __str__(self):
        return f'BOM: {self.product.name} ({self.qty_produced} {self.uom.symbol})'

    # ── Cálculo de custos ────────────────────────────────────────────

    def calculate_total_cost(self) -> Decimal:
        """
        Calcula o custo total de UMA execução desta receita.
        Inclui todos os componentes (recursivos) + mão-de-obra.
        """
        total = Decimal('0')
        for line in self.lines.select_related('component__bom', 'uom').all():
            total += line.calculate_cost()
        total += self.labor_cost
        return total

    def calculate_unit_cost(self) -> Decimal:
        """
        Custo por unidade do produto final.
        Ex: custo total = 24€, qty_produced = 12 → custo por fatia = 2€
        """
        if not self.qty_produced:
            return Decimal('0')
        return self.calculate_total_cost() / self.qty_produced

    def calculate_total_sale(self) -> Decimal:
        """
        Calcula o preço total de venda de UMA execução desta receita.
        Soma (component.sale_price * qty) de todas as linhas.
        """
        total = Decimal('0')
        for line in self.lines.select_related('component').all():
            total += (line.component.sale_price or Decimal('0')) * line.quantity
        return total

    def calculate_unit_sale(self) -> Decimal:
        """Preço de venda por unidade do produto final."""
        if not self.qty_produced:
            return Decimal('0')
        return self.calculate_total_sale() / self.qty_produced

    def sync_to_product(self):
        """Actualiza cost_price e sale_price do produto com os valores calculados pelo BOM."""
        self.product.cost_price = self.calculate_unit_cost().quantize(Decimal('0.01'))
        self.product.sale_price = self.calculate_unit_sale().quantize(Decimal('0.01'))
        self.product.save(update_fields=['cost_price', 'sale_price', 'updated_at'])

    def update_product_cost(self):
        """Compat: mantém API antiga, delega para sync_to_product."""
        self.sync_to_product()


class ProductBOMLine(AbstractBaseModel):
    """
    Uma linha de componente numa receita BOM.

    O componente pode ser:
    - Matéria-prima (sem BOM) → custo = component.cost_price convertido para a uom desta linha
    - Subproduto (com BOM)    → custo = BOM do componente (recursivo)
    """

    bom = models.ForeignKey(
        ProductBOM,
        on_delete=models.CASCADE,
        related_name='lines',
        verbose_name='Receita',
    )
    component = models.ForeignKey(
        'inventory.Product',
        on_delete=models.PROTECT,
        related_name='bom_lines',
        verbose_name='Componente',
        help_text='Ingrediente ou sub-produto que compõe esta receita.',
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        verbose_name='Quantidade',
        help_text='Quantidade deste componente necessária para produzir qty_produced do produto final.',
    )
    uom = models.ForeignKey(
        'inventory.UoM',
        on_delete=models.PROTECT,
        related_name='bom_lines',
        verbose_name='UdM',
        help_text='Unidade em que a quantidade é expressa nesta linha.',
    )
    sequence = models.PositiveSmallIntegerField(
        default=10,
        verbose_name='Ordem',
        help_text='Ordem de apresentação na receita.',
    )
    notes = models.CharField(
        max_length=255,
        blank=True,
        default='',
        verbose_name='Notas',
    )

    class Meta:
        verbose_name = 'Linha de Receita'
        verbose_name_plural = 'Linhas de Receita'
        ordering = ['sequence', 'component__name']

    def __str__(self):
        return f'{self.quantity} {self.uom.symbol} {self.component.name}'

    # ── Custo desta linha ────────────────────────────────────────────

    def get_component_unit_cost(self) -> Decimal:
        """
        Custo unitário do componente na unidade BASE do componente (component.uom).

        - Se o componente TEM BOM → custo vem do BOM (recursivo).
        - Se NÃO tem BOM → custo vem do cost_price do produto.
        """
        if hasattr(self.component, 'bom') and self.component.bom:
            return self.component.bom.calculate_unit_cost()
        return self.component.cost_price or Decimal('0')

    def calculate_cost(self) -> Decimal:
        """
        Custo desta linha = quantidade (convertida para a UdM do componente) × custo unitário.

        A conversão UoM só é possível dentro da mesma categoria.
        Ex: linha em kg, componente em g → converte 0.5 kg → 500 g → calcula custo em g.
        """
        component_uom = self.component.uom
        unit_cost = self.get_component_unit_cost()  # custo por 1 component_uom

        # Converter a quantidade desta linha para a UdM base do componente
        if self.uom_id == component_uom.pk:
            qty_in_component_uom = self.quantity
        else:
            try:
                qty_in_component_uom = self.uom.convert_to(self.quantity, component_uom)
            except ValueError:
                # Categorias diferentes — não é possível converter; usa a quantidade directa
                qty_in_component_uom = self.quantity

        return (qty_in_component_uom * unit_cost).quantize(Decimal('0.0001'))
