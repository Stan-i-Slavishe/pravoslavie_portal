from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404
from .models import Category, Tag, ContactMessage, SiteSettings
from .forms import ContactForm

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        
        # Получаем категории по типам контента
        context['story_categories'] = Category.objects.filter(
            content_type='story', 
            is_active=True
        )[:3]
        context['book_categories'] = Category.objects.filter(
            content_type='book', 
            is_active=True
        )[:3]
        context['audio_categories'] = Category.objects.filter(
            content_type='audio', 
            is_active=True
        )[:3]
        
        # Популярные теги
        context['popular_tags'] = Tag.objects.filter(is_active=True)[:10]
        
        # Настройки сайта
        context['site_settings'] = SiteSettings.get_settings()
        
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О проекте'
        context['site_settings'] = SiteSettings.get_settings()
        
        # Добавляем статистику для страницы "О проекте"
        context['founding_year'] = 2023  # Год основания проекта
        
        try:
            # Импортируем модели только когда они нужны
            from stories.models import Story
            from books.models import Book
            from audio.models import AudioTrack
            
            context['total_stories'] = Story.objects.filter(is_published=True).count()
            context['total_books'] = Book.objects.filter(is_published=True).count()
            context['total_audio'] = AudioTrack.objects.filter(is_published=True).count()
            
        except ImportError:
            # Если модели не найдены, ставим нули
            context['total_stories'] = 0
            context['total_books'] = 0
            context['total_audio'] = 0
            
        return context

class ContactView(TemplateView):
    template_name = 'core/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        context['form'] = ContactForm()
        context['site_settings'] = SiteSettings.get_settings()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Создаем сообщение
            contact_message = form.save(commit=False)
            
            # Добавляем техническую информацию
            contact_message.ip_address = self.get_client_ip(request)
            contact_message.user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            contact_message.save()
            
            # Отправляем email уведомление (если настроено)
            self.send_notification_email(contact_message)
            
            messages.success(
                request, 
                'Спасибо за ваше сообщение! Мы обязательно свяжемся с вами в ближайшее время.'
            )
            return redirect('core:contact')
        
        # Если форма невалидна, показываем ошибки
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)
    
    def get_client_ip(self, request):
        """Получить IP адрес клиента"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
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
Тема: {contact_message.get_subject_display()}

Сообщение:
{contact_message.message}

IP адрес: {contact_message.ip_address}
Дата: {contact_message.created_at}

Для ответа перейдите в админ-панель: {settings.ALLOWED_HOSTS[0]}/admin/
            '''
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[site_settings.contact_email],
                fail_silently=True
            )
        except Exception:
            # Логируем ошибку, но не прерываем процесс
            pass

class CategoryListView(ListView):
    model = Category
    template_name = 'core/categories.html'
    context_object_name = 'categories'
    paginate_by = 20
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категории'
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
        
        # В будущем здесь будем загружать контент категории
        context['content_items'] = []
        
        return context

class TagListView(ListView):
    model = Tag
    template_name = 'core/tags.html'
    context_object_name = 'tags'
    paginate_by = 50
    
    def get_queryset(self):
        return Tag.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Теги'
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
        
        # В будущем здесь будем загружать контент с этим тегом
        context['content_items'] = []
        
        return context

def custom_404_view(request, exception):
    """Кастомная страница 404"""
    return render(request, '404.html', status=404)

def custom_500_view(request):
    """Кастомная страница 500"""
    return render(request, '500.html', status=500)