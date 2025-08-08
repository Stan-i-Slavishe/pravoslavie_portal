import os
import sys
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('E:/pravoslavie_portal')

django.setup()

from django.urls import reverse

print("🔍 Проверка всех URL namespaces...")

# Список namespaces для проверки
namespaces_to_check = [
    ('stories:list', 'Видео-рассказы'),
    ('books:list', 'Библиотека'),
    ('audio:list', 'Аудио'),
    ('fairy_tales:list', 'Сказки'),
    ('shop:list', 'Магазин'),
    ('core:tags', 'Теги'),
    ('core:categories', 'Категории'),
]

for url_name, description in namespaces_to_check:
    try:
        url = reverse(url_name)
        print(f"✅ {description}: {url_name} -> {url}")
    except Exception as e:
        print(f"❌ {description}: {url_name} -> ОШИБКА: {e}")

print("\n🎯 Исправлены URL в tag_detail.html:")
print("   'fairy-tales:list' -> 'fairy_tales:list'")
print("\n🚀 Теперь страница тегов должна работать без ошибок!")
