@echo off
echo 🚀 Запуск исправления системы заказов...

cd /d E:\pravoslavie_portal

echo 1. Исправление существующих покупок...
python fix_existing_purchases.py

echo.
echo 2. Запуск диагностики...
python diagnose_orders_issue.py

echo.
echo 3. Тестирование системы...
python test_orders_system.py

echo.
echo ✅ Все скрипты выполнены!
pause
