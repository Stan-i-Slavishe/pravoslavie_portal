#!/usr/bin/env python
"""
Итоговая проверка всех исправлений Schema.org
"""
import os
import sys
import django

# Настройка Django
sys.path.append(r'E:\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

print("🔍 ПРОВЕРКА ИСПРАВЛЕНИЙ SCHEMA.ORG")
print("=" * 50)

def test_schema_imports():
    """Тест импортов Schema.org"""
    try:
        from core.seo.schema_org import get_schema_data, SchemaGenerator
        print("✅ Schema.org модули импортируются")
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта Schema.org: {e}")
        return False

def test_templatetags():
    """Тест templatetags"""
    try:
        from core.templatetags.seo_tags import schema_ld, social_image_url
        print("✅ SEO templatetags импортируются")
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта templatetags: {e}")
        return False

def test_book_model():
    """Тест модели Book"""
    try:
        from books.models import Book
        # Проверяем, что поле cover существует
        if hasattr(Book, 'cover'):
            print("✅ Модель Book имеет поле 'cover'")
            return True
        else:
            print("❌ У модели Book нет поля 'cover'")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки модели Book: {e}")
        return False

def test_schema_generation():
    """Тест генерации схемы для книги"""
    try:
        from core.seo.schema_org import SchemaGenerator
        from books.models import Book
        
        # Создаем тестовый объект без обращения к БД
        class MockBook:
            title = "Тестовая книга"
            description = "Описание тестовой книги"
            created_at = "2024-01-01T00:00:00Z"
            updated_at = "2024-01-01T00:00:00Z"
            slug = "test-book"
            price = 0
            cover = None
            
            def reviews(self):
                return None
                
        mock_book = MockBook()
        generator = SchemaGenerator()
        
        # Пытаемся сгенерировать схему
        schema = generator.get_book_schema(mock_book)
        
        if schema and '@type' in schema and schema['@type'] == 'Book':
            print("✅ Schema.org для книг генерируется корректно")
            return True
        else:
            print("❌ Проблема с генерацией схемы книг")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестирования генерации схемы: {e}")
        return False

# Запуск всех тестов
tests = [
    test_schema_imports,
    test_templatetags,
    test_book_model,
    test_schema_generation
]

passed = 0
for test in tests:
    if test():
        passed += 1

print("\n" + "=" * 50)
print(f"📊 РЕЗУЛЬТАТ: {passed}/{len(tests)} тестов пройдено")

if passed == len(tests):
    print("🎉 ВСЕ ИСПРАВЛЕНИЯ РАБОТАЮТ КОРРЕКТНО!")
    print("🚀 Сервер должен запускаться без ошибок в Schema.org")
else:
    print("⚠️  Есть проблемы, которые нужно исправить")

print("\n🔄 Для запуска сервера используйте: restart_fixed.bat")
