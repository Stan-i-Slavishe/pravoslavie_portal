# 🚨 Исправление ошибки Google OAuth: SocialApp.DoesNotExist

## 🎯 Проблема
При попытке входа через Google появляется ошибка:
```
allauth.socialaccount.models.SocialApp.DoesNotExist
```

## 🔍 Причина
В базе данных Django отсутствует запись о Google OAuth приложении, которая нужна для работы django-allauth.

## ⚡ Быстрое решение

### Вариант 1: Автоматическое исправление
Запустите master-скрипт, который все сделает автоматически:

```bash
# Остановите Django сервер, затем запустите:
master_fix_google_oauth.bat
```

### Вариант 2: Ручное исправление
1. Остановите Django сервер
2. Запустите скрипт исправления:
   ```bash
   python fix_google_oauth_complete.py
   ```
3. Запустите Django сервер:
   ```bash
   python manage.py runserver
   ```

## 🔧 Что делают скрипты

1. **check_allauth_settings.py** - проверяет настройки allauth в settings.py
2. **check_allauth_status.py** - проверяет состояние базы данных
3. **fix_google_oauth_complete.py** - исправляет проблему:
   - Создает/настраивает сайт (Site) для разработки
   - Удаляет конфликтующие Google приложения
   - Создает новое тестовое Google OAuth приложение
   - Привязывает приложение к сайту

## ✅ Результат
После выполнения скрипта:
- Ошибка `DoesNotExist` исчезнет
- Google OAuth будет работать с тестовыми ключами
- Можно будет войти через: http://127.0.0.1:8000/accounts/google/login/

## 🔑 Для продакшена

### Получение настоящих Google OAuth ключей:
1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте проект или выберите существующий
3. Включите **Google+ API** или **Google Sign-In API**
4. Создайте **OAuth 2.0 учетные данные**
5. Добавьте **Authorized redirect URIs**:
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
   - `http://localhost:8000/accounts/google/login/callback/`
   - Ваш продакшен домен: `https://yourdomain.com/accounts/google/login/callback/`

### Замена тестовых ключей:
1. Перейдите в админку: http://127.0.0.1:8000/admin/socialaccount/socialapp/
2. Отредактируйте Google OAuth приложение
3. Замените `client_id` и `secret` на настоящие

## 📁 Созданные файлы

- `master_fix_google_oauth.bat` - главный скрипт исправления
- `fix_google_oauth_complete.py` - основной скрипт исправления
- `check_allauth_settings.py` - проверка настроек
- `check_allauth_status.py` - проверка базы данных
- `quick_fix_google_oauth.py` - быстрое исправление
- `setup_google_oauth.py` - расширенная настройка

## 🛡️ Безопасность

Тестовые ключи безопасны для разработки, но НЕ используйте их в продакшене. Обязательно замените на настоящие ключи перед публикацией сайта.

## 🔄 Если проблема повторится

1. Проверьте, что не удалили записи из админки
2. Убедитесь, что `SITE_ID = 1` в settings.py
3. Проверьте, что django.contrib.sites в INSTALLED_APPS
4. Запустите скрипт исправления повторно

## 📞 Техподдержка

Если проблема не решилась:
1. Проверьте логи Django
2. Убедитесь, что все миграции применены: `python manage.py migrate`
3. Проверьте права доступа к базе данных
4. Перезапустите скрипт исправления

---

**🎉 После исправления Google OAuth будет работать корректно!**
