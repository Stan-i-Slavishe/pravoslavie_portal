/**
 * Система мобильной обратной связи с долгим нажатием
 * Позволяет пользователям быстро отправлять отзывы через долгое нажатие на мобильных устройствах
 */

class MobileFeedbackSystem {
    constructor() {
        // Настройки
        this.longPressDuration = 2000; // 2 секунды
        this.debounceTime = 300; // Предотвращение случайных срабатываний
        
        // Состояние
        this.longPressTimer = null;
        this.selectedOption = null;
        this.isModalOpen = false;
        this.lastTouchTime = 0;
        
        // DOM элементы
        this.overlay = null;
        this.indicator = null;
        this.form = null;
        this.textarea = null;
        this.submitBtn = null;
        
        // Инициализация только на мобильных устройствах
        if (this.isMobileDevice()) {
            this.init();
        }
    }

    /**
     * Проверка, является ли устройство мобильным
     */
    isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               ('ontouchstart' in window) ||
               window.innerWidth <= 768;
    }

    /**
     * Инициализация системы
     */
    init() {
        this.createHTML();
        this.initEventListeners();
        console.log('🔥 Система мобильной обратной связи активирована');
    }

    /**
     * Создание HTML элементов
     */
    createHTML() {
        // Индикатор долгого нажатия
        this.indicator = document.createElement('div');
        this.indicator.className = 'long-press-indicator';
        this.indicator.id = 'longPressIndicator';
        this.indicator.innerHTML = '<div class="long-press-circle"></div>';
        document.body.appendChild(this.indicator);

        // Оверлей с формой
        this.overlay = document.createElement('div');
        this.overlay.className = 'feedback-overlay';
        this.overlay.id = 'feedbackOverlay';
        this.overlay.innerHTML = `
            <div class="feedback-modal">
                <button class="feedback-close" id="feedbackClose">
                    <i class="bi bi-x"></i>
                </button>
                
                <div class="feedback-header">
                    <div class="feedback-icon">
                        <i class="bi bi-chat-heart"></i>
                    </div>
                    <h4>Улучшить приложение</h4>
                    <p>Помогите нам стать лучше! Выберите тип обращения:</p>
                </div>

                <form id="feedbackForm">
                    <div class="feedback-options">
                        <div class="feedback-option" data-value="bug">
                            <div class="feedback-option-icon">
                                <i class="bi bi-bug"></i>
                            </div>
                            <div class="feedback-option-text">
                                <div class="feedback-option-title">Нашёл ошибку</div>
                                <div class="feedback-option-desc">Сообщить о технической проблеме</div>
                            </div>
                        </div>

                        <div class="feedback-option" data-value="feature">
                            <div class="feedback-option-icon">
                                <i class="bi bi-lightbulb"></i>
                            </div>
                            <div class="feedback-option-text">
                                <div class="feedback-option-title">Предложить улучшение</div>
                                <div class="feedback-option-desc">Идея новой функции или улучшения</div>
                            </div>
                        </div>

                        <div class="feedback-option" data-value="design">
                            <div class="feedback-option-icon">
                                <i class="bi bi-palette"></i>
                            </div>
                            <div class="feedback-option-text">
                                <div class="feedback-option-title">Дизайн и интерфейс</div>
                                <div class="feedback-option-desc">Предложения по улучшению внешнего вида</div>
                            </div>
                        </div>

                        <div class="feedback-option" data-value="content">
                            <div class="feedback-option-icon">
                                <i class="bi bi-book"></i>
                            </div>
                            <div class="feedback-option-text">
                                <div class="feedback-option-title">Контент и материалы</div>
                                <div class="feedback-option-desc">Предложения по содержанию сайта</div>
                            </div>
                        </div>

                        <div class="feedback-option" data-value="performance">
                            <div class="feedback-option-icon">
                                <i class="bi bi-speedometer2"></i>
                            </div>
                            <div class="feedback-option-text">
                                <div class="feedback-option-title">Скорость работы</div>
                                <div class="feedback-option-desc">Проблемы с производительностью</div>
                            </div>
                        </div>

                        <div class="feedback-option" data-value="other">
                            <div class="feedback-option-icon">
                                <i class="bi bi-chat-dots"></i>
                            </div>
                            <div class="feedback-option-text">
                                <div class="feedback-option-title">Другое</div>
                                <div class="feedback-option-desc">Общие вопросы и предложения</div>
                            </div>
                        </div>
                    </div>

                    <textarea 
                        class="feedback-textarea" 
                        id="feedbackText" 
                        placeholder="Опишите подробнее вашу проблему или предложение..."
                        maxlength="1000">
                    </textarea>

                    <div class="feedback-buttons">
                        <button type="button" class="btn-feedback-cancel" id="feedbackCancel">
                            <i class="bi bi-x-circle"></i>Отмена
                        </button>
                        <button type="submit" class="btn-feedback-submit" id="feedbackSubmit" disabled>
                            <i class="bi bi-send"></i>Отправить отзыв
                        </button>
                    </div>
                </form>
            </div>
        `;
        document.body.appendChild(this.overlay);

        // Получаем ссылки на элементы
        this.form = document.getElementById('feedbackForm');
        this.textarea = document.getElementById('feedbackText');
        this.submitBtn = document.getElementById('feedbackSubmit');
    }

    /**
     * Инициализация обработчиков событий
     */
    initEventListeners() {
        // Долгое нажатие
        document.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: false });
        document.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: false });
        document.addEventListener('touchmove', this.handleTouchEnd.bind(this), { passive: false });

        // Клики по опциям
        document.querySelectorAll('.feedback-option').forEach(option => {
            option.addEventListener('click', this.selectOption.bind(this));
        });

        // Закрытие модального окна
        document.getElementById('feedbackClose').addEventListener('click', this.closeFeedback.bind(this));
        document.getElementById('feedbackCancel').addEventListener('click', this.closeFeedback.bind(this));
        this.overlay.addEventListener('click', (e) => {
            if (e.target === this.overlay) {
                this.closeFeedback();
            }
        });

        // Валидация формы
        this.textarea.addEventListener('input', this.validateForm.bind(this));

        // Отправка формы
        this.form.addEventListener('submit', this.submitFeedback.bind(this));

        // Escape для закрытия
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isModalOpen) {
                this.closeFeedback();
            }
        });
    }

    /**
     * Обработка начала касания
     */
    handleTouchStart(e) {
        // Игнорируем, если модальное окно уже открыто
        if (this.isModalOpen) return;

        // Предотвращение случайных срабатываний
        const currentTime = Date.now();
        if (currentTime - this.lastTouchTime < this.debounceTime) {
            return;
        }
        this.lastTouchTime = currentTime;

        // Игнорируем клики по интерактивным элементам
        const target = e.target;
        if (target.closest('button, a, input, textarea, select, .feedback-overlay, .btn, [role="button"]')) {
            return;
        }

        // Игнорируем скроллинг и жесты
        if (e.touches.length > 1) {
            return;
        }

        this.startLongPress(e.touches[0]);
    }

    /**
     * Обработка завершения касания
     */
    handleTouchEnd(e) {
        this.cancelLongPress();
    }

    /**
     * Начало долгого нажатия
     */
    startLongPress(touch) {
        this.showIndicator(touch.clientX, touch.clientY);
        
        this.longPressTimer = setTimeout(() => {
            this.hideIndicator();
            this.showFeedback();
            
            // Вибрация (если поддерживается)
            if (navigator.vibrate) {
                navigator.vibrate([50, 30, 50]);
            }
        }, this.longPressDuration);
    }

    /**
     * Отмена долгого нажатия
     */
    cancelLongPress() {
        if (this.longPressTimer) {
            clearTimeout(this.longPressTimer);
            this.longPressTimer = null;
        }
        this.hideIndicator();
    }

    /**
     * Показать индикатор
     */
    showIndicator(x, y) {
        this.indicator.style.left = x + 'px';
        this.indicator.style.top = y + 'px';
        this.indicator.style.transform = 'translate(-50%, -50%)';
        this.indicator.style.display = 'flex';
    }

    /**
     * Скрыть индикатор
     */
    hideIndicator() {
        this.indicator.style.display = 'none';
    }

    /**
     * Показать форму обратной связи
     */
    showFeedback() {
        this.isModalOpen = true;
        this.overlay.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Фокус на форме для лучшей доступности
        setTimeout(() => {
            if (this.textarea) {
                this.textarea.focus();
            }
        }, 300);
    }

    /**
     * Закрыть форму обратной связи
     */
    closeFeedback() {
        this.isModalOpen = false;
        this.overlay.classList.remove('show');
        document.body.style.overflow = '';
        
        // Сброс формы с задержкой для плавной анимации
        setTimeout(() => {
            this.resetForm();
        }, 300);
    }

    /**
     * Сброс формы
     */
    resetForm() {
        // Сброс выбранной опции
        document.querySelectorAll('.feedback-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        // Сброс формы
        this.form.reset();
        this.selectedOption = null;
        this.validateForm();
    }

    /**
     * Выбор опции
     */
    selectOption(e) {
        const option = e.currentTarget;
        
        // Убираем выделение с других опций
        document.querySelectorAll('.feedback-option').forEach(opt => {
            opt.classList.remove('selected');
        });
        
        // Выделяем выбранную опцию
        option.classList.add('selected');
        this.selectedOption = option.dataset.value;
        
        this.validateForm();
    }

    /**
     * Валидация формы
     */
    validateForm() {
        const hasOption = this.selectedOption !== null;
        const hasText = this.textarea.value.trim().length > 0;
        
        this.submitBtn.disabled = !(hasOption && hasText);
    }

    /**
     * Отправка формы
     */
    async submitFeedback(e) {
        e.preventDefault();
        
        if (!this.selectedOption || !this.textarea.value.trim()) {
            return;
        }

        const feedbackData = {
            type: this.selectedOption,
            message: this.textarea.value.trim(),
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            url: window.location.href,
            screenResolution: `${screen.width}x${screen.height}`
        };

        try {
            this.submitBtn.disabled = true;
            this.submitBtn.innerHTML = '<i class="bi bi-hourglass-split"></i>Отправляем...';

            await this.sendToServer(feedbackData);
            
            this.showSuccessMessage();
            setTimeout(() => {
                this.closeFeedback();
            }, 2500);

        } catch (error) {
            console.error('Ошибка отправки обратной связи:', error);
            this.showToast('Произошла ошибка при отправке. Попробуйте ещё раз.', 'error');
            
        } finally {
            this.submitBtn.disabled = false;
            this.submitBtn.innerHTML = '<i class="bi bi-send"></i>Отправить отзыв';
        }
    }

    /**
     * Отправка данных на сервер
     */
    async sendToServer(data) {
        const response = await fetch('/api/mobile-feedback/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Ошибка сервера');
        }

        return response.json();
    }

    /**
     * Получение CSRF токена
     */
    getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue;
    }

    /**
     * Показать сообщение об успехе
     */
    showSuccessMessage() {
        const modal = document.querySelector('.feedback-modal');
        modal.innerHTML = `
            <div class="feedback-success-content">
                <div class="feedback-success-icon">
                    <i class="bi bi-check-lg"></i>
                </div>
                <h4>Спасибо!</h4>
                <p>Ваш отзыв отправлен. Мы обязательно его рассмотрим!</p>
            </div>
        `;
    }

    /**
     * Показать уведомление
     */
    showToast(message, type = 'success') {
        // Удаляем предыдущие уведомления
        const existingToast = document.querySelector('.feedback-toast');
        if (existingToast) {
            existingToast.remove();
        }

        const toast = document.createElement('div');
        toast.className = `feedback-toast ${type}`;
        toast.innerHTML = `
            <i class="bi bi-${type === 'error' ? 'exclamation-triangle' : 'check-circle'}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(toast);
        
        // Показываем с анимацией
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);
        
        // Автоматически скрываем через 4 секунды
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 4000);
    }

    /**
     * Статический метод для инициализации
     */
    static init() {
        return new MobileFeedbackSystem();
    }
}

// Автоматическая инициализация при загрузке DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        MobileFeedbackSystem.init();
    });
} else {
    // DOM уже загружен
    MobileFeedbackSystem.init();
}

// Экспорт для возможного использования в других скриптах
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MobileFeedbackSystem;
}
if (typeof window !== 'undefined') {
    window.MobileFeedbackSystem = MobileFeedbackSystem;
}