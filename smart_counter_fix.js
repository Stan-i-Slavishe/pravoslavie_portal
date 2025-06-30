// Умное обновление счетчика символов - ИСПРАВЛЕНИЕ ДЛЯ МОБИЛЬНЫХ
// Заменить функцию updateCharCounter() в comments_section.html

function updateCharCounter() {
    const length = commentText.value.length;
    charCounter.textContent = length;
    
    // Получаем контейнер счетчика
    const counterWrapper = charCounter.parentElement;
    
    // Умная логика - показываем только когда приближаемся к лимиту
    if (length > 850) {
        counterWrapper.style.display = 'block';
        
        // Сброс классов
        counterWrapper.classList.remove('warning', 'danger');
        
        // Добавляем классы в зависимости от количества символов
        if (length > 950) {
            counterWrapper.classList.add('danger');
        } else if (length > 900) {
            counterWrapper.classList.add('warning');
        }
    } else {
        // Скрываем счетчик когда символов мало
        counterWrapper.style.display = 'none';
    }
}

// Дополнительно: функция для форм ответов
function updateReplyCounter(replyId) {
    const replyTextarea = document.getElementById(`reply-text-${replyId}`);
    const counterWrapper = document.getElementById(`reply-counter-${replyId}`);
    const counter = counterWrapper.querySelector('.reply-char-count');
    
    const length = replyTextarea.value.length;
    counter.textContent = length;
    
    if (length > 850) {
        counterWrapper.style.display = 'block';
        counterWrapper.classList.remove('warning', 'danger');
        
        if (length > 950) {
            counterWrapper.classList.add('danger');
        } else if (length > 900) {
            counterWrapper.classList.add('warning');
        }
    } else {
        counterWrapper.style.display = 'none';
    }
}

// HTML изменения для контейнера счетчика:
// Заменить:
// <div class="form-text">
//     <span id="char-counter">0</span>/1000 символов
// </div>
//
// На:
// <div class="form-text smart-counter" id="char-counter-wrapper" style="display: none;">
//     <span id="char-counter">0</span>/1000 символов
// </div>

console.log('✅ Умный счетчик символов готов к использованию!');
