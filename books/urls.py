from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # Основные страницы
    path('', views.book_list, name='list'),
    path('book/<slug:slug>/', views.book_detail, name='detail'),
    path('download/<int:book_id>/', views.download_book, name='download'),
    
    # Чтение книг
    path('read/<slug:slug>/', views.read_book, name='read'),
    path('modern-reader/<slug:slug>/', views.modern_reader, name='modern_reader'),
    path('progress/<int:book_id>/', views.update_reading_progress, name='progress'),
    path('bookmark/<int:book_id>/', views.add_bookmark, name='bookmark'),
    path('bookmarks/<int:book_id>/', views.get_bookmarks, name='get_bookmarks'),
    path('bookmark/<int:book_id>/<int:bookmark_id>/', views.remove_bookmark, name='remove_bookmark'),
    
    # Категории
    path('categories/', views.category_list, name='categories'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    
    # Пользовательские действия
    path('favorites/', views.user_favorites, name='favorites'),
    path('favorite/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('review/<int:book_id>/', views.add_review, name='add_review'),
    
    # История и статистика чтения
    path('reading-history/', views.reading_history, name='reading_history'),
    path('reading-stats/', views.reading_stats, name='reading_stats'),
    
    # AJAX
    path('search/', views.search_books, name='search'),
    path('favorites-count/', views.get_favorites_count, name='favorites_count'),
]
