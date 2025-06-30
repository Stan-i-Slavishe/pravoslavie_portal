from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Category, Tag, SiteSettings


class Command(BaseCommand):
    help = 'Создает базовые данные для проекта (категории, теги, настройки)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--superuser',
            action='store_true',
            help='Создать суперпользователя',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Создание базовых данных для Православного портала...')
        )

        # Создаем настройки сайта
        self.create_site_settings()
        
        # Создаем базовые категории
        self.create_categories()
        
        # Создаем базовые теги
        self.create_tags()
        
        # Создаем суперпользователя если нужно
        if options['superuser']:
            self.create_superuser()

        self.stdout.write(
            self.style.SUCCESS('✅ Базовые данные успешно созданы!')
        )

    def create_site_settings(self):
        """Создать настройки сайта"""
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        if created:
            self.stdout.write('✅ Настройки сайта созданы')
        else:
            self.stdout.write('ℹ️  Настройки сайта уже существуют')

    def create_categories(self):
        """Создать базовые категории"""
        categories_data = [
            # Видео-рассказы
            {
                'name': 'Духовные истории',
                'content_type': 'story',
                'description': 'Рассказы о духовных переживаниях и опыте веры',
                'icon': 'bi-heart',
                'color': '#e17055',
                'order': 1
            },
            {
                'name': 'Жития святых',
                'content_type': 'story',
                'description': 'Видео-рассказы о жизни православных святых',
                'icon': 'bi-star',
                'color': '#fdcb6e',
                'order': 2
            },
            {
                'name': 'Паломничество',
                'content_type': 'story',
                'description': 'Рассказы о паломнических поездках и святых местах',
                'icon': 'bi-geo-alt',
                'color': '#00b894',
                'order': 3
            },
            
            # Книги
            {
                'name': 'Духовная литература',
                'content_type': 'book',
                'description': 'Книги о православной вере и духовности',
                'icon': 'bi-book',
                'color': '#0984e3',
                'order': 10
            },
            {
                'name': 'Богословие',
                'content_type': 'book',
                'description': 'Богословские труды и исследования',
                'icon': 'bi-mortarboard',
                'color': '#6c5ce7',
                'order': 11
            },
            {
                'name': 'Детские книги',
                'content_type': 'book',
                'description': 'Православная литература для детей',
                'icon': 'bi-emoji-smile',
                'color': '#fd79a8',
                'order': 12
            },
            
            # Аудио
            {
                'name': 'Проповеди',
                'content_type': 'audio',
                'description': 'Аудиозаписи проповедей священников',
                'icon': 'bi-mic',
                'color': '#00cec9',
                'order': 20
            },
            {
                'name': 'Акафисты',
                'content_type': 'audio',
                'description': 'Аудиозаписи православных акафистов',
                'icon': 'bi-music-note',
                'color': '#a29bfe',
                'order': 21
            },
            {
                'name': 'Аудиокниги',
                'content_type': 'audio',
                'description': 'Духовная литература в аудиоформате',
                'icon': 'bi-headphones',
                'color': '#74b9ff',
                'order': 22
            },
        ]

        created_count = 0
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                created_count += 1

        self.stdout.write(f'✅ Создано категорий: {created_count}')

    def create_tags(self):
        """Создать базовые теги"""
        tags_data = [
            {'name': 'вера', 'color': '#e17055'},
            {'name': 'молитва', 'color': '#0984e3'},
            {'name': 'покаяние', 'color': '#6c5ce7'},
            {'name': 'любовь', 'color': '#fd79a8'},
            {'name': 'смирение', 'color': '#00b894'},
            {'name': 'надежда', 'color': '#fdcb6e'},
            {'name': 'семья', 'color': '#e84393'},
            {'name': 'дети', 'color': '#00cec9'},
            {'name': 'воспитание', 'color': '#a29bfe'},
            {'name': 'традиции', 'color': '#74b9ff'},
            {'name': 'праздники', 'color': '#55a3ff'},
            {'name': 'пост', 'color': '#81ecec'},
            {'name': 'исповедь', 'color': '#fab1a0'},
            {'name': 'причастие', 'color': '#ff7675'},
            {'name': 'храм', 'color': '#636e72'},
        ]

        created_count = 0
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_data['name'],
                defaults=tag_data
            )
            if created:
                created_count += 1

        self.stdout.write(f'✅ Создано тегов: {created_count}')

    def create_superuser(self):
        """Создать суперпользователя"""
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@pravoslavie-portal.ru',
                password='admin123'
            )
            self.stdout.write(
                self.style.WARNING('⚠️  Создан суперпользователь:')
            )
            self.stdout.write('   Логин: admin')
            self.stdout.write('   Пароль: admin123')
            self.stdout.write('   🔒 ОБЯЗАТЕЛЬНО смените пароль в продакшене!')
        else:
            self.stdout.write('ℹ️  Суперпользователь уже существует')