from allauth.account.forms import SignupForm as AllauthSignupForm
from allauth.socialaccount.forms import SignupForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, Div, HTML
from crispy_forms.bootstrap import PrependedText, AppendedText
from django.conf import settings

# Кондициональный импорт reCAPTCHA
if not settings.DEBUG:
    from django_recaptcha.fields import ReCaptchaField
    from django_recaptcha.widgets import ReCaptchaV3

from .models import UserProfile


class CustomSignupForm(AllauthSignupForm):
    """Кастомная форма регистрации с условной Google reCAPTCHA v3"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Добавляем капчу только на продакшене
        if not settings.DEBUG:
            # На продакшене добавляем reCAPTCHA
            self.fields['captcha'] = ReCaptchaField(
                widget=ReCaptchaV3,
                label=''
            )
        
        # Настраиваем поля формы
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
        
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            })
        
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'class': 'form-control',
                'placeholder': 'Повторите пароль'
            })
    
    def save(self, request):
        """Сохранение пользователя (с капчей только на продакшене)"""
        user = super().save(request)
        return user


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


class UserProfileForm(forms.ModelForm):
    """Форма редактирования профиля пользователя"""
    
    first_name = forms.CharField(
        label='Имя',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя'
        })
    )
    
    last_name = forms.CharField(
        label='Фамилия',
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваша фамилия'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'bio', 'gender', 'birth_date', 'phone', 'city',
            'favorite_saints', 'confession_frequency', 'favorite_prayers', 'parish',
            'email_notifications', 'newsletter_subscription', 
            'new_content_notifications', 'order_notifications',
            'preferred_font_size', 'preferred_theme'
        ]
        
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите немного о себе...'
            }),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш город'
            }),
            'favorite_saints': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'св. Николай Чудотворец, св. Сергий Радонежский'
            }),
            'confession_frequency': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Раз в месяц, по большим праздникам'
            }),
            'favorite_prayers': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ваши любимые молитвы...'
            }),
            'parish': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Храм, который вы посещаете'
            }),
            'email_notifications': forms.Select(attrs={'class': 'form-select'}),
            'preferred_font_size': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.8',
                'max': '2.0',
                'step': '0.1'
            }),
            'preferred_theme': forms.Select(attrs={'class': 'form-select'}),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<div class="row">'),
            HTML('<div class="col-md-8">'),
            
            # Основная информация
            HTML('<div class="card mb-4">'),
            HTML('<div class="card-header"><h5 class="mb-0"><i class="bi bi-person-circle me-2"></i>Основная информация</h5></div>'),
            HTML('<div class="card-body">'),
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name', css_class='col-md-6'),
            ),
            Row(
                Column('email', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
            ),
            Row(
                Column('gender', css_class='col-md-4'),
                Column('birth_date', css_class='col-md-4'),
                Column('city', css_class='col-md-4'),
            ),
            'bio',
            HTML('</div></div>'),
            
            # Православные интересы
            HTML('<div class="card mb-4">'),
            HTML('<div class="card-header"><h5 class="mb-0"><i class="bi bi-star-fill me-2"></i>Православные интересы</h5></div>'),
            HTML('<div class="card-body">'),
            'favorite_saints',
            Row(
                Column('confession_frequency', css_class='col-md-6'),
                Column('parish', css_class='col-md-6'),
            ),
            'favorite_prayers',
            HTML('</div></div>'),
            
            # Настройки уведомлений
            HTML('<div class="card mb-4">'),
            HTML('<div class="card-header"><h5 class="mb-0"><i class="bi bi-bell-fill me-2"></i>Уведомления</h5></div>'),
            HTML('<div class="card-body">'),
            'email_notifications',
            Row(
                Column(
                    Field('newsletter_subscription', wrapper_class='form-check form-switch'),
                    css_class='col-md-4'
                ),
                Column(
                    Field('new_content_notifications', wrapper_class='form-check form-switch'),
                    css_class='col-md-4'
                ),
                Column(
                    Field('order_notifications', wrapper_class='form-check form-switch'),
                    css_class='col-md-4'
                ),
            ),
            HTML('</div></div>'),
            
            # Настройки чтения
            HTML('<div class="card mb-4">'),
            HTML('<div class="card-header"><h5 class="mb-0"><i class="bi bi-book-fill me-2"></i>Настройки чтения</h5></div>'),
            HTML('<div class="card-body">'),
            Row(
                Column('preferred_font_size', css_class='col-md-6'),
                Column('preferred_theme', css_class='col-md-6'),
            ),
            HTML('</div></div>'),
            
            HTML('</div>'),  # col-md-8
            
            # Боковая панель
            HTML('<div class="col-md-4">'),
            HTML('<div class="card sticky-top">'),
            HTML('<div class="card-header"><h5 class="mb-0"><i class="bi bi-image-fill me-2"></i>Аватар</h5></div>'),
            HTML('<div class="card-body text-center">'),
            HTML('<div class="mb-3" id="avatar-preview">'),
            HTML('{% if form.instance.avatar %}'),
            HTML('<img src="{{ form.instance.avatar.url }}" alt="Аватар" class="rounded-circle mb-3" width="150" height="150" style="object-fit: cover;">'),
            HTML('{% else %}'),
            HTML('<img src="/static/images/default-avatar.svg" alt="Аватар по умолчанию" class="rounded-circle mb-3" width="150" height="150" style="object-fit: cover;">'),
            HTML('{% endif %}'),
            HTML('</div>'),
            'avatar',
            HTML('<small class="text-muted">Рекомендуемый размер: 200x200 пикселей</small>'),
            HTML('</div>'),
            
            HTML('<div class="card-footer">'),
            Submit('submit', 'Сохранить изменения', css_class='btn btn-primary w-100'),
            HTML('</div>'),
            HTML('</div>'),
            HTML('</div>'),
            
            HTML('</div>'),  # row
        )
    
    def save(self, user=None):
        """Сохранение профиля и данных пользователя"""
        profile = super().save(commit=False)
        
        if user:
            # Обновляем данные пользователя
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.email = self.cleaned_data.get('email', '')
            user.save()
            
            profile.user = user
        
        profile.save()
        return profile


class PasswordChangeForm(forms.Form):
    """Форма смены пароля"""
    
    old_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите текущий пароль'
        })
    )
    
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите новый пароль'
        }),
        help_text='Пароль должен содержать минимум 8 символов'
    )
    
    new_password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите новый пароль'
        })
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'old_password',
            'new_password1',
            'new_password2',
            Submit('submit', 'Изменить пароль', css_class='btn btn-primary')
        )
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Неверный текущий пароль')
        return old_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError('Пароли не совпадают')
        
        return cleaned_data
    
    def save(self):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        self.user.save()
        return self.user
