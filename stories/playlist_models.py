# МОДЕЛИ ПЛЕЙЛИСТОВ ДЛЯ ДОБАВЛЕНИЯ В stories/models.py

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

class Playlist(models.Model):
    """Модель плейлистов для рассказов"""
    
    PLAYLIST_TYPES = [
        ('public', 'Публичный'),
        ('private', 'Приватный'),
        ('unlisted', 'По ссылке'),
    ]
    
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='playlists',
        verbose_name="Создатель"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Название плейлиста"
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name="URL-адрес"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание плейлиста"
    )
    playlist_type = models.CharField(
        max_length=20,
        choices=PLAYLIST_TYPES,
        default='private',
        verbose_name="Тип плейлиста"
    )
    stories_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество рассказов"
    )
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлен"
    )
    
    class Meta:
        verbose_name = "Плейлист"
        verbose_name_plural = "Плейлисты"
        unique_together = ['creator', 'slug']
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['creator', '-updated_at']),
            models.Index(fields=['playlist_type', '-created_at']),
        ]
    
    def __str__(self):
        return f'{self.title} ({self.creator.username})'
    
    def get_absolute_url(self):
        return reverse('stories:playlist_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class PlaylistItem(models.Model):
    """Модель элементов плейлистов"""
    
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name='playlist_items',
        verbose_name="Плейлист"
    )
    story = models.ForeignKey(
        'Story',
        on_delete=models.CASCADE,
        related_name='playlist_items',
        verbose_name="Рассказ"
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name="Порядок"
    )
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлен"
    )
    
    class Meta:
        verbose_name = "Элемент плейлиста"
        verbose_name_plural = "Элементы плейлистов"
        unique_together = ['playlist', 'story']
        ordering = ['order']
        indexes = [
            models.Index(fields=['playlist', 'order']),
            models.Index(fields=['story']),
        ]
    
    def __str__(self):
        return f'{self.story.title} в {self.playlist.title}'


class StoryRecommendation(models.Model):
    """Модель рекомендаций рассказов"""
    
    RECOMMENDATION_TYPES = [
        ('tag_based', 'По тегам'),
        ('category_based', 'По категории'),
        ('user_based', 'Пользовательские'),
        ('popular', 'Популярные'),
    ]
    
    story = models.ForeignKey(
        'Story',
        on_delete=models.CASCADE,
        related_name='recommendations_for',
        verbose_name="Рассказ"
    )
    recommended_story = models.ForeignKey(
        'Story',
        on_delete=models.CASCADE,
        related_name='recommended_in',
        verbose_name="Рекомендуемый рассказ"
    )
    recommendation_type = models.CharField(
        max_length=20,
        choices=RECOMMENDATION_TYPES,
        verbose_name="Тип рекомендации"
    )
    score = models.FloatField(
        default=0.0,
        verbose_name="Вес рекомендации"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создана"
    )
    
    class Meta:
        verbose_name = "Рекомендация"
        verbose_name_plural = "Рекомендации"
        unique_together = ['story', 'recommended_story']
        ordering = ['-score', '-created_at']
        indexes = [
            models.Index(fields=['story', '-score']),
            models.Index(fields=['recommendation_type']),
        ]
    
    def __str__(self):
        return f'{self.story.title} -> {self.recommended_story.title}'
