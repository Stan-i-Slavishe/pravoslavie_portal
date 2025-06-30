// Улучшенный JavaScript для портала "Добрые истории"

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Инициализация всех функций
    initSmoothScrolling();
    initCardAnimations();
    initNavbarEffects();
    initTagCloudEffects();
    initButtonEffects();
    initSearchEnhancements();
    initProgressiveLoading();
    initAccessibilityFeatures();
    
    // Автоматическое скрытие алертов
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert.classList.contains('alert-dismissible')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);

    console.log('Портал "Добрые истории" загружен успешно!');
});

// Плавная прокрутка для якорных ссылок
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Анимации для карточек
function initCardAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const cardObserver = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Задержка для последовательного появления
                setTimeout(() => {
                    entry.target.classList.add('animate-in');
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 150);
                
                cardObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Подготавливаем карточки к анимации
    document.querySelectorAll('.card, .hero-section, .cta-section').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        cardObserver.observe(element);
    });
}

// Эффекты для навигации
function initNavbarEffects() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    let lastScrollTop = 0;

    // Скрытие/показ навбара при скролле
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Скролл вниз
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Скролл вверх
            navbar.style.transform = 'translateY(0)';
        }
        
        // Добавляем тень при скролле
        if (scrollTop > 10) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        lastScrollTop = scrollTop;
    });

    // Добавляем CSS для плавных переходов
    navbar.style.transition = 'transform 0.3s ease-in-out, box-shadow 0.3s ease';
    
    // Активная ссылка в навигации
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Эффекты для облака тегов
function initTagCloudEffects() {
    const tags = document.querySelectorAll('.tag-cloud .badge');
    
    tags.forEach((tag, index) => {
        // Анимация появления с задержкой
        tag.style.opacity = '0';
        tag.style.transform = 'scale(0.8)';
        tag.style.transition = 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
        
        setTimeout(() => {
            tag.style.opacity = '1';
            tag.style.transform = 'scale(1)';
        }, index * 50);

        // Hover эффекты
        tag.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05) translateY(-2px)';
            this.style.zIndex = '10';
        });

        tag.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) translateY(0)';
            this.style.zIndex = '1';
        });
    });
}

// Улучшенные эффекты кнопок
function initButtonEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        // Ripple эффект
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });

        // Улучшенный hover эффект
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });

        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // CSS для ripple эффекта
    const style = document.createElement('style');
    style.textContent = `
        .btn {
            position: relative;
            overflow: hidden;
        }
        
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.4);
            transform: scale(0);
            animation: ripple-animation 0.6s linear;
            pointer-events: none;
        }
        
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        .navbar.scrolled {
            box-shadow: 0 2px 20px rgba(0,0,0,0.1);
            background-color: rgba(255,255,255,0.95) !important;
            backdrop-filter: blur(10px);
        }
    `;
    document.head.appendChild(style);
}

// Улучшения поиска (если есть форма поиска)
function initSearchEnhancements() {
    const searchInputs = document.querySelectorAll('input[type="search"], .search-input');
    
    searchInputs.forEach(input => {
        // Автофокус с задержкой
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });

        // Мгновенный поиск с debounce
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                // Здесь можно добавить AJAX поиск
                console.log('Поиск:', this.value);
            }, 300);
        });
    });
}

// Прогрессивная загрузка изображений
function initProgressiveLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('fade-in');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Функции доступности
function initAccessibilityFeatures() {
    // Навигация с клавиатуры
    document.addEventListener('keydown', function(e) {
        // ESC для закрытия модальных окон
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                bootstrap.Modal.getInstance(modal)?.hide();
            });
        }
        
        // Tab navigation для карточек
        if (e.key === 'Tab') {
            const focusedElement = document.activeElement;
            if (focusedElement.classList.contains('card')) {
                focusedElement.style.outline = '3px solid var(--accent-color)';
                focusedElement.style.outlineOffset = '4px';
            }
        }
    });

    // Убираем outline при клике мышью
    document.addEventListener('mousedown', function() {
        document.querySelectorAll('.card').forEach(card => {
            card.style.outline = 'none';
        });
    });

    // Уведомления для screen readers
    const announcer = document.createElement('div');
    announcer.setAttribute('aria-live', 'polite');
    announcer.setAttribute('aria-atomic', 'true');
    announcer.style.position = 'absolute';
    announcer.style.left = '-10000px';
    announcer.style.width = '1px';
    announcer.style.height = '1px';
    announcer.style.overflow = 'hidden';
    document.body.appendChild(announcer);

    window.announceToScreenReader = function(message) {
        announcer.textContent = message;
        setTimeout(() => {
            announcer.textContent = '';
        }, 1000);
    };
}

