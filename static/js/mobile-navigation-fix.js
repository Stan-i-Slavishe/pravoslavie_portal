// JavaScript для исправления проблем с z-index в мобильной навигации

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Загрузка исправлений для мобильной навигации...');
    
    // Функция для исправления z-index элементов
    function fixMobileNavigation() {
        // Найдем все dropdown меню в навигации
        const dropdownMenus = document.querySelectorAll('.navbar .dropdown-menu');
        const adminDropdown = document.querySelector('.navbar-nav .nav-item.dropdown:last-child');
        
        // Устанавливаем правильные z-index для dropdown меню
        dropdownMenus.forEach((menu, index) => {
            menu.style.zIndex = '1060';
        });
        
        // Понижаем z-index для admin элемента
        if (adminDropdown) {
            adminDropdown.style.zIndex = '900';
        }
        
        console.log('✅ Z-index исправлен для', dropdownMenus.length, 'dropdown меню');
    }
    
    // Функция для обработки открытия/закрытия dropdown
    function handleDropdownToggle() {
        const dropdownToggles = document.querySelectorAll('.navbar .dropdown-toggle');
        
        dropdownToggles.forEach(toggle => {
            toggle.addEventListener('click', function(e) {
                // Небольшая задержка для обработки Bootstrap логики
                setTimeout(() => {
                    const dropdownMenu = this.nextElementSibling;
                    if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
                        if (dropdownMenu.classList.contains('show')) {
                            dropdownMenu.style.zIndex = '1070';
                            console.log('📱 Dropdown открыт, z-index установлен в 1070');
                        }
                    }
                }, 10);
            });
        });
    }
    
    // Функция для проверки размера экрана и применения соответствующих исправлений
    function checkScreenSize() {
        const isMobile = window.innerWidth <= 768;
        const adminDropdown = document.querySelector('.navbar-nav .nav-item.dropdown:last-child');
        
        if (isMobile && adminDropdown) {
            // В мобильной версии понижаем приоритет admin элемента
            adminDropdown.style.zIndex = '800';
            adminDropdown.style.position = 'relative';
            
            console.log('📱 Мобильная версия: admin z-index установлен в 800');
        } else if (adminDropdown) {
            // В десктопной версии возвращаем обычный приоритет
            adminDropdown.style.zIndex = '900';
            
            console.log('🖥️ Десктопная версия: admin z-index установлен в 900');
        }
    }
    
    // Применяем исправления
    fixMobileNavigation();
    handleDropdownToggle();
    checkScreenSize();
    
    // Отслеживаем изменения размера экрана
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            checkScreenSize();
            fixMobileNavigation();
        }, 250);
    });
    
    // Дополнительная проверка через MutationObserver для динамических изменений
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                const target = mutation.target;
                if (target.classList.contains('dropdown-menu') && target.classList.contains('show')) {
                    target.style.zIndex = '1070';
                    console.log('🔄 Динамически исправлен z-index для показанного dropdown');
                }
            }
        });
    });
    
    // Наблюдаем за изменениями в навигации
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        observer.observe(navbar, {
            attributes: true,
            subtree: true,
            attributeFilter: ['class']
        });
    }
    
    console.log('✅ Система исправления мобильной навигации активирована');
});

// Экспортируем функции для ручного использования
window.fixMobileNavigation = function() {
    const dropdownMenus = document.querySelectorAll('.navbar .dropdown-menu');
    dropdownMenus.forEach(menu => {
        menu.style.zIndex = '1070';
    });
    
    const adminDropdown = document.querySelector('.navbar-nav .nav-item.dropdown:last-child');
    if (adminDropdown) {
        adminDropdown.style.zIndex = '800';
    }
    
    console.log('🔧 Ручное исправление применено');
};

// Функция для отладки z-index элементов
window.debugZIndex = function() {
    const elements = document.querySelectorAll('.navbar *');
    console.log('🐛 Отладка z-index элементов навигации:');
    
    elements.forEach((el, index) => {
        const zIndex = window.getComputedStyle(el).zIndex;
        if (zIndex !== 'auto') {
            console.log(`${index}: ${el.tagName}.${el.className} - z-index: ${zIndex}`);
        }
    });
};