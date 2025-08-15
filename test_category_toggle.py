#!/usr/bin/env python3
"""
Тестирование функциональности переключения категорий
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from fairy_tales.models import FairyTaleCategory, AgeGroup


def test_categories_display():
    """Тестирование отображения категорий"""
    
    print("🧚 Тестирование системы переключения категорий")
    print("=" * 50)
    
    # Получаем все активные категории
    categories = FairyTaleCategory.objects.filter(is_active=True).order_by('age_group', 'order', 'name')
    total_categories = categories.count()
    
    print(f"📊 Общее количество категорий: {total_categories}")
    
    # Показываем первые 5 категорий (всегда видимые)
    visible_categories = categories[:5]
    hidden_categories = categories[5:]
    
    print(f"👁️  Всегда видимые категории: {len(visible_categories)}")
    for i, cat in enumerate(visible_categories, 1):
        print(f"   {i}. {cat.name} ({cat.get_age_group_display()}) - {cat.icon}")
    
    print(f"🔒 Скрытые категории: {len(hidden_categories)}")
    for i, cat in enumerate(hidden_categories, 1):
        print(f"   {i}. {cat.name} ({cat.get_age_group_display()}) - {cat.icon}")
    
    # Тестируем логику кнопки
    if len(hidden_categories) > 0:
        print(f"\n✅ Кнопка 'Показать все категории' будет отображена")
        print(f"📈 Счетчик покажет: +{len(hidden_categories)}")
    else:
        print(f"\n❌ Кнопка 'Показать все категории' НЕ будет отображена")
    
    print("\n" + "=" * 50)
    print("📱 Тестирование шаблонной логики:")
    print(f"categories|slice:':5' = {[c.name for c in categories[:5]]}")
    print(f"categories|slice:'5:' = {[c.name for c in categories[5:]]}")
    print(f"categories|length = {total_categories}")
    print(f"categories|length|add:'-5' = {total_categories - 5}")
    
    return True


def create_test_categories_if_needed():
    """Создает тестовые категории если их мало"""
    
    existing_count = FairyTaleCategory.objects.filter(is_active=True).count()
    
    if existing_count < 8:
        print(f"🔨 Создаем дополнительные тестовые категории (текущее количество: {existing_count})")
        
        test_categories = [
            {
                'name': 'Преодоление страхов',
                'description': 'Сказки для помощи детям в преодолении различных страхов',
                'age_group': AgeGroup.CHILD,
                'icon': 'shield-check',
                'color': '#e74c3c'
            },
            {
                'name': 'Повышение уверенности',
                'description': 'Истории для развития уверенности в себе',
                'age_group': AgeGroup.CHILD,
                'icon': 'star',
                'color': '#f39c12'
            },
            {
                'name': 'Семейные отношения',
                'description': 'Сказки о важности семьи и взаимопонимания',
                'age_group': AgeGroup.FAMILY,
                'icon': 'house-heart',
                'color': '#2ecc71'
            },
            {
                'name': 'Управление эмоциями',
                'description': 'Помощь в понимании и контроле эмоций',
                'age_group': AgeGroup.CHILD,
                'icon': 'emoji-smile',
                'color': '#9b59b6'
            },
            {
                'name': 'Духовные добродетели',
                'description': 'Православные сказки о добродетелях',
                'age_group': AgeGroup.FAMILY,
                'icon': 'church',
                'color': '#3498db'
            },
            {
                'name': 'Развитие терпения',
                'description': 'Сказки о важности терпения и настойчивости',
                'age_group': AgeGroup.CHILD,
                'icon': 'hourglass',
                'color': '#1abc9c'
            },
            {
                'name': 'Воспитание доброты',
                'description': 'Истории о сострадании и помощи ближним',
                'age_group': AgeGroup.CHILD,
                'icon': 'heart',
                'color': '#e91e63'
            },
            {
                'name': 'Благодарность',
                'description': 'Сказки о важности быть благодарным',
                'age_group': AgeGroup.FAMILY,
                'icon': 'gift',
                'color': '#ff9800'
            }
        ]
        
        created_count = 0
        for cat_data in test_categories:
            category, created = FairyTaleCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                created_count += 1
                print(f"  ✅ Создана категория: {category.name}")
        
        print(f"🎉 Создано {created_count} новых категорий")
        return created_count
    
    return 0


if __name__ == "__main__":
    try:
        print("🚀 Запуск тестирования функциональности переключения категорий\n")
        
        # Создаем тестовые категории если нужно
        create_test_categories_if_needed()
        
        print()
        
        # Тестируем отображение
        test_categories_display()
        
        print("\n🎯 Рекомендации для тестирования:")
        print("1. Запустите сервер: python manage.py runserver")
        print("2. Перейдите на: http://127.0.0.1:8000/fairy-tales/")
        print("3. Проверьте:")
        print("   - Отображаются ли первые 5 категорий")
        print("   - Есть ли кнопка 'Показать все категории'")
        print("   - Работает ли анимация разворачивания")
        print("   - Корректно ли работает на мобильных устройствах")
        
        print("\n✅ Тестирование завершено успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
