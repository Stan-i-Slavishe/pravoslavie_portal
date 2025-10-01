# 🚀 Быстрый старт: Telegram OAuth для dobrist.com

## ⚡ За 5 минут до запуска

### 1. Создайте бота (2 минуты)
1. Откройте Telegram → найдите [@BotFather](https://t.me/BotFather)
2. Отправьте: `/newbot`
3. Имя бота: `Dobrist Login Bot`
4. Username: `dobrist_login_bot`
5. **Сохраните токен!** (выглядит так: `123456789:ABCdefGHI...`)

### 2. Настройте домен (1 минута)
1. В BotFather: `/setdomain`
2. Выберите бота
3. Введите: `https://dobrist.com` (или `http://localhost:8000` для теста)

### 3. Добавьте в Django Admin (2 минуты)
1. Запустите: `python manage.py runserver`
2. Откройте: `http://localhost:8000/admin/`
3. `Social applications` → `Add`
4. Заполните:
   - **Provider:** `Telegram`
   - **Name:** `Telegram Login`
   - **Client ID:** `dobrist_login_bot` (ваш username)
   - **Secret key:** `123456789:ABCdef...` (ваш токен)
   - **Sites:** выберите ваш сайт
5. Сохраните

### 4. Проверьте (30 секунд)
```bash
python check_telegram_oauth.bat
```

### 5. Тестируйте! 🎉
Откройте: `http://localhost:8000/accounts/login/`
Нажмите кнопку **Telegram** → должно работать!

---

## 📝 Для продакшена (dobrist.com)

### В .env добавьте:
```env
TELEGRAM_BOT_NAME=dobrist_login_bot
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
```

### Обновите Social App в админке:
- Client ID: `dobrist_login_bot`
- Sites: `dobrist.com` ✅

### Перезапустите сервер:
```bash
sudo systemctl restart gunicorn
```

---

## ✅ Готово!
Теперь пользователи могут войти через Telegram на **dobrist.com**!

---

## 🔧 Если что-то не работает

### Проблема: Кнопка не реагирует
**Решение:** Проверьте, что Social App создан в админке

### Проблема: "Invalid bot token"
**Решение:** Проверьте токен в BotFather → `/token`

### Проблема: "Domain not set"
**Решение:** `/setdomain` в BotFather → введите домен

### Проблема: Redirect loop
**Решение:** Проверьте, что домен в BotFather совпадает с вашим сайтом

---

## 📞 Нужна помощь?

Запустите диагностику:
```bash
python check_telegram_oauth.bat
```

Скрипт покажет, что настроено, а что нужно исправить!

---

**Документация:** [TELEGRAM_OAUTH_SETUP.md](TELEGRAM_OAUTH_SETUP.md)
