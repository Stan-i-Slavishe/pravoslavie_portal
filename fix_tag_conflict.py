import os
import sys
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('E:/pravoslavie_portal')

django.setup()

print("🔧 Объединение моделей Tag...")

try:
    # Проверяем, какие модели Tag существуют
    from core.models import Tag as CoreTag
    from books.models import Tag as BooksTag
    
    print("❌ Обнаружен конфликт: две модели Tag!")
    print("   - core.models.Tag")
    print("   - books.models.Tag")
    
    # Выводим количество записей в каждой
    core_tags_count = CoreTag.objects.count()
    books_tags_count = BooksTag.objects.count()
    
    print(f"📊 Теги в core: {core_tags_count}")
    print(f"📊 Теги в books: {books_tags_count}")
    
    print("\n🛠️ Нужно:")
    print("1. Перенести данные из books.Tag в core.Tag")
    print("2. Обновить связи в books.Book")
    print("3. Удалить books.Tag модель")
    print("4. Создать миграцию")
    
    # Переносим теги из books в core (если есть)
    if books_tags_count > 0:
        print(f"\n📋 Переносим {books_tags_count} тегов из books в core...")
        
        for books_tag in BooksTag.objects.all():
            core_tag, created = CoreTag.objects.get_or_create(
                name=books_tag.name,
                defaults={
                    'slug': books_tag.slug,
                    'color': '#74b9ff',  # Цвет по умолчанию
                    'is_active': True
                }
            )
            if created:
                print(f"  ✅ Создан тег: {core_tag.name}")
            else:
                print(f"  ℹ️  Тег уже существует: {core_tag.name}")
    
    print("\n✅ Данные подготовлены для миграции!")
    print("\n🚀 Следующие шаги:")
    print("1. python manage.py makemigrations books")
    print("2. python manage.py migrate")
    
except ImportError as e:
    print(f"✅ Конфликта моделей нет: {e}")
    print("Все приложения используют единую модель core.Tag")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
