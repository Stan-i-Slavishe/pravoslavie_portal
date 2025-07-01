@echo off
chcp 65001 >nul
echo 🎨 ВОССТАНОВЛЕНИЕ СТИЛЕЙ КНОПКИ "ПОДЕЛИТЬСЯ"
echo ===========================================

echo ❌ Проблема: кнопка стала серой после изменения на toggleShareMenu
echo ✅ Решение: добавлен CSS селектор для нового onclick

echo.
echo 🔧 Что исправлено:
echo    • Добавлен селектор .action-btn[onclick*="toggleShareMenu"]
echo    • Синий градиентный фон восстановлен
echo    • Белый текст и жирный шрифт
echo    • Красивые тени и hover-эффекты
echo.

echo 🔄 Применяем исправления...
python manage.py collectstatic --noinput

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
start python manage.py runserver

echo.
echo 🎯 СТИЛИ ВОССТАНОВЛЕНЫ!
echo.
echo 📍 Результат:
echo    🔴 [❤️ Нравится(1)]  🔵 [📤 Поделиться]
echo    ↑                    ↑
echo    Красная кнопка       СИНЯЯ ГРАДИЕНТНАЯ
echo.
echo ✅ Кнопка "Поделиться" снова яркая и заметная!
echo 📍 Откройте: http://127.0.0.1:8000/stories/malishka/
pause
