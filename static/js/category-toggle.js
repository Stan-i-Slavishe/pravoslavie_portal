// Функция для переключения категорий на странице видео-рассказов
(function() {
    'use strict';
    
    let categoriesExpanded = false;
    
    function toggleAllCategories() {
        console.log('🔄 Переключение категорий. Текущее состояние:', categoriesExpanded);
        
        const hiddenCategories = document.querySelectorAll('.category-hidden');
        const toggleIcon = document.getElementById('toggleIcon');
        const toggleText = document.getElementById('toggleText');
        
        if (!hiddenCategories.length) {
            console.log('❌ Скрытые категории не найдены');
            return;
        }
        
        console.log('📋 Найдено скрытых категорий:', hiddenCategories.length);
        
        hiddenCategories.forEach((category, index) => {
            if (categoriesExpanded) {
                // Сворачиваем - скрываем категории
                category.style.display = 'none';
                category.style.visibility = 'hidden';
                console.log(`➖ Скрыта категория ${index + 1}: ${category.textContent.trim()}`);
            } else {
                // Разворачиваем - показываем категории
                category.style.display = 'flex';
                category.style.visibility = 'visible';
                console.log(`➕ Показана категория ${index + 1}: ${category.textContent.trim()}`);
            }
        });
        
        // Переключаем состояние
        categoriesExpanded = !categoriesExpanded;
        console.log('🔄 Новое состояние:', categoriesExpanded);
        
        // Обновляем кнопку
        if (toggleIcon && toggleText) {
            if (categoriesExpanded) {
                toggleIcon.className = 'bi bi-chevron-up me-1';
                toggleText.textContent = 'Скрыть';
                console.log('🔼 Кнопка: Скрыть');
            } else {
                toggleIcon.className = 'bi bi-chevron-down me-1';
                toggleText.textContent = 'Показать все категории';
                console.log('🔽 Кнопка: Показать все категории');
            }
        } else {
            console.log('❌ Элементы кнопки не найдены');
        }
    }
    
    function initCategoryToggle() {
        console.log('🚀 Инициализация переключения категорий...');
        
        // Убеждаемся, что скрытые категории действительно скрыты
        const hiddenCategories = document.querySelectorAll('.category-hidden');
        console.log('📋 Всего скрытых категорий:', hiddenCategories.length);
        
        if (hiddenCategories.length === 0) {
            console.log('❌ Скрытые категории не найдены, возможно их меньше 6');
            return;
        }
        
        // Принудительно скрываем все скрытые категории
        hiddenCategories.forEach((category, index) => {
            category.style.display = 'none';
            category.style.visibility = 'hidden';
            console.log(`🚫 Принудительно скрыта категория ${index + 1}: ${category.textContent.trim()}`);
        });
        
        // Устанавливаем начальное состояние
        categoriesExpanded = false;
        
        // Настраиваем кнопку
        const toggleIcon = document.getElementById('toggleIcon');
        const toggleText = document.getElementById('toggleText');
        const toggleButton = document.getElementById('toggleCategories');
        
        if (toggleIcon && toggleText) {
            toggleIcon.className = 'bi bi-chevron-down me-1';
            toggleText.textContent = 'Показать все категории';
            console.log('✅ Кнопка настроена: Показать все категории');
        }
        
        // Добавляем обработчик клика
        if (toggleButton) {
            toggleButton.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                toggleAllCategories();
            });
            console.log('✅ Обработчик клика добавлен');
        } else {
            console.log('❌ Кнопка переключения не найдена');
        }
        
        // Делаем функцию глобальной для совместимости
        window.toggleAllCategories = toggleAllCategories;
        
        console.log('✅ Инициализация завершена');
    }
    
    // Ждем загрузки DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCategoryToggle);
    } else {
        initCategoryToggle();
    }
    
})();
