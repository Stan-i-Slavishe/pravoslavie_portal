@echo off
echo Применяем КОМПАКТНЫЕ исправления для мобильной читалки...
cd /d "E:\pravoslavie_portal"
call .venv\Scripts\activate
python manage.py collectstatic --noinput
echo.
echo =================================
echo ✅ ИСПРАВЛЕНИЯ ПРИМЕНЕНЫ!
echo.
echo Изменения:
echo • Заголовок стал меньше (13px)
echo • Уменьшены отступы верхней панели
echo • Кнопки стали компактнее
echo • Убран конфликт с нижней панелью
echo.
echo 🔄 Перезапустите сервер и обновите страницу
echo =================================
pause
