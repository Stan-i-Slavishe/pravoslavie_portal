from allauth.socialaccount.forms import SignupForm
from django import forms

class CustomSocialSignupForm(SignupForm):
    """Упрощенная форма социальной регистрации"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Убираем требование пароля для социальной регистрации
        if 'password1' in self.fields:
            del self.fields['password1']
        if 'password2' in self.fields:
            del self.fields['password2']
    
    def save(self, request):
        # Просто сохраняем пользователя без дополнительных полей
        user = super().save(request)
        return user
