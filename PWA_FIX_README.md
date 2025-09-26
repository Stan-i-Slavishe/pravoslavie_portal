# ✅ PWA PUSH-УВЕДОМЛЕНИЯ: КРАТКАЯ ИНСТРУКЦИЯ

## 🎯 Проблема
Push-уведомления на мобильных устройствах показывают колокольчик вместо иконки сайта.

## 🔧 Решение
Добавлены правильные иконки и обновлен Service Worker.

## 📋 ЧТО СДЕЛАНО:

### 1. Файлы обновлены:
- ✅ `static/sw.js` - добавлены явные пути к иконкам
- ✅ `static/manifest.json` - добавлены все размеры иконок
- ✅ `scripts/generate_pwa_icons.py` - скрипт генерации
- ✅ `docs/PWA_ICONS_GUIDE.md` - документация
- ✅ `docs/DEPLOY_PWA_ICONS.md` - инструкция деплоя

### 2. Иконки которые нужно создать:
- `static/icons/icon-96x96.png`
- `static/icons/icon-128x128.png`
- `static/icons/icon-144x144.png`
- `static/icons/icon-384x384.png`
- `static/icons/badge-72x72.png` ⭐ **Самое важное!**

## 🚀 БЫСТРЫЙ СТАРТ (3 команды):

```bash
# 1. Генерируем иконки
python scripts/generate_pwa_icons.py

# 2. Собираем статику
python manage.py collectstatic --noinput

# 3. Коммитим в Git
git add .
git commit -m "🔔 Исправить PWA иконки уведомлений"
git push origin main
```

## 📱 НА СЕРВЕРЕ:

```bash
ssh user@server
cd /path/to/pravoslavie_portal
git pull origin main
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn nginx
```

## ✅ ПРОВЕРКА:

1. Откройте сайт на телефоне
2. Разрешите уведомления
3. Отправьте тестовое уведомление
4. **Результат:** Должна показаться иконка "ДИ" (Добрые Истории) на золотом фоне ✨

## 🆘 Если не работает:

1. Обновите Service Worker:
   - Chrome DevTools → Application → Service Workers → Update

2. Очистите кеш:
   - DevTools → Application → Clear storage → Clear site data

3. Проверьте, что badge-72x72.png создан:
   ```bash
   ls -la static/icons/badge-72x72.png
   ```

## 📚 Подробная документация:
- `docs/PWA_ICONS_GUIDE.md` - полное руководство
- `docs/DEPLOY_PWA_ICONS.md` - детальная инструкция деплоя

---

**Важно:** Badge иконка (72x72) - это ключевой файл для корректного отображения уведомлений!
