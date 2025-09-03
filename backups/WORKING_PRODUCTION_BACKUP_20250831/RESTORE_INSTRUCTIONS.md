# 🚨 ИНСТРУКЦИЯ ПО ВОССТАНОВЛЕНИЮ РАБОЧЕЙ КОНФИГУРАЦИИ

## ЧТО ЗДЕСЬ НАХОДИТСЯ
Этот backup содержит ВСЕ рабочие настройки продакшена на момент 31.08.2025.

## КРИТИЧЕСКИ ВАЖНЫЕ ФАЙЛЫ:
- `.env.production` - настройки продакшена (ГЛАВНЫЙ ФАЙЛ!) ⭐
- `dot_env_current` - текущий .env файл  
- `config_backup/settings.py` - основной файл настроек Django
- `system_info.txt` - информация о системе на момент backup

## 🚨 ЭКСТРЕННОЕ ВОССТАНОВЛЕНИЕ (если сайт не работает):

### Windows (PowerShell):
```powershell
# 1. Восстанавливаем главный файл продакшена
Copy-Item "backups\WORKING_PRODUCTION_BACKUP_20250831\.env.production" ".env.production"

# 2. Восстанавливаем настройки Django
Copy-Item "backups\WORKING_PRODUCTION_BACKUP_20250831\config_backup\*" "config\" -Recurse -Force

# 3. Устанавливаем правильную переменную окружения
$env:DJANGO_ENV = "production"

# 4. Проверяем, что всё работает
python manage.py check
```

### Linux/Mac:
```bash
# 1. Восстанавливаем главный файл продакшена  
cp backups/WORKING_PRODUCTION_BACKUP_20250831/.env.production .env.production

# 2. Восстанавливаем настройки Django
cp -r backups/WORKING_PRODUCTION_BACKUP_20250831/config_backup/* config/

# 3. Устанавливаем правильную переменную окружения
export DJANGO_ENV=production

# 4. Перезапускаем сервер
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# 5. Проверяем статус
sudo systemctl status gunicorn
```

## ✅ КОНТРОЛЬНЫЙ СПИСОК ВОССТАНОВЛЕНИЯ:
1. ✅ Скопирован файл .env.production
2. ✅ Скопированы файлы config/
3. ✅ Установлена переменная DJANGO_ENV=production  
4. ✅ Выполнена команда: python manage.py check
5. ✅ Перезапущен веб-сервер
6. ✅ Проверена доступность сайта dobrist.com
7. ✅ Проверены логи на ошибки

## ⚠️ КРИТИЧЕСКИ ВАЖНО:
- **НЕ УДАЛЯЙТЕ** этот backup - это ваша страховка!
- Перед любыми изменениями на продакшене **создавайте новый backup**
- **Всегда тестируйте** изменения на staging перед продакшеном
- Этот backup создан **31.08.2025** - он содержит РАБОЧУЮ конфигурацию

## 🔍 ДИАГНОСТИКА ПРОБЛЕМ:

### Если сайт всё равно не работает:
1. Проверить логи: `sudo tail -f /var/log/dobrist/django_errors.log`
2. Проверить Gunicorn: `sudo journalctl -u gunicorn -f`  
3. Проверить Nginx: `sudo nginx -t && sudo systemctl status nginx`
4. Проверить базу данных: `python manage.py dbshell`

### Команды для диагностики:
```bash
python manage.py check --deploy  # Проверка настроек продакшена
python manage.py migrate --check  # Проверка миграций
python manage.py collectstatic --dry-run  # Проверка статики
```

---

**🎯 ГЛАВНОЕ ПРАВИЛО:** Если что-то сломалось - сначала восстановите из этого backup, потом разбирайтесь в проблеме!