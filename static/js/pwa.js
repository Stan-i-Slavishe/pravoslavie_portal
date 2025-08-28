// 🚀 PWA Core functionality for Православный портал
// Версия: 1.0.0

class PWAManager {
    constructor() {
        this.isInstalled = false;
        this.deferredPrompt = null;
        this.swRegistration = null;
        
        this.init();
    }
    
    // 🚀 Инициализация PWA
    async init() {
        console.log('🚀 PWA Manager initializing...');
        
        // Регистрируем Service Worker
        await this.registerServiceWorker();
        
        // Настраиваем события установки
        this.setupInstallPrompt();
        
        // Настраиваем push-уведомления
        this.setupPushNotifications();
        
        // Настраиваем офлайн синхронизацию
        this.setupOfflineSync();
        
        // Настраиваем кеширование контента
        this.setupContentCaching();
        
        console.log('✅ PWA Manager initialized successfully!');
    }
    
    // 📦 Регистрация Service Worker
    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                this.swRegistration = await navigator.serviceWorker.register('/sw.js', {
                    scope: '/'
                });
                
                console.log('✅ Service Worker registered:', this.swRegistration.scope);
                
                // Слушаем обновления
                this.swRegistration.addEventListener('updatefound', () => {
                    const newWorker = this.swRegistration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            this.showUpdateNotification();
                        }
                    });
                });
                
            } catch (error) {
                console.error('❌ Service Worker registration failed:', error);
            }
        }
    }
    
    // 📱 Настройка промпта установки
    setupInstallPrompt() {
        // Отслеживаем событие установки
        window.addEventListener('beforeinstallprompt', (e) => {
            console.log('📱 Install prompt available');
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallButton();
        });
        
        // Отслеживаем успешную установку
        window.addEventListener('appinstalled', () => {
            console.log('✅ PWA installed successfully');
            this.isInstalled = true;
            this.hideInstallButton();
            this.showWelcomeMessage();
        });
    }
    
    // 📱 Показываем кнопку установки
    showInstallButton() {
        if (!document.getElementById('pwa-install-btn')) {
            const installBtn = document.createElement('button');
            installBtn.id = 'pwa-install-btn';
            installBtn.className = 'btn btn-primary position-fixed pwa-install-btn';
            installBtn.innerHTML = '<i class="fas fa-download"></i> Установить приложение';
            installBtn.style.cssText = `
                bottom: 20px;
                right: 20px;
                z-index: 1000;
                border-radius: 25px;
                padding: 12px 20px;
                font-weight: bold;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                animation: slideIn 0.3s ease-out;
            `;
            
            installBtn.addEventListener('click', () => this.promptInstall());
            document.body.appendChild(installBtn);
        }
    }
    
    // 📱 Прячем кнопку установки
    hideInstallButton() {
        const installBtn = document.getElementById('pwa-install-btn');
        if (installBtn) {
            installBtn.remove();
        }
    }
    
    // 📱 Запрос установки
    async promptInstall() {
        if (this.deferredPrompt) {
            this.deferredPrompt.prompt();
            const result = await this.deferredPrompt.userChoice;
            
            console.log('📱 Install prompt result:', result.outcome);
            this.deferredPrompt = null;
        }
    }
    
    // 🔔 Настройка push-уведомлений
    async setupPushNotifications() {
        if ('Notification' in window && 'serviceWorker' in navigator) {
            setTimeout(() => this.requestNotificationPermission(), 5000);
        }
    }
    
    // 🔔 Запрос разрешения на уведомления
    async requestNotificationPermission() {
        const permission = await Notification.requestPermission();
        
        if (permission === 'granted') {
            console.log('✅ Notification permission granted');
            await this.subscribeToPush();
            this.showWelcomeNotification();
        }
    }
    
    // 🔔 Подписка на push-уведомления
    async subscribeToPush() {
        try {
            const subscription = await this.swRegistration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: this.urlBase64ToUint8Array(window.VAPID_PUBLIC_KEY || '')
            });
            
            await fetch('/push/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    subscription: subscription,
                    user_agent: navigator.userAgent
                })
            });
            
            console.log('✅ Push subscription successful');
            
        } catch (error) {
            console.error('❌ Push subscription failed:', error);
        }
    }
    
    // 🔄 Настройка офлайн синхронизации
    setupOfflineSync() {
        window.addEventListener('online', () => {
            console.log('🌐 Connection restored, syncing...');
            this.syncOfflineData();
            this.showConnectionRestored();
        });
        
        window.addEventListener('offline', () => {
            console.log('📱 Gone offline, enabling offline mode');
            this.showOfflineIndicator();
        });
        
        if (navigator.onLine) {
            this.syncOfflineData();
        }
    }
    
    // 🔄 Синхронизация офлайн данных
    async syncOfflineData() {
        if ('serviceWorker' in navigator && 'sync' in window.ServiceWorkerRegistration.prototype) {
            try {
                const registration = await navigator.serviceWorker.ready;
                await registration.sync.register('playlist-sync');
                await registration.sync.register('favorites-sync');
                await registration.sync.register('cart-sync');
                
                console.log('✅ Background sync registered');
            } catch (error) {
                console.error('❌ Background sync failed:', error);
            }
        }
    }
    
    // 📚 Кеширование контента для офлайн
    setupContentCaching() {
        this.cacheCurrentPage();
        this.setupSmartCaching();
    }
    
    // 📚 Кеширование текущей страницы
    async cacheCurrentPage() {
        if ('serviceWorker' in navigator) {
            try {
                const cache = await caches.open('pravoslavie-portal-v1-pages');
                await cache.add(window.location.pathname);
                console.log('📚 Current page cached');
            } catch (error) {
                console.error('❌ Page caching failed:', error);
            }
        }
    }
    
    // 🧠 Умное кеширование
    setupSmartCaching() {
        if (window.location.pathname.includes('/fairy-tales/')) {
            this.cacheFairyTales();
        }
        
        document.addEventListener('click', (e) => {
            if (e.target.closest('.download-book-btn')) {
                const bookId = e.target.dataset.bookId;
                this.cacheBook(bookId);
            }
        });
    }
    
    // 🧚 Кеширование сказок
    async cacheFairyTales() {
        try {
            const cache = await caches.open('pravoslavie-portal-v1-fairy-tales');
            const categories = ['straxi', 'samoocenka', 'otnosheniya', 'povedenie'];
            for (const category of categories) {
                await cache.add(`/fairy-tales/category/${category}/`);
            }
            console.log('🧚 Fairy tales cached for offline');
        } catch (error) {
            console.error('❌ Fairy tales caching failed:', error);
        }
    }
    
    // 📖 Кеширование книги
    async cacheBook(bookId) {
        try {
            const cache = await caches.open('pravoslavie-portal-v1-books');
            await cache.add(`/books/${bookId}/`);
            console.log(`📖 Book ${bookId} cached`);
        } catch (error) {
            console.error(`❌ Book ${bookId} caching failed:`, error);
        }
    }
    
    // 🎉 Показываем welcome сообщение после установки
    showWelcomeMessage() {
        this.showToast('🎉 Приложение установлено! Теперь вы можете пользоваться им офлайн', 'success');
    }
    
    // 🔔 Welcome уведомление
    showWelcomeNotification() {
        if ('serviceWorker' in navigator && this.swRegistration) {
            this.swRegistration.showNotification('Добро пожаловать!', {
                body: 'Теперь вы будете получать уведомления о новом контенте',
                icon: '/static/icons/icon-192x192.png',
                tag: 'welcome'
            });
        }
    }
    
    // 🌐 Показываем индикатор восстановления соединения
    showConnectionRestored() {
        this.showToast('🌐 Соединение восстановлено. Данные синхронизированы!', 'success');
    }
    
    // 📱 Показываем индикатор офлайн режима
    showOfflineIndicator() {
        this.showToast('📱 Работаем в офлайн режиме. Ваши действия будут синхронизированы позже.', 'info');
    }
    
    // 🔄 Уведомление об обновлении
    showUpdateNotification() {
        this.showToast('🔄 Доступно обновление приложения. Перезагрузите страницу для обновления.', 'info');
    }
    
    // 🍞 Универсальный toast
    showToast(message, type = 'info', duration = 5000) {
        let toastContainer = document.getElementById('pwa-toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'pwa-toast-container';
            toastContainer.className = 'position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '9999';
            document.body.appendChild(toastContainer);
        }
        
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} alert-dismissible fade show`;
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        toastContainer.appendChild(toast);
        
        if (duration > 0) {
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.remove();
                }
            }, duration);
        }
    }
    
    // 🔧 Вспомогательные функции
    getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='));
        return cookieValue ? cookieValue.split('=')[1] : '';
    }
    
    urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding)
            .replace(/-/g, '+')
            .replace(/_/g, '/');
        
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }
}

// 🎯 Православные PWA функции
class OrthodoxyPWAFeatures {
    constructor(pwaManager) {
        this.pwa = pwaManager;
        this.setupOrthodoxyFeatures();
    }
    
    setupOrthodoxyFeatures() {
        this.setupBedtimeReminders();
        this.setupOrthodoxyCalendar();
        this.setupFamilySync();
        this.setupChildMode();
    }
    
    setupBedtimeReminders() {
        setInterval(() => {
            const now = new Date();
            const hour = now.getHours();
            
            if (hour === 19 && now.getMinutes() === 0) {
                this.sendBedtimeReminder();
            }
        }, 60000);
    }
    
    sendBedtimeReminder() {
        if ('serviceWorker' in navigator && this.pwa.swRegistration) {
            this.pwa.swRegistration.showNotification('Время сказки! 🌙', {
                body: 'Выберите добрую сказку для вашего малыша перед сном',
                icon: '/static/icons/icon-192x192.png',
                tag: 'bedtime_reminder',
                data: { url: '/fairy-tales/', type: 'bedtime_story' }
            });
        }
    }
    
    setupOrthodoxyCalendar() {
        setInterval(() => {
            const now = new Date();
            if (now.getHours() === 9 && now.getMinutes() === 0) {
                this.checkOrthodoxyCalendar();
            }
        }, 60000);
    }
    
    async checkOrthodoxyCalendar() {
        try {
            const response = await fetch('/api/orthodoxy-calendar/today/');
            const data = await response.json();
            
            if (data.events && data.events.length > 0) {
                for (const event of data.events) {
                    this.sendOrthodoxyNotification(event);
                }
            }
        } catch (error) {
            console.error('❌ Orthodox calendar check failed:', error);
        }
    }
    
    sendOrthodoxyNotification(event) {
        if ('serviceWorker' in navigator && this.pwa.swRegistration) {
            this.pwa.swRegistration.showNotification(`⛪ ${event.name}`, {
                body: 'Послушайте тематические рассказы и почитайте духовную литературу',
                icon: '/static/icons/icon-192x192.png',
                tag: `orthodox_${event.id}`,
                data: { url: `/stories/category/${event.category}/`, type: 'orthodox_calendar' }
            });
        }
    }
    
    setupFamilySync() {
        if ('serviceWorker' in navigator) {
            setInterval(async () => {
                try {
                    const registration = await navigator.serviceWorker.ready;
                    await registration.sync.register('family-sync');
                } catch (error) {
                    console.error('❌ Family sync failed:', error);
                }
            }, 300000);
        }
    }
    
    setupChildMode() {
        const isChildMode = localStorage.getItem('childMode') === 'true';
        
        if (isChildMode) {
            this.enableChildMode();
        }
    }
    
    enableChildMode() {
        document.body.classList.add('child-mode');
        
        if (!document.getElementById('child-mode-styles')) {
            const childModeStyles = document.createElement('style');
            childModeStyles.id = 'child-mode-styles';
            childModeStyles.textContent = `
                .child-mode { font-size: 1.2em !important; }
                .child-mode .btn { 
                    padding: 15px 25px !important;
                    font-size: 1.1em !important;
                    border-radius: 15px !important;
                }
                .child-mode .card {
                    border-radius: 15px !important;
                    border-width: 3px !important;
                }
                .child-mode .fairy-tale-card {
                    background: linear-gradient(45deg, #FFE0B2, #FFCC80) !important;
                }
            `;
            document.head.appendChild(childModeStyles);
        }
    }
}

// 🚀 Инициализация PWA при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing PWA...');
    
    // Создаем глобальные объекты PWA
    window.pwaManager = new PWAManager();
    window.orthodoxyFeatures = new OrthodoxyPWAFeatures(window.pwaManager);
    
    // Добавляем CSS анимации
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        .pwa-install-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
    `;
    document.head.appendChild(style);
    
    console.log('✅ PWA initialization complete!');
});
