// Управление уведомлениями на основе админских настроек
// admin-controlled-notifications.js

class AdminControlledNotifications {
    constructor() {
        this.activeCategories = new Set();
        this.loadActiveCategories();
    }

    async loadActiveCategories() {
        try {
            const response = await fetch('/pwa/api/notification-categories/');
            const data = await response.json();
            
            if (data.categories) {
                // Сохраняем только активные категории
                this.activeCategories.clear();
                data.categories.forEach(category => {
                    if (category.is_active) {
                        this.activeCategories.add(category.name);
                    }
                });
                
                console.log(`Загружено ${this.activeCategories.size} активных категорий уведомлений`);
                this.updateNotificationUI();
            }
        } catch (error) {
            console.error('Ошибка загрузки категорий уведомлений:', error);
        }
    }

    updateNotificationUI() {
        // Обновляем UI на странице настроек уведомлений
        const notificationCategories = document.querySelectorAll('[data-notification-category]');
        
        notificationCategories.forEach(categoryElement => {
            const categoryName = categoryElement.getAttribute('data-notification-category');
            const isActive = this.activeCategories.has(categoryName);
            
            // Показываем/скрываем категорию
            if (isActive) {
                categoryElement.style.display = 'block';
                categoryElement.classList.remove('disabled');
            } else {
                categoryElement.style.display = 'none';
                categoryElement.classList.add('disabled');
                
                // Отключаем переключатель если категория неактивна
                const toggle = categoryElement.querySelector('input[type="checkbox"]');
                if (toggle) {
                    toggle.checked = false;
                    toggle.disabled = true;
                }
            }
        });

        // Обновляем счетчик активных категорий
        this.updateCategoryCounter();
    }

    updateCategoryCounter() {
        const counterElement = document.getElementById('active-categories-count');
        if (counterElement) {
            counterElement.textContent = this.activeCategories.size;
        }
    }

    isCategoryActive(categoryName) {
        return this.activeCategories.has(categoryName);
    }

    // Метод для проверки перед отправкой уведомления
    canSendNotification(categoryName) {
        if (!this.activeCategories.has(categoryName)) {
            console.warn(`Категория "${categoryName}" неактивна. Уведомление не отправлено.`);
            return false;
        }
        return true;
    }

    // Refresh метод для обновления списка (например, после изменений в админке)
    async refresh() {
        await this.loadActiveCategories();
    }
}

// Глобальный экземпляр
window.adminNotifications = new AdminControlledNotifications();

// Обновляем список каждые 5 минут (на случай изменений в админке)
setInterval(() => {
    window.adminNotifications.refresh();
}, 5 * 60 * 1000);

// Также обновляем при получении фокуса на странице
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        window.adminNotifications.refresh();
    }
});
