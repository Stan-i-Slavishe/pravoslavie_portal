/* 
 * PRODUCTION ANALYTICS SYSTEM
 * Полноценная система аналитики без заглушек
 * Отслеживает поведение пользователей, покупки, просмотры
 */

class ProductionAnalytics {
    constructor() {
        this.sessionId = this.generateSessionId();
        this.userId = this.getUserId();
        this.debug = window.DEBUG || false;
        this.init();
    }
    
    init() {
        this.trackPageView();
        this.bindEvents();
        this.startSessionTracking();
        if (this.debug) console.log('📊 Аналитика инициализирована');
    }
    
    // Генерация уникального ID сессии
    generateSessionId() {
        const stored = sessionStorage.getItem('analytics_session_id');
        if (stored) return stored;
        
        const sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        sessionStorage.setItem('analytics_session_id', sessionId);
        return sessionId;
    }
    
    // Получение ID пользователя
    getUserId() {
        const userIdMeta = document.querySelector('meta[name="user-id"]');
        return userIdMeta ? userIdMeta.content : null;
    }
    
    // Отслеживание просмотра страницы
    trackPageView() {
        this.sendEvent('page_view', {
            page_url: window.location.href,
            page_title: document.title,
            referrer: document.referrer,
            user_agent: navigator.userAgent,
            screen_resolution: `${screen.width}x${screen.height}`,
            timestamp: new Date().toISOString()
        });
    }
    
    // Отслеживание покупок (реальных, не заглушек!)
    trackPurchase(productId, productType, amount, currency = 'RUB') {
        this.sendEvent('purchase', {
            product_id: productId,
            product_type: productType,
            amount: amount,
            currency: currency,
            payment_method: 'test', // Можно будет изменить на real
            timestamp: new Date().toISOString()
        });
        
        if (this.debug) console.log('💰 Отслежена покупка:', productId);
    }
    
    // Отслеживание добавления в корзину
    trackAddToCart(productId, productType, price) {
        this.sendEvent('add_to_cart', {
            product_id: productId,
            product_type: productType,
            price: price,
            timestamp: new Date().toISOString()
        });
    }
    
    // Отслеживание скачиваний
    trackDownload(itemId, itemType, format = 'pdf') {
        this.sendEvent('download', {
            item_id: itemId,
            item_type: itemType,
            format: format,
            timestamp: new Date().toISOString()
        });
        
        if (this.debug) console.log('📥 Отслежено скачивание:', itemId);
    }
    
    // Отслеживание лайков и взаимодействий
    trackInteraction(action, targetId, targetType) {
        this.sendEvent('interaction', {
            action: action, // like, dislike, share, bookmark
            target_id: targetId,
            target_type: targetType,
            timestamp: new Date().toISOString()
        });
    }
    
    // Отслеживание поиска
    trackSearch(query, resultsCount, category = null) {
        this.sendEvent('search', {
            query: query,
            results_count: resultsCount,
            category: category,
            timestamp: new Date().toISOString()
        });
    }
    
    // Отслеживание времени на странице
    startSessionTracking() {
        this.sessionStartTime = Date.now();
        this.lastActivityTime = Date.now();
        
        // Отслеживаем активность
        ['click', 'scroll', 'keypress', 'mousemove'].forEach(event => {
            document.addEventListener(event, () => {
                this.lastActivityTime = Date.now();
            });
        });
        
        // Отправляем данные о сессии при выходе
        window.addEventListener('beforeunload', () => {
            this.trackSessionEnd();
        });
        
        // Периодически отправляем данные о времени на странице
        setInterval(() => {
            this.trackTimeOnPage();
        }, 30000); // Каждые 30 секунд
    }
    
    trackSessionEnd() {
        const sessionDuration = Date.now() - this.sessionStartTime;
        const activeTime = this.lastActivityTime - this.sessionStartTime;
        
        this.sendEvent('session_end', {
            session_duration: sessionDuration,
            active_time: activeTime,
            pages_viewed: this.pagesViewed || 1,
            timestamp: new Date().toISOString()
        }, true); // Синхронный запрос
    }
    
