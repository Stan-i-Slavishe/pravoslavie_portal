// ИСПРАВЛЕННАЯ ФУНКЦИЯ toggleUserPlaylist
// Заменяет старую функцию в шаблоне

console.log('🔧 Загружено исправление toggleUserPlaylist');

// Переопределяем глобальную функцию
window.toggleUserPlaylist = async function(playlistId) {
    console.log('🎯 toggleUserPlaylist вызвана для плейлиста:', playlistId);
    
    const checkbox = document.getElementById(`playlist_${playlistId}`);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    if (!checkbox) {
        console.error('❌ Чекбокс не найден:', `playlist_${playlistId}`);
        return;
    }
    
    // Переключаем чекбокс
    checkbox.checked = !checkbox.checked;
    const action = checkbox.checked ? 'add' : 'remove';
    
    console.log(`🔄 ${action} - плейлист ${playlistId}`);
    
    try {
        // Используем наш новый API
        const formData = new FormData();
        formData.append('story_slug', getStorySlugFromUrl());
        formData.append('playlist_id', playlistId);
        formData.append('action', action);
        
        const response = await fetch('/stories/api/toggle-playlist/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                console.log('✅ Успешно:', data.message);
                showMiniToast(data.message, 'success');
                
                // Обновляем счетчик если есть
                updatePlaylistCounter(playlistId, action);
            } else {
                console.error('❌ Ошибка API:', data.message);
                checkbox.checked = !checkbox.checked; // Откат
                showMiniToast(data.message || 'Ошибка', 'error');
            }
        } else {
            console.error('❌ HTTP ошибка:', response.status);
            checkbox.checked = !checkbox.checked; // Откат
            showMiniToast('Ошибка сервера', 'error');
        }
        
    } catch (error) {
        console.error('❌ Ошибка AJAX:', error);
        checkbox.checked = !checkbox.checked; // Откат
        showMiniToast('Ошибка соединения', 'error');
    }
};

// Вспомогательные функции
function getStorySlugFromUrl() {
    const url = window.location.pathname;
    const parts = url.split('/').filter(Boolean);
    return parts[parts.length - 1] || parts[parts.length - 2];
}

function updatePlaylistCounter(playlistId, action) {
    const checkbox = document.getElementById(`playlist_${playlistId}`);
    const playlistItem = checkbox?.closest('.playlist-item');
    const countElement = playlistItem?.querySelector('.playlist-count');
    
    if (countElement) {
        const currentText = countElement.textContent;
        const currentCount = parseInt(currentText.match(/\d+/)?.[0] || '0');
        const newCount = action === 'add' ? currentCount + 1 : Math.max(0, currentCount - 1);
        const newText = newCount > 0 ? `${newCount} видео` : 'Пустой';
        countElement.textContent = newText;
    }
}

// Переопределяем функцию showMiniToast если её нет
if (typeof showMiniToast === 'undefined') {
    window.showMiniToast = function(message, type = 'success') {
        console.log(`📢 ${type.toUpperCase()}: ${message}`);
        
        // Создаем простое уведомление
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed; top: 20px; right: 20px; z-index: 10000;
            background: ${type === 'success' ? '#28a745' : '#dc3545'}; 
            color: white; padding: 12px 20px; border-radius: 8px;
            font-size: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            max-width: 300px; word-wrap: break-word;
        `;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100%)';
                setTimeout(() => toast.remove(), 300);
            }
        }, 3000);
    };
}

console.log('✅ toggleUserPlaylist исправлена и готова к работе!');
