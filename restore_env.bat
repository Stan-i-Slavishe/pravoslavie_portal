@echo off
echo 🔄 Восстанавливаем оригинальный .env файл...

if exist .env.temp_backup (
    copy .env.temp_backup .env
    del .env.temp_backup
    echo ✅ Оригинальный .env восстановлен
) else (
    echo ⚠️ Backup не найден
)

echo 🔄 Возвращаем окружение к local...
set DJANGO_ENV=local
