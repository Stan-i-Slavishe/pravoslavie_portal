// Простое тестирование добавления кнопки "Все плейлисты"
console.log('🚀 Тестовый скрипт для кнопки "Все плейлисты" загружен');

setTimeout(function() {
    console.log('📱 Ищем мобильный виджет плейлистов...');
    
    const mobileList = document.getElementById('mobilePlaylistList');
    if (mobileList) {
        console.log('✅ Виджет найден! Содержимое:', mobileList.innerHTML);
        
        // Добавляем кнопку если её еще нет
        if (!mobileList.querySelector('.mobile-all-playlists-btn')) {
            const buttonHtml = `
                <div class="text-center mt-2 pt-1" style="border-top: 1px solid rgba(0,0,0,0.1); animation: fadeIn 0.5s ease;">
                    <a href="/stories/playlists/" 
                       class="btn btn-sm btn-outline-primary text-decoration-none mobile-all-playlists-btn"
                       style="font-size: 0.7rem; padding: 2px 8px; border-radius: 12px; 
                              color: #0d6efd; border-color: #0d6efd; background: rgba(13, 110, 253, 0.05);
                              transition: all 0.2s ease; font-weight: 500; display: inline-flex; 
                              align-items: center; gap: 4px;">
                        <i class="bi bi-collection me-1" style="font-size: 0.7rem;"></i>
                        Все плейлисты (1)
                    </a>
                </div>
            `;
            
            mobileList.insertAdjacentHTML('beforeend', buttonHtml);
            console.log('🎉 Кнопка "Все плейлисты" успешно добавлена!');
        }
    } else {
        console.log('❌ Мобильный виджет плейлистов не найден');
        console.log('📋 Все элементы на странице:', document.querySelectorAll('[id*="mobile"]'));
    }
}, 2000);