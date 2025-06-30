@echo off
echo "🧹 Очистка неправильных записей аналитики..."
cd /d E:\pravoslavie_portal
python clean_analytics.py
echo.
echo "✅ Готово! Обновите дашборд аналитики:"
echo "   http://127.0.0.1:8000/analytics/dashboard/"
echo.
pause
