# 🛠️ РЕШЕНИЕ ПРОБЛЕМЫ С БЕСПЛАТНЫМИ ТОВАРАМИ В МАГАЗИНЕ

## 🎯 Проблема
После изменения кода бесплатная книга "Яндекс директ" все еще отображается в магазине, несмотря на добавленный фильтр `price__gt=0`.

## 🔍 Причина
В базе данных уже существуют товары с `price=0`, которые были созданы ранее. Изменение фильтра в коде не удаляет существующие записи из БД.

## ✅ Решения

### Решение 1: Django Management команда (рекомендуется)
```bash
python manage.py clean_free_products
```

### Решение 2: Батник для Windows
```bash
clean_free_products.bat
```

### Решение 3: Python скрипт
```bash
python clean_free_products.py
```

### Решение 4: Ручная очистка через Django shell
```bash
python manage.py shell
```

Затем в shell:
```python
from shop.models import Product

# Показать все бесплатные товары
free_products = Product.objects.filter(price=0)
print(f"Найдено бесплатных товаров: {free_products.count()}")
for p in free_products:
    print(f"- {p.title}: {p.price}₽")

# Деактивировать бесплатные товары
free_products.update(is_active=False)

# Или полностью удалить
# free_products.delete()

# Проверить результат
remaining = Product.objects.filter(is_active=True, price=0)
print(f"Осталось активных бесплатных товаров: {remaining.count()}")
```

### Решение 5: SQL запрос (для продвинутых)
```sql
-- Деактивировать бесплатные товары
UPDATE shop_product SET is_active = FALSE WHERE price = 0;

-- Или удалить полностью
-- DELETE FROM shop_product WHERE price = 0;
```

## 🚀 Рекомендуемые шаги

### 1. Запустите команду очистки:
```bash
python manage.py clean_free_products
```

### 2. Перезапустите сервер:
```bash
python manage.py runserver
```

### 3. Проверьте магазин:
- Откройте `http://127.0.0.1:8000/shop/`
- Убедитесь, что бесплатных товаров нет

### 4. Проверьте библиотеку:
- Откройте `http://127.0.0.1:8000/books/`  
- Убедитесь, что бесплатные книги доступны

## 📊 Что делают команды очистки

### 🔍 Анализ:
- Находят все товары с `price = 0`
- Показывают список для проверки
- Считают количество

### 🛠️ Действия:
- **По умолчанию:** деактивируют (`is_active = False`)
- **С флагом --delete:** полностью удаляют из БД

### 📈 Статистика:
- Показывают итоговое количество товаров
- Выводят список активных платных товаров

## 🔧 Автоматическая синхронизация

### Сигналы уже настроены:
В `shop/signals.py` есть логика, которая:
- ✅ Создает товары только для платных книг (`price > 0`)
- ✅ Деактивирует товары, если книга становится бесплатной
- ✅ Автоматически синхронизирует при изменениях

### Будущие книги:
Новые бесплатные книги НЕ будут попадать в магазин автоматически.

## 🎯 Проверочный чек-лист

### После очистки убедитесь:
- [ ] В магазине нет товаров с ценой 0₽
- [ ] Все товары в магазине платные
- [ ] Бесплатные книги доступны в библиотеке
- [ ] Фильтры в магазине работают корректно
- [ ] Поиск находит только платные товары

## 🔄 Если проблема повторится

### Причины:
1. **Кеширование Django** - перезапустите сервер
2. **Кеширование браузера** - обновите страницу (Ctrl+F5)  
3. **Новые бесплатные товары** - запустите очистку повторно

### Диагностика:
```python
# В Django shell
from shop.models import Product
Product.objects.filter(is_active=True).values('title', 'price')
```

## 📝 Дополнительные команды

### Показать все товары:
```bash
python manage.py shell -c "
from shop.models import Product
for p in Product.objects.all():
    print(f'{p.title}: {p.price}₽ (активен: {p.is_active})')
"
```

### Статистика товаров:
```bash
python manage.py shell -c "
from shop.models import Product
from django.db.models import Count
stats = Product.objects.aggregate(
    total=Count('id'),
    active=Count('id', filter=models.Q(is_active=True)),
    paid=Count('id', filter=models.Q(is_active=True, price__gt=0)),
    free=Count('id', filter=models.Q(is_active=True, price=0))
)
print('Статистика товаров:', stats)
"
```

---

## 🎉 Заключение

**После выполнения любого из решений бесплатные товары исчезнут из магазина, но останутся доступными в соответствующих разделах (библиотека, сказки, аудио).**

**Выберите наиболее удобный способ и выполните очистку!** 🧹✨