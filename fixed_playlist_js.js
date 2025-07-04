// ИСПРАВЛЕННЫЙ JavaScript для плейлистов - story_detail.html

// Переключение рассказа в плейлисте
function togglePlaylistStory(playlistId, storyId, checkbox) {
    console.log('togglePlaylistStory called:', { playlistId, storyId, checked: checkbox.checked });
    
    const isAdding = checkbox.checked;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // ИСПРАВЛЕНИЕ: Используем правильные URL из urls.py
    const url = isAdding ? '/stories/playlist/add-story/' : '/stories/playlist/remove-story/';
    
    const requestData = {
        playlist_id: playlistId,
        story_id: storyId
    };
    
    console.log('Отправляем запрос:', url, requestData);
    
    // Блокируем checkbox на время запроса
    checkbox.disabled = true;
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        
        // Проверяем тип контента
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Сервер вернул не JSON ответ');
        }
        
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        
        if (data.success) {
            showToast(data.message, 'success');
        } else {
            // Откатываем состояние checkbox
            checkbox.checked = !checkbox.checked;
            showToast(data.message || 'Ошибка при обновлении плейлиста', 'error');
        }
    })
    .catch(error => {
        console.error('Playlist error:', error);
        
        // Откатываем состояние checkbox
        checkbox.checked = !checkbox.checked;
        showToast('Произошла ошибка при обновлении плейлиста: ' + error.message, 'error');
    })
    .finally(() => {
        // Разблокируем checkbox
        checkbox.disabled = false;
    });
}

// Создание плейлиста - ИСПРАВЛЕННАЯ ВЕРСИЯ
function createPlaylist() {
    const form = document.getElementById('createPlaylistForm');
    const formData = new FormData(form);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // Проверяем обязательное поле
    const name = formData.get('name').trim();
    if (!name) {
        showToast('Введите название плейлиста', 'error');
        return;
    }
    
    // Добавляем CSRF токен в FormData
    formData.append('csrfmiddlewaretoken', csrfToken);
    
    console.log('Создаем плейлист:', {
        name: formData.get('name'),
        description: formData.get('description'),
        is_public: formData.get('is_public')
    });
    
    fetch('/stories/playlist/create/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        console.log('Create response status:', response.status);
        
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    })
    .then(data => {
        console.log('Create response data:', data);
        
        if (data.success) {
            showToast('Плейлист создан успешно!', 'success');
            
            // Закрываем модальное окно
            const modal = bootstrap.Modal.getInstance(document.getElementById('createPlaylistModal'));
            modal.hide();
            
            // Перезагружаем страницу через 1 секунду
            setTimeout(() => {
                location.reload();
            }, 1000);
        } else {
            showToast(data.message || 'Ошибка при создании плейлиста', 'error');
        }
    })
    .catch(error => {
        console.error('Create playlist error:', error);
        showToast('Произошла ошибка при создании плейлиста: ' + error.message, 'error');
    });
}
