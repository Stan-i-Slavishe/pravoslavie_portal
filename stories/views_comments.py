"""
YouTube-style комментарии для рассказов
AJAX views без перезагрузки страницы
"""

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, Count, Prefetch
import json

from .models import Story, StoryComment, CommentReaction, CommentReport
from django.contrib.auth.models import User


@require_http_methods(["GET"])
def load_comments(request, story_slug):
    """Загрузка комментариев для рассказа (AJAX)"""
    try:
        story = get_object_or_404(Story, slug=story_slug, is_published=True)
        page = int(request.GET.get('page', 1))
        sort_by = request.GET.get('sort', 'newest')  # newest, oldest, top
        
        # Получаем комментарии верхнего уровня (не ответы)
        comments_query = StoryComment.objects.filter(
            story=story,
            parent=None,
            is_approved=True
        ).select_related('user').prefetch_related(
            Prefetch(
                'replies',
                queryset=StoryComment.objects.filter(is_approved=True).select_related('user')[:3],
                to_attr='top_replies'
            )
        )
        
        # Сортировка
        if sort_by == 'oldest':
            comments_query = comments_query.order_by('created_at')
        elif sort_by == 'top':
            comments_query = comments_query.order_by('-likes_count', '-created_at')
        else:  # newest
            comments_query = comments_query.order_by('-created_at')
        
        # Пагинация
        paginator = Paginator(comments_query, 20)  # 20 комментариев на страницу
        comments_page = paginator.get_page(page)
        
        # Получаем реакции пользователя (если авторизован)
        user_reactions = {}
        if request.user.is_authenticated:
            reactions = CommentReaction.objects.filter(
                user=request.user,
                comment__in=[c.id for c in comments_page.object_list]
            ).values('comment_id', 'reaction_type')
            user_reactions = {r['comment_id']: r['reaction_type'] for r in reactions}
        
        # Рендерим HTML комментариев
        comments_html = render_to_string('stories/ajax/comments_list.html', {
            'comments': comments_page.object_list,
            'user_reactions': user_reactions,
            'user': request.user,
        })
        
        return JsonResponse({
            'success': True,
            'html': comments_html,
            'has_next': comments_page.has_next(),
            'has_previous': comments_page.has_previous(),
            'current_page': page,
            'total_pages': paginator.num_pages,
            'total_comments': paginator.count,
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка загрузки комментариев: {str(e)}'
        }, status=500)


@require_POST
@login_required
def add_comment(request, story_slug):
    """Добавление нового комментария (AJAX)"""
    try:
        story = get_object_or_404(Story, slug=story_slug, is_published=True)
        
        # Получаем данные из POST
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        parent_id = data.get('parent_id')
        
        if not text:
            return JsonResponse({
                'success': False,
                'error': 'Комментарий не может быть пустым'
            }, status=400)
        
        if len(text) > 1000:
            return JsonResponse({
                'success': False,
                'error': 'Комментарий слишком длинный (максимум 1000 символов)'
            }, status=400)
        
        # Проверяем родительский комментарий (если это ответ)
        parent = None
        if parent_id:
            try:
                parent = StoryComment.objects.get(
                    id=parent_id,
                    story=story,
                    is_approved=True
                )
            except StoryComment.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Родительский комментарий не найден'
                }, status=400)
        
        # Создаем комментарий
        comment = StoryComment.objects.create(
            story=story,
            user=request.user,
            text=text,
            parent=parent
        )
        
        # Рендерим HTML нового комментария
        comment_html = render_to_string('stories/ajax/comment_item.html', {
            'comment': comment,
            'user': request.user,
            'user_reactions': {},
        })
        
        return JsonResponse({
            'success': True,
            'message': 'Комментарий добавлен!',
            'html': comment_html,
            'comment_id': comment.id,
            'is_reply': comment.is_reply,
            'parent_id': parent.id if parent else None,
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Неверный формат данных'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка при добавлении комментария: {str(e)}'
        }, status=500)


