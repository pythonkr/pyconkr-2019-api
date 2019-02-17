#!/bin/bash

echo "Apply database migrations"
python manage.py migrate
echo "Create admin user"
USERNAME = 'pyconkr'
EMAIL = 'pyconkr@pycon.kr'
PASSWORD = ${PYCONKR_ADMIN_PASSWORD}
echo "from django.contrib.auth.models import User; User.objects.create_superuser('${USERNAME}', '${EMAIL}', '${PASSWORD}')"  | python manage.py shell | true

echo "Starting server"
python manage.py runserver 0.0.0.0:8000
