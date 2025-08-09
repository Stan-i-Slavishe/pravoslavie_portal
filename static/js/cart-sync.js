/**
 * Система синхронизации корзины для православного портала
 * Обеспечивает синхронное обновление всех счетчиков корзины
 */

(function() {
    'use strict';
    
    // Конфигурация селекторов для поиска счетчиков корзины
    const CART_SELECTORS = {
        desktop: '#cart-badge',
        mobile: '#mobile-cart-badge',
        floating: '.floating-cart .badge, .cart-float .badge, [class*="floating"][class*="cart"] .badge',
        all: '[id*="cart-badge"], [class*="cart-badge"], [class*="cart-count"]'
    };
    
    /**
     * Главная функция обновления всех счетчиков корзины
     */
    function updateAllCartBadges(cartCount) {
        console.log(`🛒 Синхронизация корзины: ${cartCount} товаров`);
        
        // 1. Обновляем основной значок в десктопной навигации
        updateBadge(CART_SELECTORS.desktop, cartCount, 'Десктопная навигация');
        
        // 2. Обновляем значок в мобильной навигации
        updateBadge(CART_SELECTORS.mobile, cartCount, 'Мобильная навигация');
        
        // 3. Обновляем плавающую корзину
        updateFloatingCartBadges(cartCount);
        
        // 4. Обновляем все дополнительные значки
        updateAdditionalBadges(cartCount);
        
        // 5. Уведомляем другие компоненты через событие
        dispatchCartUpdateEvent(cartCount);
        
        console.log(`✅ Синхронизация завершена: ${cartCount} товаров`);
    }
    
    /**
     * Обновляет конкретный значок
     */
    function updateBadge(selector, count, description) {
        const badge = document.querySelector(selector);
        if (badge) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline' : 'none';
            
            // Добавляем анимацию обновления
            badge.classList.add('badge-update');
            setTimeout(() => badge.classList.remove('badge-update'), 300);
            
            console.log(`✓ ${description}: обновлен`);
        } else {
            console.log(`⚠ ${description}: не найден (${selector})`);
        }
    }
    
    /**
     * Обновляет плавающие значки корзины
     */
    function updateFloatingCartBadges(count) {
        const floatingBadges = document.querySelectorAll(CART_SELECTORS.floating);
        
        if (floatingBadges.length > 0) {
            floatingBadges.forEach((badge, index) => {
                badge.textContent = count;
                badge.style.display = count > 0 ? 'block' : 'none';
                
                // Добавляем анимацию
                badge.classList.add('badge-update');
                setTimeout(() => badge.classList.remove('badge-update'), 300);
            });
            console.log(`✓ Плавающая корзина: обновлено ${floatingBadges.length} элементов`);
        } else {
            console.log(`⚠ Плавающая корзина: не найдена`);
        }
    }
    
    /**
     * Обновляет дополнительные значки корзины
     */
    function updateAdditionalBadges(count) {
        const additionalBadges = document.querySelectorAll(CART_SELECTORS.all);
        let updated = 0;
        
        additionalBadges.forEach(badge => {
            // Исключаем уже обработанные основные элементы
            if (badge.id !== 'cart-badge' && badge.id !== 'mobile-cart-badge') {
                badge.textContent = count;
                badge.style.display = count > 0 ? 'inline' : 'none';
                updated++;
            }
        });
        
        if (updated > 0) {
            console.log(`✓ Дополнительные значки: обновлено ${updated} элементов`);
        }
    }
    
    /**
     * Отправляет событие об обновлении корзины
     */
    function dispatchCartUpdateEvent(count) {
        const event = new CustomEvent('cartSynced', {
            detail: { 
                count: count,
                timestamp: Date.now()
            },
            bubbles: true
        });
        document.dispatchEvent(event);
    }
    
    /**
     * Получает актуальное количество товаров в корзине с сервера
     */
    async function fetchCartCount() {
        try {
            const response = await fetch('/shop/cart/count/', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            return data.count || 0;
        } catch (error) {
            console.error('Ошибка загрузки счетчика корзины:', error);
            return 0;
        }
    }
    
    /**
     * Обновляет счетчики, получая данные с сервера
     */
    async function refreshCartFromServer() {
        const count = await fetchCartCount();
        updateAllCartBadges(count);
        return count;
    }
    
    /**
     * Перехватывает AJAX запросы для автоматического обновления
     */
    function interceptCartRequests() {
        const originalFetch = window.fetch;
        
        window.fetch = function(...args) {
            return originalFetch.apply(this, args).then(response => {
                const url = args[0];
                
                // Проверяем, является ли это запросом к корзине
                if (typeof url === 'string' && isCartRequest(url)) {
                    // Клонируем ответ для обработки
                    response.clone().json().then(data => {
                        if (data.status === 'success' && data.cart_total_items !== undefined) {
                            updateAllCartBadges(data.cart_total_items);
                        }
                    }).catch(() => {
                        // Если не удалось получить данные, обновляем с сервера
                        setTimeout(refreshCartFromServer, 100);
                    });
                }
                
                return response;
            });
        };
    }
    
    /**
     * Проверяет, является ли URL запросом к корзине
     */
    function isCartRequest(url) {
        const cartUrls = [
            '/shop/add-to-cart/',
            '/shop/remove-from-cart/',
            '/shop/update-cart-item/',
            '/shop/cart/'
        ];
        
        return cartUrls.some(cartUrl => url.includes(cartUrl));
    }
    
    /**
     * Добавляет CSS стили для анимации обновления
     */
    function addAnimationStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .badge-update {
                animation: badge-pulse 0.3s ease-in-out;
                transform-origin: center;
            }
            
            @keyframes badge-pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            
            /* Улучшенные стили для значков */
            .badge {
                transition: all 0.2s ease;
            }
            
            .badge:not(.badge-update) {
                animation: none;
            }
        `;
        document.head.appendChild(style);
    }
    
    /**
     * Обработчик событий DOM
     */
    function setupEventListeners() {
        // Слушаем кастомные события обновления корзины
        document.addEventListener('cartUpdated', function(e) {
            if (e.detail && e.detail.count !== undefined) {
                updateAllCartBadges(e.detail.count);
            }
        });
        
        // Обновляем при фокусе на странице (возврат с другой вкладки)
        document.addEventListener('visibilitychange', function() {
            if (!document.hidden) {
                setTimeout(refreshCartFromServer, 500);
            }
        });
        
        // Обновляем при возврате на страницу
        window.addEventListener('pageshow', function(e) {
            if (e.persisted) {
                refreshCartFromServer();
            }
        });
    }
    
    /**
     * Инициализация системы синхронизации
     */
    function initCartSync() {
        console.log('🚀 Инициализация системы синхронизации корзины...');
        
        // Добавляем стили анимации
        addAnimationStyles();
        
        // Настраиваем слушателей событий
        setupEventListeners();
        
        // Перехватываем AJAX запросы
        interceptCartRequests();
        
        // Обновляем счетчики при загрузке
        refreshCartFromServer();
        
        console.log('✅ Система синхронизации корзины готова!');
    }
    
    // Экспортируем функции в глобальную область
    window.CartSync = {
        updateAllCartBadges,
        refreshCartFromServer,
        fetchCartCount
    };
    
    // Совместимость с существующими функциями
    window.updateAllCartBadges = updateAllCartBadges;
    window.refreshCartBadges = refreshCartFromServer;
    
    // Автоматическая инициализация при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCartSync);
    } else {
        initCartSync();
    }
    
})();
