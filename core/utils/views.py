"""
Утилита для отслеживания просмотров с защитой от накрутки
"""


def track_view_session(request, obj, field_name='views_count'):
    """
    Отслеживает просмотр объекта один раз за сессию
    
    Args:
        request: HTTP запрос
        obj: Объект для отслеживания (должен иметь поле views_count)
        field_name: Название поля со счетчиком просмотров
    
    Returns:
        bool: True если просмотр засчитан, False если нет
    """
    # Создаем уникальный ключ для сессии
    session_key = f'viewed_{obj.__class__.__name__.lower()}_{obj.pk}'
    
    # Проверяем, был ли объект уже просмотрен в этой сессии
    if not request.session.get(session_key, False):
        # Увеличиваем счетчик просмотров
        current_count = getattr(obj, field_name, 0)
        obj.__class__.objects.filter(pk=obj.pk).update(**{field_name: current_count + 1})
        
        # Отмечаем в сессии, что объект был просмотрен
        request.session[session_key] = True
        
        return True
    
    return False


def get_client_ip(request):
    """Получение IP-адреса клиента"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    return ip