@require_POST
@login_required
def toggle_comment_reaction(request, comment_id):
    """Переключение лайка/дизлайка комментария (AJAX)"""
    try:
        comment = get_object_or_404(StoryComment, id=comment_id, is_approved=True)
        
        data = json.loads(request.body)
        reaction_type = data.get('reaction_type')
        
        if reaction_type not in ['like', 'dislike']:
            return JsonResponse({
                'success': False,
                'error': 'Неверный тип реакции'
            }, status=400)
        
        # Получаем существующую реакцию пользователя
        existing_reaction = CommentReaction.objects.filter(
            comment=comment,
            user=request.user
        ).first()
        
        if existing_reaction:
            if existing_reaction.reaction_type == reaction_type:
                # Убираем реакцию (пользователь нажал на ту же кнопку)
                existing_reaction.delete()
                user_reaction = None
                message = 'Реакция убрана'
            else:
                # Меняем тип реакции
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
                user_reaction = reaction_type
                message = f'Реакция изменена на {reaction_type}'
        else:
            # Создаем новую реакцию
            CommentReaction.objects.create(
                comment=comment,
                user=request.user,
                reaction_type=reaction_type
            )
            user_reaction = reaction_type
            message = f'{reaction_type.title()} добавлен'
        
        # Обновляем счетчики
        comment.refresh_from_db()
        
        return JsonResponse({
            'success': True,
            'message': message,
            'likes_count': comment.likes_count,
            'dislikes_count': comment.dislikes_count,
            'user_reaction': user_reaction,
            'reaction_score': comment.get_reaction_score(),
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Неверный формат данных'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка при обработке реакции: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def load_replies(request, comment_id):
    """Загрузка ответов на комментарий (AJAX)"""
    try:
        comment = get_object_or_404(StoryComment, id=comment_id, is_approved=True)
        page = int(request.GET.get('page', 1))
        
        # Получаем ответы
        replies = StoryComment.objects.filter(
            parent=comment,
            is_approved=True
        ).select_related('user').order_by('created_at')
        
        # Пагинация для ответов
        paginator = Paginator(replies, 10)  # 10 ответов на страницу
        replies_page = paginator.get_page(page)
        
        # Получаем реакции пользователя на ответы
        user_reactions = {}
        if request.user.is_authenticated:
            reactions = CommentReaction.objects.filter(
                user=request.user,
                comment__in=[r.id for r in replies_page.object_list]
            ).values('comment_id', 'reaction_type')
            user_reactions = {r['comment_id']: r['reaction_type'] for r in reactions}
        
        # Рендерим HTML ответов
        replies_html = render_to_string('stories/ajax/replies_list.html', {
            'replies': replies_page.object_list,
            'user_reactions': user_reactions,
            'user': request.user,
            'parent_comment': comment,
        })
        
        return JsonResponse({
            'success': True,
            'html': replies_html,
            'has_next': replies_page.has_next(),
            'current_page': page,
            'total_pages': paginator.num_pages,
            'total_replies': paginator.count,
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка загрузки ответов: {str(e)}'
        }, status=500)


@require_POST
@login_required
def edit_comment(request, comment_id):
    """Редактирование комментария (AJAX)"""
    try:
        comment = get_object_or_404(
            StoryComment,
            id=comment_id,
            user=request.user,  # Только автор может редактировать
            is_approved=True
        )
        
        data = json.loads(request.body)
        new_text = data.get('text', '').strip()
        
        if not new_text:
            return JsonResponse({
                'success': False,
                'error': 'Комментарий не может быть пустым'
            }, status=400)
        
        if len(new_text) > 1000:
            return JsonResponse({
                'success': False,
                'error': 'Комментарий слишком длинный (максимум 1000 символов)'
            }, status=400)
        
        # Обновляем комментарий
        comment.text = new_text
        comment.is_edited = True
        comment.save(update_fields=['text', 'is_edited', 'updated_at'])
        
        return JsonResponse({
            'success': True,
            'message': 'Комментарий обновлен',
            'new_text': comment.text,
            'is_edited': comment.is_edited,
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Неверный формат данных'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка при редактировании: {str(e)}'
        }, status=500)


@require_POST
@login_required
def delete_comment(request, comment_id):
    """Удаление комментария (AJAX)"""
    try:
        comment = get_object_or_404(StoryComment, id=comment_id, is_approved=True)
        
        # Проверяем права на удаление (автор или администратор)
        if comment.user != request.user and not request.user.is_staff:
            return JsonResponse({
                'success': False,
                'error': 'У вас нет прав на удаление этого комментария'
            }, status=403)
        
        # Сохраняем информацию для ответа
        is_reply = comment.is_reply
        parent_id = comment.parent.id if comment.parent else None
        
        # Удаляем комментарий
        comment.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Комментарий удален',
            'is_reply': is_reply,
            'parent_id': parent_id,
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка при удалении: {str(e)}'
        }, status=500)


@require_POST
@login_required
def report_comment(request, comment_id):
    """Жалоба на комментарий (AJAX)"""
    try:
        comment = get_object_or_404(StoryComment, id=comment_id, is_approved=True)
        
        data = json.loads(request.body)
        reason = data.get('reason')
        description = data.get('description', '').strip()
        
        if reason not in [choice[0] for choice in CommentReport.REPORT_REASONS]:
            return JsonResponse({
                'success': False,
                'error': 'Неверная причина жалобы'
            }, status=400)
        
        # Проверяем, не жаловался ли пользователь уже
        if CommentReport.objects.filter(comment=comment, reporter=request.user).exists():
            return JsonResponse({
                'success': False,
                'error': 'Вы уже жаловались на этот комментарий'
            }, status=400)
        
        # Создаем жалобу
        CommentReport.objects.create(
            comment=comment,
            reporter=request.user,
            reason=reason,
            description=description
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Жалоба отправлена. Спасибо за помощь в поддержании порядка!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Неверный формат данных'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка при отправке жалобы: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def comments_stats(request, story_slug):
    """Получение статистики комментариев (AJAX)"""
    try:
        story = get_object_or_404(Story, slug=story_slug, is_published=True)
        
        # Подсчитываем статистику
        total_comments = StoryComment.objects.filter(
            story=story,
            is_approved=True
        ).count()
        
        top_level_comments = StoryComment.objects.filter(
            story=story,
            parent=None,
            is_approved=True
        ).count()
        
        total_replies = total_comments - top_level_comments
        
        return JsonResponse({
            'success': True,
            'total_comments': total_comments,
            'top_level_comments': top_level_comments,
            'total_replies': total_replies,
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка получения статистики: {str(e)}'
        }, status=500)
