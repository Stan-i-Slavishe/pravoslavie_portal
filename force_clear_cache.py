#!/usr/bin/env python
"""
Принудительная очистка кеша и проверка отображения содержания
"""
import os
import sys
import django

# Добавляем проект в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.cache import cache
from books.models import Book

def force_clear_cache_and_check():
    """Принудительно очищает кеш и проверяет данные"""
    
    print("🚀 Принудительная очистка кеша и проверка")
    print("=" * 60)
    
    # 1. Очищаем все кеши Django
    try:
        cache.clear()
        print("✅ Django кеш очищен")
    except Exception as e:
        print(f"⚠️  Ошибка при очистке кеша: {e}")
    
    # 2. Проверяем данные в базе
    try:
        book = Book.objects.filter(slug='velikaya-kniga').first()
        if not book:
            book = Book.objects.filter(title__icontains="Великая").first()
        
        if book:
            print(f"\n📚 Книга найдена: {book.title} (ID: {book.id})")
            print(f"   Slug: {book.slug}")
            print(f"   Описание есть: {'✅' if book.description else '❌'}")
            print(f"   Содержание есть: {'✅' if book.content else '❌'}")
            
            if book.content:
                print(f"\n📄 Содержание (первые 200 символов):")
                print(f"   {book.content[:200]}...")
                print(f"   Полная длина: {len(book.content)} символов")
            else:
                print(f"\n❌ СОДЕРЖАНИЕ ПУСТОЕ!")
                
        else:
            print("❌ Книга не найдена!")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке книги: {e}")
    
    # 3. Тестируем отображение в шаблоне
    print(f"\n🧪 Проверка шаблона...")
    
    try:
        from django.template import Template, Context
        
        # Простой тест шаблона
        template_code = '''
        {% if book.content %}
        СОДЕРЖАНИЕ НАЙДЕНО: {{ book.content|length }} символов
        {% else %}
        СОДЕРЖАНИЕ НЕ НАЙДЕНО
        {% endif %}
        '''
        
        template = Template(template_code)
        context = Context({'book': book})
        result = template.render(context)
        
        print(f"   Результат теста шаблона: {result.strip()}")
        
    except Exception as e:
        print(f"❌ Ошибка в тесте шаблона: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"📋 ИНСТРУКЦИЯ ПО ИСПРАВЛЕНИЮ:")
    print(f"1. ⏹️  ОСТАНОВИТЕ Django сервер (Ctrl+C)")
    print(f"2. 🔄 ЗАПУСТИТЕ сервер заново: python manage.py runserver")
    print(f"3. 🧹 ОЧИСТИТЕ кеш браузера (Ctrl+Shift+R или Ctrl+F5)")
    print(f"4. 🔍 ОТКРОЙТЕ страницу в режиме инкогнито")
    print(f"5. 📱 ПРОВЕРЬТЕ на другом браузере")
    
    if book and book.content:
        print(f"\n✅ Данные в базе ЕСТЬ! Проблема в кешировании.")
    else:
        print(f"\n❌ Данные в базе НЕТ! Проблема в админке.")

if __name__ == "__main__":
    try:
        force_clear_cache_and_check()
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        import traceback
        traceback.print_exc()
