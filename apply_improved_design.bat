@echo off
echo 🎨 ПРИМЕНЯЕМ УЛУЧШЕННЫЙ ДИЗАЙН СЧЕТЧИКА СИМВОЛОВ
echo.

echo ✅ Что изменилось:
echo - Счетчик перенесен справа от кнопок (не под полем ввода)
echo - Компактный формат: 0/1000 (без слова "символов")
echo - Адаптивные кнопки и текст для мобильных
echo - Цветовые предупреждения (желтый при 750+, красный при 900+)
echo - На очень маленьких экранах счетчик переносится под кнопки
echo.

echo 📋 Создаем резервную копию...
copy "comments\templates\comments\comments_section.html" "comments\templates\comments\comments_section_backup.html"

echo.
echo 📁 Ищем улучшенный шаблон...
if exist "improved_comments_template.html" (
    echo ✅ Найден улучшенный шаблон
    copy "improved_comments_template.html" "comments\templates\comments\comments_section.html"
    echo ✅ Шаблон заменен
) else (
    echo ❌ Шаблон не найден. Создайте файл из артефакта improved_comments_template
    echo.
    echo 💡 Скопируйте содержимое артефакта в файл:
    echo    improved_comments_template.html
    echo.
    pause
    exit /b 1
)

echo.
echo 📦 Собираем статические файлы...
python manage.py collectstatic --noinput

echo.
echo 🎯 РЕЗУЛЬТАТ:
echo - Счетчик теперь справа от кнопок
echo - Не занимает место под полем ввода
echo - Компактный и аккуратный дизайн
echo - Полностью адаптивен для мобильных
echo.

echo 🚀 Перезапустите сервер:
echo python manage.py runserver
echo.

echo 💡 После перезапуска:
echo 1. Ctrl+Shift+R для перезагрузки
echo 2. Проверьте в мобильном режиме
echo 3. Счетчик должен быть справа от кнопок!
echo.

pause
