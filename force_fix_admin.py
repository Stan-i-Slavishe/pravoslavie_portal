#!/usr/bin/env python
"""
Принудительное исправление настроек админки
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_minimal')
django.setup()

def fix_admin_settings():
    """Принудительное исправление"""
    
    print("🔧 ПРИНУДИТЕЛЬНОЕ ИСПРАВЛЕНИЕ НАСТРОЕК")
    
    try:
        from core.models import SiteSettings
        from django.contrib import admin
        
        # 1. Удаляем все существующие записи
        SiteSettings.objects.all().delete()
        print("🗑️  Очищены старые записи")
        
        # 2. Создаем новую запись с ID=1 (как в модели)
        settings = SiteSettings(
            id=1,  # Принудительно устанавливаем ID=1
            site_name='Добрые истории',
            site_description='Духовные рассказы, книги и аудио для современного человека',
            contact_email='info@dobrye-istorii.ru',
            contact_phone='+7 (800) 123-45-67',
            social_telegram='https://t.me/dobrye_istorii',
            social_youtube='https://www.youtube.com/@dobrye_istorii',
            social_vk='https://vk.com/dobrye_istorii'
        )
        settings.save()
        print(f"✅ Создана запись с ID: {settings.id}")
        
        # 3. Проверяем методы модели
        test_get = SiteSettings.get_settings()
        print(f"✅ Метод get_settings() работает: {test_get.site_name}")
        
        # 4. Проверяем права доступа в админке
        admin_class = admin.site._registry.get(SiteSettings)
        if admin_class:
            print(f"✅ Админ-класс найден: {admin_class.__class__.__name__}")
            
            # Проверяем права
            print(f"   has_add_permission: {admin_class.has_add_permission(None)}")
            print(f"   has_delete_permission: {admin_class.has_delete_permission(None, None)}")
        
        # 5. Проверяем в базе данных напрямую
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT id, site_name FROM core_sitesettings WHERE id=1;")
        result = cursor.fetchone()
        
        if result:
            print(f"✅ Запись в БД подтверждена: ID={result[0]}, Name={result[1]}")
        else:
            print("❌ Запись в БД не найдена!")
            
        # 6. Пересоздаем суперпользователя если нужно
        from django.contrib.auth.models import User
        if not User.objects.filter(is_superuser=True).exists():
            print("⚠️  Создайте суперпользователя: python manage.py createsuperuser --settings=config.settings_minimal")
        
        print("\n🎉 ИСПРАВЛЕНИЕ ЗАВЕРШЕНО!")
        print("Теперь:")
        print("1. Перезапустите сервер")
        print("2. Обновите страницу админки")
        print("3. Настройки сайта должны стать активными")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    fix_admin_settings()
