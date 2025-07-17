@echo off
call .venv\Scripts\activate
echo Starting HTTP server at http://127.0.0.1:8000/
python manage.py runserver
