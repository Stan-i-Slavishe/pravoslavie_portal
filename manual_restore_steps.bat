REM Step-by-step manual restoration

REM 1. Copy files
copy restored_views.py fairy_tales\views.py
copy restored_urls.py fairy_tales\urls.py

REM 2. Apply migrations
python manage.py makemigrations fairy_tales
python manage.py migrate

REM 3. Create test data
python create_fairy_tales_data.py

REM 4. Collect static (optional)
python manage.py collectstatic --noinput

REM 5. Start server
python manage.py runserver
