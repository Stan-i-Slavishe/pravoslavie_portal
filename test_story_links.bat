@echo off
echo 🔍 БЫСТРАЯ ПРОВЕРКА ПРОБЛЕМЫ С ДЕТАЛИЗАЦИЕЙ
echo.

echo ===============================================
echo 📋 ШАГ 1: Проверка конкретного URL
echo ===============================================

python manage.py shell -c "
from django.urls import reverse
from stories.models import Story

print('=== ТЕСТИРОВАНИЕ URL ДЛЯ РЕДАКТИРОВАНИЯ ===')

# Находим рассказ 'Как святой Лука дочь спас' 
luka_story = Story.objects.filter(title__icontains='святой Лука').first()

if luka_story:
    change_url = reverse('admin:stories_story_change', args=[luka_story.pk])
    print('✅ Правильный URL для редактирования:')
    print('   http://127.0.0.1:8000{}'.format(change_url))
    print('📝 ID рассказа: {}'.format(luka_story.pk))
    print('📝 Заголовок: {}'.format(luka_story.title))
else:
    # Берем любой первый рассказ
    first_story = Story.objects.first()
    if first_story:
        change_url = reverse('admin:stories_story_change', args=[first_story.pk])
        print('✅ Правильный URL для первого рассказа:')
        print('   http://127.0.0.1:8000{}'.format(change_url))
        print('📝 ID рассказа: {}'.format(first_story.pk))
        print('📝 Заголовок: {}'.format(first_story.title))
    else:
        print('❌ Нет рассказов в базе данных!')
"

echo.
echo ===============================================
echo 📋 ШАГ 2: Прямое тестирование
echo ===============================================

echo 🎯 ПОПРОБУЙТЕ ЭТИ ССЫЛКИ ВРУЧНУЮ:
echo.
echo 📚 Список рассказов:
echo    http://127.0.0.1:8000/admin/stories/story/
echo.
echo 📝 Добавить новый рассказ:
echo    http://127.0.0.1:8000/admin/stories/story/add/
echo.

REM Получаем ID первого рассказа для тестирования
for /f %%i in ('python manage.py shell -c "from stories.models import Story; s=Story.objects.first(); print(s.pk if s else 'нет')"') do set STORY_ID=%%i

if "%STORY_ID%" neq "нет" (
    echo 🔧 Редактирование первого рассказа ^(ID %STORY_ID%^):
    echo    http://127.0.0.1:8000/admin/stories/story/%STORY_ID%/change/
) else (
    echo ⚠️ Нет рассказов для тестирования
)

echo.
echo ===============================================
echo 📋 ШАГ 3: Инструкции по тестированию
echo ===============================================

echo 🔧 ЧТО ДЕЛАТЬ:
echo.
echo 1. Скопируйте ссылку редактирования выше
echo 2. Вставьте её в адресную строку браузера
echo 3. Нажмите Enter
echo 4. Должна открыться форма редактирования рассказа
echo.
echo 💡 АЛЬТЕРНАТИВНЫЙ СПОСОБ:
echo 1. В списке рассказов кликните ПРАВОЙ кнопкой на название
echo 2. Выберите "Копировать адрес ссылки"
echo 3. Вставьте ссылку в новую вкладку
echo.
echo ⚠️ ЕСЛИ НЕ РАБОТАЕТ:
echo 1. Очистите кеш браузера (Ctrl+Shift+Del)
echo 2. Попробуйте режим инкогнито (Ctrl+Shift+N)
echo 3. Проверьте консоль браузера (F12) на ошибки
echo.
pause

echo Запускаем сервер...
python manage.py runserver
