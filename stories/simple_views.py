from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Story, StoryComment

def story_detail_simple(request, slug):
    """Простая страница рассказа с комментариями"""
    story = get_object_or_404(Story, slug=slug, is_published=True)
    comments = story.comments.filter(is_approved=True, parent=None).order_by('-created_at')
    
    # Увеличиваем просмотры
    story.views_count += 1
    story.save()
    
    context = {
        'story': story,
        'comments': comments,
    }
    return render(request, 'stories/story_simple.html', context)

@login_required
def add_comment_simple(request, story_slug):
    """Добавление комментария"""
    if request.method == 'POST':
        story = get_object_or_404(Story, slug=story_slug, is_published=True)
        text = request.POST.get('text', '').strip()
        
        if text:
            StoryComment.objects.create(
                story=story,
                user=request.user,
                text=text
            )
            messages.success(request, 'Комментарий добавлен!')
        else:
            messages.error(request, 'Комментарий не может быть пустым')
    
    return redirect('stories:detail_simple', slug=story_slug)

@login_required
def add_reply_simple(request, comment_id):
    """Добавление ответа на комментарий"""
    if request.method == 'POST':
        parent_comment = get_object_or_404(StoryComment, id=comment_id, is_approved=True)
        text = request.POST.get('text', '').strip()
        
        if text:
            StoryComment.objects.create(
                story=parent_comment.story,
                user=request.user,
                text=text,
                parent=parent_comment
            )
            messages.success(request, 'Ответ добавлен!')
        else:
            messages.error(request, 'Ответ не может быть пустым')
    
    return redirect('stories:detail_simple', slug=parent_comment.story.slug)


@login_required
def delete_comment_simple(request, comment_id):
    
    if request.user == comment.user or request.user.is_staff:
        story_slug = comment.story.slug
        comment.delete()
        messages.success(request, 'Комментарий удален!')
        return redirect('stories:detail_simple', slug=story_slug)
    else:
        messages.error(request, 'Нет прав для удаления')
        return redirect('stories:detail_simple', slug=comment.story.slug)
