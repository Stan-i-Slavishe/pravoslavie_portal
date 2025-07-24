# Production Deployment Configuration

## Требования к серверу
- Ubuntu 20.04+ или CentOS 8+
- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Nginx
- SSL сертификат (Let's Encrypt)

## Environment переменные
```env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost:5432/pravoslavie_db
REDIS_URL=redis://localhost:6379/0
YOUTUBE_API_KEY=your-youtube-api-key
YOOKASSA_SHOP_ID=your-shop-id
YOOKASSA_SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password