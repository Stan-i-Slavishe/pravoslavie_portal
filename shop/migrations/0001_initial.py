# Generated manually for shop app

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
from decimal import Decimal
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Цена')),
                ('product_type', models.CharField(choices=[('book', 'Книга'), ('audio', 'Аудио'), ('subscription', 'Подписка')], max_length=20, verbose_name='Тип товара')),
                ('book_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='ID книги')),
                ('audio_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='ID аудио')),
                ('subscription_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='ID подписки')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('is_digital', models.BooleanField(default=True, verbose_name='Цифровой товар')),
                ('image', models.ImageField(blank=True, null=True, upload_to='shop/products/', verbose_name='Изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='ID заказа')),
                ('status', models.CharField(choices=[('pending', 'Ожидает оплаты'), ('processing', 'Обрабатывается'), ('paid', 'Оплачен'), ('completed', 'Завершен'), ('cancelled', 'Отменен'), ('refunded', 'Возврат')], default='pending', max_length=20, verbose_name='Статус')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Общая сумма')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Телефон')),
                ('payment_method', models.CharField(blank=True, max_length=50, verbose_name='Способ оплаты')),
                ('payment_id', models.CharField(blank=True, max_length=100, verbose_name='ID платежа')),
                ('payment_data', models.JSONField(blank=True, default=dict, verbose_name='Данные платежа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('paid_at', models.DateTimeField(blank=True, null=True, verbose_name='Оплачено')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='Завершено')),
                ('notes', models.TextField(blank=True, verbose_name='Заметки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Промокод')),
                ('description', models.CharField(max_length=200, verbose_name='Описание')),
                ('discount_type', models.CharField(choices=[('percentage', 'Процент'), ('fixed', 'Фиксированная сумма')], max_length=20, verbose_name='Тип скидки')),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Размер скидки')),
                ('min_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Минимальная сумма заказа')),
                ('max_uses', models.PositiveIntegerField(blank=True, null=True, verbose_name='Максимальное количество использований')),
                ('uses_count', models.PositiveIntegerField(default=0, verbose_name='Количество использований')),
                ('valid_from', models.DateTimeField(verbose_name='Действует с')),
                ('valid_until', models.DateTimeField(verbose_name='Действует до')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
            ],
            options={
                'verbose_name': 'Скидка',
                'verbose_name_plural': 'Скидки',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchased_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='auth.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
                'ordering': ['-purchased_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(max_length=200, verbose_name='Название товара')),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена товара')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('is_downloaded', models.BooleanField(default=False, verbose_name='Скачано')),
                ('download_count', models.PositiveIntegerField(default=0, verbose_name='Количество скачиваний')),
                ('first_download_at', models.DateTimeField(blank=True, null=True, verbose_name='Первое скачивание')),
                ('last_download_at', models.DateTimeField(blank=True, null=True, verbose_name='Последнее скачивание')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Элемент заказа',
                'verbose_name_plural': 'Элементы заказа',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Количество')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.cart', verbose_name='Корзина')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Элемент корзины',
                'verbose_name_plural': 'Элементы корзины',
            },
        ),
        migrations.AddConstraint(
            model_name='purchase',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='unique_user_product_purchase'),
        ),
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.UniqueConstraint(fields=('order', 'product'), name='unique_order_product'),
        ),
        migrations.AddConstraint(
            model_name='cartitem',
            constraint=models.UniqueConstraint(fields=('cart', 'product'), name='unique_cart_product'),
        ),
    ]
