// analytics.js - Отслеживание покупательских намерений

class PurchaseAnalytics {
    constructor() {
        this.init();
    }

    init() {
        // Получаем session key
        this.sessionKey = this.getSessionKey();
        
        // Инициализируем отслеживание кликов
        this.initClickTracking();
        
        console.log('📊 Purchase Analytics initialized');
    }

    getSessionKey() {
        // Получаем session key из cookies или создаем временный
        const sessionId = this.getCookie('sessionid') || this.generateSessionKey();
        return sessionId;
    }

    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    generateSessionKey() {
        return 'anon_' + Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
    }

    getCSRFToken() {
        return this.getCookie('csrftoken') || 
               document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
               document.querySelector('meta[name=csrf-token]')?.getAttribute('content');
    }

    initClickTracking() {
        // Флаг для предотвращения дублирования
        this.isTracking = false;
        
        // Отслеживаем клики на кнопки покупки/скачивания
        document.addEventListener('click', (e) => {
            // Предотвращаем множественное срабатывание
            if (this.isTracking) return;
            
            const target = e.target.closest('[data-analytics-track]');
            if (target) {
                this.isTracking = true;
                this.trackPurchaseIntent(target, e);
                // Сбрасываем флаг через 1 секунду
                setTimeout(() => this.isTracking = false, 1000);
                return; // Выходим, чтобы не сработал второй обработчик
            }
            
            // Отслеживаем клики на ссылки "Купить" и похожие (только если нет data-analytics-track)
            const button = e.target.closest('a, button');
            if (button && !button.hasAttribute('data-analytics-track') && this.isPurchaseButton(button)) {
                this.isTracking = true;
                this.trackGenericPurchaseIntent(button, e);
                // Сбрасываем флаг через 1 секунду
                setTimeout(() => this.isTracking = false, 1000);
            }
        });
    }

    isPurchaseButton(element) {
        const text = element.textContent.toLowerCase();
        const href = element.href?.toLowerCase() || '';
        
        // Проверяем текст кнопки/ссылки
        const purchaseKeywords = [
            'купить', 'скачать', 'приобрести', 'заказать', 'подписаться',
            'оформить', 'получить доступ', 'разблокировать', 'premium'
        ];
        
        // Проверяем классы
        const classList = element.className.toLowerCase();
        const purchaseClasses = ['btn-buy', 'btn-download', 'btn-purchase', 'btn-subscribe'];
        
        return purchaseKeywords.some(keyword => text.includes(keyword)) ||
               purchaseClasses.some(cls => classList.includes(cls)) ||
               href.includes('buy') || href.includes('purchase') || href.includes('subscribe');
    }

    trackPurchaseIntent(element, event) {
        const data = {
            content_type: element.dataset.contentType || this.detectContentType(),
            object_id: element.dataset.objectId || this.detectObjectId(),
            button_type: element.dataset.buttonType || this.detectButtonType(element),
            session_key: this.sessionKey,
            page_url: window.location.href,
            referer: document.referrer,
            timestamp: new Date().toISOString()
        };

        // Приоритет data-атрибутам над автоопределением
        if (element.dataset.contentType) {
            data.content_type = element.dataset.contentType;
        }
        if (element.dataset.objectId) {
            data.object_id = parseInt(element.dataset.objectId);
        }

        this.sendAnalytics(data, element);
    }

    trackGenericPurchaseIntent(element, event) {
        // Автоматическое определение типа контента и действия
        const data = {
            content_type: element.dataset.contentType || this.detectContentType(),
            object_id: element.dataset.objectId || this.detectObjectId(),
            button_type: element.dataset.buttonType || this.detectButtonType(element),
            session_key: this.sessionKey,
            page_url: window.location.href,
            referer: document.referrer,
            timestamp: new Date().toISOString()
        };

        // Приоритет data-атрибутам
        if (element.dataset.contentType) {
            data.content_type = element.dataset.contentType;
        }
        if (element.dataset.objectId) {
            data.object_id = parseInt(element.dataset.objectId);
        }

        // Если это кнопка покупки, но нет данных - не отправляем
        if (!data.content_type || !data.object_id) {
            console.log('⚠️ Insufficient data for analytics:', data);
            return;
        }

        this.sendAnalytics(data, element);
    }

    detectContentType() {
        const url = window.location.pathname;
        
        if (url.includes('/books/')) return 'book';
        if (url.includes('/fairy-tales/')) return 'fairy_tale';
        if (url.includes('/audio/')) return 'audio';
        if (url.includes('/subscriptions/')) return 'subscription';
        if (url.includes('/shop/')) return 'product';
        
        return 'unknown';
    }

