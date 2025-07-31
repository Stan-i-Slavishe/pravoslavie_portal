#!/usr/bin/env python
"""
Скрипт для исправления логики отображения кнопок покупки в book_detail.html
"""

def fix_book_detail_template():
    template_path = 'E:/pravoslavie_portal/templates/books/book_detail.html'
    
    try:
        # Читаем файл
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Находим блок с кнопками и заменяем его
        start_marker = '<!-- Кнопки действий -->'
        end_marker = '</div>'
        
        # Ищем начало блока кнопок
        start_pos = content.find(start_marker)
        if start_pos == -1:
            print("❌ Не найден маркер начала блока кнопок")
            return False
        
        # Ищем конец блока (первое появление </div> после кнопок)
        # Нужно найти конец div.book-actions
        search_start = start_pos
        div_count = 0
        end_pos = -1
        
        # Ищем <div class="book-actions">
        actions_start = content.find('<div class="book-actions">', search_start)
        if actions_start == -1:
            print("❌ Не найден div с классом book-actions")
            return False
        
        # Начинаем поиск с открывающего тега
        i = actions_start
        while i < len(content):
            if content[i:i+4] == '<div':
                div_count += 1
            elif content[i:i+6] == '</div>':
                div_count -= 1
                if div_count == 0:
                    end_pos = i + 6
                    break
            i += 1
        
        if end_pos == -1:
            print("❌ Не найден конец блока div.book-actions")
            return False
        
        print(f"✅ Найден блок кнопок: позиции {actions_start} - {end_pos}")
        
        # Новый блок кнопок
        new_buttons_block = '''<!-- Кнопки действий - ИСПРАВЛЕННАЯ ВЕРСИЯ -->
                <div class="book-actions">
                    {% if user.is_authenticated %}
                        <!-- Проверяем, может ли пользователь читать книгу -->
                        {% if book.is_free or user_can_read %}
                            <!-- Кнопки для чтения (если книга бесплатная или уже куплена) -->
                            <a href="{% url 'books:read' book.slug %}" class="btn-read">
                                <i class="bi bi-book-open"></i>
                                {% if reading_session %}
                                    Продолжить чтение
                                {% else %}
                                    Читать книгу
                                {% endif %}
                            </a>
                            
                            <!-- Современный reader (только для PDF) -->
                            {% if book.format == 'pdf' and book.file %}
                            <a href="{% url 'books:modern_reader' book.slug %}" class="btn" 
                               style="background: linear-gradient(135deg, #FF6B9D, #C73650); 
                                      border: none; 
                                      color: white; 
                                      padding: 12px 24px; 
                                      border-radius: 8px; 
                                      font-weight: 500; 
                                      transition: all 0.3s ease; 
                                      text-decoration: none; 
                                      display: inline-flex; 
                                      align-items: center; 
                                      gap: 8px;
                                      width: 100%;
                                      justify-content: center;"
                               onmouseover="this.style.background='linear-gradient(135deg, #C73650, #FF6B9D)'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(255, 107, 157, 0.3)'"
                               onmouseout="this.style.background='linear-gradient(135deg, #FF6B9D, #C73650)'; this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                                <i class="bi bi-tablet-landscape"></i>
                                Читать на весь экран
                            </a>
                            {% endif %}
                        {% else %}
                            <!-- Кнопка покупки для авторизованных пользователей (если книга платная и не куплена) -->
                            <a href="{% url 'shop:catalog' %}?book={{ book.id }}" class="btn-purchase">
                                <i class="bi bi-cart-plus"></i>
                                Купить за {{ book.price }} ₽
                            </a>
                        {% endif %}
                    {% else %}
                        <!-- Для неавторизованных пользователей -->
                        {% if book.is_free %}
                            <a href="{% url 'account_login' %}?next={% url 'books:read' book.slug %}" class="btn-read">
                                <i class="bi bi-book-open"></i>
                                Войти для чтения
                            </a>
                        {% else %}
                            <!-- Показать цену и предложить войти -->
                            <div class="book-price-info mb-3">
                                <h4 class="text-center mb-2">
                                    <span class="badge bg-warning text-dark fs-5">{{ book.price }} ₽</span>
                                </h4>
                            </div>
                            <a href="{% url 'account_login' %}" class="btn-purchase">
                                <i class="bi bi-person-plus"></i>
                                Войти для покупки
                            </a>
                        {% endif %}
                    {% endif %}

                    <!-- Кнопка скачивания (только если доступна) -->
                    {% if book.file and user.is_authenticated %}
                        {% if book.is_free or user_can_read %}
                        <a href="{% url 'books:download' book.id %}" class="btn-download" 
                           style="background: linear-gradient(135deg, #28a745, #20692b);
                                  border: none;
                                  color: white;
                                  padding: 12px 24px;
                                  border-radius: 8px;
                                  font-weight: 500;
                                  transition: all 0.3s ease;
                                  text-decoration: none;
                                  display: inline-flex;
                                  align-items: center;
                                  gap: 8px;
                                  flex: 1;
                                  justify-content: center;"
                           onmouseover="this.style.background='linear-gradient(135deg, #20692b, #28a745)'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(40, 167, 69, 0.3)'"
                           onmouseout="this.style.background='linear-gradient(135deg, #28a745, #20692b)'; this.style.transform='translateY(0)'; this.style.boxShadow='none'">
                            <i class="bi bi-download"></i>
                            Скачать
                        </a>
                        {% endif %}
                    {% endif %}

                    <!-- Кнопка избранного (только для авторизованных пользователей) -->
                    {% if user.is_authenticated %}
                        <button class="btn-favorite {% if is_favorite %}active{% endif %}" 
                                style="background: {% if is_favorite %}linear-gradient(135deg, #ffc107, #e0a800){% else %}transparent{% endif %};
                                       border: 2px solid #ffc107;
                                       color: {% if is_favorite %}white{% else %}#ffc107{% endif %};
                                       padding: 10px 20px;
                                       border-radius: 8px;
                                       font-weight: 500;
                                       transition: all 0.3s ease;
                                       display: inline-flex;
                                       align-items: center;
                                       gap: 8px;
                                       cursor: pointer;
                                       flex: 1;
                                       justify-content: center;"
                                onmouseover="this.style.background='linear-gradient(135deg, #ffc107, #e0a800)'; this.style.color='white'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 12px rgba(255, 193, 7, 0.3)'"
                                onmouseout="this.style.background='{% if is_favorite %}linear-gradient(135deg, #ffc107, #e0a800){% else %}transparent{% endif %}'; this.style.color='{% if is_favorite %}white{% else %}#ffc107{% endif %}'; this.style.transform='translateY(0)'; this.style.boxShadow='none'"
                                onclick="toggleFavorite({{ book.id }}, event)">
                            <i class="bi bi-bookmark{% if is_favorite %}-fill{% endif %}"></i>
                            <span class="favorite-text">
                                {% if is_favorite %}В избранном{% else %}В избранное{% endif %}
                            </span>
                        </button>
                    {% endif %}
                </div>'''
        
        # Заменяем блок
        new_content = content[:actions_start] + new_buttons_block + content[end_pos:]
        
        # Создаем резервную копию
        backup_path = template_path + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Создана резервная копия: {backup_path}")
        
        # Записываем исправленный файл
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Шаблон book_detail.html успешно исправлен!")
        print("\n📋 Что изменилось:")
        print("   1. Исправлена логика отображения кнопки покупки для авторизованных пользователей")
        print("   2. Добавлен блок с ценой для неавторизованных пользователей")
        print("   3. Улучшена структура условий if/else")
        print("\n🔍 Теперь кнопка 'Купить за X ₽' будет отображаться когда:")
        print("   - Пользователь авторизован")
        print("   - Книга платная (is_free=False)")
        print("   - Пользователь не купил книгу (user_can_read=False)")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == '__main__':
    print("🔧 ИСПРАВЛЕНИЕ ЛОГИКИ КНОПОК ПОКУПКИ В BOOK_DETAIL.HTML")
    print("=" * 60)
    
    if fix_book_detail_template():
        print("\n✅ Исправление завершено успешно!")
        print("\n🚀 Перезапустите сервер Django для применения изменений:")
        print("   python manage.py runserver")
    else:
        print("\n❌ Исправление не удалось.")
