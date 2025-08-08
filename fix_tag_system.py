#!/usr/bin/env python3
"""
Скрипт для исправления TagDetailView в core/views.py
"""

import os
import sys

def fix_tag_detail_view():
    """Исправляет TagDetailView для поиска контента по тегам"""
    
    views_path = r'E:\pravoslavie_portal\core\views.py'
    
    # Читаем текущий файл
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Добавляем импорты в начало файла
    imports_to_add = '''# Импортируем модели из других приложений для поиска контента
try:
    from stories.models import Story
except ImportError:
    Story = None

try:
    from books.models import Book
except ImportError:
    Book = None

try:
    from fairy_tales.models import FairyTale
except ImportError:
    FairyTale = None

try:
    from audio.models import AudioTrack
except ImportError:
    AudioTrack = None

'''
    
    # Заменяем строку импортов
    old_imports = 'from django.http import Http404'
    new_imports = '''from django.http import Http404
from django.db.models import Count, Q'''
    
    content = content.replace(old_imports, new_imports)
    
    # Добавляем импорты моделей после основных импортов
    insert_position = content.find('from .forms import ContactForm') + len('from .forms import ContactForm')
    content = content[:insert_position] + '\n\n' + imports_to_add + content[insert_position:]
    
    # Заменяем старый TagDetailView
    old_tag_view = '''class TagDetailView(TemplateView):
    template_name = 'core/tag_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tag = get_object_or_404(
            Tag, 
            slug=kwargs['slug'], 
            is_active=True
        )
        
        context['tag'] = tag
        context['title'] = f'Тег: {tag.name}'
        
        # В будущем здесь будем загружать контент с этим тегом
        context['content_items'] = []
        
        return context'''
    
    new_tag_view = '''class TagDetailView(TemplateView):
    template_name = 'core/tag_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tag = get_object_or_404(
            Tag, 
            slug=kwargs['slug'], 
            is_active=True
        )
        
        context['tag'] = tag
        context['title'] = f'Тег: {tag.name}'
        
        # Собираем контент из всех приложений
        content_items = []
        
        # 1. Видео-рассказы
        if Story:
            stories = Story.objects.filter(
                tags=tag, 
                is_published=True
            ).select_related('category').order_by('-created_at')[:10]
            
            for story in stories:
                content_items.append({
                    'type': 'story',
                    'object': story,
                    'title': story.title,
                    'description': story.description,
                    'url': f'/stories/{story.slug}/',
                    'created_at': story.created_at,
                    'category': story.category.name if story.category else None,
                    'views_count': getattr(story, 'views_count', 0),
                    'image': story.thumbnail_url if hasattr(story, 'thumbnail_url') else None,
                })
        
        # 2. Книги
        if Book:
            books = Book.objects.filter(
                tags=tag
            ).select_related('category').order_by('-created_at')[:10]
            
            for book in books:
                content_items.append({
                    'type': 'book',
                    'object': book,
                    'title': book.title,
                    'description': book.description,
                    'url': f'/books/{book.slug}/',
                    'created_at': book.created_at,
                    'category': book.category.name if book.category else None,
                    'price': getattr(book, 'price', None),
                    'image': book.cover_image.url if book.cover_image else None,
                })
        
        # 3. Терапевтические сказки
        if FairyTale:
            fairy_tales = FairyTale.objects.filter(
                tags=tag
            ).select_related('category').order_by('-created_at')[:10]
            
            for fairy_tale in fairy_tales:
                content_items.append({
                    'type': 'fairy_tale',
                    'object': fairy_tale,
                    'title': fairy_tale.title,
                    'description': fairy_tale.description,
                    'url': f'/fairy-tales/{fairy_tale.slug}/',
                    'created_at': fairy_tale.created_at,
                    'category': fairy_tale.category.name if fairy_tale.category else None,
                    'age_group': getattr(fairy_tale, 'age_group', None),
                    'image': getattr(fairy_tale, 'cover_image', None),
                })
        
        # 4. Аудио
        if AudioTrack:
            audio_tracks = AudioTrack.objects.filter(
                tags=tag
            ).select_related('category').order_by('-created_at')[:10]
            
            for track in audio_tracks:
                content_items.append({
                    'type': 'audio',
                    'object': track,
                    'title': track.title,
                    'description': getattr(track, 'description', ''),
                    'url': f'/audio/{track.slug}/',
                    'created_at': track.created_at,
                    'category': track.category.name if track.category else None,
                    'duration': getattr(track, 'duration', None),
                    'image': getattr(track, 'cover_image', None),
                })
        
        # Сортируем по дате создания (новые сначала)
        content_items.sort(key=lambda x: x['created_at'], reverse=True)
        
        context['content_items'] = content_items
        context['total_items'] = len(content_items)
        
        # Группируем по типам для статистики
        context['stats'] = {
            'stories': len([item for item in content_items if item['type'] == 'story']),
            'books': len([item for item in content_items if item['type'] == 'book']),
            'fairy_tales': len([item for item in content_items if item['type'] == 'fairy_tale']),
            'audio': len([item for item in content_items if item['type'] == 'audio']),
        }
        
        return context'''
    
    # Выполняем замену
    content = content.replace(old_tag_view, new_tag_view)
    
    # Записываем обратно в файл
    with open(views_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ TagDetailView успешно обновлен!")
    print(f"📁 Файл: {views_path}")

def update_template():
    """Обновляет шаблон tag_detail.html"""
    
    template_path = r'E:\pravoslavie_portal\templates\core\tag_detail.html'
    
    new_template_content = '''{% extends 'base.html' %}
{% load static %}

{% block title %}{{ tag.name }} - Православный портал{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <!-- Хлебные крошки -->
        <nav aria-label="breadcrumb" class="mb-4">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="{% url 'core:home' %}">Главная</a></li>
                <li class="breadcrumb-item"><a href="{% url 'core:tags' %}">Теги</a></li>
                <li class="breadcrumb-item active">{{ tag.name }}</li>
            </ol>
        </nav>
        
        <!-- Заголовок тега -->
        <div class="d-flex align-items-center mb-4">
            <div>
                <h1 class="mb-2">
                    <i class="bi bi-tag me-2"></i>
                    {{ tag.name }}
                </h1>
                <span class="badge rounded-pill" 
                      style="background-color: {{ tag.color }}; font-size: 16px; padding: 8px 12px;">
                    #{{ tag.slug }}
                </span>
                {% if total_items %}
                    <span class="badge bg-secondary ms-2">{{ total_items }} материал{{ total_items|pluralize:"ов" }}</span>
                {% endif %}
            </div>
        </div>
        
        <!-- Описание тега -->
        {% if tag.description %}
            <div class="alert alert-info mb-4">
                <i class="bi bi-info-circle me-2"></i>
                {{ tag.description }}
            </div>
        {% endif %}
        
        <!-- Статистика по типам контента -->
        {% if total_items %}
            <div class="row mb-4">
                {% if stats.stories %}
                    <div class="col-md-3">
                        <div class="card text-center bg-primary text-white">
                            <div class="card-body">
                                <i class="bi bi-play-circle display-6"></i>
                                <h5 class="card-title">{{ stats.stories }}</h5>
                                <p class="card-text">Видео-рассказы</p>
                            </div>
                        </div>
                    </div>
                {% endif %}
                {% if stats.books %}
                    <div class="col-md-3">
                        <div class="card text-center bg-success text-white">
                            <div class="card-body">
                                <i class="bi bi-book display-6"></i>
                                <h5 class="card-title">{{ stats.books }}</h5>
                                <p class="card-text">Книги</p>
                            </div>
                        </div>
                    </div>
                {% endif %}
                {% if stats.fairy_tales %}
                    <div class="col-md-3">
                        <div class="card text-center bg-info text-white">
                            <div class="card-body">
                                <i class="bi bi-star display-6"></i>
                                <h5 class="card-title">{{ stats.fairy_tales }}</h5>
                                <p class="card-text">Сказки</p>
                            </div>
                        </div>
                    </div>
                {% endif %}
                {% if stats.audio %}
                    <div class="col-md-3">
                        <div class="card text-center bg-warning text-white">
                            <div class="card-body">
                                <i class="bi bi-music-note display-6"></i>
                                <h5 class="card-title">{{ stats.audio }}</h5>
                                <p class="card-text">Аудио</p>
                            </div>
                        </div>
                    </div>
                {% endif %}
            </div>
        {% endif %}
        
        <!-- Контент с тегом -->
        <div class="row">
            <div class="col-lg-8">
                {% if content_items %}
                    <div class="row g-4">
                        {% for item in content_items %}
                            <div class="col-md-6">
                                <div class="card h-100 shadow-sm">
                                    {% if item.image %}
                                        <img src="{{ item.image }}" class="card-img-top" alt="{{ item.title }}" style="height: 200px; object-fit: cover;">
                                    {% endif %}
                                    
                                    <div class="card-body d-flex flex-column">
                                        <!-- Тип контента -->
                                        <div class="mb-2">
                                            {% if item.type == 'story' %}
                                                <span class="badge bg-primary">
                                                    <i class="bi bi-play-circle me-1"></i>Видео-рассказ
                                                </span>
                                            {% elif item.type == 'book' %}
                                                <span class="badge bg-success">
                                                    <i class="bi bi-book me-1"></i>Книга
                                                </span>
                                                {% if item.price %}
                                                    <span class="badge bg-warning text-dark">{{ item.price }} ₽</span>
                                                {% endif %}
                                            {% elif item.type == 'fairy_tale' %}
                                                <span class="badge bg-info">
                                                    <i class="bi bi-star me-1"></i>Сказка
                                                </span>
                                                {% if item.age_group %}
                                                    <span class="badge bg-secondary">{{ item.age_group }}</span>
                                                {% endif %}
                                            {% elif item.type == 'audio' %}
                                                <span class="badge bg-warning">
                                                    <i class="bi bi-music-note me-1"></i>Аудио
                                                </span>
                                                {% if item.duration %}
                                                    <span class="badge bg-secondary">{{ item.duration }}</span>
                                                {% endif %}
                                            {% endif %}
                                            
                                            {% if item.category %}
                                                <span class="badge bg-light text-dark">{{ item.category }}</span>
                                            {% endif %}
                                        </div>
                                        
                                        <!-- Заголовок и описание -->
                                        <h5 class="card-title">{{ item.title }}</h5>
                                        <p class="card-text flex-grow-1">{{ item.description|truncatewords:20 }}</p>
                                        
                                        <!-- Дополнительная информация -->
                                        <div class="text-muted small mb-3">
                                            <i class="bi bi-calendar me-1"></i>
                                            {{ item.created_at|date:"d.m.Y" }}
                                            {% if item.views_count %}
                                                <span class="ms-2">
                                                    <i class="bi bi-eye me-1"></i>{{ item.views_count }}
                                                </span>
                                            {% endif %}
                                        </div>
                                        
                                        <!-- Кнопка -->
                                        <div class="mt-auto">
                                            <a href="{{ item.url }}" class="btn btn-outline-primary btn-sm w-100">
                                                {% if item.type == 'story' %}
                                                    <i class="bi bi-play me-1"></i>Смотреть
                                                {% elif item.type == 'book' %}
                                                    <i class="bi bi-book-half me-1"></i>Читать
                                                {% elif item.type == 'fairy_tale' %}
                                                    <i class="bi bi-star me-1"></i>Читать сказку
                                                {% elif item.type == 'audio' %}
                                                    <i class="bi bi-play me-1"></i>Слушать
                                                {% else %}
                                                    Подробнее
                                                {% endif %}
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                {% else %}
                    <div class="text-center py-5">
                        <i class="bi bi-search display-1 text-muted"></i>
                        <h3 class="mt-3">Контент не найден</h3>
                        <p class="text-muted">Материалы с тегом "{{ tag.name }}" пока отсутствуют</p>
                        
                        <div class="mt-4">
                            <p>Попробуйте найти интересующий вас контент в наших разделах:</p>
                            <div class="d-flex gap-2 justify-content-center flex-wrap">
                                <a href="{% url 'stories:list' %}" class="btn btn-outline-primary btn-sm">
                                    <i class="bi bi-play-circle"></i> Видео-рассказы
                                </a>
                                <a href="{% url 'books:list' %}" class="btn btn-outline-success btn-sm">
                                    <i class="bi bi-book"></i> Библиотека
                                </a>
                                <a href="{% url 'audio:list' %}" class="btn btn-outline-info btn-sm">
                                    <i class="bi bi-music-note"></i> Аудио
                                </a>
                                <a href="{% url 'fairy_tales:list' %}" class="btn btn-outline-warning btn-sm">
                                    <i class="bi bi-star"></i> Сказки
                                </a>
                            </div>
                        </div>
                    </div>
                {% endif %}
            </div>
            
            <!-- Боковая панель -->
            <div class="col-lg-4">
                <div class="card bg-light">
                    <div class="card-header">
                        <h5 class="mb-0">О теге</h5>
                    </div>
                    <div class="card-body">
                        <table class="table table-sm table-borderless">
                            <tr>
                                <td><strong>Тег:</strong></td>
                                <td>{{ tag.name }}</td>
                            </tr>
                            <tr>
                                <td><strong>Slug:</strong></td>
                                <td><code>{{ tag.slug }}</code></td>
                            </tr>
                            <tr>
                                <td><strong>Материалов:</strong></td>
                                <td>{{ total_items|default:0 }}</td>
                            </tr>
                            <tr>
                                <td><strong>Создан:</strong></td>
                                <td>{{ tag.created_at|date:"d.m.Y" }}</td>
                            </tr>
                        </table>
                    </div>
                </div>
                
                <!-- Быстрые ссылки -->
                {% if total_items %}
                    <div class="card mt-4">
                        <div class="card-header">
                            <h5 class="mb-0">Быстрые ссылки</h5>
                        </div>
                        <div class="card-body">
                            {% if stats.stories %}
                                <a href="{% url 'stories:list' %}?tag={{ tag.slug }}" class="btn btn-primary btn-sm w-100 mb-2">
                                    <i class="bi bi-play-circle me-1"></i>
                                    Только видео-рассказы ({{ stats.stories }})
                                </a>
                            {% endif %}
                            {% if stats.books %}
                                <a href="{% url 'books:list' %}?tag={{ tag.slug }}" class="btn btn-success btn-sm w-100 mb-2">
                                    <i class="bi bi-book me-1"></i>
                                    Только книги ({{ stats.books }})
                                </a>
                            {% endif %}
                            {% if stats.fairy_tales %}
                                <a href="{% url 'fairy_tales:list' %}?tag={{ tag.slug }}" class="btn btn-info btn-sm w-100 mb-2">
                                    <i class="bi bi-star me-1"></i>
                                    Только сказки ({{ stats.fairy_tales }})
                                </a>
                            {% endif %}
                            {% if stats.audio %}
                                <a href="{% url 'audio:list' %}?tag={{ tag.slug }}" class="btn btn-warning btn-sm w-100 mb-2">
                                    <i class="bi bi-music-note me-1"></i>
                                    Только аудио ({{ stats.audio }})
                                </a>
                            {% endif %}
                        </div>
                    </div>
                {% endif %}
                
                <!-- Похожие теги -->
                <div class="card mt-4">
                    <div class="card-header">
                        <h5 class="mb-0">Популярные теги</h5>
                    </div>
                    <div class="card-body">
                        <div class="tag-cloud">
                            <a href="{% url 'core:tags' %}" class="btn btn-outline-secondary btn-sm">
                                <i class="bi bi-tags"></i> Все теги
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''
    
    # Записываем новый шаблон
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(new_template_content)
    
    print("✅ Шаблон tag_detail.html успешно обновлен!")
    print(f"📁 Файл: {template_path}")

if __name__ == "__main__":
    print("🔧 Исправление системы тегов...")
    print("=" * 50)
    
    try:
        # Обновляем view
        fix_tag_detail_view()
        
        # Обновляем шаблон  
        update_template()
        
        print("=" * 50)
        print("🎉 Исправление завершено успешно!")
        print()
        print("📋 Что было сделано:")
        print("   • Обновлен TagDetailView для поиска контента по тегам")
        print("   • Добавлены импорты моделей из всех приложений")
        print("   • Обновлен шаблон с поддержкой разных типов контента")
        print("   • Добавлена статистика по типам контента")
        print("   • Добавлены быстрые ссылки для фильтрации")
        print()
        print("🔄 Перезапустите Django-сервер для применения изменений:")
        print("   python manage.py runserver")
        print()
        print("🧪 Проверьте работу:")
        print("   http://127.0.0.1:8000/tag/doch/")
        
    except Exception as e:
        print(f"❌ Ошибка при исправлении: {e}")
        sys.exit(1)
