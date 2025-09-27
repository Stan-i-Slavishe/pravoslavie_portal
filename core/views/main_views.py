from django.views.generic import TemplateView, ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json
from ..models import Category, Tag, ContactMessage, SiteSettings, MobileFeedback
from ..forms import ContactForm
from ..seo import page_meta  # Правильный импорт из пакета seo
from django.contrib.auth.decorators import login_required

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        
        # SEO мета-теги
        context['page_key'] = 'home'
        context['seo'] = page_meta('home', request=self.request)
        
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
        
        # SEO мета-теги
        context['page_key'] = 'about'
        context['seo'] = page_meta('about', request=self.request)
        
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
                fail_silently=False
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
    
    def get(self, request, *args, **kwargs):
        """Переопределяем GET для возможности перенаправления"""
        category = get_object_or_404(
            Category, 
            slug=kwargs['slug'], 
            is_active=True
        )
        
        # АВТОМАТИЧЕСКОЕ ПЕРЕНАПРАВЛЕНИЕ для категорий stories
        if category.content_type == 'story' and request.GET.get('redirect', '1') == '1':
            # Проверяем, есть ли рассказы в этой категории
            try:
                from stories.models import Story
                stories_count = Story.objects.filter(
                    category=category,
                    is_published=True
                ).count()
                
                # Если есть рассказы, перенаправляем сразу
                if stories_count > 0:
                    return redirect(f"/stories/?category={category.slug}")
                    
            except ImportError:
                pass
        
        # Если не перенаправляем, показываем обычную страницу
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category = get_object_or_404(
            Category, 
            slug=kwargs['slug'], 
            is_active=True
        )
        
        context['category'] = category
        context['title'] = category.name
        
        # ИСПРАВЛЕНИЕ: Загружаем контент в зависимости от типа категории
        content_items = []
        
        # Для категорий типа 'story' загружаем видео-рассказы
        if category.content_type == 'story':
            try:
                from stories.models import Story
                stories = Story.objects.filter(
                    category=category,
                    is_published=True
                ).select_related('category').prefetch_related('tags').order_by('-created_at')[:12]
                
                for story in stories:
                    content_items.append({
                        'title': story.title,
                        'description': story.description,
                        'content_type': 'Видео-рассказ',
                        'url': story.get_absolute_url(),
                        'image': story.get_thumbnail_url(),
                        'created_at': story.created_at,
                        'views_count': story.views_count,
                        'duration': story.duration,
                        'youtube_id': story.youtube_embed_id,
                    })
                    
            except ImportError:
                pass
        
        # Для категорий типа 'book' загружаем книги
        elif category.content_type == 'book':
            try:
                from books.models import Book
                books = Book.objects.filter(
                    category=category,
                    is_published=True
                ).select_related('category').prefetch_related('tags').order_by('-created_at')[:12]
                
                for book in books:
                    content_items.append({
                        'title': book.title,
                        'description': book.description,
                        'content_type': 'Книга',
                        'url': book.get_absolute_url(),
                        'image': book.cover.url if book.cover else None,
                        'created_at': book.created_at,
                        'price': book.price,
                    })
                    
            except ImportError:
                pass
        
        # Для категорий типа 'audio' загружаем аудио
        elif category.content_type == 'audio':
            try:
                from audio.models import AudioTrack
                audio_tracks = AudioTrack.objects.filter(
                    category=category,
                    is_published=True
                ).select_related('category').prefetch_related('tags').order_by('-created_at')[:12]
                
                for audio in audio_tracks:
                    content_items.append({
                        'title': audio.title,
                        'description': getattr(audio, 'description', ''),
                        'content_type': 'Аудио',
                        'url': audio.get_absolute_url(),
                        'image': getattr(audio, 'cover_image', None).url if getattr(audio, 'cover_image', None) else None,
                        'created_at': audio.created_at,
                        'duration': getattr(audio, 'duration', None),
                    })
                    
            except (ImportError, AttributeError):
                pass
        
        # Также загружаем связанные сказки
        try:
            from fairy_tales.models import FairyTale
            fairy_tales = FairyTale.objects.filter(
                category__slug=category.slug,  # Ищем по slug для совместимости
                is_published=True
            ).select_related('category', 'age_group').prefetch_related('tags').order_by('-created_at')[:6]
            
            for fairy_tale in fairy_tales:
                content_items.append({
                    'title': fairy_tale.title,
                    'description': getattr(fairy_tale, 'description', ''),
                    'content_type': 'Сказка',
                    'url': fairy_tale.get_absolute_url(),
                    'image': getattr(fairy_tale, 'cover_image', None).url if getattr(fairy_tale, 'cover_image', None) else None,
                    'created_at': fairy_tale.created_at,
                    'age_group': getattr(fairy_tale, 'age_group', None).name if getattr(fairy_tale, 'age_group', None) else None,
                })
        except (ImportError, AttributeError):
            pass
        
        context['content_items'] = content_items
        context['has_content'] = len(content_items) > 0
        
        # Альтернативные ссылки для пустых категорий или когда хотим показать специализированную страницу
        if category.content_type == 'story':
            context['alternative_url'] = f"/stories/?category={category.slug}"
            context['alternative_text'] = "Перейти к видео-рассказам"
        elif category.content_type == 'book':
            context['alternative_url'] = f"/books/?category={category.slug}"
            context['alternative_text'] = "Перейти к книгам"
        elif category.content_type == 'audio':
            context['alternative_url'] = f"/audio/?category={category.slug}"
            context['alternative_text'] = "Перейти к аудио"
        
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
        
        # ИСПРАВЛЕНИЕ: Загружаем контент с этим тегом
        content_items = []
        
        # Получаем истории с этим тегом
        try:
            from stories.models import Story
            stories = Story.objects.filter(
                tags__id=tag.id,
                is_published=True
            ).select_related('category').prefetch_related('tags')[:20]
            
            for story in stories:
                content_items.append({
                    'title': story.title,
                    'description': story.description,
                    'content_type': 'Видео-рассказ',
                    'get_absolute_url': story.get_absolute_url(),
                    'image': story.get_thumbnail_url(),
                    'created_at': story.created_at,
                    'category': story.category.name if story.category else None,
                    'views_count': story.views_count,
                })
        except ImportError:
            pass
        
        # Получаем книги с этим тегом
        try:
            from books.models import Book
            books = Book.objects.filter(
                tags__id=tag.id,
                is_published=True
            ).select_related('category').prefetch_related('tags')[:20]
            
            for book in books:
                content_items.append({
                    'title': book.title,
                    'description': book.description,
                    'content_type': 'Книга',
                    'get_absolute_url': book.get_absolute_url(),
                    'image': book.cover.url if book.cover else None,
                    'created_at': book.created_at,
                    'category': book.category.name if book.category else None,
                    'price': book.price,
                })
        except ImportError:
            pass
        
        # Получаем аудио с этим тегом
        try:
            from audio.models import AudioTrack
            audio_tracks = AudioTrack.objects.filter(
                tags__id=tag.id,
                is_published=True
            ).select_related('category').prefetch_related('tags')[:20]
            
            for audio in audio_tracks:
                content_items.append({
                    'title': audio.title,
                    'description': getattr(audio, 'description', ''),
                    'content_type': 'Аудио',
                    'get_absolute_url': audio.get_absolute_url(),
                    'image': getattr(audio, 'cover_image', None).url if getattr(audio, 'cover_image', None) else None,
                    'created_at': audio.created_at,
                    'category': audio.category.name if audio.category else None,
                    'duration': getattr(audio, 'duration', None),
                })
        except (ImportError, AttributeError):
            pass
        
        # Получаем сказки с этим тегом
        try:
            from fairy_tales.models import FairyTale
            fairy_tales = FairyTale.objects.filter(
                tags__id=tag.id,
                is_published=True
            ).select_related('category', 'age_group').prefetch_related('tags')[:20]
            
            for fairy_tale in fairy_tales:
                content_items.append({
                    'title': fairy_tale.title,
                    'description': getattr(fairy_tale, 'description', ''),
                    'content_type': 'Сказка',
                    'get_absolute_url': fairy_tale.get_absolute_url(),
                    'image': getattr(fairy_tale, 'cover_image', None).url if getattr(fairy_tale, 'cover_image', None) else None,
                    'created_at': fairy_tale.created_at,
                    'category': fairy_tale.category.name if fairy_tale.category else None,
                    'age_group': getattr(fairy_tale, 'age_group', None).name if getattr(fairy_tale, 'age_group', None) else None,
                })
        except (ImportError, AttributeError):
            pass
        
        # Сортируем по дате создания (новые сначала)
        content_items.sort(key=lambda x: x['created_at'], reverse=True)
        
        context['content_items'] = content_items
        
        return context

