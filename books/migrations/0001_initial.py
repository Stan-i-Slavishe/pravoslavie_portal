# Generated manually for books app

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='URL-имя')),
                ('icon', models.CharField(blank=True, help_text='Bootstrap Icons класс', max_length=50, verbose_name='Иконка')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='URL-имя')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='URL-имя')),
                ('author', models.CharField(blank=True, max_length=200, verbose_name='Автор')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('content', models.TextField(blank=True, verbose_name='Содержание')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='books/covers/', verbose_name='Обложка')),
                ('file', models.FileField(blank=True, null=True, upload_to='books/files/', verbose_name='Файл книги')),
                ('format', models.CharField(choices=[('pdf', 'PDF'), ('epub', 'EPUB'), ('fb2', 'FB2'), ('audio', 'Аудиокнига')], default='pdf', max_length=10, verbose_name='Формат')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена')),
                ('is_free', models.BooleanField(default=True, verbose_name='Бесплатная')),
                ('downloads_count', models.PositiveIntegerField(default=0, verbose_name='Количество скачиваний')),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=3, verbose_name='Рейтинг')),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='Просмотры')),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Рекомендуемая')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')),
                ('isbn', models.CharField(blank=True, max_length=17, verbose_name='ISBN')),
                ('pages', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество страниц')),
                ('language', models.CharField(default='ru', max_length=10, verbose_name='Язык')),
                ('publisher', models.CharField(blank=True, max_length=100, verbose_name='Издательство')),
                ('publication_year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Год издания')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='books.category', verbose_name='Категория')),
                ('tags', models.ManyToManyField(blank=True, to='books.tag', verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserFavoriteBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book', verbose_name='Книга')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранная книга',
                'verbose_name_plural': 'Избранные книги',
                'ordering': ['-added_at'],
            },
        ),
        migrations.CreateModel(
            name='BookReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], verbose_name='Оценка')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='books.book', verbose_name='Книга')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BookDownload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP адрес')),
                ('downloaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Скачано')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book', verbose_name='Книга')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Скачивание',
                'verbose_name_plural': 'Скачивания',
                'ordering': ['-downloaded_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='userfavoritebook',
            constraint=models.UniqueConstraint(fields=('user', 'book'), name='unique_user_favorite_book'),
        ),
        migrations.AddConstraint(
            model_name='bookreview',
            constraint=models.UniqueConstraint(fields=('book', 'user'), name='unique_book_user_review'),
        ),
    ]
