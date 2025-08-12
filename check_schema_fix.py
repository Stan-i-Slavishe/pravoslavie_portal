#!/usr/bin/env python
"""
QUICK SCHEMA.ORG CHECK
"""
import os
import sys
import django

# Настройка Django
sys.path.append(r'E:\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    from core.seo.schema_org import SchemaGenerator
    
    generator = SchemaGenerator()
    
    # Создаем тестовый объект Book
    class MockBook:
        title = 'Test Book'
        description = 'Test Description'
        created_at = '2024-01-01T00:00:00Z'
        updated_at = '2024-01-01T00:00:00Z'
        slug = 'test-book'
        price = 0
        cover = None
        author = 'Test Author'
        
        class reviews:
            @staticmethod
            def exists():
                return False
    
    # Тестируем генерацию схемы
    mock_book = MockBook()
    result = generator.get_book_schema(mock_book)
    
    if result and result.get('@type') == 'Book':
        print('✅ Schema.org для книг исправлено!')
    else:
        print('❌ Проблема с генерацией схемы книги')
        
except Exception as e:
    print(f'❌ Проблема: {e}')
