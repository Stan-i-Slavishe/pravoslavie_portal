@echo off
echo 🔧 Подготовка изменений для деплоя на продакшен...
echo.

echo 📋 Текущий статус git:
git status

echo.
echo 📦 Добавляем все изменения в git:
git add .

echo.
echo 💾 Создаем коммит:
git commit -m "feat: добавлены поля адреса и режима работы в SiteSettings - Добавлены поля work_hours, work_hours_note, address_city, address_country, address_full в модель SiteSettings - Обновлена админка с новыми секциями Время работы и Адрес и местоположение - Обновлен шаблон contact.html для использования данных из БД вместо хардкода - Создана миграция 0003_add_address_work_hours_fields - Добавлены скрипты для применения изменений"

echo.
echo 🚀 Отправляем на сервер:
git push origin main

echo.
echo ✅ Локальные изменения отправлены!
echo.
echo 🌐 Теперь выполните команды на сервере:
echo.
echo ssh root@46.62.167.17
echo cd /var/www/pravoslavie_portal  
echo source venv/bin/activate
echo git pull origin main
echo python manage.py migrate
echo python manage.py shell -c "from core.models import SiteSettings; settings = SiteSettings.get_settings(); settings.work_hours = 'Пн-Пт: 9:00 - 18:00'; settings.work_hours_note = 'По московскому времени'; settings.address_city = 'г. Москва'; settings.address_country = 'Россия'; settings.save(); print('✅ Начальные значения установлены')"
echo sudo systemctl reload nginx
echo sudo systemctl restart pravoslavie_portal
echo.
pause
