#!/bin/bash
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-pyconkr.settings}

# echo "Wait for starting database"
# while !</dev/tcp/db/5432; do sleep 1; done;
# sleep 10

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
    UserModel.objects.get(username=USERNAME)
except UserModel.DoesNotExist:
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
"
echo "${CREATE_ADMIN_SOURCE}"  | python manage.py shell

echo "==== Starting cron ====="
python manage.py crontab show
python manage.py crontab add
python manage.py crontab show
service cron start

touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

echo "==== Starting server ====="
gunicorn pyconkr.wsgi:application \
    --bind=0.0.0.0:8000 \
    --workers 13 \
    --threads 512 \
    --worker-connections=5000 \
    --max-requests 10000 \
    --max-requests-jitter 5 \
    -k gevent \
    --log-level=info \
    --log-file=/srv/logs/gunicorn.log \
    --access-logfile=/srv/logs/access.log
