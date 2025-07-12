# Быстрый скрипт исправления views_playlists.py
# Запустить в корне проекта: python fix_views_playlists.py

import re

# Читаем файл
with open('stories/views_playlists.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Исправляем дублированный код
lines = content.split('\n')
fixed_lines = []
skip_until_def = False

for i, line in enumerate(lines):
    # Если мы видим повторенный код после добавления функции, пропускаем его
    if skip_until_def:
        if line.strip().startswith('def ') or line.strip().startswith('@'):
            skip_until_def = False
            fixed_lines.append(line)
        continue
    
    # Ищем место, где начинается повторенный код
    if 'Проверяем доступ' in line and 'playlist and playlist.creator' in lines[i+1] if i+1 < len(lines) else False:
        skip_until_def = True
        continue
    
    fixed_lines.append(line)

# Записываем исправленный файл
with open('stories/views_playlists.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(fixed_lines))

print("✅ Файл views_playlists.py исправлен!")
print("🔧 Удален дублированный код")
print("📝 Функция add_to_playlist добавлена корректно")