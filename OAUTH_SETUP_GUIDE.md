# 🔐 Руководство по настройке OAuth для социальных сетей

## 📋 Общий чек-лист

- [x] Google - **УЖЕ РАБОТАЕТ** ✅
- [ ] ВКонтакте (VK)
- [ ] Telegram
- [ ] Mail.ru
- [ ] Яндекс

---

## 🔵 1. ВКонтакте (VK)

### Шаг 1: Создание приложения VK

1. Перейти на https://vk.com/apps?act=manage
2. Нажать **"Создать приложение"**
3. Заполнить форму:
   - **Название**: Добрист (или любое другое)
   - **Платформа**: Веб-сайт
   - **Адрес сайта**: `https://dobrist.com`
   - **Базовый домен**: `dobrist.com`

4. После создания открыть **"Настройки"**
5. Найти и сохранить:
   - **ID приложения** (App ID) - например: `51234567`
   - **Защищённый ключ** (Secure Key) - длинная строка

6. В разделе **"Настройки" → "Redirect URI"** добавить:
   ```
   https://dobrist.com/accounts/vk/login/callback/
   ```

7. **Включить** приложение (сделать его публичным)

### Шаг 2: Добавление в .env

Добавить в файл `.env` (или `.env.local`):

```env
# ВКонтакте OAuth
VK_APP_ID=ваш_app_id_от_vk
VK_APP_SECRET=ваш_secure_key_от_vk
```

### Шаг 3: Добавление в Django Admin

1. Запустить сервер: `python manage.py runserver`
2. Зайти в админку: http://localhost:8000/admin/
3. Найти **"Sites" → "Social applications"**
4. Нажать **"Add Social Application"**
5. Заполнить:
   - **Provider**: VK
   - **Name**: ВКонтакте
   - **Client id**: ваш VK_APP_ID
   - **Secret key**: ваш VK_APP_SECRET
   - **Sites**: выбрать `dobrist.com` (или `example.com` если тестируете локально)
6. Сохранить

---

## 💬 2. Telegram

### Шаг 1: Создание бота для OAuth

1. Открыть Telegram и найти бота **@BotFather**
2. Отправить команду: `/newbot`
3. Следовать инструкциям:
   - Ввести имя бота: `Добрист OAuth Bot`
   - Ввести username: `dobrist_oauth_bot` (должен заканчиваться на `_bot`)
4. Получить **Token** - длинная строка типа `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

5. Отправить команду: `/setdomain`
6. Выбрать своего бота
7. Ввести домен: `https://dobrist.com`

### Шаг 2: Добавление в .env

```env
# Telegram OAuth
TELEGRAM_BOT_TOKEN=ваш_токен_от_botfather
```

### Шаг 3: Добавление в Django Admin

1. Зайти в админку
2. **"Social applications" → "Add"**
3. Заполнить:
   - **Provider**: Telegram
   - **Name**: Telegram
   - **Client id**: не нужен (оставить пустым)
   - **Secret key**: ваш TELEGRAM_BOT_TOKEN
   - **Sites**: выбрать нужный сайт
4. Сохранить

---

## 📧 3. Mail.ru

### Шаг 1: Создание приложения Mail.ru

1. Перейти на https://o2.mail.ru/app/
2. Нажать **"Создать приложение"**
3. Заполнить:
   - **Название**: Добрист
   - **Тип**: Веб-сайт
   - **URL сайта**: `https://dobrist.com`
   - **Redirect URI**: `https://dobrist.com/accounts/mailru/login/callback/`

4. Получить:
   - **ID приложения** (Client ID)
   - **Секретный ключ** (Private Key)

### Шаг 2: Добавление в .env

```env
# Mail.ru OAuth
MAILRU_CLIENT_ID=ваш_client_id
MAILRU_CLIENT_SECRET=ваш_secret_key
```

### Шаг 3: Добавление в Django Admin

