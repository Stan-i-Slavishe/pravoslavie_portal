from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Avg, Count, F
from django.utils import timezone
from decimal import Decimal
import json
import logging

from .models import (
    FairyTaleCategory, 
    FairyTaleTemplate, 
    PersonalizationOrder, 
    FairyTaleReview,
    FairyTaleFavorite,
    TherapeuticGoal,
    AgeGroup
)

logger = logging.getLogger(__name__)


class FairyTaleListView(ListView):
    """Список всех терапевтических сказок"""
    model = FairyTaleTemplate
    template_name = 'fairy_tales/fairy_tale_list.html'
    context_object_name = 'fairy_tales'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = FairyTaleTemplate.objects.filter(
            is_published=True,
            category__is_active=True
        ).select_related('category').prefetch_related('reviews')
        
        # Фильтрация по категории
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Фильтрация по возрасту
        age_group = self.request.GET.get('age_group')
        if age_group:
            queryset = queryset.filter(category__age_group=age_group)
        
        # Фильтрация по терапевтическим целям
        goal = self.request.GET.get('goal')
        if goal:
            queryset = queryset.filter(therapeutic_goals__contains=[goal])
        
        # Поиск по названию и описанию
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        # Сортировка
        sort = self.request.GET.get('sort', 'featured')
        if sort == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort == 'popular':
            queryset = queryset.order_by('-orders_count', '-views_count')
        elif sort == 'age_asc':
            queryset = queryset.order_by('target_age_min')
        elif sort == 'age_desc':
            queryset = queryset.order_by('-target_age_max')
        else:  # featured
            queryset = queryset.order_by('-featured', '-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Добавляем категории для фильтров
        context['categories'] = FairyTaleCategory.objects.filter(
            is_active=True
        ).order_by('age_group', 'order', 'name')
        
        # Добавляем терапевтические цели
        context['therapeutic_goals'] = TherapeuticGoal.choices
        
        # Добавляем возрастные группы
        context['age_groups'] = AgeGroup.choices
        
        # Текущие фильтры
        context['current_filters'] = {
            'category': self.request.GET.get('category', ''),
            'age_group': self.request.GET.get('age_group', ''),
            'goal': self.request.GET.get('goal', ''),
            'search': self.request.GET.get('search', ''),
            'sort': self.request.GET.get('sort', 'featured'),
        }
        
        # Статистика
        context['total_tales'] = FairyTaleTemplate.objects.filter(is_published=True).count()
        context['featured_tales'] = self.get_queryset().filter(featured=True)[:3]
        
        return context


class FairyTaleDetailView(DetailView):
    """Детальная страница сказки"""
    model = FairyTaleTemplate
    template_name = 'fairy_tales/fairy_tale_detail.html'
    context_object_name = 'fairy_tale'
    
    def get_queryset(self):
        return FairyTaleTemplate.objects.filter(
            is_published=True
        ).select_related('category').prefetch_related('reviews__author')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Увеличиваем счетчик просмотров
        FairyTaleTemplate.objects.filter(id=obj.id).update(
            views_count=F('views_count') + 1
        )
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fairy_tale = self.object
        
        # Отзывы
        context['reviews'] = fairy_tale.reviews.filter(
            is_published=True
        ).order_by('-created_at')[:10]
        
        # Средний рейтинг
        avg_rating = fairy_tale.reviews.filter(is_published=True).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        context['avg_rating'] = round(avg_rating, 1) if avg_rating else 0
        context['reviews_count'] = fairy_tale.reviews.filter(is_published=True).count()
        
        # Проверяем, в избранном ли у пользователя
        if self.request.user.is_authenticated:
            context['is_favorite'] = FairyTaleFavorite.objects.filter(
                user=self.request.user,
                template=fairy_tale
            ).exists()
        else:
            context['is_favorite'] = False
        
        # Рекомендуемые сказки
        context['related_tales'] = FairyTaleTemplate.objects.filter(
            category=fairy_tale.category,
            is_published=True
        ).exclude(id=fairy_tale.id)[:4]
        
        # Ценообразование
        context['total_price'] = fairy_tale.total_price_with_options
        
        return context


class CategoryListView(ListView):
    """Список категорий сказок"""
    model = FairyTaleCategory
    template_name = 'fairy_tales/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return FairyTaleCategory.objects.filter(
            is_active=True
        ).annotate(
            tales_count=Count('templates', filter=Q(templates__is_published=True))
        ).order_by('age_group', 'order', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Группируем по возрастным группам
        categories_by_age = {}
        for category in context['categories']:
            age_group = category.age_group
            if age_group not in categories_by_age:
                categories_by_age[age_group] = []
            categories_by_age[age_group].append(category)
        
        context['categories_by_age'] = categories_by_age
        context['age_groups'] = AgeGroup.choices
        
        return context


class CategoryDetailView(DetailView):
    """Детальная страница категории"""
    model = FairyTaleCategory
    template_name = 'fairy_tales/category_detail.html'
    context_object_name = 'category'
    
    def get_queryset(self):
        return FairyTaleCategory.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        
        # Сказки в этой категории
        tales_queryset = category.templates.filter(is_published=True)
        
        # Фильтрация по терапевтическим целям
        goal = self.request.GET.get('goal')
        if goal:
            tales_queryset = tales_queryset.filter(therapeutic_goals__contains=[goal])
        
        # Сортировка
        sort = self.request.GET.get('sort', 'featured')
        if sort == 'newest':
            tales_queryset = tales_queryset.order_by('-created_at')
        elif sort == 'popular':
            tales_queryset = tales_queryset.order_by('-orders_count', '-views_count')
        elif sort == 'age_asc':
            tales_queryset = tales_queryset.order_by('target_age_min')
        elif sort == 'age_desc':
            tales_queryset = tales_queryset.order_by('-target_age_max')
        else:  # featured
            tales_queryset = tales_queryset.order_by('-featured', '-created_at')
        
        context['fairy_tales'] = tales_queryset
        context['therapeutic_goals'] = TherapeuticGoal.choices
        context['current_goal'] = goal
        context['current_sort'] = sort
        
        return context


class PersonalizationOrderView(LoginRequiredMixin, CreateView):
    """Заказ персонализации сказки"""
    model = PersonalizationOrder
    template_name = 'fairy_tales/personalization_order.html'
    fields = [
        'customer_name', 'customer_email', 'customer_phone',
        'personalization_data', 'include_audio', 'include_illustrations',
        'special_requests'
    ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        template_slug = self.kwargs['slug']
        fairy_tale = get_object_or_404(
            FairyTaleTemplate,
            slug=template_slug,
            is_published=True
        )
        context['fairy_tale'] = fairy_tale
        
        return context
    
    def form_valid(self, form):
        template_slug = self.kwargs['slug']
        fairy_tale = get_object_or_404(
            FairyTaleTemplate,
            slug=template_slug,
            is_published=True
        )
        
        order = form.save(commit=False)
        order.template = fairy_tale
        order.user = self.request.user
        order.base_price = fairy_tale.base_price
        
        # Рассчитываем дополнительные цены
        if order.include_audio and fairy_tale.has_audio_option:
            order.audio_price = fairy_tale.audio_price
        if order.include_illustrations and fairy_tale.has_illustration_option:
            order.illustration_price = fairy_tale.illustration_price
        
        order.save()
        
        # Увеличиваем счетчик заказов
        FairyTaleTemplate.objects.filter(id=fairy_tale.id).update(
            orders_count=F('orders_count') + 1
        )
        
        messages.success(
            self.request,
            f'Заказ #{order.short_order_id} успешно создан! Мы свяжемся с вами для подтверждения деталей.'
        )
        
        return redirect('fairy_tales:order_success', order_id=order.order_id)


class OrderSuccessView(LoginRequiredMixin, DetailView):
    """Страница успешного заказа"""
    model = PersonalizationOrder
    template_name = 'fairy_tales/order_success.html'
    context_object_name = 'order'
    slug_field = 'order_id'
    slug_url_kwarg = 'order_id'
    
    def get_queryset(self):
        return PersonalizationOrder.objects.filter(user=self.request.user)


class MyOrdersView(LoginRequiredMixin, ListView):
    """Мои заказы персонализации"""
    model = PersonalizationOrder
    template_name = 'fairy_tales/my_orders.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        return PersonalizationOrder.objects.filter(
            user=self.request.user
        ).select_related('template').order_by('-created_at')


class MyFavoritesView(LoginRequiredMixin, ListView):
    """Мои избранные сказки"""
    model = FairyTaleFavorite
    template_name = 'fairy_tales/my_favorites.html'
    context_object_name = 'favorites'
    paginate_by = 12
    
    def get_queryset(self):
        return FairyTaleFavorite.objects.filter(
            user=self.request.user
        ).select_related('template__category').order_by('-created_at')


# ==========================================
# AJAX Views
# ==========================================

@login_required
@require_POST
def toggle_favorite(request, template_id):
    """Добавить/убрать из избранного"""
    try:
        template = get_object_or_404(FairyTaleTemplate, id=template_id, is_published=True)
        
        favorite, created = FairyTaleFavorite.objects.get_or_create(
            user=request.user,
            template=template
        )
        
        if created:
            is_favorite = True
            message = f'Сказка "{template.title}" добавлена в избранное'
        else:
            favorite.delete()
            is_favorite = False
            message = f'Сказка "{template.title}" убрана из избранного'
        
        return JsonResponse({
            'status': 'success',
            'is_favorite': is_favorite,
            'message': message
        })
        
    except Exception as e:
        logger.error(f"Ошибка переключения избранного: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'Произошла ошибка'
        }, status=500)


