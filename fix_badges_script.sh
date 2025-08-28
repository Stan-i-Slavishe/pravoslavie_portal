#!/bin/bash

# Исправляем бейджи плейлистов
echo "🔧 Исправляем бейджи количества рассказов в плейлистах..."

# Путь к файлу
FILE_PATH="/e/pravoslavie_portal/templates/stories/playlists_list.html"

# Создаем резервную копию
cp "$FILE_PATH" "${FILE_PATH}.backup_$(date +%Y%m%d_%H%M%S)"

# Используем sed для замены
# Находим строки с {{ playlist.calculated_stories_count }} и заменяем на версию с "рассказов"
sed -i 's/{{ playlist\.calculated_stories_count }}$/{{ playlist.calculated_stories_count }} рассказов/g' "$FILE_PATH"

# Удаляем дублирования если они есть
sed -i 's/рассказов рассказов рассказов/рассказов/g' "$FILE_PATH"
sed -i 's/рассказов рассказов/рассказов/g' "$FILE_PATH"

echo "✅ Исправления применены!"
echo "📋 Показываем измененные строки:"

# Показываем строки с рассказов
grep -n "calculated_stories_count.*рассказов" "$FILE_PATH"

echo ""
echo "🎉 Готово! Теперь в бейджах отображается '1 рассказов', '2 рассказов' и т.д."
