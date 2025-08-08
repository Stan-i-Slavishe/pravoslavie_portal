from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # Категории и теги
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('category/<str:slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('tags/', views.TagListView.as_view(), name='tags'),
    path('tags/<str:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
]