// Тест системы мобильной обратной связи
console.log('🔍 Проверка системы мобильной обратной связи...');

// Проверяем CSS
const cssLink = document.querySelector('link[href*="mobile-feedback.css"]');
console.log('📄 CSS загружен:', !!cssLink);

// Проверяем JavaScript
const feedbackSystem = window.MobileFeedbackSystem;
console.log('⚡ JavaScript класс:', !!feedbackSystem);

// Проверяем элементы
setTimeout(() => {
    const overlay = document.getElementById('feedbackOverlay');
    const textarea = document.getElementById('feedbackText');
    
    console.log('🖼️ Overlay создан:', !!overlay);
    console.log('📝 Textarea создан:', !!textarea);
    
    if (textarea) {
        console.log('📐 Textarea стили:', {
            display: getComputedStyle(textarea).display,
            visibility: getComputedStyle(textarea).visibility,
            height: getComputedStyle(textarea).height
        });
    }
}, 1000);