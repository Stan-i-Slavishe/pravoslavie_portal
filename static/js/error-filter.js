/**
 * 🛡️ Система фильтрации ошибок браузера
 * Убирает ошибки от расширений браузера и рекламных блокировщиков
 */

(function() {
    'use strict';
    
    console.log('🛡️ Инициализация системы фильтрации ошибок...');
    
    // Список паттернов для игнорирования
    const IGNORE_PATTERNS = [
        'googleads',
        'doubleclick', 
        'ERR_BLOCKED_BY_CLIENT',
        'googleleads',
        'pagead/id',
        'polyfill',
        'Extension context invalidated',
        'content-script-start',
        'content-script-end',
        'chrome-extension://',
        'moz-extension://',
        'safari-extension://',
        'adnxs.com',
        'adsystem.com',
        'googlesyndication',
        'adsafeprotected'
    ];
    
    function shouldIgnoreError(message, source = '') {
        const text = `${message} ${source}`.toLowerCase();
        return IGNORE_PATTERNS.some(pattern => text.includes(pattern.toLowerCase()));
    }
    
    // 1. Фильтрация console.error
    const originalConsoleError = console.error;
    console.error = function(...args) {
        const message = args.join(' ');
        if (shouldIgnoreError(message)) {
            return; // Игнорируем
        }
        originalConsoleError.apply(console, args);
    };
    
    // 2. Фильтрация console.warn (тоже может быть много спама)
    const originalConsoleWarn = console.warn;
    console.warn = function(...args) {
        const message = args.join(' ');
        if (shouldIgnoreError(message)) {
            return; // Игнорируем
        }
        originalConsoleWarn.apply(console, args);
    };
    
    // 3. Обработчик window.onerror
    const originalWindowError = window.onerror;
    window.onerror = function(message, source, lineno, colno, error) {
        if (shouldIgnoreError(message, source)) {
            return true; // Предотвращаем дальнейшую обработку
        }
        
        if (originalWindowError) {
            return originalWindowError.call(this, message, source, lineno, colno, error);
        }
        return false;
    };
    
    // 4. Обработчик unhandledrejection для Promise ошибок
    window.addEventListener('unhandledrejection', function(event) {
        const message = event.reason ? event.reason.toString() : '';
        const stack = event.reason && event.reason.stack ? event.reason.stack : '';
        
        if (shouldIgnoreError(message, stack)) {
            event.preventDefault();
            return;
        }
    });
    
    // 5. Обработчик error events
    window.addEventListener('error', function(event) {
        let source = '';
        let message = '';
        
        if (event.target && event.target.src) {
            source = event.target.src;
        }
        
        if (event.error && event.error.message) {
            message = event.error.message;
        } else if (event.message) {
            message = event.message;
        }
        
        if (shouldIgnoreError(message, source)) {
            event.preventDefault();
            event.stopPropagation();
            return true;
        }
    }, true);
    
    // 6. Фильтрация addEventListener для error events
    const originalAddEventListener = EventTarget.prototype.addEventListener;
    EventTarget.prototype.addEventListener = function(type, listener, options) {
        if (type === 'error' && typeof listener === 'function') {
            const wrappedListener = function(event) {
                let source = '';
                let message = '';
                
                if (event.target && event.target.src) {
                    source = event.target.src;
                }
                
                if (event.error && event.error.message) {
                    message = event.error.message;
                } else if (event.message) {
                    message = event.message;
                }
                
                if (shouldIgnoreError(message, source)) {
                    event.preventDefault();
                    event.stopPropagation();
                    return true;
                }
                
                return listener.call(this, event);
            };
            
            return originalAddEventListener.call(this, type, wrappedListener, options);
        }
        
        return originalAddEventListener.call(this, type, listener, options);
    };
    
    // 7. Подавление ошибок в iframe (для рекламы)
    function suppressIframeErrors() {
        const iframes = document.querySelectorAll('iframe');
        iframes.forEach(iframe => {
            try {
                if (iframe.src && shouldIgnoreError('', iframe.src)) {
                    iframe.style.display = 'none';
                }
            } catch (e) {
                // Cross-origin iframe, игнорируем
            }
        });
    }
    
    // Запускаем подавление ошибок iframe при загрузке и при изменениях DOM
    document.addEventListener('DOMContentLoaded', suppressIframeErrors);
    
    // MutationObserver для новых iframe
    if (window.MutationObserver) {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach(function(node) {
                        if (node.nodeType === 1 && node.tagName === 'IFRAME') {
                            try {
                                if (node.src && shouldIgnoreError('', node.src)) {
                                    node.style.display = 'none';
                                }
                            } catch (e) {
                                // Игнорируем ошибки доступа
                            }
                        }
                    });
                }
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    console.log('✅ Система фильтрации ошибок активирована');
    console.log(`🛡️ Игнорируются паттерны: ${IGNORE_PATTERNS.slice(0, 5).join(', ')}...`);
    
})();
