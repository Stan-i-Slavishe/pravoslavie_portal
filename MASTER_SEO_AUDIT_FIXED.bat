@echo off
title MASTER SEO AUDIT - Православный портал
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║                        MASTER SEO AUDIT SUITE                             ║
echo ║                     Православный портал "Добрые истории"                  ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
echo 🎯 КОМПЛЕКСНАЯ ПРОВЕРКА SEO ИНТЕГРАЦИИ
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo 📋 Этот audit включает:
echo    🔍 Comprehensive Test - полная проверка SEO системы
echo    📄 Templates Check - проверка шаблонов на SEO элементы  
echo    🧪 Schema.org Validation - валидация структурированных данных
echo    🛠️  Import Tests - проверка всех модулей и зависимостей
echo    📊 Quality Metrics - проверка качества по стандартам Google
echo.
echo ⏱️  Ожидаемое время: 2-3 минуты
echo 📊 Результат: детальный отчет с оценкой готовности к продакшену
echo.
pause

cd /d "E:\pravoslavie_portal"

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo 📋 ЭТАП 1: Активация окружения и подготовка
echo ═══════════════════════════════════════════════════════════════════════════
call .venv\Scripts\activate

echo ✅ Виртуальное окружение активировано
echo 🧹 Очистка Python кеша...
python clean_and_check.py > nul 2>&1

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo 🔍 ЭТАП 2: COMPREHENSIVE SEO TEST
echo ═══════════════════════════════════════════════════════════════════════════
echo 📊 Запуск полной проверки SEO интеграции...
echo.
python -u test_comprehensive_seo.py

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo 📄 ЭТАП 3: TEMPLATES SEO CHECK  
echo ═══════════════════════════════════════════════════════════════════════════
echo 🔎 Проверка шаблонов на SEO элементы...
echo.
python -u check_templates_seo.py

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo 🧪 ЭТАП 4: SCHEMA.ORG VALIDATION
echo ═══════════════════════════════════════════════════════════════════════════
echo 🏗️  Дополнительная валидация Schema.org данных...
echo.
python -u validate_schema.py

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo 🛠️  ЭТАП 5: IMPORT TESTS
echo ═══════════════════════════════════════════════════════════════════════════
echo 🔧 Проверка всех критических импортов...
echo.
python -c "import sys; sys.path.append(r'E:\pravoslavie_portal'); print('🔍 Тестирование критических импортов...'); critical_imports = [('core.seo', 'Основной SEO модуль'), ('core.seo.meta_tags', 'Мета-теги'), ('core.seo.schema_org', 'Schema.org'), ('core.templatetags.seo_tags', 'SEO templatetags'), ('core.views.main_views', 'Основные views'), ('core.views.seo_views', 'SEO views')]; failed = 0; [print(f'   ✅ {description}: {module}') if not (lambda: (exec('try: __import__(module); return False\nexcept: return True')))() else (print(f'   ❌ {description}: {module} - ошибка'), setattr(locals(), 'failed', failed + 1)) for module, description in critical_imports]; print('✨ Все критические модули импортируются успешно!') if failed == 0 else print(f'⚠️  Проблемы с {failed} модулями из {len(critical_imports)}')"

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo 🌐 ЭТАП 6: URL PATTERNS CHECK
echo ═══════════════════════════════════════════════════════════════════════════
echo 🔗 Проверка SEO URL паттернов...
echo.
python validate_urls.py

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo 📊 ЭТАП 7: SEO QUALITY METRICS
echo ═══════════════════════════════════════════════════════════════════════════
echo 🎯 Проверка качества SEO по стандартам Google...
echo.
python -u check_seo_quality.py

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo 📊 ИТОГОВЫЙ SUMMARY
echo ═══════════════════════════════════════════════════════════════════════════
echo.
echo 📋 MASTER SEO AUDIT ЗАВЕРШЕН! Результаты проверки выше.
echo.
echo 💡 ИНТЕРПРЕТАЦИЯ РЕЗУЛЬТАТОВ:
echo    🎉 90-100%% - Проект полностью готов к продакшену  
echo    ✅ 80-89%%  - Отличное состояние, мелкие доработки
echo    ⚠️  70-79%%  - Хорошо, но требуются улучшения
echo    🔧 60-69%%  - Удовлетворительно, нужна доработка
echo    ❌ 0-59%%   - Критические проблемы, требует исправления
echo.
echo 🚀 СЛЕДУЮЩИЕ ШАГИ:
echo    1. Проанализируйте результаты выше
echo    2. Исправьте выявленные проблемы (если есть)
echo    3. Запустите сервер: restart_fixed.bat
echo    4. Протестируйте SEO на реальных страницах
echo.
echo 📊 Для повторного audit запустите этот файл снова
echo 🌐 Для просмотра сайта: python manage.py runserver
echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║  ПРАВОСЛАВНЫЙ ПОРТАЛ "ДОБРЫЕ ИСТОРИИ" - SEO AUDIT COMPLETE               ║  
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.
pause
