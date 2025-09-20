# Команды для исправления проблем с .gitignore

# КРИТИЧНО: Добавьте .env в .gitignore (уже сделано выше)

# Удалите .env из индекса git (если он уже отслеживается)
git rm --cached .env

# Добавьте дополнительные критические исключения
echo "
# Ключи и сертификаты
*.key
*.pem  
*.cert
ssl/

# Временные файлы настроек с паролями
*_local_backup.py
settings_production*.backup

# Файлы деплоя с секретами
server_commands.sh
deploy_*.sh

# Логи приложения  
error.log
access.log
gunicorn.log" >> .gitignore

# Зафиксируйте изменения
git add .gitignore
git commit -m "fix: исправлен .gitignore - добавлен .env и критические файлы"
git push origin main

echo "✅ .gitignore исправлен - теперь .env файлы не будут синхронизироваться"
