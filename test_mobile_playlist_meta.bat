@echo off
echo ========================================
echo  ТЕСТ МОБИЛЬНЫХ МЕТАДАННЫХ ПЛЕЙЛИСТА
echo ========================================
echo.

echo 1. Проверяем CSS стили для метаданных...
python -c "
with open('templates/stories/playlist_detail.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Проверяем наличие ключевых CSS классов
css_classes = [
    'playlist-meta',
    'playlist-header', 
    'playlist-title',
    'playlist-actions'
]

missing = []
for css_class in css_classes:
    if css_class not in content:
        missing.append(css_class)

if missing:
    print(f'❌ Отсутствуют CSS классы: {missing}')
else:
    print('✅ Все CSS классы найдены')

# Проверяем медиа-запросы
if '@media (max-width: 768px)' in content:
    print('✅ Мобильные стили добавлены')
else:
    print('❌ Мобильные стили не найдены')

# Проверяем горизонтальное расположение
if 'flex-direction: row' in content:
    print('✅ Горизонтальное расположение настроено')
else:
    print('❌ Горизонтальное расположение не настроено')
"

echo.
echo 2. Структура метаданных плейлиста:
echo    [3 рассказов] [Июль 2025] [Приватный]
echo    ^^ должны быть в одной строке на мобильных
echo.

echo 3. Запускаем сервер для тестирования...
echo Откройте: http://127.0.0.1:8000/stories/playlists/кукриниксы/
echo Переключите на мобильный режим в браузере
echo.

python manage.py runserver 127.0.0.1:8000
