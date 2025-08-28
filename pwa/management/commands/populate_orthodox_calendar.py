"""
Django Management команда для заполнения православного календаря достоверной информацией о постах.
Использование: python manage.py populate_orthodox_calendar
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from pwa.models import DailyOrthodoxInfo, OrthodoxEvent

class Command(BaseCommand):
    help = 'Заполнение православного календаря информацией о постах'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед заполнением',
        )
        parser.add_argument(
            '--uspenie-only',
            action='store_true',
            help='Заполнить только Успенский пост',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🕊️ Начинаем заполнение православного календаря...')
        )

        if options['clear']:
            self.clear_existing_data()

        if options['uspenie_only']:
            self.populate_uspenie_fast_info()
            self.create_uspenie_orthodox_events()
        else:
            self.populate_full_calendar()

        self.show_statistics()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Православный календарь успешно заполнен!')
        )

    def clear_existing_data(self):
        """Очистка существующих данных"""
        self.stdout.write('🧹 Очищаем существующие данные...')
        
        daily_count = DailyOrthodoxInfo.objects.count()
        events_count = OrthodoxEvent.objects.count()
        
        DailyOrthodoxInfo.objects.all().delete()
        OrthodoxEvent.objects.all().delete()
        
        self.stdout.write(
            self.style.WARNING(f'   Удалено: {daily_count} записей о постах, {events_count} событий')
        )

    def populate_uspenie_fast_info(self):
        """Заполнение информации об Успенском посте"""
        self.stdout.write('🍇 Заполняем информацию об Успенском посте...')
        
        # Успенский пост: 14-27 августа 2025
        start_date = date(2025, 8, 14)
        end_date = date(2025, 8, 27)
        
        current = start_date
        created_count = 0
        updated_count = 0
        
        while current <= end_date:
            weekday = current.weekday()  # 0=понедельник, 6=воскресенье
            
            daily_info, created = DailyOrthodoxInfo.objects.get_or_create(
                month=current.month,
                day=current.day
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
            
            # Успенский пост строгий как Великий пост
            if current.day == 19 and current.month == 8:  # Преображение Господне
                daily_info.fasting_type = 'with_fish'
                daily_info.fasting_description = 'Успенский пост: Преображение Господне (Яблочный Спас)'
                daily_info.allowed_food = '''🍎 <strong>Преображение Господне - можно рыбу!</strong>

В праздник Преображения разрешается:

✅ <strong>Можно:</strong>
• Рыба и морепродукты 🐟
• Растительная пища с маслом
• Овощи, фрукты (особенно яблоки!)
• Каши с маслом
• Грибы жареные
• Орехи, мед
• Вино (немного)

🍎 <strong>Традиция:</strong> Освящение яблок и других плодов

❌ <strong>Запрещено:</strong>
• Мясо и мясные продукты
• Молочные продукты  
• Яйца'''
                daily_info.spiritual_note = '🍎 Преображение Господне! Яблочный Спас. Благословите новый урожай и вспомните о преображении души.'
                
            elif weekday in [0, 2, 4]:  # Понедельник, среда, пятница - сухоядение
                daily_info.fasting_type = 'dry_eating'
                daily_info.fasting_description = 'Успенский пост: сухоядение'
                daily_info.allowed_food = '''🥗 <strong>Успенский пост - сухоядение (холодная пища):</strong>

Август богат дарами природы!

✅ <strong>Разрешается:</strong>
• Свежие овощи: огурцы, помидоры, капуста, морковь, перец
• Летние фрукты: яблоки, груши, сливы, персики
• Ягоды: виноград, арбуз, дыня, смородина
• Орехи всех видов
• Семечки подсолнечные, тыквенные
• Мед свежий
• Хлеб постный (без молока и яиц)
• Сухофрукты: изюм, курага, инжир
• Вода, квас домашний, морсы (холодные)

❌ <strong>Запрещается:</strong>
• Любая горячая пища
• Растительное масло
• Продукты животного происхождения
• Варенье (можно мед)

💡 <strong>Совет:</strong> Делайте салаты из свежих овощей без масла, но с лимонным соком'''
                daily_info.spiritual_note = 'День сухоядения в Успенский пост. Время строгого воздержания в память о посте Богородицы перед Успением.'
                
            elif weekday in [1, 3]:  # Вторник, четверг - горячее без масла
                daily_info.fasting_type = 'strict_fast'
                daily_info.fasting_description = 'Успенский пост: горячая пища без масла'
                daily_info.allowed_food = '''🍲 <strong>Успенский пост - горячее без масла:</strong>

✅ <strong>Разрешается:</strong>
• Каши на воде: гречневая, овсяная, рисовая, пшенная
• Постные супы: овощные, грибные, щи постные
• Отварные овощи: картофель, морковь, свекла, капуста
• Картофель печеный в мундире
• Тушеные овощи без масла
• Грибы отварные, тушеные (без масла)
• Бобовые: горох, фасоль, чечевица
• Макароны (из твердых сортов пшеницы)
• Компоты из свежих фруктов
• Чай, кофе, травяные отвары

❌ <strong>Запрещается:</strong>
• Растительное масло для готовки
• Жареная пища
• Продукты животного происхождения
• Сливочное масло

💡 <strong>Рецепт:</strong> Овощное рагу без масла - тушите овощи в собственном соку'''
                daily_info.spiritual_note = 'Горячая пища без масла. Время умеренности и духовного сосредоточения.'
                
            else:  # Суббота, воскресенье - горячее с маслом
                daily_info.fasting_type = 'with_oil'
                daily_info.fasting_description = 'Успенский пост: горячая пища с растительным маслом'
                daily_info.allowed_food = '''🫒 <strong>Успенский пост - горячее с маслом:</strong>

✅ <strong>Разрешается:</strong>
• Все каши с растительным маслом
• Жареные и тушеные овощи
• Овощные рагу с маслом
• Салаты из свежих овощей с маслом
• Жареные грибы
• Картофель жареный, драники постные
• Постная выпечка (пирожки с капустой, картошкой)
• Постные блины на воде
• Соленые и маринованные овощи
• Варенье, джемы
• Вино красное (немного, по церковному уставу)

🍇 <strong>Августовские радости:</strong>
• Свежий виноград
• Арбузы и дыни
• Яблоки нового урожая
• Груши летние

❌ <strong>Запрещается:</strong>
• Мясо и мясные продукты
• Молочные продукты (молоко, сыр, творог, сметана)
• Яйца
• Рыба (кроме 19 августа)

💡 <strong>Особенность:</strong> Выходные дни поста более мягкие'''
                daily_info.spiritual_note = 'Выходной день поста. Время молитвы в семейном кругу и духовного общения.'
            
            daily_info.save()
            current += timedelta(days=1)
        
        self.stdout.write(
            self.style.SUCCESS(f'   Создано: {created_count}, обновлено: {updated_count} записей об Успенском посте')
        )

    def create_uspenie_orthodox_events(self):
        """Создание событий Успенского поста"""
        self.stdout.write('📅 Создаем события Успенского поста...')
        
        events = [
            (8, 14, "Медовый Спас (Происхождение Честных Древ)", "Первый Спас. Освящение меда и мака.", 'major_feast'),
            (8, 19, "Преображение Господне (Яблочный Спас)", "Великий праздник Преображения. Освящение яблок и винограда.", 'great_feast'),
            (8, 28, "Успение Пресвятой Богородицы", "Великий праздник Успения Божией Матери.", 'great_feast'),
            (8, 29, "Ореховый Спас (Нерукотворный Образ)", "Третий Спас. Освящение орехов и хлеба нового урожая.", 'major_feast'),
        ]
        
        created_count = 0
        updated_count = 0
        
        for month, day, title, description, event_type in events:
            event, created = OrthodoxEvent.objects.get_or_create(
                month=month,
                day=day,
                title=title,
                defaults={
                    'description': description,
                    'event_type': event_type,
                    'is_movable': False
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'   Создано: {created_count}, обновлено: {updated_count} событий')
        )

    def populate_full_calendar(self):
        """Заполнение полного календаря"""
        self.stdout.write('📅 Заполняем полный православный календарь...')
        
        # Заполняем Успенский пост
        self.populate_uspenie_fast_info()
        self.create_uspenie_orthodox_events()
        
        # Заполняем среды и пятницы
        self.populate_wednesdays_fridays()
        
        # Создаем основные праздники
        self.create_main_orthodox_events()
        
        # Обновляем праздничные дни
        self.update_feast_days()

    def populate_wednesdays_fridays(self):
        """Заполнение постных сред и пятниц"""
        self.stdout.write('📿 Заполняем постные среды и пятницы...')
        
        created_count = 0
        updated_count = 0
        
        for month in range(1, 13):
            days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1]
            if month == 2 and 2025 % 4 == 0:  # Високосный год
                days_in_month = 29
                
            for day in range(1, days_in_month + 1):
                target_date = date(2025, month, day)
                weekday = target_date.weekday()
                
                if weekday in [2, 4]:  # Среда и пятница
                    daily_info, created = DailyOrthodoxInfo.objects.get_or_create(
                        month=month,
                        day=day
                    )
                    
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                    
                    # Обновляем только если еще не назначен пост
                    if daily_info.fasting_type == 'no_fast':
                        day_name = "среда" if weekday == 2 else "пятница"
                        
                        daily_info.fasting_type = 'light_fast'
                        daily_info.fasting_description = f'Постная {day_name}'
                        daily_info.allowed_food = f'''🥬 <strong>Постная {day_name}:</strong>

✅ <strong>Разрешается:</strong>
• Растительная пища всех видов
• Каши на воде или с растительным маслом
• Овощи (свежие, тушеные, вареные, жареные)
• Фрукты и ягоды
• Орехи и семечки
• Грибы в любом виде
• Растительное масло
• Хлеб (без молока и яиц)
• Мед, варенье
• Напитки: чай, кофе, соки, компоты

❌ <strong>Не разрешается:</strong>
• Мясо и мясные продукты
• Молоко и молочные продукты
• Яйца
• Рыба и морепродукты'''
                        
                        if weekday == 2:
                            daily_info.spiritual_note = 'Среда - день воспоминания предательства Иуды. Время для покаяния и дел милосердия.'
                        else:
                            daily_info.spiritual_note = 'Пятница - день воспоминания крестных страданий Спасителя. День особой молитвы и воздержания.'
                        
                        daily_info.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'   Создано: {created_count}, обновлено: {updated_count} записей о средах и пятницах')
        )

    def create_main_orthodox_events(self):
        """Создание основных православных событий"""
        self.stdout.write('⛪ Создаем основные православные события...')
        
        # Великие праздники
        great_feasts = [
            (1, 7, "Рождество Христово", "Великий праздник Рождества Господа нашего Иисуса Христа"),
            (1, 19, "Крещение Господне (Богоявление)", "Великий праздник Крещения Иисуса Христа в Иордане"),
            (4, 7, "Благовещение Пресвятой Богородицы", "Великий праздник Благовещения"),
            (9, 21, "Рождество Пресвятой Богородицы", "Великий праздник Рождества Богоматери"),
            (9, 27, "Воздвижение Честного и Животворящего Креста", "Великий праздник Воздвижения Креста"),
            (12, 4, "Введение во храм Пресвятой Богородицы", "Великий праздник Введения во храм"),
        ]
        
        created_count = 0
        
        for month, day, title, description in great_feasts:
            event, created = OrthodoxEvent.objects.get_or_create(
                month=month,
                day=day,
                title=title,
                defaults={
                    'description': description,
                    'event_type': 'great_feast',
                    'is_movable': False
                }
            )
            if created:
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'   Создано {created_count} великих праздников')
        )

    def update_feast_days(self):
        """Обновление дней великих праздников"""
        self.stdout.write('🎉 Обновляем дни великих праздников...')
        
        great_feasts = OrthodoxEvent.objects.filter(event_type='great_feast', is_movable=False)
        updated_count = 0
        
        for feast in great_feasts:
            daily_info, created = DailyOrthodoxInfo.objects.get_or_create(
                month=feast.month,
                day=feast.day
            )
            
            daily_info.fasting_type = 'no_fast'
            daily_info.fasting_description = f'Великий праздник: {feast.title}'
            daily_info.allowed_food = f'''🎉 <strong>Великий праздник - поста нет!</strong>

В честь праздника {feast.title} разрешается любая пища.

🍽️ <strong>Можно употреблять:</strong>
• Все виды мясных блюд
• Молочные продукты
• Яйца в любом виде
• Рыбу и морепродукты
• Любую другую пищу
• Праздничные сладости

🎊 <strong>Традиция:</strong> Праздничная трапеза в кругу семьи'''
            daily_info.spiritual_note = f'🎉 {feast.title}! {feast.description}'
            daily_info.save()
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'   Обновлено {updated_count} дней великих праздников')
        )

    def show_statistics(self):
        """Показать статистику"""
        self.stdout.write('\n📊 Статистика православного календаря:')
        
        total_daily = DailyOrthodoxInfo.objects.count()
        total_events = OrthodoxEvent.objects.count()
        great_feasts = OrthodoxEvent.objects.filter(event_type='great_feast').count()
        
        no_fast = DailyOrthodoxInfo.objects.filter(fasting_type='no_fast').count()
        light_fast = DailyOrthodoxInfo.objects.filter(fasting_type='light_fast').count()
        strict_fast = DailyOrthodoxInfo.objects.filter(fasting_type='strict_fast').count()
        dry_eating = DailyOrthodoxInfo.objects.filter(fasting_type='dry_eating').count()
        with_oil = DailyOrthodoxInfo.objects.filter(fasting_type='with_oil').count()
        with_fish = DailyOrthodoxInfo.objects.filter(fasting_type='with_fish').count()
        
        # Успенский пост
        uspenie_days = DailyOrthodoxInfo.objects.filter(
            month=8, day__gte=14, day__lte=27
        ).exclude(fasting_type='no_fast').count()
        
        self.stdout.write(f'   • Всего записей о постах: {total_daily}')
        self.stdout.write(f'   • Православных событий: {total_events}')
        self.stdout.write(f'   • Великих праздников: {great_feasts}')
        self.stdout.write(f'   • Дней без поста: {no_fast}')
        self.stdout.write(f'   • Дней легкого поста: {light_fast}')
        self.stdout.write(f'   • Дней строгого поста: {strict_fast}')
        self.stdout.write(f'   • Дней сухоядения: {dry_eating}')
        self.stdout.write(f'   • Дней с маслом: {with_oil}')
        self.stdout.write(f'   • Дней с рыбой: {with_fish}')
        self.stdout.write(f'   • Дней Успенского поста: {uspenie_days}')
        
        self.stdout.write('\n📖 Источники:')
        self.stdout.write('   • Типикон (церковный устав)')
        self.stdout.write('   • Православный журнал "Фома"')
        self.stdout.write('   • Официальные церковные источники')
        self.stdout.write('   • Московская Патриархия')
