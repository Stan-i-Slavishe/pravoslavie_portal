/**
 * Простое решение для dropdown конфликтов
 * Автоматическое закрытие предыдущих меню
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Инициализация простого dropdown менеджера');
    
    // Находим все dropdown toggle в навигации
    const dropdownToggles = document.querySelectorAll('.navbar .dropdown-toggle');
    
    if (dropdownToggles.length === 0) {
        console.log('❌ Dropdown элементы не найдены');
        return;
    }
    
    console.log(`✅ Найдено ${dropdownToggles.length} dropdown элементов`);
    
    // Добавляем обработчик для каждого dropdown
    dropdownToggles.forEach((toggle, index) => {
        toggle.addEventListener('click', function(e) {
            console.log(`📂 Клик по dropdown #${index}: ${toggle.textContent.trim()}`);
            
            // В мобильной версии закрываем все остальные dropdown
            if (window.innerWidth < 992) {
                console.log('📱 Мобильная версия - закрываем другие dropdown');
                
                dropdownToggles.forEach((otherToggle, otherIndex) => {
                    if (otherIndex !== index) {
                        const otherDropdown = bootstrap.Dropdown.getInstance(otherToggle);
                        if (otherDropdown) {
                            console.log(`🔄 Закрываем dropdown #${otherIndex}`);
                            otherDropdown.hide();
                        }
                    }
                });
            }
        });
    });
    
    // Обработчик для отслеживания состояния
    dropdownToggles.forEach((toggle, index) => {
        const dropdown = toggle.closest('.dropdown');
        
        dropdown.addEventListener('show.bs.dropdown', function() {
            console.log(`📂 Открывается dropdown #${index}`);
        });
        
        dropdown.addEventListener('hide.bs.dropdown', function() {
            console.log(`📁 Закрывается dropdown #${index}`);
        });
    });
    
    console.log('✅ Простой dropdown менеджер готов');
});

// Дополнительная функция для принудительного закрытия всех меню
window.closeAllDropdowns = function() {
    console.log('🔄 Принудительное закрытие всех dropdown');
    
    const dropdownToggles = document.querySelectorAll('.navbar .dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        const dropdown = bootstrap.Dropdown.getInstance(toggle);
        if (dropdown) {
            dropdown.hide();
        }
    });
};

// Простые CSS стили для улучшения UX
const simpleDropdownStyles = `
    /* Улучшенные стили для мобильных dropdown */
    @media (max-width: 991.98px) {
        .navbar .dropdown-menu {
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            border: 1px solid rgba(0, 0, 0, 0.15) !important;
            border-radius: 0.5rem !important;
            margin-top: 0.25rem !important;
        }
        
        .navbar .dropdown-item {
            padding: 0.75rem 1rem !important;
            transition: background-color 0.2s ease !important;
        }
        
        .navbar .dropdown-item:hover {
            background-color: rgba(0, 123, 255, 0.1) !important;
        }
        
        /* Анимация появления */
        .navbar .dropdown-menu.show {
            animation: fadeInDown 0.3s ease;
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    }
`;

// Добавляем стили
const styleElement = document.createElement('style');
styleElement.textContent = simpleDropdownStyles;
document.head.appendChild(styleElement);

console.log('🎨 Простые стили dropdown добавлены');
