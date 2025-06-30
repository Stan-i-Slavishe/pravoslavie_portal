@echo off
echo 🔧 ПРИНУДИТЕЛЬНАЯ ДИАГНОСТИКА AJAX СИСТЕМЫ
echo.
echo ✅ Добавлена подробная диагностика в шаблон:
echo 1. Проверка загрузки ajax_comments.js
echo 2. Проверка создания AjaxComments класса
echo 3. Проверка переменных USER_ID, STORY_SLUG, CSRF_TOKEN
echo 4. Принудительное создание AJAX системы
echo 5. Проверка формы и обработчиков
echo.

echo 🚀 Сборка статических файлов...
python manage.py collectstatic --noinput

echo.
echo ✅ ДИАГНОСТИКА ГОТОВА!
echo.
echo 🔍 ИНСТРУКЦИЯ ПО ДИАГНОСТИКЕ:
echo 1. Обновите страницу (Ctrl+F5)
echo 2. Откройте DevTools (F12)
echo 3. Перейдите на вкладку Console
echo 4. Посмотрите на сообщения в консоли
echo.
echo 📱 Ожидаемые сообщения в консоли:
echo - "🎯 Проверка AJAX системы..."
echo - "✅ AJAX система принудительно создана!"
echo - "✅ Форма найдена:"
echo.
echo ❌ Если видите ошибки:
echo - "❌ AjaxComments класс не найден!" - проблема с ajax_comments.js
echo - "❌ Форма не найдена!" - проблема с шаблоном
echo.
echo Попробуйте написать комментарий и смотрите на консоль!
echo.
pause
