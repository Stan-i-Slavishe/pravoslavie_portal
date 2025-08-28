from django import template
from django.utils.safestring import mark_safe
import math

register = template.Library()


@register.filter
def smart_category_split(categories, target_visible=5):
    """
    Умное разделение категорий на видимые и скрытые
    с учетом длины названий для оптимального заполнения строки
    """
    if not categories:
        return {'visible': [], 'hidden': []}
    
    categories_list = list(categories)
    total_categories = len(categories_list)
    
    if total_categories <= target_visible:
        return {
            'visible': categories_list,
            'hidden': [],
            'has_hidden': False,
            'hidden_count': 0
        }
    
    # Простая логика: показываем первые target_visible категорий
    # Но с учетом длины названий для более равномерного распределения
    
    visible_categories = []
    hidden_categories = []
    
    # Вычисляем "вес" категорий по длине названия
    category_weights = []
    for cat in categories_list:
        # Базовый вес + дополнительный вес за длинные названия
        weight = len(cat.name) / 10  # нормализуем длину
        category_weights.append((cat, weight))
    
    # Сортируем по весу (короткие названия первыми для лучшего заполнения)
    sorted_by_weight = sorted(category_weights, key=lambda x: x[1])
    
    # Берем первые категории, но стараемся уместить их в разумные рамки
    current_weight = 0
    max_weight_per_row = 3.5  # примерная оценка "веса" строки
    
    for cat, weight in sorted_by_weight:
        if len(visible_categories) < target_visible and current_weight + weight <= max_weight_per_row:
            visible_categories.append(cat)
            current_weight += weight
        else:
            hidden_categories.append(cat)
    
    # Если у нас слишком мало видимых категорий, добавляем еще
    remaining_categories = [cat for cat, _ in sorted_by_weight if cat not in visible_categories and cat not in hidden_categories]
    
    while len(visible_categories) < target_visible and remaining_categories:
        visible_categories.append(remaining_categories.pop(0))
    
    # Все оставшиеся идут в скрытые
    hidden_categories.extend(remaining_categories)
    
    # Сортируем обратно по оригинальному порядку
    original_order = {cat.id: i for i, cat in enumerate(categories_list)}
    visible_categories.sort(key=lambda x: original_order[x.id])
    hidden_categories.sort(key=lambda x: original_order[x.id])
    
    return {
        'visible': visible_categories,
        'hidden': hidden_categories,
        'has_hidden': len(hidden_categories) > 0,
        'hidden_count': len(hidden_categories)
    }


@register.filter
def estimate_row_capacity(categories, avg_chars_per_button=12):
    """
    Оценивает, сколько категорий поместится в одной строке
    на основе средней длины названий
    """
    if not categories:
        return 5
    
    # Средняя длина названий категорий
    total_chars = sum(len(cat.name) for cat in categories)
    avg_length = total_chars / len(categories)
    
    # Примерная оценка количества кнопок в строке
    # Исходя из ширины экрана ~1200px и ширины кнопки ~150-200px
    estimated_buttons_per_row = max(3, min(8, int(50 / avg_length)))
    
    return estimated_buttons_per_row


@register.filter
def optimize_category_display(categories):
    """
    Оптимизированное отображение категорий с учетом их длины
    """
    if not categories:
        return {'visible': [], 'hidden': []}
    
    categories_list = list(categories)
    
    # Анализируем длину названий
    short_categories = []  # <= 15 символов
    medium_categories = []  # 16-25 символов  
    long_categories = []   # > 25 символов
    
    for cat in categories_list:
        name_length = len(cat.name)
        if name_length <= 15:
            short_categories.append(cat)
        elif name_length <= 25:
            medium_categories.append(cat)
        else:
            long_categories.append(cat)
    
    # Формируем первую строку: стараемся уместить оптимально
    visible_categories = []
    
    # Сначала добавляем короткие (помещается больше)
    visible_categories.extend(short_categories[:3])
    
    # Добавляем средние, если есть место
    remaining_slots = 5 - len(visible_categories)
    if remaining_slots > 0:
        visible_categories.extend(medium_categories[:remaining_slots])
    
    # Добавляем длинные, если еще есть место
    remaining_slots = 5 - len(visible_categories)
    if remaining_slots > 0:
        visible_categories.extend(long_categories[:remaining_slots])
    
    # Все остальные - в скрытые
    hidden_categories = []
    hidden_categories.extend(short_categories[3:])
    hidden_categories.extend(medium_categories[max(0, 5-len(short_categories[:3])):])
    hidden_categories.extend(long_categories[max(0, 5-len(visible_categories)):])
    
    # Сортируем по оригинальному порядку
    original_order = {cat.id: i for i, cat in enumerate(categories_list)}
    visible_categories.sort(key=lambda x: original_order[x.id])
    hidden_categories.sort(key=lambda x: original_order[x.id])
    
    return {
        'visible': visible_categories,
        'hidden': hidden_categories,
        'has_hidden': len(hidden_categories) > 0,
        'hidden_count': len(hidden_categories)
    }


@register.inclusion_tag('fairy_tales/category_buttons.html')
def render_category_buttons(categories, current_category=''):
    """
    Рендерит кнопки категорий с оптимальным распределением
    """
    optimized = optimize_category_display(categories)
    
    return {
        'visible_categories': optimized['visible'],
        'hidden_categories': optimized['hidden'],
        'has_hidden_categories': optimized['has_hidden'],
        'hidden_count': optimized['hidden_count'],
        'current_category': current_category
    }
