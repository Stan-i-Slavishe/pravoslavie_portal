# shop/payments/yookassa_payment.py
"""
Интеграция с платежной системой YooKassa
Документация: https://yookassa.ru/developers/api
"""

import uuid
import logging
from decimal import Decimal
from typing import Dict, Optional, Tuple
from django.conf import settings
from django.urls import reverse
from django.http import HttpRequest

try:
    from yookassa import Configuration, Payment
    YOOKASSA_AVAILABLE = True
except ImportError:
    YOOKASSA_AVAILABLE = False

logger = logging.getLogger(__name__)


class YooKassaPaymentError(Exception):
    """Базовое исключение для ошибок YooKassa"""
    pass


class YooKassaPaymentService:
    """Сервис для работы с платежами YooKassa"""
    
    def __init__(self):
        if not YOOKASSA_AVAILABLE:
            raise YooKassaPaymentError(
                "YooKassa SDK не установлен. Выполните: pip install yookassa"
            )
        
        # Проверяем настройки
        self.shop_id = getattr(settings, 'YOOKASSA_SHOP_ID', None)
        self.secret_key = getattr(settings, 'YOOKASSA_SECRET_KEY', None)
        
        if not self.shop_id or not self.secret_key:
            logger.warning("YooKassa credentials not configured")
            return
        
        # Конфигурируем YooKassa SDK
        Configuration.account_id = self.shop_id
        Configuration.secret_key = self.secret_key
        
        logger.info("YooKassa payment service initialized")
    
    def is_configured(self) -> bool:
        """Проверяет, настроена ли интеграция"""
        return bool(self.shop_id and self.secret_key)
    
    def create_payment(self, order, request: HttpRequest) -> Tuple[bool, Dict]:
        """
        Создает платеж в YooKassa
        
        Args:
            order: Объект заказа
            request: HTTP запрос для построения URLs
            
        Returns:
            Tuple[bool, Dict]: (успех, данные платежа или ошибка)
        """
        if not self.is_configured():
            return False, {
                'error': 'Платежная система не настроена',
                'use_test_payment': True
            }
        
        try:
            # Генерируем уникальный ключ идемпотентности
            idempotency_key = str(uuid.uuid4())
            
            # Формируем описание платежа
            description = f"Заказ #{order.short_id}"
            if hasattr(order, 'items') and order.items.exists():
                items_count = order.items.count()
                description += f" ({items_count} товар" + ("" if items_count == 1 else "ов") + ")"
            
            # URLs для возврата
            return_url = request.build_absolute_uri(
                reverse('shop:payment_success', kwargs={'order_id': order.order_id})
            )
            
            # Метаданные заказа
            metadata = {
                'order_id': str(order.order_id),
                'user_id': str(order.user.id),
                'user_email': order.