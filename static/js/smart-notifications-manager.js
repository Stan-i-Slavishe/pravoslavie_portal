// Обновленная версия с настройками частоты
// smart-notifications-manager-v2.js

class SmartNotificationsManager {
    constructor() {
        this.sessionKey = 'notifications_intro_shown';
        this.localStorageKey = 'notifications_intro_last_shown';
        this.userVisitedKey = 'user_visited_before';
        
        // Настройки по умолчанию (можно переопределить через data-атрибуты)
        this.settings = {
            frequency: 'weekly', // session, daily, weekly, monthly, first_visit, disabled
            autoHideDelay: 8000, // 8 секунд
            enabled: true,
            mobileEnabled: true,
            text: 'Добро пожаловать! Теперь вы будете получать уведомления о новом контенте'
        };
        
        this.loadSettingsFromDOM();
        this.init();
    }

    loadSettingsFromDOM() {
        // Загружаем настройки из data-атрибутов body
        const body = document.body;
        
        if (body.dataset.notificationFrequency) {
            this.settings.frequency = body.dataset.notificationFrequency;
        }
        
        if (body.dataset.notificationText) {
            this.settings.text = body.dataset.notificationText;
        }
        
        if (body.dataset.notificationEnabled) {
            this.settings.enabled = body.dataset.notificationEnabled === 'true';
        }
        
        if (body.dataset.notificationMobileEnabled) {
            this.settings.mobileEnabled = body.dataset.notificationMobileEnabled === 'true';
        }
        
        if (body.dataset.notificationAutoHide) {
            this.settings.autoHideDelay = parseInt(body.dataset.notificationAutoHide) * 1000;
        }
    }

    init() {
        // Проверяем, включены ли уведомления
        if (!this.settings.enabled) {
            return;
        }
        
        // Проверяем мобильные устройства
        if (this.isMobile() && !this.settings.mobileEnabled) {
            return;
        }
        
        // Проверяем, нужно ли показывать уведомление
        if (this.shouldShowNotification()) {
            this.showWelcomeNotification();
        }
    }

    isMobile() {
        return window.innerWidth <= 768 || /Mobi|Android/i.test(navigator.userAgent);
    }

    shouldShowNotification() {
        const frequency = this.settings.frequency;
        
        // Если отключено
        if (frequency === 'disabled') {
            return false;
        }
        
        // Проверяем сессию для всех режимов кроме first_visit
        if (frequency !== 'first_visit' && sessionStorage.getItem(this.sessionKey)) {
            return false;
        }
        
        switch (frequency) {
            case 'session':
                // Один раз за сессию - проверяем только sessionStorage
                return !sessionStorage.getItem(this.sessionKey);
            
            case 'first_visit':
                // Только при первом посещении
                return !localStorage.getItem(this.userVisitedKey);
            
            case 'daily':
                return this.checkTimeInterval(1);
            
            case 'weekly':
                return this.checkTimeInterval(7);
            
            case 'monthly':
                return this.checkTimeInterval(30);
            
            default:
                return this.checkTimeInterval(7); // По умолчанию раз в неделю
        }
    }

    checkTimeInterval(days) {
        const lastShown = localStorage.getItem(this.localStorageKey);
        if (!lastShown) {
            return true; // Первый раз
        }
        
        const daysSinceLastShown = (Date.now() - parseInt(lastShown)) / (1000 * 60 * 60 * 24);
        return daysSinceLastShown >= days;
    }

    showWelcomeNotification() {
        // Создаем уведомление
        const notification = this.createNotificationElement();
        document.body.appendChild(notification);

        // Показываем с анимацией
        setTimeout(() => {
            notification.classList.add('show');
        }, 100);

        // Автоматически скрываем
        if (this.settings.autoHideDelay > 0) {
            setTimeout(() => {
                this.hideNotification(notification);
            }, this.settings.autoHideDelay);
        }

        // Отмечаем, что показали
        this.markAsShown();
    }

    createNotificationElement() {
        const notification = document.createElement('div');
        notification.className = 'smart-notification';
        
        // Адаптируем для мобильных
        const isMobile = this.isMobile();
        
        notification.innerHTML = `
            <div class="smart-notification-content">
                <div class="smart-notification-header">
                    <i class="fas fa-bell text-primary"></i>
                    <strong>Добро пожаловать!</strong>
                    <button class="smart-notification-close" onclick="smartNotifications.hideNotification(this.closest('.smart-notification'))">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="smart-notification-body">
                    ${this.settings.text}
                </div>
                <div class="smart-notification-actions">
                    <button class="btn btn-sm btn-primary" onclick="smartNotifications.goToSettings()">
                        ${isMobile ? 'Настроить' : 'Настроить уведомления'}
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="smartNotifications.remindLater(this.closest('.smart-notification'))">
                        ${isMobile ? 'Позже' : 'Напомнить позже'}
                    </button>
                </div>
            </div>
        `;

        return notification;
    }

