import os
import django
from django.core import serializers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local')
django.setup()

from stories.models import Story
from core.models import Tag, Category

# Получаем все объекты
categories = Category.objects.all()
tags = Tag.objects.all()
stories = Story.objects.all()

print(f"Найдено категорий: {categories.count()}")
print(f"Найдено тегов: {tags.count()}")
print(f"Найдено рассказов: {stories.count()}")

# Создаем список всех объектов для сериализации
all_objects = list(categories) + list(tags) + list(stories)

# Сериализуем все объекты в один JSON
serialized_data = serializers.serialize('json', all_objects, indent=2)

# Записываем в файл с явной UTF-8 кодировкой
with open('stories_manual.json', 'w', encoding='utf-8') as f:
    f.write(serialized_data)

print("Файл stories_manual.json создан с UTF-8 кодировкой")
