@echo off
echo 🔧 Применяем изменения для полей адреса и режима работы...
echo.

echo 📦 Применение миграции...
python manage.py migrate

echo.
echo 📝 Заполнение начальных значений...
python manage.py shell -c "from core.models import SiteSettings; settings = SiteSettings.get_settings(); settings.work_hours = 'Пн-Пт: 9:00 - 18:00' if not settings.work_hours else settings.work_hours; settings.work_hours_note = 'По московскому времени' if not settings.work_hours_note else settings.work_hours_note; settings.address_city = 'г. Москва' if not settings.address_city else settings.address_city; settings.address_country = 'Россия' if not settings.address_country else settings.address_country; settings.save(); print('✅ Начальные значения установлены')"

echo.
echo 🎉 Все изменения успешно применены!
echo.
echo 📋 Что изменилось:
echo    ✅ Добавлены поля в модель SiteSettings
echo    ✅ Обновлена админка с новыми секциями
echo    ✅ Шаблон контактов теперь использует данные из БД
echo.
echo 🚀 Теперь вы можете:
echo    1. Запустить сервер: python manage.py runserver
echo    2. Зайти в админку: http://127.0.0.1:8000/admin/
echo    3. Перейти в 'Настройки сайта'
echo    4. Изменить время работы и адрес
echo.
pause
