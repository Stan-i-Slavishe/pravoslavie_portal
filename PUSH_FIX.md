# 🔔 Исправление: Постоянный запрос Push-уведомлений

## Проблема
Браузер постоянно показывал запрос разрешения на push-уведомления при каждой загрузке страницы, даже если пользователь уже дал разрешение.

## Решение
Добавлена проверка текущего статуса разрешений перед запросом.

## Что изменено

### Файл: `static/js/pwa.js`
**Было:**
```javascript
async requestNotificationPermission() {
    const permission = await Notification.requestPermission();
```

**Стало:**
```javascript
async requestNotificationPermission() {
    // Запрашивать только если не было ответа (статус 'default')
    if (Notification.permission !== 'default') {
        console.log('ℹ️ Notification permission already set:', Notification.permission);
        return;
    }
    
    const permission = await Notification.requestPermission();
```

## Логика работы
1. ✅ **'granted'** - разрешено → не показываем запрос
2. ❌ **'denied'** - заблокировано → не показываем запрос (пользователь сам решил)
3. ❓ **'default'** - не было ответа → показываем запрос (первый раз)

## Деплой на сервер

```bash
# 1. Закоммитить изменения
git add static/js/pwa.js
git commit -m "fix: Исправлен постоянный запрос push-уведомлений"

# 2. Запушить на сервер
git push origin main

# 3. На сервере:
cd /var/www/pravoslavie_portal
git pull origin main
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn nginx
```

## Проверка
После деплоя:
- ✅ Запрос больше не появляется, если уже дан ответ
- ✅ Запрос появляется только для новых пользователей (первый визит)
- ✅ Консоль показывает логи: `ℹ️ Notification permission already set: granted`

---

**Исправлено:** {{ now }}
**Автор:** Claude AI Assistant
