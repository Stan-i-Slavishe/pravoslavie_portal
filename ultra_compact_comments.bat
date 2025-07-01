@echo off
chcp 65001 >nul
echo ⚡ УЛЬТРАКОМПАКТНЫЕ КОММЕНТАРИИ - УМЕНЬШЕНО НА 50%
echo ===============================================

echo 🎯 Что было изменено:
echo.
echo 📏 Отступы уменьшены на 50%:
echo    ✓ margin-bottom: 0.15rem → 0.075rem
echo    ✓ padding: 0.35rem → 0.175rem
echo    ✓ comment-text margin: 0.25rem → 0.125rem
echo    ✓ comment-actions margin: 0.15rem → 0.075rem
echo.
echo 📱 Кнопки стали компактнее:
echo    ✓ padding: 0.375rem → 0.1875rem
echo    ✓ font-size: 0.875rem → 0.75rem
echo    ✓ border-radius: 20px → 15px
echo    ✓ min-width: 60px → 45px
echo.
echo 📏 Высота строк уменьшена:
echo    ✓ line-height: 1.3 → 1.2
echo    ✓ На мобильных: 1.25 → 1.15
echo.

echo 🔧 Применяем ультракомпактные стили...
python manage.py collectstatic --noinput --clear

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

echo ⚡ Запускаем с УЛЬТРАКОМПАКТНЫМИ стилями...
start python manage.py runserver

echo.
echo 🎉 УЛЬТРАКОМПАКТНЫЕ КОММЕНТАРИИ ГОТОВЫ!
echo.
echo 📊 Итоговые размеры (уменьшено на 50%):
echo    • Отступы между комментариями: 0.075rem
echo    • Внутренние отступы: 0.175rem  
echo    • Отступы текста: 0.125rem
echo    • Кнопки лайков: 0.1875rem padding
echo    • Высота строк: 1.2
echo.
echo 💡 Теперь комментарии максимально компактные!
echo 🌐 Обновите страницу в браузере для просмотра
echo.
pause
