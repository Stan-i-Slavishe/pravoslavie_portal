from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    help = 'Подтвердить email пользователя'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email пользователя для подтверждения')

    def handle(self, *args, **options):
        email = options['email']
        
        try:
            # Находим пользователя
            user = User.objects.get(email=email)
            
            # Находим или создаем EmailAddress
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=email,
                defaults={
                    'verified': True,
                    'primary': True
                }
            )
            
            if not email_address.verified:
                email_address.verified = True
                email_address.save()
                
            if not email_address.primary:
                email_address.primary = True
                email_address.save()
                
            # Активируем пользователя
            if not user.is_active:
                user.is_active = True
                user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Email {email} успешно подтвержден для пользователя {user.username}')
            )
            
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Пользователь с email {email} не найден')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Ошибка: {str(e)}')
            )
