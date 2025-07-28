// Современный Reader для PDF книг
class ModernReader {
    constructor() {
        this.currentPage = 1;
        this.totalPages = 0;
        this.isFullscreen = false;
        this.pdfDoc = null;
        this.scale = 1.0;
        this.isControlsVisible = false;
        this.touchStartX = 0;
        this.touchStartY = 0;
        
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
            
            // Псевдо-полноэкранный режим
            this.enterFullscreen();
            
            // Показываем контролы сразу для тестирования
            setTimeout(() => {
                this.toggleControls();
            }, 500);
            
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
            
        } catch (error) {
            console.error('Ошибка загрузки PDF:', error);
            this.showError(`Не удалось загрузить книгу: ${error.message}`);
        }
    }

    async renderPage(pageNum) {
        if (!this.pdfDoc) return;
        
        try {
            const page = await this.pdfDoc.getPage(pageNum);
            const canvas = document.getElementById('pdf-canvas');
            const context = canvas.getContext('2d');
            
            // Рассчитываем масштаб под размер экрана
            const viewport = page.getViewport({ scale: 1 });
            const containerWidth = window.innerWidth;
            const containerHeight = window.innerHeight;
            
            const scaleX = containerWidth / viewport.width;
            const scaleY = containerHeight / viewport.height;
            this.scale = Math.min(scaleX, scaleY) * 0.9;
            
            const scaledViewport = page.getViewport({ scale: this.scale });
            
            canvas.width = scaledViewport.width;
            canvas.height = scaledViewport.height;
            
            // Центрируем canvas
            canvas.style.marginLeft = `${(containerWidth - scaledViewport.width) / 2}px`;
            canvas.style.marginTop = `${(containerHeight - scaledViewport.height) / 2}px`;
            
            const renderContext = {
                canvasContext: context,
                viewport: scaledViewport
            };
            
            await page.render(renderContext).promise;
            
            // Обновляем прогресс
            this.updateProgress();
            
        } catch (error) {
            console.error('Ошибка рендеринга страницы:', error);
        }
    }

    setupEventListeners() {
        // Касание экрана для показа/скрытия контролов
        document.addEventListener('click', (e) => {
            if (e.target.closest('.reader-controls')) return;
            this.toggleControls();
        });

        // Свайпы для перелистывания
        document.addEventListener('touchstart', (e) => {
            this.touchStartX = e.touches[0].clientX;
            this.touchStartY = e.touches[0].clientY;
        });

        document.addEventListener('touchend', (e) => {
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            
            const deltaX = touchEndX - this.touchStartX;
            const deltaY = Math.abs(touchEndY - this.touchStartY);
            
            // Только горизонтальные свайпы
            if (Math.abs(deltaX) > 50 && deltaY < 100) {
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
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const title = btn.getAttribute('title') || `Button ${index}`;
                console.log(`Additional button clicked: ${title}`);
                
                // Пока просто показываем алерт
                this.showNotification(`Кнопка "${title}" нажата!\nЭта функция в разработке...`);
            });
        });

        // Изменение ориентации экрана
        window.addEventListener('orientationchange', () => {
            setTimeout(() => this.renderPage(this.currentPage), 500);
        });

        // Изменение размера окна
        window.addEventListener('resize', () => {
            this.renderPage(this.currentPage);
        });
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
            // Автоскрытие через 3 секунды
            setTimeout(() => {
                if (this.isControlsVisible) {
                    this.hideControls();
                }
            }, 3000);
        } else {
            this.hideControls();
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
}

// Инициализация reader при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Загружаем PDF.js если еще не загружен
    if (typeof pdfjsLib === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.min.js';
        script.onload = () => {
            pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/pdf.worker.min.js';
            new ModernReader();
        };
        document.head.appendChild(script);
    } else {
        new ModernReader();
    }
});
