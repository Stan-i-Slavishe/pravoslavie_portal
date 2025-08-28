/**
 * Умное управление dropdown меню для предотвращения наложений
 * Автор: Система управления конфликтами dropdown
 * Версия: 1.0
 */

class SmartDropdownManager {
    constructor() {
        this.dropdowns = {};
        this.strategies = {
            'xs': 'close-others',     // < 576px - закрываем другие
            'sm': 'shift-down',       // < 768px - смещаем вниз  
            'md': 'shift-smart',      // < 992px - умное смещение
            'lg': 'default'           // >= 992px - стандартное поведение
        };
        
        this.init();
    }
    
    init() {
        // Ждём полной загрузки DOM
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }
    
    setup() {
        this.findDropdowns();
        this.addEventListeners();
        console.log('✅ SmartDropdownManager активирован');
    }
    
    findDropdowns() {
        // Автоматически находим все dropdown в навигации
        const navDropdowns = document.querySelectorAll('.navbar .dropdown');
        
        navDropdowns.forEach((dropdown, index) => {
            const toggle = dropdown.querySelector('.dropdown-toggle');
            const menu = dropdown.querySelector('.dropdown-menu');
            
            if (toggle && menu) {
                const id = toggle.id || `dropdown-${index}`;
                this.dropdowns[id] = {
                    element: dropdown,
                    toggle: toggle,
                    menu: menu,
                    isOpen: false,
                    originalPosition: null
                };
            }
        });
        
        console.log(`🔍 Найдено ${Object.keys(this.dropdowns).length} dropdown меню`);
    }
    
    addEventListeners() {
        Object.keys(this.dropdowns).forEach(id => {
            const dropdown = this.dropdowns[id];
            
            // События Bootstrap dropdown
            dropdown.element.addEventListener('show.bs.dropdown', (e) => {
                this.handleDropdownShow(id, e);
            });
            
            dropdown.element.addEventListener('shown.bs.dropdown', (e) => {
                this.handleDropdownShown(id, e);
            });
            
            dropdown.element.addEventListener('hide.bs.dropdown', (e) => {
                this.handleDropdownHide(id, e);
            });
        });
        
        // Обработчик изменения размера окна
        window.addEventListener('resize', () => {
            this.handleResize();
        });
        
        // Закрытие при клике вне области
        document.addEventListener('click', (e) => {
            this.handleOutsideClick(e);
        });
    }
    
    handleDropdownShow(currentId, event) {
        console.log(`📂 Открывается dropdown: ${currentId}`);
        
        const openDropdowns = this.getOpenDropdowns();
        const strategy = this.getCurrentStrategy();
        
        if (openDropdowns.length > 0 && this.isMobile()) {
            console.log(`⚠️ Конфликт с: ${openDropdowns.join(', ')}`);
            console.log(`🎯 Применяется стратегия: ${strategy}`);
            
            this.applyStrategy(strategy, currentId, openDropdowns);
        }
        
        this.dropdowns[currentId].isOpen = true;
    }
    
    handleDropdownShown(currentId, event) {
        // Проверяем позиционирование после полного открытия
        if (this.isMobile()) {
            this.checkCollisions(currentId);
        }
    }
    
    handleDropdownHide(currentId, event) {
        console.log(`📁 Закрывается dropdown: ${currentId}`);
        
        this.dropdowns[currentId].isOpen = false;
        this.resetPosition(currentId);
        this.clearConflictMarkers();
    }
    
    applyStrategy(strategy, currentId, openDropdowns) {
        switch (strategy) {
            case 'close-others':
                this.closeOtherDropdowns(currentId);
                break;
                
            case 'shift-down':
                this.shiftDropdownsDown(openDropdowns);
                break;
                
            case 'shift-smart':
                this.applySmartShift(currentId, openDropdowns);
                break;
                
            default:
                // Стандартное поведение Bootstrap
                break;
        }
    }
    
    closeOtherDropdowns(exceptId) {
        console.log('🔄 Закрываем другие dropdown');
        
        Object.keys(this.dropdowns).forEach(id => {
            if (id !== exceptId && this.dropdowns[id].isOpen) {
                const bsDropdown = bootstrap.Dropdown.getInstance(this.dropdowns[id].toggle);
                if (bsDropdown) {
                    bsDropdown.hide();
                }
            }
        });
    }
    
    shiftDropdownsDown(dropdownIds) {
        console.log('⬇️ Смещаем dropdown вниз');
        
        dropdownIds.forEach((id, index) => {
            const dropdown = this.dropdowns[id];
            if (dropdown && dropdown.menu) {
                const shiftAmount = 15 + (index * 10); // Увеличиваем смещение для каждого
                this.applyTransform(dropdown.menu, `translateY(${shiftAmount}px)`);
                this.markAsShifted(dropdown.element);
            }
        });
    }
    
