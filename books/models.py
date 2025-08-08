from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from core.models import Tag  # Используем единую модель Tag из core
import re
import json


def create_slug(text):
    """Создает slug из русского текста"""
    # Словарь для транслитерации
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    
    text = text.lower()
    result = ''
    for char in text:
        if char in translit_dict:
            result += translit_dict[char]
        elif char.isalnum() or char in [' ', '-']:
            result += char
        else:
            result += '-'
    
    # Убираем лишние дефисы и создаем slug
    result = re.sub(r'[-\s]+', '-', result)
    result = result.strip('-')
    return result[:50]  # Ограничиваем длину


class Category(models.Model):
    """Категории книг"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL-имя', unique=True, blank=True)
    icon = models.CharField('Иконка', max_length=50, blank=True, help_text='Bootstrap Icons класс')
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = create_slug(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)



class Book(models.Model):
    """Модель книги"""
    
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('epub', 'EPUB'),
        ('fb2', 'FB2'),
        ('audio', 'Аудиокнига'),
    ]
    
    title = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL-имя', unique=True, blank=True)
    author = models.CharField('Автор', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)
    content = models.TextField('Содержание', blank=True)
    
    # Медиа
    cover = models.ImageField('Обложка', upload_to='books/covers/', blank=True, null=True)
    file = models.FileField('Файл книги', upload_to='books/files/', blank=True, null=True)
    
    # Метаданные
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name='Теги', blank=True)
    format = models.CharField('Формат', max_length=10, choices=FORMAT_CHOICES, default='pdf')
    
    # Ценообразование
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=0)
    is_free = models.BooleanField('Бесплатная', default=True)
    
    # Статистика
    downloads_count = models.PositiveIntegerField('Количество скачиваний', default=0)
    rating = models.DecimalField('Рейтинг', max_digits=3, decimal_places=2, default=0)
    views_count = models.PositiveIntegerField('Просмотры', default=0)
    
    # Статус
    is_published = models.BooleanField('Опубликовано', default=True)
    is_featured = models.BooleanField('Рекомендуемая', default=False)
    
    # Временные метки
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    published_at = models.DateTimeField('Дата публикации', blank=True, null=True)
    
    # Дополнительные поля
    isbn = models.CharField('ISBN', max_length=17, blank=True)
    pages = models.PositiveIntegerField('Количество страниц', blank=True, null=True)
    language = models.CharField('Язык', max_length=10, default='ru')
    publisher = models.CharField('Издательство', max_length=100, blank=True)
    publication_year = models.PositiveIntegerField('Год издания', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = create_slug(self.title)
            slug = base_slug
            counter = 1
            while Book.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'slug': self.slug})
    
    @property
    def reviews_count(self):
        """Количество отзывов"""
        return self.reviews.count()
    
    @property
    def is_available_for_download(self):
        """Доступна ли книга для скачивания"""
        return self.is_published and (self.is_free or self.file)


class BookReview(models.Model):
    """Отзывы о книгах"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга', related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.PositiveSmallIntegerField('Оценка', choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField('Отзыв', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ['book', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.book.title} ({self.rating}/5)'


class BookDownload(models.Model):
    """Статистика скачиваний"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    ip_address = models.GenericIPAddressField('IP адрес', null=True, blank=True)
    downloaded_at = models.DateTimeField('Скачано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Скачивание'
        verbose_name_plural = 'Скачивания'
        ordering = ['-downloaded_at']
    
    def __str__(self):
        return f'{self.book.title} - {self.downloaded_at}'


class UserFavoriteBook(models.Model):
    """Избранные книги пользователей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    added_at = models.DateTimeField('Добавлено', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Избранная книга'
        verbose_name_plural = 'Избранные книги'
        unique_together = ['user', 'book']
        ordering = ['-added_at']
    
    def __str__(self):
        return f'{self.user.username} - {self.book.title}'


class ReadingSession(models.Model):
    """Сессии чтения пользователей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    current_page = models.PositiveIntegerField('Текущая страница', default=1)
    total_pages = models.PositiveIntegerField('Всего страниц', default=1)
    reading_time = models.PositiveIntegerField('Время чтения (минуты)', default=0)
    last_read = models.DateTimeField('Последнее чтение', auto_now=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    # Настройки чтения
    font_size = models.FloatField('Размер шрифта', default=1.1)
    theme = models.CharField('Тема', max_length=20, default='light', choices=[
        ('light', 'Светлая'),
        ('dark', 'Темная'),
        ('sepia', 'Сепия')
    ])
    
    class Meta:
        verbose_name = 'Сессия чтения'
        verbose_name_plural = 'Сессии чтения'
        unique_together = ['user', 'book']
        ordering = ['-last_read']
    
    def __str__(self):
        return f'{self.user.username} - {self.book.title} (стр. {self.current_page})'
    
    @property
    def progress_percentage(self):
        """Процент прочитанного"""
        if self.total_pages == 0:
            return 0
        return min(100, (self.current_page / self.total_pages) * 100)
    
    @property
    def is_completed(self):
        """Книга прочитана полностью"""
        return self.current_page >= self.total_pages


class ReadingBookmark(models.Model):
    """Закладки в книгах"""
    session = models.ForeignKey(ReadingSession, on_delete=models.CASCADE, verbose_name='Сессия чтения', related_name='bookmarks')
    page = models.PositiveIntegerField('Страница')
    note = models.TextField('Заметка', blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'
        ordering = ['page']
    
    def __str__(self):
        return f'{self.session.book.title} - стр. {self.page}'


class BookChapter(models.Model):
    """Главы книг для структурированного чтения"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга', related_name='chapters')
    title = models.CharField('Название главы', max_length=200)
    content = models.TextField('Содержание главы')
    order = models.PositiveIntegerField('Порядок', default=0)
    page_start = models.PositiveIntegerField('Начальная страница', default=1)
    page_end = models.PositiveIntegerField('Конечная страница', default=1)
    
    class Meta:
        verbose_name = 'Глава книги'
        verbose_name_plural = 'Главы книг'
        ordering = ['order']
    
    def __str__(self):
        return f'{self.book.title} - {self.title}'
