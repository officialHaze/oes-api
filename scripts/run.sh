#!/bin/sh

set -e

until nc -z db 5432; do
    echo "Trying to establish connection with db..."
    sleep 1s & ${!}
done

echo "Connection established"

python manage.py wait_for_db
python manage.py collectstatic --no-input
python manage.py migrate

uwsgi --socket :8080 --workers 4 --master --enable-threads --module core.wsgi