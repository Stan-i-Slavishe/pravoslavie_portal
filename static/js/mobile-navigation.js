// static/js/mobile-navigation.js
// Мобильная навигация для православного портала "Добрые истории"

(function() {
    'use strict';

    // Инициализация при загрузке DOM
    document.addEventListener('DOMContentLoaded', function() {
        initMobileNavigation();
    });

    function initMobileNavigation() {
        setActiveNavItem();
        initScrollBehavior();
        initRippleEffect();
        initHapticFeedback();
        
        console.log('✅ Мобильная навигация инициализирована');
    }

    // Установка активного пункта навигации
    function setActiveNavItem() {
        const currentPath = window.location.pathname;
        const navItems = document.querySelectorAll('.mobile-nav-item');
        
        // Убираем все активные классы
        navItems.forEach(item => {
            item.classList.remove('active');
        });

        // Определяем активный раздел
        let activeSection = 'home';
        
        if (currentPath.includes('/stories/')) {
            activeSection = 'stories';
        } else if (currentPath.includes('/books/')) {
            activeSection = 'books';
        } else if (currentPath.includes('/fairy-tales/') || currentPath.includes('/fairy_tales/')) {
            activeSection = 'fairy-tales';
        } else if (currentPath.includes('/audio/')) {
            activeSection = 'audio';
        } else if (currentPath.includes('/shop/')) {
            activeSection = 'shop';
        } else if (currentPath === '/') {
            activeSection = 'home';
        }

        // Устанавливаем активный элемент
        const activeItem = document.querySelector(`.mobile-nav-item[data-section="${activeSection}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
    }

    // Поведение при скролле (скрытие/показ навигации)
    function initScrollBehavior() {
        let lastScrollTop = 0;
        let scrollTimeout;
        const nav = document.getElementById('mobileNav');
        
        if (!nav) return;

        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            clearTimeout(scrollTimeout);
            
            scrollTimeout = setTimeout(() => {
                if (scrollTop > lastScrollTop && scrollTop > 100) {
                    // Скролл вниз - скрываем навигацию
                    nav.classList.add('hide');
                    nav.classList.remove('show');
                } else {
                    // Скролл вверх - показываем навигацию
                    nav.classList.remove('hide');
                    nav.classList.add('show');
                }
                lastScrollTop = scrollTop;
            }, 100);
        });
    }

    // Эффект ряби при клике
    function initRippleEffect() {
        const navItems = document.querySelectorAll('.mobile-nav-item');
        
        navItems.forEach(item => {
            item.addEventListener('click', function(e) {
                // Создаем эффект ряби
                const rect = this.getBoundingClientRect();
                const ripple = document.createElement('div');
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');
                
                this.appendChild(ripple);
                
                // Удаляем эффект через 600ms
                setTimeout(() => {
                    if (ripple.parentNode) {
                        ripple.parentNode.removeChild(ripple);
                    }
                }, 600);
                
                // Если это не модальное окно, обновляем активный элемент
                if (!this.hasAttribute('data-bs-toggle')) {
                    setTimeout(() => {
                        document.querySelectorAll('.mobile-nav-item').forEach(nav => nav.classList.remove('active'));
                        this.classList.add('active');
                    }, 150);
                }
            });
        });
    }

    // Тактильная обратная связь (если поддерживается)
    function initHapticFeedback() {
        const navItems = document.querySelectorAll('.mobile-nav-item');
        
        navItems.forEach(item => {
            item.addEventListener('touchstart', function() {
                // Легкая вибрация на устройствах, которые поддерживают
                if ('vibrate' in navigator) {
                    navigator.vibrate(10);
                }
            });
        });
    }

    // Обновление бейджей
    function updateNavigationBadges() {
        // Обновляем счетчик корзины в мобильной навигации
        if (window.updateCartBadge) {
            window.updateCartBadge();
        }
        
        // Обновляем счетчик избранного
        if (window.updateFavoritesCount) {
            window.updateFavoritesCount();
        }
    }

    // Плавная анимация переходов
    function animateNavigation() {
        const nav = document.getElementById('mobileNav');
        if (!nav) return;
        
        // Анимация появления при загрузке
        nav.style.transform = 'translateY(100%)';
        nav.style.opacity = '0';
        
        setTimeout(() => {
            nav.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            nav.style.transform = 'translateY(0)';
            nav.style.opacity = '1';
        }, 100);
    }

    // Обработка изменения ориентации экрана
    function handleOrientationChange() {
        window.addEventListener('orientationchange', function() {
            setTimeout(() => {
                setActiveNavItem();
                updateNavigationBadges();
            }, 200);
        });
    }

    // Обработка deep links и hash navigation
    function handleDeepLinks() {
        window.addEventListener('hashchange', function() {
            setActiveNavItem();
        });
        
        // Обработка navigation API (если поддерживается)
        if ('navigation' in window) {
            window.navigation.addEventListener('navigate', function() {
                setTimeout(setActiveNavItem, 50);
            });
        }
    }

    // Accessibility improvements
    function initAccessibility() {
        const navItems = document.querySelectorAll('.mobile-nav-item');
        
        navItems.forEach(item => {
            // Добавляем ARIA labels
            const text = item.querySelector('.mobile-nav-text')?.textContent;
            if (text) {
                item.setAttribute('aria-label', text);
            }
            
            // Улучшенная навигация с клавиатуры
            item.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.click();
                }
            });
        });
    }

    // Обработка сетевых состояний
    function initNetworkHandling() {
        function updateConnectivityStatus() {
            const navItems = document.querySelectorAll('.mobile-nav-item');
            
            if (!navigator.onLine) {
                navItems.forEach(item => {
                    item.style.opacity = '0.6';
                    item.setAttribute('title', 'Нет подключения к интернету');
                });
            } else {
                navItems.forEach(item => {
                    item.style.opacity = '1';
                    item.removeAttribute('title');
                });
            }
        }
        
        window.addEventListener('online', updateConnectivityStatus);
        window.addEventListener('offline', updateConnectivityStatus);
        updateConnectivityStatus(); // Проверяем при загрузке
    }

    // Отслеживание производительности
    function initPerformanceTracking() {
        const navItems = document.querySelectorAll('.mobile-nav-item');
        
        navItems.forEach(item => {
            item.addEventListener('click', function() {
                const section = this.getAttribute('data-section');
                
                // Отправляем аналитику (если настроена)
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'mobile_navigation_click', {
                        'section': section,
                        'device_type': 'mobile'
                    });
                }
                
                // Яндекс.Метрика (если настроена)
                if (typeof ym !== 'undefined') {
                    ym(window.yaCounterId || 0, 'reachGoal', 'mobile_nav_' + section);
                }
            });
        });
    }

    // Кеширование для оффлайн режима
    function initOfflineCaching() {
        if ('serviceWorker' in navigator) {
            // Регистрируем service worker для кеширования
            navigator.serviceWorker.register('/sw.js').then(function(registration) {
                console.log('SW registered: ', registration);
            }).catch(function(registrationError) {
                console.log('SW registration failed: ', registrationError);
            });
        }
    }

    // Обновление времени последней активности
    function updateLastActivity() {
        localStorage.setItem('lastActivity', Date.now().toString());
    }

    // Инициализация всех функций
    function initAdvancedFeatures() {
        handleOrientationChange();
        handleDeepLinks();
        initAccessibility();
        initNetworkHandling();
        initPerformanceTracking();
        // initOfflineCaching(); // Раскомментировать если нужен оффлайн режим
        
        // Обновляем активность при взаимодействии
        document.addEventListener('click', updateLastActivity);
        document.addEventListener('scroll', updateLastActivity);
    }

    // Полная инициализация
    document.addEventListener('DOMContentLoaded', function() {
        initMobileNavigation();
        animateNavigation();
        initAdvancedFeatures();
        
        // Обновляем бейджи через небольшую задержку
        setTimeout(updateNavigationBadges, 500);
    });

    // Экспортируем функции для использования в других скриптах
    window.MobileNavigation = {
        setActiveItem: setActiveNavItem,
        updateBadges: updateNavigationBadges,
        show: function() {
            const nav = document.getElementById('mobileNav');
            if (nav) {
                nav.classList.remove('hide');
                nav.classList.add('show');
            }
        },
        hide: function() {
            const nav = document.getElementById('mobileNav');
            if (nav) {
                nav.classList.add('hide');
                nav.classList.remove('show');
            }
        }
    };

})();

// CSS для эффекта ряби (добавляется динамически)
const rippleStyles = `
    .mobile-nav-item {
        overflow: hidden;
        position: relative;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(2);
            opacity: 0;
        }
    }
`;

// Добавляем стили в head
if (!document.getElementById('ripple-styles')) {
    const style = document.createElement('style');
    style.id = 'ripple-styles';
    style.textContent = rippleStyles;
    document.head.appendChild(style);
}
