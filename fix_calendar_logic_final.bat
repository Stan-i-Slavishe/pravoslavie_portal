@echo off
echo 🔧 ИСПРАВЛЕНИЕ ЛОГИЧЕСКОЙ ОШИБКИ В КАЛЕНДАРЕ
echo ===============================================
cd /d "E:\pravoslavie_portal"

echo.
echo 🐛 Обнаруженная проблема:
echo    Календарь показывал "Пост + Сплошная неделя"
echo    Это логическое противоречие!
echo.
echo 💡 Сплошная неделя по определению означает:
echo    "Отмена поста в среду и пятницу"
echo.
echo ✅ Правильная логика:
echo    - Сплошная неделя ОТМЕНЯЕТ пост
echo    - Возможны только: Праздник + Сплошная неделя
echo    - Невозможно: Пост + Сплошная неделя
echo.

pause

echo 🔧 Исправляем логику...
python fix_calendar_logic_error.py

echo.
echo 🔄 Применяем изменения...
python manage.py collectstatic --noinput

echo.
echo ✅ Исправления завершены!
echo.
echo 📊 Теперь календарь показывает:
echo   🔴 Красный = Праздники
echo   🟣 Фиолетовый = Посты 
echo   🟢 Зеленый = Сплошные недели (БЕЗ постов!)
echo   🎭 Комбинированные:
echo      • Праздник + Пост (80/20)
echo      • Праздник + Сплошная неделя (80/20)
echo.
echo 🚀 Запустить сервер для проверки? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    echo Запускаем сервер...
    python manage.py runserver
) else (
    echo Для запуска выполните: python manage.py runserver
)

pause
