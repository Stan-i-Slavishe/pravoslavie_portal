// ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ AJAX ПЛЕЙЛИСТОВ + ЗАГРУЗКА СОСТОЯНИЯ
(function() {
    'use strict';
    
    console.log('🚨 ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ ПЛЕЙЛИСТОВ АКТИВИРОВАНО');
    
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
               document.querySelector('meta[name=csrf-token]')?.content ||
               getCookie('csrftoken');
    }
    
    function getCookie(name) {
        if (document.cookie) {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [key, value] = cookie.trim().split('=');
                if (key === name) {
                    return decodeURIComponent(value);
                }
            }
        }
        return null;
    }
    
    function getStoryId() {
        const path = window.location.pathname;
        const parts = path.split('/').filter(Boolean);
        
        if (parts[0] === 'stories' && parts[1] && !parts[1].includes('playlists')) {
            return parts[1];
        }
        return null;
    }
    
    function notify(message, type = 'success') {
        const existing = document.querySelector('.emergency-notification');
        if (existing) existing.remove();
        
        const div = document.createElement('div');
        div.className = 'emergency-notification';
        div.style.cssText = `
            position: fixed; top: 20px; right: 20px; z-index: 99999;
            padding: 15px 20px; border-radius: 8px; color: white; font-weight: bold;
            background: ${type === 'success' ? '#28a745' : '#dc3545'};
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        div.textContent = message;
        document.body.appendChild(div);
        
        setTimeout(() => div && div.remove(), 3000);
        console.log(`📢 ${message}`);
    }
    
    async function handleCheckbox(checkbox) {
        const playlistId = checkbox.dataset.playlistId || checkbox.id.replace('playlist_', '');
        const isChecked = checkbox.checked;
        const storyId = getStoryId();
        
        console.log(`🔄 Playlist: ${playlistId}, Checked: ${isChecked}, Story: ${storyId}`);
        
        if (!storyId) {
            notify('Ошибка: не найден ID рассказа', 'error');
            checkbox.checked = !isChecked;
            return;
        }
        
        checkbox.disabled = true;
        
        try {
            const csrf = getCSRFToken();
            if (!csrf) {
                throw new Error('CSRF токен не найден');
            }
            
            const url = isChecked ? 
                '/stories/playlists/add-to-playlist/' : 
                '/stories/playlists/remove-from-playlist/';
            
            console.log(`📡 Запрос: ${url}`);
            console.log(`📡 Данные: story_id=${storyId}, playlist_id=${playlistId}`);
            
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    story_id: storyId,
                    playlist_id: playlistId
                })
            });
            
            console.log(`📡 Ответ: ${response.status} ${response.statusText}`);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ Ошибка сервера:', errorText);
                throw new Error(`Ошибка ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            console.log('📡 Данные ответа:', data);
            
            if (data.success) {
                notify(data.message || (isChecked ? 'Добавлено в плейлист!' : 'Удалено из плейлиста!'), 'success');
                updateCounter(checkbox, isChecked);
            } else {
                throw new Error(data.message || 'Неизвестная ошибка');
            }
            
        } catch (error) {
            console.error('❌ Ошибка запроса:', error);
            checkbox.checked = !isChecked;
            notify(`Ошибка: ${error.message}`, 'error');
        } finally {
            checkbox.disabled = false;
        }
    }
    
    function updateCounter(checkbox, wasAdded) {
        const container = checkbox.closest('.playlist-checkbox-row, .d-flex, .form-check');
        if (!container) return;
        
        const counter = container.querySelector('.small, .text-muted');
        if (!counter) return;
        
        const match = counter.textContent.match(/(\d+) рассказов?/);
        if (match) {
            let count = parseInt(match[1]);
            count += wasAdded ? 1 : -1;
            count = Math.max(0, count);
            
            counter.textContent = counter.textContent.replace(
                /(\d+) рассказов?/,
                `${count} рассказ${count === 1 ? '' : count < 5 ? 'а' : 'ов'}`
            );
        }
    }
    
    // 🆕 НОВАЯ ФУНКЦИЯ: Загрузка текущего состояния плейлистов
    async function loadPlaylistStates() {
        const storyId = getStoryId();
        if (!storyId) return;
        
        console.log('📋 Загружаем состояние плейлистов для рассказа:', storyId);
        
        try {
            const csrf = getCSRFToken();
            if (!csrf) return;
            
            const response = await fetch('/stories/playlists/get-story-status/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ story_id: storyId })
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.success && data.playlists) {
                    console.log('✅ Получены данные о плейлистах:', data.playlists);
                    // Обновляем состояние чекбоксов
                    Object.entries(data.playlists).forEach(([playlistId, hasStory]) => {
                        const checkbox = document.querySelector(`[data-playlist-id="${playlistId}"]`);
                        if (checkbox) {
                            checkbox.checked = hasStory;
                            console.log(`📌 Плейлист ${playlistId}: ${hasStory ? 'ЕСТЬ' : 'НЕТ'}`);
                        }
                    });
                    
                    // Показываем уведомление о загрузке
                    notify('🔄 Состояние плейлистов обновлено!', 'success');
                }
            }
        } catch (error) {
            console.log('⚠️ Не удалось загрузить состояние плейлистов:', error);
        }
    }
    
    function init() {
        const selectors = [
            '.playlist-checkbox-item',
            '[data-playlist-id]',
            'input[type="checkbox"][id*="playlist"]',
            'input[type="checkbox"][data-playlist]'
        ];
        
        const checkboxes = [];
        selectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(cb => {
                if (!checkboxes.includes(cb)) {
                    checkboxes.push(cb);
                }
            });
        });
        
        checkboxes.forEach(checkbox => {
            checkbox.removeEventListener('change', handleCheckbox);
            checkbox.addEventListener('change', function() {
                handleCheckbox(this);
            });
        });
        
        console.log(`🎯 Обработчики установлены на ${checkboxes.length} чекбоксов`);
        
        // 🆕 АВТОМАТИЧЕСКИ ЗАГРУЖАЕМ СОСТОЯНИЕ ПЛЕЙЛИСТОВ
        if (checkboxes.length > 0) {
            setTimeout(loadPlaylistStates, 500); // Загружаем через полсекунды
        }
        
        return checkboxes.length;
    }
    
    const observer = new MutationObserver(() => {
        setTimeout(init, 100);
    });
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Глобальные функции для отладки
    window.emergencyPlaylistFix = {
        getStoryId,
        getCSRFToken,
        init,
        loadPlaylistStates,
        test: () => {
            console.log('🧪 ТЕСТ ЭКСТРЕННОГО ИСПРАВЛЕНИЯ:');
            console.log('Story ID:', getStoryId());
            console.log('CSRF:', getCSRFToken() || 'НЕ НАЙДЕН');
            console.log('URL:', window.location.pathname);
            console.log('Чекбоксов найдено:', init());
            
            // Показываем уведомление
            notify('Тест выполнен! Проверьте консоль', 'success');
            
            // Загружаем состояние плейлистов
            loadPlaylistStates();
        }
    };
    
    // Запуск
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Показываем что система активна
    setTimeout(() => {
        if (getStoryId()) {
            notify('🚨 Экстренное исправление плейлистов активно!', 'success');
        }
    }, 1000);
    
    console.log('✅ ЭКСТРЕННОЕ ИСПРАВЛЕНИЕ ПЛЕЙЛИСТОВ ГОТОВО!');
    
})();

// Добавляем тестовую кнопку
(function() {
    function addTestButton() {
        if (document.getElementById('emergencyTestBtn')) return;
        
        const btn = document.createElement('button');
        btn.id = 'emergencyTestBtn';
        btn.textContent = '🚨 ТЕСТ ПЛЕЙЛИСТОВ';
        btn.style.cssText = `
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 99999;
            padding: 10px 15px;
            background: #dc3545;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        `;
        
        btn.onclick = () => {
            if (window.emergencyPlaylistFix) {
                window.emergencyPlaylistFix.test();
            } else {
                alert('Система экстренного исправления не найдена!');
            }
        };
        
        document.body.appendChild(btn);
        console.log('🚨 Тестовая кнопка добавлена');
    }
    
    // Добавляем кнопку через 2 секунды после загрузки
    setTimeout(addTestButton, 2000);
})();