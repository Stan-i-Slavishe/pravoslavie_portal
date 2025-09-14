from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.template.loader import render_to_string

class AccountAdapter(DefaultAccountAdapter):
    
    def render_mail(self, template_prefix, email, context):
        """
        Используем кастомные русские шаблоны вместо стандартных allauth
        """
        # Для подтверждения email используем наш шаблон
        if template_prefix == 'account/email/email_confirmation':
            subject = render_to_string('registration/email/email_confirmation_subject.txt', context)
            body = render_to_string('registration/email/email_confirmation_message.txt', context)
            return {
                'subject': subject.strip(),
                'body': body,
            }
        else:
            # Для других типов писем используем стандартные
            return super().render_mail(template_prefix, email, context)

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    pass
