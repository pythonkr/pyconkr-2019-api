#!/bin/bash

echo "Collect static files"
python manage.py collectstatic --noinput

sleep 15
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
except UserModel.DoesNotExist:
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
"
echo "${CREATE_ADMIN_SOURCE}"  | python manage.py shell

echo "Starting server"
python manage.py runserver 0.0.0.0:8000