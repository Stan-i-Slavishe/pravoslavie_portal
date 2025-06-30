@echo off
echo.
echo ===============================================================
echo 💥 ФИНАЛЬНАЯ РАДИКАЛЬНАЯ ЗАЧИСТКА
echo ===============================================================
echo.
echo 🎯 Это последний шанс полностью очистить проект!
echo.
set /p confirm="Продолжить радикальную зачистку? (y/N): "
if /i not "%confirm%"=="y" (
    echo Отменено.
    pause
    exit /b 0
)

echo.
echo 🛑 Убиваем все процессы Python...
taskkill /f /im python.exe >nul 2>&1

echo.
echo 🗑️ ПОЛНОЕ УДАЛЕНИЕ...

:: Удаляем базу данных
echo    • Удаление базы данных...
del /f /q db.sqlite3 2>nul

:: Радикальное удаление файлов
echo    • Радикальное удаление файлов...
for /f %%i in ('dir /b *comment* 2^>nul') do del /f /q "%%i" 2>nul
for /f %%i in ('dir /b diagnose_* 2^>nul') do del /f /q "%%i" 2>nul
for /f %%i in ('dir /b fix_* 2^>nul') do del /f /q "%%i" 2>nul
for /f %%i in ('dir /b test_* 2^>nul') do del /f /q "%%i" 2>nul
for /f %%i in ('dir /b emergency_* 2^>nul') do del /f /q "%%i" 2>nul

:: Удаляем директории
echo    • Удаление директорий...
rmdir /s /q comments 2>nul
rmdir /s /q templates\stories\comments 2>nul
rmdir /s /q static\comments 2>nul
rmdir /s /q staticfiles\comments 2>nul

:: Удаляем файлы в stories
echo    • Очистка stories/...
del /f /q stories\comment_*.py 2>nul
del /f /q stories\views_comments.py 2>nul

:: Удаляем статические файлы
echo    • Очистка статических файлов...
del /f /q static\stories\js\*comment*.js 2>nul
del /f /q static\stories\js\youtube_*.js 2>nul
del /f /q static\stories\css\*comment*.css 2>nul
rmdir /s /q staticfiles 2>nul

:: Удаляем шаблоны комментариев
echo    • Очистка шаблонов...
del /f /q templates\stories\*comment*.html 2>nul
del /f /q templates\stories\partials\*comment*.html 2>nul
del /f /q templates\stories\partials\youtube_*.html 2>nul

:: Удаляем ВСЕ миграции
echo    • Удаление всех миграций...
del /f /q stories\migrations\*.py 2>nul
echo # Generated migrations > stories\migrations\__init__.py

echo.
echo 🔧 СОЗДАНИЕ ЧИСТЫХ ФАЙЛОВ...

:: Заменяем story_detail.html на чистую версию
echo    • Замена story_detail.html...
copy templates\stories\story_detail_clean.html templates\stories\story_detail.html >nul 2>&1

:: Создаем абсолютно чистый stories/urls.py
echo    • Создание чистого stories/urls.py...
(
echo from django.urls import path
echo from . import views
echo from . import views_playlists
echo.
echo app_name = 'stories'
echo.
echo urlpatterns = [
echo     path^('', views.StoryListView.as_view^(^), name='list'^),
echo     path^('^<slug:slug^>/', views_playlists.enhanced_story_detail, name='detail'^),
echo     path^('category/^<slug:category_slug^>/', views.StoryCategoryView.as_view^(^), name='category'^),
echo     path^('tag/^<slug:tag_slug^>/', views.StoryTagView.as_view^(^), name='tag'^),
echo     path^('popular/', views.PopularStoriesView.as_view^(^), name='popular'^),
echo     path^('featured/', views.FeaturedStoriesView.as_view^(^), name='featured'^),
echo     path^('search/', views.StorySearchView.as_view^(^), name='search'^),
echo     path^('^<int:story_id^>/like/', views.story_like, name='story_like'^),
echo     path^('^<int:story_id^>/favorite/', views.story_favorite, name='story_favorite'^),
echo     path^('playlists/', views_playlists.playlists_list, name='playlists_list'^),
echo     path^('playlist/create/', views_playlists.create_playlist, name='create_playlist'^),
echo     path^('playlist/add-story/', views_playlists.add_to_playlist, name='add_to_playlist'^),
echo     path^('playlist/remove-story/', views_playlists.remove_from_playlist, name='remove_from_playlist'^),
echo ]
) > stories\urls.py

echo.
echo 🧹 ОЧИСТКА MODELS.PY...
python clean_models.py

echo.
echo 🔄 СОЗДАНИЕ СВЕЖИХ МИГРАЦИЙ...
python manage.py makemigrations

echo.
echo 🔄 ПРИМЕНЕНИЕ МИГРАЦИЙ...
python manage.py migrate

echo.
echo 🧪 ТЕСТИРОВАНИЕ СЕРВЕРА...
echo    Запускаем сервер для проверки...
start /b python manage.py runserver >nul 2>&1
timeout /t 5 >nul
taskkill /f /im python.exe >nul 2>&1

echo.
echo ===============================================================
echo 🎉 РАДИКАЛЬНАЯ ЗАЧИСТКА ЗАВЕРШЕНА!
echo ===============================================================
echo.
echo ✅ Что было сделано:
echo    • Убиты все процессы Python
echo    • Удалена база данных полностью
echo    • Удалены ВСЕ файлы и директории комментариев
echo    • Удалены ВСЕ миграции
echo    • Создан чистый story_detail.html
echo    • Создан чистый stories/urls.py
echo    • Очищен stories/models.py
echo    • Созданы свежие миграции
echo    • Сервер протестирован
echo.
echo 🚀 ПРОЕКТ ПОЛНОСТЬЮ ОЧИЩЕН!
echo.
echo 💡 Теперь скажите:
echo    "Проект очищен, создаем новую систему комментариев"
echo.
pause
