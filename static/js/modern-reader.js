// Современный Reader для PDF книг
class ModernReader {
    constructor() {
        this.currentPage = 1;
        this.totalPages = 0;
        this.isFullscreen = false;
        this.pdfDoc = null;
        this.userScale = 1.0; // Пользовательский масштаб (множитель)
        this.isControlsVisible = false;
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.scaleTimeout = null; // Для оптимизации перерисовки при изменении масштаба
        this.isRendering = false; // Флаг для предотвращения одновременного рендеринга
        
        this.init();
    }

    async init() {
        try {
            // Получаем PDF URL из атрибута data
            const bookContainer = document.getElementById('book-container');
            if (!bookContainer) {
                console.error('Book container not found');
                return;
            }
            
            const pdfUrl = bookContainer.dataset.pdfUrl;
            console.log('PDF URL from dataset:', pdfUrl);
            
            if (!pdfUrl) {
                this.showError('Не указан путь к PDF файлу');
                return;
            }
            
            // Настраиваем обработчики событий
            this.setupEventListeners();
            this.setupOrientationHandlers(); // Новые обработчики
        this.setupTitleClick(); // Обработчик клика по заголовку
            
            // Псевдо-полноэкранный режим
            this.enterFullscreen();
            
            // Показываем контролы сразу для тестирования
            setTimeout(() => {
                this.toggleControls();
            }, 500);
            
            // Ограничиваем название книги для десктопа
            this.limitTitleForDesktop();
            
            // Загружаем PDF
            await this.loadPDF(pdfUrl);
            
        } catch (error) {
            console.error('Initialization error:', error);
            this.showError(`Ошибка инициализации: ${error.message}`);
        }
    }

    async loadPDF(url) {
        try {
            console.log('Loading PDF from:', url);
            
            // Показываем спиннер
            const spinner = document.querySelector('.loading-spinner');
            if (spinner) spinner.style.display = 'flex';
            
            // Загружаем PDF с помощью PDF.js
            const loadingTask = pdfjsLib.getDocument({
                url: url,
                cMapUrl: 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/cmaps/',
                cMapPacked: true
            });
            
            this.pdfDoc = await loadingTask.promise;
            this.totalPages = this.pdfDoc.numPages;
            
            console.log('PDF loaded successfully. Pages:', this.totalPages);
            
            // Обновляем UI
            document.getElementById('page-info').textContent = `${this.currentPage} из ${this.totalPages}`;
            
            // Настраиваем слайдер
            const slider = document.getElementById('page-slider');
            slider.max = this.totalPages;
            slider.value = this.currentPage;
            
            // Скрываем спиннер
            if (spinner) spinner.style.display = 'none';
            
            // Рендерим первую страницу
            await this.renderPage(this.currentPage);
            
            // Загружаем сохранённые настройки
            this.loadSavedSettings();
            
        } catch (error) {
            console.error('Ошибка загрузки PDF:', error);
            this.showError(`Не удалось загрузить книгу: ${error.message}`);
        }
    }

