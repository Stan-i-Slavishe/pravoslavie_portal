from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from decimal import Decimal
import json
import logging
from django.utils import timezone

from .models import Product, Cart, CartItem, Order, OrderItem, Purchase, Discount
from .forms import PersonalizationForm, CartForm
from .utils import send_order_email, send_order_confirmation_email
from fairy_tales.models import PersonalizationOrder  # Импортируем заказы сказок

logger = logging.getLogger(__name__)

def product_list_view(request):
    """Каталог товаров"""
    # Исключаем бесплатные товары из магазина
    products = Product.objects.filter(is_active=True, price__gt=0).order_by('-created_at')
    
    # Отладочная информация
    all_products = Product.objects.filter(is_active=True)
    logger.info(f"Всего активных товаров: {all_products.count()}")
    logger.info(f"Платных товаров: {products.count()}")
    for product in all_products:
        logger.info(f"Товар: {product.name}, Цена: {product.price}, В магазине: {product.price > 0}")
    
    # Фильтрация по категориям
    category = request.GET.get('category')
    if category:
        products = products.filter(category__slug=category)
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Пагинация
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Категории для фильтра
    categories = Product.objects.values('category__name', 'category__slug').distinct()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category,
        'search_query': search_query,
    }
    
    return render(request, 'shop/product_list.html', context)


def product_detail_view(request, product_id):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Похожие товары
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True,
        price__gt=0
    ).exclude(id=product.id)[:4]
    
    # Проверяем, купил ли пользователь этот товар
    is_purchased = False
    if request.user.is_authenticated:
        is_purchased = Purchase.objects.filter(
            user=request.user,
            product=product
        ).exists()
    
    context = {
        'product': product,
        'related_products': related_products,
        'is_purchased': is_purchased,
    }
    
    return render(request, 'shop/product_detail.html', context)


@login_required
def cart_view(request):
    """Корзина покупок"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Обновляем итоги корзины (на случай если цены изменились)
    cart.update_totals()
    
    # Проверим доступность товаров
    unavailable_items = []
    for item in cart.items.all():
        if not item.product.is_active:
            unavailable_items.append(item)
    
    # Удаляем недоступные товары
    for item in unavailable_items:
        item.delete()
    
    if unavailable_items:
        messages.warning(request, f'Удалено {len(unavailable_items)} недоступных товаров из корзины')
        cart.update_totals()
    
    context = {
        'cart': cart,
    }
    
    return render(request, 'shop/cart.html', context)


@login_required
@require_POST
def add_to_cart(request):
    """Добавление товара в корзину (AJAX)"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({'error': 'Некорректное количество'}, status=400)
        
        if quantity > 99:
            quantity = 99
            
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Проверяем, не купил ли уже пользователь этот товар
        if Purchase.objects.filter(user=request.user, product=product).exists():
            return JsonResponse({
                'error': f'Вы уже приобрели "{product.name}"'
            }, status=400)
        
        cart, cart_created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            cart_item.quantity += quantity
            if cart_item.quantity > 99:
                cart_item.quantity = 99
            cart_item.save()
        
        # Обновляем итоги корзины
        cart.update_totals()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Товар "{product.name}" добавлен в корзину',
            'cart_total_items': cart.total_items,
            'cart_total_price': float(cart.total_price)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Некорректное количество'}, status=400)
    except Exception as e:
        logger.error(f'Ошибка добавления товара в корзину: {e}')
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)


@login_required
@require_POST  
def update_cart_item(request):
    """Обновление количества товара в корзине (AJAX)"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({'error': 'Количество должно быть больше 0'}, status=400)
        
        if quantity > 99:
            quantity = 99
            
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        
        # Обновляем итоги корзины
        cart_item.cart.update_totals()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Количество обновлено',
            'item_total': float(cart_item.total_price),
            'cart_total_items': cart_item.cart.total_items,
            'cart_total_price': float(cart_item.cart.total_price)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Некорректное количество'}, status=400)
    except Exception as e:
        logger.error(f'Ошибка обновления товара в корзине: {e}')
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)


@login_required
@require_POST
def remove_from_cart(request):
    """Удаление товара из корзины (AJAX)"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        product_name = cart_item.product.name
        cart_item.delete()
        
        # Обновляем итоги корзины
        cart = Cart.objects.get(user=request.user)
        cart.update_totals()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Товар "{product_name}" удален из корзины',
            'cart_total_items': cart.total_items,
            'cart_total_price': float(cart.total_price)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        logger.error(f'Ошибка удаления товара из корзины: {e}')
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)


