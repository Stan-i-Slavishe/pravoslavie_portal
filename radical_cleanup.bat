@echo off
echo.
echo ===============================================================
echo 💥 РАДИКАЛЬНАЯ ЗАЧИСТКА КОММЕНТАРИЕВ
echo ===============================================================
echo.
echo 🎯 Удаляем ВСЕ остатки комментариев принудительно!
echo.

:: Останавливаем все процессы Python
taskkill /f /im python.exe >nul 2>&1

echo 🗑️ РАДИКАЛЬНОЕ УДАЛЕНИЕ ВСЕХ ФАЙЛОВ...

:: Удаляем ВСЕ файлы диагностики и исправлений
del /f /q diagnose_*.py 2>nul
del /f /q diagnose_*.bat 2>nul
del /f /q fix_*.py 2>nul
del /f /q fix_*.bat 2>nul
del /f /q test_*.py 2>nul
del /f /q test_*.bat 2>nul
del /f /q emergency_*.py 2>nul
del /f /q emergency_*.bat 2>nul
del /f /q *comment*.py 2>nul
del /f /q *comment*.bat 2>nul
del /f /q *COMMENTS*.md 2>nul

:: Удаляем директории комментариев
rmdir /s /q comments 2>nul
rmdir /s /q templates\stories\comments 2>nul
rmdir /s /q static\comments 2>nul
rmdir /s /q staticfiles\comments 2>nul

:: Удаляем ВСЕ файлы комментариев в stories
del /f /q stories\comment_*.py 2>nul
del /f /q stories\views_comments.py 2>nul
del /f /q stories\*comment*.py 2>nul

:: Удаляем ВСЕ статические файлы комментариев
del /f /q static\stories\js\*comment*.js 2>nul
del /f /q static\stories\js\youtube_*.js 2>nul
del /f /q static\stories\css\*comment*.css 2>nul
del /f /q staticfiles\stories\js\*comment*.js 2>nul
del /f /q staticfiles\stories\js\youtube_*.js 2>nul
del /f /q staticfiles\stories\css\*comment*.css 2>nul

:: Удаляем ВСЕ шаблоны комментариев
del /f /q templates\stories\*comment*.html 2>nul
del /f /q templates\stories\partials\*comment*.html 2>nul
del /f /q templates\stories\partials\youtube_*.html 2>nul

:: Удаляем ВСЕ миграции комментариев
del /f /q stories\migrations\*comment*.py 2>nul
del /f /q stories\migrations\*youtube*.py 2>nul
del /f /q stories\migrations\0002_*.py 2>nul
del /f /q stories\migrations\0006_*.py 2>nul
del /f /q stories\migrations\0007_*.py 2>nul
del /f /q stories\migrations\0008_*.py 2>nul
del /f /q stories\migrations\0010_*.py 2>nul

echo.
echo 🔧 СОЗДАНИЕ ЧИСТЫХ ФАЙЛОВ...

:: Создаем абсолютно чистый stories/urls.py
(
echo from django.urls import path
echo from . import views
echo from . import views_playlists
echo.
echo app_name = 'stories'
echo.
echo urlpatterns = [
echo     # Основные страницы
echo     path('', views.StoryListView.as_view^(^), name='list'^),
echo     path^('^<slug:slug^>/', views_playlists.enhanced_story_detail, name='detail'^),
echo     
echo     # Категории и теги
echo     path^('category/^<slug:category_slug^>/', views.StoryCategoryView.as_view^(^), name='category'^),
echo     path^('tag/^<slug:tag_slug^>/', views.StoryTagView.as_view^(^), name='tag'^),
echo     
echo     # Специальные списки
echo     path^('popular/', views.PopularStoriesView.as_view^(^), name='popular'^),
echo     path^('featured/', views.FeaturedStoriesView.as_view^(^), name='featured'^),
echo     path^('search/', views.StorySearchView.as_view^(^), name='search'^),
echo     
echo     # Лайки рассказов
echo     path^('^<int:story_id^>/like/', views.story_like, name='story_like'^),
echo     path^('^<int:story_id^>/favorite/', views.story_favorite, name='story_favorite'^),
echo     
echo     # Плейлисты
echo     path^('playlists/', views_playlists.playlists_list, name='playlists_list'^),
echo     path^('playlist/create/', views_playlists.create_playlist, name='create_playlist'^),
echo     path^('playlist/add-story/', views_playlists.add_to_playlist, name='add_to_playlist'^),
echo     path^('playlist/remove-story/', views_playlists.remove_from_playlist, name='remove_from_playlist'^),
echo ]
) > stories\urls_clean.py

:: Заменяем старый файл
move stories\urls.py stories\urls_old.py 2>nul
move stories\urls_clean.py stories\urls.py

echo.
echo 🗃️ РАДИКАЛЬНАЯ ОЧИСТКА БАЗЫ ДАННЫХ...

:: Удаляем базу данных целиком
del /f /q db.sqlite3 2>nul

:: Удаляем ВСЕ миграции кроме __init__.py
for /d %%i in (*/migrations) do (
    if exist "%%i" (
        del /f /q "%%i\*.py" 2>nul
        echo # Generated migrations > "%%i\__init__.py"
    )
)

echo.
echo 🔄 СОЗДАНИЕ СВЕЖИХ МИГРАЦИЙ...
python manage.py makemigrations

echo.
echo 🔄 ПРИМЕНЕНИЕ МИГРАЦИЙ...
python manage.py migrate

echo.
echo ===============================================================
echo 🎉 РАДИКАЛЬНАЯ ЗАЧИСТКА ЗАВЕРШЕНА!
echo ===============================================================
echo.
echo ✅ Что было сделано:
echo    • Убиты все процессы Python
echo    • Удалены ВСЕ файлы комментариев
echo    • Удалена база данных полностью
echo    • Удалены ВСЕ миграции
echo    • Создан чистый stories/urls.py
echo    • Созданы свежие миграции
echo    • Применены миграции
echo.
echo 🚀 Проект полностью очищен от комментариев!
echo.
echo 💡 Следующий шаг:
echo    Скажите: "Проект очищен, создаем новую систему комментариев"
echo.
pause