    async renderPage(pageNum) {
        if (!this.pdfDoc) return;
        
        // Предотвращаем одновременный рендеринг
        if (this.isRendering) {
            console.log('⚠️ Рендеринг уже в процессе, пропускаем...');
            return;
        }
        
        this.isRendering = true;
        
        try {
            const page = await this.pdfDoc.getPage(pageNum);
            const canvas = document.getElementById('pdf-canvas');
            const context = canvas.getContext('2d');
            const container = document.querySelector('.book-container');
            
            // Получаем размеры контейнера
            const containerWidth = container.clientWidth;
            const containerHeight = container.clientHeight;
            
            // Рассчитываем базовый масштаб под размер экрана
            const viewport = page.getViewport({ scale: 1 });
            const scaleX = containerWidth / viewport.width;
            const scaleY = containerHeight / viewport.height;
            const baseScale = Math.min(scaleX, scaleY) * 0.9; // 0.9 для отступов
            
            // Применяем пользовательский масштаб поверх базового
            const finalScale = baseScale * this.userScale;
            
            const scaledViewport = page.getViewport({ scale: finalScale });
            
            // Устанавливаем размеры canvas
            canvas.width = scaledViewport.width;
            canvas.height = scaledViewport.height;
            
            // ИСПРАВЛЕНИЕ: Кардинальное решение для всех масштабов
            const canvasWidth = scaledViewport.width;
            const canvasHeight = scaledViewport.height;
            
            // Простое решение: всегда центрируем canvas относительно контейнера
            const leftMargin = (containerWidth - canvasWidth) / 2;
            const topMargin = (containerHeight - canvasHeight) / 2;
            
            // КАРДИНАЛЬНОЕ РЕШЕНИЕ: используем flexbox для центрирования
            if (canvasWidth > containerWidth || canvasHeight > containerHeight) {
                // Большой масштаб: используем flexbox центрирование
                container.style.display = 'flex';
                container.style.alignItems = 'center';
                container.style.justifyContent = 'center';
                container.style.overflow = 'auto';
                container.style.cursor = 'grab';
                
                canvas.style.position = 'static';
                canvas.style.left = 'auto';
                canvas.style.top = 'auto';
                canvas.style.transform = 'none';
                canvas.style.margin = '0';
                canvas.style.flexShrink = '0'; // ВАЖНО: запрещаем сжатие canvas
                canvas.style.minWidth = canvasWidth + 'px';  // Фиксируем минимальную ширину
                canvas.style.minHeight = canvasHeight + 'px'; // Фиксируем минимальную высоту
                
                console.log(`📺 FLEXBOX центрирование: ${canvasWidth}x${canvasHeight} в ${containerWidth}x${containerHeight}`);
            } else {
                // Малый масштаб: обычное absolute позиционирование
                container.style.display = 'flex';
                container.style.alignItems = 'center';
                container.style.justifyContent = 'center';
                container.style.overflow = 'hidden';
                container.style.cursor = 'default';
                
                canvas.style.position = 'static';
                canvas.style.left = 'auto';
                canvas.style.top = 'auto';
                canvas.style.transform = 'none';
                canvas.style.margin = '0';
                canvas.style.flexShrink = '0'; // Также запрещаем сжатие для малых масштабов
                canvas.style.minWidth = canvasWidth + 'px';
                canvas.style.minHeight = canvasHeight + 'px';
                
                console.log(`📐 FLEXBOX малый масштаб: ${canvasWidth}x${canvasHeight} в ${containerWidth}x${containerHeight}`);
            }
            
            console.log(`📄 Рендеринг страницы ${pageNum}:`);
            console.log(`📐 Контейнер: ${containerWidth}x${containerHeight}`);
            console.log(`🖼️ Canvas: ${canvasWidth}x${canvasHeight}`);
            console.log(`📍 Позиция: left=${leftMargin}px, top=${topMargin}px`);
            console.log(`🔍 Масштаб: ${Math.round(this.userScale * 100)}% (${finalScale.toFixed(2)})`);
            console.log(`📏 Соотношение: ${canvasWidth > containerWidth ? 'БОЛЬШЕ' : 'МЕНЬШЕ'} контейнера`);
            
            const renderContext = {
                canvasContext: context,
                viewport: scaledViewport
            };
            
            // Очищаем canvas перед рендерингом
            context.clearRect(0, 0, canvas.width, canvas.height);
            
            // Рендерим страницу
            await page.render(renderContext).promise;
            
            // Обновляем прогресс
            this.updateProgress();
            
        } catch (error) {
            console.error('❌ Ошибка рендеринга страницы:', error);
            this.showNotification('Ошибка при загрузке страницы');
        } finally {
            // Сбрасываем флаг рендеринга
            this.isRendering = false;
        }
    }