@login_required
@require_POST
def add_review(request, template_id):
    """Добавить отзыв о сказке"""
    try:
        template = get_object_or_404(FairyTaleTemplate, id=template_id, is_published=True)
        
        # Проверяем, не оставлял ли пользователь уже отзыв
        if FairyTaleReview.objects.filter(template=template, author=request.user).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Вы уже оставляли отзыв об этой сказке'
            }, status=400)
        
        data = json.loads(request.body)
        
        review = FairyTaleReview.objects.create(
            template=template,
            author=request.user,
            rating=int(data.get('rating', 5)),
            title=data.get('title', ''),
            content=data.get('content', ''),
            helped_with_problem=data.get('helped_with_problem'),
            child_liked=data.get('child_liked'),
            would_recommend=data.get('would_recommend', True)
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Спасибо за отзыв! Он поможет другим родителям.',
            'review_id': review.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Некорректные данные'
        }, status=400)
    except Exception as e:
        logger.error(f"Ошибка добавления отзыва: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'Произошла ошибка при сохранении отзыва'
        }, status=500)


@require_POST
def preview_personalization(request):
    """Предварительный просмотр персонализированной сказки"""
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        personalization_data = data.get('personalization_data', {})
        
        template = get_object_or_404(FairyTaleTemplate, id=template_id, is_published=True)
        
        # Заменяем переменные в шаблоне
        content = template.content_template
        for key, value in personalization_data.items():
            content = content.replace(f'{{{key}}}', str(value))
        
        return JsonResponse({
            'status': 'success',
            'preview_content': content[:500] + '...' if len(content) > 500 else content
        })
        
    except Exception as e:
        logger.error(f"Ошибка предпросмотра: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'Произошла ошибка'
        }, status=500)