@login_required
def checkout_view(request):
    """Оформление заказа"""
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.error(request, 'Ваша корзина пуста')
        return redirect('shop:cart')
    
    if request.method == 'POST':
        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            discount=cart.discount,
            discount_amount=cart.discount_amount,
            status='pending'
        )
        
        # Создаем позиции заказа
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # Очищаем корзину
        cart.items.all().delete()
        cart.discount = None
        cart.save()
        cart.update_totals()
        
        # Отправляем email уведомление
        try:
            send_order_confirmation_email(order)
        except Exception as e:
            logger.error(f'Ошибка отправки email для заказа {order.id}: {e}')
        
        messages.success(request, f'Заказ №{order.id} создан! Проверьте вашу почту.')
        return redirect('shop:payment', order_id=order.id)
    
    context = {
        'cart': cart,
    }
    
    return render(request, 'shop/checkout.html', context)


@login_required
def payment_view(request, order_id):
    """Страница оплаты"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    
    return render(request, 'shop/payment.html', context)


@login_required
def payment_success_view(request, order_id):
    """Успешная оплата"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Обновляем статус заказа
    order.status = 'paid'
    order.paid_at = timezone.now()
    order.save()
    
    # Создаем записи о покупках
    for order_item in order.items.all():
        Purchase.objects.get_or_create(
            user=request.user,
            product=order_item.product,
            defaults={
                'order': order,
                'download_count': 0,
                'purchased_at': timezone.now()
            }
        )
    
    # Отправляем email уведомление об успешной оплате
    try:
        send_order_confirmation_email(order)
    except Exception as e:
        logger.error(f'Ошибка отправки email об оплате заказа {order.id}: {e}')
    
    context = {
        'order': order,
    }
    
    return render(request, 'shop/payment_success.html', context)


@login_required
@require_POST
def apply_discount(request):
    """Применение промокода (AJAX)"""
    try:
        data = json.loads(request.body)
        discount_code = data.get('code', '').strip().upper()
        
        if not discount_code:
            return JsonResponse({'error': 'Введите промокод'}, status=400)
        
        cart = get_object_or_404(Cart, user=request.user)
        
        # Проверяем промокод
        try:
            discount = Discount.objects.get(
                code=discount_code,
                active=True,
                valid_from__lte=timezone.now(),
                valid_until__gte=timezone.now()
            )
        except Discount.DoesNotExist:
            return JsonResponse({'error': 'Промокод не найден или истек'}, status=400)
        
        # Проверяем минимальную сумму заказа
        if cart.total_price < discount.min_order_amount:
            return JsonResponse({
                'error': f'Минимальная сумма заказа для этого промокода: {discount.min_order_amount}₽'
            }, status=400)
        
        # Применяем скидку
        cart.discount = discount
        cart.save()
        cart.update_totals()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Промокод применен! Скидка: {discount.get_discount_display()}',
            'discount_amount': float(cart.discount_amount),
            'cart_total_price': float(cart.total_price)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        logger.error(f'Ошибка применения промокода: {e}')
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)


@login_required
def apply_discount_form(request):
    """Форма применения промокода"""
    if request.method == 'POST':
        discount_code = request.POST.get('code', '').strip().upper()
        
        if not discount_code:
            messages.error(request, 'Введите промокод')
            return redirect('shop:cart')
        
        cart = get_object_or_404(Cart, user=request.user)
        
        # Проверяем промокод
        try:
            discount = Discount.objects.get(
                code=discount_code,
                active=True,
                valid_from__lte=timezone.now(),
                valid_until__gte=timezone.now()
            )
        except Discount.DoesNotExist:
            messages.error(request, 'Промокод не найден или истек')
            return redirect('shop:cart')
        
        # Проверяем минимальную сумму заказа
        if cart.total_price < discount.min_order_amount:
            messages.error(request, f'Минимальная сумма заказа для этого промокода: {discount.min_order_amount}₽')
            return redirect('shop:cart')
        
        # Применяем скидку
        cart.discount = discount
        cart.save()
        cart.update_totals()
        
        messages.success(request, f'Промокод применен! Скидка: {discount.get_discount_display()}')
        return redirect('shop:cart')
    
    return redirect('shop:cart')


@login_required
def my_orders_view(request):
    """Мои заказы"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'shop/my_orders.html', context)


@login_required
def order_detail_view(request, order_id):
    """Детали заказа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    
    return render(request, 'shop/order_detail.html', context)


@login_required
def my_purchases_view(request):
    """Мои покупки"""
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_at')
    
    # Пагинация
    paginator = Paginator(purchases, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'shop/my_purchases.html', context)


