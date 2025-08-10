from django import template

register = template.Library()

@register.filter
def russian_pluralize(count, forms):
    """
    Склоняет слова в зависимости от числа для русского языка.
    
    Использование:
    {{ count|russian_pluralize:"рассказ,рассказа,рассказов" }}
    
    Правила:
    1, 21, 31, 101, 121... → рассказ
    2, 3, 4, 22, 23, 24, 102, 103, 104... → рассказа  
    5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25, 100, 111, 112... → рассказов
    """
    try:
        count = int(count)
        forms_list = forms.split(',')
        
        if len(forms_list) != 3:
            return forms_list[0] if forms_list else ''
        
        form1, form2, form3 = forms_list  # рассказ, рассказа, рассказов
        
        # Определяем правильную форму
        if count % 10 == 1 and count % 100 != 11:
            return form1  # 1, 21, 31... рассказ
        elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
            return form2  # 2, 3, 4, 22, 23, 24... рассказа
        else:
            return form3  # 5, 6, 7, 8, 9, 10, 11, 12... рассказов
            
    except (ValueError, TypeError):
        return forms.split(',')[0] if forms else ''

@register.filter  
def russian_count_with_word(count, forms):
    """
    Возвращает число с правильно склоненным словом.
    
    Использование:
    {{ count|russian_count_with_word:"рассказ,рассказа,рассказов" }}
    
    Результат:
    "1 рассказ", "2 рассказа", "5 рассказов"
    """
    word = russian_pluralize(count, forms)
    return f"{count} {word}"

@register.simple_tag
def pluralize_stories(count):
    """
    Простой тег для склонения слова "рассказ".
    
    Использование:
    {% pluralize_stories count %}
    """
    return russian_count_with_word(count, "рассказ,рассказа,рассказов")
