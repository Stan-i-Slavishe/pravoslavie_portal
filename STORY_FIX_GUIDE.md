# 🚀 Пошаговое исправление ошибок видео-рассказов

## Проблемы, которые мы исправляем:

1. **TemplateSyntaxError**: неправильный `{% endblock %}` в шаблоне
2. **AttributeError**: отсутствует `youtube_embed_id` у некоторых рассказов  
3. **Видео не отображается**: пустые YouTube ID

## 📋 Шаги исправления:

### Шаг 1: Исправление шаблона ✅ ГОТОВО
Шаблон `templates/stories/story_detail.html` уже исправлен!

### Шаг 2: Исправление данных в базе

Выполните следующие команды:

```bash
# 1. Активируйте виртуальное окружение (если есть)
.venv\Scripts\activate

# 2. Откройте Django shell
python manage.py shell

# 3. Выполните в shell:
```

```python
from stories.models import Story
import re

def extract_youtube_id(url):
    """Извлекает YouTube ID из URL"""
    if not url:
        return None
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/v\/([^&\n?#]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

# Исправляем проблемный рассказ
try:
    story = Story.objects.get(slug='kak-svyatoj-luka-doch-spas')
    print(f"✅ Найден: {story.title}")
    
    if story.youtube_url and not story.youtube_embed_id:
        youtube_id = extract_youtube_id(story.youtube_url)
        if youtube_id:
            story.youtube_embed_id = youtube_id
            story.save(update_fields=['youtube_embed_id'])
            print(f"✅ YouTube ID установлен: {youtube_id}")
        else:
            print("❌ Не удалось извлечь ID из URL")
    elif not story.youtube_url:
        # Устанавливаем тестовое видео для демонстрации
        story.youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        story.youtube_embed_id = "dQw4w9WgXcQ"
        story.save(update_fields=['youtube_url', 'youtube_embed_id'])
        print("🧪 Установлено тестовое видео")
    else:
        print(f"✅ Видео уже настроено: {story.youtube_embed_id}")
        
except Story.DoesNotExist:
    print("❌ Рассказ не найден")

# Исправляем ВСЕ рассказы без YouTube ID
print("\n🔧 Исправляем все рассказы...")
stories_fixed = 0
total_stories = Story.objects.count()

for story in Story.objects.filter(youtube_embed_id__isnull=True):
    if story.youtube_url:
        youtube_id = extract_youtube_id(story.youtube_url)
        if youtube_id:
            story.youtube_embed_id = youtube_id
            story.save(update_fields=['youtube_embed_id'])
            stories_fixed += 1
            print(f"✅ {story.title}: {youtube_id}")

# Исправляем рассказы с пустыми YouTube ID
for story in Story.objects.filter(youtube_embed_id=''):
    if story.youtube_url:
        youtube_id = extract_youtube_id(story.youtube_url)
        if youtube_id:
            story.youtube_embed_id = youtube_id
            story.save(update_fields=['youtube_embed_id'])
            stories_fixed += 1
            print(f"✅ {story.title}: {youtube_id}")

print(f"\n🎉 Исправлено {stories_fixed} из {total_stories} рассказов")

# Показываем статистику
stories_with_video = Story.objects.exclude(youtube_embed_id__isnull=True).exclude(youtube_embed_id='').count()
stories_without_video = Story.objects.filter(youtube_embed_id__isnull=True).count() + Story.objects.filter(youtube_embed_id='').count()

print(f"📊 Статистика:")
print(f"   ✅ С видео: {stories_with_video}")
print(f"   ❌ Без видео: {stories_without_video}")
```

### Шаг 3: Перезапуск сервера

```bash
# Выйдите из Django shell
exit()

# Перезапустите сервер
python manage.py runserver
```

### Шаг 4: Проверка

Откройте в браузере:
- http://127.0.0.1:8000/stories/kak-svyatoj-luka-doch-spas/
- Любой другой рассказ

**Что должно работать:**
- ✅ Страница загружается без ошибок
- ✅ Видео отображается или показывается заглушка
- ✅ Все метаданные отображаются корректно
- ✅ Кнопки лайков и поделиться работают

## 🚨 Если проблемы остались:

### Проблема: Рассказ не найден
```python
# В Django shell создайте тестовый рассказ:
from stories.models import Story

test_story = Story.objects.create(
    title="Тестовый рассказ",
    slug="test-story-fix",
    description="Рассказ для тестирования исправлений",
    youtube_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    youtube_embed_id="dQw4w9WgXcQ"
)
print(f"✅ Создан тестовый рассказ: {test_story.get_absolute_url()}")
```

### Проблема: URL не найден (404)
Проверьте файл `stories/urls.py`:
```python
# Должна быть строка вида:
path('<slug:slug>/', views.story_detail, name='detail'),
```

### Проблема: Ошибки в шаблоне
Убедитесь, что файл `templates/stories/story_detail.html` заменён исправленной версией.

## 🎉 После исправления

Все рассказы должны:
- Загружаться без ошибок
- Показывать видео или красивую заглушку
- Иметь правильные метаданные
- Поддерживать лайки и социальные кнопки

**Готово! Ваш сайт должен работать корректно.**