@login_required
def download_product(request, order_item_id):
    """Скачивание товара из заказа"""
    order_item = get_object_or_404(OrderItem, id=order_item_id, order__user=request.user)
    
    # Проверяем что заказ оплачен
    if order_item.order.status != 'paid':
        messages.error(request, 'Заказ еще не оплачен')
        return redirect('shop:order_detail', order_id=order_item.order.id)
    
    # Проверяем что товар цифровой
    if not order_item.product.digital_file:
        messages.error(request, 'У этого товара нет файла для скачивания')
        return redirect('shop:order_detail', order_id=order_item.order.id)
    
    # Увеличиваем счетчик скачиваний
    purchase, created = Purchase.objects.get_or_create(
        user=request.user,
        product=order_item.product,
        defaults={'order': order_item.order, 'download_count': 0}
    )
    purchase.download_count += 1
    purchase.save()
    
    # Возвращаем файл
    try:
        response = HttpResponse(
            order_item.product.digital_file.read(),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{order_item.product.name}.pdf"'
        return response
    except Exception as e:
        logger.error(f'Ошибка скачивания файла: {e}')
        messages.error(request, 'Ошибка при скачивании файла')
        return redirect('shop:order_detail', order_id=order_item.order.id)


@login_required
def download_purchase(request, purchase_id):
    """Скачивание товара из покупок"""
    purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user)
    
    # Проверяем что товар цифровой
    if not purchase.product.digital_file:
        messages.error(request, 'У этого товара нет файла для скачивания')
        return redirect('shop:my_purchases')
    
    # Увеличиваем счетчик скачиваний
    purchase.download_count += 1
    purchase.save()
    
    # Возвращаем файл
    try:
        response = HttpResponse(
            purchase.product.digital_file.read(),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{purchase.product.name}.pdf"'
        return response
    except Exception as e:
        logger.error(f'Ошибка скачивания файла: {e}')
        messages.error(request, 'Ошибка при скачивании файла')
        return redirect('shop:my_purchases')


@login_required
@require_POST
def add_book_to_cart(request):
    """Добавление книги из каталога книг в корзину магазина"""
    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')
        quantity = int(data.get('quantity', 1))
        
        # Импортируем модель Book
        from books.models import Book
        
        book = get_object_or_404(Book, id=book_id)
        
        # Создаем или находим соответствующий товар в магазине
        product, created = Product.objects.get_or_create(
            name=book.title,
            defaults={
                'description': book.description or f'Духовная книга "{book.title}"',
                'price': Decimal('99.00'),  # Стандартная цена для книг
                'is_active': True,
                'product_type': 'book',
                'digital_file': book.pdf_file,
                'category_id': 1,  # Базовая категория
            }
        )
        
        # Проверяем, не купил ли уже пользователь эту книгу
        if Purchase.objects.filter(user=request.user, product=product).exists():
            return JsonResponse({
                'error': f'Вы уже приобрели книгу "{book.title}"'
            }, status=400)
        
        # Добавляем в корзину
        cart, cart_created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            cart_item.quantity += quantity
            if cart_item.quantity > 99:
                cart_item.quantity = 99
            cart_item.save()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Книга "{book.title}" добавлена в корзину',
            'cart_total_items': cart.total_items,
            'cart_total_price': float(cart.total_price),
            'product_created': created
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Некорректное количество'}, status=400)
    except Exception as e:
        logger.error(f'Ошибка добавления книги в корзину: {e}')
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)


@login_required
def get_cart_count(request):
    """
    Получение количества товаров в корзине (AJAX)
    """
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return JsonResponse({
            'status': 'success',
            'count': cart.total_items,
            'total_price': float(cart.total_price)
        })
    except Exception as e:
        logger.error(f'Ошибка получения счетчика корзины: {e}')
        return JsonResponse({
            'status': 'error',
            'message': 'Ошибка получения данных корзины'
        }, status=500)


# Дополнительные функции для интеграции email уведомлений
@login_required  
def order_fairy_tale(request, product_id):
    """Заказ персонализированной сказки"""
    product = get_object_or_404(Product, id=product_id, product_type='fairy_tale')
    
    if request.method == 'POST':
        form = PersonalizationForm(request.POST)
        if form.is_valid():
            # Создаем заказ сказки с персонализацией
            # Логика создания персонализированного заказа
            messages.success(request, 'Заказ на персонализированную сказку принят!')
            return redirect('shop:my_orders')
    else:
        form = PersonalizationForm()
    
    context = {
        'product': product,
        'form': form,
    }
    
    return render(request, 'shop/order_fairy_tale.html', context)


# Тестовые функции (удалить в продакшене)
@login_required
def test_payment_success(request, order_id):
    """Тестовая функция успешной оплаты"""
    return payment_success_view(request, order_id)


@login_required
def debug_cart_view(request):
    """Отладочная информация о корзине"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    context = {
        'cart': cart,
        'debug_info': {
            'total_items': cart.total_items,
            'total_price': cart.total_price,
            'items_count': cart.items.count(),
        }
    }
    
    return render(request, 'shop/debug_cart.html', context)
