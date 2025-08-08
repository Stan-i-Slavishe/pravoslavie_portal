@echo off
echo 🔧 Исправили проблему с namespace 'fairy-tales'...
echo.

cd /d "E:\pravoslavie_portal"

echo 📋 Проверяем все URL namespaces...
python check_namespaces.py

echo.
echo ✅ Исправление применено:
echo    templates/core/tag_detail.html строка 151
echo    'fairy-tales:list' заменено на 'fairy_tales:list'
echo.
echo 🌐 Теперь проверьте страницы тегов:
echo    http://127.0.0.1:8000/tags/vera/
echo    http://127.0.0.1:8000/tags/doch/
echo.
pause
