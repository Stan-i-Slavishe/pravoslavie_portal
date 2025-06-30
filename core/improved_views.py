from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404
from django.db.models import Count, Q
from django.contrib.auth.models import User
from .models import Category, Tag, ContactMessage, SiteSettings

# Импорты для статистики (если приложения существуют)
try:
    from stories.models import Story
except ImportError:
    Story = None

try:
    from books.models import Book
except ImportError:
    Book = None

try:
    from audio.models import Audio
except ImportError:
    Audio = None


class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        
        # Получаем категории по типам контента с цветами
        context['story_categories'] = Category.objects.filter(
            content_type='story', 
            is_active=True
        ).order_by('order', 'name')[:4]
        
        context['book_categories'] = Category.objects.filter(
            content_type='book', 
            is_active=True
        ).order_by('order', 'name')[:4]
        
        context['audio_categories'] = Category.objects.filter(
            content_type='audio', 
            is_active=True
        ).order_by('order', 'name')[:4]
        
        # Популярные теги с подсчетом использования
        context['popular_tags'] = Tag.objects.filter(
            is_active=True
        ).annotate(
            usage_count=Count('story') + Count('book') + Count('audio')
        ).order_by('-usage_count', 'name')[:12]
        
        # Статистика для счетчиков
        context.update(self.get_statistics())
        
        # Настройки сайта
        context['site_settings'] = SiteSettings.get_settings()
        
        # Последний контент (опционально)
        context.update(self.get_recent_content())
        
        return context
    
    def get_statistics(self):
        """Получить статистику для отображения"""
        stats = {}
        
        # Подсчет историй
        if Story:
            stats['total_stories'] = Story.objects.filter(
                is_published=True
            ).count()
        else:
            stats['total_stories'] = 0
        
        # Подсчет книг
        if Book:
            stats['total_books'] = Book.objects.filter(
                is_published=True
            ).count()
        else:
            stats['total_books'] = 0
        
        # Подсчет аудио
        if Audio:
            stats['total_audio'] = Audio.objects.filter(
                is_published=True
            ).count()
        else:
            stats['total_audio'] = 0
        
        # Подсчет пользователей
        stats['total_users'] = User.objects.filter(
            is_active=True
        ).count()
        
        # Подсчет категорий
        stats['total_categories'] = Category.objects.filter(
            is_active=True
        ).count()
        
        # Подсчет тегов
        stats['total_tags'] = Tag.objects.filter(
            is_active=True
        ).count()
        
        return stats
    
    def get_recent_content(self):
        """Получить последний контент"""
        recent = {}
        
        # Последние истории
        if Story:
            recent['recent_stories'] = Story.objects.filter(
                is_published=True
            ).order_by('-created_at')[:3]
        
        # Последние книги
        if Book:
            recent['recent_books'] = Book.objects.filter(
                is_published=True
            ).order_by('-created_at')[:3]
        
        # Последнее аудио
        if Audio:
            recent['recent_audio'] = Audio.objects.filter(
                is_published=True
            ).order_by('-created_at')[:3]
        
        return recent


class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О проекте'
        context['site_settings'] = SiteSettings.get_settings()
        
        # Добавляем статистику на страницу "О проекте"
        context.update(self.get_about_statistics())
        
        return context
    
    def get_about_statistics(self):
        """Статистика для страницы о проекте"""
        stats = {}
        
        # Общая статистика контента
        total_content = 0
        if Story:
            story_count = Story.objects.filter(is_published=True).count()
            stats['story_count'] = story_count
            total_content += story_count
        
        if Book:
            book_count = Book.objects.filter(is_published=True).count()
            stats['book_count'] = book_count
            total_content += book_count
        
        if Audio:
            audio_count = Audio.objects.filter(is_published=True).count()
            stats['audio_count'] = audio_count
            total_content += audio_count
        
        stats['total_content'] = total_content
        stats['active_categories'] = Category.objects.filter(is_active=True).count()
        stats['active_tags'] = Tag.objects.filter(is_active=True).count()
        
        return stats


