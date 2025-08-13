@echo off
echo 🛡️ Активация системы безопасности православного портала...
echo ===============================================================

echo.
echo 📋 Проверка готовности системы...

REM Проверяем наличие ключевых файлов
if not exist "core\middleware\advanced_security.py" (
    echo ❌ Файл advanced_security.py не найден!
    goto :error
)

if not exist "core\management\commands\security_admin.py" (
    echo ❌ Файл security_admin.py не найден!
    goto :error
)

echo ✅ Все файлы найдены

echo.
echo 🔧 Применяем миграции...
python manage.py migrate

echo.
echo 📊 Собираем статические файлы...
python manage.py collectstatic --noinput

echo.
echo 🛡️ Тестируем систему безопасности...
echo.
echo Тест 1: Показываем текущую статистику
python manage.py security_admin --stats

echo.
echo Тест 2: Проверяем подозрительные паттерны
python manage.py security_admin --test-patterns

echo.
echo 🚀 Запускаем сервер с защитой...
echo.
echo ⚠️ ВАЖНО: Система безопасности активна!
echo    - Rate limiting включен
echo    - Подозрительные паттерны блокируются
echo    - Логирование работает
echo.
echo 📊 Команды управления:
echo    python manage.py security_admin --stats          - Статистика
echo    python manage.py security_admin --show-blocked   - Заблокированные IP
echo    python manage.py security_admin --help           - Все команды
echo.

REM Запускаем сервер
python manage.py runserver

goto :end

:error
echo.
echo ❌ Ошибка! Система безопасности не готова к активации.
echo    Проверьте наличие всех файлов и повторите попытку.
pause
goto :end

:end
