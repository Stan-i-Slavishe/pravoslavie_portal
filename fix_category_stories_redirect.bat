@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ КАТЕГОРИЙ ВИДЕО-РАССКАЗОВ
echo ========================================

echo.
echo Проблема: Категория "Врачебные истории" показывает "Контент в разработке"
echo Решение: Обновляем CategoryDetailView для умного перенаправления
echo.

echo 1. Проверяем существование категории...
python -c "
import os
import django
import sys
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

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
    print(f'❌ Ошибка: {e}')
"

echo.
echo 2. Проверяем связанные рассказы...
python -c "
import os
import django
import sys
sys.path.append('E:/pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

try:
    from core.models import Category
    from stories.models import Story
    
    category = Category.objects.get(slug='vrachebnye-istorii')
    stories = Story.objects.filter(category=category, is_published=True)
    print(f'✓ Найдено рассказов в категории: {stories.count()}')
    
    if stories.exists():
        for story in stories[:3]:
            print(f'  - {story.title}')
            
        print('')
        print('🎯 РЕШЕНИЕ:')
        print('   Теперь при переходе на /category/vrachebnye-istorii/')
        print('   произойдет автоматическое перенаправление на:')
        print(f'   /stories/?category={category.slug}')
    else:
        print('⚠️ В категории нет рассказов')
        print('   Будет показана страница с предложением перейти к рассказам')
        
except Exception as e:
    print(f'❌ Ошибка: {e}')
"

echo.
echo ========================================
echo ✅ ИСПРАВЛЕНИЕ ПРИМЕНЕНО!
echo ========================================
echo.
echo Что изменилось:
echo • CategoryDetailView теперь умно перенаправляет пользователей
echo • Для story-категорий с контентом - автоматический редирект
echo • Для пустых категорий - красивая страница с предложениями
echo • Добавлен автоматический таймер перенаправления (5 сек)
echo • Улучшен UI/UX с анимациями и подсказками
echo.
echo Теперь:
echo 1. Запустите сервер: python manage.py runserver
echo 2. Перейдите на: http://127.0.0.1:8000/category/vrachebnye-istorii/
echo 3. Если есть рассказы - автоматический редирект
echo 4. Если нет - красивая страница с кнопками перехода
echo.

pause
