from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Category, Tag
import re

# Новые модели комментариев определены в comment_models.py

# ==========================================
# НОВЫЕ МОДЕЛИ ДЛЯ РАСШИРЕННОЙ ФУНКЦИОНАЛЬНОСТИ ПЛЕЙЛИСТОВ
# ==========================================

class StoryView(models.Model):
    """Модель для отслеживания просмотров"""
    story = models.ForeignKey(
        'Story',
        on_delete=models.CASCADE,
        related_name='views'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь"
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="IP адрес",
        null=True,
        blank=True
    )
    view_count = models.PositiveIntegerField(
        default=1,
        verbose_name="Количество просмотров"
    )
    first_viewed = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Первый просмотр"
    )
    last_viewed = models.DateTimeField(
        auto_now=True,
        verbose_name="Последний просмотр"
    )
    
    class Meta:
        verbose_name = "Просмотр"
        verbose_name_plural = "Просмотры"
        # Один пользователь/IP может иметь только одну запись на рассказ
        unique_together = [['story', 'user'], ['story', 'ip_address']]
        indexes = [
            models.Index(fields=['story', 'user']),
            models.Index(fields=['story', 'ip_address']),
        ]
    
    def __str__(self):
        if self.user:
            return f"{self.user.username} смотрел {self.story.title} ({self.view_count} раз)"
        return f"IP {self.ip_address} смотрел {self.story.title} ({self.view_count} раз)"

