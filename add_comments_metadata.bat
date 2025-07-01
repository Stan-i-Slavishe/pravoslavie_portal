@echo off
echo ========================================
echo   ДОБАВЛЕНИЕ МЕТАДАННЫХ КОММЕНТАРИЕВ
echo ========================================
echo.

echo 🗂️ Переходим в директорию проекта...
cd /d "E:\pravoslavie_portal"

echo 🔧 Активируем виртуальное окружение...
call venv\Scripts\activate

echo 📦 Собираем статические файлы...
python manage.py collectstatic --noinput

echo 🔄 Очищаем кэш Django...
python manage.py shell -c "from django.core.cache import cache; cache.clear(); print('Кэш очищен!')"

echo ✅ Метаданные комментариев добавлены!
echo.
echo 📋 Что добавлено в карточки рассказов:
echo    ✓ Иконка комментариев (bi-chat) рядом с просмотрами
echo    ✓ Количество комментариев для каждого рассказа
echo    ✓ Автоматический подсчет только основных комментариев (не ответы)
echo    ✓ Горизонтальное расположение: [👁️ 1] [💬 26]
echo    ✓ Обновлено представление для передачи данных
echo.
echo 📍 Результат на карточках:
echo    Было: [👁️ 1] 
echo    Стало: [👁️ 1] [💬 26]
echo.
echo 🔄 Перезагрузите страницу в браузере (Ctrl+F5)
echo 🌐 http://127.0.0.1:8000/stories/
echo.

pause
