from django.urls import path
from . import views

app_name = 'stories'

urlpatterns = [
    path('', views.StoryListView.as_view(), name='list'),
    path('<slug:slug>/', views.StoryDetailView.as_view(), name='detail'),
    path('category/<slug:category_slug>/', views.StoryCategoryView.as_view(), name='category'),
]