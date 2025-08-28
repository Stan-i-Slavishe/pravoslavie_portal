from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, Sum, F
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

from .models import UserProfile
from .forms import UserProfileForm, PasswordChangeForm
from books.models import UserFavoriteBook, ReadingSession, BookDownload
from shop.models import Order, Purchase
# from stories.models import Playlist  # Временно закомментировано

@method_decorator(login_required, name='dispatch')
class ProfileView(LoginRequiredMixin, TemplateView):
    """Главная страница профиля пользователя"""
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Получаем или создаем профиль
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Статистика чтения
        reading_stats = {
            'books_reading': ReadingSession.objects.filter(user=user).count(),
            'books_completed': ReadingSession.objects.filter(
                user=user, 
                current_page__gte=F('total_pages')
            ).count(),
            'books_downloaded': BookDownload.objects.filter(user=user).count(),
            'favorite_books': UserFavoriteBook.objects.filter(user=user).count(),
        }
        
        # Статистика покупок
        purchase_stats = {
            'total_orders': Order.objects.filter(user=user).count(),
            'completed_orders': Order.objects.filter(user=user, status='completed').count(),
            'total_purchases': Purchase.objects.filter(user=user).count(),
            'total_spent': Order.objects.filter(
                user=user, 
                status='completed'
            ).aggregate(total=Sum('total_amount'))['total'] or 0,
        }
        
        # Последние активности
        recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
        recent_reading = ReadingSession.objects.filter(user=user).select_related('book').order_by('-last_read')[:5]
        recent_favorites = UserFavoriteBook.objects.filter(user=user).select_related('book').order_by('-added_at')[:5]
        
        # Плейлисты пользователя (временно отключено)
        # user_playlists = Playlist.objects.filter(user=user).annotate(
        #     story_count=Count('items')
        # ).order_by('-created_at')[:5]
        user_playlists = []  # Пустой список пока
        
        # Вычисляем время с регистрации
        membership_duration = self.get_membership_duration(user.date_joined)
        
        context.update({
            'title': 'Мой профиль',
            'profile': profile,
            'reading_stats': reading_stats,
            'purchase_stats': purchase_stats,
            'recent_orders': recent_orders,
            'recent_reading': recent_reading,
            'recent_favorites': recent_favorites,
            'user_playlists': user_playlists,
            'membership_duration': membership_duration,
        })
        
        return context
    
    def get_membership_duration(self, join_date):
        """Вычисляет красивое отображение времени регистрации"""
        now = timezone.now()
        diff = now - join_date
        
        # Если меньше месяца
        if diff.days < 30:
            if diff.days < 1:
                return "Добро пожаловать! ✨"
            elif diff.days == 1:
                return "Вы с нами уже день! 🌟"
            elif diff.days == 2:
                return "Вы с нами уже 2 дня! 🌟"
            elif diff.days < 5:
                return f"Вы с нами уже {diff.days} дня! 🌟"
            elif diff.days < 7:
                return f"Вы с нами уже {diff.days} дней! 🌟"
            else:
                weeks = diff.days // 7
                if weeks == 1:
                    return "Вы с нами уже неделю! 🌟"
                elif weeks == 2:
                    return "Вы с нами уже 2 недели! 🌟"
                elif weeks == 3:
                    return "Вы с нами уже 3 недели! 🌟"
                else:
                    return f"Вы с нами уже {weeks} недели! 🌟"
        
        # Если меньше года
        elif diff.days < 365:
            months = diff.days // 30
            if months == 1:
                return "Вы с нами уже месяц! 🌟"
            elif months == 2:
                return "Вы с нами уже 2 месяца! 🌟"
            elif months == 3:
                return "Вы с нами уже 3 месяца! 🌟"
            elif months == 4:
                return "Вы с нами уже 4 месяца! 🌟"
            elif months < 12:
                return f"Вы с нами уже {months} месяцев! 🌟"
        
        # Если больше года
        else:
            years = diff.days // 365
            if years == 1:
                return "Вы с нами уже целый год! 🎉"
            elif years == 2:
                return "Вы с нами уже 2 года! 🎉"
            elif years == 3:
                return "Вы с нами уже 3 года! 🎉"
            elif years == 4:
                return "Вы с нами уже 4 года! 🎉"
            elif years < 10:
                return f"Вы с нами уже {years} лет! 🎉"
            else:
                return f"Вы с нами уже {years} лет! 🎊 Спасибо за верность!"


@method_decorator(login_required, name='dispatch')
class ProfileEditView(LoginRequiredMixin, TemplateView):
    """Редактирование профиля пользователя"""
    template_name = 'accounts/profile_edit.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Получаем или создаем профиль
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        context.update({
            'title': 'Редактирование профиля',
            'form': UserProfileForm(instance=profile, user=user),
            'profile': profile,
        })
        
        return context
    
    def post(self, request, *args, **kwargs):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=user)
        
        if form.is_valid():
            form.save(user=user)
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class PasswordChangeView(LoginRequiredMixin, TemplateView):
    """Смена пароля"""
    template_name = 'accounts/password_change.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Смена пароля',
            'form': PasswordChangeForm(user=self.request.user),
        })
        return context
    
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Важно! Сохраняем сессию
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class FavoritesView(LoginRequiredMixin, TemplateView):
    """Избранное пользователя"""
    template_name = 'accounts/favorites.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Избранные книги
        favorite_books = UserFavoriteBook.objects.filter(user=user).select_related('book').order_by('-added_at')
        
        # Пагинация
        paginator = Paginator(favorite_books, 12)  # 12 книг на страницу
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'title': 'Избранные книги',
            'favorite_books': page_obj,
            'total_favorites': favorite_books.count(),
        })
        
        return context


