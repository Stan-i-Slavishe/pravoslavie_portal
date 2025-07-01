@echo off
chcp 65001 >nul
echo ✨ СТИЛЬНАЯ КНОПКА "ПОДЕЛИТЬСЯ"
echo ===============================

echo 🎨 Что улучшено:
echo.
echo 📍 Внешний вид:
echo    ✓ Синий градиентный фон (#007bff → #0056b3)
echo    ✓ Белый текст с жирным шрифтом (font-weight: 600)
echo    ✓ Красивая тень (box-shadow с синим оттенком)
echo    ✓ Иконка изменена на bi-share-fill (заполненная)
echo.
echo 📍 Анимации:
echo    ✓ При наведении: более темный градиент
echo    ✓ Подъем на 2px вместо 1px
echo    ✓ Увеличенная тень при hover
echo    ✓ Плавные переходы (transition: all 0.2s ease)
echo.
echo 📍 Эффекты:
echo    ✓ Кнопка теперь выделяется на фоне
echo    ✓ Современный материальный дизайн
echo    ✓ Градиентный фон привлекает внимание
echo    ✓ Профессиональный внешний вид
echo.

echo 🔧 Применяем стильную кнопку...
python manage.py collectstatic --noinput

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul
start python manage.py runserver

echo.
echo 🎯 СТИЛЬНАЯ КНОПКА ГОТОВА!
echo.
echo 📍 Откройте: http://127.0.0.1:8000/stories/malishka/
echo.
echo 💡 Результат:
echo    🔴 [❤️ Нравится(1)]  🔵 [📤 Поделиться]
echo    ↑                    ↑
echo    Красная кнопка      СИНЯЯ ГРАДИЕНТНАЯ
echo.
echo ✨ Кнопка "Поделиться" теперь:
echo    • Яркая и заметная
echo    • С современным дизайном
echo    • С красивыми анимациями
echo    • Привлекает внимание пользователей
echo.
pause
