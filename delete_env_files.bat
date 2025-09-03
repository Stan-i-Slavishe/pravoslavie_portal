@echo off
echo 🧹 Удаление лишних .env файлов (Windows CMD)...

if exist .env (
    del .env
    echo ❌ Удален: .env
) else (
    echo ⚠️ Не найден: .env
)

if exist .env.lightweight (
    del .env.lightweight
    echo ❌ Удален: .env.lightweight
) else (
    echo ⚠️ Не найден: .env.lightweight
)

if exist .env.postgres_local (
    del .env.postgres_local
    echo ❌ Удален: .env.postgres_local
) else (
    echo ⚠️ Не найден: .env.postgres_local
)

if exist .env.push_test (
    del .env.push_test
    echo ❌ Удален: .env.push_test
) else (
    echo ⚠️ Не найден: .env.push_test
)

if exist .env.temp (
    del .env.temp
    echo ❌ Удален: .env.temp
) else (
    echo ⚠️ Не найден: .env.temp
)

echo.
echo ✅ Очистка завершена!
echo 📋 Проверьте результат: dir .env*
echo.
echo 🎯 Должны остаться только:
echo   - .env.local
echo   - .env.staging  
echo   - .env.production
