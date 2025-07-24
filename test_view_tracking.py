# test_view_tracking.py
"""
Скрипт для тестирования системы отслеживания просмотров
"""

import os
import django
import sys

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser

from books.models import Book
from fairy_tales.models import FairyTaleTemplate
from stories.models import Story
from core.utils.views import track_view_session


def create_test_request():
    """Создает тестовый запрос с сессией"""
    factory = RequestFactory()
    request = factory.get('/')
    request.user = AnonymousUser()
    
    # Добавляем middleware для сессий
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()
    
    return request


def test_book_views():
    """Тестирует отслеживание просмотров книг"""
    print("🧪 Тестирование просмотров книг...")
    
    try:
        # Получаем первую книгу
        book = Book.objects.first()
        if not book:
            print("❌ Книги не найдены в БД")
            return
        
        print(f"📚 Тестируем книгу: {book.title}")
        initial_views = book.views_count
        
        # Создаем два запроса
        request1 = create_test_request()
        request2 = create_test_request()
        
        # Первый просмотр - должен засчитаться
        counted1 = track_view_session(request1, book)
        book.refresh_from_db()
        views_after_1 = book.views_count
        
        # Второй просмотр из той же сессии - не должен засчитаться
        counted2 = track_view_session(request1, book)
        book.refresh_from_db()
        views_after_2 = book.views_count
        
        # Третий просмотр из новой сессии - должен засчитаться
        counted3 = track_view_session(request2, book)
        book.refresh_from_db()
        views_after_3 = book.views_count
        
        print(f"📊 Результаты:")
        print(f"   Начальные просмотры: {initial_views}")
        print(f"   После 1-го просмотра: {views_after_1} (засчитан: {counted1})")
        print(f"   После 2-го просмотра (та же сессия): {views_after_2} (засчитан: {counted2})")
        print(f"   После 3-го просмотра (новая сессия): {views_after_3} (засчитан: {counted3})")
        
        # Проверяем ожидаемые результаты
        expected_after_1 = initial_views + 1
        expected_after_2 = initial_views + 1  # Не должно увеличиться
        expected_after_3 = initial_views + 2
        
        if (views_after_1 == expected_after_1 and 
            views_after_2 == expected_after_2 and 
            views_after_3 == expected_after_3 and
            counted1 and not counted2 and counted3):
            print("✅ Тест прошел успешно!")
        else:
            print("❌ Тест провален!")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")


if __name__ == "__main__":
    print("🚀 Запуск тестов системы отслеживания просмотров")
    print("=" * 50)
    
    test_book_views()
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")