@require_POST
def calculate_price(request):
    """Расчет стоимости персонализации"""
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        include_audio = data.get('include_audio', False)
        include_illustrations = data.get('include_illustrations', False)
        
        template = get_object_or_404(FairyTaleTemplate, id=template_id, is_published=True)
        
        total_price = template.base_price
        
        if include_audio and template.has_audio_option:
            total_price += template.audio_price
        
        if include_illustrations and template.has_illustration_option:
            total_price += template.illustration_price
        
        return JsonResponse({
            'status': 'success',
            'base_price': float(template.base_price),
            'audio_price': float(template.audio_price) if include_audio else 0,
            'illustration_price': float(template.illustration_price) if include_illustrations else 0,
            'total_price': float(total_price)
        })
        
    except Exception as e:
        logger.error(f"Ошибка расчета цены: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'Произошла ошибка'
        }, status=500)


# ==========================================
# LEGACY: Подписка на уведомления (для совместимости)
# ==========================================

@require_POST
def subscribe_notification(request):
    """Подписка на уведомления о запуске (legacy)"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        child_age = data.get('child_age', '').strip()
        
        if not email:
            return JsonResponse({'error': 'Email обязателен'}, status=400)
        
        logger.info(f"Legacy: Подписка на сказки: {email}, возраст ребенка: {child_age}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Спасибо! Сказки уже доступны в каталоге.'
        })
        
    except Exception as e:
        logger.error(f"Ошибка legacy подписки: {e}")
        return JsonResponse({'error': 'Произошла ошибка'}, status=500)
