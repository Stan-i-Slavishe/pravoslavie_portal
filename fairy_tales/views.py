from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count
from decimal import Decimal
import json

from .models import (
    FairyTaleCategory, 
    FairyTaleTemplate, 
    PersonalizationOrder, 
    FairyTaleReview,
    FairyTaleFavorite,
    TherapeuticGoal,
    AgeGroup
)

class FairyTaleListView(ListView):
    """Каталог терапевтических сказок"""
    model = FairyTaleTemplate
    template_name = 'fairy_tales/fairy_tale_list.html'
    context_object_name = 'fairy_tales'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = FairyTaleTemplate.objects.filter(is_published=True)
        
        # Фильтры
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        age_group = self.request.GET.get('age_group')
        if age_group:
            queryset = queryset.filter(category__age_group=age_group)
        
        goal = self.request.GET.get('goal')
        if goal:
            queryset = queryset.filter(therapeutic_goals__contains=[goal])
        
        is_free = self.request.GET.get('is_free')
        if is_free == 'true':
            queryset = queryset.filter(is_free=True)
        elif is_free == 'false':
            queryset = queryset.filter(is_free=False)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(content_template__icontains=search)
            )
        
        # Сортировка
        sort = self.request.GET.get('sort', 'featured')
        if sort == 'price_low':
            queryset = queryset.order_by('base_price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-base_price')
        elif sort == 'popular':
            queryset = queryset.order_by('-orders_count', '-views_count')
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')
        else:  # featured
            queryset = queryset.order_by('-featured', '-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = FairyTaleCategory.objects.filter(is_active=True)
        context['age_groups'] = AgeGroup.choices
        context['therapeutic_goals'] = TherapeuticGoal.choices
        context['current_filters'] = {
            'category': self.request.GET.get('category', ''),
            'age_group': self.request.GET.get('age_group', ''),
            'goal': self.request.GET.get('goal', ''),
            'is_free': self.request.GET.get('is_free', ''),
            'search': self.request.GET.get('search', ''),
            'sort': self.request.GET.get('sort', 'featured'),
        }
        
        # Добавляем информацию о связанных товарах в магазине
        for fairy_tale in context['fairy_tales']:
            fairy_tale.shop_product = fairy_tale.get_shop_product()
        
        return context

class FairyTaleDetailView(DetailView):
    """Страница отдельной сказки"""
    model = FairyTaleTemplate
    template_name = 'fairy_tales/fairy_tale_detail.html'
    context_object_name = 'fairy_tale'
    
    def get_queryset(self):
        return FairyTaleTemplate.objects.filter(is_published=True)
    
    def get_object(self):
        obj = super().get_object()
        # Увеличиваем счетчик просмотров
        FairyTaleTemplate.objects.filter(pk=obj.pk).update(views_count=obj.views_count + 1)
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fairy_tale = self.get_object()
        
        # Похожие сказки
        context['related_fairy_tales'] = FairyTaleTemplate.objects.filter(
            is_published=True,
            category=fairy_tale.category
        ).exclude(id=fairy_tale.id)[:4]
        
        # Отзывы
        context['reviews'] = fairy_tale.reviews.filter(is_published=True)[:5]
        context['avg_rating'] = fairy_tale.reviews.filter(is_published=True).aggregate(
            avg=Avg('rating')
        )['avg']
        
        # Проверяем, есть ли в избранном у пользователя
        if self.request.user.is_authenticated:
            context['is_favorited'] = FairyTaleFavorite.objects.filter(
                user=self.request.user,
                template=fairy_tale
            ).exists()
        
        # Получаем связанный товар в магазине
        context['shop_product'] = fairy_tale.get_shop_product()
        
        return context

class PersonalizationOrderView(TemplateView):
    """Форма заказа персонализации"""
    template_name = 'fairy_tales/personalization_order.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        template_slug = kwargs.get('slug')
        
        try:
            fairy_tale = FairyTaleTemplate.objects.get(
                slug=template_slug,
                is_published=True
            )
            context['fairy_tale'] = fairy_tale
        except FairyTaleTemplate.DoesNotExist:
            raise Http404("Сказка не найдена")
        
        return context
    
    def post(self, request, *args, **kwargs):
        template_slug = kwargs.get('slug')
        
        try:
            fairy_tale = FairyTaleTemplate.objects.get(
                slug=template_slug,
                is_published=True
            )
        except FairyTaleTemplate.DoesNotExist:
            messages.error(request, "Сказка не найдена")
            return redirect('fairy_tales:list')
        
        # Собираем данные формы
        personalization_data = {}
        
        # Основные данные
        customer_name = request.POST.get('customer_name', '').strip()
        customer_email = request.POST.get('customer_email', '').strip()
        customer_phone = request.POST.get('customer_phone', '').strip()
        
        # Данные для персонализации
        child_name = request.POST.get('child_name', '').strip()
        child_age = request.POST.get('child_age', '')
        child_gender = request.POST.get('child_gender', '')
        main_problem = request.POST.get('main_problem', '').strip()
        child_interests = request.POST.get('child_interests', '').strip()
        family_situation = request.POST.get('family_situation', '').strip()
        special_requests = request.POST.get('special_requests', '').strip()
        
        # Опции
        include_audio = request.POST.get('include_audio') == 'on'
        include_illustrations = request.POST.get('include_illustrations') == 'on'
        
        # Валидация
        if not all([customer_name, customer_email, child_name, main_problem]):
            messages.error(request, "Пожалуйста, заполните все обязательные поля")
            return render(request, self.template_name, {
                'fairy_tale': fairy_tale,
                'form_data': request.POST
            })
        
        # Сохраняем данные персонализации
        personalization_data = {
            'child_name': child_name,
            'child_age': child_age,
            'child_gender': child_gender,
            'main_problem': main_problem,
            'child_interests': child_interests,
            'family_situation': family_situation,
        }
        
        # Расчет цены
        base_price = fairy_tale.base_price
        audio_price = fairy_tale.audio_price if include_audio else Decimal('0.00')
        illustration_price = fairy_tale.illustration_price if include_illustrations else Decimal('0.00')
        total_price = base_price + audio_price + illustration_price
        
        # Создаем заказ
        order = PersonalizationOrder.objects.create(
            template=fairy_tale,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            user=request.user if request.user.is_authenticated else None,
            personalization_data=personalization_data,
            include_audio=include_audio,
            include_illustrations=include_illustrations,
            special_requests=special_requests,
            base_price=base_price,
            audio_price=audio_price,
            illustration_price=illustration_price,
            total_price=total_price,
        )
        
        # Увеличиваем счетчик заказов для шаблона
        FairyTaleTemplate.objects.filter(pk=fairy_tale.pk).update(
            orders_count=fairy_tale.orders_count + 1
        )
        
        messages.success(
            request, 
            f'Заказ #{order.short_order_id} успешно создан! '
            f'Мы свяжемся с вами в ближайшее время.'
        )
        
        return redirect('fairy_tales:order_success', order_id=order.order_id)

class OrderSuccessView(DetailView):
    """Страница успешного заказа"""
    model = PersonalizationOrder
    template_name = 'fairy_tales/order_success.html'
    context_object_name = 'order'
    slug_field = 'order_id'
    slug_url_kwarg = 'order_id'

class CategoryListView(ListView):
    """Список категорий сказок"""
    model = FairyTaleCategory
    template_name = 'fairy_tales/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return FairyTaleCategory.objects.filter(is_active=True).annotate(
            templates_count=Count('templates', filter=Q(templates__is_published=True))
        )

