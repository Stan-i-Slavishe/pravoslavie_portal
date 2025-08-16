@echo off
echo Pagination fix applied!
echo.
echo Testing pagination changes...
echo Open browser and check: http://127.0.0.1:8000/stories/?page=5
echo.
echo Expected behavior:
echo - Pages should show: 1 ... 3 4 [5] 6 7 ... 19
echo - Not: 1 ... 3 4 [5] 6 7 19 ...
echo.
pause
