from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # Основные страницы
    path('', views.book_list, name='list'),
    path('book/<slug:slug>/', views.book_detail, name='detail'),
    path('download/<int:book_id>/', views.download_book, name='download'),
    
    # Категории
    path('categories/', views.category_list, name='categories'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    
    # Пользовательские действия
    path('favorites/', views.user_favorites, name='favorites'),
    path('favorite/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('review/<int:book_id>/', views.add_review, name='add_review'),
    # path('<int:book_id>/view/', views.track_book_view, name='track_view'),
    
    # AJAX
    path('search/', views.search_books, name='search'),
    path('favorites-count/', views.get_favorites_count, name='favorites_count'),
]
