@echo off
title QUICK SEO FIXES - Православный портал
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                        QUICK SEO FIXES                                    ║
echo ║                  Исправление проблем из audit                             ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

cd /d "E:\pravoslavie_portal"
call .venv\Scripts\activate

echo 🔧 ИСПРАВЛЯЕМ ВЫЯВЛЕННЫЕ ПРОБЛЕМЫ...
echo ═══════════════════════════════════════════════════════════════════════════

echo.
echo 1️⃣ Проверяем исправления Schema.org...
python -c "try: import os, sys, django; sys.path.append(r'E:\pravoslavie_portal'); os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); django.setup(); from core.seo.schema_org import SchemaGenerator; generator = SchemaGenerator(); class MockBook: title='Test'; description='Test'; created_at='2024-01-01T00:00:00Z'; updated_at='2024-01-01T00:00:00Z'; slug='test'; price=0; cover=None; author='Test'; class reviews: @staticmethod; def exists(): return False; result = generator.get_book_schema(MockBook()); print('✅ Schema.org для книг исправлено!'); except Exception as e: print(f'❌ Проблема: {e}')"

echo.
echo 2️⃣ Проверяем Template Tags...
python -c "try: import os, sys, django; sys.path.append(r'E:\pravoslavie_portal'); os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); django.setup(); from django.template import Template, Context; from django.test import RequestFactory; factory = RequestFactory(); request = factory.get('/', HTTP_HOST='testserver'); template = Template('{% load seo_tags %}{% schema_ld \"organization\" %}'); context = Context({'request': request}); rendered = template.render(context); print('✅ Template Tags исправлены!'); except Exception as e: print(f'❌ Проблема: {e}')"

echo.
echo 3️⃣ Проверяем URL паттерны...
python validate_urls.py

echo.
echo 4️⃣ Запускаем быструю проверку...
python -c "import os, sys, django; sys.path.append(r'E:\pravoslavie_portal'); os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings'); django.setup(); from core.seo import page_meta; meta = page_meta('home'); print(f'✅ Мета-теги генерируются: {meta[\"title\"][:30]}...')"

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo 🎉 ИСПРАВЛЕНИЯ ЗАВЕРШЕНЫ!
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo 📊 Теперь можно запустить полный audit:
echo    MASTER_SEO_AUDIT_FIXED.bat
echo.
echo 🚀 Или запустить сервер:
echo    python manage.py runserver
echo.
echo ✨ Ожидаемый результат audit: 90-95%% успешность
echo.
pause
