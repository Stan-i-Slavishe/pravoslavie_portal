@echo off
echo 🧹 ПОЛНАЯ ОЧИСТКА БРАУЗЕРА И СИСТЕМЫ
echo.

echo 🔄 Очищаем DNS кеш...
ipconfig /flushdns

echo 🌐 Сбрасываем сетевые настройки...
netsh winsock reset
netsh int ip reset

echo 📱 Закрываем все браузеры...
taskkill /f /im chrome.exe >nul 2>&1
taskkill /f /im firefox.exe >nul 2>&1
taskkill /f /im edge.exe >nul 2>&1
taskkill /f /im opera.exe >nul 2>&1

echo ⏳ Ждем 3 секунды...
timeout /t 3 /nobreak >nul

echo 🗑️ Очищаем временные файлы...
del /q /s "%TEMP%\*" >nul 2>&1
del /q /s "%LOCALAPPDATA%\Temp\*" >nul 2>&1

echo.
echo ✅ Очистка завершена!
echo.
echo 📋 ЧТО ДЕЛАТЬ ДАЛЬШЕ:
echo.
echo 1. 🚀 Запустите: nuclear_fix.bat
echo 2. 🌐 Откройте НОВОЕ окно браузера
echo 3. 🔗 Идите на: http://127.0.0.1:8080 (порт 8080!)
echo 4. ❌ НЕ используйте порт 8000!
echo 5. ❌ НЕ используйте HTTPS!
echo.
echo 💡 Если браузер пытается перенаправить на HTTPS:
echo    - Печатайте URL вручную: http://127.0.0.1:8080
echo    - Используйте режим инкогнито
echo    - Или другой браузер
echo.

pause
