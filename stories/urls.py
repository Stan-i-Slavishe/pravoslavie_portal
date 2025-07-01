from django.urls import path
from . import views
from . import views_playlists
from . import views_comments

app_name = 'stories'

urlpatterns = [
    path('', views.StoryListView.as_view(), name='list'),
    path('<slug:slug>/', views_playlists.enhanced_story_detail, name='detail'),
    path('category/<slug:category_slug>/', views.StoryCategoryView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.StoryTagView.as_view(), name='tag'),
    path('popular/', views.PopularStoriesView.as_view(), name='popular'),
    path('featured/', views.FeaturedStoriesView.as_view(), name='featured'),
    path('search/', views.StorySearchView.as_view(), name='search'),
    path('<int:story_id>/like/', views.story_like, name='story_like'),
    path('<int:story_id>/favorite/', views.story_favorite, name='story_favorite'),
    
    # Новые URL'ы для комментариев
    path('<int:story_id>/comments/add/', views.add_comment, name='add_comment'),
    path('<int:story_id>/comments/load/', views.load_comments, name='load_comments'),
    path('<int:story_id>/comments/load-more/', views.load_more_comments, name='load_more_comments'),
    path('comments/<int:comment_id>/reaction/', views.comment_reaction, name='comment_reaction'),
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('playlists/', views_playlists.playlists_list, name='playlists_list'),
    path('playlist/create/', views_playlists.create_playlist, name='create_playlist'),
    path('playlist/add-story/', views_playlists.add_to_playlist, name='add_to_playlist'),
    path('playlist/remove-story/', views_playlists.remove_from_playlist, name='remove_from_playlist'),
    
    # YouTube-style комментарии AJAX API
    path('ajax/<slug:story_slug>/comments/', views_comments.load_comments, name='ajax_load_comments'),
    path('ajax/<slug:story_slug>/comments/add/', views_comments.add_comment, name='ajax_add_comment'),
    path('ajax/comments/<int:comment_id>/replies/', views_comments.load_replies, name='ajax_load_replies'),
    path('ajax/comments/<int:comment_id>/reaction/', views_comments.toggle_comment_reaction, name='ajax_comment_reaction'),
    path('ajax/comments/<int:comment_id>/edit/', views_comments.edit_comment, name='ajax_edit_comment'),
    path('ajax/comments/<int:comment_id>/delete/', views_comments.delete_comment, name='ajax_delete_comment'),
    path('ajax/comments/<int:comment_id>/report/', views_comments.report_comment, name='ajax_report_comment'),
    path('ajax/<slug:story_slug>/comments/stats/', views_comments.comments_stats, name='ajax_comments_stats'),
]
