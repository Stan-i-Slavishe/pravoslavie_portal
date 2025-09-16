@echo off
REM Скрипт мониторинга для Windows
REM Создан автоматически для интеграции системы мониторинга

set PROJECT_DIR=E:\pravoslavie_portal
set PYTHON_PATH=python
set MANAGE_PY=%PROJECT_DIR%\manage.py
set LOG_FILE=%PROJECT_DIR%\logs\monitoring_cron.log

REM Функция логирования
echo [%date% %time%] Запуск мониторинга >> "%LOG_FILE%"

REM Переход в директорию проекта
cd /d "%PROJECT_DIR%"
set DJANGO_ENV=production

REM Выбор действия
if "%1"=="system" goto system_check
if "%1"=="cleanup" goto cleanup_logs
if "%1"=="report" goto generate_report
if "%1"=="health" goto health_check
if "%1"=="all" goto all_checks
goto usage

:system_check
echo [%date% %time%] Проверка системы >> "%LOG_FILE%"
%PYTHON_PATH% %MANAGE_PY% monitor_system --check-all --send-alerts >> "%LOG_FILE%" 2>&1
goto end

:cleanup_logs
echo [%date% %time%] Очистка логов >> "%LOG_FILE%"
%PYTHON_PATH% %MANAGE_PY% cleanup_logs --days=7 >> "%LOG_FILE%" 2>&1
goto end

:generate_report
echo [%date% %time%] Создание отчета >> "%LOG_FILE%"
set REPORT_FILE=%PROJECT_DIR%\logs\monitoring_report_%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%.txt
%PYTHON_PATH% %MANAGE_PY% monitoring_report --hours=24 --save="%REPORT_FILE%" >> "%LOG_FILE%" 2>&1
goto end

:health_check
echo [%date% %time%] Проверка здоровья >> "%LOG_FILE%"
curl -s -o nul -w "%%{http_code}" http://localhost:8000/health/simple/ > temp_status.txt
set /p STATUS_CODE=<temp_status.txt
del temp_status.txt
if "%STATUS_CODE%"=="200" (
    echo [%date% %time%] Django приложение: OK >> "%LOG_FILE%"
) else (
    echo [%date% %time%] Django приложение: FAILED >> "%LOG_FILE%"
)
goto end

:all_checks
call :health_check
call :system_check
goto end

:usage
echo Использование: %0 {system|cleanup|report|health|all}
echo   system  - Проверка системных ресурсов
echo   cleanup - Очистка старых логов
echo   report  - Создание отчета
echo   health  - Проверка здоровья сервисов
echo   all     - Полная проверка
goto end

:end
echo [%date% %time%] Мониторинг завершен >> "%LOG_FILE%"
