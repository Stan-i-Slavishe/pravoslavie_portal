// Упрощенный JavaScript для админки товаров (ИСПРАВЛЕННАЯ ВЕРСИЯ)

(function($) {
    'use strict';
    
    $(document).ready(function() {
        console.log('🎯 Product Admin JS загружен!');
        
        // Функция для скрытия/показа полей связи с контентом
        function toggleContentFields() {
            const productType = $('#id_product_type').val();
            console.log('Выбран тип товара:', productType);
            
            // Скрываем все поля связи
            $('.field-book_id, .field-audio_id, .field-subscription_id, .field-fairy_tale_template_id').hide();
            
            // Показываем только нужное поле
            switch(productType) {
                case 'book':
                    $('.field-book_id').show();
                    console.log('Показано поле книги');
                    break;
                case 'audio':
                    $('.field-audio_id').show();
                    break;
                case 'subscription':
                    $('.field-subscription_id').show();
                    break;
                case 'fairy_tale':
                    $('.field-fairy_tale_template_id').show();
                    // Показываем настройки для сказок
                    $('.field-requires_personalization, .field-has_audio_option, .field-audio_option_price, .field-has_illustration_option, .field-illustration_option_price').closest('fieldset').show();
                    break;
                default:
                    // Скрываем настройки сказок если тип не "fairy_tale"
                    if (productType !== 'fairy_tale') {
                        $('.field-requires_personalization').closest('fieldset').hide();
                    }
            }
        }
        
        // Функция для автозаполнения полей на основе выбранного контента
        function autoFillFromContent() {
            const productType = $('#id_product_type').val();
            let contentSelect;
            
            switch(productType) {
                case 'book':
                    contentSelect = $('#id_book_id');
                    break;
                case 'audio':
                    contentSelect = $('#id_audio_id');
                    break;
                case 'subscription':
                    contentSelect = $('#id_subscription_id');
                    break;
                case 'fairy_tale':
                    contentSelect = $('#id_fairy_tale_template_id');
                    break;
            }
            
            if (contentSelect && contentSelect.val()) {
                const selectedOption = contentSelect.find('option:selected').text();
                console.log('Выбран контент:', selectedOption);
                
                if (selectedOption && selectedOption !== '-- Выберите --') {
                    // Извлекаем название из текста опции (до первой скобки)
                    const contentTitle = selectedOption.split('(')[0].trim();
                    
                    // Автозаполняем название товара, если оно пустое
                    if (!$('#id_title').val()) {
                        $('#id_title').val(contentTitle);
                        console.log('Автозаполнено название:', contentTitle);
                    }
                }
            }
        }
        
        // Обработчики событий
        $('#id_product_type').change(function() {
            console.log('Изменен тип товара');
            toggleContentFields();
            autoFillFromContent();
        });
        
        // Обработчики для автозаполнения при выборе контента
        $('#id_book_id, #id_audio_id, #id_subscription_id, #id_fairy_tale_template_id').change(function() {
            console.log('Изменен выбор контента');
            autoFillFromContent();
        });
        
        // Начальная инициализация
        toggleContentFields();
        
        // Добавляем стили для улучшения визуала
        $('<style>')
            .prop('type', 'text/css')
            .html(`
                .field-content_preview {
                    margin-top: 15px;
                }
                .content-preview-box {
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 15px;
                    margin: 10px 0;
                    background: #f9f9f9;
                }
                .product-type-hint {
                    font-size: 12px;
                    color: #666;
                    margin-top: 5px;
                    padding: 5px 10px;
                    background: #f0f8ff;
                    border-radius: 3px;
                    border-left: 3px solid #007cba;
                }
            `)
            .appendTo('head');
        
        // Добавляем подсказку
        if ($('#id_product_type').length) {
            $('#id_product_type').after('<div class="product-type-hint">💡 Выберите тип товара, чтобы увидеть соответствующие поля</div>');
        }
        
        console.log('✅ Product Admin JS инициализирован');
    });
    
})(django.jQuery);
