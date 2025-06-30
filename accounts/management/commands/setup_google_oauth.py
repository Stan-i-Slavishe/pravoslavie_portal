from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings
from decouple import config


class Command(BaseCommand):
    help = 'Настройка Google OAuth для разработки'

    def add_arguments(self, parser):
        parser.add_argument(
            '--client-id',
            type=str,
            help='Google OAuth Client ID',
        )
        parser.add_argument(
            '--secret',
            type=str,
            help='Google OAuth Secret',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Настройка Google OAuth...\n')
        )

        # Настраиваем сайт для разработки
        self.setup_local_site()

        # Получаем учетные данные
        client_id = options.get('client_id') or config('GOOGLE_OAUTH2_CLIENT_ID', default='')
        secret = options.get('secret') or config('GOOGLE_OAUTH2_SECRET', default='')

        if not client_id or not secret:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Google OAuth учетные данные не найдены!\n'
                    'Добавьте их в .env файл:\n'
                    'GOOGLE_OAUTH2_CLIENT_ID=ваш_client_id\n'
                    'GOOGLE_OAUTH2_SECRET=ваш_secret\n\n'
                    'Или используйте параметры:\n'
                    'python manage.py setup_google_oauth --client-id=xxx --secret=yyy'
                )
            )
            return

        # Создаем или обновляем Google приложение
        self.create_google_app(client_id, secret)

        # Проверяем настройки
        self.check_setup()

        self.stdout.write(
            self.style.SUCCESS(
                '\n✅ Google OAuth настроен!\n'
                'Теперь можете тестировать вход через Google на:\n'
                'http://127.0.0.1:8000/accounts/login/\n'
            )
        )

    def setup_local_site(self):
        """Настраивает локальный сайт для разработки"""
        site, created = Site.objects.get_or_create(
            pk=settings.SITE_ID,
            defaults={
                'domain': '127.0.0.1:8000',
                'name': 'Православие Портал (Разработка)'
            }
        )

        if not created and site.domain != '127.0.0.1:8000':
            site.domain = '127.0.0.1:8000'
            site.name = 'Православие Портал (Разработка)'
            site.save()
            self.stdout.write('🔄 Сайт обновлен для локальной разработки')
        else:
            self.stdout.write(f'✅ Сайт настроен: {site.domain}')

        return site

    def create_google_app(self, client_id, secret):
        """Создает или обновляет Google OAuth приложение"""
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth2',
                'client_id': client_id,
                'secret': secret,
            }
        )

        if not created:
            google_app.client_id = client_id
            google_app.secret = secret
            google_app.save()
            self.stdout.write('🔄 Google приложение обновлено')
        else:
            self.stdout.write('✅ Google приложение создано')

        # Привязываем к сайту
        site = Site.objects.get(pk=settings.SITE_ID)
        google_app.sites.add(site)
        self.stdout.write(f'✅ Приложение привязано к сайту {site.domain}')

        return google_app

    def check_setup(self):
        """Проверяет правильность настройки"""
        self.stdout.write('\n🔍 Проверка настроек...')
        
        # Проверяем настройки
        has_google_provider = 'google' in settings.SOCIALACCOUNT_PROVIDERS
        self.stdout.write(f'   Google провайдер: {"✅" if has_google_provider else "❌"}')
        
        # Проверяем сайт
        try:
            site = Site.objects.get(pk=settings.SITE_ID)
            self.stdout.write(f'   Сайт: ✅ {site.domain}')
        except Site.DoesNotExist:
            self.stdout.write('   Сайт: ❌ Не найден')
            return
        
        # Проверяем Google приложение
        try:
            google_app = SocialApp.objects.get(provider='google')
            self.stdout.write(f'   Google приложение: ✅ {google_app.name}')
            
            has_client_id = bool(google_app.client_id)
            has_secret = bool(google_app.secret)
            is_linked_to_site = site in google_app.sites.all()
            
            self.stdout.write(f'   Client ID: {"✅" if has_client_id else "❌"}')
            self.stdout.write(f'   Secret: {"✅" if has_secret else "❌"}')
            self.stdout.write(f'   Привязан к сайту: {"✅" if is_linked_to_site else "❌"}')
            
        except SocialApp.DoesNotExist:
            self.stdout.write('   Google приложение: ❌ Не найдено')
        
        # Показываем URL для тестирования
        self.stdout.write('\n🔗 URL для тестирования:')
        self.stdout.write(f'   Страница входа: http://127.0.0.1:8000/accounts/login/')
        self.stdout.write(f'   Google OAuth: http://127.0.0.1:8000/accounts/google/login/')
        self.stdout.write(f'   Callback URL: http://127.0.0.1:8000/accounts/google/login/callback/')
