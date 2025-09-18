# 🛡️ GUIDE: Безопасная синхронизация production настроек

## ⚠️ ВАЖНО: Защита production настроек

На продакшн сервере файл `config/settings_production.py` защищен от перезаписи git'ом:
- Используется `git update-index --skip-worktree`
- Добавлен в `.gitignore`
- Создаются бэкапы: `settings_production_working.py` и `.env_working`

## 🔄 Безопасная синхронизация

### На локальной машине:
```bash
# 1. Сохранить локальные настройки
cp config/settings_production.py config/settings_production_local_backup.py

# 2. Отправить изменения (кроме защищенных файлов)
git add .
git commit -m "Update project files (excluding production settings)"
git push origin main
```

### На продакшн сервере:
```bash
# 1. Синхронизировать изменения
git pull origin main

# 2. Проверить что защищенные настройки остались
ls -la config/settings_production*
git ls-files -v | grep settings_production

# 3. Если что-то пошло не так - восстановить
cp config/settings_production_working.py config/settings_production.py
cp .env_working .env
sudo systemctl restart gunicorn
```

## 📋 Файлы под защитой:

- `config/settings_production.py` - production настройки Django
- `.env` - переменные окружения для production
- `.env_working` - бэкап рабочих переменных
- `config/settings_production_working.py` - бэкап рабочих настроек

## 🚨 В случае проблем:

1. Проверить статус защиты: `git ls-files -v | grep S`
2. Восстановить из бэкапа: `cp config/settings_production_working.py config/settings_production.py`
3. Перезапустить сервис: `sudo systemctl restart gunicorn`

---
**Создано:** $(date)
**Проект:** Православный портал (dobrist.com)
