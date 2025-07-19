@echo off
echo ========================================
echo    ТЕСТ ИСПРАВЛЕНИЯ КНОПКИ УДАЛЕНИЯ
echo ========================================
echo.

echo 1. Проверяем синтаксис JavaScript в шаблоне...
python -c "
import re
with open('templates/stories/playlists_list.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Ищем JavaScript блок
js_start = content.find('{% block extra_js %}')
js_end = content.find('{% endblock %}', js_start)

if js_start == -1 or js_end == -1:
    print('❌ JavaScript блок не найден!')
    exit(1)
    
js_block = content[js_start:js_end]

# Проверяем наличие функций
functions = ['deletePlaylist', 'showCreatePlaylistModal', 'createPlaylist']
missing = []

for func in functions:
    if f'function {func}' not in js_block:
        missing.append(func)

if missing:
    print(f'❌ Отсутствуют функции: {missing}')
else:
    print('✅ Все JavaScript функции найдены')

# Проверяем синтаксические ошибки
bracket_count = js_block.count('{') - js_block.count('}')
if bracket_count != 0:
    print(f'❌ Несоответствие скобок: {bracket_count}')
else:
    print('✅ Синтаксис скобок корректен')
"

echo.
echo 2. Запускаем Django сервер для тестирования...
echo Откройте браузер: http://127.0.0.1:8000/stories/playlists/
echo Проверьте кнопку "Удалить" в мобильной версии
echo.

python manage.py runserver 127.0.0.1:8000
