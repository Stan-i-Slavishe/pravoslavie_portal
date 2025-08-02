// JavaScript для обработки кнопок-закладок

document.addEventListener('DOMContentLoaded', function() {
    
    // Получаем CSRF токен
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') ||
               document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
    }
    
    // Функция для показа уведомлений
    function showNotification(message, type = 'success') {
        // Создаем простое уведомление
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'success' ? 'success' : 'danger'} notification-toast`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            border-radius: 6px;
        `;
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="bi bi-${type === 'success' ? 'check-circle' : 'exclamation-triangle'} me-2"></i>
                <span>${message}</span>
                <button type="button" class="btn-close ms-auto" aria-label="Close"></button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Анимация появления
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Автоматическое скрытие
        setTimeout(() => {
            hideNotification(notification);
        }, 4000);
        
        // Обработчик кнопки закрытия
        notification.querySelector('.btn-close').addEventListener('click', () => {
            hideNotification(notification);
        });
    }
    
    function hideNotification(notification) {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }
    
    // Функция обновления счетчика избранного
    function updateFavoritesCounter(count) {
        const counters = document.querySelectorAll('[data-favorites-count]');
        counters.forEach(counter => {
            counter.textContent = count;
            counter.style.display = count > 0 ? 'flex' : 'none';
        });
    }
    
    // Функция анимации кнопки
    function animateButton(button, animation) {
        button.classList.add(animation);
        setTimeout(() => {
            button.classList.remove(animation);
        }, 600);
    }
    
    // Основная функция обработки избранного
    function handleFavoriteToggle(button, bookId) {
        // Проверяем авторизацию через Django template переменную
        const userAuthElement = document.querySelector('#user-auth-status');
        const isAuthenticated = userAuthElement ? userAuthElement.dataset.authenticated === 'true' : false;
        
        if (!isAuthenticated) {
            showNotification('Для добавления в избранное необходимо войти в систему', 'error');
            setTimeout(() => {
                window.location.href = '/accounts/login/';
            }, 1500);
            return;
        }
        
        const icon = button.querySelector('i');
        const wasActive = button.classList.contains('active') || button.classList.contains('favorited');
        
        // Блокируем кнопку на время запроса
        button.disabled = true;
        button.style.opacity = '0.7';
        
        // Показываем анимацию загрузки
        const originalIcon = icon.className;
        icon.className = 'bi bi-arrow-repeat';
        icon.style.animation = 'spin 1s linear infinite';
        
        // AJAX запрос
        fetch(`/books/favorite/${bookId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                // Останавливаем анимацию загрузки
                icon.style.animation = '';
                
                if (data.is_favorite) {
                    // Книга добавлена в избранное
                    button.classList.add('active', 'favorited');
                    icon.className = 'bi bi-bookmark-fill';
                    button.title = 'Удалить из избранного';
                    
                    // Анимация добавления
                    animateButton(button, 'adding');
                    showNotification(data.message || 'Книга добавлена в избранное', 'success');
                    
                } else {
                    // Книга удалена из избранного
                    button.classList.remove('active', 'favorited');
                    icon.className = 'bi bi-bookmark';
                    button.title = 'Добавить в избранное';
                    
                    // Анимация удаления
                    animateButton(button, 'removing');
                    showNotification(data.message || 'Книга удалена из избранного', 'success');
                }
                
                // Обновляем счетчик
                if (data.favorites_count !== undefined) {
                    updateFavoritesCounter(data.favorites_count);
                }
                
            } else {
                // Восстанавливаем иконку
                icon.className = originalIcon;
                icon.style.animation = '';
                
                console.error('❌ Ошибка:', data.message);
                showNotification(data.message || 'Произошла ошибка', 'error');
            }
        })
        .catch(error => {
            // Восстанавливаем иконку
            icon.className = originalIcon;
            icon.style.animation = '';
            
            console.error('❌ Ошибка сети:', error);
            showNotification('Ошибка сети. Попробуйте еще раз.', 'error');
        })
        .finally(() => {
            // Разблокируем кнопку
            button.disabled = false;
            button.style.opacity = '1';
        });
    }
    
    // Инициализация кнопок избранного
    function initFavoriteButtons() {
        const favoriteButtons = document.querySelectorAll('[data-action="favorite"]');
        
        favoriteButtons.forEach(button => {
            // Проверяем, не был ли уже инициализирован
            if (button.hasAttribute('data-initialized')) {
                return;
            }
            
            button.setAttribute('data-initialized', 'true');
            
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const bookId = this.dataset.bookId;
                if (!bookId) {
                    console.error('❌ Не указан ID книги');
                    showNotification('Ошибка: не указан ID книги', 'error');
                    return;
                }
                
                handleFavoriteToggle(this, bookId);
            });
            
            // Добавляем класс для стилизации
            if (!button.classList.contains('btn-bookmark')) {
                button.classList.add('btn-bookmark');
            }
        });
        
        console.log(`✅ Инициализировано ${favoriteButtons.length} кнопок избранного`);
    }
    
    // Функция для динамически добавляемого контента
    function reinitializeFavoriteButtons() {
        initFavoriteButtons();
    }
    
    // Первичная инициализация
    initFavoriteButtons();
    
    // Наблюдатель за изменениями DOM для динамического контента
    const observer = new MutationObserver(function(mutations) {
        let shouldReinitialize = false;
        
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                const addedNodes = Array.from(mutation.addedNodes);
                const hasFavoriteButtons = addedNodes.some(node => {
                    return node.nodeType === 1 && (
                        (node.hasAttribute && node.hasAttribute('data-action') && node.getAttribute('data-action') === 'favorite') ||
                        (node.querySelector && node.querySelector('[data-action="favorite"]'))
                    );
                });
                
                if (hasFavoriteButtons) {
                    shouldReinitialize = true;
                }
            }
        });
        
        if (shouldReinitialize) {
            setTimeout(reinitializeFavoriteButtons, 100);
        }
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Экспортируем функции для внешнего использования
    window.BookmarkButtons = {
        init: initFavoriteButtons,
        reinit: reinitializeFavoriteButtons,
        showNotification: showNotification,
        updateCounter: updateFavoritesCounter
    };
    
    // Добавляем CSS анимации через JavaScript
    const style = document.createElement('style');
    style.textContent = `
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        .notification-toast {
            animation: slideInRight 0.3s ease-out;
        }
        
        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(100%);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
    `;
    document.head.appendChild(style);
    
    console.log('✅ Система кнопок-закладок инициализирована');
});
