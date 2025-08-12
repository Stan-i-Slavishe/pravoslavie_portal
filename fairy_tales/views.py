from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

def coming_soon(request):
    """Заглушка 'Скоро' для терапевтических сказок"""
    return render(request, 'fairy_tales/coming_soon.html')

@require_POST
def subscribe_notification(request):
    """Подписка на уведомления о запуске"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        child_age = data.get('child_age', '').strip()
        
        if not email:
            return JsonResponse({'error': 'Email обязателен'}, status=400)
        
        # Здесь можно сохранить в БД или отправить админу
        # Пока просто логируем
        logger.info(f"Новая подписка на сказки: {email}, возраст ребенка: {child_age}")
        
        # Опционально: отправить email админу
        try:
            admin_emails = getattr(settings, 'ADMIN_EMAIL_LIST', [])
            if admin_emails:
                send_mail(
                    subject='Новая подписка на терапевтические сказки',
                    message=f'Email: {email}\nВозраст ребенка: {child_age}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=admin_emails,
                    fail_silently=True,
                )
        except Exception as e:
            logger.error(f"Ошибка отправки email админу: {e}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Спасибо за подписку! Мы обязательно уведомим вас о запуске.'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Некорректные данные'}, status=400)
    except Exception as e:
        logger.error(f"Ошибка при подписке: {e}")
        return JsonResponse({'error': 'Произошла ошибка'}, status=500)

# Остальные views можно оставить для будущего использования, но закомментировать

"""
# БУДУЩИЕ VIEWS - РАЗКОММЕНТИРОВАТЬ ПРИ ЗАПУСКЕ СКАЗОК

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count
from decimal import Decimal

from .models import (
    FairyTaleCategory, 
    FairyTaleTemplate, 
    PersonalizationOrder, 
    FairyTaleReview,
    FairyTaleFavorite,
    TherapeuticGoal,
    AgeGroup
)

# Здесь будут все остальные views когда запустим сказки...
"""