1. **"Social applications" → "Add"**
2. Заполнить:
   - **Provider**: Mail.ru
   - **Name**: Mail.ru
   - **Client id**: ваш MAILRU_CLIENT_ID
   - **Secret key**: ваш MAILRU_CLIENT_SECRET
   - **Sites**: выбрать нужный сайт
3. Сохранить

---

## 🟡 4. Яндекс

### Шаг 1: Создание приложения Яндекс

1. Перейти на https://oauth.yandex.ru/
2. Нажать **"Зарегистрировать новое приложение"**
3. Заполнить:
   - **Название**: Добрист
   - **Платформы**: Веб-сервисы
   - **Redirect URI**: `https://dobrist.com/accounts/yandex/login/callback/`
   - **Доступы**: 
     - ✅ Доступ к email адресу
     - ✅ Доступ к аватару
     - ✅ Доступ к имени пользователя

4. Получить:
   - **ID** (Client ID)
   - **Пароль** (Client Secret)

### Шаг 2: Добавление в .env

```env
# Яндекс OAuth
YANDEX_CLIENT_ID=ваш_client_id
YANDEX_CLIENT_SECRET=ваш_client_secret
```

### Шаг 3: Добавление в Django Admin

1. **"Social applications" → "Add"**
2. Заполнить:
   - **Provider**: Yandex
   - **Name**: Яндекс
   - **Client id**: ваш YANDEX_CLIENT_ID
   - **Secret key**: ваш YANDEX_CLIENT_SECRET
   - **Sites**: выбрать нужный сайт
3. Сохранить

---

## 🧪 Тестирование

### Локальное тестирование

Для локального тестирования нужно:

1. Добавить в `/etc/hosts` (Windows: `C:\Windows\System32\drivers\etc\hosts`):
   ```
   127.0.0.1 dobrist.local
   ```

2. В настройках приложений соцсетей использовать:
   ```
   http://dobrist.local:8000/accounts/{provider}/login/callback/
   ```

3. Или использовать ngrok для туннелирования:
   ```bash
   ngrok http 8000
   ```
   И использовать временный URL от ngrok

### Продакшен

На продакшене убедиться, что:
- Все Redirect URI правильные: `https://dobrist.com/...`
- SSL сертификат установлен
- В Django Admin выбран правильный Site (dobrist.com)

---

## 🐛 Возможные проблемы

### Проблема 1: "Redirect URI mismatch"
**Решение**: Проверить, что Redirect URI в настройках приложения точно совпадает с:
```
https://dobrist.com/accounts/{provider}/login/callback/
```

### Проблема 2: "Application not found"
**Решение**: Убедиться, что приложение добавлено в Django Admin и привязано к правильному Site

### Проблема 3: Кнопки не работают
**Решение**: Проверить, что провайдер добавлен в `INSTALLED_APPS` в settings.py

### Проблема 4: "Invalid token"
**Решение**: Перепроверить Client ID и Secret Key, возможно скопировались лишние пробелы

---

## 📝 Чек-лист перед запуском

- [ ] Все провайдеры зарегистрированы в соцсетях
- [ ] Все ключи добавлены в `.env`
- [ ] Все провайдеры добавлены в Django Admin
- [ ] Redirect URI правильные во всех приложениях
- [ ] Протестировано на локальной версии
- [ ] Протестировано на продакшене
- [ ] SSL сертификат установлен (для продакшена)

---

## 💡 Полезные ссылки

- **VK Developers**: https://vk.com/dev
- **Telegram Bot API**: https://core.telegram.org/bots
- **Mail.ru OAuth**: https://o2.mail.ru/
- **Яндекс OAuth**: https://oauth.yandex.ru/
- **django-allauth docs**: https://django-allauth.readthedocs.io/

---

## 🚀 Следующие шаги

После настройки всех провайдеров:

1. Обновить страницу логина
2. Протестировать каждую кнопку
3. Проверить, что данные пользователя корректно сохраняются
4. Настроить дополнительные разрешения (если нужно)

**Удачи с настройкой OAuth! 🎉**
