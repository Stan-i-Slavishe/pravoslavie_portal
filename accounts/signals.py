from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib.auth import login
from allauth.account.utils import perform_login

@receiver(pre_social_login)
def auto_login_social_user(sender, request, sociallogin, **kwargs):
    """
    Автоматически авторизует пользователя после успешной социальной авторизации
    """
    # Если пользователь уже существует, авторизуем его
    if sociallogin.user and sociallogin.user.pk:
        perform_login(request, sociallogin.user, email_verification='none')