class StoryRecommendation(models.Model):
    """Модель для системы рекомендаций"""
    source_story = models.ForeignKey(
        'Story',
        on_delete=models.CASCADE,
        related_name='source_recommendations',
        verbose_name="Исходный рассказ"
    )
    recommended_story = models.ForeignKey(
        'Story',
        on_delete=models.CASCADE,
        related_name='target_recommendations',
        verbose_name="Рекомендуемый рассказ"
    )
    similarity_score = models.FloatField(
        default=0.0,
        verbose_name="Оценка сходства",
        help_text="От 0.0 до 1.0"
    )
    recommendation_type = models.CharField(
        max_length=50,
        choices=[
            ('category', 'По категории'),
            ('tags', 'По тегам'),
            ('popularity', 'По популярности'),
            ('collaborative', 'Коллаборативная фильтрация'),
            ('content', 'По содержанию'),
        ],
        default='category',
        verbose_name="Тип рекомендации"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    
    class Meta:
        verbose_name = "Рекомендация"
        verbose_name_plural = "Рекомендации"
        unique_together = ['source_story', 'recommended_story']
        ordering = ['-similarity_score', '-created_at']
        indexes = [
            models.Index(fields=['source_story', 'similarity_score']),
            models.Index(fields=['recommendation_type']),
        ]
    
    def __str__(self):
        return f"Для '{self.source_story.title}' рекомендуем '{self.recommended_story.title}' ({self.similarity_score:.2f})"

# ==========================================
# ОБНОВЛЕННЫЕ МОДЕЛИ
# ==========================================

class Playlist(models.Model):
    """Модель для плейлистов видео"""
    PLAYLIST_TYPES = [
        ('public', 'Публичный'),
        ('private', 'Приватный'),
        ('featured', 'Рекомендуемый'),
        ('series', 'Серия'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название плейлиста")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL (slug)")
    description = models.TextField(blank=True, verbose_name="Описание")
    creator = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='playlists',
        verbose_name="Создатель"
    )
    stories = models.ManyToManyField(
        'Story', 
        through='PlaylistItem',
        related_name='playlists',
        verbose_name="Рассказы"
    )
    playlist_type = models.CharField(
        max_length=20, 
        choices=PLAYLIST_TYPES, 
        default='public',
        verbose_name="Тип плейлиста"
    )
    cover_image = models.ImageField(
        upload_to='playlists/covers/', 
        blank=True, 
        null=True,
        verbose_name="Обложка плейлиста"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Плейлист"
        verbose_name_plural = "Плейлисты"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('stories:playlist_detail', kwargs={'slug': self.slug})
    
    @property
    def stories_count(self):
        """Количество рассказов в плейлисте"""
        return self.playlist_items.count()
    
    @property
    def total_duration(self):
        """Общая длительность плейлиста"""
        # Логика подсчета длительности
        return "Расчет длительности"
    
    def increment_views(self):
        """Увеличивает счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def can_be_edited_by(self, user):
        """Проверяет, может ли пользователь редактировать плейлист"""
        return self.creator == user or user.is_staff
    
    # Добавляем свойства для совместимости с новыми views
    @property
    def name(self):
        """Алиас для title для совместимости"""
        return self.title
    
    @property
    def user(self):
        """Алиас для creator для совместимости"""
        return self.creator
    
    @property
    def is_public(self):
        """Проверяет, является ли плейлист публичным"""
        return self.playlist_type == 'public'
    
    @property
    def is_featured(self):
        """Проверяет, является ли плейлист рекомендуемым"""
        return self.playlist_type == 'featured'
    
    @property
    def story_count(self):
        """Алиас для stories_count"""
        return self.stories_count
    
    def get_public_url(self):
        """Получить публичную ссылку на плейлист"""
        if self.is_public:
            return reverse('stories:public_playlist_detail', kwargs={
                'user_id': self.creator.id,
                'slug': self.slug
            })
        return None

class PlaylistItem(models.Model):
    """Модель для элементов плейлиста (обновленная)"""
    playlist = models.ForeignKey(
        Playlist, 
        on_delete=models.CASCADE,
        related_name='playlist_items',  # Возвращаем старое название для совместимости
        verbose_name="Плейлист"
    )
    story = models.ForeignKey(
        'Story', 
        on_delete=models.CASCADE,
        related_name='playlist_items',
        verbose_name="Рассказ"
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Порядок",
        help_text="Порядок в плейлисте"
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено"
    )
    
    class Meta:
        verbose_name = "Элемент плейлиста"
        verbose_name_plural = "Элементы плейлиста"
        ordering = ['order', 'added_at']
        unique_together = ('playlist', 'story')  # Обеспечиваем, что рассказ может быть только один раз в плейлисте
        indexes = [
            models.Index(fields=['playlist', 'order']),
            models.Index(fields=['story']),
        ]
    
    def __str__(self):
        return f"{self.playlist.title} - {self.story.title} (позиция {self.order})"  # Используем playlist.title
    
    def save(self, *args, **kwargs):
        # Автоматически устанавливаем порядок, если он не указан
        if not self.order:
            last_item = PlaylistItem.objects.filter(
                playlist=self.playlist
            ).order_by('-order').first()
            self.order = (last_item.order + 1) if last_item else 1
        
        super().save(*args, **kwargs)

class Story(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL (slug)")
    description = models.TextField(verbose_name="Описание")
    youtube_url = models.URLField(
        verbose_name="YouTube URL",
        help_text="Ссылка на видео YouTube (например: https://www.youtube.com/watch?v=VIDEO_ID)"
    )
    youtube_embed_id = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="YouTube ID",
        help_text="Автоматически извлекается из URL"
    )
    duration = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Длительность",
        help_text="Например: 15:32"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Категория"
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемое")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    # Наша простая система комментариев работает через ForeignKey в StoryComment

    class Meta:
        verbose_name = "Рассказ"
        verbose_name_plural = "Рассказы"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоматическое создание slug из заголовка
        if not self.slug:
            # Транслитерация кириллицы
            self.slug = self.create_safe_slug(self.title)
        
        # Извлечение YouTube ID из URL
        if self.youtube_url and not self.youtube_embed_id:
            self.youtube_embed_id = self.extract_youtube_id(self.youtube_url)
        
        super().save(*args, **kwargs)
    
    def create_safe_slug(self, title):
        """Создает безопасный slug с транслитерацией"""
        # Словарь для транслитерации
        cyrillic_to_latin = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
            'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
            'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
            'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
            'э': 'e', 'ю': 'yu', 'я': 'ya',
            
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
            'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
            'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
            'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
            'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch',
            'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
            'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
        }
        
        # Транслитерируем кириллицу
        transliterated = ""
        for char in title:
            if char in cyrillic_to_latin:
                transliterated += cyrillic_to_latin[char]
            else:
                transliterated += char
        
        # Создаем slug
        slug = slugify(transliterated)
        
        # Если slug пустой, создаем уникальный
        if not slug:
            slug = f"story-{hash(title) % 100000}"
        
        # Проверяем уникальность
        original_slug = slug
        counter = 1
        while Story.objects.filter(slug=slug).exclude(id=self.id if self.id else None).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        return slug

    def extract_youtube_id(self, url):
        """Извлекает YouTube ID из различных форматов URL"""
        patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^&\n?#]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^&\n?#]+)',
            r'(?:https?://)?(?:www\.)?youtu\.be/([^&\n?#]+)',
            r'(?:https?://)?(?:www\.)?youtube\.com/v/([^&\n?#]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return ''

    def get_absolute_url(self):
        return reverse('stories:detail', kwargs={'slug': self.slug})

    def get_youtube_embed_url(self):
        """Возвращает URL для встраивания YouTube видео"""
        if self.youtube_embed_id:
            return f"https://www.youtube.com/embed/{self.youtube_embed_id}"
        return None
    
    @property
    def youtube_id(self):
        """Алиас для youtube_embed_id"""
        return self.youtube_embed_id

    def increment_views(self):
        """Увеличивает счетчик просмотров"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    @property
    def video_url(self):
        """Алиас для youtube_url"""
        return self.youtube_url

class StoryLike(models.Model):
    """Модель для лайков рассказов"""
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('story', 'user')
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f"{self.user.username} лайкнул {self.story.title}"

# Модели комментариев перенесены в comment_models.py

class SearchQuery(models.Model):
    """Модель для отслеживания популярных запросов"""
    query = models.CharField(max_length=255, verbose_name="Запрос")
    count = models.PositiveIntegerField(default=1, verbose_name="Количество поисков")
    last_searched = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Поисковый запрос"
        verbose_name_plural = "Поисковые запросы"
        ordering = ['-count', '-last_searched']
    
    def __str__(self):
        return f"{self.query} ({self.count} раз)"
    
    @classmethod
    def log_search(cls, query):
        """Логирование поискового запроса"""
        if query and len(query.strip()) > 2:
            search_query, created = cls.objects.get_or_create(
                query=query.strip().lower()
            )
            if not created:
                search_query.count += 1
                search_query.save()
            return search_query
        return None
    
    @classmethod
    def get_popular_queries(cls, limit=10):
        """Получение популярных запросов"""
        return cls.objects.filter(count__gte=2)[:limit]

class UserRecommendation(models.Model):
    """Модель для персональных рекомендаций"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    story = models.ForeignKey(
        'Story',
        on_delete=models.CASCADE,
        related_name='user_recommendations'
    )
    score = models.FloatField(default=0.0, verbose_name="Оценка релевантности")
    reason = models.CharField(
        max_length=100,
        choices=[
            ('similar_category', 'Похожая категория'),
            ('similar_tags', 'Похожие теги'),
            ('popular', 'Популярное'),
            ('new', 'Новое'),
            ('similar_users', 'Похожие пользователи'),
        ],
        verbose_name="Причина рекомендации"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_viewed = models.BooleanField(default=False, verbose_name="Просмотрено")
    
    class Meta:
        verbose_name = "Рекомендация"
        verbose_name_plural = "Рекомендации"
        ordering = ['-score', '-created_at']
        unique_together = ('user', 'story')
    
    def __str__(self):
        return f"Рекомендация для {self.user.username}: {self.story.title}"

class UserWatchHistory(models.Model):
    """Модель для истории просмотров пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='watch_history'
    )
    story = models.ForeignKey(
        'Story',
        on_delete=models.CASCADE,
        related_name='user_views'
    )
    watched_at = models.DateTimeField(auto_now_add=True)
    watch_duration = models.PositiveIntegerField(
        default=0, 
        verbose_name="Длительность просмотра (сек)"
    )
    completed = models.BooleanField(
        default=False, 
        verbose_name="Просмотрено полностью"
    )
    
    class Meta:
        verbose_name = "История просмотров"
        verbose_name_plural = "История просмотров"
        ordering = ['-watched_at']
    
    def __str__(self):
        return f"{self.user.username} смотрел {self.story.title}"


# ==========================================
# YOUTUBE-STYLE СИСТЕМА КОММЕНТАРИЕВ
# ==========================================

class StoryComment(models.Model):
    """Модель комментариев к рассказам (YouTube-style)"""
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Рассказ'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Максимум 1000 символов'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Родительский комментарий'
    )
    
    # Статистика
    likes_count = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    dislikes_count = models.PositiveIntegerField(default=0, verbose_name='Дизлайки')
    replies_count = models.PositiveIntegerField(default=0, verbose_name='Ответы')
    
    # Модерация
    is_approved = models.BooleanField(default=True, verbose_name='Одобрен')
    is_pinned = models.BooleanField(default=False, verbose_name='Закреплен')
    is_edited = models.BooleanField(default=False, verbose_name='Отредактирован')
    
    # Временные метки
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['story', '-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['parent']),
        ]
    
    def __str__(self):
        return f'{self.user.username}: {self.text[:50]}...'
    
    @property
    def is_reply(self):
        """Проверяет, является ли комментарий ответом"""
        return self.parent is not None
    
    @property
    def thread_replies(self):
        """Получает все ответы в треде"""
        if self.is_reply:
            return self.parent.replies.filter(is_approved=True)
        return self.replies.filter(is_approved=True)
    
    def get_reaction_score(self):
        """Получает общий счет реакций"""
        return self.likes_count - self.dislikes_count
    
    def save(self, *args, **kwargs):
        # Ограничиваем длину комментария
        if len(self.text) > 1000:
            self.text = self.text[:1000]
        
        # Обновляем счетчик ответов у родительского комментария
        if self.parent and not self.pk:
            self.parent.replies_count = self.parent.replies.count() + 1
            self.parent.save(update_fields=['replies_count'])
        
        super().save(*args, **kwargs)


