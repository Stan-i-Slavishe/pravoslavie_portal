# Исправление проблемы с Google OAuth

## Проблема
Постоянно появлялась страница "Вход через Google" (`/accounts/google/login/`) с ошибкой "DoesNotExist", хотя мы пытались ее убрать редиректом.

## Причина
В настройках Django были включены провайдеры социальной аутентификации, но не настроены в админке:

1. В `settings_base.py` были включены все провайдеры allauth
2. В `settings_local_postgresql.py` были настройки SOCIALACCOUNT
3. Django автоматически создавал URL'ы для Google OAuth

## Решение

### 1. Отключение провайдеров в settings_base.py
```python
THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Провайдеры социальных сетей (отключены)
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.vk',
    # 'allauth.socialaccount.providers.telegram',
    # 'allauth.socialaccount.providers.mailru',
    # 'allauth.socialaccount.providers.yandex',
]
```

### 2. Отключение настроек в settings_local_postgresql.py
```python
# Отключаем социальную аутентификацию Google
# SOCIALACCOUNT_LOGIN_ON_GET = True
# SOCIALACCOUNT_AUTO_SIGNUP = True
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }
```

## Результат

После изменений:
- ✅ Страница `/accounts/google/login/` больше не генерируется
- ✅ Нет ошибок "DoesNotExist" 
- ✅ Пользователи используют только стандартную аутентификацию Django
- ✅ Админка работает корректно

## Если понадобится включить Google OAuth в будущем

1. Раскомментировать провайдер в `settings_base.py`
2. Раскомментировать настройки в локальном файле настроек
3. Создать Google OAuth приложение в Google Cloud Console
4. Добавить SocialApp в Django Admin с ключами от Google
5. Настроить правильные redirect URLs

## Команды для применения изменений

```bash
# Локально
python manage.py runserver

# На сервере через git
git add .
git commit -m "Отключение Google OAuth провайдеров"
git push
systemctl restart gunicorn
```

Теперь сайт использует только стандартную аутентификацию Django без внешних провайдеров.
