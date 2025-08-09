#!/usr/bin/env python
"""
Исправление конкретной сказки "Семейные ценности"
"""

import os
import sys
import django

# Добавляем путь к проекту
project_path = 'E:/pravoslavie_portal'
if project_path not in sys.path:
    sys.path.append(project_path)

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product

def fix_specific_fairy_tale():
    """Исправляем конкретную сказку"""
    
    print("🔧 Ищем сказку 'Семейные ценности'...")
    
    # Ищем сказку по названию
    try:
        tale = Product.objects.get(
            title__icontains="Семейные ценности"
        )
        
        print(f"📖 Найдена сказка: {tale.title}")
        print(f"   ID: {tale.id}")
        print(f"   Тип: {tale.product_type}")
        print(f"   Цена: {tale.price}₽")
        print(f"   Активен: {tale.is_active}")
        print(f"   Требует персонализации: {tale.requires_personalization}")
        
        # Исправляем
        if not tale.requires_personalization:
            print("   🔧 ИСПРАВЛЯЕМ: Устанавливаем requires_personalization=True")
            tale.requires_personalization = True
            tale.save()
            print("   ✅ ИСПРАВЛЕНО!")
        else:
            print("   ✅ Уже настроено правильно")
            
        # Проверяем еще раз
        tale.refresh_from_db()
        print(f"\n🔍 ПРОВЕРКА: requires_personalization = {tale.requires_personalization}")
        
    except Product.DoesNotExist:
        print("❌ Сказка не найдена")
        
        # Покажем все сказки
        all_tales = Product.objects.filter(product_type='fairy_tale')
        print(f"\n📚 Все сказки в системе ({all_tales.count()}):")
        for t in all_tales:
            print(f"   - {t.title} (ID: {t.id}) - персонализация: {t.requires_personalization}")
    
    except Product.MultipleObjectsReturned:
        print("⚠️ Найдено несколько сказок с похожим названием")
        
        tales = Product.objects.filter(title__icontains="Семейные ценности")
        for tale in tales:
            print(f"📖 {tale.title} (ID: {tale.id})")
            if not tale.requires_personalization:
                tale.requires_personalization = True
                tale.save()
                print(f"   ✅ Исправлено!")

if __name__ == "__main__":
    fix_specific_fairy_tale()
