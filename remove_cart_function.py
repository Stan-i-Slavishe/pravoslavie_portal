@login_required
@require_POST
@csrf_exempt
def remove_from_cart(request):
    """Удалить товар из корзины (AJAX)"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        if not item_id:
            return JsonResponse({'error': 'Не указан ID товара'}, status=400)
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart = cart_item.cart
        cart_item.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Товар удален из корзины',
            'cart_total': float(cart.total_price),
            'cart_total_items': cart.total_items
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        logger.error(f'Ошибка удаления товара из корзины: {e}')
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)
