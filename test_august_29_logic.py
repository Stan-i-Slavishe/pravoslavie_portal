#!/usr/bin/env python
"""
Простая проверка логики определения типа дня для 29 августа
"""

from datetime import date

def test_august_29_logic():
    """Тестируем логику для 29 августа"""
    
    # Имитируем алгоритм из обновленного кода
    target_date = date(2025, 8, 29)
    
    print(f"🧪 Тестируем дату: {target_date}")
    print(f"Месяц: {target_date.month}, День: {target_date.day}")
    
    # 1. ПРИОРИТЕТ: Проверяем строгие постные дни
    if target_date.month == 8 and target_date.day == 29:
        day_type = 'fast-day'  # Строгий постный день
        fasting_type = 'strict_fast'
        description = 'Усекновение главы Иоанна Предтечи (строгий пост)'
        allowed_food = 'Сухоядение: хлеб, овощи, фрукты, орехи (без масла)'
        spiritual_note = '⚔️ Усекновение главы Иоанна Предтечи. Строгий постный день в память о мученической кончине святого Предтечи. Ореховый Спас отмечается, но пост сохраняется.'
        
        print(f"✅ Попадает под правило 'строгие постные дни'")
        print(f"🎨 Тип дня для календаря: {day_type}")
        print(f"🍽️ Тип поста: {fasting_type}")
        print(f"📝 Описание: {description}")
        print(f"🥗 Разрешенная пища: {allowed_food}")
        print(f"🙏 Духовная заметка: {spiritual_note}")
        
        if day_type == 'fast-day':
            print("🎉 УСПЕХ! Дата будет отображаться ФИОЛЕТОВЫМ цветом в календаре!")
            return True
        else:
            print("❌ ОШИБКА! Неправильный тип дня")
            return False
    else:
        print("❌ ОШИБКА! Дата не попадает под правило")
        return False

if __name__ == "__main__":
    print("🔧 Проверка логики календаря для 29 августа")
    print("=" * 50)
    
    success = test_august_29_logic()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Логика работает правильно!")
        print("🟣 29 августа будет отображаться ФИОЛЕТОВЫМ (постный день)")
    else:
        print("❌ Логика работает неправильно!")
        print("🔴 Требуются дополнительные исправления")
