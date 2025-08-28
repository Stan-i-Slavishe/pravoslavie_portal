#!/usr/bin/env python
"""
БЫСТРОЕ ИСПРАВЛЕНИЕ: Заполнение 21 августа правильными данными
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from datetime import date
from pwa.models import DailyOrthodoxInfo, OrthodoxEvent

def fix_august_21():
    """Исправление данных для 21 августа"""
    print("🔧 Исправляем данные для 21 августа...")
    
    try:
        # Получаем или создаем запись для 21 августа
        daily_info, created = DailyOrthodoxInfo.objects.get_or_create(
            month=8,
            day=21
        )
        
        # 21 августа 2025 - четверг, Успенский пост: горячее без масла
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
        daily_info.save()
        
        action = "Создана" if created else "Обновлена"
        print(f"✅ {action} запись для 21 августа")
        print(f"   Тип поста: {daily_info.get_fasting_type_display()}")
        print(f"   Описание: {daily_info.fasting_description}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def check_current_data():
    """Проверим текущие данные"""
    print("\n📊 Проверяем текущие данные:")
    
    for day in [20, 21, 22]:
        try:
            info = DailyOrthodoxInfo.objects.get(month=8, day=day)
            print(f"   {day}.08: {info.get_fasting_type_display()} - {info.fasting_description}")
        except DailyOrthodoxInfo.DoesNotExist:
            print(f"   {day}.08: Данных нет")

if __name__ == "__main__":
    print("🚀 Быстрое исправление данных для 21 августа")
    print("=" * 50)
    
    # Проверяем текущее состояние
    check_current_data()
    
    # Исправляем данные
    if fix_august_21():
        print("\n✅ Данные успешно исправлены!")
        print("🔄 Обновите страницу в браузере")
    else:
        print("\n❌ Не удалось исправить данные")
    
    # Проверяем результат
    check_current_data()
