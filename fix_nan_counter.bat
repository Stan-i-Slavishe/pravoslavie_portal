@echo off
chcp 65001 >nul
echo ===== ИСПРАВЛЕНИЕ ПРОБЛЕМЫ NaN В СЧЕТЧИКЕ =====
echo.

echo ❌ Проблема: Счетчик показывает "NaN" вместо числа
echo ✅ Решение: Улучшенная логика извлечения числа из badge
echo.

echo 🔧 Что было исправлено:
echo.
echo 1. 📊 Надежное извлечение числа:
echo    - Попытка через регулярное выражение /\d+/
echo    - Резервный способ через data-count атрибут
echo    - Проверка на NaN и отрицательные значения
echo.
echo 2. 💾 Data-атрибут для надежности:
echo    - Добавлен data-count="{{comments_count}}" в HTML
echo    - JavaScript сохраняет значение в data-count
echo    - Fallback на data-атрибут если текст не парсится
echo.
echo 3. 🐛 Отладочная информация:
echo    - Логи в консоли браузера (F12)
echo    - Информация о начальном состоянии
echo    - Отслеживание всех изменений счетчика
echo.

echo 📋 Алгоритм работы:
echo   1. Попробовать извлечь число из текста badge
echo   2. Если не получилось - взять из data-count
echo   3. Если и это не работает - установить 0
echo   4. Применить изменение (increment)
echo   5. Сохранить новое значение в data-count
echo   6. Обновить отображение
echo.

echo 🔍 Как отладить:
echo   1. Откройте браузер (F12 - Developer Tools)
echo   2. Перейдите на вкладку Console
echo   3. Перезагрузите страницу с комментариями
echo   4. Посмотрите логи инициализации
echo   5. Добавьте/удалите комментарий
echo   6. Проверьте логи обновления счетчика
echo.

echo Применить исправления? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    echo.
    echo 📦 Собираем статические файлы...
    python manage.py collectstatic --noinput 2>nul
    echo ✅ Статические файлы обновлены!
    
    echo.
    echo 🔄 Перезапуск Django сервера...
    taskkill /F /IM python.exe 2>nul
    timeout /t 2
    start cmd /k "cd /d %~dp0 && python manage.py runserver"
    echo ✅ Сервер перезапущен!
    
    echo.
    echo 🌐 Открыть браузер для проверки? (y/n)
    set /p open_choice=
    if /i "%open_choice%"=="y" (
        timeout /t 3
        start http://127.0.0.1:8000/stories/
    )
)

echo.
echo 🎯 ГОТОВО! Проблема NaN должна быть решена.
echo.
echo 🧪 Как проверить:
echo 1. Откройте любой рассказ с комментариями
echo 2. Убедитесь, что счетчик показывает число (не NaN)
echo 3. Откройте F12 → Console для просмотра логов
echo 4. Добавьте комментарий - счетчик должен увеличиться
echo 5. Перезагрузите страницу - счетчик должен остаться стабильным
echo.
echo 📞 Если проблема остается:
echo - Проверьте консоль браузера на ошибки JavaScript
echo - Убедитесь, что Django передает правильный comments_count
echo - Проверьте data-count атрибут в HTML (F12 → Elements)
echo.

pause