class ContactView(TemplateView):
    template_name = 'core/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        context['form'] = ContactForm()
        context['site_settings'] = SiteSettings.get_settings()
        return context
    
    def post(self, request, *args, **kwargs):
        from .forms import ContactForm
        
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Создаем сообщение
            contact_message = form.save(commit=False)
            
            # Добавляем техническую информацию
            contact_message.ip_address = self.get_client_ip(request)
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            # Если пользователь авторизован, сохраняем связь
            if request.user.is_authenticated:
                contact_message.user = request.user
            
            contact_message.save()
            
            # Отправляем email уведомление
            self.send_notification_email(contact_message)
            
            messages.success(
                request, 
                'Спасибо за ваше сообщение! Мы обязательно свяжемся с вами в ближайшее время.',
                extra_tags='contact-success'
            )
            return redirect('core:contact')
        
        # Если форма невалидна
        messages.error(
            request,
            'Пожалуйста, исправьте ошибки в форме.',
            extra_tags='contact-error'
        )
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)
    
    def get_client_ip(self, request):
        """Получить IP адрес клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def send_notification_email(self, contact_message):
        """Отправить уведомление о новом сообщении"""
        try:
            site_settings = SiteSettings.get_settings()
            
            subject = f'Новое сообщение с сайта: {contact_message.get_subject_display()}'
            message = f'''
Получено новое сообщение с сайта {site_settings.site_name}

Отправитель: {contact_message.name}
Email: {contact_message.email}
Телефон: {getattr(contact_message, 'phone', 'Не указан')}
Тема: {contact_message.get_subject_display()}

Сообщение:
{contact_message.message}

IP адрес: {contact_message.ip_address}
User Agent: {contact_message.user_agent[:100]}...
Дата: {contact_message.created_at.strftime('%d.%m.%Y %H:%M')}

Для ответа перейдите в админ-панель.
            '''
            
            # Получаем список администраторов
            admin_emails = []
            if hasattr(site_settings, 'contact_email') and site_settings.contact_email:
                admin_emails.append(site_settings.contact_email)
            
            # Добавляем email суперпользователей
            admin_emails.extend(
                User.objects.filter(
                    is_superuser=True, 
                    is_active=True,
                    email__isnull=False
                ).exclude(email='').values_list('email', flat=True)
            )
            
            if admin_emails:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=list(set(admin_emails)),  # Убираем дубликаты
                    fail_silently=True
                )
        except Exception as e:
            # Логируем ошибку
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Ошибка отправки уведомления о контакте: {e}')


class CategoryListView(ListView):
    model = Category
    template_name = 'core/categories.html'
    context_object_name = 'categories'
    paginate_by = 24
    
    def get_queryset(self):
        queryset = Category.objects.filter(is_active=True)
        
        # Фильтрация по типу контента
        content_type = self.request.GET.get('type')
        if content_type in ['story', 'book', 'audio']:
            queryset = queryset.filter(content_type=content_type)
        
        # Поиск
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset.order_by('order', 'name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
        context['current_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        # Статистика по типам
        context['type_stats'] = {
            'story': Category.objects.filter(content_type='story', is_active=True).count(),
            'book': Category.objects.filter(content_type='book', is_active=True).count(),
            'audio': Category.objects.filter(content_type='audio', is_active=True).count(),
        }
        
        return context


class CategoryDetailView(TemplateView):
    template_name = 'core/category_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category = get_object_or_404(
            Category, 
            slug=kwargs['slug'], 
            is_active=True
        )
        
        context['category'] = category
        context['title'] = category.name
        
        # Получаем связанный контент
        context.update(self.get_category_content(category))
        
        return context
    
    def get_category_content(self, category):
        """Получить контент категории"""
        content = {}
        
        # Контент по типу категории
        if category.content_type == 'story' and Story:
            content['stories'] = Story.objects.filter(
                categories=category,
                is_published=True
            ).order_by('-created_at')[:12]
            content['stories_count'] = Story.objects.filter(
                categories=category,
                is_published=True
            ).count()
        
        elif category.content_type == 'book' and Book:
            content['books'] = Book.objects.filter(
                categories=category,
                is_published=True
            ).order_by('-created_at')[:12]
            content['books_count'] = Book.objects.filter(
                categories=category,
                is_published=True
            ).count()
        
        elif category.content_type == 'audio' and Audio:
            content['audio_items'] = Audio.objects.filter(
                categories=category,
                is_published=True
            ).order_by('-created_at')[:12]
            content['audio_count'] = Audio.objects.filter(
                categories=category,
                is_published=True
            ).count()
        
        return content


class TagListView(ListView):
    model = Tag
    template_name = 'core/tags.html'
    context_object_name = 'tags'
    paginate_by = 60
    
    def get_queryset(self):
        queryset = Tag.objects.filter(is_active=True)
        
        # Поиск по тегам
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Сортировка
        sort_by = self.request.GET.get('sort', 'name')
        if sort_by == 'popular':
            # Сортировка по популярности (количеству использований)
            queryset = queryset.annotate(
                usage_count=Count('story') + Count('book') + Count('audio')
            ).order_by('-usage_count', 'name')
        else:
            queryset = queryset.order_by('name')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Теги'
        context['search_query'] = self.request.GET.get('search', '')
        context['current_sort'] = self.request.GET.get('sort', 'name')
        
        # Статистика тегов
        context['total_tags'] = Tag.objects.filter(is_active=True).count()
        
        return context


class TagDetailView(TemplateView):
    template_name = 'core/tag_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tag = get_object_or_404(
            Tag, 
            slug=kwargs['slug'], 
            is_active=True
        )
        
        context['tag'] = tag
        context['title'] = f'Тег: {tag.name}'
        
        # Получаем весь контент с этим тегом
        context.update(self.get_tag_content(tag))
        
        return context
    
    def get_tag_content(self, tag):
        """Получить весь контент с данным тегом"""
        content = {}
        
        # Истории с тегом
        if Story:
            content['stories'] = Story.objects.filter(
                tags=tag,
                is_published=True
            ).order_by('-created_at')[:6]
            content['stories_count'] = Story.objects.filter(
                tags=tag,
                is_published=True
            ).count()
        
        # Книги с тегом
        if Book:
            content['books'] = Book.objects.filter(
                tags=tag,
                is_published=True
            ).order_by('-created_at')[:6]
            content['books_count'] = Book.objects.filter(
                tags=tag,
                is_published=True
            ).count()
        
        # Аудио с тегом
        if Audio:
            content['audio_items'] = Audio.objects.filter(
                tags=tag,
                is_published=True
            ).order_by('-created_at')[:6]
            content['audio_count'] = Audio.objects.filter(
                tags=tag,
                is_published=True
            ).count()
        
        # Общий счетчик
        content['total_content'] = sum([
            content.get('stories_count', 0),
            content.get('books_count', 0),
            content.get('audio_count', 0)
        ])
        
        return content


# Кастомные представления для ошибок
def custom_404_view(request, exception):
    """Улучшенная страница 404"""
    context = {
        'title': 'Страница не найдена',
        'site_settings': SiteSettings.get_settings(),
        'popular_tags': Tag.objects.filter(is_active=True)[:8],
        'categories': Category.objects.filter(is_active=True)[:6],
    }
    return render(request, '404.html', context, status=404)


def custom_500_view(request):
    """Улучшенная страница 500"""
    context = {
        'title': 'Ошибка сервера',
        'site_settings': SiteSettings.get_settings(),
    }
    return render(request, '500.html', context, status=500)


# Дополнительные API views для AJAX запросов
class SearchSuggestionsView(TemplateView):
    """API для подсказок поиска"""
    
    def get(self, request, *args, **kwargs):
        from django.http import JsonResponse
        
        query = request.GET.get('q', '').strip()
        if len(query) < 2:
            return JsonResponse({'suggestions': []})
        
        suggestions = []
        
        # Подсказки по тегам
        tags = Tag.objects.filter(
            name__icontains=query,
            is_active=True
        )[:5]
        
        for tag in tags:
            suggestions.append({
                'type': 'tag',
                'title': tag.name,
                'url': tag.get_absolute_url(),
                'description': f'Тег'
            })
        
        # Подсказки по категориям
        categories = Category.objects.filter(
            name__icontains=query,
            is_active=True
        )[:5]
        
        for category in categories:
            suggestions.append({
                'type': 'category',
                'title': category.name,
                'url': category.get_absolute_url(),
                'description': f'Категория ({category.get_content_type_display()})'
            })
        
        return JsonResponse({'suggestions': suggestions[:10]})
