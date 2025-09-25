#!/usr/bin/env python
"""
Тест блокировки Google reCAPTCHA v3
Симулирует поведение бота для проверки защиты
"""
import requests
import time

def test_recaptcha_blocking():
    """Тестируем блокировку reCAPTCHA множественными запросами"""
    
    url = 'https://dobrist.com/accounts/signup/'
    
    print("🤖 ТЕСТ БЛОКИРОВКИ GOOGLE reCAPTCHA v3")
    print("=" * 60)
    print("Отправляем множественные запросы регистрации...")
    print()
    
    # Получаем CSRF токен
    session = requests.Session()
    response = session.get(url)
    
    # Пытаемся зарегистрироваться 10 раз подряд
    for i in range(10):
        data = {
            'email': f'bot-test-{i}@example.com',
            'password1': 'BotPassword123!',
            'password2': 'BotPassword123!',
        }
        
        try:
            response = session.post(url, data=data, timeout=5)
            
            if 'recaptcha' in response.text.lower() or 'captcha' in response.text.lower():
                print(f"❌ Попытка {i+1}: ЗАБЛОКИРОВАНО reCAPTCHA!")
                print(f"   Код ответа: {response.status_code}")
                return True
            elif response.status_code == 200:
                print(f"✅ Попытка {i+1}: Прошла (пока)")
            else:
                print(f"⚠️ Попытка {i+1}: Код {response.status_code}")
                
        except Exception as e:
            print(f"❌ Попытка {i+1}: Ошибка - {e}")
        
        time.sleep(0.1)  # Минимальная задержка (бот-поведение)
    
    print()
    print("⚠️ reCAPTCHA не сработала после 10 попыток")
    print("Возможно нужно больше запросов или другой паттерн")
    return False

if __name__ == "__main__":
    test_recaptcha_blocking()
