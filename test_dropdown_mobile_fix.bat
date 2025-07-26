@echo off
echo ==================================================
echo  ТЕСТИРОВАНИЕ ИСПРАВЛЕНИЯ DROPDOWN В МОБИЛЬНОЙ ВЕРСИИ
echo ==================================================
echo.
echo [1] Исправлены дублирующиеся ID dropdown:
echo     - sectionsDropdown для меню "Разделы"
echo     - userDropdown для пользовательского меню
echo.
echo [2] Добавлен JavaScript для управления dropdown:
echo     - Закрытие всех dropdown при открытии нового
echo     - Закрытие при клике вне области
echo     - Закрытие при изменении размера экрана
echo.
echo [3] Добавлены CSS стили:
echo     - dropdown-mobile-enhancement.css
echo     - Правильные z-index для наложения
echo     - Анимации открытия/закрытия
echo     - Адаптивность для разных экранов
echo.
echo [4] Что изменилось в base.html:
echo     - Исправлены ID dropdown элементов
echo     - Добавлен JavaScript для управления
echo     - Подключен новый CSS файл
echo.
echo ==================================================
echo  ИНСТРУКЦИЯ ПО ТЕСТИРОВАНИЮ:
echo ==================================================
echo.
echo 1. Откройте сайт в браузере
echo 2. Переключитесь в мобильный режим (F12 -> устройства)
echo 3. Откройте меню "Разделы"
echo 4. Затем откройте пользовательское меню
echo 5. Убедитесь, что меню "Разделы" закрылось
echo 6. Пользовательское меню должно быть поверх всего
echo.
echo ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:
echo - При открытии одного dropdown другой закрывается
echo - Пользовательское меню всегда поверх меню "Разделы"
echo - Плавные анимации открытия/закрытия
echo - Клик вне области закрывает все dropdown
echo.
echo ==================================================
echo.

echo Запускаем сервер для тестирования...
cd /d "%~dp0"

:: Активируем виртуальное окружение
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo Виртуальное окружение не найдено!
    pause
    exit /b 1
)

:: Проверяем наличие файлов
if not exist "templates\base.html" (
    echo ОШИБКА: templates\base.html не найден!
    pause
    exit /b 1
)

if not exist "static\css\dropdown-mobile-enhancement.css" (
    echo ОШИБКА: dropdown-mobile-enhancement.css не найден!
    pause
    exit /b 1
)

echo.
echo ✅ Все файлы найдены, запускаем сервер...
echo.
echo После запуска откройте: http://127.0.0.1:8000
echo.
echo Для тестирования мобильной версии:
echo 1. Нажмите F12 в браузере
echo 2. Выберите "Toggle device toolbar" (Ctrl+Shift+M)
echo 3. Выберите устройство (например, iPhone SE)
echo 4. Протестируйте dropdown меню
echo.

python manage.py runserver 0.0.0.0:8000

pause
