# 📝 OAuth Шпаргалка - Всё на одной странице

## 🚀 Быстрый старт (5 шагов):

```
1. Зарегистрируй приложение в соцсети
   ↓
2. Получи Client ID и Secret Key
   ↓
3. Открой Django Admin
   ↓
4. Добавь Social Application
   ↓
5. Протестируй кнопку - готово! ✅
```

---

## 🔵 ВКонтакте (5 минут)

**Регистрация**: https://vk.com/apps?act=manage
- Создать → Веб-сайт
- Адрес: `https://dobrist.com`
- Redirect: `https://dobrist.com/accounts/vk/login/callback/`

**Django Admin**: http://localhost:8000/admin/socialaccount/socialapp/add/
```
Provider: VK
Client ID: [App ID от VK]
Secret: [Secure Key от VK]
Sites: ✓ dobrist.com
```

---

## 💬 Telegram (3 минуты)

**Регистрация**: @BotFather в Telegram
```
/newbot
Имя: Добрист OAuth Bot
Username: dobrist_oauth_bot

/setdomain
https://dobrist.com
```

**Django Admin**:
```
Provider: Telegram
Client ID: [пусто]
Secret: [Token от BotFather]
Sites: ✓ dobrist.com
```

---

## 📧 Mail.ru (5 минут)

**Регистрация**: https://o2.mail.ru/app/
- Создать приложение → Веб-сайт
- Redirect: `https://dobrist.com/accounts/mailru/login/callback/`

**Django Admin**:
```
Provider: Mail.ru
Client ID: [ID приложения]
Secret: [Private Key]
Sites: ✓ dobrist.com
```

---

## 🟡 Яндекс (7 минут)

**Регистрация**: https://oauth.yandex.ru/
- Зарегистрировать приложение
- Платформы: Веб-сервисы
- Redirect: `https://dobrist.com/accounts/yandex/login/callback/`
- Доступы: ✓ Email, ✓ Аватар, ✓ Имя

**Django Admin**:
```
Provider: Yandex
Client ID: [ID]
Secret: [Пароль]
Sites: ✓ dobrist.com
```

---

## 🛠️ Проверка:

```bash
# Запустить проверку
python check_oauth_status.py

# Или
check_oauth.bat
```

**Ожидаемый результат**:
```
✅ Google      - Настроен и активен
✅ ВКонтакте   - Настроен и активен
✅ Telegram    - Настроен и активен
✅ Mail.ru     - Настроен и активен
✅ Яндекс      - Настроен и активен

📊 Настроено: 5/5
```

---

## 🐛 Частые ошибки:

| Ошибка | Причина | Решение |
|--------|---------|---------|
| "Redirect URI mismatch" | Неправильный Redirect URI | Скопируй точно: `https://dobrist.com/accounts/{provider}/login/callback/` |
| "Invalid client_id" | Лишние пробелы или неверный ID | Скопируй Client ID заново, проверь на пробелы |
| "Application not found" | Не добавлен в Django Admin | Добавь через Admin или не привязан Site |
| Кнопка не работает | Провайдер неактивен | Убедись, что Sites = dobrist.com |

---

## 📊 Приоритеты:

```
Критично (сделай первыми):
├── ⭐⭐⭐ ВКонтакте (70 млн пользователей)
└── ⭐⭐⭐ Яндекс (40 млн пользователей)

Желательно:
├── ⭐⭐ Telegram (50 млн, но растёт)
└── ⭐ Mail.ru (30 млн пользователей)
```

---

## ⏱️ Время:

- **ВКонтакте**: 5 мин
- **Telegram**: 3 мин
- **Mail.ru**: 5 мин
- **Яндекс**: 7 мин
- **Тестирование**: 5 мин

**Итого**: ~25 минут на всё!

---

## 🔗 Ссылки:

| Что | Где |
|-----|-----|
| Подробная инструкция | [OAUTH_SETUP_GUIDE.md](OAUTH_SETUP_GUIDE.md) |
| Быстрый старт | [OAUTH_QUICK_STEPS.md](OAUTH_QUICK_STEPS.md) |
| Как работает OAuth | [OAUTH_HOW_IT_WORKS.md](OAUTH_HOW_IT_WORKS.md) |
| Резюме | [OAUTH_READY.md](OAUTH_READY.md) |
| Django Admin | http://localhost:8000/admin/socialaccount/socialapp/ |

---

## 🎯 Redirect URIs (копируй как есть):

```
ВКонтакте: https://dobrist.com/accounts/vk/login/callback/
Telegram:  https://dobrist.com/accounts/telegram/login/callback/
Mail.ru:   https://dobrist.com/accounts/mailru/login/callback/
Яндекс:    https://dobrist.com/accounts/yandex/login/callback/
```

**Важно**: Слэш `/` в конце обязателен!

---

## ✅ Чек-лист:

```
Для каждого провайдера:

□ Зарегистрировал приложение в соцсети
□ Получил Client ID
□ Получил Secret Key
□ Настроил Redirect URI
□ Активировал приложение в соцсети
□ Открыл Django Admin
□ Создал Social Application
□ Выбрал правильный Provider
□ Ввёл Client ID
□ Ввёл Secret Key
□ Привязал к Site (dobrist.com)
□ Сохранил
□ Протестировал кнопку
□ Работает! ✅
```

---

## 🎨 Результат:

```
Страница логина:
┌──────────────────────────┐
│  Email: [___________]    │
│  Пароль: [__________]    │
│  [      Войти      ]     │
│                          │
│  ── Или войти через ──   │
│                          │
│  [Google] [ВКонтакте]    │
│  [Telegram] [Mail.ru]    │
│  [Войти через Яндекс]    │
└──────────────────────────┘

Все кнопки работают! 🎉
```

---

## 💡 Совет:

**Начни с ВКонтакте** - самый популярный в России, настраивается проще всего!

---

**Сохрани эту шпаргалку - она всегда под рукой! 📌**