class CommentReaction(models.Model):
    """Модель реакций на комментарии (лайки/дизлайки)"""
    
    REACTION_CHOICES = [
        ('like', 'Лайк'),
        ('dislike', 'Дизлайк'),
    ]
    
    comment = models.ForeignKey(
        StoryComment,
        on_delete=models.CASCADE,
        related_name='reactions',
        verbose_name='Комментарий'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    reaction_type = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES,
        verbose_name='Тип реакции'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    
    class Meta:
        verbose_name = 'Реакция на комментарий'
        verbose_name_plural = 'Реакции на комментарии'
        unique_together = ['comment', 'user']  # Один пользователь = одна реакция
        indexes = [
            models.Index(fields=['comment', 'reaction_type']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f'{self.user.username} {self.get_reaction_type_display()} {self.comment.id}'
    
    def save(self, *args, **kwargs):
        # Обновляем счетчики у комментария
        if self.pk:
            # Если редактируем существующую реакцию
            old_reaction = CommentReaction.objects.get(pk=self.pk)
            if old_reaction.reaction_type != self.reaction_type:
                # Уменьшаем старый счетчик
                if old_reaction.reaction_type == 'like':
                    self.comment.likes_count = max(0, self.comment.likes_count - 1)
                else:
                    self.comment.dislikes_count = max(0, self.comment.dislikes_count - 1)
                
                # Увеличиваем новый счетчик
                if self.reaction_type == 'like':
                    self.comment.likes_count += 1
                else:
                    self.comment.dislikes_count += 1
                
                self.comment.save(update_fields=['likes_count', 'dislikes_count'])
        else:
            # Новая реакция
            if self.reaction_type == 'like':
                self.comment.likes_count += 1
            else:
                self.comment.dislikes_count += 1
            
            self.comment.save(update_fields=['likes_count', 'dislikes_count'])
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Уменьшаем счетчики при удалении
        if self.reaction_type == 'like':
            self.comment.likes_count = max(0, self.comment.likes_count - 1)
        else:
            self.comment.dislikes_count = max(0, self.comment.dislikes_count - 1)
        
        self.comment.save(update_fields=['likes_count', 'dislikes_count'])
        super().delete(*args, **kwargs)


class CommentReport(models.Model):
    """Модель жалоб на комментарии"""
    
    REPORT_REASONS = [
        ('spam', 'Спам'),
        ('hate', 'Разжигание ненависти'),
        ('harassment', 'Притеснение'),
        ('violence', 'Насилие'),
        ('inappropriate', 'Неподходящий контент'),
        ('other', 'Другое'),
    ]
    
    comment = models.ForeignKey(
        StoryComment,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='Комментарий'
    )
    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Жалобщик'
    )
    reason = models.CharField(
        max_length=20,
        choices=REPORT_REASONS,
        verbose_name='Причина жалобы'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Дополнительное описание'
    )
    is_resolved = models.BooleanField(default=False, verbose_name='Рассмотрена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    
    class Meta:
        verbose_name = 'Жалоба на комментарий'
        verbose_name_plural = 'Жалобы на комментарии'
        unique_together = ['comment', 'reporter']  # Одна жалоба от пользователя
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Жалоба от {self.reporter.username} на комментарий {self.comment.id}'


class UserPlaylistPreference(models.Model):
    """Настройки пользователя для плейлистов"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='playlist_preferences'
    )
    
    # Системные плейлисты
    watch_later_playlist = models.ForeignKey(
        'Playlist',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='watch_later_users',
        verbose_name="Плейлист 'Посмотреть позже'"
    )
    
    favorites_playlist = models.ForeignKey(
        'Playlist',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='favorites_users',
        verbose_name="Плейлист 'Избранное'"
    )
    
    # Настройки автовоспроизведения
    autoplay_enabled = models.BooleanField(
        default=True,
        verbose_name="Автовоспроизведение"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Настройки плейлистов пользователя"
        verbose_name_plural = "Настройки плейлистов пользователей"

    def get_or_create_watch_later(self):
        """Создает или возвращает плейлист 'Посмотреть позже'"""
        if not self.watch_later_playlist:
            playlist = Playlist.objects.create(
                title="Посмотреть позже",
                slug=f"watch-later-{self.user.id}",
                creator=self.user,
                playlist_type='private',
                description="Автоматически созданный плейлист для сохранения видео на потом"
            )
            self.watch_later_playlist = playlist
            self.save()
        return self.watch_later_playlist

    def get_or_create_favorites(self):
        """Создает или возвращает плейлист 'Избранное'"""
        if not self.favorites_playlist:
            playlist = Playlist.objects.create(
                title="Избранное",
                slug=f"favorites-{self.user.id}",
                creator=self.user,
                playlist_type='private',
                description="Автоматически созданный плейлист для избранных видео"
            )
            self.favorites_playlist = playlist
            self.save()
        return self.favorites_playlist


# Сигнал для автоматического создания настроек плейлистов
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_playlist_preferences(sender, instance, created, **kwargs):
    """Создаем настройки плейлистов для нового пользователя"""
    if created:
        UserPlaylistPreference.objects.create(user=instance)
