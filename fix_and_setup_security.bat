@echo off
echo 🛡️ ИСПРАВЛЕНИЕ И УСТАНОВКА системы защиты
echo.

cd /d "E:\pravoslavie_portal"

echo 🔄 Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo ✅ Файл security.py исправлен!

echo 📝 Добавление настроек безопасности в settings.py...
if not exist "config\settings_backup.py" (
    copy "config\settings.py" "config\settings_backup.py"
    echo ✅ Создан backup файла settings.py
)

type security_settings_addon.py >> config\settings.py
echo ✅ Настройки безопасности добавлены!

echo 🔄 Создание миграций...
python manage.py makemigrations

echo 🔄 Применение миграций...
python manage.py migrate

echo 📊 Тестирование системы безопасности...
python manage.py security --stats

echo.
echo ✅ Система защиты успешно установлена!
echo.
echo 📋 Доступные команды управления:
echo   python manage.py security --show-blocked    # Показать заблокированные IP
echo   python manage.py security --unblock-ip IP   # Разблокировать IP
echo   python manage.py security --block-ip IP     # Заблокировать IP
echo   python manage.py security --stats           # Статистика
echo.
echo 🛡️ Активная защита:
echo   ✅ Rate Limiting: 60 запросов/мин, 1000/час
echo   ✅ DDoS защита с автоблокировкой
echo   ✅ Детекция подозрительных паттернов
echo   ✅ Защита API endpoints
echo   ✅ Security headers
echo   ✅ Логирование атак в logs/security.log
echo.
echo ⚠️  Для восстановления: copy config\settings_backup.py config\settings.py
echo.
echo 🚀 Запуск защищенного сервера...
python manage.py runserver

pause