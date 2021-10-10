#!/bin/bash
python manage.py collectstatic --noinput &&
python manage.py migrate --noinput &&
gunicorn arttherapy.wsgi --bind 0.0.0.0:8000