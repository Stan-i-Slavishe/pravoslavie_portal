# 🔧 Исправление аналитики покупательских намерений

## Проблема
Система аналитики настроена, но данные не собираются, потому что:
1. ❌ JavaScript для отслеживания не подключен везде
2. ❌ Кнопки покупки не имеют data-атрибутов для аналитики
3. ❌ Нет автоматического отслеживания кликов

## ✅ Что уже сделано
1. ✅ Созданы модели аналитики (PurchaseIntent, PopularContent, UserBehavior, EmailSubscription)
2. ✅ Настроены URL и views для API
3. ✅ Создан дашборд аналитики
4. ✅ Создан JavaScript файл analytics.js
5. ✅ Подключен analytics.js в base.html
6. ✅ Обновлен шаблон books/book_detail.html с data-атрибутами

## 🚀 Что нужно сделать

### 1. Обновить другие шаблоны
Добавить data-атрибуты для аналитики в:
- templates/fairy_tales/fairytale_detail.html 
- templates/audio/audio_detail.html
- templates/shop/product_detail.html
- templates/subscriptions/plans.html

### 2. Запустить тест
```bash
python test_analytics.py
```

### 3. Собрать статические файлы
```bash
python manage.py collectstatic --noinput
```

### 4. Запустить сервер и протестировать
```bash
python manage.py runserver
```

Затем:
1. Зайти как admin/admin123
2. Перейти на страницу книги
3. Кликнуть "Купить" несколько раз
4. Открыть дашборд: http://localhost:8000/analytics/dashboard/

## 🎯 Ожидаемый результат

После исправления:
- ✅ Клики на кнопки покупки будут отслеживаться
- ✅ Данные будут появляться в дашборде аналитики  
- ✅ Пользователи с высокой активностью получат предложение подписки
- ✅ Админ увидит статистику намерений покупки

## 📊 Дашборд покажет:
- Количество кликов на "Купить"
- Самый популярный контент
- Пользователей готовых к покупке
- География интереса
- Конверсию по типам контента

## 🔍 Отладка

Если не работает:
1. Проверить консоль браузера (F12) на ошибки JavaScript
2. Убедиться что analytics.js загружается
3. Проверить что сервер возвращает 200 для /analytics/track-purchase-intent/
4. Проверить что data-атрибуты есть на кнопках

## 📱 Примеры data-атрибутов:

```html
<!-- Книга -->
<a href="#" 
   data-analytics-track="true"
   data-content-type="book" 
   data-object-id="1"
   data-button-type="buy">
   Купить книгу
</a>

<!-- Сказка -->
<a href="#" 
   data-analytics-track="true"
   data-content-type="fairy_tale"
   data-object-id="5" 
   data-button-type="read_full">
   Читать полностью
</a>

<!-- Подписка -->
<a href="#"
   data-analytics-track="true" 
   data-content-type="subscription"
   data-object-id="1"
   data-button-type="subscribe">
   Подписаться
</a>
```

Система готова к работе! 🎉
