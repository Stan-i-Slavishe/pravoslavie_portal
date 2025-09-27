from django.urls import path
from .views.main_views import (
    HomeView, AboutView, ContactView, CategoryListView, 
    CategoryDetailView, TagListView, TagDetailView, MobileFeedbackView,
    DonateView
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('donate/', DonateView.as_view(), name='donate'),
    
    # Категории и теги
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category'),
    path('tags/', TagListView.as_view(), name='tags'),
    path('tags/<str:slug>/', TagDetailView.as_view(), name='tag_detail'),
    
    # API для мобильной обратной связи
    path('api/mobile-feedback/', MobileFeedbackView.as_view(), name='mobile_feedback'),
]