def custom_404_view(request, exception):
    """Кастомная страница 404"""
    return render(request, '404.html', status=404)

def custom_500_view(request):
    """Кастомная страница 500"""
    return render(request, '500.html', status=500)


@method_decorator(csrf_exempt, name='dispatch')
class MobileFeedbackView(View):
    """AJAX обработчик для мобильной обратной связи"""
    
    def post(self, request):
        try:
            # Парсим JSON данные
            data = json.loads(request.body)
            
            # Валидация обязательных полей
            feedback_type = data.get('type')
            message = data.get('message', '').strip()
            
            if not feedback_type or not message:
                return JsonResponse({
                    'success': False,
                    'error': 'Пожалуйста, выберите тип обращения и введите сообщение'
                }, status=400)
            
            # Проверяем валидность типа обращения
            valid_types = [choice[0] for choice in MobileFeedback.FEEDBACK_TYPES]
            if feedback_type not in valid_types:
                return JsonResponse({
                    'success': False,
                    'error': 'Неверный тип обращения'
                }, status=400)
            
            # Получаем IP адрес пользователя
            def get_client_ip(request):
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                return ip
            
            # Создаем запись обратной связи
            feedback = MobileFeedback.objects.create(
                feedback_type=feedback_type,
                message=message,
                user=request.user if request.user.is_authenticated else None,
                user_agent=data.get('userAgent', request.META.get('HTTP_USER_AGENT', '')),
                url=data.get('url', ''),
                ip_address=get_client_ip(request),
                screen_resolution=data.get('screenResolution', ''),
                # Автоматически устанавливаем высокий приоритет для багов
                priority='high' if feedback_type == 'bug' else 'medium'
            )
            
            # Отправляем email уведомление администратору (опционально)
            if hasattr(settings, 'FEEDBACK_EMAIL_NOTIFICATIONS') and settings.FEEDBACK_EMAIL_NOTIFICATIONS:
                self.send_admin_notification(feedback)
            
            return JsonResponse({
                'success': True,
                'message': 'Спасибо за ваш отзыв! Мы обязательно его рассмотрим.',
                'feedback_id': feedback.id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Неверный формат данных'
            }, status=400)
            
        except Exception as e:
            # Логируем ошибку для отладки
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Ошибка при сохранении мобильной обратной связи: {e}")
            
            return JsonResponse({
                'success': False,
                'error': 'Произошла ошибка при отправке обратной связи. Попробуйте ещё раз.'
            }, status=500)
    
    def send_admin_notification(self, feedback):
        """Отправка email уведомления администратору"""
        try:
            site_settings = SiteSettings.get_settings()
            
            subject = f"[{site_settings.site_name}] Новая мобильная обратная связь: {feedback.get_feedback_type_display()}"
            
            message = f"""
Получена новая обратная связь через мобильное приложение:

Тип: {feedback.get_feedback_type_display()}
Сообщение: {feedback.message}

Техническая информация:
Пользователь: {feedback.user.username if feedback.user else 'Анонимный'}
IP адрес: {feedback.ip_address}
URL: {feedback.url}
User Agent: {feedback.user_agent}
Разрешение экрана: {feedback.screen_resolution}

Посмотреть в админке: {settings.SITE_URL}/admin/core/mobilefeedback/{feedback.id}/change/
"""
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [site_settings.contact_email],
                fail_silently=False
            )
            
        except Exception as e:
            # Не прерываем процесс, если отправка email не удалась
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Не удалось отправить email уведомление: {e}")
    
    def get(self, request):
        """GET запрос не поддерживается"""
        return JsonResponse({
            'success': False,
            'error': 'Метод GET не поддерживается для этого API'
        }, status=405)


class DonateView(TemplateView):
    """Страница поддержки проекта"""
    template_name = 'core/donate.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поддержать проект'
        
        # SEO мета-теги
        context['page_key'] = 'donate'
        context['seo'] = page_meta('donate', request=self.request)
        
        # Данные для ЮMoney
        context['yumoney_account'] = '5599002068582453'
        context['yumoney_formatted'] = '5599 0020 6858 2453'
        
        # Настройки сайта
        context['site_settings'] = SiteSettings.get_settings()
        
        return context
