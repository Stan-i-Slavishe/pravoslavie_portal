// КАРДИНАЛЬНОЕ ИСПРАВЛЕНИЕ МОБИЛЬНОЙ НАВИГАЦИИ
// Бургер-меню в левом верхнем углу, полное разделение навигации

(function() {
    'use strict';
    
    console.log('🚀 Кардинальное исправление мобильной навигации (бургер слева)...');
    
    // Функция для определения мобильного устройства
    function isMobile() {
        return window.innerWidth <= 991;
    }
    
    // Функция полного скрытия десктопной навигации
    function hideAllDesktopNavigation() {
        const elementsToHide = [
            'nav.navbar',
            '.navbar',
            '.navbar-expand-lg', 
            '.navbar-nav',
            '.nav-item',
            '.nav-link',
            '.navbar-toggler',
            '.navbar-collapse',
            '.dropdown-menu',
            '.desktop-nav'
        ];
        
        elementsToHide.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
                el.style.opacity = '0';
                el.style.position = 'absolute';
                el.style.left = '-999999px';
                el.style.top = '-999999px';
                el.style.zIndex = '-999999';
                el.style.pointerEvents = 'none';
            });
        });
    }
    
    // Основная функция исправления навигации
    function fixMobileNavigation() {
        if (isMobile()) {
            console.log('📱 Мобильное устройство: применяем исправления...');
            
            // 1. Скрываем всю десктопную навигацию
            hideAllDesktopNavigation();
            
            // 2. Настраиваем бургер-меню слева
            const burgerMenu = document.querySelector('.mobile-burger-menu');
            if (burgerMenu) {
                burgerMenu.style.display = 'flex';
                burgerMenu.style.position = 'fixed';
                burgerMenu.style.top = '15px';
                burgerMenu.style.left = '15px';  // СЛЕВА!
                burgerMenu.style.right = 'auto';
                burgerMenu.style.zIndex = '999999';
                burgerMenu.style.width = '50px';
                burgerMenu.style.height = '50px';
                burgerMenu.style.background = 'rgba(43, 90, 160, 0.95)';
                burgerMenu.style.borderRadius = '15px';
                burgerMenu.style.border = '2px solid rgba(255, 255, 255, 0.3)';
                burgerMenu.style.boxShadow = '0 6px 25px rgba(43, 90, 160, 0.4)';
                burgerMenu.style.pointerEvents = 'auto';
                
                // Стили иконки
                const icon = burgerMenu.querySelector('.mobile-burger-icon');
                if (icon) {
                    icon.style.color = 'white';
                    icon.style.fontSize = '24px';
                }
                
                console.log('✅ Бургер-меню настроено (слева)');
            }
            
            // 3. Показываем мобильную навигацию снизу
            const mobileNav = document.querySelector('.mobile-bottom-nav');
            if (mobileNav) {
                mobileNav.style.display = 'block';
                mobileNav.style.position = 'fixed';
                mobileNav.style.bottom = '0';
                mobileNav.style.left = '0';
                mobileNav.style.right = '0';
                mobileNav.style.zIndex = '1040';
                console.log('✅ Мобильная навигация активна');
            }
            
            // 4. Корректируем отступы контента
            document.body.style.paddingTop = '0';
            document.body.style.marginTop = '0';
            document.body.style.paddingBottom = '80px'; // Для нижней навигации
            
            const mainContainer = document.querySelector('main.container');
            if (mainContainer) {
                mainContainer.style.marginTop = '20px';
                mainContainer.style.paddingTop = '20px';
                mainContainer.style.paddingLeft = '85px'; // Отступ для бургера слева
                mainContainer.style.paddingRight = '20px';
            }
            
            console.log('✅ Мобильные исправления применены');
            
        } else {
            console.log('🖥️ Десктопное устройство: скрываем мобильные элементы...');
            
            // На десктопе скрываем бургер-меню
            const burgerMenu = document.querySelector('.mobile-burger-menu');
            if (burgerMenu) {
                burgerMenu.style.display = 'none';
                burgerMenu.style.visibility = 'hidden';
            }
            
            // Возвращаем нормальные отступы
            const mainContainer = document.querySelector('main.container');
            if (mainContainer) {
                mainContainer.style.paddingLeft = '15px';
                mainContainer.style.paddingRight = '15px';
            }
            
            console.log('✅ Десктопные настройки восстановлены');
        }
    }
    
    // Обработчик изменения размера окна
    function handleResize() {
        clearTimeout(window.mobileNavResizeTimer);
        window.mobileNavResizeTimer = setTimeout(fixMobileNavigation, 50);
    }
    
    // Инициализация при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fixMobileNavigation);
    } else {
        fixMobileNavigation();
    }
    
    // Обработка изменения размера окна
    window.addEventListener('resize', handleResize);
    
    // Дополнительные проверки
    setTimeout(fixMobileNavigation, 100);
    setTimeout(fixMobileNavigation, 500);
    
    // Обработка клика по бургер-меню
    document.addEventListener('click', function(e) {
        const burger = e.target.closest('.mobile-burger-menu');
        if (burger) {
            burger.classList.toggle('active');
            console.log('🍔 Клик по бургер-меню');
        }
    });
    
    console.log('🎯 Кардинальное исправление навигации инициализировано');
    
})();

