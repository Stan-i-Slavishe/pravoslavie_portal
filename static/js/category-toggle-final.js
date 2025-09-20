// Финальное решение для переключения категорий
(function() {
    'use strict';
    
    // Предотвращаем повторное выполнение
    if (window.categoryToggleInitialized) {
        return;
    }
    window.categoryToggleInitialized = true;
    
    let isExpanded = false;
    
    function toggleCategories() {
        console.log('🔄 Вызвана функция переключения категорий');
        
        // Пробуем разные селекторы для поиска скрытых категорий
        let hiddenCategories = document.querySelectorAll('.category-hidden');
        
        if (!hiddenCategories.length) {
            // Пробуем найти по data-category-index > 6
            hiddenCategories = document.querySelectorAll('[data-category-index]');
            const filtered = [];
            hiddenCategories.forEach(cat => {
                const index = parseInt(cat.getAttribute('data-category-index'));
                if (index > 6) {
                    filtered.push(cat);
                }
            });
            hiddenCategories = filtered;
            console.log('📋 Найдено категорий с индексом > 6:', filtered.length);
        }
        
        if (!hiddenCategories.length) {
            // Пробуем найти все кнопки категорий после 6-й
            const allCategories = document.querySelectorAll('.category-btn');
            const filtered = [];
            allCategories.forEach((cat, index) => {
                if (index > 6) { // Пропускаем первые 7 (0-6)
                    filtered.push(cat);
                }
            });
            hiddenCategories = filtered;
            console.log('📋 Найдено категорий после 6-й позиции:', filtered.length);
        }
        
        console.log('📋 Всего скрытых категорий для переключения:', hiddenCategories.length);
        
        if (!hiddenCategories.length) {
            console.log('❌ Не найдено категорий для скрытия/показа');
            return;
        }
        
        const toggleIcon = document.getElementById('toggleIcon');
        const toggleText = document.getElementById('toggleText');
        
        // Переключаем видимость
        hiddenCategories.forEach((category, index) => {
            if (isExpanded) {
                // Скрываем - добавляем класс скрытия
                category.classList.add('category-hidden');
                category.classList.remove('category-shown');
                console.log(`➖ Скрыта категория ${index + 1}:`, category.textContent.trim());
            } else {
                // Показываем - убираем класс скрытия
                category.classList.remove('category-hidden');
                category.classList.add('category-shown');
                console.log(`➕ Показана категория ${index + 1}:`, category.textContent.trim());
            }
        });
        
        // Переключаем состояние
        isExpanded = !isExpanded;
        
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
        
        console.log('✅ Категории переключены. Состояние:', isExpanded ? 'показаны' : 'скрыты');
    }
    
    function initializeToggle() {
        console.log('🚀 Инициализация переключения категорий...');
        
        // Ищем все категории
        const allCategories = document.querySelectorAll('.category-btn');
        console.log('📋 Всего найдено кнопок категорий:', allCategories.length);
        
        // Показываем информацию о каждой категории
        allCategories.forEach((cat, index) => {
            console.log(`Категория ${index}:`, cat.textContent.trim(), '| data-index:', cat.getAttribute('data-category-index'));
        });
        
        // Скрываем категории после 6-й (индексы 7, 8, 9, ...)
        let hiddenCount = 0;
        allCategories.forEach((category, index) => {
            if (index > 6) { // Скрываем после первых 7 (индексы 0-6)
                category.style.display = 'none';
                category.style.visibility = 'hidden';
                category.classList.add('category-hidden');
                hiddenCount++;
                console.log(`🚫 Скрыта категория ${index}:`, category.textContent.trim());
            }
        });
        
        console.log(`✅ Скрыто ${hiddenCount} категорий`);
        
        // Устанавливаем начальное состояние кнопки
        const toggleIcon = document.getElementById('toggleIcon');
        const toggleText = document.getElementById('toggleText');
        if (toggleIcon && toggleText) {
            toggleIcon.className = 'bi bi-chevron-down me-1';
            toggleText.textContent = 'Показать все категории';
            console.log('✅ Кнопка настроена на начальное состояние');
        }
        
        // Устанавливаем обработчик
        const toggleButton = document.getElementById('toggleCategories');
        if (toggleButton) {
            toggleButton.onclick = function(e) {
                e.preventDefault();
                toggleCategories();
            };
            console.log('✅ Обработчик клика установлен');
        } else {
            console.log('❌ Кнопка toggleCategories не найдена');
        }
        
        // Делаем функцию глобально доступной
        window.toggleAllCategories = toggleCategories;
        
        console.log('🎉 Инициализация завершена!');
    }
    
    // Запускаем инициализацию при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeToggle);
    } else {
        initializeToggle();
    }
    
})();
