@echo off
echo =======================================
echo ПОИСК IFRAME В ШАБЛОНЕ
echo =======================================

cd /d E:\pravoslavie_portal

echo.
echo Ищем строки с iframe в шаблоне...
findstr /n /i "iframe\|youtube_embed_id\|video-container" templates\stories\story_detail.html

echo.
echo Ищем блок content...
findstr /n /i "block content" templates\stories\story_detail.html

pause
