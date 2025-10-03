# 🔵 Настройка Telegram OAuth для dobrist.com

## ✅ Что уже сделано:
1. ✅ Установлен провайдер `allauth.socialaccount.providers.telegram`
2. ✅ Добавлена кнопка Telegram в шаблон login.html
3. ✅ Настроена конфигурация в settings_base.py

---

## 📝 Пошаговая инструкция настройки

### Шаг 1: Создать Telegram Bot

1. **Откройте Telegram** и найдите [@BotFather](https://t.me/BotFather)

2. **Создайте нового бота:**
   ```
   /newbot
   ```

3. **Введите имя бота** (отображаемое имя):
   ```
   Dobrist Login Bot
   ```

4. **Введите username бота** (должен заканчиваться на `bot`):
   ```
   dobrist_login_bot
   ```

5. **Сохраните токен**, который выдаст BotFather:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

### Шаг 2: Настроить домен для авторизации

1. **Отправьте команду в BotFather:**
   ```
   /setdomain
   ```

2. **Выберите своего бота** из списка

3. **Введите домен вашего сайта:**
   ```
   https://dobrist.com
   ```

### Шаг 3: Добавить Social App в Django Admin

1. **Запустите сервер:**
   ```bash
   python manage.py runserver
   ```

2. **Откройте Django Admin:**
   ```
   http://localhost:8000/admin/
   ```

3. **Перейдите в:** `Учетные записи социальных приложений` → `Social applications`

4. **Нажмите** "Добавить Social application"

5. **Заполните форму:**
   - **Provider:** Telegram
   - **Name:** Telegram Login
   - **Client ID:** `ваш_bot_username` (например: `dobrist_login_bot`)
   - **Secret key:** `ваш_bot_token` (полученный от BotFather)
   - **Sites:** Выберите `dobrist.com` (или `example.com` для локальной разработки)

6. **Сохраните**

### Шаг 4: Добавить переменные в .env

Добавьте в файл `.env`:

```env
# Telegram OAuth
TELEGRAM_BOT_NAME=dobrist_login_bot
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### Шаг 5: Проверка на локальном сервере

1. **Запустите сервер:**
   ```bash
   python manage.py runserver
   ```

2. **Откройте страницу входа:**
   ```
   http://localhost:8000/accounts/login/
   ```

3. **Нажмите кнопку "Telegram"**

4. **Проверьте redirect URL:**
   ```
   /accounts/telegram/login/callback/
   ```

### Шаг 6: Настройка на продакшене (dobrist.com)

1. **Обновите домен в BotFather:**
   ```
   /setdomain
   → выбрать бота
   → https://dobrist.com
   ```

2. **Обновите .env на сервере:**
   ```bash
   nano /path/to/project/.env
   ```
   
   Добавьте:
   ```env
   TELEGRAM_BOT_NAME=dobrist_login_bot
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

3. **Обновите Social App в админке:**
   - Client ID: `dobrist_login_bot`
   - Secret key: ваш токен
   - Sites: `dobrist.com`

4. **Перезапустите сервер:**
   ```bash
   sudo systemctl restart gunicorn
   sudo systemctl restart nginx
   ```

---

## 🔍 Проверка работоспособности

### 1. Проверка конфигурации:
```bash
python manage.py shell
```

```python
from allauth.socialaccount.models import SocialApp
apps = SocialApp.objects.filter(provider='telegram')
print(apps)
# Должно показать ваше приложение
```

### 2. Проверка URL:
```bash
python manage.py show_urls | grep telegram
```

Должны быть URL:
- `/accounts/telegram/login/`
- `/accounts/telegram/login/callback/`

### 3. Проверка в браузере:
- Откройте `/accounts/login/`
- Нажмите кнопку "Telegram"
- Должно открыться окно авторизации Telegram

---

## 🎨 Кастомизация кнопки (опционально)

Если хотите изменить стиль кнопки, отредактируйте `templates/account/login.html`:

```html
<a href="{% provider_login_url 'telegram' %}" class="social-btn btn-telegram">
    <i class="fab fa-telegram-plane"></i>
    Telegram
</a>
```

---

## ⚠️ Troubleshooting

### Ошибка: "SocialApp matching query does not exist"
**Решение:** Добавьте Social Application в Django Admin (Шаг 3)

### Ошибка: "Invalid bot token"
**Решение:** Проверьте токен бота в BotFather и обновите в админке

### Ошибка: "Domain not set"
**Решение:** Установите домен в BotFather командой `/setdomain`

### Кнопка не работает
**Решение:** Проверьте, что провайдер `telegram` добавлен в `INSTALLED_APPS`

---

## 📚 Дополнительные настройки

### Получение дополнительных данных пользователя

В `settings_base.py` можно настроить:

```python
SOCIALACCOUNT_PROVIDERS = {
    'telegram': {
        'AUTH_PARAMS': {
            'auth_date': True,
        },
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'username',
            'photo_url',
        ],
    }
}
```

### Автоматическое создание аккаунта

```python
SOCIALACCOUNT_AUTO_SIGNUP = True  # Автоматически создавать аккаунт
ACCOUNT_EMAIL_REQUIRED = False  # Email не обязателен для Telegram
```

---

## ✅ Чек-лист готовности

- [ ] Создан бот через BotFather
- [ ] Получен bot token
- [ ] Установлен домен в BotFather
- [ ] Добавлен Social App в Django Admin
- [ ] Добавлены переменные в .env
- [ ] Протестирована авторизация на локальном сервере
- [ ] Настроена конфигурация на продакшене
- [ ] Проверена работа на dobrist.com

---

## 🚀 Готово!

После выполнения всех шагов авторизация через Telegram будет работать на вашем сайте!

**Контакт для поддержки:** Если возникнут вопросы, обращайтесь в поддержку Telegram Bot API.
