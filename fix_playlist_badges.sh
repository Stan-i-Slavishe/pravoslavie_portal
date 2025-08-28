#!/bin/bash

# Поиск и замена всех вхождений количества рассказов в плейлистах
# Заменяем {{ playlist.calculated_stories_count }} на {{ playlist.calculated_stories_count }} рассказов

sed -i 's/{{ playlist\.calculated_stories_count }}/{{ playlist.calculated_stories_count }} рассказов/g' /cygdrive/e/pravoslavie_portal/templates/stories/playlists_list.html

echo "✅ Обновлены все бейджи количества рассказов"
