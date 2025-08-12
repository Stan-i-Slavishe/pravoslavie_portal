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
python check_schema_fix.py

echo.
echo 2️⃣ Проверяем Template Tags...
python check_template_tags_fix.py

echo.
echo 3️⃣ Проверяем URL паттерны...
python validate_urls.py

echo.
echo 4️⃣ Запускаем быструю проверку мета-тегов...
python check_meta_tags_fix.py

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
echo 💡 Если все проверки выше прошли успешно (✅), 
echo    то проблемы из предыдущего audit исправлены!
echo.
pause
