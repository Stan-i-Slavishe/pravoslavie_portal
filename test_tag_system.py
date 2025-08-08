#!/usr/bin/env python3
"""
Тест для проверки исправленной системы тегов
"""

import os
import sys

def test_tag_detail_view():
    """Проверяет, что TagDetailView исправлен"""
    
    views_path = r'E:\pravoslavie_portal\core\views.py'
    
    try:
        with open(views_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем ключевые элементы исправления
        checks = [
            ('Импорт Count и Q', 'from django.db.models import Count, Q'),
            ('Импорт Story', 'from stories.models import Story'),
            ('Импорт Book', 'from books.models import Book'),
            ('Импорт FairyTale', 'from fairy_tales.models import FairyTale'),
            ('Поиск Stories', 'Story.objects.filter'),
            ('Поиск Books', 'books = Book.objects.filter'),
            ('Контент айтемы', 'content_items = []'),
            ('Статистика', "context['stats'] = {"),
            ('Общее количество', "context['total_items']")
        ]
        
        results = []
        for name, check in checks:
            if check in content:
                results.append(f"✅ {name}")
            else:
                results.append(f"❌ {name}")
        
        # Проверяем шаблон
        template_path = r'E:\pravoslavie_portal\templates\core\tag_detail.html'
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            template_checks = [
                ('Статистические карточки', 'stats.stories'),
                ('Карточки контента', 'content_items'),
                ('Быстрые ссылки', 'Быстрые ссылки'),
                ('Бейджи типов', 'item.type'),
                ('Bootstrap карточки', 'card h-100')
            ]
            
            for name, check in template_checks:
                if check in template_content:
                    results.append(f"✅ Шаблон: {name}")
                else:
                    results.append(f"❌ Шаблон: {name}")
                    
        except FileNotFoundError:
            results.append("❌ Шаблон tag_detail.html не найден")
        
        # Выводим результаты
        print("🧪 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ СИСТЕМЫ ТЕГОВ")
        print("=" * 50)
        
        passed = sum(1 for r in results if r.startswith('✅'))
        total = len(results)
        
        for result in results:
            print(result)
        
        print("=" * 50)
        print(f"📊 Результат: {passed}/{total} тестов пройдено")
        
        if passed == total:
            print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Система тегов исправлена корректно.")
            print()
            print("🚀 Следующие шаги:")
            print("   1. Перезапустите Django-сервер: python manage.py runserver")
            print("   2. Откройте: http://127.0.0.1:8000/tag/doch/")
            print("   3. Проверьте отображение контента")
            return True
        else:
            print("⚠️ Некоторые тесты не пройдены. Проверьте исправления.")
            return False
            
    except FileNotFoundError:
        print("❌ Файл core/views.py не найден!")
        return False
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False

if __name__ == "__main__":
    test_tag_detail_view()
