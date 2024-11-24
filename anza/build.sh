#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

export DJANGO_COLLECTSTATIC=1
python manage.py collectstatic --noinput

python manage.py migrate