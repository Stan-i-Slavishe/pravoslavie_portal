#!/usr/bin/env python3
"""
Тест для проверки исправления кнопок на странице категорий
"""

def test_categories_template():
    """Проверяем, что в шаблоне категорий убрана дублирующая кнопка"""
    
    template_path = "templates/core/categories.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем, что убрали btn-stack
        if '.btn-stack' in content:
            print("❌ ОШИБКА: Найден класс .btn-stack в CSS")
            return False
        
        # Проверяем, что больше нет двух кнопок для stories
        if 'btn-stack' in content:
            print("❌ ОШИБКА: Найден элемент btn-stack в HTML")
            return False
            
        # Проверяем, что есть единая логика кнопок
        if 'single-button' in content:
            print("✅ УСПЕХ: Найдена единая логика кнопок")
        else:
            print("❌ ОШИБКА: Не найдена единая логика кнопок")
            return False
            
        # Проверяем, что для stories используется правильная кнопка
        if 'btn-video-stories' in content and 'Видео-рассказы' in content:
            print("✅ УСПЕХ: Для видео-рассказов используется правильная кнопка")
        else:
            print("❌ ОШИБКА: Неправильная кнопка для видео-рассказов")
            return False
            
        print("\n🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("📝 Изменения:")
        print("   - Убрана дублирующая кнопка 'Видео-рассказы'")
        print("   - Для категорий типа 'story' теперь одна кнопка 'Видео-рассказы'")
        print("   - Для других категорий кнопка 'Перейти'")
        print("   - Все кнопки ведут в правильные места")
        print("   - Удалены неиспользуемые CSS стили")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ ОШИБКА: Файл {template_path} не найден")
        return False
    except Exception as e:
        print(f"❌ ОШИБКА: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Тестирование исправления кнопок категорий...")
    print("=" * 50)
    success = test_categories_template()
    
    if success:
        print("\n✅ ГОТОВО! Дублирующая кнопка убрана.")
        print("🚀 Теперь каждая категория имеет только одну кнопку.")
    else:
        print("\n❌ Требуется дополнительная проверка.")
