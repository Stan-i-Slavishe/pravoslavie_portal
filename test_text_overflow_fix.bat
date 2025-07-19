@echo off
echo ========================================
echo    ТЕСТ ИСПРАВЛЕНИЯ ПЕРЕПОЛНЕНИЯ ТЕКСТА
echo ========================================
echo.

echo 1. Проверяем CSS стили для контроля ширины...
python -c "
with open('templates/stories/playlist_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Проверяем наличие контроля ширины
overflow_elements = [
    'max-width:',
    'overflow: hidden',
    'text-overflow: ellipsis'
]

missing = []
for element in overflow_elements:
    if element not in content:
        missing.append(element)

if missing:
    print(f'❌ Отсутствуют элементы: {missing}')
else:
    print('✅ Все элементы контроля переполнения найдены')

# Проверяем медиа-запросы для маленьких экранов
if '@media (max-width: 400px)' in content:
    print('✅ Добавлены стили для очень маленьких экранов')
else:
    print('❌ Стили для маленьких экранов не найдены')
"

echo.
echo 2. Ограничения ширины метаданных:
echo    Desktop: max-width: 150px
echo    Mobile:  max-width: 120px  
echo    Small:   max-width: 100px
echo    ^^^ с обрезкой длинного текста
echo.

echo 3. Запускаем сервер для тестирования...
echo Откройте: http://127.0.0.1:8000/stories/playlists/кукриниксы/
echo Проверьте что текст не выходит за пределы
echo.

python manage.py runserver 127.0.0.1:8000
