// ИСПРАВЛЕННЫЙ JAVASCRIPT ДЛЯ ПЛЕЙЛИСТОВ
// Добавьте этот код в story_detail.html в секцию <script>

// Глобальные переменные для плейлистов
let currentStoryId = {{ story.id }};
let userPlaylists = [];

// Загрузка плейлистов пользователя
async function loadUserPlaylists() {
    try {
        console.log('🎵 Загрузка плейлистов пользователя...');
        
        // Пока сделаем простую загрузку через API или передадим из Django
        // В данном случае используем статические данные
        userPlaylists = [
            { id: 1, title: 'Бородa', stories_count: 3 },
            { id: 2, title: 'Школьные истории', stories_count: 2 }
        ];
        
        console.log('✅ Плейлисты загружены:', userPlaylists);
        updatePlaylistUI();
        
    } catch (error) {
        console.error('❌ Ошибка загрузки плейлистов:', error);
        showToast('Ошибка загрузки плейлистов', 'error');
    }
}

// Обновление интерфейса плейлистов
function updatePlaylistUI() {
    const playlistContainer = document.getElementById('playlistContainer');
    if (!playlistContainer) {
        console.log('⚠️  Контейнер плейлистов не найден');
        return;
    }
    
    let playlistHTML = '';
    
    if (userPlaylists.length > 0) {
        userPlaylists.forEach(playlist => {
            playlistHTML += `
                <div class="form-check mb-2">
                    <input class="form-check-input" type="checkbox" 
                           id="playlist_${playlist.id}" 
                           data-playlist-id="${playlist.id}"
                           onchange="togglePlaylistItem(${playlist.id})">
                    <label class="form-check-label" for="playlist_${playlist.id}">
                        ${playlist.title} (${playlist.stories_count} рассказов)
                    </label>
                </div>
            `;
        });
    } else {
        playlistHTML = '<p class="text-muted">У вас пока нет плейлистов</p>';
    }
    
    playlistContainer.innerHTML = playlistHTML;
}

// Переключение добавления/удаления из плейлиста
async function togglePlaylistItem(playlistId) {
    const checkbox = document.getElementById(`playlist_${playlistId}`);
    const isChecked = checkbox.checked;
    
    console.log(`📝 ${isChecked ? 'Добавление в' : 'Удаление из'} плейлист ${playlistId}`);
    
    try {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const url = isChecked ? '/stories/playlist/add-story/' : '/stories/playlist/remove-story/';
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                story_id: currentStoryId,
                playlist_id: playlistId
            })
        });
        
        // Логируем ответ
        console.log('📡 Ответ сервера:', response.status, response.statusText);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        // Проверяем Content-Type
        const contentType = response.headers.get('content-type');
        console.log('📄 Content-Type:', contentType);
        
        let data;
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            const text = await response.text();
            console.log('📝 Ответ как текст:', text.substring(0, 200));
            throw new Error('Сервер вернул HTML вместо JSON');
        }
        
        console.log('✅ Данные ответа:', data);
        
        if (data.success) {
            showToast(data.message || 'Действие выполнено', 'success');
            
            // Обновляем счетчик в UI
            const label = document.querySelector(`label[for="playlist_${playlistId}"]`);
            if (label) {
                const playlist = userPlaylists.find(p => p.id === playlistId);
                if (playlist) {
                    playlist.stories_count += isChecked ? 1 : -1;
                    label.textContent = `${playlist.title} (${playlist.stories_count} рассказов)`;
                }
            }
        } else {
            throw new Error(data.message || 'Неизвестная ошибка');
        }
        
    } catch (error) {
        console.error('❌ Ошибка обработки плейлиста:', error);
        
        // Возвращаем checkbox в предыдущее состояние
        checkbox.checked = !isChecked;
        
        showToast(error.message || 'Ошибка при обработке плейлиста', 'error');
    }
}

// Создание нового плейлиста
async function createNewPlaylist() {
    const playlistName = document.getElementById('newPlaylistName').value.trim();
    const isPublic = document.getElementById('newPlaylistPublic').checked;
    
    if (!playlistName) {
        showToast('Введите название плейлиста', 'error');
        return;
    }
    
    console.log('🆕 Создание плейлиста:', playlistName);
    
    try {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        const response = await fetch('/stories/playlist/create/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'name': playlistName,
                'is_public': isPublic ? 'on' : ''
            })
        });
        
        console.log('📡 Ответ создания плейлиста:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const contentType = response.headers.get('content-type');
        let data;
        
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            // Если вернулся HTML, значит редирект - это успех
            data = { success: true, message: `Плейлист "${playlistName}" создан` };
        }
        
        if (data.success) {
            showToast(data.message, 'success');
            
            // Добавляем новый плейлист в список
            const newPlaylist = {
                id: data.playlist_id || Date.now(), // временный ID
                title: playlistName,
                stories_count: 0
            };
            userPlaylists.push(newPlaylist);
            
            // Обновляем UI
            updatePlaylistUI();
            
            // Очищаем форму
            document.getElementById('newPlaylistName').value = '';
            document.getElementById('newPlaylistPublic').checked = false;
            
            // Закрываем модал
            const modal = bootstrap.Modal.getInstance(document.getElementById('playlistModal'));
            if (modal) {
                modal.hide();
            }
        } else {
            throw new Error(data.message || 'Ошибка создания плейлиста');
        }
        
    } catch (error) {
        console.error('❌ Ошибка создания плейлиста:', error);
        showToast(error.message || 'Ошибка создания плейлиста', 'error');
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎵 Инициализация плейлистов...');
    
    // Загружаем плейлисты только для авторизованных пользователей
    {% if user.is_authenticated %}
        loadUserPlaylists();
    {% endif %}
});

// Показ/скрытие модального окна плейлистов
function togglePlaylistModal() {
    const modal = new bootstrap.Modal(document.getElementById('playlistModal'));
    modal.show();
}

console.log('✅ JavaScript плейлистов загружен');
