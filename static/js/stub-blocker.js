/* 
 * ПОЛНАЯ БЛОКИРОВКА АНАЛИТИКИ И ЗАГЛУШЕК
 * Этот файл перехватывает любые попытки показа модальных окон
 */

// Полная блокировка всех модальных окон с заглушками
window.addEventListener('DOMContentLoaded', function() {
    console.log('🚫 Блокировщик заглушек активирован');
    
    // Блокируем все потенциальные функции заглушек
    window.showComingSoonModal = function() {
        console.log('🚫 showComingSoonModal заблокирована');
        return false;
    };
    
    window.trackPurchaseIntent = function() {
        console.log('🚫 trackPurchaseIntent заблокирована');
        return false;
    };
    
    // Блокируем создание модальных окон с определенным содержимым
    const originalCreateElement = document.createElement;
    document.createElement = function(tagName) {
        const element = originalCreateElement.call(document, tagName);
        
        if (tagName.toLowerCase() === 'div') {
            const originalSetClassName = element.setAttribute.bind(element);
            element.setAttribute = function(name, value) {
                // Блокируем создание модальных окон заглушек
                if (name === 'class' && value && (
                    value.includes('purchase-intent-modal') ||
                    value.includes('coming-soon-modal') ||
                    value.includes('modal-overlay')
                )) {
                    console.log('🚫 Заблокировано создание модального окна заглушки');
                    return;
                }
                return originalSetClassName(name, value);
            };
        }
        
        return element;
    };
    
    // Блокируем appendChild для модальных окон
    const originalAppendChild = document.body.appendChild;
    document.body.appendChild = function(child) {
        if (child && child.className && (
            child.className.includes('purchase-intent-modal') ||
            child.className.includes('coming-soon-modal') ||
            child.innerHTML && child.innerHTML.includes('Подтвердите действие')
        )) {
            console.log('🚫 Заблокировано добавление модального окна заглушки');
            return child;
        }
        return originalAppendChild.call(this, child);
    };
    
    // Удаляем существующие заглушки
    function removeStubModals() {
        const stubSelectors = [
            '.purchase-intent-modal',
            '.coming-soon-modal',
            '[class*="modal"][class*="intent"]',
            'div[style*="position: fixed"]:has-text("Подтвердите действие")'
        ];
        
        stubSelectors.forEach(selector => {
            try {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    console.log('🗑️ Удален элемент заглушки:', el);
                    el.remove();
                });
            } catch (e) {
                // Игнорируем ошибки селекторов
            }
        });
        
        // Дополнительная проверка по содержимому
        const allModals = document.querySelectorAll('[class*="modal"], [style*="position: fixed"]');
        allModals.forEach(modal => {
            if (modal.textContent && (
                modal.textContent.includes('Подтвердите действие') ||
                modal.textContent.includes('Платежная система скоро') ||
                modal.textContent.includes('записали ваш интерес')
            )) {
                console.log('🗑️ Удалена заглушка по содержимому:', modal);
                modal.remove();
            }
        });
    }
    
    // Запускаем проверку периодически
    setInterval(removeStubModals, 500);
    
    // Блокируем события клика, которые могут вызывать заглушки
    document.addEventListener('click', function(e) {
        const button = e.target.closest('button, a');
        if (button && button.hasAttribute && (
            button.hasAttribute('data-purchase-intent') ||
            button.hasAttribute('data-intent') ||
            button.hasAttribute('data-stub')
        )) {
            console.log('🚫 Заблокирован клик по кнопке заглушки');
            e.stopPropagation();
            e.stopImmediatePropagation();
        }
    }, true); // Используем capture фазу
});

// Блокируем fetch запросы к аналитике
const originalFetch = window.fetch;
window.fetch = function(url, options) {
    if (typeof url === 'string' && (
        url.includes('/analytics/') ||
        url.includes('track-purchase-intent') ||
        url.includes('subscribe-notifications')
    )) {
        console.log('🚫 Заблокирован запрос к аналитике:', url);
        return Promise.resolve(new Response('{"blocked": true}', {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        }));
    }
    return originalFetch.apply(this, arguments);
};

console.log('✅ Блокировщик заглушек полностью активирован');
