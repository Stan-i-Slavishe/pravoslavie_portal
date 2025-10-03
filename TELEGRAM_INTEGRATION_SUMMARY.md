# Telegram OAuth - Интеграция

## Что сделано

✅ Провайдер настроен в `settings_base.py`  
✅ Кнопка уже есть в `login.html`  
✅ Создана документация  

## Что нужно сделать

1. **Создать бота:** @BotFather → `/newbot`
2. **Установить домен:** `/setdomain` → `https://dobrist.com`
3. **Добавить в админке:** `/admin/socialaccount/socialapp/add/`
   - Provider: Telegram
   - Client ID: username бота
   - Secret: токен от BotFather
4. **Проверить:** `python check_telegram_oauth.bat`

## Документация

- `TELEGRAM_OAUTH_QUICKSTART.md` - быстрый старт
- `TELEGRAM_OAUTH_SETUP.md` - полная инструкция
- `check_telegram_oauth.py` - скрипт проверки

Время настройки: ~5 минут
