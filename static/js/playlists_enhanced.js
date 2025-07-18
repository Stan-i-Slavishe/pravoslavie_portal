// Улучшенный JavaScript для плейлистов

document.addEventListener('DOMContentLoaded', function() {
    initializePlaylistsPage();
});

function initializePlaylistsPage() {
    // Инициализация всех компонентов
    setupCardAnimations();
    setupPreviewLoading();
    setupLazyLoading();
    setupKeyboardNavigation();
    setupTouchGestures();
    setupProgressiveEnhancement();
}

// Анимации появления карточек
function setupCardAnimations() {
    const cards = document.querySelectorAll('.playlist-card');
    
    // Intersection Observer для анимации при скролле
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '50px'
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
}

// Ленивая загрузка превью изображений
function setupLazyLoading() {
    const previewItems = document.querySelectorAll('.preview-item');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const item = entry.target;
                const bgImage = item.style.backgroundImage;
                
                if (bgImage && !item.dataset.loaded) {
                    loadBackgroundImage(item, bgImage);
                    imageObserver.unobserve(item);
                }
            }
        });
    });
    
    previewItems.forEach(item => imageObserver.observe(item));
}

// Загрузка фонового изображения с fallback
function loadBackgroundImage(element, imageUrl) {
    element.classList.add('loading');
    
    const img = new Image();
    const url = imageUrl.slice(5, -2); // Убираем url("...")
    
    img.onload = function() {
        element.style.backgroundImage = imageUrl;
        element.classList.remove('loading');
        element.dataset.loaded = 'true';
        
        // Добавляем эффект появления
        element.style.opacity = '0';
        element.style.transition = 'opacity 0.3s ease';
        setTimeout(() => {
            element.style.opacity = '1';
        }, 50);
    };
    
    img.onerror = function() {
        // Fallback для ошибок загрузки
        const videoId = extractVideoIdFromUrl(url);
        if (videoId) {
            // Пробуем другие форматы превью YouTube
            const fallbackUrls = [
                `https://img.youtube.com/vi/${videoId}/hqdefault.jpg`,
                `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`,
                `https://img.youtube.com/vi/${videoId}/default.jpg`
            ];
            
            tryFallbackImages(element, fallbackUrls, 0);
        } else {
            showErrorPlaceholder(element);
        }
    };
    
    img.src = url;
}

// Попытка загрузки fallback изображений
function tryFallbackImages(element, urls, index) {
    if (index >= urls.length) {
        showErrorPlaceholder(element);
        return;
    }
    
    const img = new Image();
    img.onload = function() {
        element.style.backgroundImage = `url('${urls[index]}')`;
        element.classList.remove('loading');
        element.dataset.loaded = 'true';
    };
    
    img.onerror = function() {
        tryFallbackImages(element, urls, index + 1);
    };
    
    img.src = urls[index];
}

// Показать заглушку при ошибке
function showErrorPlaceholder(element) {
    element.classList.remove('loading');
    element.style.background = 'linear-gradient(45deg, #f8f9fa, #e9ecef)';
    element.innerHTML = `
        <div style="
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: #6c757d;
            font-size: 0.8rem;
        ">
            <i class="fas fa-image" style="font-size: 1.5rem; margin-bottom: 5px;"></i>
            <div>Превью недоступно</div>
        </div>
    `;
}

// Извлечение YouTube ID из URL
function extractVideoIdFromUrl(url) {
    const patterns = [
        /(?:https?:\/\/)?(?:www\.)?youtube\.com\/vi\/([^\/&\n?#]+)/,
        /(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&\n?#]+)/,
        /(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^&\n?#]+)/,
        /(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^&\n?#]+)/
    ];
    
    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match) return match[1];
    }
    return null;
}

// Настройка предзагрузки превью
function setupPreviewLoading() {
    // Предзагружаем превью при наведении на карточку
    const cards = document.querySelectorAll('.playlist-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const previewItems = card.querySelectorAll('.preview-item:not([data-loaded])');
            previewItems.forEach(item => {
                const bgImage = item.style.backgroundImage;
                if (bgImage) {
                    loadBackgroundImage(item, bgImage);
                }
            });
        });
    });
}

// Навигация с клавиатуры
function setupKeyboardNavigation() {
    const cards = document.querySelectorAll('.playlist-card');
    let currentIndex = -1;
    
    document.addEventListener('keydown', function(e) {
        // Только если фокус не на форме
        if (document.activeElement.tagName === 'INPUT' || 
            document.activeElement.tagName === 'TEXTAREA') {
            return;
        }
        
        switch(e.key) {
            case 'ArrowRight':
            case 'ArrowDown':
                e.preventDefault();
                currentIndex = Math.min(currentIndex + 1, cards.length - 1);
                focusCard(cards[currentIndex]);
                break;
                
            case 'ArrowLeft':
            case 'ArrowUp':
                e.preventDefault();
                currentIndex = Math.max(currentIndex - 1, 0);
                focusCard(cards[currentIndex]);
                break;
                
            case 'Enter':
                if (currentIndex >= 0 && cards[currentIndex]) {
                    const playBtn = cards[currentIndex].querySelector('.playlist-play-btn');
                    if (playBtn) playBtn.click();
                }
                break;
        }
    });
}

