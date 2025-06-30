// Диагностика умного счетчика - выполните в консоли браузера
// Откройте DevTools (F12) → Console и выполните этот код:

console.log('🔍 Диагностика умного счетчика...');

// Проверяем элементы
const commentText = document.getElementById('comment-text');
const charCounter = document.getElementById('char-counter');
const counterWrapper = document.getElementById('char-counter-wrapper');

console.log('📝 Поле комментария:', commentText);
console.log('🔢 Счетчик:', charCounter);
console.log('📦 Контейнер счетчика:', counterWrapper);

if (commentText && charCounter && counterWrapper) {
    console.log('✅ Все элементы найдены');
    
    // Проверяем текущую длину
    const currentLength = commentText.value.length;
    console.log('📏 Текущая длина:', currentLength);
    console.log('👁 Видимость контейнера:', counterWrapper.style.display);
    console.log('🎨 Классы контейнера:', counterWrapper.className);
    
    // Принудительно показываем счетчик для теста
    if (currentLength > 0) {
        console.log('🔧 Принудительно показываем счетчик...');
        counterWrapper.style.display = 'block';
        charCounter.textContent = currentLength;
        
        if (currentLength > 950) {
            counterWrapper.classList.add('danger');
            console.log('🔴 Добавлен класс danger');
        } else if (currentLength > 900) {
            counterWrapper.classList.add('warning');
            console.log('🟡 Добавлен класс warning');
        }
    }
    
    // Тестируем функцию updateCharCounter
    if (typeof updateCharCounter === 'function') {
        console.log('🔄 Вызываем updateCharCounter...');
        updateCharCounter();
    } else {
        console.log('❌ Функция updateCharCounter не найдена');
    }
    
} else {
    console.log('❌ Некоторые элементы не найдены:');
    console.log('  - commentText:', !!commentText);
    console.log('  - charCounter:', !!charCounter);
    console.log('  - counterWrapper:', !!counterWrapper);
}

console.log('🏁 Диагностика завершена');
