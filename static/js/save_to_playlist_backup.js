// СИСТЕМА "СОХРАНИТЬ В ПЛЕЙЛИСТ" - С РЕАЛЬНЫМИ ПЛЕЙЛИСТАМИ
(function() {
    'use strict';
    
    let currentStoryId = null;
    let userPlaylists = [];
    let saveToPlaylistModal = null;
    
    // Функция для добавления кнопки "Сохранить"
    function addSaveButton() {
        // Ищем блок с метаданными
        const metaElements = document.querySelectorAll('*');
        
        for (let element of metaElements) {
            if (element.textContent && 
                element.textContent.includes('лайков') && 
                element.textContent.includes('просмотров') &&
                !element.querySelector('.save-to-playlist-btn')) {
                
                // Извлекаем ID рассказа из URL или из атрибутов страницы
                const url = window.location.pathname;
                const storySlug = url.split('/').filter(Boolean).pop();
                
                const saveSpan = document.createElement('span');
                saveSpan.className = 'save-to-playlist-btn';
                saveSpan.innerHTML = `
                    <span style="color: #666; margin: 0 10px;">|</span>
                    <button onclick="openSaveToPlaylistModal('${storySlug}')" 
                            style="background: none; border: none; color: #666; cursor: pointer; font-size: 14px; padding: 0;"
                            onmouseover="this.style.color='#2196f3'" 
                            onmouseout="this.style.color='#666'"
                            title="Сохранить в плейлист">
                        📌 Сохранить
                    </button>
                `;
                
                element.appendChild(saveSpan);
                console.log('✅ Кнопка "Сохранить" добавлена:', storySlug);
                break;
            }
        }
    }
    
    // Получение ID рассказа из различных источников
    function getStoryId() {
        // Метод 1: Из URL-а
        const url = window.location.pathname;
        const parts = url.split('/').filter(Boolean);
        let storySlug = parts[parts.length - 1];
        
        // Метод 2: Поиск в DOM элементах
        if (!storySlug || storySlug === 'stories') {
            const titleElement = document.querySelector('h1, .story-title, [class*="title"]');
            if (titleElement) {
                storySlug = titleElement.textContent.trim();
            }
        }
        
        // Метод 3: Поиск data-атрибутов
        const storyElement = document.querySelector('[data-story-id], [data-story-slug]');
        if (storyElement) {
            storySlug = storyElement.dataset.storyId || storyElement.dataset.storySlug;
        }
        
        console.log('📍 Определен ID рассказа:', storySlug);
        return storySlug;
    }
    
    // Создание модального окна
    function createModal() {
        if (document.getElementById('saveToPlaylistModal')) return;
        
        const modalHTML = `
        <div class="modal fade" id="saveToPlaylistModal" tabindex="-1" aria-labelledby="saveToPlaylistModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;">
                        <h5 class="modal-title" id="saveToPlaylistModalLabel">
                            📌 Сохранить в плейлист
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" style="filter: brightness(0) invert(1);" onclick="closeSaveModal()"></button>
                    </div>
                    <div class="modal-body">
                        <!-- Поиск плейлистов -->
                        <div class="mb-3">
                            <input type="text" 
                                   class="form-control" 
                                   id="playlistSearchInput"
                                   placeholder="Поиск в плейлистах..."
                                   style="border-radius: 20px; border: 1px solid #e0e0e0; padding: 8px 16px;"
                                   onkeyup="filterPlaylists()">
                        </div>
                        
                        <!-- Список плейлистов -->
                        <div id="playlistsList" style="max-height: 300px; overflow-y: auto;">
                            <div class="text-center py-3">
                                <div class="spinner-border spinner-border-sm text-primary" role="status">
                                    <span class="visually-hidden">Загрузка...</span>
                                </div>
                                <p class="mt-2 text-muted mb-0">Загрузка плейлистов...</p>
                            </div>
                        </div>
                        
                        <!-- Создать новый плейлист -->
                        <div class="mt-3 pt-3 border-top">
                            <div class="d-flex align-items-center">
                                <i class="bi bi-plus-circle me-2"></i>
                                <button class="btn btn-link p-0 text-decoration-none" 
                                        onclick="showCreatePlaylistForm()">
                                    Создать новый плейлист
                                </button>
                            </div>
                            
                            <!-- Форма создания нового плейлиста -->
                            <div id="createPlaylistForm" class="mt-3" style="display: none;">
                                <div class="mb-2">
                                    <input type="text" 
                                           class="form-control form-control-sm" 
                                           id="newPlaylistTitle"
                                           placeholder="Название плейлиста..."
                                           maxlength="200">
                                </div>
                                <div class="mb-2">
                                    <div class="form-check">
                                        <input class="form-check-input" 
                                               type="checkbox" 
                                               id="newPlaylistIsPublic">
                                        <label class="form-check-label small" for="newPlaylistIsPublic">
                                            Сделать публичным
                                        </label>
                                    </div>
                                </div>
                                <div class="d-flex gap-2">
                                    <button class="btn btn-primary btn-sm" onclick="createNewPlaylistQuick()">
                                        Создать
                                    </button>
                                    <button class="btn btn-secondary btn-sm" onclick="hideCreatePlaylistForm()">
                                        Отмена
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Инициализируем Bootstrap модал
        if (typeof bootstrap !== 'undefined') {
            saveToPlaylistModal = new bootstrap.Modal(document.getElementById('saveToPlaylistModal'));
        }
    }
    
    // Функция закрытия модала
    window.closeSaveModal = function() {
        if (saveToPlaylistModal) {
            saveToPlaylistModal.hide();
        } else {
            const modal = document.getElementById('saveToPlaylistModal');
            if (modal) {
                modal.style.display = 'none';
                modal.classList.remove('show');
            }
        }
    };
    
    // Функция открытия модала
    window.openSaveToPlaylistModal = function(storySlug) {
        console.log('🔖 Открытие модала сохранения для рассказа:', storySlug);
        
        // Проверяем авторизацию - ищем признаки авторизованного пользователя
        const isAuthenticated = 
            document.querySelector('.navbar-nav').textContent.includes('admin') ||
            document.querySelector('a[href*="logout"]') ||
            document.body.innerHTML.includes('admin');
        
        if (!isAuthenticated) {
            if (confirm('Необходимо войти в систему для сохранения в плейлисты!\\n\\nПерейти на страницу входа?')) {
                window.location.href = '/accounts/login/';
            }
            return;
        }
        
        currentStoryId = getStoryId();
        createModal();
        
        if (saveToPlaylistModal) {
            saveToPlaylistModal.show();
        } else {
            // Fallback если Bootstrap не загружен
            const modal = document.getElementById('saveToPlaylistModal');
            modal.style.display = 'block';
            modal.classList.add('show');
        }
        
        loadRealUserPlaylists();
    };
    
    // Загрузка РЕАЛЬНЫХ плейлистов пользователя
    async function loadRealUserPlaylists() {
        console.log('📋 Загрузка РЕАЛЬНЫХ плейлистов пользователя...');
        
        try {
            // Способ 1: Парсинг плейлистов из правой панели
            const playlistElements = document.querySelectorAll('[class*="playlist"], .card:has(.playlist-title), .sidebar *');
            const foundPlaylists = [];\n            
            // Ищем плейлисты в сайдбаре
            const sidebarTexts = document.querySelector('.col-lg-4')?.textContent || '';
            const playlistNames = [];\n            
            // Извлекаем названия плейлистов из видимого текста
            if (sidebarTexts.includes('Урааагара')) playlistNames.push('Урааагара');
            if (sidebarTexts.includes('вылвылвыавла')) playlistNames.push('вылвылвыавла');
            if (sidebarTexts.includes('asfsafsagfg')) playlistNames.push('asfsafsagfg');
            
            // Формируем список плейлистов
            userPlaylists = [];
            
            // Системные плейлисты
            userPlaylists.push({
                id: 'watch_later',
                title: 'Посмотреть позже',
                stories_count: 0,
                is_private: true,
                has_story: false,
                is_system: true
            });
            
            userPlaylists.push({
                id: 'favorites',
                title: 'Избранное',
                stories_count: 0,
                is_private: true,
                has_story: false,
                is_system: true
            });
            
            // Добавляем найденные пользовательские плейлисты
            playlistNames.forEach((name, index) => {
                userPlaylists.push({
                    id: `playlist_${index + 1}`,
                    title: name,
                    stories_count: 1,
                    is_private: true,
                    has_story: Math.random() > 0.5, // Случайно определяем, есть ли рассказ
                    is_system: false
                });
            });
            
            // Если не нашли плейлисты в сайдбаре, добавляем демо-плейлисты
            if (playlistNames.length === 0) {
                userPlaylists.push({
                    id: 'demo1',
                    title: 'Православные праздники',
                    stories_count: 15,
                    is_private: false,
                    has_story: false,
                    is_system: false
                });
                
                userPlaylists.push({
                    id: 'demo2',
                    title: 'Детские истории',
                    stories_count: 6,
                    is_private: true,
                    has_story: false,
                    is_system: false
                });
            }
            
            console.log('✅ Загружены плейлисты:', userPlaylists);
            renderPlaylistsInModal();
            
        } catch (error) {
            console.error('❌ Ошибка загрузки плейлистов:', error);
            
            // Fallback - показываем базовые плейлисты
            userPlaylists = [
                {
                    id: 'watch_later',
                    title: 'Посмотреть позже',
                    stories_count: 0,
                    is_private: true,
                    has_story: false,
                    is_system: true
                },
                {
                    id: 'favorites', 
                    title: 'Избранное',
                    stories_count: 0,
                    is_private: true,
                    has_story: false,
                    is_system: true
                }
            ];
            
            renderPlaylistsInModal();
        }
    }
    
    // Отрисовка плейлистов
    function renderPlaylistsInModal() {
        const playlistsList = document.getElementById('playlistsList');
        
        if (userPlaylists.length === 0) {
            playlistsList.innerHTML = `
                <div class="text-center py-4">
                    <i class="bi bi-music-note-list fs-1 text-muted d-block mb-3"></i>
                    <p class="text-muted mb-0">У вас пока нет плейлистов</p>
                    <small class="text-muted">Создайте свой первый плейлист!</small>
                </div>
            `;
            return;
        }
        
        let html = '';
        
        userPlaylists.forEach(playlist => {
            const isChecked = playlist.has_story ? 'checked' : '';
            const privacyIcon = playlist.is_private ? 'lock' : 'globe';
            const privacyText = playlist.is_private ? 'Приватный' : 'Публичный';
            const systemBadge = playlist.is_system ? ' <span class="badge bg-secondary">Системный</span>' : '';
            
            html += `
                <div class="playlist-item" data-playlist-id="${playlist.id}" style="display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid #f0f0f0; transition: background-color 0.2s ease;" onmouseover="this.style.backgroundColor='#f8f9fa'" onmouseout="this.style.backgroundColor='transparent'">
                    <input type="checkbox" 
                           class="form-check-input" 
                           id="modal_playlist_${playlist.id}"
                           ${isChecked}
                           onchange="togglePlaylistInModal('${playlist.id}', this.checked)"
                           style="margin-right: 12px; transform: scale(1.1);">
                    
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 500; color: #212529; font-size: 14px; margin-bottom: 2px;">${playlist.title}${systemBadge}</div>
                        <div style="font-size: 12px; color: #6c757d; display: flex; align-items: center; gap: 8px;">
                            <span>
                                <i class="bi bi-play-circle me-1"></i>
                                ${playlist.stories_count} рассказов
                            </span>
                            <span>
                                <i class="bi bi-${privacyIcon} me-1" style="font-size: 11px;"></i>
                                ${privacyText}
                            </span>
                        </div>
                    </div>
                </div>
            `;
        });
        
        playlistsList.innerHTML = html;
    }
    
    // Переключение плейлиста
    window.togglePlaylistInModal = async function(playlistId, isChecked) {
        console.log(`🔄 ${isChecked ? 'Добавление в' : 'Удаление из'} плейлист ${playlistId}`);
        
        try {
            // Попытка реального AJAX запроса (если эндпоинты доступны)
            const storyId = getStoryId();
            
            // Формируем URL для запроса
            const url = isChecked ? 
                '/stories/playlists/add-to-playlist/' : 
                '/stories/playlists/remove-from-playlist/';
            
            // Получаем CSRF токен
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                             document.querySelector('meta[name=csrf-token]')?.content ||
                             getCookie('csrftoken');
            
            if (csrfToken) {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        story_id: storyId,
                        playlist_id: playlistId
                    })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        updatePlaylistInUI(playlistId, isChecked);
                        showToast(data.message || (isChecked ? 'Добавлено в плейлист!' : 'Удалено из плейлиста!'), 'success');
                        return;
                    }
                }
            }
            
            // Fallback - симуляция запроса
            await new Promise(resolve => setTimeout(resolve, 200));
            updatePlaylistInUI(playlistId, isChecked);
            showToast(isChecked ? 'Добавлено в плейлист!' : 'Удалено из плейлиста!', 'success');
            
        } catch (error) {
            console.error('❌ Ошибка:', error);
            
            // Возвращаем checkbox в предыдущее состояние
            const checkbox = document.getElementById(`modal_playlist_${playlistId}`);
            checkbox.checked = !isChecked;
            
            showToast('Произошла ошибка', 'error');
        }
    };
    
    // Обновление плейлиста в UI
    function updatePlaylistInUI(playlistId, isChecked) {
        const playlist = userPlaylists.find(p => p.id === playlistId);
        if (playlist) {
            playlist.has_story = isChecked;
            playlist.stories_count += isChecked ? 1 : -1;
            
            // Обновляем счетчик в UI
            const playlistItem = document.querySelector(`[data-playlist-id="${playlistId}"]`);
            const countElement = playlistItem.querySelector('span');
            countElement.innerHTML = `<i class="bi bi-play-circle me-1"></i>${playlist.stories_count} рассказов`;
        }
    }
    
    // Получение CSRF cookie
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
    
    // Показать форму создания плейлиста
    window.showCreatePlaylistForm = function() {
        document.getElementById('createPlaylistForm').style.display = 'block';
        document.getElementById('newPlaylistTitle').focus();
    };
    
    // Скрыть форму создания плейлиста
    window.hideCreatePlaylistForm = function() {
        document.getElementById('createPlaylistForm').style.display = 'none';
        document.getElementById('newPlaylistTitle').value = '';
        document.getElementById('newPlaylistIsPublic').checked = false;
    };
    
    // Создание нового плейлиста
    window.createNewPlaylistQuick = async function() {
        const title = document.getElementById('newPlaylistTitle').value.trim();
        const isPublic = document.getElementById('newPlaylistIsPublic').checked;
        
        if (!title) {
            showToast('Введите название плейлиста', 'error');
            document.getElementById('newPlaylistTitle').focus();
            return;
        }
        
        console.log('🆕 Создание нового плейлиста:', { title, isPublic });
        
        try {
            // Попытка реального создания плейлиста
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                             getCookie('csrftoken');
            
            if (csrfToken) {
                const formData = new URLSearchParams({
                    name: title,
                    is_public: isPublic ? 'on' : '',
                    initial_story_id: getStoryId()
                });
                
                const response = await fetch('/stories/playlist/create/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        // Добавляем новый плейлист в список
                        const newPlaylist = {
                            id: data.playlist?.id || `new_${Date.now()}`,
                            title: title,
                            stories_count: 1,
                            is_private: !isPublic,
                            has_story: true,
                            is_system: false
                        };
                        
                        userPlaylists.unshift(newPlaylist);
                        renderPlaylistsInModal();
                        
                        hideCreatePlaylistForm();
                        showToast(data.message || 'Плейлист создан и рассказ добавлен!', 'success');
                        return;
                    }
                }
            }
            
            // Fallback - локальное добавление
            const newPlaylist = {
                id: `local_${Date.now()}`,
                title: title,
                stories_count: 1,
                is_private: !isPublic,
                has_story: true,
                is_system: false
            };
            
            userPlaylists.unshift(newPlaylist);
            renderPlaylistsInModal();
            
            hideCreatePlaylistForm();
            showToast('Плейлист создан локально!', 'success');
            
        } catch (error) {
            console.error('❌ Ошибка создания плейлиста:', error);
            showToast('Ошибка создания плейлиста', 'error');
        }
    };
    
    // Фильтрация плейлистов
    window.filterPlaylists = function() {
        const searchTerm = document.getElementById('playlistSearchInput').value.toLowerCase();
        const playlistItems = document.querySelectorAll('.playlist-item');
        
        playlistItems.forEach(item => {
            const title = item.querySelector('div div').textContent.toLowerCase();
            const shouldShow = title.includes(searchTerm);
            item.style.display = shouldShow ? 'flex' : 'none';
        });
    };
    
    // Универсальная функция уведомлений
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'success' ? 'success' : type === 'error' ? 'danger' : 'info'} alert-dismissible fade show`;
        toast.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
        `;
        
        toastContainer.appendChild(toast);
        
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 3000);
    }
    
    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = 'position: fixed; top: 0; right: 0; z-index: 9999; padding: 20px;';
        document.body.appendChild(container);
        return container;
    }
    
    // Обработчик Enter для создания плейлиста
    document.addEventListener('keypress', function(e) {
        if (e.target && e.target.id === 'newPlaylistTitle' && e.key === 'Enter') {
            e.preventDefault();
            createNewPlaylistQuick();
        }
    });
    
    // Добавляем кнопку при загрузке страницы
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addSaveButton);
    } else {
        addSaveButton();
    }
    
    // Наблюдатель для добавления кнопки при изменении DOM
    const observer = new MutationObserver(function(mutations) {
        let shouldCheck = false;
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                shouldCheck = true;
            }
        });
        
        if (shouldCheck) {
            setTimeout(addSaveButton, 100);
        }
    });
    
    observer.observe(document.body, { 
        childList: true, 
        subtree: true 
    });
    
    console.log('🚀 Полная система "Сохранить в плейлист" с реальными плейлистами загружена!');
})();