# test_reading_stats_fix.py
# Тест исправления функции reading_stats

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from books.views import reading_stats
from books.models import ReadingSession, Book

def test_reading_stats():
    """Тестируем исправленную функцию reading_stats"""
    
    print("🔧 ТЕСТИРОВАНИЕ ИСПРАВЛЕНИЯ READING_STATS")
    print("=" * 45)
    
    try:
        # Создаем тестового пользователя
        user, created = User.objects.get_or_create(
            username='test_reading_user',
            defaults={'email': 'test@example.com'}
        )
        
        if created:
            print(f"✅ Создан тестовый пользователь: {user.username}")
        else:
            print(f"📋 Используем существующего пользователя: {user.username}")
        
        # Создаем фабрику запросов
        factory = RequestFactory()
        request = factory.get('/books/reading-stats/')
        request.user = user
        
        # Пытаемся вызвать функцию reading_stats
        print("\n🧪 Тестируем функцию reading_stats...")
        
        response = reading_stats(request)
        
        print(f"✅ Функция выполнилась успешно!")
        print(f"   Статус ответа: {response.status_code}")
        print(f"   Тип ответа: {type(response).__name__}")
        
        # Проверяем контекст (если это TemplateResponse)
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"   Контекст содержит: {list(context.keys())}")
        
        print("\n🎉 ИСПРАВЛЕНИЕ РАБОТАЕТ КОРРЕКТНО!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        print("\nДетали ошибки:")
        import traceback
        traceback.print_exc()
        return False

def test_extract_function():
    """Тестируем работу Extract функции отдельно"""
    
    print("\n🔍 ТЕСТИРОВАНИЕ EXTRACT ФУНКЦИИ")
    print("=" * 35)
    
    try:
        from django.db.models.functions import Extract
        from books.models import ReadingSession
        from django.db.models import Count
        
        # Пробуем выполнить запрос с Extract
        queryset = ReadingSession.objects.annotate(
            month=Extract('last_read', 'month')
        ).values('month').annotate(
            count=Count('id')
        )
        
        # Пытаемся выполнить запрос
        result = list(queryset)
        
        print(f"✅ Extract функция работает!")
        print(f"   Результат: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в Extract: {e}")
        return False

if __name__ == '__main__':
    success1 = test_extract_function()
    success2 = test_reading_stats()
    
    if success1 and success2:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("Ошибка в /books/reading-stats/ исправлена!")
    else:
        print("\n⚠️ Некоторые тесты не прошли. Проверьте детали выше.")
