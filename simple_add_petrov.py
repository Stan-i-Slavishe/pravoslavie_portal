#!/usr/bin/env python
"""
УПРОЩЕННОЕ добавление Петрова поста
"""

import os
import sys
import django

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def create_petrov_fast_simple():
    """Простое создание Петрова поста"""
    try:
        from pwa.models import FastingPeriod
        
        print("⛪ Добавляем Петров пост (упрощенно)...")
        
        # Удаляем старый (если есть)
        FastingPeriod.objects.filter(name='peter_paul_fast').delete()
        
        # Создаем новый
        petrov_fast = FastingPeriod.objects.create(
            name='peter_paul_fast',
            title='Петров пост',
            description='Пост перед днем Петра и Павла',
            
            # ВАЖНО: Смешанный пост
            easter_start_offset=57,  # Начало от Пасхи (после Троицы)
            easter_end_offset=None,  # Конец НЕ от Пасхи
            end_month=7,             # Конец 12 июля  
            end_day=12,
            
            # Правила поста
            fasting_rules={
                'monday': 'strict_fast',
                'tuesday': 'with_fish', 
                'wednesday': 'strict_fast',
                'thursday': 'with_fish',
                'friday': 'strict_fast',
                'saturday': 'with_fish',
                'sunday': 'with_fish'
            },
            
            priority=8,
            is_active=True
        )
        
        print(f"✅ Петров пост создан: {petrov_fast.title}")
        print(f"   ID: {petrov_fast.id}")
        print(f"   Приоритет: {petrov_fast.priority}")
        print(f"   Easter offset: {petrov_fast.easter_start_offset}")
        print(f"   Конец: {petrov_fast.end_month}/{petrov_fast.end_day}")
        
        # Тестируем
        from datetime import date
        test_date = date(2026, 6, 15)
        is_active = petrov_fast.is_active_for_date(test_date)
        print(f"   Тест 15.06.2026: {'✅ Активен' if is_active else '❌ Не активен'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания Петрова поста: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 УПРОЩЕННОЕ ДОБАВЛЕНИЕ ПЕТРОВА ПОСТА")
    print("=" * 50)
    
    if create_petrov_fast_simple():
        print("=" * 50)
        print("🎉 УСПЕШНО!")
        print("🔄 Перезапустите сервер: python manage.py runserver")
        print("📅 Проверьте июнь 2026 в календаре")
    else:
        print("=" * 50)
        print("❌ ОШИБКА! Возможно нужны миграции:")
        print("1. python manage.py makemigrations pwa")
        print("2. python manage.py migrate")
        print("3. Повторите этот скрипт")

if __name__ == "__main__":
    main()
