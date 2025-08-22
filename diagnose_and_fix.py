#!/usr/bin/env python
"""
Диагностика: проверяем что в базе данных
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from pwa.models import DailyOrthodoxInfo, OrthodoxEvent

def check_database():
    """Проверяем содержимое базы данных"""
    print("🔍 Проверяем содержимое базы данных...")
    
    print("\n📅 DailyOrthodoxInfo:")
    total = DailyOrthodoxInfo.objects.count()
    print(f"   Всего записей: {total}")
    
    if total > 0:
        print("   Последние 10 записей:")
        for info in DailyOrthodoxInfo.objects.all()[:10]:
            print(f"   {info.day:02d}.{info.month:02d} - {info.get_fasting_type_display()} - {info.fasting_description}")
    
    print("\n⛪ OrthodoxEvent:")
    total_events = OrthodoxEvent.objects.count()
    print(f"   Всего событий: {total_events}")
    
    if total_events > 0:
        print("   События:")
        for event in OrthodoxEvent.objects.all():
            print(f"   {event.day:02d}.{event.month:02d} - {event.title}")
    
    print("\n🎯 Проверяем конкретно 21 августа:")
    try:
        info21 = DailyOrthodoxInfo.objects.get(month=8, day=21)
        print(f"   ✅ Найдена запись: {info21.get_fasting_type_display()}")
        print(f"   Описание: {info21.fasting_description}")
    except DailyOrthodoxInfo.DoesNotExist:
        print("   ❌ Записи для 21 августа НЕТ в базе данных!")
    
    return total > 0

def create_test_data():
    """Создаем тестовые данные для августа"""
    print("\n🔧 Создаем тестовые данные для августа...")
    
    august_data = {
        21: {
            'fasting_type': 'strict_fast',
            'description': 'Успенский пост: горячая пища без масла',
            'allowed_food': '''🍲 <strong>Успенский пост - горячее без масла:</strong>

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

💡 <strong>Рецепт:</strong> Овощное рагу без масла - тушите овощи в собственном соку''',
            'spiritual_note': 'Горячая пища без масла. Время умеренности и духовного сосредоточения.'
        },
        29: {
            'fasting_type': 'no_fast',
            'description': 'Ореховый Спас (Нерукотворный Образ)',
            'allowed_food': '''🌰 <strong>Ореховый Спас - поста нет!</strong>

Третий Спас - день перенесения Нерукотворного Образа Спасителя.

🍽️ <strong>Можно употреблять:</strong>
• Любую пищу (пост уже завершен)
• Орехи нового урожая
• Хлеб из нового зерна
• Праздничные блюда

🌰 <strong>Традиции:</strong>
• Освящение орехов и хлеба
• Покупка тканей и холстов
• Заготовка орехов на зиму''',
            'spiritual_note': '🌰 Ореховый Спас! День Нерукотворного Образа Спасителя. Время благодарения за урожай и подготовки к осени.'
        }
    }
    
    created_count = 0
    for day, data in august_data.items():
        info, created = DailyOrthodoxInfo.objects.get_or_create(
            month=8,
            day=day,
            defaults={
                'fasting_type': data['fasting_type'],
                'fasting_description': data['description'],
                'allowed_food': data['allowed_food'],
                'spiritual_note': data['spiritual_note']
            }
        )
        
        if not created:
            # Обновляем существующую запись
            info.fasting_type = data['fasting_type']
            info.fasting_description = data['description']
            info.allowed_food = data['allowed_food']
            info.spiritual_note = data['spiritual_note']
            info.save()
        
        action = "Создана" if created else "Обновлена"
        print(f"   ✅ {action} запись для {day} августа")
        created_count += 1
    
    return created_count

if __name__ == "__main__":
    print("🔍 ДИАГНОСТИКА базы данных православного календаря")
    print("=" * 60)
    
    # Проверяем текущее состояние
    has_data = check_database()
    
    if not has_data:
        print("\n❌ В базе данных НЕТ записей о постах!")
        print("🔧 Создаем минимальные данные...")
        created = create_test_data()
        print(f"\n✅ Создано {created} записей")
    else:
        print("\n🔧 Обновляем ключевые записи...")
        created = create_test_data()
        print(f"\n✅ Обработано {created} записей")
    
    # Проверяем результат
    print("\n" + "="*60)
    check_database()
    
    print("\n🎯 ГОТОВО! Теперь обновите страницу в браузере")
    print("📍 URL для проверки API: http://127.0.0.1:8000/pwa/api/daily-orthodox/2025/8/21/")