// Функция для анимации счетчиков
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent.replace(/\D/g, ''));
        let current = 0;
        const increment = target / 50; // 50 шагов анимации
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            // Форматируем число с + в конце если было
            const formatted = Math.floor(current).toLocaleString('ru-RU');
            counter.textContent = counter.textContent.includes('+') ? 
                formatted + '+' : formatted;
        }, 20);
    });
}

// Запуск анимации счетчиков при появлении в зоне видимости
function initCounterAnimation() {
    const statsSection = document.querySelector('.stats-row');
    if (!statsSection) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    observer.observe(statsSection);
}

// Функция для создания параллакс эффекта
function initParallaxEffect() {
    const parallaxElements = document.querySelectorAll('.hero-section, .cta-section');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const rate = scrolled * -0.5;
            element.style.transform = `translateY(${rate}px)`;
        });
    });
}

// Функция для lazy loading контента
function initLazyLoading() {
    const lazyElements = document.querySelectorAll('[data-lazy]');
    
    const lazyObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                
                // Загружаем контент
                if (element.dataset.lazy === 'content') {
                    loadLazyContent(element);
                }
                
                lazyObserver.unobserve(element);
            }
        });
    });

    lazyElements.forEach(element => lazyObserver.observe(element));
}

// Функция для загрузки контента по требованию
function loadLazyContent(element) {
    // Здесь можно добавить AJAX загрузку дополнительного контента
    element.classList.add('loaded');
}

// Вспомогательные функции
const utils = {
    // Throttle функция для оптимизации событий scroll
    throttle: function(func, delay) {
        let timeoutId;
        let lastExecTime = 0;
        return function (...args) {
            const currentTime = Date.now();
            
            if (currentTime - lastExecTime > delay) {
                func.apply(this, args);
                lastExecTime = currentTime;
            } else {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    func.apply(this, args);
                    lastExecTime = Date.now();
                }, delay - (currentTime - lastExecTime));
            }
        };
    },

    // Debounce функция для оптимизации поиска
    debounce: function(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    },

    // Проверка поддержки различных функций
    supportsIntersectionObserver: function() {
        return 'IntersectionObserver' in window;
    },

    // Определение мобильного устройства
    isMobile: function() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
};

// Инициализация дополнительных функций
document.addEventListener('DOMContentLoaded', function() {
    initCounterAnimation();
    
    // Отключаем параллакс на мобильных для производительности
    if (!utils.isMobile()) {
        initParallaxEffect();
    }
    
    initLazyLoading();
});

// Функция для AJAX запросов с CSRF токеном
function getCookie(name) {
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

const csrftoken = getCookie('csrftoken');

// Экспорт функций для использования в других скриптах
window.PortalJS = {
    utils,
    animateCounters,
    announceToScreenReader: window.announceToScreenReader
};

// Функция для закрытия фиксированного CTA блока
function closeCTA() {
    const ctaSection = document.getElementById('ctaSection');
    if (ctaSection) {
        ctaSection.classList.add('hidden');
        
        // Сохраняем состояние в localStorage
        localStorage.setItem('ctaClosed', 'true');
        
        // Уведомление для screen readers
        if (window.announceToScreenReader) {
            window.announceToScreenReader('Блок приглашения закрыт');
        }
    }
}

// Проверяем, был ли CTA блок закрыт ранее
document.addEventListener('DOMContentLoaded', function() {
    const ctaSection = document.getElementById('ctaSection');
    if (ctaSection && localStorage.getItem('ctaClosed') === 'true') {
        ctaSection.classList.add('hidden');
    }
});