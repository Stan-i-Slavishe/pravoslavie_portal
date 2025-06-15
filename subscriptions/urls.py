from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.SubscriptionPlansView.as_view(), name='plans'),
    path('subscribe/<int:plan_id>/', views.SubscribeView.as_view(), name='subscribe'),
    path('manage/', views.ManageSubscriptionView.as_view(), name='manage'),
]