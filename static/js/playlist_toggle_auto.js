// АВТОМАТИЧЕСКИЙ СКРИПТ ДЛЯ ДОБАВЛЕНИЯ КНОПКИ СВОРАЧИВАНИЯ К ПЛЕЙЛИСТАМ
// Добавьте этот скрипт в конец HTML файла или подключите как отдельный JS файл

(function() {
    'use strict';
    
    console.log('🔧 Запуск автоматического исправления плейлистов...');
    
    // Функция для поиска блока плейлистов
    function findPlaylistBlock() {
        // Вариант 1: Поиск по тексту "Плейлисты"
        const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        for (const heading of headings) {
            if (heading.textContent.includes('Плейлисты')) {
                console.log('✅ Найден заголовок плейлистов:', heading);
                return heading.closest('.card') || heading.parentElement;
            }
        }
        
        // Вариант 2: Поиск по иконке музыки
        const musicIcons = document.querySelectorAll('.bi-music-note-list');
        for (const icon of musicIcons) {
            const parent = icon.closest('.card, .card-header, .sidebar, div');
            if (parent) {
                console.log('✅ Найден блок плейлистов по иконке:', parent);
                return parent;
            }
        }
        
        // Вариант 3: Поиск по классам плейлистов
        const playlistContainers = document.querySelectorAll('.playlist-item, .user-playlists, .playlist-list');
        if (playlistContainers.length > 0) {
            const container = playlistContainers[0].closest('.card, .sidebar, div[class*="playlist"]') || 
                            playlistContainers[0].parentElement.parentElement;
            if (container) {
                console.log('✅ Найден контейнер плейлистов:', container);
                return container;
            }
        }
        
        return null;
    }
    
    // Функция создания кнопки сворачивания
    function createToggleButton() {
        const button = document.createElement('button');
        button.id = 'togglePlaylistsBtn';
        button.className = 'btn btn-sm btn-outline-secondary border-0 p-1';
        button.title = 'Свернуть/развернуть плейлисты';
        button.style.cssText = 'width: 24px; height: 24px; border-radius: 4px; transition: all 0.2s ease;';
        
        const icon = document.createElement('i');
        icon.id = 'togglePlaylistsIcon';
        icon.className = 'bi bi-chevron-up';
        icon.style.cssText = 'font-size: 0.8rem; transition: transform 0.3s ease;';
        
        button.appendChild(icon);
        button.onclick = togglePlaylistVisibility;
        
        return button;
    }
    
    // Функция добавления заголовка с кнопкой
    function addHeaderWithButton(playlistBlock) {
        // Проверяем, есть ли уже наш заголовок
        if (document.getElementById('togglePlaylistsBtn')) {
            console.log('⚠️ Кнопка уже существует, пропускаем...');
            return;
        }
        
        // Создаем новый заголовок
        const header = document.createElement('div');
        header.className = 'card-header d-flex justify-content-between align-items-center py-2 px-3';
        header.style.cssText = 'background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-bottom: 1px solid #dee2e6;';
        
        // Левая часть с иконкой и текстом
        const leftPart = document.createElement('div');
        leftPart.className = 'd-flex align-items-center';
        
        const icon = document.createElement('i');
        icon.className = 'bi bi-music-note-list text-primary me-2';
        icon.style.cssText = 'font-size: 1.1rem;';
        
        const title = document.createElement('h6');
        title.className = 'mb-0 fw-semibold text-dark';
        title.textContent = 'Плейлисты';
        
        leftPart.appendChild(icon);
        leftPart.appendChild(title);
        
        // Правая часть с кнопкой
        const toggleButton = createToggleButton();
        
        // Собираем заголовок
        header.appendChild(leftPart);
        header.appendChild(toggleButton);
        
        // Ищем содержимое плейлистов и сохраняем его
        const existingContent = playlistBlock.innerHTML;
        
        // Создаем контейнер для содержимого
        const contentContainer = document.createElement('div');
        contentContainer.className = 'card-body p-0';
        contentContainer.id = 'playlistsContent';
        contentContainer.innerHTML = existingContent;
        
        // Очищаем блок и добавляем новую структуру
        playlistBlock.innerHTML = '';
        playlistBlock.appendChild(header);
        playlistBlock.appendChild(contentContainer);
        
        // Добавляем класс карточки если его нет
        if (!playlistBlock.classList.contains('card')) {
            playlistBlock.classList.add('card', 'shadow-sm', 'mb-3');
        }
        
        console.log('✅ Заголовок с кнопкой добавлен!');
    }
    
    // Функция сворачивания/разворачивания
    window.togglePlaylistVisibility = function() {
        const content = document.getElementById('playlistsContent');
        const icon = document.getElementById('togglePlaylistsIcon');
        const btn = document.getElementById('togglePlaylistsBtn');
        
        if (!content || !icon) {
            console.log('⚠️ Элементы не найдены');
            return;
        }
        
        const isVisible = content.style.display !== 'none';
        
        if (isVisible) {
            // Сворачиваем
            content.style.transition = 'all 0.3s ease';
            content.style.opacity = '0';
            content.style.transform = 'translateY(-10px)';
            
            setTimeout(() => {
                content.style.display = 'none';
            }, 300);
            
            icon.classList.remove('bi-chevron-up');
            icon.classList.add('bi-chevron-down');
            if (btn) btn.title = 'Развернуть плейлисты';
            localStorage.setItem('playlistsCollapsed', 'true');
            
            console.log('📁 Плейлисты свернуты');
            
        } else {
            // Разворачиваем
            content.style.display = 'block';
            content.style.opacity = '0';
            content.style.transform = 'translateY(-10px)';
            
            setTimeout(() => {
                content.style.opacity = '1';
                content.style.transform = 'translateY(0)';
            }, 10);
            
            icon.classList.remove('bi-chevron-down');
            icon.classList.add('bi-chevron-up');
            if (btn) btn.title = 'Свернуть плейлисты';
            localStorage.setItem('playlistsCollapsed', 'false');
            
            console.log('📂 Плейлисты развернуты');
        }
    };
    
    // Восстановление состояния
    function restoreState() {
        const content = document.getElementById('playlistsContent');
        const icon = document.getElementById('togglePlaylistsIcon');
        const btn = document.getElementById('togglePlaylistsBtn');
        
        if (!content || !icon) return;
        
        const isCollapsed = localStorage.getItem('playlistsCollapsed') === 'true';
        
        if (isCollapsed) {
            content.style.display = 'none';
            icon.classList.remove('bi-chevron-up');
            icon.classList.add('bi-chevron-down');
            if (btn) btn.title = 'Развернуть плейлисты';
            console.log('📁 Восстановлено свернутое состояние');
        }
    }
    
    // Добавление CSS стилей
    function addStyles() {
        if (document.getElementById('playlistToggleStyles')) return;
        
        const style = document.createElement('style');
        style.id = 'playlistToggleStyles';
        style.textContent = `
            #togglePlaylistsBtn:hover {
                background-color: rgba(0, 123, 255, 0.1) !important;
                border-color: #007bff !important;
                transform: scale(1.05);
            }
            
            #togglePlaylistsBtn:hover i {
                color: #007bff !important;
            }
            
            #playlistsContent {
                transition: all 0.3s ease;
                transform-origin: top;
            }
            
            .card.shadow-sm {
                box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1) !important;
                border: 1px solid #e3e6ea;
                border-radius: 8px;
            }
        `;
        
        document.head.appendChild(style);
        console.log('🎨 CSS стили добавлены');
    }
    
    // Основная функция
    function init() {
        console.log('🔍 Поиск блока плейлистов...');
        
        const playlistBlock = findPlaylistBlock();
        
        if (playlistBlock) {
            console.log('✅ Блок плейлистов найден!');
            addStyles();
            addHeaderWithButton(playlistBlock);
            
            // Восстанавливаем состояние через небольшую задержку
            setTimeout(restoreState, 100);
            
            console.log('🎉 Автоматическое исправление завершено!');
        } else {
            console.log('❌ Блок плейлистов не найден на странице');
            
            // Попробуем еще раз через секунду (может быть загружается динамически)
            setTimeout(() => {
                console.log('🔄 Повторная попытка поиска...');
                const retryBlock = findPlaylistBlock();
                if (retryBlock) {
                    addStyles();
                    addHeaderWithButton(retryBlock);
                    setTimeout(restoreState, 100);
                    console.log('🎉 Автоматическое исправление завершено (повторная попытка)!');
                } else {
                    console.log('❌ Блок плейлистов так и не найден');
                }
            }, 1000);
        }
    }
    
    // Запускаем когда страница загружена
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();