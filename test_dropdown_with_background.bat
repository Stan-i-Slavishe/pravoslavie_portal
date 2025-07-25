@echo off
echo ==================================================
echo ПРОСТОЕ ИСПРАВЛЕНИЕ DROPDOWN МЕНЮ + ФОН
echo ==================================================
echo.
echo Проблема: admin просвечивает через меню "Разделы"
echo Решение: Добавлен непрозрачный белый фон
echo.
echo ЧТО ДОБАВЛЕНО:
echo • background-color: #ffffff !important
echo • border: 1px solid rgba(0,0,0,0.15)
echo • box-shadow: 0 4px 12px rgba(0,0,0,0.15)
echo • opacity: 1 !important
echo.
echo Теперь меню должно ПОЛНОСТЬЮ скрывать admin!
echo.

cd /d "E:\pravoslavie_portal"
python manage.py runserver 127.0.0.1:8000

echo.
echo ТЕСТ:
echo 1. Откройте http://127.0.0.1:8000
echo 2. iPhone SE в DevTools
echo 3. Авторизуйтесь
echo 4. Нажмите "Разделы"
echo 5. Меню admin НЕ должно быть видно!
echo.
pause
