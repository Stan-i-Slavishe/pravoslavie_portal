# 🐳 Православный портал - Production Dockerfile
FROM python:3.11-slim

# 📝 Метаданные
LABEL maintainer="Pravoslavie Portal Team"
LABEL description="Orthodox Christian Portal with therapeutic fairy tales"
LABEL version="1.0"

# 🛠️ Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    gettext \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 📂 Создание рабочей директории
WORKDIR /app

# 📦 Копирование и установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 📁 Копирование проекта
COPY . .

# 🔧 Создание необходимых директорий
RUN mkdir -p /app/logs /app/media /app/staticfiles

# 👤 Создание пользователя для безопасности
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# 🚀 Сборка статических файлов
RUN python manage.py collectstatic --noinput --settings=config.settings

# 🌐 Открытие порта
EXPOSE 8000

# 🎯 Команда запуска
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "config.wsgi:application"]
