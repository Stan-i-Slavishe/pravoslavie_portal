@echo off
echo 🔓 Разблокировка вашего IP после тестирования...
echo.

echo Разблокируем IP 127.0.0.1...
python manage.py security_admin --unblock-ip 127.0.0.1

echo.
echo Проверяем статистику...
python manage.py security_admin --stats

echo.
echo ✅ Готово! Теперь можете снова пользоваться сайтом.
echo 🌐 Откройте: http://127.0.0.1:8000/
echo.
pause
