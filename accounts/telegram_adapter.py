from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
import logging

logger = logging.getLogger(__name__)

class TelegramSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        logger.error(f"Telegram pre_social_login called")
        logger.error(f"User data: {sociallogin.account.extra_data}")
        super().pre_social_login(request, sociallogin)
