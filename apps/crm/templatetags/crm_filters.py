from django import template

register = template.Library()


@register.filter
def short_value(value):
    """
    Formata valores grandes com sufixos K, M, B.
    Ex: 1500 -> 1.5K, 137000 -> 137K, 2000000 -> 2M, 1500000000 -> 1.5B
    Valores < 1000 ficam como estão.
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        return '0'

    if value >= 1_000_000_000:
        formatted = value / 1_000_000_000
        if formatted == int(formatted):
            return f'{int(formatted)}B'
        return f'{formatted:.1f}B'
    elif value >= 1_000_000:
        formatted = value / 1_000_000
        if formatted == int(formatted):
            return f'{int(formatted)}M'
        return f'{formatted:.1f}M'
    elif value >= 1_000:
        formatted = value / 1_000
        if formatted == int(formatted):
            return f'{int(formatted)}K'
        return f'{formatted:.1f}K'
    else:
        return str(int(value))