@method_decorator(login_required, name='dispatch')
class MyOrdersView(LoginRequiredMixin, TemplateView):
    """Мои заказы"""
    template_name = 'accounts/my_orders.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Заказы пользователя
        orders = Order.objects.filter(user=user).order_by('-created_at')
        
        # Фильтрация по статусу
        status_filter = self.request.GET.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)
        
        # Пагинация
        paginator = Paginator(orders, 10)  # 10 заказов на страницу
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Статистика заказов
        order_stats = {
            'total': Order.objects.filter(user=user).count(),
            'pending': Order.objects.filter(user=user, status='pending').count(),
            'completed': Order.objects.filter(user=user, status='completed').count(),
            'cancelled': Order.objects.filter(user=user, status='cancelled').count(),
        }
        
        context.update({
            'title': 'Мои заказы',
            'orders': page_obj,
            'order_stats': order_stats,
            'current_filter': status_filter,
        })
        
        return context


@method_decorator(login_required, name='dispatch')
class MyPurchasesView(LoginRequiredMixin, TemplateView):
    """Мои покупки"""
    template_name = 'accounts/my_purchases.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Покупки пользователя
        purchases = Purchase.objects.filter(user=user).select_related('product', 'order').order_by('-purchased_at')
        
        # Фильтрация по типу товара
        product_type = self.request.GET.get('type')
        if product_type:
            purchases = purchases.filter(product__product_type=product_type)
        
        # Пагинация
        paginator = Paginator(purchases, 12)  # 12 покупок на страницу
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Статистика покупок
        purchase_stats = {
            'total': purchases.count(),
            'books': purchases.filter(product__product_type='book').count(),
            'audio': purchases.filter(product__product_type='audio').count(),
            'subscriptions': purchases.filter(product__product_type='subscription').count(),
        }
        
        context.update({
            'title': 'Мои покупки',
            'purchases': page_obj,
            'purchase_stats': purchase_stats,
            'current_filter': product_type,
        })
        
        return context


@method_decorator(login_required, name='dispatch')
class MyPlaylistsView(LoginRequiredMixin, TemplateView):
    """Мои плейлисты"""
    template_name = 'accounts/my_playlists.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Плейлисты пользователя (временно отключено)
        # playlists = Playlist.objects.filter(user=user).annotate(
        #     story_count=Count('items')
        # ).order_by('-created_at')
        playlists = []  # Пустой список
        
        # Пагинация
        paginator = Paginator(playlists, 12)  # 12 плейлистов на страницу
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context.update({
            'title': 'Мои плейлисты',
            'playlists': page_obj,
            'total_playlists': playlists.count(),
        })
        
        return context


@method_decorator(login_required, name='dispatch')
class ReadingProgressView(LoginRequiredMixin, TemplateView):
    """Прогресс чтения"""
    template_name = 'accounts/reading_progress.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Сессии чтения
        reading_sessions = ReadingSession.objects.filter(user=user).select_related('book').order_by('-last_read')
        
        # Разделяем на активные и завершенные
        active_reading = reading_sessions.filter(current_page__lt=F('total_pages'))
        completed_reading = reading_sessions.filter(current_page__gte=F('total_pages'))
        
        # Пагинация для активного чтения
        active_paginator = Paginator(active_reading, 10)
        active_page = self.request.GET.get('active_page', 1)
        active_page_obj = active_paginator.get_page(active_page)
        
        # Пагинация для завершенного чтения
        completed_paginator = Paginator(completed_reading, 10)
        completed_page = self.request.GET.get('completed_page', 1)
        completed_page_obj = completed_paginator.get_page(completed_page)
        
        # Статистика чтения
        reading_stats = {
            'total_books': reading_sessions.count(),
            'active_books': active_reading.count(),
            'completed_books': completed_reading.count(),
            'total_reading_time': reading_sessions.aggregate(
                total_time=Sum('reading_time')
            )['total_time'] or 0,
        }
        
        context.update({
            'title': 'Прогресс чтения',
            'active_reading': active_page_obj,
            'completed_reading': completed_page_obj,
            'reading_stats': reading_stats,
        })
        
        return context


@login_required
def profile_stats_api(request):
    """API для получения статистики профиля (для AJAX)"""
    user = request.user
    
    stats = {
        'reading': {
            'active': ReadingSession.objects.filter(user=user, current_page__lt=F('total_pages')).count(),
            'completed': ReadingSession.objects.filter(user=user, current_page__gte=F('total_pages')).count(),
            'favorites': UserFavoriteBook.objects.filter(user=user).count(),
        },
        'purchases': {
            'orders': Order.objects.filter(user=user).count(),
            'completed_orders': Order.objects.filter(user=user, status='completed').count(),
            'total_spent': float(Order.objects.filter(user=user, status='completed').aggregate(
                total=Sum('total_amount')
            )['total'] or 0),
        },
        'social': {
            'playlists': Playlist.objects.filter(user=user).count(),
        }
    }
    
    return JsonResponse(stats)
