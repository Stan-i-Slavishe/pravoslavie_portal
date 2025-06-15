from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='list'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='detail'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
]