@echo off
chcp 65001 >nul
call .venv\Scripts\activate

echo HTTPS Django Server
echo ===================
echo.

REM Проверяем есть ли pyOpenSSL
python -c "import OpenSSL" 2>nul
if %ERRORLEVEL% neq 0 (
    echo Installing pyOpenSSL...
    pip install pyOpenSSL --quiet
)

echo Starting HTTPS server at https://127.0.0.1:8000/
echo Browser will show security warning - click "Advanced" then "Proceed"
echo.

python manage.py runserver_plus --cert-file ssl/cert.pem --key-file ssl/key.pem
