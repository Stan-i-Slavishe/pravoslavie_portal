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
from .utils import send_order_email
from fairy_tales.models import PersonalizationOrder  # Импортируем заказы сказок

logger = logging.getLogger(__name__)

def product_list_view(request):
    """Каталог товаров"""
    # Исключаем бесплатные товары из магазина
    products = Product.objects.filter(is_active=True, price__gt=0).order_by('-created_at')
    
    # Отладочная информация
    all_products = Product.objects.filter(is_active=True)
    logger.info(f"\u0412сего активных товаров: {all_products.count()}")
    logger.info(f"Платных товаров: {products.count()}")
    for product in all_products:
        logger.info(f"Товар: {product.title} - {product.price}₽ (ID: {product.id})")
    
    # Фильтрация по типу товара
    product_type = request.GET.get('type')
    if product_type:
        products = products.filter(product_type=product_type)
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Сортировка
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'title':
        products = products.order_by('title')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Статистика для фильтров (только платные товары)
    product_types_stats = Product.objects.filter(is_active=True, price__gt=0).values('product_type').annotate(
        count=Count('id')
    ).order_by('product_type')
    
    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'product_types_stats': product_types_stats,
        'current_type': product_type,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    
    return render(request, 'shop/product_list.html', context)


def product_detail_view(request, product_id):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Получаем связанный объект контента
    content_object = product.content_object
    
    # Проверяем, приобрел ли пользователь этот товар
    is_purchased = False
    if request.user.is_authenticated:
        is_purchased = Purchase.objects.filter(
            user=request.user,
            product=product
        ).exists()
    
    context = {
        'product': product,
        'content_object': content_object,
        'is_purchased': is_purchased,
    }
    
    return render(request, 'shop/product_detail.html', context)


def cart_view(request):
    """Просмотр корзины"""
    if not request.user.is_authenticated:
        messages.warning(request, "Войдите в систему для просмотра корзины")
        return redirect('account_login')
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()  # Добавляем элементы корзины
    return render(request, 'shop/cart.html', {'cart': cart, 'items': items})