class CategoryDetailView(DetailView):
    """Страница категории сказок"""
    model = FairyTaleCategory
    template_name = 'fairy_tales/category_detail.html'
    context_object_name = 'category'
    
    def get_queryset(self):
        return FairyTaleCategory.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        
        context['fairy_tales'] = FairyTaleTemplate.objects.filter(
            category=category,
            is_published=True
        ).order_by('-featured', '-created_at')[:12]
        
        return context

class MyOrdersView(LoginRequiredMixin, ListView):
    """Мои заказы сказок"""
    model = PersonalizationOrder
    template_name = 'fairy_tales/my_orders.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        return PersonalizationOrder.objects.filter(
            user=self.request.user
        ).order_by('-created_at')

class MyFavoritesView(LoginRequiredMixin, ListView):
    """Мои избранные сказки"""
    model = FairyTaleFavorite
    template_name = 'fairy_tales/my_favorites.html'
    context_object_name = 'favorites'
    paginate_by = 12
    
    def get_queryset(self):
        return FairyTaleFavorite.objects.filter(
            user=self.request.user
        ).select_related('template').order_by('-created_at')

# AJAX Views
@require_POST
@csrf_exempt
def toggle_favorite(request, template_id):
    """Добавить/убрать из избранного"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Требуется авторизация'}, status=401)
    
    try:
        fairy_tale = FairyTaleTemplate.objects.get(
            id=template_id,
            is_published=True
        )
    except FairyTaleTemplate.DoesNotExist:
        return JsonResponse({'error': 'Сказка не найдена'}, status=404)
    
    favorite, created = FairyTaleFavorite.objects.get_or_create(
        user=request.user,
        template=fairy_tale
    )
    
    if not created:
        favorite.delete()
        is_favorited = False
    else:
        is_favorited = True
    
    return JsonResponse({
        'status': 'success',
        'is_favorited': is_favorited,
        'favorites_count': fairy_tale.favorited_by.count()
    })

@require_POST
def add_review(request, template_id):
    """Добавить отзыв о сказке"""
    if not request.user.is_authenticated:
        messages.error(request, 'Для оставления отзыва необходимо войти в систему')
        return redirect('account_login')
    
    try:
        fairy_tale = FairyTaleTemplate.objects.get(
            id=template_id,
            is_published=True
        )
    except FairyTaleTemplate.DoesNotExist:
        messages.error(request, 'Сказка не найдена')
        return redirect('fairy_tales:list')
    
    # Проверяем, что пользователь еще не оставлял отзыв
    if FairyTaleReview.objects.filter(template=fairy_tale, author=request.user).exists():
        messages.error(request, 'Вы уже оставляли отзыв об этой сказке')
        return redirect('fairy_tales:detail', slug=fairy_tale.slug)
    
    rating = request.POST.get('rating')
    title = request.POST.get('title', '').strip()
    content = request.POST.get('content', '').strip()
    helped_with_problem = request.POST.get('helped_with_problem')
    child_liked = request.POST.get('child_liked')
    
    # Валидация
    if not all([rating, title, content]):
        messages.error(request, 'Пожалуйста, заполните все поля')
        return redirect('fairy_tales:detail', slug=fairy_tale.slug)
    
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError()
    except (ValueError, TypeError):
        messages.error(request, 'Некорректная оценка')
        return redirect('fairy_tales:detail', slug=fairy_tale.slug)
    
    # Создаем отзыв
    FairyTaleReview.objects.create(
        template=fairy_tale,
        author=request.user,
        rating=rating,
        title=title,
        content=content,
        helped_with_problem=helped_with_problem == 'yes' if helped_with_problem else None,
        child_liked=child_liked == 'yes' if child_liked else None,
    )
    
    messages.success(request, 'Спасибо за ваш отзыв!')
    return redirect('fairy_tales:detail', slug=fairy_tale.slug)

def preview_personalization(request):
    """Предпросмотр персонализированной сказки (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)
    
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        personalization_data = data.get('personalization_data', {})
        
        fairy_tale = FairyTaleTemplate.objects.get(
            id=template_id,
            is_published=True
        )
        
        # Простая замена переменных в шаблоне
        preview_text = fairy_tale.content_template
        
        # Заменяем основные переменные
        replacements = {
            '{name}': personalization_data.get('child_name', '[Имя ребенка]'),
            '{age}': personalization_data.get('child_age', '[возраст]'),
            '{problem}': personalization_data.get('main_problem', '[проблема]'),
            '{interests}': personalization_data.get('child_interests', '[увлечения]'),
            '{hobby}': personalization_data.get('child_interests', '[хобби]'),
        }
        
        for placeholder, value in replacements.items():
            preview_text = preview_text.replace(placeholder, value)
        
        # Ограничиваем предпросмотр первыми 500 символами
        preview_text = preview_text[:500] + '...' if len(preview_text) > 500 else preview_text
        
        return JsonResponse({
            'status': 'success',
            'preview': preview_text
        })
        
    except FairyTaleTemplate.DoesNotExist:
        return JsonResponse({'error': 'Сказка не найдена'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)

def calculate_price(request):
    """Расчет стоимости заказа (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)
    
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        include_audio = data.get('include_audio', False)
        include_illustrations = data.get('include_illustrations', False)
        
        fairy_tale = FairyTaleTemplate.objects.get(
            id=template_id,
            is_published=True
        )
        
        base_price = fairy_tale.base_price
        audio_price = fairy_tale.audio_price if include_audio else Decimal('0.00')
        illustration_price = fairy_tale.illustration_price if include_illustrations else Decimal('0.00')
        total_price = base_price + audio_price + illustration_price
        
        return JsonResponse({
            'status': 'success',
            'base_price': float(base_price),
            'audio_price': float(audio_price),
            'illustration_price': float(illustration_price),
            'total_price': float(total_price)
        })
        
    except FairyTaleTemplate.DoesNotExist:
        return JsonResponse({'error': 'Сказка не найдена'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)