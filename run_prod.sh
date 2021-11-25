#!/bin/bash
python manage.py collectstatic --noinput &&
python manage.py migrate --noinput &&
gunicorn arttherapy.wsgi --worker-tmp-dir /dev/shm --workers=2 --threads=4 --bind 0.0.0.0:8000 