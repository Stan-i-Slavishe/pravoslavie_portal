from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Кастомный backend аутентификации, который позволяет входить 
    как по email, так и по username
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('email')
        
        if username is None or password is None:
            return None
        
        try:
            # Пытаемся найти пользователя по email или username
            user = User.objects.get(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
        except User.DoesNotExist:
            # Запускаем хеширование пароля для защиты от атак времени
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # Если найдено несколько пользователей, берем первого
            user = User.objects.filter(
                Q(email__iexact=username) | Q(username__iexact=username)
            ).first()
        
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
