from django.urls import path
from . import views
from .simple_views import story_detail_simple, add_comment_simple, delete_comment_simple, add_reply_simple

app_name = 'stories'

urlpatterns = [
    # Основные страницы
    path('', views.StoryListView.as_view(), name='list'),
    
    # ПРОСТАЯ СИСТЕМА КОММЕНТАРИЕВ
    path('<slug:slug>/', story_detail_simple, name='detail_simple'),
    path('comment/add/<slug:story_slug>/', add_comment_simple, name='add_comment'),
    path('comment/reply/<int:comment_id>/', add_reply_simple, name='add_reply'),
    path('comment/delete/<int:comment_id>/', delete_comment_simple, name='delete_comment'),
    path('comment/reaction/<int:comment_id>/<str:reaction_type>/', delete_comment_simple, name='toggle_comment_reaction'),  # Заглушка
]