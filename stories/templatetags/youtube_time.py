from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def youtube_time(value):
    """
    Отображает время в стиле YouTube - только одна единица времени
    Например: "5 дней назад", "2 месяца назад", "1 год назад"
    """
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value
    
    seconds = diff.total_seconds()
    
    # Годы
    if seconds >= 31536000:  # 365 дней
        years = int(seconds / 31536000)
        if years == 1:
            return "1 год назад"
        elif years < 5:
            return f"{years} года назад"
        else:
            return f"{years} лет назад"
    
    # Месяцы
    elif seconds >= 2592000:  # 30 дней
        months = int(seconds / 2592000)
        if months == 1:
            return "1 месяц назад"
        elif months < 5:
            return f"{months} месяца назад"
        else:
            return f"{months} месяцев назад"
    
    # Недели
    elif seconds >= 604800:  # 7 дней
        weeks = int(seconds / 604800)
        if weeks == 1:
            return "1 неделю назад"
        elif weeks < 5:
            return f"{weeks} недели назад"
        else:
            return f"{weeks} недель назад"
    
    # Дни
    elif seconds >= 86400:  # 1 день
        days = int(seconds / 86400)
        if days == 1:
            return "1 день назад"
        elif days < 5:
            return f"{days} дня назад"
        else:
            return f"{days} дней назад"
    
    # Часы
    elif seconds >= 3600:  # 1 час
        hours = int(seconds / 3600)
        if hours == 1:
            return "1 час назад"
        elif hours < 5:
            return f"{hours} часа назад"
        else:
            return f"{hours} часов назад"
    
    # Минуты
    elif seconds >= 60:
        minutes = int(seconds / 60)
        if minutes == 1:
            return "1 минуту назад"
        elif minutes < 5:
            return f"{minutes} минуты назад"
        else:
            return f"{minutes} минут назад"
    
    # Секунды
    else:
        return "только что"
