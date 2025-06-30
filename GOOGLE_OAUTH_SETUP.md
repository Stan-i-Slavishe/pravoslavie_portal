# 🚀 Быстрая настройка Google OAuth

## Что нужно сделать:

### 1. Создать приложение в Google Console
- Перейти: https://console.cloud.google.com/
- Создать проект: "Православие Портал"
- Включить Google+ API
- Создать OAuth 2.0 Client ID
- Добавить redirect URI: `http://127.0.0.1:8000/accounts/google/login/callback/`

### 2. Добавить учетные данные в .env
```bash
GOOGLE_OAUTH2_CLIENT_ID=ваш_client_id_здесь
GOOGLE_OAUTH2_SECRET=ваш_secret_здесь
```

### 3. Выполнить настройку Django
```bash
python manage.py migrate
python manage.py setup_google_oauth
python manage.py runserver
```

### 4. Тестировать
- Открыть: http://127.0.0.1:8000/accounts/login/
- Нажать "Войти через социальные сети"
- Нажать "Google"
- Должен открыться Google OAuth

## Команды для отладки:

```bash
# Проверить настройки
python manage.py setup_google_oauth

# Создать суперпользователя
python manage.py createsuperuser

# Посмотреть админку
http://127.0.0.1:8000/admin/

# Прямая ссылка на Google OAuth
http://127.0.0.1:8000/accounts/google/login/
```

## Если что-то не работает:

1. **Проверить .env файл** - правильные ли Client ID и Secret
2. **Проверить админку** - есть ли Social Application для Google
3. **Проверить сайт** - domain должен быть 127.0.0.1:8000
4. **Проверить Google Console** - правильный ли redirect URI

## Готовые команды:

```bash
# Полная перенастройка
python manage.py setup_google_oauth --client-id=ВАШ_ID --secret=ВАШ_SECRET

# Только проверка
python manage.py setup_google_oauth
```
