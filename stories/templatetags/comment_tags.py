from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Получает значение из словаря по ключу"""
    if dictionary and key:
        return dictionary.get(key)
    return None

@register.filter  
def user_reaction(user_reactions, comment_id):
    """Получает реакцию пользователя на комментарий"""
    if user_reactions and comment_id:
        return user_reactions.get(comment_id)
    return None
