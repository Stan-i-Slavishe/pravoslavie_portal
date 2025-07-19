# ✅ ПРОСТОЕ ИСПРАВЛЕНИЕ БЕЙДЖЕЙ ПЛЕЙЛИСТОВ

## 🎯 Что нужно сделать:

В файле `templates/stories/playlists_list.html` найти все вхождения:
```django
{{ playlist.calculated_stories_count }}
```

И заменить на:
```django
{{ playlist.calculated_stories_count }} рассказов
```

## 📍 Места для замены:

### 1. YouTube превью (строка ~386):
```django
<!-- Бейдж количества рассказов -->
<div class="playlist-count-badge">
    <i class="bi bi-collection me-1"></i>
    {{ playlist.calculated_stories_count }} рассказов
</div>
```

### 2. Кастомная обложка (строка ~399):
```django
<!-- Бейдж количества рассказов -->
<div class="playlist-count-badge">
    <i class="bi bi-collection me-1"></i>
    {{ playlist.calculated_stories_count }} рассказов
</div>
```

### 3. Градиентный фон по умолчанию (строка ~409):
```django
<!-- Бейдж количества рассказов -->
<div class="playlist-count-badge">
    <i class="bi bi-collection me-1"></i>
    {{ playlist.calculated_stories_count }} рассказов
</div>
```

## 📱 Результат:
После исправления в бейджах будет отображаться:
- `1 рассказов` (временно, до добавления склонений)
- `2 рассказов`
- `5 рассказов`
- `21 рассказов`

Потом мы добавим правильные склонения! 📚
