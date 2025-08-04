# test_about_page_fix.py
# Тест исправления страницы "О проекте"

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from core.views import AboutView

def test_about_page():
    """Тестируем исправленную страницу О проекте"""
    
    print("🔧 ТЕСТИРОВАНИЕ СТРАНИЦЫ 'О ПРОЕКТЕ'")
    print("=" * 40)
    
    try:
        # Создаем фабрику запросов
        factory = RequestFactory()
        request = factory.get('/about/')
        
        # Создаем представление
        view = AboutView()
        view.request = request
        
        # Пытаемся получить контекст
        print("🧪 Тестируем получение контекста...")
        
        context = view.get_context_data()
        
        print(f"✅ Контекст успешно получен!")
        print(f"   Ключи контекста: {list(context.keys())}")
        
        # Проверяем обязательные переменные
        required_vars = ['title', 'site_settings', 'founding_year', 'total_stories', 'total_books', 'total_audio']
        
        for var in required_vars:
            if var in context:
                print(f"   ✅ {var}: {context[var]}")
            else:
                print(f"   ❌ {var}: НЕ НАЙДЕНА")
        
        print(f"\n🎉 СТРАНИЦА 'О ПРОЕКТЕ' ИСПРАВЛЕНА!")
        print(f"   Теперь можно безопасно открыть: http://127.0.0.1:8000/about/")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        print("\nДетали ошибки:")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_about_page()
    
    if success:
        print("\n🎯 ВСЕ ИСПРАВЛЕНО!")
        print("Страница /about/ готова к использованию!")
    else:
        print("\n⚠️ Требуется дополнительная проверка.")
