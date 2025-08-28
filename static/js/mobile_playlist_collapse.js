// АВТОМАТИЧЕСКОЕ ДОБАВЛЕНИЕ КНОПКИ СВОРАЧИВАНИЯ К МОБИЛЬНОМУ ВИДЖЕТУ ПЛЕЙЛИСТОВ
(function() {
    'use strict';
    
    console.log('📱 Инициализация кнопки сворачивания для мобильных плейлистов...');
    
    // Функция для поиска мобильного виджета плейлистов (УЛУЧШЕННАЯ ВЕРСИЯ)
    function findMobilePlaylistWidget() {
        console.log('🔍 Поиск мобильного виджета плейлистов...');
        
        // Вариант 1: Поиск по тексту "🎵 Плейлисты" или просто "Плейлисты"
        const textVariants = ['🎵 Плейлисты', 'Плейлисты', '📱 Мои плейлисты'];
        for (const text of textVariants) {
            const elements = document.querySelectorAll('*');
            for (const element of elements) {
                if (element.textContent && element.textContent.includes(text)) {
                    const widget = element.closest('.card, .mobile-widget, div[style*="background"], div[class*="mobile"], .widget, .playlist-widget');
                    if (widget) {
                        console.log(`✅ Найден мобильный виджет плейлистов по тексту "${text}":`, widget);
                        return widget;
                    }
                }
            }
        }
        
        // Вариант 2: Поиск по красному фону (разные варианты цветов)
        const redSelectors = [
            '[style*="background-color: rgb(231, 76, 60)"]',
            '[style*="background: #e74c3c"]',
            '[style*="background-color: #e74c3c"]',
            '.bg-danger',
            '.bg-primary',
            '[style*="background-color: red"]',
            '[style*="background: red"]'
        ];
        
        for (const selector of redSelectors) {
            const elements = document.querySelectorAll(selector);
            for (const element of elements) {
                if (element.textContent && (element.textContent.includes('Плейлисты') || element.textContent.includes('плейлист'))) {
                    console.log(`✅ Найден мобильный виджет плейлистов по селектору "${selector}":`, element);
                    return element;
                }
            }
        }
        
        // Вариант 3: Поиск по иконкам (различные варианты)
        const iconSelectors = [
            '.bi-bookmark', '.bi-bookmark-plus', '.bi-music-note-list',
            '.bi-list', '.bi-collection', '.bi-folder',
            'i[class*="bookmark"]', 'i[class*="music"]', 'i[class*="list"]'
        ];
        
        for (const selector of iconSelectors) {
            const icons = document.querySelectorAll(selector);
            for (const icon of icons) {
                const container = icon.closest('.card, div[style*="background"], .widget, .mobile-widget, .playlist-container');
                if (container && (container.textContent.includes('Плейлисты') || container.textContent.includes('плейлист'))) {
                    console.log(`✅ Найден мобильный виджет плейлистов по иконке "${selector}":`, container);
                    return container;
                }
            }
        }
        
        // Вариант 4: Поиск по классам, связанным с плейлистами
        const playlistSelectors = [
            '.mobile-playlist-widget', '.playlist-widget', '.user-playlists',
            '.playlist-container', '.playlist-sidebar', '[class*="playlist"]',
            '[id*="playlist"]', '.mobile-widget'
        ];
        
        for (const selector of playlistSelectors) {
            const elements = document.querySelectorAll(selector);
            for (const element of elements) {
                if (element.textContent && (element.textContent.includes('Плейлисты') || element.textContent.includes('плейлист'))) {
                    console.log(`✅ Найден мобильный виджет плейлистов по классу "${selector}":`, element);
                    return element;
                }
            }
        }
        
        // Вариант 5: Поиск по мобильным классам Bootstrap
        const mobileSelectors = [
            '.d-lg-none', '.d-md-none', '.d-sm-block',
            '[class*="mobile"]', '.visible-xs', '.hidden-lg'
        ];
        
        for (const selector of mobileSelectors) {
            const elements = document.querySelectorAll(selector);
            for (const element of elements) {
                if (element.textContent && (element.textContent.includes('Плейлисты') || element.textContent.includes('плейлист'))) {
                    console.log(`✅ Найден мобильный виджет плейлистов по мобильному классу "${selector}":`, element);
                    return element;
                }
            }
        }
        
        console.log('❌ Мобильный виджет плейлистов не найден');
        return null;
    }
    
    // Функция для создания кнопки сворачивания
    function createCollapseButton() {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-outline-light ms-2';
        button.style.cssText = `
            padding: 6px 10px;
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.3);
            background: rgba(255,255,255,0.1);
            color: white;
            transition: all 0.2s ease;
            min-width: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        button.title = 'Свернуть/развернуть плейлисты';
        button.id = 'mobilePlaylistCollapseBtn';
        
        const icon = document.createElement('i');
        icon.className = 'bi bi-chevron-down';
        icon.id = 'mobilePlaylistCollapseIcon';
        icon.style.cssText = 'font-size: 0.9rem; transition: transform 0.3s ease;';
        
        button.appendChild(icon);
        return button;
    }
    
    // Функция для добавления кнопки к существующему виджету
    function addCollapseButtonToWidget(widget) {
        // Проверяем, не добавлена ли уже кнопка
        if (document.getElementById('mobilePlaylistCollapseBtn')) {
            console.log('⚠️ Кнопка сворачивания уже существует');
            return;
        }
        
        // Ищем кнопку с иконкой bookmark (кнопка "Сохранить")
        const saveButton = widget.querySelector('.bi-bookmark, .bi-bookmark-plus, .bi-plus')?.closest('button');
        
        if (saveButton) {
            // Добавляем кнопку рядом с кнопкой "Сохранить"
            const collapseButton = createCollapseButton();
            
            // Находим родительский контейнер кнопок
            const buttonContainer = saveButton.parentElement;
            
            // Убеждаемся что контейнер имеет правильные классы
            if (!buttonContainer.classList.contains('d-flex')) {
                buttonContainer.classList.add('d-flex', 'align-items-center');
            }
            
            // Вставляем кнопку после кнопки сохранения
            saveButton.insertAdjacentElement('afterend', collapseButton);
            
            // Добавляем обработчик события
            collapseButton.addEventListener('click', toggleMobilePlaylistContent);
            
            console.log('✅ Кнопка сворачивания добавлена к мобильному виджету рядом с кнопкой сохранения');
            return true;
        } else {
            // Если кнопка "Сохранить" не найдена, добавляем в заголовок
            const header = widget.querySelector('h3, h4, h5, h6, .fw-bold, [style*="font-weight"]');
            if (header) {
                const headerContainer = header.parentElement;
                
                // Делаем заголовок flex контейнером
                headerContainer.style.display = 'flex';
                headerContainer.style.justifyContent = 'space-between';
                headerContainer.style.alignItems = 'center';
                
                // Создаем контейнер для кнопок
                const buttonGroup = document.createElement('div');
                buttonGroup.className = 'd-flex align-items-center';
                
                const collapseButton = createCollapseButton();
                buttonGroup.appendChild(collapseButton);
                
                headerContainer.appendChild(buttonGroup);
                
                // Добавляем обработчик события
                collapseButton.addEventListener('click', toggleMobilePlaylistContent);
                
                console.log('✅ Кнопка сворачивания добавлена в заголовок виджета');
                return true;
            }
        }
        
        console.log('❌ Не удалось найти место для добавления кнопки');
        return false;
    }
    
    // Функция сворачивания/разворачивания контента
    function toggleMobilePlaylistContent() {
        const button = document.getElementById('mobilePlaylistCollapseBtn');
        const icon = document.getElementById('mobilePlaylistCollapseIcon');
        const widget = button.closest('.card, div[style*="background"]');
        
        if (!widget) {
            console.log('❌ Виджет не найден');
            return;
        }
        
        // Ищем контент плейлистов (все что не заголовок)
        const allElements = Array.from(widget.children);
        const header = allElements.find(el => 
            el.querySelector('h1, h2, h3, h4, h5, h6') || 
            el.textContent.includes('Плейлисты')
        );
        
        const contentElements = allElements.filter(el => el !== header);
        
        if (contentElements.length === 0) {
            console.log('❌ Контент плейлистов не найден');
            return;
        }
        
        // Проверяем текущее состояние
        const isCollapsed = contentElements[0].style.display === 'none';
        
        if (isCollapsed) {
            // Разворачиваем
            contentElements.forEach(el => {
                el.style.display = '';
                el.style.opacity = '0';
                el.style.transform = 'translateY(-10px)';
                el.style.transition = 'all 0.3s ease';
                
                setTimeout(() => {
                    el.style.opacity = '1';
                    el.style.transform = 'translateY(0)';
                }, 10);
            });
            
            icon.classList.remove('bi-chevron-up');
            icon.classList.add('bi-chevron-down');
            button.title = 'Свернуть плейлисты';
            
            // Вибрация если поддерживается
            if (navigator.vibrate) {
                navigator.vibrate(50);
            }
            
            console.log('📂 Мобильные плейлисты развернуты');
            
        } else {
            // Сворачиваем
            contentElements.forEach(el => {
                el.style.transition = 'all 0.3s ease';
                el.style.opacity = '0';
                el.style.transform = 'translateY(-10px)';
                
                setTimeout(() => {
                    el.style.display = 'none';
                }, 300);
            });
            
            icon.classList.remove('bi-chevron-down');
            icon.classList.add('bi-chevron-up');
            button.title = 'Развернуть плейлисты';
            
            // Вибрация если поддерживается
            if (navigator.vibrate) {
                navigator.vibrate(30);
            }
            
            console.log('📁 Мобильные плейлисты свернуты');
        }
        
        // Анимация кнопки
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 150);
    }
    
    // Добавляем CSS стили
    function addStyles() {
        if (document.getElementById('mobilePlaylistCollapseStyles')) return;
        
        const style = document.createElement('style');
        style.id = 'mobilePlaylistCollapseStyles';
        style.textContent = `
            #mobilePlaylistCollapseBtn:hover {
                background: rgba(255,255,255,0.2) !important;
                border-color: rgba(255,255,255,0.5) !important;
                transform: translateY(-1px);
                box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            }
            
            #mobilePlaylistCollapseBtn:active {
                transform: scale(0.95);
            }
            
            #mobilePlaylistCollapseIcon {
                transition: transform 0.3s ease;
            }
            
            /* Анимация для мобильного виджета */
            .mobile-playlist-content {
                transition: all 0.3s ease;
            }
            
            /* Адаптивность - показываем только на мобильных */
            @media (min-width: 992px) {
                #mobilePlaylistCollapseBtn {
                    display: none !important;
                }
            }
        `;
        
        document.head.appendChild(style);
        console.log('🎨 CSS стили добавлены');
    }
    
    // Основная функция инициализации
    function init() {
        console.log('🔍 Поиск мобильного виджета плейлистов...');
        
        const widget = findMobilePlaylistWidget();
        
        if (widget) {
            console.log('✅ Мобильный виджет плейлистов найден!');
            addStyles();
            
            if (addCollapseButtonToWidget(widget)) {
                console.log('🎉 Кнопка сворачивания успешно добавлена!');
            }
        } else {
            console.log('❌ Мобильный виджет плейлистов не найден на странице');
            
            // Попробуем еще раз через 2 секунды (виджет может загружаться динамически)
            setTimeout(() => {
                console.log('🔄 Повторная попытка поиска мобильного виджета...');
                const retryWidget = findMobilePlaylistWidget();
                if (retryWidget) {
                    addStyles();
                    if (addCollapseButtonToWidget(retryWidget)) {
                        console.log('🎉 Кнопка сворачивания добавлена (повторная попытка)!');
                    }
                } else {
                    console.log('❌ Мобильный виджет плейлистов так и не найден');
                }
            }, 2000);
        }
    }
    
    // Наблюдатель за изменениями DOM для динамически создаваемых элементов
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        // Проверяем, добавлен ли виджет плейлистов
                        if (node.textContent && node.textContent.includes('🎵 Плейлисты') ||
                            node.querySelector && node.querySelector('.bi-bookmark, [style*="background-color: rgb(231, 76, 60)"]')) {
                            console.log('📱 Обнаружен новый мобильный виджет плейлистов');
                            setTimeout(init, 100); // Небольшая задержка для полной загрузки
                        }
                    }
                });
            }
        });
    });
    
    // Запускаем наблюдатель
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // Запускаем инициализацию когда страница готова
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Экспортируем функции для отладки
    window.mobilePlaylistCollapse = {
        init,
        findWidget: findMobilePlaylistWidget,
        toggle: toggleMobilePlaylistContent,
        test: function() {
            console.log('🧪 ТЕСТ МОБИЛЬНОГО СВОРАЧИВАНИЯ:');
            const widget = findMobilePlaylistWidget();
            console.log('Виджет найден:', !!widget);
            if (widget) {
                console.log('Элемент виджета:', widget);
                console.log('Текст виджета:', widget.textContent.substring(0, 100) + '...');
            }
            const button = document.getElementById('mobilePlaylistCollapseBtn');
            console.log('Кнопка сворачивания найдена:', !!button);
        }
    };
    
    console.log('✅ Система мобильного сворачивания плейлистов готова!');
    
})();

// Добавляем тестовую кнопку для отладки (только в dev режиме)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    setTimeout(() => {
        const testBtn = document.createElement('button');
        testBtn.textContent = '📱 ТЕСТ МОБИЛЬНОГО СВОРАЧИВАНИЯ';
        testBtn.style.cssText = `
            position: fixed;
            bottom: 10px;
            left: 10px;
            z-index: 99999;
            padding: 8px 12px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        `;
        
        testBtn.onclick = () => {
            if (window.mobilePlaylistCollapse) {
                window.mobilePlaylistCollapse.test();
            }
        };
        
        document.body.appendChild(testBtn);
    }, 3000);
}