    hideNotification(element) {
        element.classList.remove('show');
        setTimeout(() => {
            if (element.parentNode) {
                element.parentNode.removeChild(element);
            }
        }, 300);
    }

    markAsShown() {
        const frequency = this.settings.frequency;
        
        // Всегда отмечаем в сессии (кроме first_visit)
        if (frequency !== 'first_visit') {
            sessionStorage.setItem(this.sessionKey, 'true');
        }
        
        // Отмечаем в localStorage для временных интервалов
        if (['daily', 'weekly', 'monthly'].includes(frequency)) {
            localStorage.setItem(this.localStorageKey, Date.now().toString());
        }
        
        // Отмечаем, что пользователь посещал сайт
        localStorage.setItem(this.userVisitedKey, 'true');
    }

    goToSettings() {
        // Переходим к настройкам уведомлений
        window.location.href = '/pwa/notifications/settings/';
    }

    remindLater(element) {
        // Скрываем уведомление до конца сессии
        sessionStorage.setItem(this.sessionKey, 'true');
        this.hideNotification(element);
    }

    // Админские методы для управления
    forceShow() {
        sessionStorage.removeItem(this.sessionKey);
        localStorage.removeItem(this.localStorageKey);
        this.showWelcomeNotification();
    }

    reset() {
        sessionStorage.removeItem(this.sessionKey);
        localStorage.removeItem(this.localStorageKey);
        localStorage.removeItem(this.userVisitedKey);
    }

    // Метод для изменения настроек на лету
    updateSettings(newSettings) {
        Object.assign(this.settings, newSettings);
    }

    // Метод для получения статистики
    getStats() {
        return {
            hasVisitedBefore: !!localStorage.getItem(this.userVisitedKey),
            lastShown: localStorage.getItem(this.localStorageKey),
            sessionShown: !!sessionStorage.getItem(this.sessionKey),
            frequency: this.settings.frequency,
            enabled: this.settings.enabled
        };
    }
}

// Добавляем обновленные CSS стили
const style = document.createElement('style');
style.textContent = `
    .smart-notification {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 350px;
        max-width: calc(100vw - 40px);
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.15);
        border-left: 4px solid var(--bs-primary, #0d6efd);
        z-index: 1060;
        opacity: 0;
        transform: translateX(100%);
        transition: all 0.3s ease;
        overflow: hidden;
    }

    .smart-notification.show {
        opacity: 1;
        transform: translateX(0);
    }

    .smart-notification-content {
        padding: 1rem;
    }

    .smart-notification-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.75rem;
        position: relative;
    }

    .smart-notification-header i {
        color: var(--bs-primary, #0d6efd);
        font-size: 1.1rem;
    }

    .smart-notification-header strong {
        flex-grow: 1;
        font-size: 0.95rem;
        color: #212529;
    }

    .smart-notification-close {
        background: none;
        border: none;
        color: #6c757d;
        cursor: pointer;
        padding: 0.25rem;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
        transition: all 0.2s ease;
    }

    .smart-notification-close:hover {
        background: #f8f9fa;
        color: #495057;
        transform: scale(1.1);
    }

    .smart-notification-body {
        font-size: 0.875rem;
        color: #6c757d;
        margin-bottom: 1rem;
        line-height: 1.4;
    }

    .smart-notification-actions {
        display: flex;
        gap: 0.5rem;
        justify-content: flex-end;
    }

    .smart-notification-actions .btn {
        font-size: 0.8rem;
        padding: 0.375rem 0.75rem;
        border-radius: 6px;
        transition: all 0.2s ease;
    }

    .smart-notification-actions .btn:hover {
        transform: translateY(-1px);
    }

    /* Мобильные стили */
    @media (max-width: 768px) {
        .smart-notification {
            bottom: 10px;
            right: 10px;
            left: 10px;
            width: auto;
            max-width: none;
            border-radius: 8px;
        }

        .smart-notification-content {
            padding: 0.875rem;
        }

        .smart-notification-header {
            margin-bottom: 0.625rem;
        }

        .smart-notification-header strong {
            font-size: 0.9rem;
        }

        .smart-notification-body {
            font-size: 0.8rem;
            margin-bottom: 0.875rem;
        }

        .smart-notification-actions {
            flex-direction: column;
            gap: 0.375rem;
        }

        .smart-notification-actions .btn {
            font-size: 0.75rem;
            padding: 0.5rem;
            width: 100%;
        }
    }

    /* Анимация пульса для кнопки закрытия */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .smart-notification-close:active {
        animation: pulse 0.2s ease;
    }
`;

document.head.appendChild(style);

// Создаем глобальный экземпляр после загрузки DOM
document.addEventListener('DOMContentLoaded', function() {
    window.smartNotifications = new SmartNotificationsManager();
});

// Экспортируем класс
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SmartNotificationsManager;
}
