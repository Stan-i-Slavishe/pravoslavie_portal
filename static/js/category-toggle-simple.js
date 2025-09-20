// Простое и надежное решение для переключения категорий
(function() {
    'use strict';
    
    // Предотвращаем повторное выполнение
    if (window.categoryToggleInitialized) {
        return;
    }
    window.categoryToggleInitialized = true;
    
    let isExpanded = false;
    
    function toggleCategories() {
        console.log('🔄 Переключение категорий... Текущее состояние:', isExpanded);
        
        // Ищем все кнопки категорий
        const allCategories = document.querySelectorAll('.category-btn');
        console.log('Всего категорий:', allCategories.length);
        
        if (allCategories.length <= 7) {
            console.log('Недостаточно категорий для скрытия');
            return;
        }
        
        const toggleIcon = document.getElementById('toggleIcon');
        const toggleText = document.getElementById('toggleText');
        
        // Сначала переключаем состояние
        isExpanded = !isExpanded;
        
        // Переключаем видимость категорий после 6-й позиции
        const categoryContainer = document.querySelector('.category-filter');
        if (categoryContainer) {
            // Убеждаемся, что контейнер может показать все категории
            categoryContainer.style.setProperty('flex-wrap', 'wrap', 'important');
            categoryContainer.style.setProperty('height', 'auto', 'important');
            categoryContainer.style.setProperty('max-height', 'none', 'important');
            categoryContainer.style.setProperty('overflow', 'visible', 'important');
            console.log('Контейнер категорий настроен');
        }
        
        for (let i = 7; i < allCategories.length; i++) {
            const category = allCategories[i];
            if (isExpanded) {
                // Показываем
                category.style.setProperty('display', 'flex', 'important');
                category.style.setProperty('visibility', 'visible', 'important');
                category.style.setProperty('opacity', '1', 'important');
                category.style.setProperty('position', 'static', 'important');
                category.style.setProperty('width', 'auto', 'important');
                category.style.setProperty('height', 'auto', 'important');
                console.log('Показана:', category.textContent.trim());
            } else {
                // Скрываем
                category.style.setProperty('display', 'none', 'important');
                console.log('Скрыта:', category.textContent.trim());
            }
        }
        
        // Обновляем кнопку
        if (toggleIcon && toggleText) {
            if (isExpanded) {
                toggleIcon.className = 'bi bi-chevron-up me-1';
                toggleText.textContent = 'Скрыть';
            } else {
                toggleIcon.className = 'bi bi-chevron-down me-1';
                toggleText.textContent = 'Показать все категории';
            }
        }
        
        console.log('Новое состояние:', isExpanded ? 'показаны' : 'скрыты');
    }
    
    function initializeToggle() {
        console.log('Инициализация...');
        
        // Ищем все категории
        const allCategories = document.querySelectorAll('.category-btn');
        console.log('Найдено категорий:', allCategories.length);
        
        // Принудительно скрываем категории после 6-й позиции
        let hiddenCount = 0;
        for (let i = 7; i < allCategories.length; i++) {
            const category = allCategories[i];
            category.style.setProperty('display', 'none', 'important');
            hiddenCount++;
            console.log('Принудительно скрыта:', category.textContent.trim());
        }
        
        console.log('Скрыто категорий:', hiddenCount);
        
        // Настраиваем кнопку
        const toggleIcon = document.getElementById('toggleIcon');
        const toggleText = document.getElementById('toggleText');
        if (toggleIcon && toggleText) {
            toggleIcon.className = 'bi bi-chevron-down me-1';
            toggleText.textContent = 'Показать все категории';
        }
        
        // Устанавливаем обработчик
        const toggleButton = document.getElementById('toggleCategories');
        if (toggleButton) {
            toggleButton.onclick = function(e) {
                e.preventDefault();
                toggleCategories();
            };
            console.log('Обработчик установлен');
        }
        
        // Делаем функцию глобальной
        window.toggleAllCategories = toggleCategories;
        
        console.log('Готово!');
    }
    
    // Запускаем инициализацию
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeToggle);
    } else {
        initializeToggle();
    }
    
})();
