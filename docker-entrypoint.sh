#!/bin/bash

# echo "Collect static files"
# python manage.py collectstatic --noinput
echo "Apply database migrations"
python manage.py migrate
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
