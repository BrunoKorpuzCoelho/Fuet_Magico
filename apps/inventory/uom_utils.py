"""
Helpers for converting quantities and prices between units of measure.

All stock (StockQuant), cost_price and sale_price on Product are stored in
product.uom (the base / stock unit).  Document lines (PO, SO, movements) may
use a different UoM; these helpers normalise to the product base unit.
"""
from decimal import Decimal, ROUND_HALF_UP


def get_line_uom(line_uom, product):
    """Return the UoM used on a line, falling back to the product base UoM."""
    return line_uom if line_uom else product.uom


def quantity_to_product_uom(quantity, line_uom, product) -> Decimal:
    """Convert a line quantity to the product's base (stock) UoM."""
    uom = get_line_uom(line_uom, product)
    product_uom = product.uom
    qty = Decimal(str(quantity))
    if uom.pk == product_uom.pk:
        return qty
    return uom.convert_to(qty, product_uom)


def unit_price_to_product_uom(unit_price, line_uom, product) -> Decimal:
    """Convert a unit price expressed in line_uom to price per product.uom."""
    uom = get_line_uom(line_uom, product)
    product_uom = product.uom
    price = Decimal(str(unit_price or 0))
    if uom.pk == product_uom.pk:
        return price
    return (price * product_uom.factor / uom.factor).quantize(
        Decimal('0.000001'), rounding=ROUND_HALF_UP
    )


def unit_price_from_product_uom(product_price, target_uom, product) -> Decimal:
    """Convert product.cost_price / sale_price (per product.uom) to target_uom."""
    product_uom = product.uom
    price = Decimal(str(product_price or 0))
    if target_uom.pk == product_uom.pk:
        return price
    return (price * target_uom.factor / product_uom.factor).quantize(
        Decimal('0.0004'), rounding=ROUND_HALF_UP
    )
