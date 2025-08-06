from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def clean_price(value):
    """Убирает .00 из цены если это целое число"""
    try:
        # Преобразуем в Decimal если это строка
        if isinstance(value, str):
            value = Decimal(value)
        
        # Если это целое число, показываем без дробной части
        if value == int(value):
            return f"{int(value)}₽"
        else:
            return f"{value}₽"
    except (ValueError, TypeError, Decimal.InvalidOperation):
        return f"{value}₽"

@register.filter  
def clean_number(value):
    """Убирает .00 из числа если это целое число"""
    try:
        if isinstance(value, str):
            value = Decimal(value)
        
        if value == int(value):
            return int(value)
        else:
            return value
    except (ValueError, TypeError, Decimal.InvalidOperation):
        return value
