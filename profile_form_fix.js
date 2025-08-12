/* JAVASCRIPT ИСПРАВЛЕНИЕ ПОЛЕЙ ФОРМЫ ПРОФИЛЯ */
/* Добавьте этот код в конец блока <script> в profile_edit.html */

// Принудительное исправление кликабельности полей
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Применяем исправление полей формы...');
    
    // Находим все поля
    const fields = document.querySelectorAll('input, textarea, select');
    
    fields.forEach((field, index) => {
        // Принудительно убираем блокировки
        field.style.pointerEvents = 'auto';
        field.style.position = 'relative';
        field.style.zIndex = '100';
        
        // Добавляем обработчики
        field.addEventListener('mousedown', function(e) {
            e.stopPropagation();
            this.focus();
        });
        
        field.addEventListener('click', function(e) {
            e.stopPropagation();
            this.focus();
        });
        
        console.log(`✓ Исправлено поле ${index + 1}: ${field.name || field.id || 'unnamed'}`);
    });
    
    // Убираем блокировки с контейнеров
    const containers = document.querySelectorAll('.form-group, .mb-3, .card-body');
    containers.forEach(container => {
        container.style.pointerEvents = 'auto';
    });
    
    console.log(`✅ Исправление применено к ${fields.length} полям`);
});

// Дополнительная проверка через 500мс
setTimeout(() => {
    const problematicFields = document.querySelectorAll('input[style*="pointer-events: none"], textarea[style*="pointer-events: none"], select[style*="pointer-events: none"]');
    
    if (problematicFields.length > 0) {
        console.warn(`⚠️ Найдено ${problematicFields.length} заблокированных полей, исправляем...`);
        
        problematicFields.forEach(field => {
            field.style.pointerEvents = 'auto';
            field.style.zIndex = '100';
        });
    }
}, 500);
