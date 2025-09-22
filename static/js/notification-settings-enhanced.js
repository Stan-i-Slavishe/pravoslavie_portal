// Обновленный JavaScript с поддержкой админского управления

document.addEventListener('DOMContentLoaded', function() {
    console.log('🔔 Initializing notification settings...');
    
    // Ждем загрузки админской системы
    setTimeout(() => {
        if (window.adminNotifications) {
            window.adminNotifications.loadActiveCategories();
        }
        
        // Инициализация
        setupEventHandlers();
        updateCardStates();
        updateQuietHoursVisibility();
        updateChildModeVisibility();
        
        // Загружаем текущие настройки
        loadUserSettings();
    }, 500);
});

function setupEventHandlers() {
    // Основные переключатели
    document.getElementById('notificationsEnabled').addEventListener('change', function() {
        toggleAllNotifications(this.checked);
        saveSettingsAutomatically();
    });
    
    document.getElementById('quietHoursEnabled').addEventListener('change', function() {
        updateQuietHoursVisibility();
        saveSettingsAutomatically();
    });
    
    document.getElementById('childMode').addEventListener('change', function() {
        updateChildModeVisibility();
        saveSettingsAutomatically();
    });
    
    // Переключатели категорий с проверкой админских настроек
    document.querySelectorAll('.category-toggle').forEach(toggle => {
        toggle.addEventListener('change', function() {
            const category = this.dataset.category;
            const enabled = this.checked;
            
            // Проверяем, активна ли категория в админке
            if (window.adminNotifications && !window.adminNotifications.isCategoryActive(category)) {
                console.warn(`Категория "${category}" отключена администратором`);
                this.checked = false;
                showAdminDisabledMessage(category);
                return;
            }
            
            updateCardState(category, enabled);
            saveSettingsAutomatically();
        });
    });
    
    // Автосохранение при изменении времени
    document.querySelectorAll('#quietStart, #quietEnd, #childBedtime').forEach(input => {
        input.addEventListener('change', saveSettingsAutomatically);
    });
    
    // Кнопки
    document.getElementById('saveSettings').addEventListener('click', () => saveSettings(true));
    document.getElementById('resetSettings').addEventListener('click', resetToDefaults);
}

