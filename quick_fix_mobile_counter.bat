@echo off
echo 🔧 Быстрое исправление мобильного счетчика комментариев...
echo.

echo ✅ CSS обновлен в static/stories/css/ajax_comments.css
echo.

echo 📝 Теперь нужно обновить JavaScript в шаблоне комментариев...
echo.

echo 🔍 Найти функцию updateCharCounter() в comments_section.html
echo 💡 Заменить на умную логику показа счетчика
echo.

echo 📋 Что нужно изменить в JavaScript:
echo.
echo function updateCharCounter() {
echo     const length = commentText.value.length;
echo     charCounter.textContent = length;
echo     
echo     // Умная логика - показываем только когда нужно
echo     const counterWrapper = charCounter.parentElement;
echo     
echo     if (length ^> 850^) {
echo         counterWrapper.style.display = 'block';
echo         counterWrapper.classList.remove('warning', 'danger'^);
echo         
echo         if (length ^> 950^) {
echo             counterWrapper.classList.add('danger'^);
echo         } else if (length ^> 900^) {
echo             counterWrapper.classList.add('warning'^);
echo         }
echo     } else {
echo         counterWrapper.style.display = 'none';
echo     }
echo }
echo.

echo 🔄 Для применения изменений:
echo 1. python manage.py collectstatic --noinput
echo 2. Перезапустить сервер
echo 3. Очистить кеш браузера (Ctrl+F5)
echo.

echo ✨ После исправления счетчик будет:
echo - Скрыт до 850 символов
echo - Желтый при 900+ символах  
echo - Красный при 950+ символах
echo - Компактный на мобильных
echo.

pause