    detectObjectId() {
        // Пытаемся извлечь ID из URL
        const url = window.location.pathname;
        const idMatch = url.match(/\/(\d+)\//) || url.match(/\/(\d+)$/);
        
        if (idMatch) {
            return parseInt(idMatch[1]);
        }

        // Пытаемся найти в мета-тегах
        const metaId = document.querySelector('meta[name="object-id"]');
        if (metaId) {
            return parseInt(metaId.getAttribute('content'));
        }

        // Пытаемся найти в data-атрибутах
        const elementWithId = document.querySelector('[data-object-id]');
        if (elementWithId) {
            return parseInt(elementWithId.dataset.objectId);
        }

        return null;
    }

    detectButtonType(element) {
        const text = element.textContent.toLowerCase();
        
        if (text.includes('купить') || text.includes('приобрести')) return 'buy';
        if (text.includes('скачать')) return 'download';
        if (text.includes('подписаться') || text.includes('подписка')) return 'subscribe';
        if (text.includes('слушать') || text.includes('играть')) return 'listen';
        if (text.includes('читать')) return 'read_full';
        if (text.includes('премиум') || text.includes('premium')) return 'upgrade';
        
        return 'buy'; // по умолчанию
    }

    async sendAnalytics(data, element) {
        try {
            console.log('📊 Tracking purchase intent:', {
                ...data,
                element_info: {
                    tagName: element.tagName,
                    className: element.className,
                    textContent: element.textContent?.trim().substring(0, 30),
                    datasets: element.dataset
                }
            });

            const response = await fetch('/analytics/track-purchase-intent/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const result = await response.json();
                console.log('✅ Analytics tracked:', result);
                
                // Визуальная обратная связь
                this.showTrackingFeedback(element, result);
                
                // Показываем предложение подписки на уведомления
                this.maybeShowSubscriptionOffer(result);
                
            } else {
                console.error('❌ Analytics error:', response.status, await response.text());
            }
        } catch (error) {
            console.error('❌ Analytics failed:', error);
        }
    }

    showTrackingFeedback(element, result) {
        // Кратковременная анимация кнопки
        const originalTransform = element.style.transform;
        element.style.transform = 'scale(1.05)';
        element.style.transition = 'transform 0.2s ease';
        
        setTimeout(() => {
            element.style.transform = originalTransform;
        }, 200);

        // Показываем количество кликов, если > 1
        if (result.total_clicks > 1) {
            this.showClickCounter(element, result.total_clicks);
        }
    }

    showClickCounter(element, clicks) {
        // Создаем всплывающую подсказку с количеством кликов
        const tooltip = document.createElement('div');
        tooltip.className = 'analytics-tooltip';
        tooltip.innerHTML = `
            <small>
                <i class="fas fa-mouse-pointer"></i> 
                ${clicks} раз${clicks > 4 ? '' : clicks > 1 ? 'а' : ''}
            </small>
        `;
        tooltip.style.cssText = `
            position: absolute;
            background: #333;
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            z-index: 1000;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
            transform: translateX(-50%);
        `;

        // Позиционируем относительно кнопки
        const rect = element.getBoundingClientRect();
        tooltip.style.left = (rect.left + rect.width / 2) + 'px';
        tooltip.style.top = (rect.top - 35) + 'px';

        document.body.appendChild(tooltip);

        // Анимация появления и исчезновения
        setTimeout(() => tooltip.style.opacity = '1', 10);
        setTimeout(() => {
            tooltip.style.opacity = '0';
            setTimeout(() => document.body.removeChild(tooltip), 300);
        }, 2000);
    }

    maybeShowSubscriptionOffer(result) {
        // Показываем предложение подписки после 3+ кликов
        if (result.total_clicks >= 3 && !this.hasSubscriptionOffer() && result.user_probability > 50) {
            setTimeout(() => this.showSubscriptionModal(), 1000);
        }
    }

    hasSubscriptionOffer() {
        return localStorage.getItem('subscription_offer_shown') === 'true';
    }

    showSubscriptionModal() {
        // Создаем модальное окно с предложением подписки
        const modal = document.createElement('div');
        modal.className = 'analytics-subscription-modal';
        modal.innerHTML = `
            <div class="modal-overlay" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.7);
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
            ">
                <div class="modal-content" style="
                    background: white;
                    border-radius: 15px;
                    padding: 30px;
                    max-width: 400px;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                ">
                    <h3 style="color: #2B5AA0; margin-bottom: 15px;">
                        🔔 Не пропустите запуск!
                    </h3>
                    <p style="margin-bottom: 20px; color: #666;">
                        Мы видим, что вас интересует наш контент. 
                        Подпишитесь на уведомления и узнайте первыми о запуске системы покупок!
                    </p>
                    <input type="email" placeholder="Ваш email" id="subscription-email" style="
                        width: 100%;
                        padding: 12px;
                        border: 2px solid #ddd;
                        border-radius: 8px;
                        margin-bottom: 15px;
                        font-size: 14px;
                    ">
                    <div style="display: flex; gap: 10px;">
                        <button id="subscribe-btn" style="
                            flex: 1;
                            background: #2B5AA0;
                            color: white;
                            border: none;
                            padding: 12px;
                            border-radius: 8px;
                            cursor: pointer;
                            font-weight: 600;
                        ">
                            Подписаться
                        </button>
                        <button id="close-modal-btn" style="
                            background: #ddd;
                            color: #666;
                            border: none;
                            padding: 12px 15px;
                            border-radius: 8px;
                            cursor: pointer;
                        ">
                            Позже
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        
        // 🔧 Добавляем обработчики событий после создания
        const subscribeBtn = modal.querySelector('#subscribe-btn');
        const closeBtn = modal.querySelector('#close-modal-btn');
        
        subscribeBtn.addEventListener('click', () => this.subscribeToNotifications());
        closeBtn.addEventListener('click', () => this.closeSubscriptionModal());
        
        // Закрытие по клику вне модального окна
        const overlay = modal.querySelector('.modal-overlay');
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.closeSubscriptionModal();
            }
        });
        
        localStorage.setItem('subscription_offer_shown', 'true');
    }

    async subscribeToNotifications() {
        const email = document.getElementById('subscription-email').value;
        
        if (!email || !email.includes('@')) {
            alert('Пожалуйста, введите корректный email');
            return;
        }

        try {
            const response = await fetch('/analytics/subscribe-notifications/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    email: email,
                    source_page: window.location.href,
                    interested_in: this.detectContentType()
                })
            });

            if (response.ok) {
                const result = await response.json();
                alert('Спасибо! Мы уведомим вас о запуске 📧');
                this.closeSubscriptionModal();
            } else {
                alert('Ошибка подписки. Попробуйте позже.');
            }
        } catch (error) {
            console.error('Subscription error:', error);
            alert('Ошибка подписки. Попробуйте позже.');
        }
    }

    closeSubscriptionModal() {
        const modal = document.querySelector('.analytics-subscription-modal');
        if (modal) {
            modal.remove();
        }
    }
}

// Инициализируем аналитику при загрузке страницы
let analytics;
document.addEventListener('DOMContentLoaded', function() {
    analytics = new PurchaseAnalytics();
    
    // 🔧 Добавляем глобальные функции для тестирования
    window.showCTAModal = () => {
        if (analytics) {
            analytics.showSubscriptionModal();
        } else {
            console.error('Analytics not initialized');
        }
    };
    
    // 🐛 ОТЛАДКА: Проверяем, есть ли CTA блок в DOM
    const existingCTA = document.querySelector('.cta-section');
    if (existingCTA) {
        console.log('🎯 Найден CTA блок в DOM:', existingCTA);
        console.log('🔗 Кнопки в CTA:', existingCTA.querySelectorAll('a, button'));
        
        // Добавляем обработчики событий к существующим кнопкам
        const ctaButtons = existingCTA.querySelectorAll('a, button');
        ctaButtons.forEach((btn, index) => {
            console.log(`🔘 Кнопка ${index + 1}:`, btn.textContent.trim(), 'href:', btn.href);
            
            btn.addEventListener('click', function(e) {
                console.log('🖱️ КЛИК по кнопке CTA:', this.textContent.trim());
                console.log('🔗 URL:', this.href);
                
                // Проверяем, работает ли ссылка
                if (!this.href || this.href.includes('#') || this.href === 'javascript:void(0)') {
                    e.preventDefault();
                    alert('🔧 Эта кнопка в разработке. Текст: ' + this.textContent.trim());
                    return false;
                }
                
                // Если это email ссылка
                if (this.href.startsWith('mailto:')) {
                    console.log('📧 Открываем email клиент');
                    return true; // Позволяем переход
                }
            });
        });
    } else {
        console.log('❌ CTA блок НЕ найден в DOM');
    }
    
    // Автоматический показ модального окна отключен
    // analytics.showSubscriptionModal() вызывается только после 3+ кликов
    
    // 🔧 ОТЛАДКА: Отключаем все автоматические модальные окна
    console.log('🔍 Analytics.js загружен, автомодалки отключены');
    
    // Блокируем функции, которые могут показывать модальные окна
    window.showSubscribePopup = function() {
        console.log('⚠️ showSubscribePopup заблокирована');
        return false;
    };
});

// Экспортируем для использования в других скриптах
window.analytics = analytics;