// Улучшенная функция для избранного - мгновенное обновление UI
function toggleFavorite(bookId, event) {
    // Получаем CSRF токен
    const csrfToken = getCSRFToken();
    
    if (!csrfToken) {
        console.error('CSRF token not found');
        showToast('Ошибка безопасности. Перезагрузите страницу.', 'error');
        return;
    }
    
    // Находим кнопку
    let button;
    if (event && event.target) {
        button = event.target.closest('.btn-favorite');
    } else {
        button = document.querySelector('.btn-favorite');
    }
    
    if (!button) {
        console.error('Button not found');
        showToast('Ошибка: кнопка не найдена', 'error');
        return;
    }
    
    // Получаем текущее состояние
    const wasActive = button.classList.contains('active');
    
    // Оптимистично обновляем UI сразу
    updateFavoriteButtonOptimistic(button, !wasActive);
    
    // Блокируем кнопку на время запроса
    button.disabled = true;
    
    // Отправляем AJAX запрос
    fetch(`/books/favorite/${bookId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('✅ Favorite response:', data);
        
        if (data.status === 'success') {
            // Подтверждаем изменения от сервера
            updateFavoriteButton(button, data.is_favorite);
            
            // Показываем уведомление
            showToast(data.message, 'success');
            
            // Обновляем счетчик избранного в навигации
            if (window.updateFavoritesCount) {
                window.updateFavoritesCount();
            }
            
            // Генерируем событие для других компонентов
            document.dispatchEvent(new CustomEvent('favoriteToggled', {
                detail: {
                    bookId: bookId,
                    isFavorite: data.is_favorite
                }
            }));
            
        } else {
            // Откатываем изменения при ошибке
            updateFavoriteButton(button, wasActive);
            showToast(data.message || 'Произошла ошибка', 'error');
        }
    })
    .catch(error => {
        console.error('❌ Favorite error:', error);
        // Откатываем изменения при ошибке
        updateFavoriteButton(button, wasActive);
        showToast(`Ошибка: ${error.message}`, 'error');
    })
    .finally(() => {
        // Разблокируем кнопку
        button.disabled = false;
    });
}

// Оптимистичное обновление UI (до ответа сервера)
function updateFavoriteButtonOptimistic(button, isFavorite) {
    const icon = button.querySelector('i');
    const text = button.querySelector('.favorite-text');
    
    if (isFavorite) {
        button.classList.add('active');
        if (icon) icon.className = 'bi bi-bookmark-fill';
        if (text) text.textContent = 'В избранном';
        
        button.style.background = 'linear-gradient(135deg, #ffc107, #e0a800)';
        button.style.color = 'white';
        button.style.borderColor = '#ffc107';
    } else {
        button.classList.remove('active');
        if (icon) icon.className = 'bi bi-bookmark';
        if (text) text.textContent = 'В избранное';
        
        button.style.background = 'transparent';
        button.style.color = '#ffc107';
        button.style.borderColor = '#ffc107';
    }
}

// Окончательное обновление UI (после ответа сервера)
function updateFavoriteButton(button, isFavorite) {
    updateFavoriteButtonOptimistic(button, isFavorite);
    
    // Обновляем обработчики наведения для корректного состояния
    if (isFavorite) {
        button.setAttribute('onmouseout', 
            "this.style.background='linear-gradient(135deg, #ffc107, #e0a800)'; " +
            "this.style.color='white'; " +
            "this.style.transform='translateY(0)'; " +
            "this.style.boxShadow='none'"
        );
    } else {
        button.setAttribute('onmouseout', 
            "this.style.background='transparent'; " +
            "this.style.color='#ffc107'; " +
            "this.style.transform='translateY(0)'; " +
            "this.style.boxShadow='none'"
        );
    }
    
    console.log(`✅ Button updated: ${isFavorite ? 'added to' : 'removed from'} favorites`);
}

console.log('✅ Improved favorites functionality loaded');
