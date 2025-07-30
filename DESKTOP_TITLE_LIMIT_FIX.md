# Исправление длинных названий книг в PDF ридере

## Проблема
В десктопной версии PDF ридера длинные названия книг наплывали на кнопки листания страниц, мешая навигации.

## Решение
Добавлено ограничение названия книги до 30 символов **только для десктопной версии** (экраны шире 768px).

### Изменения в `books/templates/books/modern_reader.html`:

#### 1. CSS ограничение для десктопа
```css
/* Ограничение длины названия только для десктопа */
@media (min-width: 769px) {
    .book-title {
        max-width: 300px; /* Примерно 30 символов */
    }
}
```

#### 2. JavaScript функция точного ограничения
```javascript
function limitBookTitleForDesktop() {
    const bookTitleElement = document.querySelector('.book-title');
    if (!bookTitleElement) return;
    
    // Сохраняем оригинальное название
    if (!bookTitleElement.title) {
        bookTitleElement.title = bookTitleElement.textContent.trim();
    }
    
    const originalTitle = bookTitleElement.title;
    
    // Для десктопа (ширина > 768px)
    if (window.innerWidth > 768) {
        if (originalTitle.length > 30) {
            bookTitleElement.textContent = originalTitle.substring(0, 30) + '...';
        }
    } else {
        // На мобильных показываем полное название
        bookTitleElement.textContent = originalTitle;
    }
}
```

#### 3. Автоматическое переключение при изменении размера экрана
```javascript
window.addEventListener('resize', function() {
    const bookTitleElement = document.querySelector('.book-title');
    if (bookTitleElement && bookTitleElement.title) {
        bookTitleElement.textContent = bookTitleElement.title;
        limitBookTitleForDesktop();
    }
});
```

## Особенности:

✅ **Работает только на десктопе** (экраны шире 768px)  
✅ **Точное ограничение** - ровно 30 символов + "..."  
✅ **Tooltip с полным названием** при наведении  
✅ **Автоматическое переключение** при изменении размера окна  
✅ **Полное название на мобильных** устройствах  
✅ **Адаптивность** - корректно работает при поворотах экрана  

## Тестирование
Запустите `test_desktop_title_limit.bat` для проверки изменений.

## Пример работы:
- **Исходное название:** "Приветствую всех своих новых друзей на курсе Экспресс настройки Яндекс Директ"
- **На десктопе:** "Приветствую всех своих новых..." (+ tooltip с полным названием)
- **На мобильном:** "Приветствую всех своих новых друзей на курсе Экспресс настройки Яндекс Директ"

Теперь длинные названия не мешают навигации в PDF ридере! 🎉
