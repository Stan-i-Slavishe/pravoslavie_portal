import os
import sys
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('E:/pravoslavie_portal')

django.setup()

from django.urls import reverse
from django.test import Client

print("🔍 Проверка URL-ов тегов...")

try:
    # Проверяем список тегов
    tags_url = reverse('core:tags')
    print(f"✅ URL списка тегов: {tags_url}")
    
    # Проверяем детальную страницу тега
    try:
        tag_detail_url = reverse('core:tag_detail', kwargs={'slug': 'test'})
        print(f"✅ URL детали тега: {tag_detail_url}")
    except Exception as e:
        print(f"❌ Ошибка URL детали тега: {e}")
    
    # Проверяем старый URL (должен не работать)
    try:
        old_tag_url = reverse('core:tag', kwargs={'slug': 'test'})
        print(f"⚠️ Старый URL все еще существует: {old_tag_url}")
    except Exception as e:
        print(f"✅ Старый URL 'core:tag' удален: {e}")
    
    # Проверяем доступность страниц
    client = Client()
    
    print("\n🌐 Проверка доступности страниц...")
    
    # Проверяем страницу списка тегов
    response = client.get('/tags/')
    print(f"📄 /tags/ - статус: {response.status_code}")
    if response.status_code != 200:
        print(f"   Ошибка: {response.content.decode()[:200]}...")
    
    # Проверяем несуществующий тег
    response = client.get('/tags/test-tag/')
    print(f"📄 /tags/test-tag/ - статус: {response.status_code}")
    
    print("\n✅ Проверка завершена!")
    
except Exception as e:
    print(f"❌ Общая ошибка: {e}")
    import traceback
    traceback.print_exc()
