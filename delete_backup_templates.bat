@echo off
chcp 65001 >nul
echo 🗑️ УДАЛЕНИЕ ЛИШНИХ ФАЙЛОВ ШАБЛОНОВ
echo ===================================

echo ⚠️  ВНИМАНИЕ: Будут удалены backup файлы!
echo.
echo 📁 Файлы для удаления:
echo    - story_detail.html.old (старый главный файл)
echo    - story_detail.html.bak
echo    - story_detail.html.backup_*
echo    - story_detail_clean.html
echo    - story_detail_simple.html
echo    - story_detail_fixed.html
echo    - story_detail_complete.html
echo    - detail_v2.html.bak
echo.

set /p confirm="Удалить все backup файлы? (y/N): "
if /i "%confirm%"=="y" (
    echo.
    echo 🗑️ Удаляем backup файлы...
    
    del "templates\stories\story_detail.html.old" 2>nul
    del "templates\stories\story_detail.html.bak" 2>nul
    del "templates\stories\story_detail.html.backup_*" 2>nul
    del "templates\stories\story_detail_clean.html*" 2>nul
    del "templates\stories\story_detail_simple.html*" 2>nul
    del "templates\stories\story_detail_fixed.html" 2>nul
    del "templates\stories\story_detail_complete.html" 2>nul
    del "templates\stories\detail_v2.html.bak" 2>nul
    
    echo ✅ Backup файлы удалены
) else (
    echo ❌ Удаление отменено
)

echo.
echo 📁 Оставшиеся файлы:
dir /b "templates\stories\story_detail*"

echo.
echo 🎯 Теперь в проекте только один рабочий шаблон:
echo    templates/stories/story_detail.html
echo.
pause
