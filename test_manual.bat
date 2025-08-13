@echo off
echo 🧪 Тестирование защиты в реальном времени...
echo.

echo Откройте второй терминал и попробуйте эти URL в браузере:
echo.
echo ❌ ДОЛЖНЫ БЫТЬ ЗАБЛОКИРОВАНЫ:
echo    http://127.0.0.1:8000/?id=1; DROP TABLE users;
echo    http://127.0.0.1:8000/search?q=^<script^>alert("xss")^</script^>
echo    http://127.0.0.1:8000/files?path=../../etc/passwd
echo    http://127.0.0.1:8000/wp-admin/admin.php
echo.
echo ✅ ДОЛЖНЫ РАБОТАТЬ НОРМАЛЬНО:
echo    http://127.0.0.1:8000/
echo    http://127.0.0.1:8000/stories/
echo    http://127.0.0.1:8000/books/
echo    http://127.0.0.1:8000/shop/
echo.
echo 📊 Проверить статистику после тестов:
echo    python manage.py security_admin --stats
echo.
pause
