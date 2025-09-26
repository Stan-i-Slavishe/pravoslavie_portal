# 🚀 Инструкция по деплою PWA иконок

## Что было изменено

### 1. Обновлен Service Worker (`static/sw.js`)
- ✅ Добавлена явная установка иконок для push-уведомлений
- ✅ Добавлена поддержка badge иконки
- ✅ Добавлена поддержка больших изображений в уведомлениях
- ✅ Улучшена группировка уведомлений по тегам
- ✅ Исправлены пути к иконкам в actions

### 2. Обновлен Manifest (`static/manifest.json`)
- ✅ Добавлены промежуточные размеры иконок (96, 128, 144, 384)
- ✅ Добавлена badge иконка для уведомлений
- ✅ Правильно настроен purpose для всех иконок

### 3. Создан скрипт генерации (`scripts/generate_pwa_icons.py`)
- ✅ Автоматическая генерация всех необходимых размеров
- ✅ Оптимизация PNG файлов
- ✅ Создание badge иконки

### 4. Добавлена документация (`docs/PWA_ICONS_GUIDE.md`)
- ✅ Инструкции по генерации иконок
- ✅ Требования к иконкам
- ✅ Troubleshooting
- ✅ Полезные ссылки

## Шаги для деплоя

### Шаг 1: Генерация недостающих иконок

```bash
# Перейдите в корень проекта
cd E:\pravoslavie_portal

# Запустите скрипт генерации
python scripts/generate_pwa_icons.py
```

**Ожидаемый результат:**
```
🎨 Генерация иконок PWA...
✅ Загружена исходная иконка: static/icons/icon-512x512.png
✅ Создан: icon-96x96.png
✅ Создан: icon-128x128.png
✅ Создан: icon-144x144.png
✅ Создан: icon-384x384.png
✅ Создан badge: badge-72x72.png
✨ Генерация иконок завершена успешно!
```

### Шаг 2: Проверка локально

1. **Соберите статику:**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Запустите dev-сервер:**
   ```bash
   python manage.py runserver
   ```

3. **Проверьте в браузере:**
   - Откройте DevTools (F12)
   - Application → Manifest → проверьте все иконки
   - Application → Service Workers → Update
   - Отправьте тестовое push-уведомление

### Шаг 3: Git коммит

```bash
# Проверьте изменения
git status

# Добавьте новые файлы
git add static/icons/icon-96x96.png
git add static/icons/icon-128x128.png
git add static/icons/icon-144x144.png
git add static/icons/icon-384x384.png
git add static/icons/badge-72x72.png
git add static/sw.js
git add static/manifest.json
git add scripts/generate_pwa_icons.py
git add docs/PWA_ICONS_GUIDE.md
git add docs/DEPLOY_PWA_ICONS.md

# Создайте коммит
git commit -m "🔔 Исправить иконки PWA push-уведомлений

- Добавлены все необходимые размеры иконок (96, 128, 144, 384)
- Создана badge иконка для уведомлений (72x72)
- Обновлен Service Worker с явными путями к иконкам
- Обновлен manifest.json с полным набором иконок
- Добавлен скрипт автоматической генерации иконок
- Добавлена документация по PWA иконкам

Теперь push-уведомления будут показывать иконку сайта вместо колокольчика"

# Отправьте в удаленный репозиторий
git push origin main
```

### Шаг 4: Деплой на сервер

#### Вариант А: Через SSH

```bash
# Подключитесь к серверу
ssh user@your-server.com

# Перейдите в директорию проекта
cd /path/to/pravoslavie_portal

# Получите изменения
git pull origin main

# Активируйте виртуальное окружение
source venv/bin/activate

# Соберите статику
python manage.py collectstatic --noinput

# Перезапустите сервисы
sudo systemctl restart gunicorn
sudo systemctl restart nginx

# Проверьте статус
sudo systemctl status gunicorn
sudo systemctl status nginx
```

#### Вариант Б: Через деплой-скрипт

```bash
# Если у вас есть deploy.sh
./deploy.sh
```

### Шаг 5: Проверка на продакшене

1. **Откройте сайт на мобильном устройстве**

2. **Проверьте PWA:**
   - Установите приложение на главный экран
   - Проверьте иконку приложения

3. **Проверьте уведомления:**
   - Разрешите push-уведомления
   - Отправьте тестовое уведомление
   - Убедитесь, что показывается правильная иконка

4. **Проверьте в DevTools:**
   ```
   Chrome DevTools → Application → Manifest
   - Все иконки загружены ✅
   - Badge иконка присутствует ✅
   
   Chrome DevTools → Application → Service Workers
   - Service Worker активен ✅
   - Версия обновлена ✅
   ```

## Проверочный чек-лист

### Перед коммитом:
- [ ] Все иконки сгенерированы
- [ ] Service Worker обновлен
- [ ] Manifest обновлен
- [ ] Локально протестировано
- [ ] Статика собрана

### После деплоя:
- [ ] Git push выполнен успешно
- [ ] Сервер обновлен (git pull)
- [ ] Статика собрана на сервере
- [ ] Сервисы перезапущены
- [ ] Иконки отображаются на мобильных
- [ ] Push-уведомления показывают правильную иконку

## Откат изменений (если что-то пошло не так)

```bash
# Откатить последний коммит
git revert HEAD

# Или вернуться к предыдущей версии
git checkout HEAD~1 -- static/sw.js
git checkout HEAD~1 -- static/manifest.json

# Пушим откат
git push origin main
```

## Полезные команды для отладки

### На сервере:

```bash
# Проверить логи Nginx
sudo tail -f /var/log/nginx/error.log

# Проверить логи Gunicorn
sudo journalctl -u gunicorn -f

# Проверить права на статику
ls -la /path/to/staticfiles/icons/

# Очистить кеш браузера (через curl)
curl -I https://your-site.com/static/sw.js
```

### В браузере:

```javascript
// Обновить Service Worker
navigator.serviceWorker.getRegistrations().then(registrations => {
  registrations.forEach(reg => reg.update());
});

// Удалить все кеши
caches.keys().then(names => {
  names.forEach(name => caches.delete(name));
});

// Отправить тестовое уведомление (в консоли DevTools)
// Нужен backend endpoint для отправки push
```

## Контакты для поддержки

Если возникли проблемы:
1. Проверьте раздел Troubleshooting в `docs/PWA_ICONS_GUIDE.md`
2. Проверьте логи сервера
3. Проверьте DevTools → Console на наличие ошибок

## Готово! 🎉

После выполнения всех шагов push-уведомления будут показывать иконку вашего сайта вместо стандартного колокольчика на всех устройствах.
