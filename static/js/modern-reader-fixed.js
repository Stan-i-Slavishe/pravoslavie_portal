// Современный Reader для PDF книг - ИСПРАВЛЕННАЯ ВЕРСИЯ
class ModernReader {
    constructor() {
        this.currentPage = 1;
        this.totalPages = 0;
        this.isFullscreen = false;
        this.pdfDoc = null;
        this.userScale = 1.0; // ИСПРАВЛЕНО: переименовал scale в userScale
        this.isControlsVisible = false;
        this.touchStartX = 0;
        this.touchStartY = 0;
        
        this.init();
    }

    async renderPage(pageNum) {
        if (!this.pdfDoc) return;
        
        try {
            const page = await this.pdfDoc.getPage(pageNum);
            const canvas = document.getElementById('pdf-canvas');
            const context = canvas.getContext('2d');
            
            // Рассчитываем базовый масштаб под размер экрана
            const viewport = page.getViewport({ scale: 1 });
            const containerWidth = window.innerWidth;
            const containerHeight = window.innerHeight;
            
            const scaleX = containerWidth / viewport.width;
            const scaleY = containerHeight / viewport.height;
            const baseScale = Math.min(scaleX, scaleY) * 0.9;
            
            // ИСПРАВЛЕНО: Применяем пользовательский масштаб поверх базового
            const finalScale = baseScale * this.userScale;
            
            const scaledViewport = page.getViewport({ scale: finalScale });
            
            canvas.width = scaledViewport.width;
            canvas.height = scaledViewport.height;
            
            // Центрируем canvas
            const leftMargin = (containerWidth - scaledViewport.width) / 2;
            const topMargin = (containerHeight - scaledViewport.height) / 2;
            
            canvas.style.position = 'absolute';
            canvas.style.left = `${leftMargin}px`;
            canvas.style.top = `${topMargin}px`;
            canvas.style.marginLeft = '0';
            canvas.style.marginTop = '0';
            
            const renderContext = {
                canvasContext: context,
                viewport: scaledViewport
            };
            
            console.log(`Рендерим страницу ${pageNum} с масштабом: базовый=${baseScale.toFixed(2)}, пользовательский=${this.userScale}, итоговый=${finalScale.toFixed(2)}`);
            
            await page.render(renderContext).promise;
            this.updateProgress();
            
        } catch (error) {
            console.error('Ошибка рендеринга страницы:', error);
        }
    }

    // ИСПРАВЛЕНО: обработчик масштаба в настройках
    openSettings() {
        const bookId = document.getElementById('book-container').dataset.bookId;
        const savedSettings = JSON.parse(localStorage.getItem(`reader_settings_${bookId}`) || '{}');
        
        const currentBrightness = savedSettings.brightness || 1;
        const currentTheme = savedSettings.theme || 'dark';
        
        this.createTransparentModal('Настройки чтения', `
            <div style="padding: 20px;">
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; color: white; text-shadow: 1px 1px 2px black;">Яркость:</label>
                    <input type="range" id="brightness-slider" min="0.3" max="1.5" step="0.1" value="${currentBrightness}" style="width: 100%;">
                    <span id="brightness-value" style="color: #ccc; text-shadow: 1px 1px 2px black;">${Math.round(currentBrightness * 100)}%</span>
                </div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; color: white; text-shadow: 1px 1px 2px black;">Масштаб:</label>
                    <input type="range" id="scale-slider" min="0.5" max="2" step="0.1" value="${this.userScale}" style="width: 100%;">
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
                    <button id="settings-apply" style="background: rgba(40, 167, 69, 0.9); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-right: 10px;">Применить</button>
                    <button id="settings-save" style="background: rgba(212, 175, 55, 0.9); color: black; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-right: 10px;">Сохранить</button>
                    <button id="settings-reset" style="background: rgba(220, 53, 69, 0.9); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-right: 10px;">Сброс</button>
                    <button id="settings-close" style="background: rgba(102, 102, 102, 0.9); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">Закрыть</button>
                </div>
            </div>
        `);
        
        this.applyTheme(currentTheme);
        
        // ИСПРАВЛЕНО: правильные обработчики
        document.getElementById('brightness-slider').oninput = (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('brightness-value').textContent = Math.round(value * 100) + '%';
            this.applyBrightness(value);
        };
        
        // ГЛАВНОЕ ИСПРАВЛЕНИЕ - правильная работа с масштабом
        document.getElementById('scale-slider').oninput = (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('scale-value').textContent = Math.round(value * 100) + '%';
            this.userScale = value; // ИСПРАВЛЕНО: используем userScale
            console.log('Масштаб изменён на:', value);
            this.renderPage(this.currentPage); // Немедленно перерисовываем
        };
        
        document.getElementById('theme-select').onchange = (e) => {
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
            this.userScale = 1; // ИСПРАВЛЕНО: userScale вместо scale
            this.applyTheme('dark');
            this.renderPage(this.currentPage);
            
            this.showNotification('Настройки сброшены');
        };
        
        document.getElementById('settings-close').onclick = () => this.closeModal();
    }

