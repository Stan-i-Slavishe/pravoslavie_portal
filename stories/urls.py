from django.urls import path
from . import views
from . import views_playlists
from . import views_comments

app_name = 'stories'

urlpatterns = [
    path('', views.StoryListView.as_view(), name='list'),
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
    
    # Плейлист URLs - Основные функции
    path('playlists/', views_playlists.playlists_list, name='playlists_list'),
    path('playlists/', views_playlists.playlists_list, name='playlists'),  # Alias для совместимости
    path('playlists/public/', views_playlists.public_playlists, name='public_playlists'),
    path('playlists/watch-later/', views_playlists.watch_later_playlist, name='watch_later'),
    path('playlists/favorites/', views_playlists.favorites_playlist, name='favorites'),
    
    # Системные плейлисты API
    path('system-playlist/<str:playlist_type>/', views_playlists.system_playlist_content, name='system_playlist_content'),
    
    # AJAX операции с элементами плейлистов - ПЕРЕНОСИМ ВЫШЕ!
    path('playlists/add-to-playlist/', views_playlists.add_to_playlist, name='add_to_playlist'),
    path('playlists/remove-from-playlist/', views_playlists.remove_from_playlist, name='remove_from_playlist'),
    path('playlists/toggle-watch-later/', views_playlists.toggle_watch_later, name='toggle_watch_later'),
    path('playlists/toggle-favorites/', views_playlists.toggle_favorites, name='toggle_favorites'),
    path('playlists/for-save/', views_playlists.playlists_for_save, name='playlists_for_save'),
    
    # CRUD операции с плейлистами
    path('playlist/create/', views_playlists.create_playlist, name='create_playlist'),
    path('playlist/<str:slug>/', views_playlists.playlist_detail, name='playlist_detail'),
    path('playlist/<str:slug>/edit/', views_playlists.edit_playlist, name='edit_playlist'),
    path('playlist/<str:slug>/delete/', views_playlists.delete_playlist, name='delete_playlist'),
    path('playlist/<str:slug>/reorder/', views_playlists.reorder_playlist, name='reorder_playlist'),
    
    # ВАЖНО! Модальное окно плейлиста - ПЕРЕМЕЩАЕМ ВЫШЕ story detail
    path('playlist/<int:playlist_id>/modal-content/', views_playlists.playlist_modal_content, name='playlist_modal_content'),
    
    # Публичные плейлисты
    path('u/<int:user_id>/playlist/<str:slug>/', views_playlists.public_playlist_detail, name='public_playlist_detail'),
    
    # Частичные шаблоны и дополнительные функции
    path('<slug:story_slug>/sidebar-playlists/', views_playlists.sidebar_playlists_partial, name='sidebar_playlists_partial'),
    
    # YouTube-style комментарии AJAX API
    path('ajax/<slug:story_slug>/comments/', views_comments.load_comments, name='ajax_load_comments'),
    path('ajax/<slug:story_slug>/comments/add/', views_comments.add_comment, name='ajax_add_comment'),
    path('ajax/comments/<int:comment_id>/replies/', views_comments.load_replies, name='ajax_load_replies'),
    path('ajax/comments/<int:comment_id>/reaction/', views_comments.toggle_comment_reaction, name='ajax_comment_reaction'),
    path('ajax/comments/<int:comment_id>/edit/', views_comments.edit_comment, name='ajax_edit_comment'),
    path('ajax/comments/<int:comment_id>/delete/', views_comments.delete_comment, name='ajax_delete_comment'),
    path('ajax/comments/<int:comment_id>/report/', views_comments.report_comment, name='ajax_report_comment'),
    path('ajax/<slug:story_slug>/comments/stats/', views_comments.comments_stats, name='ajax_comments_stats'),
    
    # Story detail - ОБЯЗАТЕЛЬНО в конце, чтобы не конфликтовать с другими slug'ами
    path('<slug:slug>/', views_playlists.enhanced_story_detail, name='detail'),
]
