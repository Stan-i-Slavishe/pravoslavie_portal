#!/usr/bin/env python
import os
import sys
import django

# Добавляем путь к проекту
sys.path.append('E:\\pravoslavie_portal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Настраиваем Django
django.setup()

from books.models import Category

print("=== Проверка категорий книг ===\n")

# Получаем все категории
categories = Category.objects.all()

if categories.exists():
    print(f"Найдено категорий: {categories.count()}")
    print("\nСписок категорий:")
    for cat in categories:
        print(f"- {cat.name} (slug: {cat.slug})")
        
    # Проверяем конкретный slug из ошибки
    target_slug = "seriya-sbornikov-iz-prilozheniya-dobryh-istorij"
    try:
        target_category = Category.objects.get(slug=target_slug)
        print(f"\n✅ Категория с slug '{target_slug}' найдена: {target_category.name}")
    except Category.DoesNotExist:
        print(f"\n❌ Категория с slug '{target_slug}' НЕ найдена!")
        print("Возможные причины:")
        print("1. Категория не создана в админке")
        print("2. У категории другой slug")
        
        # Предлагаем похожие slug'и
        similar_categories = Category.objects.filter(slug__icontains="seriya")
        if similar_categories.exists():
            print("\nПохожие категории:")
            for cat in similar_categories:
                print(f"- {cat.name} (slug: {cat.slug})")
        
else:
    print("❌ Категории книг не найдены!")
    print("Нужно создать категории в админке Django")

print("\n=== Конец проверки ===")