    // ИСПРАВЛЕНО: правильное сохранение настроек
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
        this.showNotification('Настройки сохранены');
    }
    
    // ИСПРАВЛЕНО: правильная загрузка настроек
    loadSavedSettings() {
        const bookId = document.getElementById('book-container').dataset.bookId;
        const savedSettings = JSON.parse(localStorage.getItem(`reader_settings_${bookId}`) || '{}');
        
        if (Object.keys(savedSettings).length > 0) {
            console.log('Загружаем сохранённые настройки:', savedSettings);
            
            if (savedSettings.brightness) {
                this.applyBrightness(savedSettings.brightness);
            }
            
            // ИСПРАВЛЕНО: правильная загрузка масштаба
            if (savedSettings.scale) {
                console.log('Загружаем сохранённый масштаб:', savedSettings.scale);
                this.userScale = savedSettings.scale;
                this.renderPage(this.currentPage);
            }
            
            if (savedSettings.theme) {
                this.applyTheme(savedSettings.theme);
            }
        }
    }

    // Остальные методы остаются как в оригинале...
    async init() {
        try {
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
            
            this.setupEventListeners();
            this.enterFullscreen();
            
            setTimeout(() => {
                this.toggleControls();
            }, 500);
            
            await this.loadPDF(pdfUrl);
            
        } catch (error) {
            console.error('Initialization error:', error);
            this.showError(`Ошибка инициализации: ${error.message}`);
        }
    }

    async loadPDF(url) {
        try {
            console.log('Loading PDF from:', url);
            
            const spinner = document.querySelector('.loading-spinner');
            if (spinner) spinner.style.display = 'flex';
            
            const loadingTask = pdfjsLib.getDocument({
                url: url,
                cMapUrl: 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.11.338/cmaps/',
                cMapPacked: true
            });
            
            this.pdfDoc = await loadingTask.promise;
            this.totalPages = this.pdfDoc.numPages;
            
            console.log('PDF loaded successfully. Pages:', this.totalPages);
            
            document.getElementById('page-info').textContent = `${this.currentPage} из ${this.totalPages}`;
            
            const slider = document.getElementById('page-slider');
            slider.max = this.totalPages;
            slider.value = this.currentPage;
            
            if (spinner) spinner.style.display = 'none';
            
            await this.renderPage(this.currentPage);
            this.loadSavedSettings(); // ИСПРАВЛЕНО: загружаем настройки после рендеринга
            
        } catch (error) {
            console.error('Ошибка загрузки PDF:', error);
            this.showError(`Не удалось загрузить книгу: ${error.message}`);
        }
    }

    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('.reader-controls')) return;
            this.toggleControls();
        });

        document.addEventListener('keydown', (e) => {
            switch(e.key) {
                case 'ArrowLeft': this.previousPage(); break;
                case 'ArrowRight': this.nextPage(); break;
                case 'Escape': this.exitFullscreen(); break;
                case ' ': e.preventDefault(); this.toggleControls(); break;
            }
        });

        const prevBtn = document.getElementById('prev-page');
        const nextBtn = document.getElementById('next-page');
        const closeBtn = document.getElementById('close-reader');
        
        if (prevBtn) prevBtn.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); this.previousPage(); });
        if (nextBtn) nextBtn.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); this.nextPage(); });
        if (closeBtn) closeBtn.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); this.exitFullscreen(); });
        
        const pageSlider = document.getElementById('page-slider');
        if (pageSlider) {
            pageSlider.addEventListener('input', (e) => {
                this.goToPage(parseInt(e.target.value));
            });
        }
        
        const additionalBtns = document.querySelectorAll('.additional-controls .control-btn');
        additionalBtns.forEach((btn, index) => {
            const icon = btn.querySelector('i');
            let functionality = 'unknown';
            
            if (icon.classList.contains('bi-gear')) {
                functionality = 'settings';
            }
            
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                if (functionality === 'settings') {
                    this.openSettings();
                } else {
                    this.showNotification('Кнопка в разработке');
                }
            });
        });

        window.addEventListener('resize', () => {
            this.renderPage(this.currentPage);
        });
    }

    nextPage() {
        if (this.currentPage < this.totalPages) {
            this.currentPage++;
            this.renderPage(this.currentPage);
            this.updatePageInfo();
        }
    }

    previousPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.renderPage(this.currentPage);
            this.updatePageInfo();
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
        this.isFullscreen = true;
        document.body.classList.add('fullscreen-reading');
        setTimeout(() => this.hideControls(), 1000);
    }

    exitFullscreen() {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        }
        
        this.isFullscreen = false;
        document.body.classList.remove('fullscreen-reading');
        window.history.back();
    }

    applyTheme(theme) {
        const canvas = document.getElementById('pdf-canvas');
        if (!canvas) return;
        
        canvas.style.filter = '';
        
        switch(theme) {
            case 'sepia':
                canvas.style.filter = 'sepia(0.6) contrast(1.1) brightness(0.95)';
                break;
            case 'light':
                canvas.style.filter = 'brightness(1.3) contrast(1.2)';
                break;
            case 'night':
                canvas.style.filter = 'brightness(0.7) contrast(1.1)';
                break;
            default:
                canvas.style.filter = 'brightness(0.95) contrast(1.05)';
        }
        
        this.showNotification(`Применена тема: ${theme}`);
    }
    
    applyBrightness(brightness) {
        const canvas = document.getElementById('pdf-canvas');
        if (canvas) {
            let currentFilter = canvas.style.filter || '';
            currentFilter = currentFilter.replace(/brightness\([^)]*\)/g, '');
            currentFilter = `brightness(${brightness}) ${currentFilter}`.trim();
            canvas.style.filter = currentFilter;
        }
    }

    showNotification(message) {
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
        `;
        
        notification.textContent = message;
        document.body.appendChild(notification);
        
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
            <div style="background: rgba(26, 26, 26, 0.6); border: 2px solid rgba(212, 175, 55, 0.8); border-radius: 10px; max-width: 450px; width: 85%; max-height: 70vh; overflow-y: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <div style="background: linear-gradient(135deg, rgba(212, 175, 55, 0.8), rgba(184, 148, 31, 0.8)); color: black; padding: 12px 20px; font-weight: 600; border-radius: 8px 8px 0 0;">${title}</div>
                ${content}
            </div>
        `;
        
        document.body.appendChild(modal);
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeModal();
            }
        });
    }
    
    closeModal() {
        const modal = document.getElementById('reader-modal');
        if (modal) {
            modal.remove();
        }
    }
}

// Инициализация
document.addEventListener('DOMContentLoaded', function() {
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
