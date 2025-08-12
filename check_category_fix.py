import os
import django
import sys

# Добавляем путь к проекту
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_and_fix_category():
    """Проверяем и исправляем категорию"""
    
    print("=" * 50)
    print("ИСПРАВЛЕНИЕ КАТЕГОРИЙ ВИДЕО-РАССКАЗОВ")
    print("=" * 50)
    print()
    
    print("Проблема: Категория 'Врачебные истории' показывает 'Контент в разработке'")
    print("Решение: Обновляем CategoryDetailView для умного перенаправления")
    print()
    
    print("1. Проверяем существование категории...")
    
    try:
        from core.models import Category
        
        try:
            category = Category.objects.get(slug='vrachebnye-istorii')
            print(f'✓ Найдена категория: {category.name}')
            print(f'  - Тип: {category.content_type}')
            print(f'  - Slug: {category.slug}')
            print(f'  - Активна: {category.is_active}')
        except Category.DoesNotExist:
            print('❌ Категория не найдена! Создаем...')
            category = Category.objects.create(
                name='Врачебные истории',
                slug='vrachebnye-istorii', 
                content_type='story',
                description='Рассказы о врачах и пациентах, о боли и надежде, о человеческом участии и Божьем промысле.',
                is_active=True
            )
            print(f'✓ Создана категория: {category.name}')
            
    except Exception as e:
        print(f'❌ Ошибка при работе с категорией: {e}')
        return False
    
    print()
    print("2. Проверяем связанные рассказы...")
    
    try:
        from stories.models import Story
        
        stories = Story.objects.filter(category=category, is_published=True)
        print(f'✓ Найдено рассказов в категории: {stories.count()}')
        
        if stories.exists():
            print("   Примеры рассказов:")
            for story in stories[:3]:
                print(f'   - {story.title}')
                
            print()
            print('🎯 РЕШЕНИЕ:')
            print('   Теперь при переходе на /category/vrachebnye-istorii/')
            print('   произойдет автоматическое перенаправление на:')
            print(f'   /stories/?category={category.slug}')
        else:
            print('⚠️ В категории нет рассказов')
            print('   Будет показана страница с предложением перейти к рассказам')
            
    except Exception as e:
        print(f'❌ Ошибка при проверке рассказов: {e}')
        return False
    
    print()
    print("3. Проверяем все story-категории...")
    
    try:
        story_categories = Category.objects.filter(content_type='story', is_active=True)
        print(f'✓ Найдено story-категорий: {story_categories.count()}')
        
        for cat in story_categories:
            story_count = Story.objects.filter(category=cat, is_published=True).count()
            print(f'   - {cat.name} ({cat.slug}): {story_count} рассказов')
            
    except Exception as e:
        print(f'⚠️ Ошибка при проверке категорий: {e}')
    
    print()
    print("=" * 50)
    print("✅ ДИАГНОСТИКА ЗАВЕРШЕНА!")
    print("=" * 50)
    print()
    print("Что изменилось в CategoryDetailView:")
    print("• Автоматическое перенаправление для story-категорий с контентом")
    print("• Красивая страница-заглушка для пустых категорий")
    print("• Таймер автоматического перенаправления (5 сек)")
    print("• Улучшенный UI/UX с анимациями")
    print()
    print("Следующие шаги:")
    print("1. Запустите сервер: python manage.py runserver")
    print("2. Перейдите на: http://127.0.0.1:8000/category/vrachebnye-istorii/")
    print("3. Проверьте работу автоматического перенаправления")
    print()
    
    return True

if __name__ == "__main__":
    try:
        check_and_fix_category()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        print("Убедитесь, что вы запускаете скрипт из корневой папки проекта")
    
    input("Нажмите Enter для продолжения...")
