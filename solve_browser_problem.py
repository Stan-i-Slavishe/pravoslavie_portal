#!/usr/bin/env python
"""
Полная очистка браузерных настроек и запуск Django
"""
import os
import subprocess
import sys

def clear_django_cache():
    """Очищает Django кеш и сессии"""
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        import django
        django.setup()
        
        # Очищаем сессии
        from django.contrib.sessions.models import Session
        Session.objects.all().delete()
        print("✅ Django sessions cleared")
        
        # Очищаем кеш
        from django.core.cache import cache
        cache.clear()
        print("✅ Django cache cleared")
        
    except Exception as e:
        print(f"⚠️ Cache clear error: {e}")

def fix_settings():
    """Исправляет настройки Django для HTTP"""
    try:
        with open('config/settings.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Отключаем принуждение к HTTPS
        content = content.replace('SECURE_SSL_REDIRECT = True', 'SECURE_SSL_REDIRECT = False')
        
        # Добавляем настройку если её нет
        if 'SECURE_SSL_REDIRECT' not in content:
            content += '\n# Disable HTTPS redirect for development\nSECURE_SSL_REDIRECT = False\n'
        
        with open('config/settings.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Django settings fixed")
        
    except Exception as e:
        print(f"⚠️ Settings fix error: {e}")

def create_browser_reset_page():
    """Создает HTML страницу для сброса браузера"""
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Django Browser Reset</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        .link { font-size: 24px; color: blue; text-decoration: underline; }
        .address { font-family: monospace; background: #f0f0f0; padding: 10px; }
    </style>
</head>
<body>
    <h1>🌐 Django Browser Reset</h1>
    <p>Click the link below to open Django with HTTP:</p>
    <p><a href="http://127.0.0.1:8000/" class="link">👉 Open Django HTTP Server</a></p>
    <p>Or copy this address to your browser:</p>
    <div class="address">http://127.0.0.1:8000/</div>
    
    <h2>💡 If problems persist:</h2>
    <ul>
        <li>Clear browser cache (Ctrl+Shift+Delete)</li>
        <li>Use incognito/private mode</li>
        <li>Try a different browser</li>
        <li>Restart your computer</li>
    </ul>
</body>
</html>"""
    
    with open('browser_reset.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Browser reset page created: browser_reset.html")

def main():
    print("🔧 DJANGO BROWSER PROBLEM SOLVER")
    print("=" * 40)
    
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Run from Django project root.")
        return
    
    print("\n1️⃣ Clearing Django cache and sessions...")
    clear_django_cache()
    
    print("\n2️⃣ Fixing Django settings...")
    fix_settings()
    
    print("\n3️⃣ Creating browser reset page...")
    create_browser_reset_page()
    
    print("\n🎯 SOLUTION:")
    print("1. Open the file: browser_reset.html")
    print("2. Click the link to open Django")
    print("3. Or manually go to: http://127.0.0.1:8000/")
    
    choice = input("\nStart Django HTTP server now? (y/n): ").lower()
    
    if choice == 'y':
        print("\n🚀 Starting Django HTTP server...")
        print("   Address: http://127.0.0.1:8000/")
        print("   Press Ctrl+C to stop")
        print()
        
        try:
            subprocess.run([sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'])
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
    else:
        print("\n✅ Ready! Open browser_reset.html when you're ready.")

if __name__ == '__main__':
    main()
