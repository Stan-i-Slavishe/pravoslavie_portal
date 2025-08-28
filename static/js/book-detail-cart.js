// Обработка добавления в корзину - использует глобальные функции
document.addEventListener('DOMContentLoaded', function() {
    const addToCartBtn = document.querySelector('.btn-add-to-cart');
    
    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const bookId = this.dataset.bookId;
            const bookPrice = this.dataset.bookPrice;
            const button = this;
            const originalText = button.innerHTML;
            
            // Блокируем кнопку
            button.disabled = true;
            button.innerHTML = '<i class="bi bi-hourglass me-1"></i>Добавляем...';
            
            // CSRF токен через глобальную функцию
            const csrfToken = getCSRFToken();
            
            if (!csrfToken) {
                console.error('CSRF token not found');
                button.innerHTML = '<i class="bi bi-exclamation-triangle me-1"></i>Ошибка';
                button.style.background = 'linear-gradient(135deg, #dc3545, #c82333)';
                showToast('Ошибка безопасности. Перезагрузите страницу.', 'error');
                
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.background = 'linear-gradient(135deg, #28a745, #20692b)';
                    button.disabled = false;
                }, 3000);
                return;
            }
            
            // Отправляем запрос на добавление в корзину
            fetch('/shop/add-book-to-cart/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'book_id': bookId,
                    'quantity': 1
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Успешно добавлено
                    button.innerHTML = '<i class="bi bi-check me-1"></i>Добавлено!';
                    button.style.background = 'linear-gradient(135deg, #28a745, #20692b)';
                    
                    // Показываем уведомление
                    showToast('Книга добавлена в корзину!', 'success');
                    
                    // Обновляем счетчик корзины
                    if (window.updateCartCount) {
                        window.updateCartCount();
                    }
                    
                    // Генерируем событие
                    document.dispatchEvent(new CustomEvent('cartUpdated', {
                        detail: {
                            count: data.cart_total_items,
                            total_price: data.cart_total_price
                        }
                    }));
                    
                    // Предлагаем перейти в корзину через 2 секунды
                    setTimeout(() => {
                        button.innerHTML = '<i class="bi bi-cart me-1"></i>Перейти в корзину';
                        button.disabled = false;
                        
                        button.onclick = function() {
                            window.location.href = '/shop/cart/';
                        };
                    }, 2000);
                    
                } else {
                    // Ошибка
                    button.innerHTML = '<i class="bi bi-exclamation-triangle me-1"></i>Ошибка';
                    button.style.background = 'linear-gradient(135deg, #dc3545, #c82333)';
                    
                    showToast(data.message || 'Ошибка добавления в корзину', 'error');
                    
                    setTimeout(() => {
                        button.innerHTML = originalText;
                        button.style.background = 'linear-gradient(135deg, #28a745, #20692b)';
                        button.disabled = false;
                    }, 3000);
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                button.innerHTML = '<i class="bi bi-exclamation-triangle me-1"></i>Ошибка сети';
                button.style.background = 'linear-gradient(135deg, #dc3545, #c82333)';
                
                showToast('Ошибка сети. Попробуйте еще раз.', 'error');
                
                setTimeout(() => {
                    button.innerHTML = originalText;
                    button.style.background = 'linear-gradient(135deg, #28a745, #20692b)';
                    button.disabled = false;
                }, 3000);
            });
        });
    }
});

console.log('✅ Book detail cart functionality loaded');
