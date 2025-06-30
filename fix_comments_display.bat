@echo off
echo ========================================
echo ПРИМЕНЕНИЕ ИСПРАВЛЕНИЙ КОММЕНТАРИЕВ
echo ========================================

cd /d "E:\pravoslavie_portal"

echo.
echo 1. Создаем миграции...
python manage.py makemigrations stories

echo.
echo 2. Применяем миграции...
python manage.py migrate

echo.
echo 3. Создаем тестовые комментарии...
python create_test_comments.py

echo.
echo 4. Собираем статические файлы...
python manage.py collectstatic --noinput

echo.
echo ========================================
echo ГОТОВО! Комментарии должны появиться
echo ========================================
echo.
echo Что было исправлено:
echo - Заменена заглушка в правильном шаблоне (detail_v2.html)
echo - Обновлен view для передачи данных комментариев
echo - Добавлены реакции пользователя
echo.
echo Теперь обновите страницу рассказа в браузере!
echo.
pause
