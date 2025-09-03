@echo off
echo 🔧 Создаем временную ссылку для тестирования staging...

REM Удаляем старую ссылку если есть
if exist .env.temp_backup del .env.temp_backup

REM Создаем backup текущего .env
if exist .env (
    copy .env .env.temp_backup
    echo ✅ Создан backup текущего .env
)

REM Копируем .env.staging в .env для тестирования
copy .env.staging .env
echo ✅ Скопирован .env.staging в .env

echo.
echo 🧪 Теперь выполните: python manage.py check --deploy
echo.
echo ⚠️ ВАЖНО: После тестирования выполните restore_env.bat
