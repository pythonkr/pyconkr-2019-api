#!/bin/bash
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-pyconkr.staging_settings}

echo "Wait for starting database"
while !</dev/tcp/db/5432; do sleep 1; done; 
sleep 10

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py migrate


echo "Create admin user"
CREATE_ADMIN_SOURCE="
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

UserModel = get_user_model()

# Create admin user
USERNAME='pyconkr'
EMAIL='pyconkr@pycon.kr'
PASSWORD='${PYCONKR_ADMIN_PASSWORD}'

try:
    user = UserModel.objects.get(username=USERNAME)
    user.set_password(PASSWORD)
    user.save()
except UserModel.DoesNotExist:
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
"
echo "${CREATE_ADMIN_SOURCE}"  | python manage.py shell

echo "Starting server"
gunicorn pyconkr.wsgi:application --bind=0.0.0.0:8000
