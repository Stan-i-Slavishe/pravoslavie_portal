@echo off
chcp 65001 >nul
echo 💬 ДОБАВЛЕНИЕ СТАТИСТИКИ КОММЕНТАРИЕВ В DETAIL_V2.HTML
echo ===================================================

echo ✅ Что добавлено:
echo.
echo 📍 В метаданные (под заголовком):
echo    ✓ Иконка комментариев (bi-chat-dots)
echo    ✓ Счетчик "X комментариев" с правильным склонением
echo    ✓ ID "comments-count-meta" для обновления
echo.
echo 📊 В боковую панель статистики:
echo    ✓ Изменена сетка с col-6 на col-4 (3 колонки)
echo    ✓ Добавлена колонка с комментариями (зеленый цвет)
echo    ✓ ID "comments-count-sidebar" для обновления
echo.
echo 🎨 JavaScript функциональность:
echo    ✓ Функция updateCommentsCounter() для обновления
echo    ✓ Правильное склонение (комментарий/комментария/комментариев)
echo    ✓ Анимация при изменении счетчика
echo    ✓ Синхронизация между двумя счетчиками
echo.

echo 🔧 Применяем изменения...
python manage.py collectstatic --noinput

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
start python manage.py runserver

echo.
echo 🎯 СТАТИСТИКА КОММЕНТАРИЕВ ДОБАВЛЕНА!
echo.
echo 📍 Откройте: http://127.0.0.1:8000/stories/malishka/
echo.
echo 💡 Теперь должно отображаться:
echo    📅 30 Июнь 2025
echo    👁️ 1 просмотров  
echo    ❤️ 1 лайков
echo    💬 0 комментариев ← НОВОЕ!
echo    📁 Врачебные истории
echo.
echo 📊 В боковой панели:
echo    Просмотры | Лайки | Комментарии
echo        1     |   1   |      0
echo.
echo 🔄 При добавлении комментария:
echo    - Счетчики обновятся автоматически
echo    - Правильное склонение слов
echo    - Анимация увеличения
echo.
pause
