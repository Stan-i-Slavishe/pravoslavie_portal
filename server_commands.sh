# Команды для выполнения на продакшен сервере
# После подключения: ssh root@46.62.167.17

# 1. Переходим в директорию проекта
cd /var/www/pravoslavie_portal

# 2. Активируем виртуальное окружение
source venv/bin/activate

# 3. Получаем последние изменения с git
git pull origin main

# 4. Применяем миграции
python manage.py migrate

# 5. Заполняем начальные данные для новых полей
python manage.py shell -c "
from core.models import SiteSettings
settings = SiteSettings.get_settings()
settings.work_hours = 'Пн-Пт: 9:00 - 18:00'
settings.work_hours_note = 'По московскому времени'  
settings.address_city = 'г. Москва'
settings.address_country = 'Россия'
settings.save()
print('✅ Начальные значения установлены')
"

# 6. Собираем статические файлы (если нужно)
python manage.py collectstatic --noinput

# 7. Перезапускаем службы
sudo systemctl reload nginx
sudo systemctl restart pravoslavie_portal

echo "🎉 Деплой завершен!"
echo "Проверьте админку: https://your-domain.com/admin/core/sitesettings/1/change/"
echo "Проверьте контакты: https://your-domain.com/contact/"
