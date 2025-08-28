// ПРОСТОЕ И НАДЕЖНОЕ ДОБАВЛЕНИЕ КНОПКИ СВОРАЧИВАНИЯ К ВИДЖЕТУ ПЛЕЙЛИСТОВ
(function() {
    'use strict';
    
    console.log('🔧 Запуск простого исправления для добавления кнопки сворачивания...');
    
    // Функция для поиска виджета плейлистов (упрощенная)
    function findPlaylistWidget() {
        console.log('🔍 Поиск виджета плейлистов...');
        
        // Ищем по тексту "Плейлисты" в заголовке
        const elements = document.querySelectorAll('*');
        for (const element of elements) {
            const text = element.textContent || '';
            if (text.includes('Плейлисты') && !text.includes('Посмотреть') && text.length < 50) {
                // Найден заголовок с "Плейлисты"
                const widget = element.closest('.card, div[style], .widget, [class*="playlist"]') || 
                              element.parentElement?.parentElement;
                if (widget && widget.querySelector('.bi-bookmark, .bi-plus, button')) {
                    console.log('✅ Найден виджет плейлистов:', widget);
                    return widget;
                }
            }
        }
        
        // Альтернативный поиск - ищем по серому фону и содержимому
        const grayElements = document.querySelectorAll('[style*="background"], .card, .bg-light');
        for (const element of grayElements) {
            if (element.textContent && 
                element.textContent.includes('Плейлисты') && 
                element.querySelector('button, .bi-bookmark')) {
                console.log('✅ Найден виджет плейлистов (альтернативный поиск):', element);
                return element;
            }
        }
        
        return null;
    }
    
    // Создание простой кнопки сворачивания
    function createCollapseButton() {
        const button = document.createElement('button');
        button.className = 'btn btn-sm btn-outline-secondary ms-2';
        button.style.cssText = `
            padding: 6px 10px;
            border-radius: 6px;
            border: 1px solid #6c757d;
            background: white;
            color: #6c757d;
            transition: all 0.2s ease;
            min-width: 36px;
        `;
        button.title = 'Свернуть/развернуть плейлисты';
        button.id = 'simplePlaylistCollapseBtn';
        
        const icon = document.createElement('i');
        icon.className = 'bi bi-chevron-down';
        icon.id = 'simplePlaylistCollapseIcon';
        icon.style.cssText = 'font-size: 0.9rem; transition: transform 0.3s ease;';
        
        button.appendChild(icon);
        return button;
    }
    
    // Добавление кнопки к виджету
    function addCollapseButton(widget) {
        // Проверяем, не добавлена ли уже кнопка
        if (document.getElementById('simplePlaylistCollapseBtn')) {
            console.log('⚠️ Кнопка уже существует');
            return false;
        }
        
        // Ищем заголовок с "Плейлисты"
        const titleElements = widget.querySelectorAll('*');
        let titleElement = null;
        
        for (const el of titleElements) {
            if (el.textContent && 
                el.textContent.includes('Плейлисты') && 
                el.textContent.length < 50 &&
                !el.textContent.includes('Посмотреть')) {
                titleElement = el;
                break;
            }
        }
        
        if (titleElement) {
            // Находим родительский контейнер заголовка
            const headerContainer = titleElement.parentElement;
            
            // Делаем контейнер flex для размещения кнопки
            headerContainer.style.display = 'flex';
            headerContainer.style.justifyContent = 'space-between';
            headerContainer.style.alignItems = 'center';
            
            // Создаем и добавляем кнопку
            const collapseButton = createCollapseButton();
            
            // Создаем контейнер для кнопки справа
            const buttonContainer = document.createElement('div');
            buttonContainer.appendChild(collapseButton);
            
            headerContainer.appendChild(buttonContainer);
            
            // Добавляем обработчик события
            collapseButton.addEventListener('click', () => toggleContent(widget));
            
            console.log('✅ Кнопка сворачивания добавлена!');
            return true;
        }
        
        return false;
    }
    
    // Функция сворачивания/разворачивания
    function toggleContent(widget) {
        const icon = document.getElementById('simplePlaylistCollapseIcon');
        const button = document.getElementById('simplePlaylistCollapseBtn');
        
        // Находим все элементы кроме заголовка
        const allChildren = Array.from(widget.children);
        const titleContainer = allChildren.find(child => 
            child.textContent && child.textContent.includes('Плейлисты')
        );
        
        const contentElements = allChildren.filter(child => child !== titleContainer);
        
        if (contentElements.length === 0) {
            console.log('❌ Контент для сворачивания не найден');
            return;
        }
        
        // Проверяем текущее состояние
        const isCollapsed = contentElements[0].style.display === 'none';
        
        if (isCollapsed) {
            // Разворачиваем
            contentElements.forEach(el => {
                el.style.display = '';
                el.style.opacity = '0';
                el.style.transition = 'opacity 0.3s ease';
                setTimeout(() => el.style.opacity = '1', 10);
            });
            
            icon.classList.remove('bi-chevron-up');
            icon.classList.add('bi-chevron-down');
            button.title = 'Свернуть плейлисты';
            
            console.log('📂 Плейлисты развернуты');
        } else {
            // Сворачиваем
            contentElements.forEach(el => {
                el.style.transition = 'opacity 0.3s ease';
                el.style.opacity = '0';
                setTimeout(() => el.style.display = 'none', 300);
            });
            
            icon.classList.remove('bi-chevron-down');
            icon.classList.add('bi-chevron-up');
            button.title = 'Развернуть плейлисты';
            
            console.log('📁 Плейлисты свернуты');
        }
        
        // Анимация кнопки
        button.style.transform = 'scale(0.95)';
        setTimeout(() => button.style.transform = 'scale(1)', 150);
    }
    
    // Основная функция
    function init() {
        const widget = findPlaylistWidget();
        
        if (widget) {
            console.log('✅ Виджет плейлистов найден!');
            if (addCollapseButton(widget)) {
                console.log('🎉 Кнопка успешно добавлена!');
            } else {
                console.log('❌ Не удалось добавить кнопку');
            }
        } else {
            console.log('❌ Виджет плейлистов не найден');
            
            // Повторяем поиск через 3 секунды
            setTimeout(() => {
                console.log('🔄 Повторный поиск виджета...');
                const retryWidget = findPlaylistWidget();
                if (retryWidget && addCollapseButton(retryWidget)) {
                    console.log('🎉 Кнопка добавлена при повторном поиске!');
                }
            }, 3000);
        }
    }
    
    // Добавляем CSS стили
    const style = document.createElement('style');
    style.textContent = `
        #simplePlaylistCollapseBtn:hover {
            background-color: #6c757d !important;
            color: white !important;
            transform: translateY(-1px);
        }
        
        #simplePlaylistCollapseBtn:active {
            transform: scale(0.95);
        }
        
        @media (min-width: 992px) {
            #simplePlaylistCollapseBtn {
                display: none !important;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Запускаем инициализацию
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        setTimeout(init, 1000); // Задержка для полной загрузки
    }
    
    // Наблюдатель за изменениями DOM
    const observer = new MutationObserver(() => {
        if (!document.getElementById('simplePlaylistCollapseBtn')) {
            setTimeout(init, 500);
        }
    });
    
    observer.observe(document.body, { childList: true, subtree: true });
    
    // Функции для отладки
    window.simplePlaylistCollapse = {
        init,
        findWidget: findPlaylistWidget,
        test: function() {
            console.log('🧪 ПРОСТОЙ ТЕСТ:');
            const widget = findPlaylistWidget();
            console.log('Виджет найден:', !!widget);
            if (widget) {
                console.log('Элемент:', widget);
                console.log('Содержимое:', widget.innerHTML.substring(0, 200) + '...');
            }
            const btn = document.getElementById('simplePlaylistCollapseBtn');
            console.log('Кнопка найдена:', !!btn);
        }
    };
    
    console.log('✅ Простая система сворачивания готова!');
    
})();

// Добавляем тестовую кнопку (только на localhost)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    setTimeout(() => {
        const testBtn = document.createElement('button');
        testBtn.textContent = '🔧 ПРОСТОЙ ТЕСТ';
        testBtn.style.cssText = `
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 99999;
            padding: 8px 12px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
        `;
        
        testBtn.onclick = () => {
            if (window.simplePlaylistCollapse) {
                window.simplePlaylistCollapse.test();
            }
        };
        
        document.body.appendChild(testBtn);
    }, 2000);
}
