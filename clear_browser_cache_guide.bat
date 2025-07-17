@echo off
echo 🧹 ОЧИСТКА БРАУЗЕРНОГО КЕША И HSTS
echo =================================
echo.

echo Этот скрипт поможет очистить кеш браузера и HSTS настройки
echo.

REM Устанавливаем кодировку UTF-8
chcp 65001 >nul

echo 🔹 ИНСТРУКЦИИ ПО ОЧИСТКЕ КЕША:
echo.

echo 🟦 GOOGLE CHROME / MICROSOFT EDGE:
echo ─────────────────────────────────
echo 1. Нажмите Ctrl+Shift+Delete
echo 2. Выберите "Все время"
echo 3. Отметьте все пункты
echo 4. Нажмите "Удалить данные"
echo.
echo 5. Откройте новую вкладку и введите: chrome://net-internals/^#hsts
echo 6. Прокрутите до "Delete domain security policies"
echo 7. Введите: localhost
echo 8. Нажмите "Delete"
echo 9. Введите: 127.0.0.1
echo 10. Нажмите "Delete"
echo.

echo 🟧 MOZILLA FIREFOX:
echo ──────────────────
echo 1. Нажмите Ctrl+Shift+Delete
echo 2. Выберите "Все"
echo 3. Отметьте все пункты
echo 4. Нажмите "Удалить сейчас"
echo.
echo 5. Откройте новую вкладку и введите: about:config
echo 6. Найдите: security.tls.insecure_fallback_hosts
echo 7. Добавьте значение: localhost,127.0.0.1
echo.

echo 🟪 АЛЬТЕРНАТИВНЫЕ РЕШЕНИЯ:
echo ─────────────────────────
echo 1. Используйте режим инкогнито/приватный просмотр
echo 2. Используйте другой браузер
echo 3. Временно отключите антивирус/firewall
echo 4. Перезагрузите компьютер
echo.

echo 💡 ПОСЛЕ ОЧИСТКИ КЕША:
echo ─────────────────────
echo 1. Полностью закройте браузер
echo 2. Откройте браузер заново
echo 3. Введите ТОЧНО: http://127.0.0.1:8000/
echo 4. НЕ используйте https://
echo.

echo 🚨 ЕСЛИ ПРОБЛЕМА ПОВТОРЯЕТСЯ:
echo ────────────────────────────
echo 1. Откройте файл open_django.html в корне проекта
echo 2. Или используйте команду: start http://127.0.0.1:8000/
echo 3. Или используйте другой порт: python manage.py runserver 127.0.0.1:8001
echo.

echo 🎯 ГОТОВЫ ПРОДОЛЖИТЬ?
echo.
set /p continue="Очистили кеш браузера? (y/n): "

if /i "%continue%"=="y" (
    echo.
    echo ✅ Отлично! Теперь запустите: fix_https_problem.bat
    echo.
    set /p run_fix="Запустить исправление сейчас? (y/n): "
    if /i "%run_fix%"=="y" (
        call fix_https_problem.bat
    )
) else (
    echo.
    echo ⚠️ Сначала очистите кеш браузера согласно инструкциям выше
    echo Затем запустите этот скрипт снова
)

pause
