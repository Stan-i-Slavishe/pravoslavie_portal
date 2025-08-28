from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib import messages

@receiver(pre_social_login)
def handle_social_login(sender, request, sociallogin, **kwargs):
    """
    Обработка социального входа без дублирования сообщений
    """
    # Если пользователь уже существует, просто пропускаем
    # (allauth сам обработает вход и покажет одно сообщение)
    if sociallogin.user and sociallogin.user.pk:
        # Убираем дополнительный perform_login - он дублирует сообщения
        # Просто добавляем кастомную логику если нужно
        pass
    
    # Можно добавить дополнительную логику здесь,
    # но без дублирования входа в систему
