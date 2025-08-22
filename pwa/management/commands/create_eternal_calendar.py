# Команда для создания вечного православного календаря

from django.core.management.base import BaseCommand
from django.db import transaction
from pwa.models import FastingPeriod, OrthodoxEvent, DailyOrthodoxInfo
from datetime import date


class Command(BaseCommand):
    help = 'Создать базовые данные для вечного православного календаря'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед созданием новых',
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            if options['clear']:
                self.stdout.write(self.style.WARNING('Очистка существующих данных...'))
                FastingPeriod.objects.all().delete()
                # Не удаляем OrthodoxEvent и DailyOrthodoxInfo, так как там могут быть пользовательские данные

            self.create_fasting_periods()
            self.create_basic_orthodox_events()
            
            self.stdout.write(
                self.style.SUCCESS('Вечный православный календарь успешно создан!')
            )

    def create_fasting_periods(self):
        """Создать периоды постов"""
        
        self.stdout.write('Создание периодов постов...')
        
        # Великий пост (переходящий, зависит от Пасхи)
        great_lent, created = FastingPeriod.objects.get_or_create(
            name='great_lent',
            defaults={
                'title': 'Великий пост',
                'description': 'Время подготовки к Пасхе, самый строгий пост в году',
                'easter_start_offset': -48,  # Начинается за 48 дней до Пасхи (Чистый понедельник)
                'easter_end_offset': -1,     # Заканчивается накануне Пасхи
                'fasting_rules': {
                    'monday': 'dry_eating',      # Понедельник - сухоядение
                    'tuesday': 'with_oil',       # Вторник - с маслом
                    'wednesday': 'dry_eating',   # Среда - сухоядение
                    'thursday': 'with_oil',      # Четверг - с маслом
                    'friday': 'dry_eating',      # Пятница - сухоядение
                    'saturday': 'wine_oil',      # Суббота - вино и масло
                    'sunday': 'wine_oil',        # Воскресенье - вино и масло
                },
                'priority': 10,  # Высший приоритет
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'  ✓ Создан: {great_lent.title}')

        # Рождественский пост (фиксированный)
        christmas_fast, created = FastingPeriod.objects.get_or_create(
            name='christmas_fast',
            defaults={
                'title': 'Рождественский пост',
                'description': 'Подготовка к празднику Рождества Христова',
                'start_month': 11,
                'start_day': 28,
                'end_month': 1,
                'end_day': 6,
                'fasting_rules': {
                    'monday': 'light_fast',
                    'tuesday': 'with_fish',      # Можно рыбу
                    'wednesday': 'light_fast',
                    'thursday': 'with_fish',
                    'friday': 'light_fast',
                    'saturday': 'with_fish',
                    'sunday': 'with_fish',
                },
                'priority': 8,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'  ✓ Создан: {christmas_fast.title}')

        # Успенский пост (фиксированный)
        assumption_fast, created = FastingPeriod.objects.get_or_create(
            name='assumption_fast',
            defaults={
                'title': 'Успенский пост',
                'description': 'Пост перед праздником Успения Пресвятой Богородицы',
                'start_month': 8,
                'start_day': 14,
                'end_month': 8,
                'end_day': 27,
                'fasting_rules': {
                    'monday': 'strict_fast',
                    'tuesday': 'strict_fast',
                    'wednesday': 'strict_fast',
                    'thursday': 'strict_fast',
                    'friday': 'strict_fast',
                    'saturday': 'with_oil',
                    'sunday': 'with_oil',
                },
                'priority': 7,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'  ✓ Создан: {assumption_fast.title}')

        # Петров пост (переходящий)
        peter_paul_fast, created = FastingPeriod.objects.get_or_create(
            name='peter_paul_fast',
            defaults={
                'title': 'Петров пост',
                'description': 'Пост перед днем святых апостолов Петра и Павла',
                'easter_start_offset': 57,   # Начинается через 57 дней после Пасхи (понедельник Всех святых)
                'easter_end_offset': 69,     # Заканчивается 11 июля (день перед Петром и Павлом)
                'fasting_rules': {
                    'monday': 'light_fast',
                    'tuesday': 'with_fish',
                    'wednesday': 'light_fast',
                    'thursday': 'with_fish',
                    'friday': 'light_fast',
                    'saturday': 'with_fish',
                    'sunday': 'with_fish',
                },
                'priority': 6,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(f'  ✓ Создан: {peter_paul_fast.title}')

    def create_basic_orthodox_events(self):
        """Создать основные православные события"""
        
        self.stdout.write('Создание основных православных событий...')
        
        # Великие праздники (фиксированные даты)
        great_feasts = [
            (1, 7, 'Рождество Христово', 'Рождение Иисуса Христа'),
            (1, 19, 'Крещение Господне (Богоявление)', 'Крещение Иисуса Христа в Иордане'),
            (2, 15, 'Сретение Господне', 'Встреча Симеона и Анны с младенцем Иисусом'),
            (3, 25, 'Благовещение Пресвятой Богородицы', 'Благая весть архангела Гавриила Деве Марии'),
            (8, 19, 'Преображение Господне', 'Преображение Иисуса на горе Фавор'),
            (8, 28, 'Успение Пресвятой Богородицы', 'Успение Божией Матери'),
            (9, 21, 'Рождество Пресвятой Богородицы', 'Рождение Девы Марии'),
            (9, 27, 'Воздвижение Креста Господня', 'Обретение и воздвижение Креста Христова'),
            (12, 4, 'Введение во храм Пресвятой Богородицы', 'Введение трехлетней Марии в храм'),
        ]
        
        for month, day, title, description in great_feasts:
            event, created = OrthodoxEvent.objects.get_or_create(
                month=month,
                day=day,
                title=title,
                defaults={
                    'description': description,
                    'event_type': 'great_feast',
                    'is_movable': False,
                    'is_old_style': False,
                }
            )
            if created:
                self.stdout.write(f'  ✓ Создан праздник: {event.title}')

        # Переходящие праздники (зависят от Пасхи)
        movable_feasts = [
            (0, 'Пасха Христова', 'Воскресение Иисуса Христа', 'great_feast'),
            (-7, 'Вход Господень в Иерусалим (Вербное воскресенье)', 'Торжественный вход Христа в Иерусалим', 'great_feast'),
            (39, 'Вознесение Господне', 'Вознесение Иисуса Христа на небо', 'great_feast'),
            (49, 'День Святой Троицы (Пятидесятница)', 'Сошествие Святого Духа на апостолов', 'great_feast'),
            (-49, 'Начало Великого поста', 'Чистый понедельник - начало подготовки к Пасхе', 'fast_start'),
            (-8, 'Лазарева суббота', 'Воскрешение Лазаря Христом', 'major_feast'),
        ]
        
        for offset, title, description, event_type in movable_feasts:
            event, created = OrthodoxEvent.objects.get_or_create(
                title=title,
                is_movable=True,
                easter_offset=offset,
                defaults={
                    'description': description,
                    'event_type': event_type,
                    'month': 1,  # Placeholder
                    'day': 1,    # Placeholder
                    'is_old_style': False,
                }
            )
            if created:
                self.stdout.write(f'  ✓ Создан переходящий праздник: {event.title}')

        # Важные святые (примеры)
        saints = [
            (1, 1, 'Святителя Василия Великого', 'minor_feast'),
            (1, 12, 'Святительи Макария, митрополита Московского', 'minor_feast'),
            (5, 6, 'Великомученика Георгия Победоносца', 'minor_feast'),
            (5, 9, 'Святителя Николая Чудотворца', 'minor_feast'),
            (7, 12, 'Святых первоверховных апостолов Петра и Павла', 'major_feast'),
            (10, 14, 'Покров Пресвятой Богородицы', 'major_feast'),
            (12, 19, 'Святителя Николая Чудотворца', 'major_feast'),
        ]
        
        for month, day, title, event_type in saints:
            event, created = OrthodoxEvent.objects.get_or_create(
                month=month,
                day=day,
                title=title,
                defaults={
                    'description': f'Память {title.lower()}',
                    'event_type': event_type,
                    'is_movable': False,
                    'is_old_style': False,
                }
            )
            if created:
                self.stdout.write(f'  ✓ Создан день святого: {event.title}')

    def test_eternal_calendar(self):
        """Протестировать вечный календарь на нескольких датах"""
        
        self.stdout.write(self.style.WARNING('\nТестирование вечного календаря:'))
        
        test_dates = [
            date(2025, 1, 7),   # Рождество
            date(2025, 3, 5),   # Среда в Великий пост
            date(2025, 4, 20),  # Пасха 2025
            date(2025, 8, 15),  # Успенский пост
            date(2025, 11, 28), # Рождественский пост
            date(2026, 4, 12),  # Пасха 2026
        ]
        
        for test_date in test_dates:
            info = DailyOrthodoxInfo.get_info_for_date(test_date)
            events = OrthodoxEvent.get_events_for_date(test_date)
            
            self.stdout.write(
                f'  📅 {test_date.strftime("%d.%m.%Y")}: '
                f'{info.get_fasting_type_display()} '
                f'({len(events)} событий)'
            )
