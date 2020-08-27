#!/bin/sh
python manage.py migrate
gunicorn api.wsgi:application --bind 0.0.0.0:8000