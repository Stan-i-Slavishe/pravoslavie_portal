from django.core.management.base import BaseCommand
from pwa.models import NotificationCategory


class Command(BaseCommand):
    help = 'Создает базовые категории уведомлений для административного управления'

    def handle(self, *args, **options):
        """Создаем основные категории уведомлений"""
        
        categories_data = [
            {
                'name': 'bedtime_stories',
                'title': 'Сказки на ночь',
                'description': 'Напоминания о чтении сказок перед сном',
                'icon': '🌙',
                'is_active': False,  # По умолчанию ВЫКЛЮЧЕНО
                'default_enabled': True
            },
            {
                'name': 'orthodox_calendar',
                'title': 'Православный календарь',
                'description': 'Уведомления о праздниках и постах',
                'icon': '⛪',
                'is_active': True,  # АКТИВНО
                'default_enabled': True
            },
            {
                'name': 'new_content',
                'title': 'Новый контент',
                'description': 'Уведомления о новых духовных рассказах и видео',
                'icon': '🎬',
                'is_active': True,  # АКТИВНО
                'default_enabled': True
            },
            {
                'name': 'fairy_tales',
                'title': 'Терапевтические сказки',
                'description': 'Рекомендации сказок для решения проблем',
                'icon': '🧚',
                'is_active': True,  # АКТИВНО
                'default_enabled': True
            },
            {
                'name': 'book_releases',
                'title': 'Новые книги',
                'description': 'Уведомления о поступлении новых книг',
                'icon': '📖',
                'is_active': True,  # АКТИВНО
                'default_enabled': True
            },
            {
                'name': 'audio_content',
                'title': 'Аудио-контент',
                'description': 'Новые аудио-рассказы и подкасты',
                'icon': '🎵',
                'is_active': False,  # По умолчанию ВЫКЛЮЧЕНО (еще не готово)
                'default_enabled': False
            },
            {
                'name': 'special_events',
                'title': 'Особые события',
                'description': 'Уведомления об особых событиях и мероприятиях',
                'icon': '🎉',
                'is_active': False,  # По умолчанию ВЫКЛЮЧЕНО
                'default_enabled': False
            },
            {
                'name': 'daily_wisdom',
                'title': 'Мудрость дня',
                'description': 'Ежедневные духовные наставления',
                'icon': '💭',
                'is_active': False,  # По умолчанию ВЫКЛЮЧЕНО
                'default_enabled': False
            }
        ]

        created_count = 0
        updated_count = 0

        for category_data in categories_data:
            category, created = NotificationCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'title': category_data['title'],
                    'description': category_data['description'],
                    'icon': category_data['icon'],
                    'is_active': category_data['is_active'],
                    'default_enabled': category_data['default_enabled']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Создана категория: {category.title}')
                )
            else:
                # Обновляем существующую категорию
                category.title = category_data['title']
                category.description = category_data['description']
                category.icon = category_data['icon']
                # НЕ обновляем is_active, чтобы сохранить админские настройки
                category.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'🔄 Обновлена категория: {category.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Итоги:\n'
                f'  • Создано новых категорий: {created_count}\n'
                f'  • Обновлено существующих: {updated_count}\n'
                f'  • Всего категорий в системе: {NotificationCategory.objects.count()}'
            )
        )

        # Показываем статус активности
        self.stdout.write(
            self.style.HTTP_INFO('\n🎛️ Текущий статус категорий:')
        )
        
        for category in NotificationCategory.objects.all().order_by('name'):
            status = '🟢 АКТИВНА' if category.is_active else '🔴 ОТКЛЮЧЕНА'
            self.stdout.write(f'  {category.icon} {category.title}: {status}')

        self.stdout.write(
            self.style.HTTP_INFO(
                '\n💡 Совет: Вы можете управлять активностью категорий через Django Admin:\n'
                '  /admin/pwa/notificationcategory/'
            )
        )
