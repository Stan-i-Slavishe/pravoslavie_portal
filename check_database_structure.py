#!/usr/bin/env python
"""
Проверка структуры базы данных и поля content
"""
import os
import sys
import django

# Добавляем проект в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from books.models import Book

def check_database_structure():
    """Проверяет структуру таблицы books_book"""
    
    print("🔍 Проверка структуры базы данных")
    print("=" * 60)
    
    try:
        # Получаем информацию о таблице
        with connection.cursor() as cursor:
            # Для SQLite
            cursor.execute("PRAGMA table_info(books_book);")
            columns = cursor.fetchall()
            
            print("📊 Структура таблицы books_book:")
            print("-" * 40)
            
            has_content_field = False
            
            for column in columns:
                column_id, name, type_name, not_null, default, pk = column
                print(f"   {column_id}: {name} ({type_name})")
                
                if name == 'content':
                    has_content_field = True
                    print(f"      ✅ ПОЛЕ 'content' НАЙДЕНО!")
            
            print("-" * 40)
            
            if not has_content_field:
                print("❌ ПОЛЕ 'content' НЕ НАЙДЕНО В БАЗЕ ДАННЫХ!")
                print("🎯 Это объясняет проблему!")
                
                # Проверяем модель
                print(f"\n🔍 Проверка модели Book...")
                fields = [field.name for field in Book._meta.fields]
                print(f"   Поля в модели: {fields}")
                
                if 'content' in fields:
                    print("✅ Поле 'content' есть в модели")
                    print("❌ Но НЕТ в базе данных - нужна миграция!")
                else:
                    print("❌ Поле 'content' НЕТ в модели!")
                    
            else:
                print("✅ Поле 'content' существует в базе данных")
                
                # Проверяем данные
                print(f"\n📚 Проверка данных в поле 'content':")
                books_with_content = Book.objects.exclude(content__isnull=True).exclude(content='')
                print(f"   Книг с заполненным content: {books_with_content.count()}")
                
                for book in books_with_content:
                    print(f"   - {book.title}: {len(book.content)} символов")
                    
    except Exception as e:
        print(f"❌ Ошибка при проверке структуры БД: {e}")
        
        # Альтернативный способ через Django ORM
        try:
            print(f"\n🔄 Альтернативная проверка через Django ORM...")
            
            # Пытаемся получить поле content
            book = Book.objects.first()
            if book:
                content_value = getattr(book, 'content', 'ПОЛЕ НЕ НАЙДЕНО')
                print(f"   Значение content: {content_value}")
                
        except Exception as e2:
            print(f"❌ Ошибка в альтернативной проверке: {e2}")

def check_migrations():
    """Проверяет состояние миграций"""
    
    print(f"\n🔄 Проверка миграций...")
    print("=" * 30)
    
    try:
        from django.core.management import execute_from_command_line
        import io
        import sys
        from contextlib import redirect_stdout
        
        # Перенаправляем вывод
        f = io.StringIO()
        
        with redirect_stdout(f):
            try:
                execute_from_command_line(['manage.py', 'showmigrations', 'books'])
            except SystemExit:
                pass  # Игнорируем SystemExit
        
        migration_output = f.getvalue()
        print("📋 Состояние миграций books:")
        print(migration_output)
        
        if '[X]' in migration_output:
            print("✅ Есть примененные миграции")
        else:
            print("❌ Нет примененных миграций")
            
        if '[ ]' in migration_output:
            print("⚠️  Есть неприменённые миграции")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке миграций: {e}")

def create_migration_if_needed():
    """Создает миграцию если нужно"""
    
    print(f"\n🛠️  Создание миграции для поля content...")
    print("=" * 40)
    
    try:
        import subprocess
        
        # Создаем миграцию
        result = subprocess.run([
            'python', 'manage.py', 'makemigrations', 'books', 
            '--name', 'add_content_field'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Миграция создана успешно:")
            print(result.stdout)
        else:
            print("⚠️  Результат создания миграции:")
            print(result.stdout)
            if result.stderr:
                print("Ошибки:")
                print(result.stderr)
                
    except Exception as e:
        print(f"❌ Ошибка при создании миграции: {e}")

if __name__ == "__main__":
    try:
        check_database_structure()
        check_migrations()
        create_migration_if_needed()
        
        print(f"\n" + "=" * 60)
        print(f"📋 ИНСТРУКЦИЯ ПО ИСПРАВЛЕНИЮ:")
        print(f"1. 🔍 Если поле content НЕ найдено в базе:")
        print(f"   python manage.py makemigrations books")
        print(f"   python manage.py migrate")
        print(f"2. 🔄 Перезапустите Django сервер")
        print(f"3. 📝 Заполните поле content в админке заново")
        print(f"4. 🌐 Проверьте на сайте")
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        import traceback
        traceback.print_exc()
