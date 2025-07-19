# ✅ ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ СКЛОНЕНИЙ

## 🎯 Что уже сделано:
- ✅ Создан templatetag `russian_pluralize.py` для правильного склонения
- ✅ Добавлен `{% load russian_pluralize %}` в шаблон
- ✅ Исправлен первый бейдж (YouTube превью) - использует `{% pluralize_stories %}`

## 📝 Что осталось исправить ВРУЧНУЮ:

Найдите в файле `templates/stories/playlists_list.html` эти **2 блока** и замените:

### 1. Кастомная обложка (около строки 399):
**НАЙТИ:**
```django
<!-- Бейдж количества рассказов -->
<div class="playlist-count-badge">
    <i class="bi bi-collection me-1"></i>
    {{ playlist.calculated_stories_count }} рассказов
</div>
```

**ЗАМЕНИТЬ НА:**
```django
<!-- Бейдж количества рассказов -->
<div class="playlist-count-badge">
    <i class="bi bi-collection me-1"></i>
    {% pluralize_stories playlist.calculated_stories_count %}
</div>
```

### 2. Градиентный фон по умолчанию (около строки 409):
**НАЙТИ:**
```django
<!-- Бейдж количества рассказов -->
<div class="playlist-count-badge">
    <i class="bi bi-collection me-1"></i>
    {{ playlist.calculated_stories_count }} рассказов
</div>
```

**ЗАМЕНИТЬ НА:**
```django
<!-- Бейдж количества рассказов -->
<div class="playlist-count-badge">
    <i class="bi bi-collection me-1"></i>
    {% pluralize_stories playlist.calculated_stories_count %}
</div>
```

## 📱 После исправления будет отображаться:
- `📹 1 рассказ` ✅
- `📹 2 рассказа` ✅
- `📹 5 рассказов` ✅
- `📹 21 рассказ` ✅
- `📹 22 рассказа` ✅
- `📹 25 рассказов` ✅

## 🧪 Как работает склонение:
```python
def pluralize_stories(count):
    if count % 10 == 1 and count % 100 != 11:
        return f"{count} рассказ"      # 1, 21, 31, 101, 121...
    elif count % 10 in [2,3,4] and count % 100 not in [12,13,14]:
        return f"{count} рассказа"     # 2, 3, 4, 22, 23, 24...
    else:
        return f"{count} рассказов"    # 5, 6, 7, 11, 12, 13, 14, 15, 20, 25...
```

**После исправления покажите скриншот!** 🎯