    setupEventListeners() {
        // Касание экрана для показа/скрытия контролов
        document.addEventListener('click', (e) => {
            // Не срабатываем, если кликнули на контролы
            if (e.target.closest('.reader-controls')) return;
            
            // Не срабатываем, если кликнули на модальное окно
            if (e.target.closest('#reader-modal')) return;
            
            // Переключаем видимость контролов
            this.toggleControls();
        });

        // Свайпы для перелистывания - только когда контролы скрыты
        let touchStartTime = 0;
        
        document.addEventListener('touchstart', (e) => {
            this.touchStartX = e.touches[0].clientX;
            this.touchStartY = e.touches[0].clientY;
            touchStartTime = Date.now();
        });

        document.addEventListener('touchend', (e) => {
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            const touchDuration = Date.now() - touchStartTime;
            
            const deltaX = touchEndX - this.touchStartX;
            const deltaY = Math.abs(touchEndY - this.touchStartY);
            
            // Короткое касание = переключить контролы
            // Длинный свайп = перелистывание (только если контролы скрыты)
            if (touchDuration < 300 && Math.abs(deltaX) < 30 && deltaY < 30) {
                // Короткое касание - переключаем контролы
                if (!e.target.closest('.reader-controls') && !e.target.closest('#reader-modal')) {
                    e.preventDefault();
                    this.toggleControls();
                }
            } else if (!this.isControlsVisible && Math.abs(deltaX) > 50 && deltaY < 100) {
                // Длинный свайп - перелистывание (только если контролы скрыты)
                if (deltaX > 0) {
                    this.previousPage(); // Свайп вправо - предыдущая
                } else {
                    this.nextPage(); // Свайп влево - следующая
                }
            }
        });

        // Клавиши для навигации
        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowLeft':
                    this.previousPage();
                    break;
                case 'ArrowRight':
                    this.nextPage();
                    break;
                case 'Escape':
                    this.exitFullscreen();
                    break;
                case ' ':
                    e.preventDefault();
                    this.toggleControls();
                    break;
            }
        });

        // Кнопки контролов с отладкой
        const prevBtn = document.getElementById('prev-page');
        const nextBtn = document.getElementById('next-page');
        const closeBtn = document.getElementById('close-reader');
        const fullscreenBtn = document.getElementById('toggle-orientation');
        
        console.log('Setting up event listeners...');
        console.log('Prev button:', prevBtn);
        console.log('Next button:', nextBtn);
        
        if (prevBtn) {
            prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('Previous page clicked');
                this.previousPage();
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('Next page clicked');
                this.nextPage();
            });
        }
        
        if (closeBtn) {
            closeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('Close clicked');
                this.exitFullscreen();
            });
        }
        
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log('Fullscreen clicked');
                this.requestFullscreen();
            });
        }
        
        // Слайдер страниц
        const pageSlider = document.getElementById('page-slider');
        if (pageSlider) {
            pageSlider.addEventListener('input', (e) => {
                this.goToPage(parseInt(e.target.value));
            });
        }
        
        // Дополнительные контролы
        const additionalBtns = document.querySelectorAll('.additional-controls .control-btn');
        console.log('Additional buttons found:', additionalBtns.length);
        
        additionalBtns.forEach((btn, index) => {
            const icon = btn.querySelector('i');
            let functionality = 'unknown';
            
            // Определяем функцию по иконке
            if (icon.classList.contains('bi-bookmark')) {
                functionality = 'bookmark';
            } else if (icon.classList.contains('bi-bookmark-star')) {
                functionality = 'bookmarks-list';
            } else if (icon.classList.contains('bi-search')) {
                functionality = 'search';
            } else if (icon.classList.contains('bi-gear')) {
                functionality = 'settings';
            } else if (icon.classList.contains('bi-info-circle')) {
                functionality = 'info';
            }
            
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                console.log(`Button clicked: ${functionality}`);
                
                switch(functionality) {
                    case 'bookmark':
                        this.addBookmark();
                        break;
                    case 'bookmarks-list':
                        this.showBookmarksList();
                        break;
                    case 'search':
                        this.openSearch();
                        break;
                    case 'settings':
                        this.openSettings();
                        break;
                    case 'info':
                        this.showBookInfo();
                        break;
                    default:
                        this.showNotification('Неизвестная кнопка');
                }
            });
        });

    }

    // Новый метод для обработки изменений ориентации и размера
    setupOrientationHandlers() {
        // Изменение ориентации экрана
        window.addEventListener('orientationchange', () => {
            console.log('📱 Изменение ориентации экрана');
            setTimeout(() => {
                this.renderPage(this.currentPage);
                
                if (this.isControlsVisible) {
                    this.hideControls();
                    setTimeout(() => this.toggleControls(), 300);
                }
            }, 300);
        });

        // Изменение размера окна
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                console.log('🖥️ Изменение размера окна');
                
                // Обновляем PDF рендер
                this.renderPage(this.currentPage);
                
                // Обновляем название книги (с задержкой)
                setTimeout(() => {
                    this.limitTitleForDesktop();
                }, 100);
            }, 300); // Увеличили debounce до 300ms
        });
    }
    
    // Обработчик клика по заголовку
    setupTitleClick() {
        const titleElement = document.querySelector('.reader-title');
        let titleExpandTimeout;
        
        if (titleElement) {
            titleElement.addEventListener('click', (e) => {
                e.stopPropagation(); // Предотвращаем скрытие меню
                
                // Переключаем класс для разворачивания
                titleElement.classList.toggle('expanded');
                
                if (titleElement.classList.contains('expanded')) {
                    console.log('📜 Заголовок развёрнут на полный размер');
                    
                    // Автоматически скрываем через 3 секунды
                    clearTimeout(titleExpandTimeout);
                    titleExpandTimeout = setTimeout(() => {
                        titleElement.classList.remove('expanded');
                        console.log('📜 Заголовок автоматически свёрнут');
                    }, 3000);
                } else {
                    console.log('📜 Заголовок свёрнут');
                    clearTimeout(titleExpandTimeout);
                }
            });
        }
    }

    nextPage() {
        console.log(`Next page: current=${this.currentPage}, total=${this.totalPages}`);
        if (this.currentPage < this.totalPages) {
            this.currentPage++;
            console.log(`Moving to page ${this.currentPage}`);
            this.renderPage(this.currentPage);
            this.updatePageInfo();
        } else {
            console.log('Already on last page');
        }
    }

    previousPage() {
        console.log(`Previous page: current=${this.currentPage}`);
        if (this.currentPage > 1) {
            this.currentPage--;
            console.log(`Moving to page ${this.currentPage}`);
            this.renderPage(this.currentPage);
            this.updatePageInfo();
        } else {
            console.log('Already on first page');
        }
    }

    goToPage(pageNum) {
        if (pageNum >= 1 && pageNum <= this.totalPages) {
            this.currentPage = pageNum;
            this.renderPage(this.currentPage);
            this.updatePageInfo();
        }
    }

    updatePageInfo() {
        document.getElementById('page-info').textContent = `${this.currentPage} из ${this.totalPages}`;
        document.getElementById('page-slider').value = this.currentPage;
    }

    updateProgress() {
        const progress = (this.currentPage / this.totalPages) * 100;
        document.getElementById('reading-progress').style.width = `${progress}%`;
        
        // Сохраняем прогресс в localStorage
        const bookId = document.getElementById('book-container').dataset.bookId;
        localStorage.setItem(`book_progress_${bookId}`, JSON.stringify({
            page: this.currentPage,
            progress: progress,
            timestamp: Date.now()
        }));
    }

    toggleControls() {
        const controls = document.querySelector('.reader-controls');
        this.isControlsVisible = !this.isControlsVisible;
        
        if (this.isControlsVisible) {
            controls.classList.add('visible');
            // УБИРАЕМ автоскрытие - теперь только по касанию
            console.log('Controls shown - tap screen to hide');
        } else {
            this.hideControls();
            console.log('Controls hidden - tap screen to show');
        }
    }

    hideControls() {
        const controls = document.querySelector('.reader-controls');
        controls.classList.remove('visible');
        this.isControlsVisible = false;
    }

    async enterFullscreen() {
        // Не вызываем fullscreen API автоматически
        // Только по реквесту пользователя
        
        this.isFullscreen = true;
        document.body.classList.add('fullscreen-reading');
        
        // Скрываем контролы сначала
        setTimeout(() => this.hideControls(), 1000);
    }

    exitFullscreen() {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
        
        this.isFullscreen = false;
        document.body.classList.remove('fullscreen-reading');
        
        // Возвращаемся на страницу книги
        window.history.back();
    }

    async requestFullscreen() {
        // Ручной запрос полноэкранного режима по клику
        try {
            const elem = document.documentElement;
            
            if (elem.requestFullscreen) {
                await elem.requestFullscreen();
            } else if (elem.webkitRequestFullscreen) {
                await elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) {
                await elem.msRequestFullscreen();
            }
        } catch (error) {
            console.log('Fullscreen not supported or blocked');
        }
    }

    toggleOrientation() {
        if (screen.orientation && screen.orientation.lock) {
            const currentOrientation = screen.orientation.angle;
            if (currentOrientation === 0 || currentOrientation === 180) {
                screen.orientation.lock('landscape');
            } else {
                screen.orientation.lock('portrait');
            }
        }
    }

    showNotification(message) {
        // Создаем красивое уведомление вместо alert
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.9);
            color: white;
            padding: 20px 30px;
            border-radius: 10px;
            font-size: 16px;
            text-align: center;
            z-index: 20000;
            backdrop-filter: blur(10px);
            border: 1px solid #D4AF37;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            animation: fadeInOut 2s ease;
        `;
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
        // Удаляем через 2 секунды
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 2000);
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'reader-error';
        errorDiv.innerHTML = `
            <div class="error-content">
                <i class="bi bi-exclamation-triangle"></i>
                <p>${message}</p>
                <button onclick="window.history.back()">Вернуться</button>
            </div>
        `;
        document.body.appendChild(errorDiv);
    }

    // Метод для восстановления позиции чтения
    restoreReadingPosition() {
        const bookId = document.getElementById('book-container').dataset.bookId;
        const saved = localStorage.getItem(`book_progress_${bookId}`);
        
        if (saved) {
            const data = JSON.parse(saved);
            this.goToPage(data.page);
        }
    }

    // === НОВАЯ ФУНКЦИОНАЛЬНОСТЬ ===
    
    // Закладки
    addBookmark() {
        const bookId = document.getElementById('book-container').dataset.bookId;
        const bookmarks = JSON.parse(localStorage.getItem(`bookmarks_${bookId}`) || '[]');
        
        const bookmark = {
            page: this.currentPage,
            timestamp: Date.now(),
            note: `Страница ${this.currentPage}`
        };
        
        // Проверяем, нет ли уже закладки на этой странице
        const existingIndex = bookmarks.findIndex(b => b.page === this.currentPage);
        
        if (existingIndex >= 0) {
            this.showNotification('Закладка на этой странице уже существует');
            return;
        }
        
        bookmarks.push(bookmark);
        localStorage.setItem(`bookmarks_${bookId}`, JSON.stringify(bookmarks));
        
        this.showNotification(`Закладка добавлена: стр. ${this.currentPage}`);
    }
    
    // Список закладок
    showBookmarksList() {
        const bookId = document.getElementById('book-container').dataset.bookId;
        const bookmarks = JSON.parse(localStorage.getItem(`bookmarks_${bookId}`) || '[]');
        
        if (bookmarks.length === 0) {
            this.showNotification('У вас пока нет сохранённых закладок');
            return;
        }
        
        // Сортируем по страницам
        bookmarks.sort((a, b) => a.page - b.page);
        
        const bookmarksHTML = bookmarks.map((bookmark, index) => `
            <div style="
                background: rgba(51, 51, 51, 0.9);
                padding: 12px;
                margin: 8px 0;
                border-radius: 8px;
                cursor: pointer;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border: 1px solid rgba(212, 175, 55, 0.3);
                transition: all 0.3s ease;
                backdrop-filter: blur(5px);
            " 
            onmouseover="this.style.background='rgba(212, 175, 55, 0.2)'; this.style.borderColor='#D4AF37'"
            onmouseout="this.style.background='rgba(51, 51, 51, 0.9)'; this.style.borderColor='rgba(212, 175, 55, 0.3)'"
            onclick="window.readerInstance.goToBookmark(${bookmark.page}); window.readerInstance.closeModal();">
                <div>
                    <div style="color: #D4AF37; font-weight: 600; margin-bottom: 4px;">
                        <i class="bi bi-bookmark-fill" style="margin-right: 8px;"></i>
                        Страница ${bookmark.page}
                    </div>
                    <div style="color: #ccc; font-size: 12px;">
                        <i class="bi bi-clock" style="margin-right: 5px;"></i>
                        ${new Date(bookmark.timestamp).toLocaleString('ru-RU')}
                    </div>
                </div>
                <button 
                    onclick="event.stopPropagation(); window.readerInstance.removeBookmark(${index})"
                    style="
                        background: rgba(255, 255, 255, 0.9);
                        border: none;
                        color: #333;
                        width: 24px;
                        height: 24px;
                        border-radius: 50%;
                        cursor: pointer;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        transition: all 0.3s ease;
                        font-weight: bold;
                    "
                    onmouseover="this.style.background='rgba(220, 53, 69, 0.9)'; this.style.color='white'; this.style.transform='scale(1.1)'"
                    onmouseout="this.style.background='rgba(255, 255, 255, 0.9)'; this.style.color='#333'; this.style.transform='scale(1)'"
                    title="Удалить закладку">
                    <i class="bi bi-x" style="font-size: 14px; font-weight: bold;"></i>
                </button>
            </div>
        `).join('');
        
        this.createModal('Список закладок', `
            <div style="padding: 20px; max-height: 400px; overflow-y: auto;">
                <div style="margin-bottom: 15px; color: white; text-align: center;">
                    <i class="bi bi-bookmark-star" style="color: #D4AF37; font-size: 24px; margin-right: 10px;"></i>
                    Найдено закладок: <strong style="color: #D4AF37;">${bookmarks.length}</strong>
                </div>
                
                ${bookmarksHTML}
                
                <div style="text-align: center; margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(212, 175, 55, 0.3);">
                    <button 
                        onclick="window.readerInstance.clearAllBookmarks()"
                        style="
                            background: rgba(220, 53, 69, 0.8);
                            color: white;
                            border: none;
                            padding: 8px 15px;
                            border-radius: 5px;
                            cursor: pointer;
                            margin-right: 10px;
                            transition: all 0.3s ease;
                        "
                        onmouseover="this.style.background='rgba(220, 53, 69, 1)'"
                        onmouseout="this.style.background='rgba(220, 53, 69, 0.8)'">
                        <i class="bi bi-trash3" style="margin-right: 5px;"></i>
                        Очистить все
                    </button>
                    
                    <button 
                        onclick="window.readerInstance.closeModal()"
                        style="
                            background: rgba(102, 102, 102, 0.8);
                            color: white;
                            border: none;
                            padding: 8px 15px;
                            border-radius: 5px;
                            cursor: pointer;
                            transition: all 0.3s ease;
                        "
                        onmouseover="this.style.background='rgba(102, 102, 102, 1)'"
                        onmouseout="this.style.background='rgba(102, 102, 102, 0.8)'">
                        <i class="bi bi-x-lg" style="margin-right: 5px;"></i>
                        Закрыть
                    </button>
                </div>
            </div>
        `);
    }
    
    // Переход к закладке
    goToBookmark(page) {
        this.goToPage(page);
        this.showNotification(`Переход к закладке: стр. ${page}`);
    }
    
    // Удаление одной закладки
    removeBookmark(index) {
        const bookId = document.getElementById('book-container').dataset.bookId;
        const bookmarks = JSON.parse(localStorage.getItem(`bookmarks_${bookId}`) || '[]');
        
        if (index >= 0 && index < bookmarks.length) {
            const removedBookmark = bookmarks.splice(index, 1)[0];
            localStorage.setItem(`bookmarks_${bookId}`, JSON.stringify(bookmarks));
            
            this.showNotification(`Закладка со стр. ${removedBookmark.page} удалена`);
            
            // Обновляем список
            this.closeModal();
            setTimeout(() => this.showBookmarksList(), 300);
        }
    }
    
    // Очистка всех закладок
    clearAllBookmarks() {
        const bookId = document.getElementById('book-container').dataset.bookId;
        const bookmarks = JSON.parse(localStorage.getItem(`bookmarks_${bookId}`) || '[]');
        
        if (bookmarks.length === 0) {
            this.showNotification('Закладок нет');
            return;
        }
        
        if (confirm(`Удалить все ${bookmarks.length} закладок?`)) {
            localStorage.removeItem(`bookmarks_${bookId}`);
            this.showNotification(`Удалено ${bookmarks.length} закладок`);
            this.closeModal();
        }
    }
    
    // Поиск
    openSearch() {
        this.createModal('Поиск по документу', `
            <div style="padding: 20px;">
                <input type="text" id="search-input" placeholder="Введите текст для поиска..." 
                       style="width: 100%; padding: 12px; font-size: 16px; border: 1px solid #D4AF37; border-radius: 5px; background: #2a2a2a; color: white;">
                <div style="margin-top: 15px; text-align: center;">
                    <button id="search-btn" style="background: #D4AF37; color: black; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-right: 10px;">Найти</button>
                    <button id="search-close" style="background: #666; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">Закрыть</button>
                </div>
                <div id="search-results" style="margin-top: 15px; color: #ccc; font-size: 14px;"></div>
            </div>
        `);
        
        // Обработчики
        document.getElementById('search-btn').onclick = () => this.performSearch();
        document.getElementById('search-close').onclick = () => this.closeModal();
        document.getElementById('search-input').focus();
    }
    
    performSearch() {
        const query = document.getElementById('search-input').value.trim();
        if (!query) {
            document.getElementById('search-results').textContent = 'Введите текст для поиска';
            return;
        }
        
        document.getElementById('search-results').textContent = `Поиск "${query}"... (Функция в разработке)`;
        
        // TODO: Реальный поиск по PDF через PDF.js
    }
    
    // Настройки
    openSettings() {
        // Загружаем сохранённые настройки
        const bookId = document.getElementById('book-container').dataset.bookId;
        const savedSettings = JSON.parse(localStorage.getItem(`reader_settings_${bookId}`) || '{}');
        
        const currentBrightness = savedSettings.brightness || 1;
        const currentTheme = savedSettings.theme || 'dark';
        
        // Создаём прозрачное модальное окно для настроек
        this.createTransparentModal('Настройки чтения', `
            <div style="padding: 20px;">
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; color: white; text-shadow: 1px 1px 2px black;">Яркость:</label>
                    <input type="range" id="brightness-slider" min="0.3" max="1.5" step="0.1" value="${currentBrightness}" 
                           style="width: 100%;">
                    <span id="brightness-value" style="color: #ccc; text-shadow: 1px 1px 2px black;">${Math.round(currentBrightness * 100)}%</span>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; color: white; text-shadow: 1px 1px 2px black;">Масштаб:</label>
                    <input type="range" id="scale-slider" min="0.5" max="2" step="0.1" value="${this.userScale}" 
                           style="width: 100%;">
                    <span id="scale-value" style="color: #ccc; text-shadow: 1px 1px 2px black;">${Math.round(this.userScale * 100)}%</span>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; color: white; text-shadow: 1px 1px 2px black;">Цветовая схема:</label>
                    <select id="theme-select" style="width: 100%; padding: 8px; background: rgba(42, 42, 42, 0.9); color: white; border: 1px solid #D4AF37; border-radius: 5px;">
                        <option value="dark" ${currentTheme === 'dark' ? 'selected' : ''}>Тёмная (стандартная)</option>
                        <option value="sepia" ${currentTheme === 'sepia' ? 'selected' : ''}>Тёплая (сепия)</option>
                        <option value="light" ${currentTheme === 'light' ? 'selected' : ''}>Светлая (дневная)</option>
                        <option value="night" ${currentTheme === 'night' ? 'selected' : ''}>Ночная (очень тёмная)</option>
                    </select>
                </div>
                
                <div style="text-align: center;">
                    <button id="settings-apply" style="background: rgba(40, 167, 69, 0.9); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-right: 10px; backdrop-filter: blur(5px);">Применить</button>
                    <button id="settings-save" style="background: rgba(212, 175, 55, 0.9); color: black; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-right: 10px; backdrop-filter: blur(5px);">Сохранить</button>
                    <button id="settings-reset" style="background: rgba(220, 53, 69, 0.9); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-right: 10px; backdrop-filter: blur(5px);">Сброс</button>
                    <button id="settings-close" style="background: rgba(102, 102, 102, 0.9); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; backdrop-filter: blur(5px);">Закрыть</button>
                </div>
            </div>
        `);
        
        // Применяем текущие настройки
        this.applyTheme(currentTheme);
        
        // Обработчики (оставляем те же самые)
        document.getElementById('brightness-slider').oninput = (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('brightness-value').textContent = Math.round(value * 100) + '%';
            this.applyBrightness(value);
        };
        
        document.getElementById('scale-slider').oninput = (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('scale-value').textContent = Math.round(value * 100) + '%';
            this.userScale = value;
            console.log('Масштаб изменён на:', value);
            // Перерисовываем с новым масштабом
            this.renderPage(this.currentPage);
        };
        
        document.getElementById('theme-select').onchange = (e) => {
            console.log('Смена темы на:', e.target.value);
            this.applyTheme(e.target.value);
        };
        
        document.getElementById('settings-apply').onclick = () => {
            this.showNotification('Настройки применены временно');
        };
        
        document.getElementById('settings-save').onclick = () => {
            this.saveSettings();
            this.closeModal();
        };
        
        document.getElementById('settings-reset').onclick = () => {
            document.getElementById('brightness-slider').value = 1;
            document.getElementById('brightness-value').textContent = '100%';
            document.getElementById('scale-slider').value = 1;
            document.getElementById('scale-value').textContent = '100%';
            document.getElementById('theme-select').value = 'dark';
            
            this.applyBrightness(1);
            this.userScale = 1;
            this.applyTheme('dark');
            this.renderPage(this.currentPage);
            
            this.showNotification('Настройки сброшены');
        };
        
        document.getElementById('settings-close').onclick = () => this.closeModal();
    }
    
    applyTheme(theme) {
        console.log('Применяем тему:', theme);
        const canvas = document.getElementById('pdf-canvas');
        const readerContainer = document.querySelector('.modern-reader');
        
        if (!canvas) {
            console.log('Канвас не найден');
            return;
        }
        
        // Сбрасываем предыдущие фильтры
        canvas.style.filter = '';
        
        switch(theme) {
            case 'sepia':
                console.log('Применяем сепию');
                canvas.style.filter = 'sepia(0.6) contrast(1.1) brightness(0.95)';
                if (readerContainer) readerContainer.style.background = '#2b1810';
                break;
                
            case 'light':
                console.log('Применяем светлую тему');
                canvas.style.filter = 'brightness(1.3) contrast(1.2) invert(0)';
                if (readerContainer) readerContainer.style.background = '#f5f5f5';
                break;
                
            case 'night':
                console.log('Применяем ночную тему');
                canvas.style.filter = 'brightness(0.7) contrast(1.1) invert(0.1)';
                if (readerContainer) readerContainer.style.background = '#0a0a0a';
                break;
                
            default: // dark
                console.log('Применяем стандартную тёмную тему');
                canvas.style.filter = 'brightness(0.95) contrast(1.05)';
                if (readerContainer) readerContainer.style.background = '#1a1a1a';
        }
        
        // Показываем уведомление
        const themeNames = {
            'dark': 'Тёмная тема',
            'sepia': 'Тёплая тема',
            'light': 'Светлая тема',
            'night': 'Ночная тема'
        };
        
        this.showNotification(`Применена: ${themeNames[theme] || theme}`);
    }
    
    applyBrightness(brightness) {
        const canvas = document.getElementById('pdf-canvas');
        if (canvas) {
            // Получаем текущие фильтры и обновляем яркость
            let currentFilter = canvas.style.filter || '';
            
            // Удаляем старое значение brightness
            currentFilter = currentFilter.replace(/brightness\([^)]*\)/g, '');
            
            // Добавляем новое
            currentFilter = `brightness(${brightness}) ${currentFilter}`.trim();
            
            canvas.style.filter = currentFilter;
        }
    }
    
    saveSettings() {
        const brightness = document.getElementById('brightness-slider').value;
        const scale = document.getElementById('scale-slider').value;
        const theme = document.getElementById('theme-select').value;
        
        const settings = {
            brightness: parseFloat(brightness),
            scale: parseFloat(scale),
            theme: theme
        };
        
        const bookId = document.getElementById('book-container').dataset.bookId;
        localStorage.setItem(`reader_settings_${bookId}`, JSON.stringify(settings));
        
        console.log('Настройки сохранены:', settings);
        this.showNotification('Настройки сохранены и будут применяться при следующем открытии');
    }
    
    // Загрузка сохранённых настроек при старте
    loadSavedSettings() {
        const bookId = document.getElementById('book-container').dataset.bookId;
        const savedSettings = JSON.parse(localStorage.getItem(`reader_settings_${bookId}`) || '{}');
        
        if (Object.keys(savedSettings).length > 0) {
            console.log('Загружаем сохранённые настройки:', savedSettings);
            
            // Применяем яркость
            if (savedSettings.brightness) {
                this.applyBrightness(savedSettings.brightness);
            }
            
            // Применяем масштаб
            if (savedSettings.scale) {
                console.log('Загружаем сохранённый масштаб:', savedSettings.scale);
                this.userScale = savedSettings.scale;
                // Перерисовываем с новым масштабом
                this.renderPage(this.currentPage);
            }
            
            // Применяем тему
            if (savedSettings.theme) {
                this.applyTheme(savedSettings.theme);
            }
        }
    }
    
    // Информация о книге
    showBookInfo() {
        const bookTitle = document.getElementById('book-container').dataset.bookTitle;
        const bookId = document.getElementById('book-container').dataset.bookId;
        
        this.createModal('Информация о книге', `
            <div style="padding: 20px; color: white;">
                <h3 style="color: #D4AF37; margin-bottom: 15px;">${bookTitle}</h3>
                
                <div style="margin-bottom: 10px;"><strong>Страниц:</strong> ${this.totalPages}</div>
                <div style="margin-bottom: 10px;"><strong>Текущая страница:</strong> ${this.currentPage}</div>
                <div style="margin-bottom: 10px;"><strong>Прогресс:</strong> ${Math.round((this.currentPage / this.totalPages) * 100)}%</div>
                <div style="margin-bottom: 10px;"><strong>ID книги:</strong> ${bookId}</div>
                
                <div style="margin-top: 20px;">
                    <strong>Закладки:</strong>
                    <div id="bookmarks-list" style="max-height: 150px; overflow-y: auto; margin-top: 10px;"></div>
                </div>
                
                <div style="text-align: center; margin-top: 20px;">
                    <button id="info-close" style="background: #D4AF37; color: black; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">Закрыть</button>
                </div>
            </div>
        `);
        
        // Загружаем закладки
        this.loadBookmarksList();
        
        document.getElementById('info-close').onclick = () => this.closeModal();
    }
    
    loadBookmarksList() {
        const bookId = document.getElementById('book-container').dataset.bookId;
        const bookmarks = JSON.parse(localStorage.getItem(`bookmarks_${bookId}`) || '[]');
        const listContainer = document.getElementById('bookmarks-list');
        
        if (bookmarks.length === 0) {
            listContainer.innerHTML = '<div style="color: #888; font-style: italic;">Закладок нет</div>';
            return;
        }
        
        listContainer.innerHTML = bookmarks.map((bookmark, index) => `
            <div style="background: #333; padding: 8px; margin: 5px 0; border-radius: 5px; cursor: pointer; display: flex; justify-content: space-between;" 
                 onclick="window.readerInstance.goToPage(${bookmark.page})">
                <span>Стр. ${bookmark.page}</span>
                <span style="color: #888; font-size: 12px;">${new Date(bookmark.timestamp).toLocaleString()}</span>
            </div>
        `).join('');
    }
    
    // Прозрачное модальное окно для настроек
    createTransparentModal(title, content) {
        const modal = document.createElement('div');
        modal.id = 'reader-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 30000;
        `;
        
        modal.innerHTML = `
            <div style="
                background: rgba(26, 26, 26, 0.6);
                border: 2px solid rgba(212, 175, 55, 0.8);
                border-radius: 10px;
                max-width: 450px;
                width: 85%;
                max-height: 70vh;
                overflow-y: auto;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            ">
                <div style="
                    background: linear-gradient(135deg, rgba(212, 175, 55, 0.8), rgba(184, 148, 31, 0.8));
                    color: black;
                    padding: 12px 20px;
                    font-weight: 600;
                    border-radius: 8px 8px 0 0;
                    text-shadow: 1px 1px 2px rgba(255,255,255,0.3);
                ">${title}</div>
                ${content}
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Закрытие по клику на фон
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeModal();
            }
        });
    }
    
    // Модальное окно
    createModal(title, content) {
        const modal = document.createElement('div');
        modal.id = 'reader-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0,0,0,0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 30000;
            backdrop-filter: blur(2px);
        `;
        
        modal.innerHTML = `
            <div style="
                background: rgba(26, 26, 26, 0.95);
                border: 2px solid #D4AF37;
                border-radius: 10px;
                max-width: 500px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 10px 30px rgba(0,0,0,0.8);
                backdrop-filter: blur(10px);
            ">
                <div style="
                    background: linear-gradient(135deg, rgba(212, 175, 55, 0.9), rgba(184, 148, 31, 0.9));
                    color: black;
                    padding: 15px 20px;
                    font-weight: 600;
                    border-radius: 8px 8px 0 0;
                ">${title}</div>
                ${content}
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Закрытие по клику на фон
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeModal();
            }
        });
    }
    
    // Ограничение названия книги для десктопа
    limitTitleForDesktop() {
        try {
            const titleElement = document.querySelector('.reader-title');
            if (!titleElement) {
                console.log('🚫 Название книги не найдено');
                return;
            }
            
            // Сохраняем оригинальное название, если ещё не сохранено
            if (!titleElement.title) {
                titleElement.title = titleElement.textContent.trim();
            }
            
            const originalTitle = titleElement.title;
            if (!originalTitle) {
                console.log('🚫 Оригинальное название пустое');
                return;
            }
            
            // Проверяем, что это десктоп (ширина больше 768px)
            if (window.innerWidth > 768) {
                if (originalTitle.length > 30) {
                    titleElement.textContent = originalTitle.substring(0, 30) + '...';
                    console.log(`📋 Название обрезано до 30 символов для десктопа`);
                } else {
                    console.log('📱 Название короткое, оставляем как есть');
                }
            } else {
                // На мобильных устройствах показываем полное название
                titleElement.textContent = originalTitle;
                console.log('📱 Полное название для мобильного');
            }
        } catch (error) {
            console.error('⚠️ Ошибка в limitTitleForDesktop:', error);
        }
    }
    
    closeModal() {
        const modal = document.getElementById('reader-modal');
        if (modal) {
            modal.remove();
        }
    }
}

// Инициализация reader при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Загружаем PDF.js если еще не загружен
    if (typeof pdfjsLib === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.min.js';
        script.onload = () => {
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.worker.min.js';
            window.readerInstance = new ModernReader();
        };
        document.head.appendChild(script);
    } else {
        window.readerInstance = new ModernReader();
    }
});
