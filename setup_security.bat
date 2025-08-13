@echo off
echo 🛡️ Установка системы защиты от DDoS и атак
echo.

cd /d "E:\pravoslavie_portal"

echo 🔄 Активация виртуального окружения...
call .venv\Scripts\activate.bat

echo 📝 Добавление настроек безопасности в settings.py...
type security_settings_addon.py >> config\settings.py

echo 🔄 Создание миграций...
python manage.py makemigrations

echo 🔄 Применение миграций...
python manage.py migrate

echo 📊 Тестирование системы безопасности...
python manage.py security --stats

echo.
echo ✅ Система защиты установлена!
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
echo 🚀 Запуск защищенного сервера...
python manage.py runserver

pause