@login_required
@require_POST
@csrf_exempt
def add_to_cart(request):
    """Добавить товар в корзину"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1 or quantity > 99:
            return JsonResponse({'error': 'Некорректное количество'}, status=400)
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        # Проверяем, что товар можно добавить в корзину
        if product.requires_personalization:
            return JsonResponse({
                'error': 'Этот товар требует персонализации и не может быть добавлен в корзину',
                'redirect_url': f'/fairy-tales/{product.content_object.slug}/order/' if product.content_object else '/'
            }, status=400)
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
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
            'message': f'{product.title} добавлен в корзину',
            'cart_total_items': cart.total_items,
            'cart_total_price': float(cart.total_price)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Некорректное количество'}, status=400)
    except Exception as e:
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

@login_required
def apply_discount_form(request):
    """Применить промокод через обычную форму (не AJAX)"""
    if request.method == 'POST':
        discount_code = request.POST.get('code', '').strip()
        
        if not discount_code:
            messages.error(request, 'Введите промокод')
            return redirect('shop:checkout')
        
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            messages.error(request, 'Корзина пуста')
            return redirect('shop:cart')
        
        try:
            discount = Discount.objects.get(code=discount_code)
            is_valid, error_message = discount.is_valid()
            
            if not is_valid:
                messages.error(request, error_message)
                return redirect('shop:checkout')
            
            # Проверяем минимальную сумму
            if cart.total_price < discount.min_amount:
                messages.error(request, f'Минимальная сумма для применения промокода: {discount.min_amount}₽')
                return redirect('shop:checkout')
            
            discount_amount = discount.calculate_discount(cart.total_price)
            
            # Сохраняем скидку в корзине
            cart.apply_discount(discount_code, discount_amount)
            
            messages.success(request, f'Промокод "{discount_code}" применен! Скидка: {discount_amount}₽')
            
        except Discount.DoesNotExist:
            messages.error(request, 'Промокод не найден')
        except Exception as e:
            logger.error(f'Ошибка применения промокода: {e}')
            messages.error(request, 'Произошла ошибка при применении промокода')
    
    return redirect('shop:checkout')

def get_cart_count(request):
    """Получить количество товаров в корзине (для AJAX) - поддерживает GET запросы"""
    if not request.user.is_authenticated:
        return JsonResponse({'count': 0})
    
    try:
        cart = Cart.objects.get(user=request.user)
        return JsonResponse({
            'count': cart.total_items,
            'total_price': float(cart.total_price)
        })
    except Cart.DoesNotExist:
        return JsonResponse({'count': 0, 'total_price': 0})
    except Exception as e:
        # Логируем ошибку, но возвращаем корректный JSON
        logger.warning(f'Ошибка получения корзины для пользователя {request.user}: {e}')
        return JsonResponse({'count': 0, 'total_price': 0})

@login_required
@require_POST
@csrf_exempt
def update_cart_item(request):
    """Обновить количество товара в корзине"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1 or quantity > 99:
            return JsonResponse({'error': 'Некорректное количество'}, status=400)
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'status': 'success',
            'item_total': float(cart_item.total_price),
            'unit_price': float(cart_item.product.price),
            'cart_total': float(cart_item.cart.total_price),
            'cart_total_items': cart_item.cart.total_items
        })
        
    except ValueError:
        return JsonResponse({'error': 'Некорректное количество'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)

@login_required
@require_POST
@csrf_exempt
def remove_from_cart(request):
    """Удалить товар из корзины"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart = cart_item.cart
        cart_item.delete()
        
        return JsonResponse({
            'status': 'success',
            'cart_total': float(cart.total_price),
            'cart_total_items': cart.total_items
        })
        
    except Exception as e:
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)

@login_required
@require_POST
@csrf_exempt
def apply_discount(request):
    """Применить промокод к корзине"""
    try:
        data = json.loads(request.body)
        discount_code = data.get('code', '').strip()
        
        if not discount_code:
            return JsonResponse({'status': 'error', 'error': 'Введите промокод'}, status=400)
        
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            return JsonResponse({'status': 'error', 'error': 'Корзина пуста'}, status=400)
        
        try:
            discount = Discount.objects.get(code=discount_code)
            is_valid, error_message = discount.is_valid()
            
            if not is_valid:
                return JsonResponse({'status': 'error', 'error': error_message}, status=400)
            
            # Проверяем минимальную сумму
            if cart.total_price < discount.min_amount:
                return JsonResponse({
                    'status': 'error', 
                    'error': f'Минимальная сумма для применения промокода: {discount.min_amount}₽'
                }, status=400)
            
            discount_amount = discount.calculate_discount(cart.total_price)
            final_price = cart.total_price - discount_amount
            
            # Сохраняем скидку в корзине
            cart.apply_discount(discount_code, discount_amount)
            
            return JsonResponse({
                'status': 'success',
                'discount_amount': float(discount_amount),
                'final_price': float(final_price),
                'discount_code': discount_code
            })
            
        except Discount.DoesNotExist:
            return JsonResponse({'status': 'error', 'error': 'Промокод не найден'}, status=400)
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        logger.error(f'Ошибка применения промокода: {e}')
        return JsonResponse({'status': 'error', 'error': 'Ошибка сервера'}, status=500)

@login_required
def apply_discount_form(request):
    """Применить промокод через обычную форму (не AJAX)"""
    if request.method == 'POST':
        discount_code = request.POST.get('code', '').strip()
        
        if not discount_code:
            messages.error(request, 'Введите промокод')
            return redirect('shop:checkout')
        
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            messages.error(request, 'Корзина пуста')
            return redirect('shop:cart')
        
        try:
            discount = Discount.objects.get(code=discount_code)
            is_valid, error_message = discount.is_valid()
            
            if not is_valid:
                messages.error(request, error_message)
                return redirect('shop:checkout')
            
            # Проверяем минимальную сумму
            if cart.total_price < discount.min_amount:
                messages.error(request, f'Минимальная сумма для применения промокода: {discount.min_amount}₽')
                return redirect('shop:checkout')
            
            discount_amount = discount.calculate_discount(cart.total_price)
            
            # Сохраняем скидку в корзине
            cart.apply_discount(discount_code, discount_amount)
            
            messages.success(request, f'Промокод "{discount_code}" применен! Скидка: {discount_amount}₽')
            
        except Discount.DoesNotExist:
            messages.error(request, 'Промокод не найден')
    
    return redirect('shop:checkout')

@login_required
def apply_discount_form(request):
    """Применить промокод через обычную форму"""
    if request.method == 'POST':
        discount_code = request.POST.get('code', '').strip()
        
        if not discount_code:
            messages.error(request, 'Введите промокод')
            return redirect('shop:checkout')
        
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            messages.error(request, 'Корзина пуста')
            return redirect('shop:cart')
        
        try:
            discount = Discount.objects.get(code=discount_code)
            is_valid, error_message = discount.is_valid()
            
            if not is_valid:
                messages.error(request, error_message)
                return redirect('shop:checkout')
            
            # Проверяем минимальную сумму
            if cart.total_price < discount.min_amount:
                messages.error(request, f'Минимальная сумма для применения промокода: {discount.min_amount}₽')
                return redirect('shop:checkout')
            
            discount_amount = discount.calculate_discount(cart.total_price)
            
            # Сохраняем скидку в корзине
            cart.apply_discount(discount_code, discount_amount)
            
            messages.success(request, f'Промокод "{discount_code}" применен! Скидка: {discount_amount}₽')
            
        except Discount.DoesNotExist:
            messages.error(request, 'Промокод не найден')
    
    return redirect('shop:checkout')

@login_required
def checkout_view(request):
    """Оформление заказа"""
    cart = get_object_or_404(Cart, user=request.user)
    
    if not cart.items.exists():
        messages.warning(request, "Ваша корзина пуста")
        return redirect('shop:cart')
    
    if request.method == 'POST':
        # Данные покупателя
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        # Валидация
        if not all([first_name, last_name, email]):
            messages.error(request, "Пожалуйста, заполните все обязательные поля")
            return render(request, 'shop/checkout.html', {'cart': cart})
        
        # Используем скидку из корзины
        discount_code = cart.applied_discount_code
        discount_amount = cart.discount_amount
        total_amount = cart.total_price_with_discount
        
        # Создаем заказ
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            total_amount=total_amount,
            discount_amount=discount_amount,
            discount_code=discount_code,
            status='pending'
        )
        
        # Создаем элементы заказа
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_title=cart_item.product.title,
                product_price=cart_item.product.price,
                quantity=cart_item.quantity,
                personalization_data=cart_item.personalization_data,
                include_audio=cart_item.include_audio,
                include_illustrations=cart_item.include_illustrations,
                special_requests=cart_item.special_requests
            )
        
        # Очищаем корзину
        cart.clear()
        
        # Логируем создание заказа
        logger.info(f"Order created: {order.short_id} for user {request.user.email if request.user.is_authenticated else 'anonymous'}")
        
        # Email уведомления отправляются автоматически через сигналы
        # (см. shop/signals.py)
        
        # Перенаправляем на страницу оплаты
        return redirect('shop:payment', order_id=order.order_id)
    
    return render(request, 'shop/checkout.html', {'cart': cart})

@login_required
def payment_view(request, order_id):
    """Страница оплаты"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.info(request, "Этот заказ уже обработан")
        return redirect('shop:order_detail', order_id=order.order_id)
    
    if request.method == 'POST':
        # Эмуляция успешной оплаты
        order.status = 'paid'
        order.payment_method = 'test'
        
        # Логируем оплату
        logger.info(f"Order paid: {order.short_id} with test payment")
        
        order.save()  # Сигналы автоматически отправят email уведомления
        
        # Создаем записи о покупках для быстрого доступа
        for item in order.items.all():
            purchase, created = Purchase.objects.get_or_create(
                user=request.user,
                product=item.product,
                defaults={'order': order}
            )
            if not created:
                # Если покупка уже существует, обновляем заказ
                purchase.order = order
                purchase.save()
        
        messages.success(request, f"Заказ #{order.short_id} успешно оплачен!")
        return redirect('shop:payment_success', order_id=order.order_id)
    
    return render(request, 'shop/payment.html', {'order': order})

@login_required
def payment_success_view(request, order_id):
    """Страница успешной оплаты"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'shop/payment_success.html', {'order': order})

@login_required
def my_orders_view(request):
    """Объединенная страница всех заказов пользователя"""
    # Получаем обычные заказы из магазина
    shop_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Получаем заказы терапевтических сказок
    fairy_tale_orders = PersonalizationOrder.objects.filter(user=request.user).order_by('-created_at')
    
    # Объединяем для отображения (создаем общий список)
    all_orders = []
    
    # Добавляем заказы из магазина
    for order in shop_orders:
        all_orders.append({
            'type': 'shop',
            'order': order,
            'id': order.short_id,
            'date': order.created_at,
            'total': order.total_amount,
            'status': order.get_status_display(),
            'status_class': order.status,
            'items_count': order.items.count(),
        })
    
    # Добавляем заказы сказок
    for order in fairy_tale_orders:
        all_orders.append({
            'type': 'fairy_tale',
            'order': order,
            'id': order.short_order_id,
            'date': order.created_at,
            'total': order.total_price,
            'status': order.get_status_display(),
            'status_class': order.status,
            'items_count': 1,  # Сказка всегда одна
        })
    
    # Сортируем по дате (новые сначала)
    all_orders.sort(key=lambda x: x['date'], reverse=True)
    
    # Пагинация
    paginator = Paginator(all_orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'shop_orders_count': shop_orders.count(),
        'fairy_tale_orders_count': fairy_tale_orders.count(),
        'total_orders_count': len(all_orders),
    }
    
    return render(request, 'shop/my_orders.html', context)

@login_required
def my_purchases_view(request):
    """Мои покупки (только оплаченные товары)"""
    purchases = Purchase.objects.filter(
        user=request.user,
        order__status__in=['paid', 'completed']
    ).select_related('product', 'order').order_by('-purchased_at')
    
    # Добавляем заказы сказок (которые оплачены)
    fairy_tale_orders = PersonalizationOrder.objects.filter(
        user=request.user,
        status__in=['paid', 'in_progress', 'completed']
    ).order_by('-created_at')
    
    paginator = Paginator(purchases, 12)
    page_number = request.GET.get('page')
    purchases_page = paginator.get_page(page_number)
    
    return render(request, 'shop/my_purchases.html', {
        'purchases': purchases_page,
        'fairy_tale_orders': fairy_tale_orders[:5],  # Показываем последние 5 сказок
    })

@login_required
def order_detail_view(request, order_id):
    """Детали заказа"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})

@login_required
def download_product(request, order_item_id):
    """Скачать цифровой товар"""
    order_item = get_object_or_404(
        OrderItem, 
        id=order_item_id, 
        order__user=request.user,
        order__status__in=['paid', 'completed']
    )
    
    # Проверяем, что товар цифровой
    if not order_item.product.is_digital:
        messages.error(request, "Этот товар не является цифровым")
        return redirect('shop:my_purchases')
    
    # Получаем связанный контент
    content_object = order_item.product.content_object
    if not content_object:
        messages.error(request, "Файл не найден")
        return redirect('shop:my_purchases')
    
    # Отмечаем скачивание
    order_item.mark_downloaded()
    
    # Перенаправляем на скачивание (зависит от типа контента)
    if order_item.product.product_type == 'book' and hasattr(content_object, 'file') and content_object.file:
        response = HttpResponse(content_object.file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{content_object.title}.pdf"'
        return response
    elif order_item.product.product_type == 'audio' and hasattr(content_object, 'audio_file') and content_object.audio_file:
        response = HttpResponse(content_object.audio_file, content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename="{content_object.title}.mp3"'
        return response
    
    messages.error(request, "Файл недоступен для скачивания")
    return redirect('shop:my_purchases')

@login_required
def download_purchase(request, purchase_id):
    """Скачать товар из покупки (принудительное скачивание)"""
    purchase = get_object_or_404(
        Purchase,
        id=purchase_id,
        user=request.user,
        order__status__in=['paid', 'completed']
    )
    
    # Проверяем, что товар цифровой
    if not purchase.product.is_digital:
        messages.error(request, "Этот товар не является цифровым")
        return redirect('shop:my_purchases')
    
    # Получаем связанный контент
    content_object = purchase.product.content_object
    if not content_object:
        messages.error(request, "Файл не найден")
        return redirect('shop:my_purchases')
    
    # Увеличиваем счетчик скачиваний
    purchase.download_count += 1
    purchase.last_downloaded = timezone.now()
    purchase.save()
    
    # Принудительное скачивание файла
    if purchase.product.product_type == 'book' and hasattr(content_object, 'file') and content_object.file:
        try:
            # Читаем файл
            file_content = content_object.file.read()
            
            # Создаем response для скачивания с усиленными заголовками
            response = HttpResponse(file_content, content_type='application/octet-stream')  # Изменил тип
            
            # Ключевые заголовки для принудительного скачивания
            filename = f"{content_object.title}.pdf".replace('"', '').replace("'", "")
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = len(file_content)
            response['Content-Type'] = 'application/force-download'  # Принудительный тип
            
            # Дополнительные заголовки для скачивания
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            response['Content-Transfer-Encoding'] = 'binary'
            
            return response
            
        except Exception as e:
            logger.error(f"Error downloading file for purchase {purchase.id}: {e}")
            messages.error(request, "Ошибка при скачивании файла")
            return redirect('shop:my_purchases')
            
    elif purchase.product.product_type == 'audio' and hasattr(content_object, 'audio_file') and content_object.audio_file:
        try:
            file_content = content_object.audio_file.read()
            response = HttpResponse(file_content, content_type='audio/mpeg')
            filename = f"{content_object.title}.mp3".replace('"', '').replace("'", "")
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Length'] = len(file_content)
            return response
        except Exception as e:
            logger.error(f"Error downloading audio file for purchase {purchase.id}: {e}")
            messages.error(request, "Ошибка при скачивании файла")
            return redirect('shop:my_purchases')
    
    messages.error(request, "Файл недоступен для скачивания")
    return redirect('shop:my_purchases')

def product_list_view(request):
    """Каталог товаров"""
    products = Product.objects.filter(is_active=True)
    
    # Фильтры
    product_type = request.GET.get('type')
    if product_type:
        products = products.filter(product_type=product_type)
    
    min_price = request.GET.get('min_price')
    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except:
            pass
    
    max_price = request.GET.get('max_price')
    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except:
            pass
    
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Сортировка
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('title')
    else:  # newest
        products = products.order_by('-created_at')
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'selected_type': request.GET.get('type', ''),
        'current_filters': {
            'type': request.GET.get('type', ''),
            'min_price': request.GET.get('min_price', ''),
            'max_price': request.GET.get('max_price', ''),
            'search': request.GET.get('search', ''),
            'sort': request.GET.get('sort', 'newest'),
        },
        'product_types': Product.PRODUCT_TYPES,
    }
    
    return render(request, 'shop/catalog.html', context)

def product_detail_view(request, product_id):
    """Страница товара"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Похожие товары
    related_products = Product.objects.filter(
        product_type=product.product_type,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Проверяем, куплен ли товар
    is_purchased = False
    if request.user.is_authenticated:
        is_purchased = Purchase.objects.filter(
            user=request.user,
            product=product
        ).exists()
    
    # Создаем форму персонализации для сказок
    fairy_tale_form = None
    if product.product_type == 'fairy_tale':
        fairy_tale_form = PersonalizationForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'content_object': product.content_object,
        'is_purchased': is_purchased,
        'fairy_tale_form': fairy_tale_form,
    }
    
    return render(request, 'shop/product_detail.html', context)

@require_POST
@csrf_exempt
def apply_discount(request):
    """Применить промокод"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Требуется авторизация'}, status=401)
    
    try:
        data = json.loads(request.body)
        discount_code = data.get('code', '').strip()
        
        if not discount_code:
            return JsonResponse({'error': 'Введите промокод'}, status=400)
        
        cart = get_object_or_404(Cart, user=request.user)
        
        if not cart.items.exists():
            return JsonResponse({'error': 'Корзина пуста'}, status=400)
        
        try:
            discount = Discount.objects.get(code=discount_code)
            is_valid, error_message = discount.is_valid()
            
            if not is_valid:
                return JsonResponse({'error': error_message}, status=400)
            
            if cart.total_price < discount.min_amount:
                return JsonResponse({
                    'error': f'Минимальная сумма для применения промокода: {discount.min_amount}₽'
                }, status=400)
            
            discount_amount = discount.calculate_discount(cart.total_price)
            final_price = cart.total_price - discount_amount
            
            return JsonResponse({
                'status': 'success',
                'discount_amount': float(discount_amount),
                'final_price': float(final_price),
                'discount_description': discount.description
            })
            
        except Discount.DoesNotExist:
            return JsonResponse({'error': 'Промокод не найден'}, status=400)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)

@login_required
def order_fairy_tale(request, product_id):
    """Добавление персонализированной сказки в корзину"""
    product = get_object_or_404(Product, id=product_id, is_active=True, product_type='fairy_tale')
    
    if request.method == 'POST':
        form = PersonalizationForm(request.POST)
        
        if form.is_valid():
            # Получаем данные из формы
            personalization_data = {
                'child_name': form.cleaned_data['child_name'],
                'child_age': form.cleaned_data['child_age'],
                'main_problem': form.cleaned_data['main_problem'],
                'child_interests': form.cleaned_data['child_interests'],
                'parent_goals': form.cleaned_data['parent_goals'],
            }
            
            include_audio = form.cleaned_data['include_audio']
            include_illustrations = form.cleaned_data['include_illustrations']
            special_requests = form.cleaned_data['special_requests']
            
            # Получаем или создаем корзину
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Добавляем сказку в корзину с персонализацией
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    'quantity': 1,
                    'personalization_data': personalization_data,
                    'include_audio': include_audio,
                    'include_illustrations': include_illustrations,
                    'special_requests': special_requests,
                }
            )
            
            if not item_created:
                # Если товар уже в корзине, обновляем данные
                cart_item.personalization_data = personalization_data
                cart_item.include_audio = include_audio
                cart_item.include_illustrations = include_illustrations
                cart_item.special_requests = special_requests
                cart_item.save()
            
            child_name = personalization_data.get('child_name', 'Ребенок')
            messages.success(
                request, 
                f'Персонализированная сказка для {child_name} добавлена в корзину!'
            )
            return redirect('shop:cart')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    
    # Если возникли ошибки, возвращаем на страницу товара
    return redirect('shop:product_detail', product_id=product.id)

