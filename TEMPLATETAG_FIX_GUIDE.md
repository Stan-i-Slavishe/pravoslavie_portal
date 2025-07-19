# 🛠️ ИСПРАВЛЕНИЕ ОШИБКИ TEMPLATETAG

## ❌ Проблема:
Django показывает ошибку: `'russian_pluralize' is not a registered tag library`

## ✅ Что я сделал для исправления:

### 1. Создал templatetag в правильном месте:
- ✅ `core/templatetags/__init__.py` (пустой файл)
- ✅ `core/templatetags/russian_pluralize.py` (с функциями склонения)

### 2. Обновил шаблон:
- ✅ Добавил `{% load russian_pluralize %}` 
- ✅ Заменил первый бейдж на `{{ playlist.calculated_stories_count|count_stories }}`

## 📝 Что нужно сделать ВРУЧНУЮ:

### 1. В файле `templates/stories/playlists_list.html` найти еще 2 места:

**НАЙТИ:**
```django
{{ playlist.calculated_stories_count }} рассказов
```

**ЗАМЕНИТЬ НА:**
```django
{{ playlist.calculated_stories_count|count_stories }}
```

### 2. Местоположение этих мест:
- 🎯 Секция "Кастомная обложка" (около строки 399)
- 🎯 Секция "Градиентный фон по умолчанию" (около строки 409)

### 3. ВАЖНО! После исправления:
1. **ПЕРЕЗАПУСТИТЕ Django сервер** (`python manage.py runserver`)
2. Обновите страницу в браузере
3. Ошибка должна исчезнуть

## 📱 Ожидаемый результат:
- `1 рассказ` ✅
- `2 рассказа` ✅ 
- `5 рассказов` ✅
- `21 рассказ` ✅
- `22 рассказа` ✅
- `25 рассказов` ✅

## 🧪 Как работает склонение:
```python
def count_stories(count):
    if count % 10 == 1 and count % 100 != 11:
        return f"{count} рассказ"      # 1, 21, 31, 101, 121...
    elif count % 10 in [2,3,4] and count % 100 not in [12,13,14]:
        return f"{count} рассказа"     # 2, 3, 4, 22, 23, 24...
    else:
        return f"{count} рассказов"    # 5, 6, 7, 11, 12, 13, 14, 15, 20, 25...
```

**После исправления и перезапуска сервера покажите результат!** 🎯
