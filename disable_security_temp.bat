@echo off
echo 🔧 Временное отключение middleware безопасности для тестирования
echo.

cd /d "E:\pravoslavie_portal"

echo 🔄 Создание временной копии settings.py...
copy config\settings.py config\settings_with_security.py

echo 🔄 Восстановление оригинального settings.py...
if exist config\settings_backup.py (
    copy config\settings_backup.py config\settings.py
    echo ✅ Восстановлен оригинальный settings.py
) else (
    echo ⚠️  Backup не найден, удаляем добавленные строки...
    powershell -Command "(Get-Content config\settings.py) | Where-Object {$_ -notmatch 'НАСТРОЙКИ БЕЗОПАСНОСТИ'} | Set-Content config\settings_temp.py"
    move config\settings_temp.py config\settings.py
)

echo.
echo ✅ Middleware безопасности временно отключен
echo 🚀 Запуск сервера для тестирования...
python manage.py runserver

pause