// Фокус на карточке
function focusCard(card) {
    if (!card) return;
    
    // Убираем фокус с других карточек
    document.querySelectorAll('.playlist-card.focused').forEach(c => {
        c.classList.remove('focused');
    });
    
    // Добавляем фокус
    card.classList.add('focused');
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Добавляем стили для фокуса
    card.style.outline = '3px solid var(--orthodox-blue)';
    card.style.outlineOffset = '2px';
}

// Сенсорные жесты
function setupTouchGestures() {
    const cards = document.querySelectorAll('.playlist-card');
    
    cards.forEach(card => {
        let touchStartY = 0;
        let touchStartTime = 0;
        
        card.addEventListener('touchstart', function(e) {
            touchStartY = e.touches[0].clientY;
            touchStartTime = Date.now();
            card.style.transform = 'scale(0.98)';
        });
        
        card.addEventListener('touchmove', function(e) {
            e.preventDefault(); // Предотвращаем скролл
        });
        
        card.addEventListener('touchend', function(e) {
            const touchEndY = e.changedTouches[0].clientY;
            const touchDuration = Date.now() - touchStartTime;
            const touchDistance = Math.abs(touchEndY - touchStartY);
            
            card.style.transform = '';
            
            // Если это был тап (короткое касание без движения)
            if (touchDuration < 300 && touchDistance < 10) {
                const playBtn = card.querySelector('.playlist-play-btn');
                if (playBtn) {
                    playBtn.click();
                }
            }
        });
    });
}

// Прогрессивные улучшения
function setupProgressiveEnhancement() {
    // Добавляем индикатор загрузки для медленных соединений
    if (navigator.connection && navigator.connection.effectiveType === 'slow-2g') {
        document.body.classList.add('slow-connection');
        
        // Показываем меньше превью для экономии трафика
        const previewGrids = document.querySelectorAll('.preview-grid');
        previewGrids.forEach(grid => {
            const items = grid.querySelectorAll('.preview-item');
            items.forEach((item, index) => {
                if (index > 1) { // Показываем только первые 2 превью
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Поддержка тёмной темы
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    updateTheme(prefersDark.matches);
    
    prefersDark.addEventListener('change', (e) => {
        updateTheme(e.matches);
    });
}

// Обновление темы
function updateTheme(isDark) {
    document.body.classList.toggle('dark-theme', isDark);
    
    // Сохраняем предпочтение пользователя
    localStorage.setItem('theme-preference', isDark ? 'dark' : 'light');
}

// Утилиты для работы с плейлистами
const PlaylistUtils = {
    // Копирование ссылки на плейлист
    copyPlaylistLink: function(playlistSlug) {
        const url = `${window.location.origin}/stories/playlist/${playlistSlug}/`;
        
        if (navigator.clipboard) {
            navigator.clipboard.writeText(url).then(() => {
                this.showToast('Ссылка скопирована в буфер обмена!');
            });
        } else {
            // Fallback для старых браузеров
            const textArea = document.createElement('textarea');
            textArea.value = url;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.showToast('Ссылка скопирована!');
        }
    },
    
    // Показать уведомление
    showToast: function(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#28a745' : '#dc3545'};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        // Анимация появления
        setTimeout(() => {
            toast.style.transform = 'translateX(0)';
        }, 100);
        
        // Автоудаление
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
    },
    
    // Поделиться плейлистом
    sharePlaylist: function(playlistData) {
        if (navigator.share) {
            navigator.share({
                title: playlistData.title,
                text: `Посмотрите плейлист "${playlistData.title}" на Добрые истории`,
                url: playlistData.url
            });
        } else {
            // Fallback - копируем ссылку
            this.copyPlaylistLink(playlistData.slug);
        }
    }
};

// Делаем утилиты доступными глобально
window.PlaylistUtils = PlaylistUtils;

// Добавляем стили для фокуса
const style = document.createElement('style');
style.textContent = `
    .playlist-card.focused {
        transform: translateY(-4px) !important;
        transition: all 0.2s ease !important;
    }
    
    .toast {
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 14px;
        font-weight: 500;
    }
    
    .slow-connection .preview-grid {
        grid-template-columns: 1fr 1fr !important;
    }
    
    .dark-theme .playlist-card {
        background: #2d3748 !important;
        color: #e2e8f0 !important;
    }
    
    .dark-theme .playlist-title a {
        color: #90cdf4 !important;
    }
    
    .dark-theme .playlist-description {
        color: #a0aec0 !important;
    }
`;
document.head.appendChild(style);
