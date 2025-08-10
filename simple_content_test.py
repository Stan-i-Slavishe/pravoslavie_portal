#!/usr/bin/env python
"""
Простая диагностика поля content
"""
import os
import sys
import django

# Добавляем проект в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from books.models import Book

def simple_content_test():
    """Простой тест поля content"""
    
    print("🔬 Простая диагностика поля content")
    print("=" * 50)
    
    try:
        # Получаем книгу "Великая книга"
        book = Book.objects.filter(title__icontains="Великая").first()
        
        if not book:
            print("❌ Книга 'Великая книга' не найдена")
            return
            
        print(f"📚 Книга найдена: {book.title}")
        print(f"   ID: {book.id}")
        print(f"   Slug: {book.slug}")
        
        # Проверяем атрибут content
        try:
            content_value = book.content
            print(f"\n📄 Поле content:")
            print(f"   Тип: {type(content_value)}")
            print(f"   Длина: {len(content_value) if content_value else 0}")
            print(f"   Пустое: {'Да' if not content_value else 'Нет'}")
            
            if content_value:
                print(f"   Первые 100 символов: {content_value[:100]}...")
            else:
                print(f"   ❌ ПОЛЕ ПУСТОЕ!")
                
        except AttributeError as e:
            print(f"❌ Ошибка доступа к полю content: {e}")
            print("🎯 Поле content НЕ СУЩЕСТВУЕТ в модели!")
            
        # Проверяем description для сравнения
        try:
            desc_value = book.description
            print(f"\n📝 Поле description (для сравнения):")
            print(f"   Длина: {len(desc_value) if desc_value else 0}")
            print(f"   Первые 50 символов: {desc_value[:50] if desc_value else 'ПУСТОЕ'}...")
            
        except AttributeError as e:
            print(f"❌ Ошибка доступа к полю description: {e}")
            
        # Проверяем все поля модели
        print(f"\n🔍 Все поля модели Book:")
        for field in Book._meta.fields:
            print(f"   - {field.name} ({field.__class__.__name__})")
            
        # Прямой SQL запрос для проверки
        print(f"\n💾 Прямая проверка базы данных:")
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT content FROM books_book WHERE id = %s", [book.id])
            row = cursor.fetchone()
            
            if row:
                db_content = row[0]
                print(f"   Content из БД: {len(db_content) if db_content else 0} символов")
                if db_content:
                    print(f"   Первые 100 символов: {db_content[:100]}...")
                else:
                    print(f"   ❌ В БД поле ПУСТОЕ!")
            else:
                print(f"   ❌ Запись не найдена в БД")
                
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

def test_template_rendering():
    """Тестирует рендеринг шаблона"""
    
    print(f"\n🎨 Тест рендеринга шаблона")
    print("=" * 30)
    
    try:
        from django.template import Template, Context
        
        book = Book.objects.filter(title__icontains="Великая").first()
        
        # Тестовый шаблон
        template_code = '''
Title: {{ book.title }}
Description exists: {% if book.description %}YES{% else %}NO{% endif %}
Content exists: {% if book.content %}YES{% else %}NO{% endif %}
Content length: {{ book.content|length }}
        '''
        
        template = Template(template_code)
        context = Context({'book': book})
        result = template.render(context)
        
        print("Результат рендеринга:")
        print(result)
        
    except Exception as e:
        print(f"❌ Ошибка в рендеринге: {e}")

if __name__ == "__main__":
    simple_content_test()
    test_template_rendering()
