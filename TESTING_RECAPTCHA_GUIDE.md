# 🧪 Тестирование Google reCAPTCHA v3 для регистрации

## 🚀 Быстрый тест

### Windows:
```cmd
python test_recaptcha_setup.py
```

### Linux/Mac:
```bash
chmod +x test_recaptcha_quick.sh
./test_recaptcha_quick.sh
```

## 🔧 Ручное тестирование

### 1. Запуск сервера разработки:
```bash
python manage.py runserver
```

### 2. Открытие формы регистрации:
```
http://127.0.0.1:8000/accounts/signup/
```

### 3. Проверка элементов:

#### ✅ Что должно быть видно:
- Поля Email, Пароль, Подтверждение пароля
- Информация "Форма защищена Google reCAPTCHA" с иконкой щита
- Красивая кнопка "Зарегистрироваться"
- Блок с социальными сетями

#### ✅ Что должно работать:
- reCAPTCHA v3 загружается невидимо (не видно галочек)
- При отправке формы капча проверяется автоматически
- Валидация паролей работает корректно
- Создание пользователя происходит только после прохождения капчи

#### ❌ Что НЕ должно быть видно:
- Видимые элементы капчи (галочки, головоломки)
- JavaScript ошибки в консоли браузера
- Ошибки 500 при отправке формы

### 4. Тестовые сценарии:

#### Сценарий 1: Успешная регистрация
1. Заполните email: `test@example.com`
2. Заполните пароль: `TestPassword123!`
3. Подтвердите пароль: `TestPassword123!`
4. Нажмите "Зарегистрироваться"
5. **Ожидаемый результат:** Пользователь создан, перенаправление на главную

#### Сценарий 2: Проверка капчи (только на продакшене)
1. Попробуйте быструю многократную отправку формы
2. **Ожидаемый результат:** На продакшене могут появиться ошибки капчи

#### Сценарий 3: Валидация формы
1. Оставьте поля пустыми или введите неправильные данные
2. **Ожидаемый результат:** Показываются ошибки валидации, капча не мешает

## 🐛 Отладка проблем

### Проблема: "reCAPTCHA validation failed"
**Решение:**
```python
# Проверьте настройки в settings.py
RECAPTCHA_PUBLIC_KEY = 'ваш-публичный-ключ'
RECAPTCHA_PRIVATE_KEY = 'ваш-приватный-ключ'
RECAPTCHA_REQUIRED_SCORE = 0.85
```

### Проблема: "ReCaptchaField not found"
**Решение:**
```bash
pip install django-recaptcha==4.0.0
```

### Проблема: Форма не отображается
**Решение:**
1. Проверьте URL: `/accounts/signup/`
2. Убедитесь что allauth настроен:
```python
# В settings.py
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.CustomSignupForm',
}
```

### Проблема: JavaScript ошибки
**Решение:**
1. Откройте Developer Tools (F12)
2. Проверьте Console на ошибки
3. Убедитесь что reCAPTCHA скрипты загружаются

## 📊 Мониторинг на продакшене

### Google reCAPTCHA Admin:
1. Перейдите: https://www.google.com/recaptcha/admin
2. Выберите сайт: `dobrist.com`
3. Просмотрите статистику:
   - Количество запросов
   - Процент заблокированных ботов
   - График активности

### Логи Django:
```bash
# Просмотр логов на сервере
tail -f /path/to/logs/django.log | grep -i recaptcha
```

### Проверка через curl (API тест):
```bash
curl -X POST https://dobrist.com/accounts/signup/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=test@example.com&password1=TestPass123&password2=TestPass123"
```

## 🔧 Настройка порога безопасности

### Текущий порог: 0.85 (высокий)

#### Если слишком много ложных срабатываний:
```python
# Снизьте порог в settings.py
RECAPTCHA_REQUIRED_SCORE = 0.7  # Среднее доверие
```

#### Если проходят боты:
```python
# Повысьте порог в settings.py
RECAPTCHA_REQUIRED_SCORE = 0.9  # Очень высокое доверие
```

#### Мониторинг и подстройка:
1. Запустите сайт с порогом 0.85
2. Наблюдайте статистику неделю
3. Корректируйте при необходимости

## 📱 Мобильное тестирование

### Адаптивность:
1. Откройте форму на телефоне
2. Проверьте отображение всех элементов
3. Убедитесь что капча работает на мобильных

### Тест на разных устройствах:
- ✅ iPhone Safari
- ✅ Android Chrome
- ✅ Desktop Chrome/Firefox
- ✅ Планшеты

## 🚀 Финальная проверка перед деплоем

### Чеклист:
- [ ] Тест `python test_recaptcha_setup.py` проходит
- [ ] Форма регистрации отображается корректно
- [ ] Капча работает в локальной разработке
- [ ] Нет JavaScript ошибок в консоли
- [ ] Мобильная версия работает
- [ ] Настройки продакшена проверены
- [ ] Ключи reCAPTCHA корректные для домена

### Команды для деплоя:
```bash
# 1. Коммит изменений
git add .
git commit -m "✅ Добавлена Google reCAPTCHA v3 в форму регистрации

- Создана кастомная форма CustomSignupForm
- Интеграция с django-allauth
- Невидимая защита от ботов
- Порог безопасности: 0.85
- Тестирование пройдено"

# 2. Пуш на сервер
git push origin main

# 3. Деплой
./deploy.sh
```

## 📚 Дополнительные ресурсы

### Документация:
- [Google reCAPTCHA v3](https://developers.google.com/recaptcha/docs/v3)
- [django-recaptcha](https://github.com/praekelt/django-recaptcha)
- [django-allauth](https://django-allauth.readthedocs.io/)

### Полезные ссылки:
- [Тестовые ключи reCAPTCHA](https://developers.google.com/recaptcha/docs/faq#id-like-to-run-automated-tests-with-recaptcha.-what-should-i-do)
- [Лучшие практики безопасности](https://developers.google.com/recaptcha/docs/verify)
- [Отладка проблем](https://developers.google.com/recaptcha/docs/troubleshooting)

---

**🎉 Поздравляем! Ваш православный портал теперь надежно защищен от ботов и спама при регистрации пользователей!**
