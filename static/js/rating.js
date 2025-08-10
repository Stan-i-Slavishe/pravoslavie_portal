// Простая логика рейтинга звёзд - слева направо
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌟 Rating script loaded');
    
    const ratingInputs = document.querySelectorAll('.rating-input');
    console.log('Found rating inputs:', ratingInputs.length);
    
    ratingInputs.forEach(function(ratingContainer) {
        const stars = ratingContainer.querySelectorAll('.star-label');
        const inputs = ratingContainer.querySelectorAll('input[type="radio"]');
        
        console.log('Stars:', stars.length, 'Inputs:', inputs.length);
        
        // Обработчик наведения
        stars.forEach(function(star, index) {
            star.addEventListener('mouseenter', function() {
                // Подсвечиваем звёзды слева до текущей включительно
                const rating = index + 1;
                console.log('Hover on star', index + 1);
                highlightStars(stars, rating);
            });
            
            // Обработчик клика
            star.addEventListener('click', function() {
                const rating = index + 1;
                const targetInput = ratingContainer.querySelector(`input[value="${rating}"]`);
                console.log('Clicked star', rating, 'target input:', targetInput);
                
                if (targetInput) {
                    // Снимаем выбор с других
                    inputs.forEach(inp => inp.checked = false);
                    // Устанавливаем выбор
                    targetInput.checked = true;
                    console.log('Set rating to:', rating);
                    highlightStars(stars, rating);
                }
            });
        });
        
        // Обработчик ухода мыши
        ratingContainer.addEventListener('mouseleave', function() {
            const checkedInput = ratingContainer.querySelector('input:checked');
            if (checkedInput) {
                const rating = parseInt(checkedInput.value);
                console.log('Mouse leave, restoring rating:', rating);
                highlightStars(stars, rating);
            } else {
                console.log('Mouse leave, no rating selected');
                clearStars(stars);
            }
        });
        
        // Инициализация при загрузке (если есть выбранное значение)
        const checkedInput = ratingContainer.querySelector('input:checked');
        if (checkedInput) {
            const rating = parseInt(checkedInput.value);
            console.log('Initial rating found:', rating);
            highlightStars(stars, rating);
        }
    });
    
    function highlightStars(stars, rating) {
        console.log('Highlighting', rating, 'stars out of', stars.length);
        clearStars(stars);
        
        // Подсвечиваем первые rating звёзд (включая выбранную)
        for (let i = 0; i < rating && i < stars.length; i++) {
            stars[i].classList.add('active');
            stars[i].style.setProperty('color', '#ffc107', 'important');
            console.log('Star', i + 1, 'highlighted');
        }
        
        // Убеждаемся что остальные звёзды серые
        for (let i = rating; i < stars.length; i++) {
            stars[i].classList.remove('active');
            stars[i].style.setProperty('color', '#ddd', 'important');
            console.log('Star', i + 1, 'dimmed');
        }
    }
    
    function clearStars(stars) {
        stars.forEach(function(star, index) {
            star.classList.remove('active');
            star.style.setProperty('color', '#ddd', 'important');
        });
        console.log('All stars cleared');
    }
});
