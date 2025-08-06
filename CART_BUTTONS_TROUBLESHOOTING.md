# 🔧 Попытки исправления горизонтального отображения кнопок +/-

## 🎯 Цель
Сделать кнопки "+" и "-" для управления количеством товаров в одну горизонтальную линию.

## 🔄 Попытки исправления

### 1. **CSS стили с !important**
- Добавили CSS с принудительным flexbox
- Использовали !important для переопределения Bootstrap
- Результат: не сработало

### 2. **Bootstrap flexbox утилиты (d-flex)**
- Заменили input-group на d-flex
- Использовали align-items-center и justify-content-center
- Результат: не сработало

### 3. **HTML таблица для принудительного горизонтального размещения**
- Использовали <table> с тремя <td> элементами
- Убрали отступы и правильно настроили границы
- Результат: должно сработать

## 🧪 Текущее решение (Попытка #3)

```html
<table style="margin: 0 auto; border-collapse: collapse;" data-item-id="{{ item.id }}">
    <tr>
        <td style="padding: 0;">
            <button class="btn btn-outline-secondary btn-sm decrease-btn">[-]</button>
        </td>
        <td style="padding: 0;">
            <input class="form-control text-center quantity-input" value="1">
        </td>
        <td style="padding: 0;">
            <button class="btn btn-outline-secondary btn-sm increase-btn">[+]</button>
        </td>
    </tr>
</table>
```

## 🔍 Возможные причины проблемы

1. **Кеширование CSS** - браузер может кешировать старые стили
2. **Конфликт с Bootstrap CSS** - Bootstrap может принудительно переопределять стили
3. **Мобильный режим** - возможно, Bootstrap применяет мобильные стили
4. **Порядок загрузки CSS** - возможно, Bootstrap загружается после наших стилей

## 🚀 Следующие шаги для диагностики

1. **Жесткое обновление** браузера (Ctrl+F5)
2. **Проверка в инструментах разработчика** (F12 → Elements)
3. **Отключение Bootstrap CSS** временно
4. **Проверка в разных браузерах**

## 💡 Альтернативные решения

### Вариант A: Inline блоки
```html
<div style="white-space: nowrap;">
    <button style="display: inline-block;">[-]</button>
    <input style="display: inline-block; width: 50px;">
    <button style="display: inline-block;">[+]</button>
</div>
```

### Вариант B: CSS Grid
```html
<div style="display: grid; grid-template-columns: auto auto auto; width: fit-content;">
    <button>[-]</button>
    <input>
    <button>[+]</button>
</div>
```

### Вариант C: Абсолютное позиционирование
```html
<div style="position: relative; width: 120px; height: 32px;">
    <button style="position: absolute; left: 0;">[-]</button>
    <input style="position: absolute; left: 32px; width: 56px;">
    <button style="position: absolute; right: 0;">[+]</button>
</div>
```

## 🎯 Рекомендация

Если текущее решение с таблицей не работает, рекомендую попробовать **Вариант A** с inline-block, так как он самый простой и надежный.

🔄 **Пожалуйста, проверьте текущий результат и сообщите, работает ли решение с таблицей!**
