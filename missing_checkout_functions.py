# === НЕДОСТАЮЩИЕ ФУНКЦИИ ДЛЯ SHOP/VIEWS.PY ===
# Добавьте эти функции перед функцией my_orders_view

@login_required
def checkout_view(request):
    """Оформление заказа"""
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('shop:cart')
    
    if not cart.items.exists():
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('shop:cart')
    
    if request.method == 'POST':
        # Получаем данные из формы
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        # Простая валидация
        errors = []
        if not first_name:
            errors.append('Укажите имя')
        if not last_name:
            errors.append('Укажите фамилию')
        if not email:
            errors.append('Укажите email')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'shop/checkout.html', {'cart': cart})
        
        try:
            # Создаем заказ
            order = Order.objects.create(
                user=request.user,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                total_amount=cart.total_price,
                status='pending'
            )
            
            # Переносим товары из корзины в заказ
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
                    special_requests=cart_item.special_requests,
                )
            
            # Очищаем корзину
            cart.clear()
            
            messages.success(request, f'Заказ #{order.short_id} создан! Переходим к оплате.')
            return redirect('shop:payment', order_id=order.order_id)
            
        except Exception as e:
            logger.error(f'Ошибка создания заказа: {e}')
            messages.error(request, 'Ошибка при создании заказа. Попробуйте еще раз.')
            return render(request, 'shop/checkout.html', {'cart': cart})
    
    # GET запрос - показываем форму оформления
    context = {
        'cart': cart,
        'user': request.user,
    }
    
    return render(request, 'shop/checkout.html', context)

@login_required
def payment_view(request, order_id):
    """Страница оплаты заказа"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    if order.status != 'pending':
        messages.info(request, f'Заказ #{order.short_id} уже имеет статус: {order.get_status_display()}')
        return redirect('shop:order_detail', order_id=order.order_id)
    
    context = {
        'order': order,
        'items': order.items.all(),
    }
    
    return render(request, 'shop/payment.html', context)

@login_required  
def payment_success_view(request, order_id):
    """Страница успешной оплаты"""
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    
    # Если заказ еще не оплачен, помечаем как оплаченный (для тестирования)
    if order.status == 'pending':
        order.status = 'paid'
        order.paid_at = timezone.now()
        order.payment_method = 'test'
        order.payment_id = f'test_{order_id}'
        order.save()
        
        # Создаем покупки
        complete_order(order)
        
        messages.success(request, f'Заказ #{order.short_id} успешно оплачен!')
    
    context = {
        'order': order,
        'items': order.items.all(),
    }
    
    return render(request, 'shop/payment_success.html', context)
