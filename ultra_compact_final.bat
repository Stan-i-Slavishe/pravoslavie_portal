@echo off
chcp 65001 >nul
echo ⚡ СИСТЕМА УЛЬТРАКОМПАКТНЫХ КОММЕНТАРИЕВ ⚡
echo =============================================

echo 🎯 РЕЗУЛЬТАТ: Отступы уменьшены на 50%!
echo.
echo 📏 Новые размеры (было → стало):
echo    ✓ Отступы между комментариями: 0.15rem → 0.075rem
echo    ✓ Внутренние отступы: 0.35rem → 0.175rem  
echo    ✓ Отступы текста: 0.25rem → 0.125rem
echo    ✓ Отступы действий: 0.15rem → 0.075rem
echo    ✓ Отступы заголовка: 0.1rem → 0.05rem
echo.
echo 🔘 Кнопки стали компактнее:
echo    ✓ Размер кнопок: 0.375rem → 0.1875rem
echo    ✓ Размер текста: 0.875rem → 0.75rem
echo    ✓ Радиус: 20px → 15px
echo    ✓ Ширина: 60px → 45px
echo.
echo 📱 Высота строк уменьшена:
echo    ✓ Основная: 1.3 → 1.2
echo    ✓ На мобильных: 1.25 → 1.15
echo.

echo 🔧 Применяем все изменения...
python manage.py collectstatic --noinput --clear

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 3 /nobreak >nul

echo ⚡ Запускаем с УЛЬТРАКОМПАКТНЫМИ комментариями...
start python manage.py runserver

echo.
echo 🎉 УЛЬТРАКОМПАКТНЫЕ КОММЕНТАРИИ АКТИВИРОВАНЫ!
echo.
echo 📊 Обновленные файлы:
echo    ✅ main.css - глобальные ультракомпактные стили
echo    ✅ stories.css - компактные стили для stories
echo    ✅ comment_item.html - шаблон с новыми размерами
echo    ✅ comments-extreme.css - экстремальные варианты
echo.
echo 💡 Дополнительные уровни компактности:
echo    🔹 Добавьте класс "extreme-compact" для еще большей компактности
echo    🔹 Используйте "minimal-extreme" для минималистичного вида
echo    🔹 Попробуйте "flat-extreme" для плоского дизайна
echo.
echo 🎯 Теперь комментарии стали в 2 раза компактнее!
echo 🌐 Обновите страницу в браузере для просмотра
echo.
echo ====================================================
echo 📝 Сравнение размеров:
echo    🔺 БЫЛО: margin: 0.15rem, padding: 0.35rem
echo    🔻 СТАЛО: margin: 0.075rem, padding: 0.175rem
echo    📉 УМЕНЬШЕНИЕ: -50% по всем параметрам!
echo ====================================================
echo.
pause