    trackTimeOnPage() {
        const timeOnPage = Date.now() - this.sessionStartTime;
        this.sendEvent('time_on_page', {
            time_seconds: Math.floor(timeOnPage / 1000),
            timestamp: new Date().toISOString()
        });
    }
    
    // Привязка событий к элементам
    bindEvents() {
        // Покупки в магазине
        document.addEventListener('click', (e) => {
            // Кнопки покупки
            if (e.target.matches('[data-product-id]')) {
                const productId = e.target.dataset.productId;
                const productType = e.target.dataset.productType;
                const price = e.target.dataset.price;
                
                if (e.target.textContent.includes('Купить') || e.target.textContent.includes('В корзину')) {
                    this.trackAddToCart(productId, productType, price);
                }
            }
            
            // Скачивания
            if (e.target.matches('[data-download-id]')) {
                const itemId = e.target.dataset.downloadId;
                const itemType = e.target.dataset.downloadType;
                this.trackDownload(itemId, itemType);
            }
            
            // Лайки и взаимодействия
            if (e.target.matches('.like-button')) {
                const targetId = e.target.dataset.targetId;
                const targetType = e.target.dataset.targetType;
                this.trackInteraction('like', targetId, targetType);
            }
            
            if (e.target.matches('.share-button')) {
                const targetId = e.target.dataset.targetId;
                const targetType = e.target.dataset.targetType;
                this.trackInteraction('share', targetId, targetType);
            }
        });
        
        // Поиск
        const searchForms = document.querySelectorAll('form[role="search"], .search-form');
        searchForms.forEach(form => {
            form.addEventListener('submit', (e) => {
                const query = form.querySelector('input[type="search"], input[name="q"]').value;
                this.trackSearch(query, null);
            });
        });
    }
    
    // Отправка события на сервер
    sendEvent(eventType, data, sync = false) {
        const payload = {
            event_type: eventType,
            session_id: this.sessionId,
            user_id: this.userId,
            data: data,
            timestamp: new Date().toISOString(),
            csrf_token: this.getCSRFToken()
        };
        
        const url = '/analytics/track-event/';
        
        if (sync) {
            // Синхронный запрос для критичных событий
            navigator.sendBeacon(url, JSON.stringify(payload));
        } else {
            // Асинхронный запрос
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify(payload),
                credentials: 'same-origin'
            }).catch(error => {
                if (this.debug) console.error('Analytics error:', error);
            });
        }
        
        if (this.debug) console.log(`📊 Событие отправлено: ${eventType}`, data);
    }
    
    // Получение CSRF токена
    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
    
    // Публичные методы для использования в шаблонах
    static trackPurchaseComplete(orderId, totalAmount, items) {
        if (window.analytics) {
            window.analytics.sendEvent('purchase_complete', {
                order_id: orderId,
                total_amount: totalAmount,
                items: items,
                timestamp: new Date().toISOString()
            });
        }
    }
    
    static trackFormSubmission(formName, formData = {}) {
        if (window.analytics) {
            window.analytics.sendEvent('form_submission', {
                form_name: formName,
                form_data: formData,
                timestamp: new Date().toISOString()
            });
        }
    }
    
    static trackError(errorType, errorMessage, errorPage) {
        if (window.analytics) {
            window.analytics.sendEvent('error', {
                error_type: errorType,
                error_message: errorMessage,
                error_page: errorPage,
                timestamp: new Date().toISOString()
            });
        }
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    window.analytics = new ProductionAnalytics();
});

// Глобальные функции для быстрого доступа
window.trackPurchase = (productId, productType, amount) => {
    if (window.analytics) window.analytics.trackPurchase(productId, productType, amount);
};

window.trackDownload = (itemId, itemType) => {
    if (window.analytics) window.analytics.trackDownload(itemId, itemType);
};

window.trackSearch = (query, resultsCount) => {
    if (window.analytics) window.analytics.trackSearch(query, resultsCount);
};
