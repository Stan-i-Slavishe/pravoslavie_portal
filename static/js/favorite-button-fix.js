// Исправление цвета кнопки избранного при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    
    // Функция принудительного исправления цветов кнопки избранного
    function fixFavoriteButtonColors() {
        const favoriteButtons = document.querySelectorAll('.btn-favorite');
        
        favoriteButtons.forEach(button => {
            const isActive = button.classList.contains('active');
            
            // Убираем все встроенные стили с желтым цветом
            const style = button.getAttribute('style') || '';
            let newStyle = style;
            
            // Заменяем желтые цвета на золотистые
            newStyle = newStyle.replace(/#ffc107/g, '#D4AF37');
            newStyle = newStyle.replace(/#e0a800/g, '#b8941f');
            
            if (isActive) {
                // Для активной кнопки - золотистый градиент
                newStyle = 'background: linear-gradient(135deg, #D4AF37, #b8941f) !important; border: 2px solid #D4AF37 !important; color: white !important; padding: 10px 20px; border-radius: 8px; font-weight: 500; transition: all 0.3s ease; display: inline-flex; align-items: center; gap: 8px; cursor: pointer; flex: 1; justify-content: center;';
            } else {
                // Для неактивной кнопки - прозрачный фон с золотистой рамкой
                newStyle = 'background: transparent !important; border: 2px solid #D4AF37 !important; color: #D4AF37 !important; padding: 10px 20px; border-radius: 8px; font-weight: 500; transition: all 0.3s ease; display: inline-flex; align-items: center; gap: 8px; cursor: pointer; flex: 1; justify-content: center;';
            }
            
            button.setAttribute('style', newStyle);
            
            // Обновляем обработчики наведения
            button.onmouseover = function() {
                this.style.background = 'linear-gradient(135deg, #D4AF37, #b8941f)';
                this.style.color = 'white';
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 4px 12px rgba(212, 175, 55, 0.3)';
            };
            
            button.onmouseout = function() {
                if (this.classList.contains('active')) {
                    this.style.background = 'linear-gradient(135deg, #D4AF37, #b8941f)';
                    this.style.color = 'white';
                } else {
                    this.style.background = 'transparent';
                    this.style.color = '#D4AF37';
                }
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            };
        });
        
        console.log('✅ Цвета кнопок избранного исправлены на золотистые');
    }
    
    // Исправляем цвета сразу при загрузке
    fixFavoriteButtonColors();
    
    // Исправляем цвета через небольшой промежуток времени (на случай позднего рендеринга)
    setTimeout(fixFavoriteButtonColors, 500);
    setTimeout(fixFavoriteButtonColors, 1000);
    
    // Следим за изменениями DOM
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                // Проверяем, добавились ли новые кнопки избранного
                const addedNodes = Array.from(mutation.addedNodes);
                const hasFavoriteButton = addedNodes.some(node => {
                    return node.nodeType === 1 && (
                        node.classList && node.classList.contains('btn-favorite') ||
                        node.querySelector && node.querySelector('.btn-favorite')
                    );
                });
                
                if (hasFavoriteButton) {
                    setTimeout(fixFavoriteButtonColors, 100);
                }
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
