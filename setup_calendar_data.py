# Создание базовых данных для вечного календаря
# Запустите: python manage.py shell
# Затем скопируйте и вставьте этот код

from pwa.models import FastingPeriod, OrthodoxEvent, DailyOrthodoxInfo

print("🔄 Создание базовых данных вечного календаря...")

# 1. Создаем еженедельный пост (среда/пятница)
weekly_fast, created = FastingPeriod.objects.get_or_create(
    name='weekly_fast',
    defaults={
        'title': 'Еженедельный пост (среда/пятница)',
        'description': 'Постные дни среды и пятницы',
        'fasting_rules': {
            'monday': 'no_fast',
            'tuesday': 'no_fast', 
            'wednesday': 'light_fast',
            'thursday': 'no_fast',
            'friday': 'light_fast',
            'saturday': 'no_fast',
            'sunday': 'no_fast',
        },
        'priority': 1,
        'is_active': True
    }
)
print(f"✓ Еженедельный пост: {'создан' if created else 'уже существует'}")

# 2. Создаем Успенский пост (сейчас активен!)
assumption_fast, created = FastingPeriod.objects.get_or_create(
    name='assumption_fast',
    defaults={
        'title': 'Успенский пост',
        'description': 'Пост перед праздником Успения Пресвятой Богородицы (14-27 августа)',
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
print(f"✓ Успенский пост: {'создан' if created else 'уже существует'}")

# 3. Создаем основные праздники
holidays = [
    (1, 7, 'Рождество Христово', 'great_feast'),
    (1, 19, 'Крещение Господне', 'great_feast'),
    (3, 25, 'Благовещение Пресвятой Богородицы', 'great_feast'),
    (8, 19, 'Преображение Господне', 'great_feast'),
    (8, 28, 'Успение Пресвятой Богородицы', 'great_feast'),
    (9, 21, 'Рождество Пресвятой Богородицы', 'great_feast'),
    (12, 4, 'Введение во храм Пресвятой Богородицы', 'great_feast'),
]

for month, day, title, event_type in holidays:
    event, created = OrthodoxEvent.objects.get_or_create(
        month=month,
        day=day,
        title=title,
        defaults={
            'description': f'Великий православный праздник',
            'event_type': event_type,
            'is_movable': False,
        }
    )
    if created:
        print(f"✓ Создан праздник: {title}")

print("🎉 Базовые данные календаря созданы!")
print("")
print("📅 Что создано:")
print("   🟣 Еженедельный пост (среда/пятница)")
print("   🟣 Успенский пост (14-27 августа)")
print("   🔴 Основные великие праздники")
print("")
print("🔗 Теперь обновите страницу календаря!")
