from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/password/', views.PasswordChangeView.as_view(), name='password_change'),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('orders/', views.MyOrdersView.as_view(), name='my_orders'),
    path('purchases/', views.MyPurchasesView.as_view(), name='my_purchases'),
    path('playlists/', views.MyPlaylistsView.as_view(), name='my_playlists'),
    path('reading/', views.ReadingProgressView.as_view(), name='reading_progress'),
    path('api/stats/', views.profile_stats_api, name='profile_stats_api'),
]
