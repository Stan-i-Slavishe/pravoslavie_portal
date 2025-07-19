@echo off
echo ========================================
echo   ТЕСТ ЦЕНТРИРОВАНИЯ МЕТАДАННЫХ
echo ========================================
echo.

echo 1. Проверяем CSS стили для центрирования...
python -c "
with open('templates/stories/playlist_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Проверяем наличие ключевых CSS элементов
css_elements = [
    'justify-content: center',
    'flex-direction: column',
    'align-items: center',
    'text-align: center'
]

missing = []
for element in css_elements:
    if element not in content:
        missing.append(element)

if missing:
    print(f'❌ Отсутствуют элементы: {missing}')
else:
    print('✅ Все CSS элементы найдены')

# Проверяем фоновую подложку
if 'background: #f8f9fa' in content:
    print('✅ Фоновая подложка добавлена')
else:
    print('❌ Фоновая подложка не найдена')
"

echo.
echo 2. Новая структура метаданных в плейлисте:
echo.
echo    [фоновая подложка]
echo      👁️     📅     📁
echo   3 просм  03.07  Школьные
echo   ^^^ центрировано с иконками сверху
echo.

echo 3. Запускаем сервер для тестирования...
echo Откройте: http://127.0.0.1:8000/stories/playlists/кукриниксы/
echo Проверьте центрирование метаданных рассказов
echo.

python manage.py runserver 127.0.0.1:8000
