# 🚀 Быстрая настройка OAuth - Что делать прямо сейчас

## ✅ Что уже готово:
1. ✅ Провайдеры добавлены в `INSTALLED_APPS`
2. ✅ Ссылки на кнопках обновлены (используют `{% provider_login_url %}`)
3. ✅ Google OAuth уже работает
4. ✅ Дизайн кнопок готов

## 📋 Что нужно сделать:

### 1️⃣ **ВКонтакте** (самый популярный в России)

**Шаг 1**: Зарегистрировать приложение
- Перейти: https://vk.com/apps?act=manage
- Создать приложение → Веб-сайт
- Адрес сайта: `https://dobrist.com`
- Redirect URI: `https://dobrist.com/accounts/vk/login/callback/`

**Шаг 2**: Получить ключи
- **App ID** (ID приложения)
- **Secure Key** (Защищённый ключ)

**Шаг 3**: Добавить в Django
```bash
# Запустить сервер
python manage.py runserver

# Зайти в админку
http://localhost:8000/admin/socialaccount/socialapp/add/

# Заполнить:
Provider: VK
Name: ВКонтакте
Client ID: [ваш App ID]
Secret key: [ваш Secure Key]
Sites: выбрать dobrist.com
```

---

### 2️⃣ **Telegram**

**Шаг 1**: Создать бота
- Найти в Telegram: @BotFather
- Команда: `/newbot`
- Ввести имя: `Добрист OAuth Bot`
- Username: `dobrist_oauth_bot`

**Шаг 2**: Настроить домен
- Команда: `/setdomain`
- Выбрать бота
- Ввести: `https://dobrist.com`

**Шаг 3**: Добавить в Django Admin
```
Provider: Telegram
Name: Telegram
Client ID: [оставить пустым]
Secret key: [токен от BotFather]
Sites: выбрать dobrist.com
```

---

### 3️⃣ **Mail.ru**

**Шаг 1**: https://o2.mail.ru/app/
- Создать приложение → Веб-сайт
- Redirect URI: `https://dobrist.com/accounts/mailru/login/callback/`

**Шаг 2**: Добавить в Django Admin
```
Provider: Mail.ru
Name: Mail.ru
Client ID: [ID приложения]
Secret key: [Private Key]
```

---

### 4️⃣ **Яндекс**

**Шаг 1**: https://oauth.yandex.ru/
- Зарегистрировать приложение
- Платформы: Веб-сервисы
- Redirect URI: `https://dobrist.com/accounts/yandex/login/callback/`

**Шаг 2**: Добавить в Django Admin
```
Provider: Yandex
Name: Яндекс
Client ID: [ID]
Secret key: [Пароль]
```

---

## 🧪 Тестирование

После добавления каждого провайдера:

1. Обновить страницу логина
2. Кликнуть на кнопку провайдера
3. Должен произойти редирект на страницу авторизации
4. После успешной авторизации - возврат на сайт

---

## ⚠️ Важно!

### Для локального тестирования:

Если тестируешь локально (localhost):
- В настройках приложений использовать: `http://localhost:8000/accounts/.../callback/`
- В Django Admin выбрать Site: `example.com` (или создать новый для localhost)

### Для продакшена:

- Обязательно использовать HTTPS
- Redirect URI должен быть точным: `https://dobrist.com/accounts/{provider}/login/callback/`
- В Django Admin выбрать правильный Site

---

## 📊 Приоритет настройки:

1. **ВКонтакте** - самая популярная соцсеть в России ⭐⭐⭐
2. **Яндекс** - много пользователей с Яндекс аккаунтами ⭐⭐⭐
3. **Telegram** - растущая популярность ⭐⭐
4. **Mail.ru** - есть пользователи, но меньше ⭐

**Рекомендация**: Начать с ВКонтакте и Яндекса

---

## 🐛 Если что-то не работает:

1. Проверить, что провайдер добавлен в Django Admin
2. Проверить правильность Redirect URI
3. Проверить, что приложение активировано в соцсети
4. Посмотреть логи Django: `python manage.py runserver` (в консоли будут ошибки)

---

## 💡 Полезные ссылки:

- **Подробная инструкция**: `OAUTH_SETUP_GUIDE.md`
- **Django allauth docs**: https://django-allauth.readthedocs.io/
- **VK Dev**: https://vk.com/dev
- **Яндекс OAuth**: https://oauth.yandex.ru/

---

**Готово! После настройки всех провайдеров пользователи смогут входить через соцсети! 🎉**
