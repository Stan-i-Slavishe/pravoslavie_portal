@echo off
echo ==================================================
echo УЛЬТРА ПРОСТОЕ РЕШЕНИЕ: CSS + JAVASCRIPT
echo ==================================================
echo.
echo Проблема: admin упорно не скрывается
echo Решение: JavaScript добавляет класс + CSS скрывает элементы
echo.
echo КАК РАБОТАЕТ:
echo • При открытии dropdown добавляется класс "dropdown-active" к body
echo • CSS скрывает все nav-item кроме активного dropdown
echo • При закрытии dropdown класс убирается
echo.
echo Файлы:
echo • static/css/ultra-simple-dropdown.css
echo • JavaScript в base.html
echo.

cd /d "E:\pravoslavie_portal"
python manage.py runserver 127.0.0.1:8000

echo.
echo УЛЬТРА ТЕСТ:
echo 1. Откройте http://127.0.0.1:8000
echo 2. iPhone SE в DevTools
echo 3. Авторизуйтесь
echo 4. Нажмите "Разделы"
echo 5. admin должен стать полупрозрачным/исчезнуть!
echo 6. Нажмите в другое место - admin должен вернуться!
echo.
pause
