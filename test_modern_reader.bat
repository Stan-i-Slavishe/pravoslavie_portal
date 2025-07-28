@echo off
echo ========================================
echo      TESTING MODERN READER
echo ========================================
echo.
echo Starting Django development server...
echo Open: http://127.0.0.1:8000/books/book/yandeks-direkt/
echo.
echo Modern Reader features:
echo - Fullscreen reading
echo - Swipe navigation (mobile)
echo - Touch controls show/hide
echo - Progress tracking
echo - Screen rotation
echo.
call .venv\Scripts\activate
python manage.py runserver
