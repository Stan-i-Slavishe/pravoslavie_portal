# Gunicorn конфигурация для продакшена
bind = "0.0.0.0:8002"
workers = 2
worker_class = "sync"
timeout = 120
keepalive = 2
max_requests = 1000
max_requests_jitter = 100

# Логирование
accesslog = "/var/www/pravoslavie_portal/logs/gunicorn_access.log"
errorlog = "/var/www/pravoslavie_portal/logs/gunicorn_error.log"
loglevel = "info"

# Безопасность
preload_app = True
