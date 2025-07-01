@echo off
chcp 65001 >nul
echo ===== УЛУЧШЕНИЕ КНОПКИ ЗАКРЫТИЯ =====
echo.

echo Что было улучшено:
echo.
echo 1. ДИЗАЙН КНОПКИ:
echo    - Круглая форма (border-radius: 50%%)
echo    - Серый фон с легкой тенью
echo    - Центрированная иконка X
echo    - Размер 32x32 пикселя
echo.
echo 2. ИНТЕРАКТИВНОСТЬ:
echo    - Увеличение при наведении (scale: 1.1)
echo    - Поворот иконки на 90 градусов при hover
echo    - Плавные анимации (transition: 0.2s)
echo    - Эффект нажатия (scale: 0.95)
echo.
echo 3. УДОБСТВО:
echo    - Легко нажимается на мобильных
echo    - Интуитивно понятное поведение
echo    - Aria-label для доступности
echo    - Визуальная обратная связь
echo.
echo 4. СТИЛИ:
echo    - Нейтральные цвета
echo    - Современный Material Design
echo    - Соответствует общему дизайну
echo    - Профессиональный вид
echo.

echo Доступные альтернативные стили:
echo - Минималистичная (прозрачная)
echo - Красная (опасная)
echo - Темная (элегантная)
echo - Градиентная (современная)
echo - Пульсирующая (анимированная)
echo.

echo Применить улучшения? (y/n)
set /p choice=
if /i "%choice%"=="y" (
    echo.
    echo Собираем статические файлы...
    python manage.py collectstatic --noinput 2>nul
    echo Статические файлы обновлены!
    
    echo.
    echo Перезапуск Django сервера...
    taskkill /F /IM python.exe 2>nul
    timeout /t 2
    start cmd /k "cd /d %~dp0 && python manage.py runserver"
    echo Сервер перезапущен!
    
    echo.
    echo Открыть браузер для проверки? (y/n)
    set /p open_choice=
    if /i "%open_choice%"=="y" (
        timeout /t 3
        start http://127.0.0.1:8000/stories/
    )
)

echo.
echo ГОТОВО! Кнопка закрытия стала намного стильнее!
echo.
echo Как проверить:
echo 1. Откройте сайт на мобильном устройстве
echo 2. Нажмите "Добавить комментарий"
echo 3. Посмотрите на кнопку X в правом верхнем углу
echo 4. Наведите курсор - кнопка увеличится
echo 5. Иконка повернется на 90 градусов
echo 6. Нажмите - кнопка сожмется и форма закроется
echo.
echo Технические особенности:
echo - border-radius: 50%% - круглая форма
echo - transform: scale() - увеличение/уменьшение
echo - transform: rotate() - поворот иконки
echo - box-shadow - красивая тень
echo - transition: all 0.2s ease - плавные анимации
echo.
echo Для смены стиля:
echo Замените "btn-close-custom" на один из вариантов:
echo - btn-close-minimal (прозрачная)
echo - btn-close-danger (красная)
echo - btn-close-dark (темная)
echo - btn-close-gradient (градиентная)
echo - btn-close-pulse (пульсирующая)
echo.
echo Файл с альтернативными стилями: alternative_close_button_styles.css

pause
