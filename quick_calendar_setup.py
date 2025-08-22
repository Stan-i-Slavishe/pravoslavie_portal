# Быстрое создание базовых данных календаря

from pwa.models import FastingPeriod, OrthodoxEvent, DailyOrthodoxInfo

def create_basic_data():
    print("Создание базовых данных календаря...")
    
    # Создаем простой еженедельный пост
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
    
    if created:
        print("✓ Создан еженедельный пост")
    
    # Создаем основные праздники
    holidays = [
        (1, 7, 'Рождество Христово'),
        (1, 19, 'Крещение Господне'),
        (3, 25, 'Благовещение'),
        (8, 19, 'Преображение'),
        (8, 28, 'Успение Богородицы'),
    ]
    
    for month, day, title in holidays:
        event, created = OrthodoxEvent.objects.get_or_create(
            month=month,
            day=day,
            title=title,
            defaults={
                'description': f'Великий праздник {title}',
                'event_type': 'great_feast',
                'is_movable': False,
            }
        )
        if created:
            print(f"✓ Создан праздник: {title}")
    
    print("Базовые данные созданы!")

if __name__ == "__main__":
    create_basic_data()
