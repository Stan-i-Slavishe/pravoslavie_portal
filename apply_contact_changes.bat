@echo off
echo 🔧 Применяем изменения для полей адреса и режима работы...
echo.

echo 📦 Применение миграции...
python manage.py migrate

echo.
echo 📝 Заполнение начальных значений...
python -c "
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import SiteSettings
settings = SiteSettings.get_settings()

# Устанавливаем значения по умолчанию
if not settings.work_hours:
    settings.work_hours = 'Пн-Пт: 9:00 - 18:00'
    settings.work_hours_note = 'По московскому времени'
    settings.address_city = 'г. Москва'
    settings.address_country = 'Россия'
    settings.save()
    print('✅ Начальные значения установлены')
else:
    print('✅ Значения уже существуют')
"

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