    applySmartShift(currentId, openDropdowns) {
        console.log('🧠 Применяем умное смещение');
        
        const currentDropdown = this.dropdowns[currentId];
        if (!currentDropdown) return;
        
        // Определяем позицию текущего dropdown
        const currentRect = currentDropdown.toggle.getBoundingClientRect();
        const isRightSide = currentRect.left > window.innerWidth / 2;
        
        openDropdowns.forEach(id => {
            const dropdown = this.dropdowns[id];
            if (!dropdown) return;
            
            const rect = dropdown.toggle.getBoundingClientRect();
            const distance = Math.abs(rect.left - currentRect.left);
            
            if (distance < 200) { // Близко расположены
                if (isRightSide) {
                    // Если справа - смещаем влево и вниз
                    this.applyTransform(dropdown.menu, 'translate(-25px, 15px)');
                } else {
                    // Если слева - смещаем вправо и вниз
                    this.applyTransform(dropdown.menu, 'translate(25px, 15px)');
                }
            } else {
                // Далеко - просто смещаем вниз
                this.applyTransform(dropdown.menu, 'translateY(20px)');
            }
            
            this.markAsShifted(dropdown.element);
        });
    }
    
    checkCollisions(currentId) {
        const currentDropdown = this.dropdowns[currentId];
        if (!currentDropdown || !currentDropdown.menu) return;
        
        const currentRect = currentDropdown.menu.getBoundingClientRect();
        const openDropdowns = this.getOpenDropdowns().filter(id => id !== currentId);
        
        openDropdowns.forEach(id => {
            const dropdown = this.dropdowns[id];
            if (!dropdown || !dropdown.menu) return;
            
            const rect = dropdown.menu.getBoundingClientRect();
            
            if (this.isColliding(currentRect, rect)) {
                console.log(`💥 Коллизия между ${currentId} и ${id}`);
                this.resolveCollision(currentId, id);
            }
        });
    }
    
    isColliding(rect1, rect2) {
        const buffer = 5; // Буферная зона в пикселях
        return !(rect1.right < rect2.left - buffer || 
                rect1.left > rect2.right + buffer || 
                rect1.bottom < rect2.top - buffer || 
                rect1.top > rect2.bottom + buffer);
    }
    
    resolveCollision(id1, id2) {
        const dropdown2 = this.dropdowns[id2];
        if (!dropdown2 || !dropdown2.menu) return;
        
        // Смещаем второй dropdown дальше
        const currentTransform = dropdown2.menu.style.transform || '';
        const additionalShift = currentTransform.includes('translateY') ? 
            'translate(0, 35px)' : 'translateY(25px)';
            
        this.applyTransform(dropdown2.menu, additionalShift);
        this.markAsConflicted(dropdown2.element);
    }
    
    applyTransform(element, transform) {
        element.style.transform = transform;
        element.style.transition = 'transform 0.3s ease';
    }
    
    resetPosition(id) {
        const dropdown = this.dropdowns[id];
        if (!dropdown || !dropdown.menu) return;
        
        // Сбрасываем позицию
        dropdown.menu.style.transform = '';
        dropdown.menu.style.transition = '';
        
        // Убираем маркеры
        this.removeShiftedMarker(dropdown.element);
        this.removeConflictMarker(dropdown.element);
    }
    
    markAsShifted(element) {
        element.classList.add('dropdown-shifted');
    }
    
    removeShiftedMarker(element) {
        element.classList.remove('dropdown-shifted');
    }
    
    markAsConflicted(element) {
        element.classList.add('dropdown-conflict');
    }
    
    removeConflictMarker(element) {
        element.classList.remove('dropdown-conflict');
    }
    
    clearConflictMarkers() {
        Object.keys(this.dropdowns).forEach(id => {
            const dropdown = this.dropdowns[id];
            if (dropdown) {
                this.removeShiftedMarker(dropdown.element);
                this.removeConflictMarker(dropdown.element);
            }
        });
    }
    
    getCurrentStrategy() {
        const width = window.innerWidth;
        
        if (width < 576) return this.strategies.xs;
        if (width < 768) return this.strategies.sm;
        if (width < 992) return this.strategies.md;
        return this.strategies.lg;
    }
    
    isMobile() {
        return window.innerWidth < 992; // Bootstrap lg breakpoint
    }
    
    getOpenDropdowns() {
        return Object.keys(this.dropdowns).filter(id => this.dropdowns[id].isOpen);
    }
    
    handleResize() {
        // Сбрасываем все позиции при изменении размера
        Object.keys(this.dropdowns).forEach(id => {
            this.resetPosition(id);
        });
        
        console.log('📱 Размер окна изменён, позиции сброшены');
    }
    
