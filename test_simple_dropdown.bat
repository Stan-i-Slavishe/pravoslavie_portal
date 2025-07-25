@echo off
echo ==================================================
echo ПРОСТОЕ ИСПРАВЛЕНИЕ DROPDOWN МЕНЮ
echo ==================================================
echo.
echo Проблема: Меню "Разделы" смещено вправо
echo Решение: ПОЛНЫЙ СБРОС всех позиционирований + только z-index
echo.
echo ЧТО СДЕЛАНО:
echo • Убраны ВСЕ сложные CSS файлы
echo • Оставлен только z-index: 9999
echo • Полный сброс позиционирования на auto
echo • Возврат к стандартному Bootstrap поведению
echo.
echo Файл: static/css/simple-dropdown-fix.css
echo.

cd /d "E:\pravoslavie_portal"
python manage.py runserver 127.0.0.1:8000

echo.
echo ТЕСТ:
echo 1. Откройте http://127.0.0.1:8000
echo 2. iPhone SE в DevTools
echo 3. Авторизуйтесь
echo 4. Нажмите "Разделы"
echo 5. ДОЛЖНО: меню под кнопкой, перекрывает admin
echo.
pause
