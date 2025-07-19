@echo off
echo ========================================
echo   ТЕСТ УЛУЧШЕННОГО SPACING МЕТАДАННЫХ
echo ========================================
echo.

echo 1. Проверяем обновленные CSS стили...
python -c "
with open('templates/stories/playlist_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Проверяем наличие увеличенных отступов
spacing_elements = [
    'gap: 1.25rem',
    'padding: 0.5rem 0.75rem',
    'margin-right: 0.5rem',
    'border-radius: 8px'
]

missing = []
for element in spacing_elements:
    if element not in content:
        missing.append(element)

if missing:
    print(f'❌ Отсутствуют элементы: {missing}')
else:
    print('✅ Все элементы spacing найдены')

# Проверяем box-shadow
if 'box-shadow:' in content:
    print('✅ Тени добавлены для глубины')
else:
    print('❌ Тени не найдены')
"

echo.
echo 2. Новое расположение метаданных плейлиста:
echo.
echo   [  3 рассказов  ] [  12 Июль 2025  ] [  Приватный  ]
echo     ^^^ больше пространства между элементами
echo.

echo 3. Запускаем сервер для тестирования...
echo Откройте: http://127.0.0.1:8000/stories/playlists/кукриниксы/
echo Проверьте улучшенный spacing между метаданными
echo.

python manage.py runserver 127.0.0.1:8000