# ===== НЕДОСТАЮЩИЕ ПРЕДСТАВЛЕНИЯ ДЛЯ ЗАКАЗОВ И ПОКУПОК =====

@login_required
def my_orders_view(request):
    """Мои заказы"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'orders': page_obj,
        'page_obj': page_obj,
    }
    
    return render(request, 'shop/my_orders.html', context)

@login_required
def my_purchases_view(request):
    """Мои покупки"""
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_at')
    
    # Группируем покупки по заказам для лучшего отображения
    orders_with_purchases = Order.objects.filter(
        user=request.user,
        status__in=['paid', 'completed']
    ).prefetch_related('items__product').order_by('-created_at')
    
    context = {
        'purchases': purchases,
        'orders_with_purchases': orders_with_purchases,
    }
    
    return render(request, 'shop/my_purchases.html', context)

@login_required
def order_detail_view(request, order_id):
    """Детальная страница заказа"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    context = {
        'order': order,
        'items': order.items.all(),
    }
    
    return render(request, 'shop/order_detail.html', context)

@login_required
def download_product(request, order_item_id):
    """Скачать товар из заказа"""
    order_item = get_object_or_404(
        OrderItem, 
        id=order_item_id, 
        order__user=request.user,
        order__status__in=['paid', 'completed']
    )
    
    # Проверяем тип товара и возвращаем соответствующий файл
    product = order_item.product
    content_object = product.content_object
    
    if not content_object:
        messages.error(request, 'Файл не найден')
        return redirect('shop:my_purchases')
    
    try:
        if product.product_type == 'book':
            # Скачивание книги
            from books.models import Book
            book = content_object
            if book.pdf_file:
                # Увеличиваем счетчик скачиваний
                order_item.mark_downloaded()
                
                # Возвращаем файл
                response = HttpResponse(book.pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{book.title}.pdf"'
                return response
        
        elif product.product_type == 'audio':
            # Скачивание аудио
            from audio.models import AudioTrack
            audio = content_object
            if audio.audio_file:
                order_item.mark_downloaded()
                
                response = HttpResponse(audio.audio_file.read(), content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="{audio.title}.mp3"'
                return response
                
        elif product.product_type == 'fairy_tale':
            # Для персонализированных сказок
            if order_item.generated_content:
                order_item.mark_downloaded()
                
                # Создаем текстовый файл со сказкой
                response = HttpResponse(order_item.generated_content, content_type='text/plain; charset=utf-8')
                response['Content-Disposition'] = f'attachment; filename="Сказка_{order_item.personalization_data.get("child_name", "ребенка")}.txt"'
                return response
        
        messages.error(request, 'Файл недоступен для скачивания')
        return redirect('shop:my_purchases')
        
    except Exception as e:
        logger.error(f'Ошибка скачивания товара {order_item_id}: {e}')
        messages.error(request, 'Ошибка при скачивании файла')
        return redirect('shop:my_purchases')

@login_required
def download_purchase(request, purchase_id):
    """Скачать товар из покупки (альтернативная ссылка)"""
    purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user)
    
    # Находим соответствующий OrderItem
    try:
        order_item = OrderItem.objects.get(
            order=purchase.order,
            product=purchase.product
        )
        return download_product(request, order_item.id)
    except OrderItem.DoesNotExist:
        messages.error(request, 'Элемент заказа не найден')
        return redirect('shop:my_purchases')

def complete_order(order):
    """
    Завершить заказ и создать записи покупок
    Вызывается после успешной оплаты
    """
    if order.status == 'paid' and not Purchase.objects.filter(order=order).exists():
        # Создаем записи покупок для всех товаров в заказе
        for order_item in order.items.all():
            Purchase.objects.get_or_create(
                user=order.user,
                product=order_item.product,
                order=order,
                defaults={
                    'purchased_at': timezone.now()
                }
            )
        
        # Обновляем статус заказа
        order.status = 'completed'
        order.completed_at = timezone.now()
        order.save()
        
        logger.info(f'Заказ {order.order_id} завершен, создано {order.items.count()} покупок')

@login_required
def test_payment_success(request, order_id):
    """
    ТЕСТОВАЯ функция для имитации успешной оплаты
    Удалить в продакшене!
    """
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if order.status == 'pending':
        # Имитируем успешную оплату
        order.status = 'paid'
        order.paid_at = timezone.now()
        order.payment_method = 'test'
        order.payment_id = f'test_{order_id}'
        order.save()
        
        # Создаем покупки
        complete_order(order)
        
        messages.success(request, f'Тестовая оплата заказа #{order.short_id} прошла успешно!')
        return redirect('shop:my_purchases')
    
    messages.warning(request, 'Заказ уже был оплачен или имеет неподходящий статус')
    return redirect('shop:my_orders')

def debug_cart_view(request):
    """Отладочная страница для счетчика количества"""
    return render(request, 'shop/debug_cart.html')

@login_required
@require_POST
@csrf_exempt
def add_book_to_cart(request):
    """Добавить книгу в корзину (создает товар если нужно)"""
    try:
        data = json.loads(request.body)
        book_id = data.get('book_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1 or quantity > 99:
            return JsonResponse({'error': 'Некорректное количество'}, status=400)
        
        # Получаем книгу
        from books.models import Book
        book = get_object_or_404(Book, id=book_id, is_published=True)
        
        # Проверяем, что книга платная
        if book.is_free or not book.price or book.price <= 0:
            return JsonResponse({
                'status': 'error',
                'message': 'Эта книга бесплатная и не может быть добавлена в корзину'
            }, status=400)
        
        # Находим или создаем товар в магазине
        product, created = Product.objects.get_or_create(
            product_type='book',
            book_id=book.id,
            defaults={
                'title': book.title,
                'description': book.description or f"Духовная книга '{book.title}' - погрузитесь в мир веры и мудрости.",
                'price': book.price,
                'is_active': True,
                'is_digital': True,
            }
        )
        
        # Обновляем товар, если он уже существовал
        if not created:
            product.title = book.title
            product.description = book.description or f"Духовная книга '{book.title}'"
            product.price = book.price
            product.is_active = True
            product.save()
        
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