    handleOutsideClick(event) {
        // Проверяем, был ли клик вне всех dropdown
        const isInsideDropdown = Object.keys(this.dropdowns).some(id => {
            const dropdown = this.dropdowns[id];
            return dropdown.element.contains(event.target);
        });
        
        if (!isInsideDropdown) {
            // Закрываем все открытые dropdown
            this.getOpenDropdowns().forEach(id => {
                const bsDropdown = bootstrap.Dropdown.getInstance(this.dropdowns[id].toggle);
                if (bsDropdown) {
                    bsDropdown.hide();
                }
            });
        }
    }
    
    // Публичные методы для внешнего использования
    forceCloseAll() {
        console.log('🔄 Принудительное закрытие всех dropdown');
        this.getOpenDropdowns().forEach(id => {
            const bsDropdown = bootstrap.Dropdown.getInstance(this.dropdowns[id].toggle);
            if (bsDropdown) {
                bsDropdown.hide();
            }
        });
    }
    
    getStatus() {
        return {
            total: Object.keys(this.dropdowns).length,
            open: this.getOpenDropdowns().length,
            shifted: Object.keys(this.dropdowns).filter(id => 
                this.dropdowns[id].element.classList.contains('dropdown-shifted')
            ).length,
            conflicts: Object.keys(this.dropdowns).filter(id => 
                this.dropdowns[id].element.classList.contains('dropdown-conflict')
            ).length,
            strategy: this.getCurrentStrategy(),
            isMobile: this.isMobile()
        };
    }
    
    // Отладочная информация
    debug() {
        console.log('🔍 Отладочная информация SmartDropdownManager:');
        console.log('Dropdown элементы:', this.dropdowns);
        console.log('Текущий статус:', this.getStatus());
        console.log('Открытые dropdown:', this.getOpenDropdowns());
    }
}

// CSS стили для визуальных индикаторов
const smartDropdownStyles = `
    /* Стили для смещённых dropdown */
    .dropdown-shifted .dropdown-toggle::after {
        border-left-color: orange !important;
        border-right-color: orange !important;
        border-top-color: orange !important;
    }
    
    .dropdown-shifted {
        position: relative;
    }
    
    .dropdown-shifted::before {
        content: '';
        position: absolute;
        top: 0;
        right: -3px;
        width: 2px;
        height: 100%;
        background: linear-gradient(45deg, orange, #ff6b35);
        border-radius: 1px;
        z-index: 1000;
        opacity: 0.7;
    }
    
    /* Стили для конфликтующих dropdown */
    .dropdown-conflict .dropdown-toggle {
        background-color: rgba(255, 193, 7, 0.1) !important;
        border-radius: 4px;
    }
    
    .dropdown-conflict .dropdown-toggle::after {
        border-left-color: #dc3545 !important;
        border-right-color: #dc3545 !important;
        border-top-color: #dc3545 !important;
    }
    
    /* Плавные анимации для dropdown меню */
    .dropdown-menu {
        transition: transform 0.3s ease, opacity 0.2s ease;
    }
    
    .dropdown-menu.show {
        animation: dropdownFadeIn 0.3s ease;
    }
    
    @keyframes dropdownFadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Улучшенные стили для мобильных устройств */
    @media (max-width: 991.98px) {
        .dropdown-menu {
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
            border-radius: 0.5rem !important;
        }
        
        .dropdown-item {
            padding: 0.7rem 1rem !important;
            transition: all 0.2s ease;
        }
        
        .dropdown-item:hover {
            background-color: rgba(0, 123, 255, 0.1) !important;
            transform: translateX(5px);
        }
    }
`;

// Функция для добавления стилей
function addSmartDropdownStyles() {
    const styleId = 'smart-dropdown-styles';
    
    // Проверяем, не добавлены ли уже стили
    if (document.getElementById(styleId)) {
        return;
    }
    
    const styleElement = document.createElement('style');
    styleElement.id = styleId;
    styleElement.textContent = smartDropdownStyles;
    document.head.appendChild(styleElement);
    
    console.log('🎨 Стили SmartDropdown добавлены');
}

// Глобальная переменная для доступа к менеджеру
let smartDropdownManager = null;

// Автоматическая инициализация
(function() {
    // Функция инициализации
    function initSmartDropdown() {
        addSmartDropdownStyles();
        smartDropdownManager = new SmartDropdownManager();
        
        // Делаем доступным глобально для отладки
        window.smartDropdownManager = smartDropdownManager;
        
        console.log('🚀 SmartDropdownManager готов к работе!');
        console.log('💡 Для отладки используйте: window.smartDropdownManager.debug()');
    }
    
    // Инициализируем после загрузки DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSmartDropdown);
    } else {
        initSmartDropdown();
    }
})();

// Экспорт для использования в модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SmartDropdownManager;
}
