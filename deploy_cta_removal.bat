@echo off
echo ===========================================
echo 🚀 Деплой: Удаление CTA блока на сервер
echo ===========================================

echo 📝 Добавляем изменения в Git...
git add templates/core/home.html

echo 📝 Создаем коммит...
git commit -m "Убрать всплывающее окно 'Присоединяйтесь к нам' с главной страницы"

echo 📤 Отправляем изменения на GitHub...
git push origin main

echo ✅ Изменения отправлены на GitHub!
echo.
echo 🖥️ Теперь подключитесь к серверу и выполните:
echo ssh root@46.62.167.17
echo cd /var/www/pravoslavie_portal
echo source venv/bin/activate
echo git pull origin main
echo sudo systemctl reload nginx
echo sudo systemctl restart pravoslavie_portal
echo.
echo 🔍 Проверьте результат на: https://your-domain.com
pause
