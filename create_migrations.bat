#!/bin/bash
cd E:/pravoslavie_portal
python manage.py makemigrations books
python manage.py migrate books