// Глобальные функции для отладки
window.mobileNavFixLeft = {
    force: function() {
        console.log('🔧 Принудительное исправление навигации...');
        
        // Скрываем все navbar
        document.querySelectorAll('nav, .navbar').forEach(el => {
            el.style.display = 'none';
        });
        
        // Показываем бургер слева
        const burger = document.querySelector('.mobile-burger-menu');
        if (burger) {
            burger.style.display = 'flex';
            burger.style.position = 'fixed';
            burger.style.top = '15px';
            burger.style.left = '15px';
            burger.style.right = 'auto';
            burger.style.zIndex = '999999';
            burger.style.background = 'rgba(43, 90, 160, 0.95)';
        }
        
        // Корректируем отступы
        const main = document.querySelector('main.container');
        if (main) {
            main.style.paddingLeft = '85px';
        }
        
        console.log('✅ Принудительное исправление применено');
    },
    
    check: function() {
        console.log('=== ПРОВЕРКА СОСТОЯНИЯ НАВИГАЦИИ ===');
        console.log('Ширина экрана:', window.innerWidth);
        console.log('Мобильное устройство:', window.innerWidth <= 991);
        
        const burger = document.querySelector('.mobile-burger-menu');
        const navbar = document.querySelector('.navbar');
        const mobileNav = document.querySelector('.mobile-bottom-nav');
        
        console.log('Бургер-меню найдено:', !!burger);
        if (burger) {
            console.log('Бургер видим:', window.getComputedStyle(burger).display !== 'none');
            console.log('Позиция бургера:', window.getComputedStyle(burger).position);
            console.log('Левый отступ:', window.getComputedStyle(burger).left);
            console.log('Правый отступ:', window.getComputedStyle(burger).right);
        }
        
        console.log('Десктопная навигация найдена:', !!navbar);
        if (navbar) {
            console.log('Десктопная навигация видима:', window.getComputedStyle(navbar).display !== 'none');
        }
        
        console.log('Мобильная навигация найдена:', !!mobileNav);
        if (mobileNav) {
            console.log('Мобильная навигация видима:', window.getComputedStyle(mobileNav).display !== 'none');
        }
        
        console.log('=====================================');
    },
    
    debug: function() {
        // Включаем отладочные стили
        const debugCSS = `
            @media (max-width: 991.98px) {
                .mobile-burger-menu {
                    background: rgba(255, 0, 0, 0.8) !important;
                    border: 3px solid yellow !important;
                }
                .navbar {
                    background: rgba(0, 255, 0, 0.5) !important;
                    display: block !important;
                    opacity: 0.3 !important;
                }
            }
        `;
        
        const style = document.createElement('style');
        style.textContent = debugCSS;
        document.head.appendChild(style);
        
        console.log('🐛 Отладочные стили включены');
    }
};

// Экспорт для совместимости
if (typeof window !== 'undefined') {
    window.fixMobileNavigation = window.mobileNavFixLeft.force;
}
