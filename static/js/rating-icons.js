// Альтернативный подход - меняем иконки вместо цвета
document.addEventListener('DOMContentLoaded', function() {
    console.log('🌟 Rating script loaded (icon approach)');
    
    const ratingInputs = document.querySelectorAll('.rating-input');
    console.log('Found rating inputs:', ratingInputs.length);
    
    ratingInputs.forEach(function(ratingContainer) {
        const stars = ratingContainer.querySelectorAll('.star-label');
        const inputs = ratingContainer.querySelectorAll('input[type="radio"]');
        
        console.log('Stars:', stars.length, 'Inputs:', inputs.length);
        
        // Обработчик наведения
        stars.forEach(function(star, index) {
            star.addEventListener('mouseenter', function() {
                const rating = index + 1;
                console.log('Hover on star', rating);
                highlightStars(stars, rating);
            });
            
            // Обработчик клика
            star.addEventListener('click', function() {
                const rating = index + 1;
                const targetInput = ratingContainer.querySelector(`input[value="${rating}"]`);
                console.log('Clicked star', rating, 'target input:', targetInput);
                
                if (targetInput) {
                    inputs.forEach(inp => inp.checked = false);
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
        
        // Инициализация при загрузке
        const checkedInput = ratingContainer.querySelector('input:checked');
        if (checkedInput) {
            const rating = parseInt(checkedInput.value);
            console.log('Initial rating found:', rating);
            highlightStars(stars, rating);
        }
    });
    
    function highlightStars(stars, rating) {
        console.log('Highlighting', rating, 'stars with filled icons');
        clearStars(stars);
        
        // Заменяем иконки на заполненные для выбранных звёзд
        for (let i = 0; i < rating && i < stars.length; i++) {
            const icon = stars[i].querySelector('i');
            if (icon) {
                icon.className = 'bi bi-star-fill';
                stars[i].style.setProperty('color', '#ffc107', 'important');
                console.log('Star', i + 1, 'filled');
            }
        }
        
        // Пустые иконки для невыбранных звёзд
        for (let i = rating; i < stars.length; i++) {
            const icon = stars[i].querySelector('i');
            if (icon) {
                icon.className = 'bi bi-star';
                stars[i].style.setProperty('color', '#ddd', 'important');
                console.log('Star', i + 1, 'empty');
            }
        }
    }
    
    function clearStars(stars) {
        stars.forEach(function(star, index) {
            const icon = star.querySelector('i');
            if (icon) {
                icon.className = 'bi bi-star';
                star.style.setProperty('color', '#ddd', 'important');
            }
        });
        console.log('All stars cleared with empty icons');
    }
});
