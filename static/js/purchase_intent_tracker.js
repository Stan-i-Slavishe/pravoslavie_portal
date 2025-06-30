// static/js/purchase_intent_tracker.js

class PurchaseIntentTracker {
    constructor() {
        this.setupEventListeners();
        this.sessionId = this.getOrCreateSessionId();
    }
    
    setupEventListeners() {
        // Отслеживаем все клики на заглушки покупок
        document.addEventListener('click', (e) => {
            const button = e.target.closest('[data-purchase-intent]');
            if (button) {
                e.preventDefault(); // Предотвращаем действие по умолчанию
                this.trackPurchaseIntent(button);
                this.showComingSoonModal(button);
            }
        });
        
        // Отслеживаем клики на подписку на уведомления
        document.addEventListener('click', (e) => {
            const notifyButton = e.target.closest('[data-notify-launch]');
            if (notifyButton) {
                this.showNotificationSubscription(notifyButton);
            }
        });
    }
    
    async trackPurchaseIntent(button) {
        const data = {
            content_type: button.dataset.contentType,
            object_id: button.dataset.objectId,
            button_type: button.dataset.buttonType,
            page_url: window.location.href,
            referer: document.referrer,
            session_key: this.sessionId,
            user_agent: navigator.userAgent,
            timestamp: new Date().toISOString()
        };
        
        try {
            const response = await fetch('/analytics/track-purchase-intent/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            console.log('Purchase intent tracked:', result);
            
            // Обновляем счетчик для админки
            this.updateClickCounter(button, result.total_clicks);
            
        } catch (error) {
            console.error('Error tracking purchase intent:', error);
        }
    }
    
    showComingSoonModal(button) {
        const contentType = button.dataset.contentType;
        const buttonType = button.dataset.buttonType;
        
        // Создаем модальное окно
        const modal = document.createElement('div');
        modal.className = 'purchase-intent-modal';
        modal.innerHTML = `
            <div class="modal-overlay">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3>🚀 Скоро запуск!</h3>
                        <button class="modal-close">&times;</button>
                    </div>
                    <div class="modal-body">
                        <p>Мы работаем над запуском системы оплаты!</p>
                        <p>Хотите получить уведомление, когда ${this.getContentTypeName(contentType)} 
                           станет доступен для покупки?</p>
                        
                        <form class="notify-form">
                            <input type="email" placeholder="Ваш email" required class="email-input">
                            <input type="hidden" name="interested_in" value="${contentType}">
                            <input type="hidden" name="button_type" value="${buttonType}">
                            <button type="submit" class="btn-notify">Уведомить меня!</button>
                        </form>
                        
                        <div class="social-share">
                            <p>А пока поделитесь с друзьями:</p>
                            <div class="share-buttons">
                                <button onclick="shareToTelegram()" class="btn-telegram">Telegram</button>
                                <button onclick="shareToVK()" class="btn-vk">VKontakte</button>
                                <button onclick="shareToWhatsApp()" class="btn-whatsapp">WhatsApp</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Обработчики для модального окна
        modal.querySelector('.modal-close').onclick = () => modal.remove();
        modal.querySelector('.modal-overlay').onclick = (e) => {
            if (e.target === modal.querySelector('.modal-overlay')) {
                modal.remove();
            }
        };
        
        // Обработка формы подписки
        modal.querySelector('.notify-form').onsubmit = (e) => {
            e.preventDefault();
            this.submitNotificationRequest(e.target, modal);
        };
    }
    
    async submitNotificationRequest(form, modal) {
        const formData = new FormData(form);
        const data = {
            email: formData.get('email'),
            interested_in: formData.get('interested_in'),
            button_type: formData.get('button_type'),
            source_page: window.location.href
        };
        
        try {
            const response = await fetch('/analytics/subscribe-notifications/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                modal.querySelector('.modal-body').innerHTML = `
                    <div class="success-message">
                        <h4>✅ Спасибо за подписку!</h4>
                        <p>Мы обязательно уведомим вас о запуске!</p>
                        <p><small>Проверьте почту для подтверждения подписки.</small></p>
                    </div>
                `;
                
                setTimeout(() => modal.remove(), 3000);
            } else {
                alert('Ошибка подписки: ' + result.error);
            }
            
        } catch (error) {
            console.error('Error subscribing:', error);
            alert('Произошла ошибка. Попробуйте позже.');
        }
    }
    
    updateClickCounter(button, totalClicks) {
        // Показываем админу количество кликов
        if (document.body.classList.contains('admin-user')) {
            let counter = button.querySelector('.click-counter');
            if (!counter) {
                counter = document.createElement('span');
                counter.className = 'click-counter';
                button.appendChild(counter);
            }
            counter.textContent = `(${totalClicks} кликов)`;
        }
    }
    
    getContentTypeName(contentType) {
        const names = {
            'book': 'книга',
            'fairy_tale': 'сказка',
            'subscription': 'подписка',
            'audio': 'аудио'
        };
        return names[contentType] || 'контент';
    }
    
    getOrCreateSessionId() {
        let sessionId = sessionStorage.getItem('purchase_intent_session');
        if (!sessionId) {
            sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('purchase_intent_session', sessionId);
        }
        return sessionId;
    }
    
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.querySelector('meta[name="csrf-token"]')?.content || '';
    }
}

// Социальные функции
function shareToTelegram() {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent('Отличный православный портал с терапевтическими сказками!');
    window.open(`https://t.me/share/url?url=${url}&text=${text}`, '_blank');
}

function shareToVK() {
    const url = encodeURIComponent(window.location.href);
    window.open(`https://vk.com/share.php?url=${url}`, '_blank');
}

function shareToWhatsApp() {
    const url = encodeURIComponent(window.location.href);
    const text = encodeURIComponent('Посмотри этот интересный православный портал!');
    window.open(`https://wa.me/?text=${text} ${url}`, '_blank');
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new PurchaseIntentTracker();
});
