// Глобальные функции для уведомлений и CSRF
// Это должно загружаться первым, чтобы другие скрипты могли использовать эти функции

// Функция показа Toast уведомлений
function showToast(message, type = 'info') {
    // Создаем toast уведомление
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        // Если контейнер не найден, создаем его
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    const toastId = 'toast-' + Date.now();
    const bgClass = type === 'success' ? 'bg-success' : type === 'error' ? 'bg-danger' : 'bg-info';
    const iconClass = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle';
    
    const toastHTML = `
        <div id="${toastId}" class="toast ${bgClass} text-white" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header ${bgClass} text-white border-0">
                <i class="bi bi-${iconClass} me-2"></i>
                <strong class="me-auto">Уведомление</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    const toastElement = document.createElement('div');
    toastElement.innerHTML = toastHTML;
    const toast = toastElement.firstElementChild;
    
    toastContainer.appendChild(toast);
    
    // Инициализируем и показываем toast
    if (typeof bootstrap !== 'undefined') {
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Удаляем toast после скрытия
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    } else {
        // Fallback для случая, если Bootstrap не загружен
        toast.style.display = 'block';
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
}

// Функция получения CSRF токена
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

// Глобальная функция получения CSRF токена из разных источников
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || 
           document.querySelector('meta[name="csrftoken"]')?.getAttribute('content') ||
           document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
           getCookie('csrftoken');
}

console.log('✅ Global utilities loaded');
