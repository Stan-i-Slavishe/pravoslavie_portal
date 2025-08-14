#!/usr/bin/env python
"""
Проверка корректности восстановления терапевтических сказок
"""

import os
import sys
import django

# Настраиваем Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def check_fairy_tales_system():
    """Проверяет корректность системы сказок"""
    
    print("🔍 Проверка системы терапевтических сказок...")
    print("=" * 50)
    
    try:
        from fairy_tales.models import FairyTaleCategory, FairyTaleTemplate
        from django.urls import reverse
        
        # Проверка моделей
        categories_count = FairyTaleCategory.objects.count()
        tales_count = FairyTaleTemplate.objects.count()
        published_tales = FairyTaleTemplate.objects.filter(is_published=True).count()
        free_tales = FairyTaleTemplate.objects.filter(is_free=True, is_published=True).count()
        
        print(f"📂 Категорий: {categories_count}")
        print(f"📖 Всего сказок: {tales_count}")
        print(f"✅ Опубликованных: {published_tales}")
        print(f"🆓 Бесплатных: {free_tales}")
        print(f"💰 Платных: {published_tales - free_tales}")
        
        # Проверка URL-ов
        print("\n🌐 Проверка URL-маршрутов:")
        urls_to_check = [
            ('fairy_tales:list', 'Главная страница сказок'),
            ('fairy_tales:categories', 'Список категорий'),
        ]
        
        for url_name, description in urls_to_check:
            try:
                url = reverse(url_name)
                print(f"  ✅ {description}: {url}")
            except Exception as e:
                print(f"  ❌ {description}: ОШИБКА - {e}")
        
        # Проверка категорий
        print("\n📁 Категории сказок:")
        for category in FairyTaleCategory.objects.all():
            tales_in_category = category.templates.filter(is_published=True).count()
            print(f"  📂 {category.name} ({category.get_age_group_display()}): {tales_in_category} сказок")
        
        # Проверка сказок
        print("\n📚 Созданные сказки:")
        for tale in FairyTaleTemplate.objects.filter(is_published=True):
            status = "🆓" if tale.is_free else f"💰 {tale.base_price}₽"
            featured = " ⭐" if tale.featured else ""
            print(f"  {status} {tale.title} ({tale.age_range_display}){featured}")
        
        print("\n" + "=" * 50)
        print("🎉 СИСТЕМА ТЕРАПЕВТИЧЕСКИХ СКАЗОК УСПЕШНО ВОССТАНОВЛЕНА!")
        print("\n🌟 Доступные страницы:")
        print("   📖 Каталог сказок: http://127.0.0.1:8000/fairy-tales/")
        print("   📂 Категории: http://127.0.0.1:8000/fairy-tales/categories/")
        print("   📋 Заглушка (старая): http://127.0.0.1:8000/fairy-tales/coming-soon/")
        
        if published_tales > 0:
            print("\n✨ Рекомендация: Перейдите на /fairy-tales/ и посмотрите результат!")
        else:
            print("\n⚠️  Рекомендация: Запустите setup_fairy_tales.bat для добавления тестовых данных")
            
    except Exception as e:
        print(f"❌ ОШИБКА при проверке: {e}")
        print("\n🔧 Попробуйте:")
        print("   1. python manage.py makemigrations fairy_tales")
        print("   2. python manage.py migrate")
        print("   3. python add_test_fairy_tales.py")

if __name__ == '__main__':
    check_fairy_tales_system()