function showAdminDisabledMessage(category) {
    const categoryNames = {
        'bedtime_stories': 'Сказки на ночь',
        'orthodox_calendar': 'Православный календарь',
        'new_content': 'Видео-рассказы',
        'fairy_tales': 'Терапевтические сказки',
        'book_releases': 'Новые книги',
        'audio_content': 'Аудио-контент'
    };
    
    const categoryName = categoryNames[category] || category;
    
    // Создаем временное уведомление
    const notification = document.createElement('div');
    notification.className = 'alert alert-warning position-fixed';
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 1060;
        min-width: 300px;
        animation: slideIn 0.3s ease;
    `;
    
    notification.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <strong>${categoryName}</strong><br>
        <small>Эта категория временно отключена администратором</small>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 4000);
}

function toggleAllNotifications(enabled) {
    document.querySelectorAll('.category-toggle').forEach(toggle => {
        const category = toggle.dataset.category;
        
        // Проверяем админские настройки
        if (window.adminNotifications && !window.adminNotifications.isCategoryActive(category)) {
            toggle.disabled = true;
            toggle.checked = false;
        } else {
            toggle.disabled = !enabled;
        }
    });
    
    document.querySelectorAll('.simple-card').forEach(card => {
        const category = card.dataset.category;
        
        if (window.adminNotifications && !window.adminNotifications.isCategoryActive(category)) {
            card.style.opacity = '0.3';
            card.classList.add('admin-disabled');
        } else {
            card.style.opacity = enabled ? '1' : '0.5';
            card.classList.remove('admin-disabled');
        }
    });
}

function updateCardState(category, enabled) {
    const card = document.querySelector(`[data-category="${category}"]`);
    if (!card) return;
    
    // Проверяем админские настройки
    if (window.adminNotifications && !window.adminNotifications.isCategoryActive(category)) {
        card.classList.add('admin-disabled');
        card.style.opacity = '0.3';
        enabled = false;
    } else {
        card.classList.remove('admin-disabled');
        card.style.opacity = '1';
    }
    
    if (enabled) {
        card.classList.add('enabled');
    } else {
        card.classList.remove('enabled');
    }
}

function updateCardStates() {
    document.querySelectorAll('.category-toggle').forEach(toggle => {
        const category = toggle.dataset.category;
        const enabled = toggle.checked;
        updateCardState(category, enabled);
    });
}

function updateQuietHoursVisibility() {
    const enabled = document.getElementById('quietHoursEnabled').checked;
    const settings = document.getElementById('quietHoursSettings');
    
    settings.style.opacity = enabled ? '1' : '0.5';
    settings.querySelectorAll('input').forEach(input => input.disabled = !enabled);
}

function updateChildModeVisibility() {
    const enabled = document.getElementById('childMode').checked;
    const settings = document.getElementById('childModeSettings');
    
    settings.style.display = enabled ? 'block' : 'none';
}

async function saveSettingsAutomatically() {
    clearTimeout(window.autoSaveTimeout);
    window.autoSaveTimeout = setTimeout(async () => {
        await saveSettings(false);
    }, 1000);
}

async function saveSettings(showNotification = true) {
    try {
        const settings = {
            notifications_enabled: document.getElementById('notificationsEnabled').checked,
            quiet_hours_enabled: document.getElementById('quietHoursEnabled').checked,
            quiet_start: document.getElementById('quietStart').value,
            quiet_end: document.getElementById('quietEnd').value,
            child_mode: document.getElementById('childMode').checked,
            child_bedtime: document.getElementById('childBedtime').value,
            categories: {}
        };
        
        // Собираем настройки только для активных категорий
        document.querySelectorAll('.category-toggle').forEach(toggle => {
            const category = toggle.dataset.category;
            
            // Проверяем админские настройки
            if (window.adminNotifications && !window.adminNotifications.isCategoryActive(category)) {
                return; // Пропускаем неактивные категории
            }
            
            settings.categories[category] = {
                enabled: toggle.checked
            };
        });
        
        const response = await fetch('/pwa/api/save-notification-settings/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(settings)
        });
        
        if (response.ok) {
            if (showNotification) {
                showSaveIndicator();
            }
            console.log('✅ Settings saved successfully');
        } else {
            throw new Error('Failed to save settings');
        }
    } catch (error) {
        console.error('❌ Error saving settings:', error);
        if (showNotification) {
            alert('Ошибка при сохранении настроек. Попробуйте еще раз.');
        }
    }
}

async function loadUserSettings() {
    try {
        const response = await fetch('/pwa/api/get-notification-settings/');
        if (response.ok) {
            const settings = await response.json();
            
            // Применяем настройки
            document.getElementById('notificationsEnabled').checked = settings.notifications_enabled;
            document.getElementById('quietHoursEnabled').checked = settings.quiet_hours_enabled;
            document.getElementById('quietStart').value = settings.quiet_start;
            document.getElementById('quietEnd').value = settings.quiet_end;
            document.getElementById('childMode').checked = settings.child_mode;
            document.getElementById('childBedtime').value = settings.child_bedtime;
            
            // Применяем настройки категорий с учетом админских настроек
            for (const [category, categorySettings] of Object.entries(settings.categories)) {
                const toggle = document.querySelector(`[data-category="${category}"]`);
                if (toggle) {
                    // Проверяем, активна ли категория в админке
                    if (window.adminNotifications && !window.adminNotifications.isCategoryActive(category)) {
                        toggle.checked = false;
                        toggle.disabled = true;
                    } else {
                        toggle.checked = categorySettings.enabled;
                        toggle.disabled = false;
                    }
                }
            }
            
            updateCardStates();
            updateQuietHoursVisibility();
            updateChildModeVisibility();
            
            console.log('✅ Settings loaded');
        }
    } catch (error) {
        console.error('❌ Error loading settings:', error);
    }
}

function resetToDefaults() {
    if (confirm('Сбросить все настройки к значениям по умолчанию?')) {
        document.getElementById('notificationsEnabled').checked = true;
        document.getElementById('quietHoursEnabled').checked = true;
        document.getElementById('quietStart').value = '22:00';
        document.getElementById('quietEnd').value = '08:00';
        document.getElementById('childMode').checked = false;
        document.getElementById('childBedtime').value = '20:00';
        
        // Включаем только активные категории
        document.querySelectorAll('.category-toggle').forEach(toggle => {
            const category = toggle.dataset.category;
            
            if (window.adminNotifications && !window.adminNotifications.isCategoryActive(category)) {
                toggle.checked = false;
                toggle.disabled = true;
            } else {
                toggle.checked = category !== 'audio_content'; // Аудио отключено по умолчанию
                toggle.disabled = false;
            }
        });
        
        updateCardStates();
        updateQuietHoursVisibility();
        updateChildModeVisibility();
        
        saveSettings(true);
    }
}

function showSaveIndicator() {
    const indicator = document.getElementById('saveIndicator');
    indicator.classList.add('show');
    
    setTimeout(() => {
        indicator.classList.remove('show');
    }, 3000);
}

function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='));
    return cookieValue ? cookieValue.split('=')[1] : '';
}

// Добавляем CSS для отключенных администратором категорий
const style = document.createElement('style');
style.textContent = `
    .admin-disabled {
        position: relative;
        pointer-events: none;
    }
    
    .admin-disabled::after {
        content: "Отключено администратором";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        white-space: nowrap;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .admin-disabled:hover::after {
        opacity: 1;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
