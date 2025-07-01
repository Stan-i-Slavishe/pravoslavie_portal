@echo off
chcp 65001 >nul
echo ✅ УСПЕШНЫЙ ОТКАТ К КОММИТУ 931402d
echo ====================================

echo 📍 Текущий коммит: 931402d (norm_koment)
echo 🔄 HEAD установлен на этот коммит
echo.

echo 📊 Проверяем статус...
git log --oneline -3

echo.
echo 🔧 Обновляем статические файлы...
python manage.py collectstatic --noinput --clear

echo 🚀 Перезапускаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 3 /nobreak >nul

echo ✨ Запускаем сервер с откатанной версией...
start python manage.py runserver

echo.
echo 🎯 ОТКАТ ЗАВЕРШЕН!
echo.
echo 📍 Откройте: http://127.0.0.1:8000/stories/malishka/
echo 📝 Должна вернуться рабочая версия статистики
echo.
echo 💡 Если все работает:
echo    - Статистика комментариев должна отображаться
echo    - Метаданные под заголовком должны быть видны
echo    - Боковая панель должна работать корректно
echo.
echo 🔄 Если нужно вернуться к последним изменениям:
echo    git checkout main
echo    (или git checkout master)
echo.
pause
