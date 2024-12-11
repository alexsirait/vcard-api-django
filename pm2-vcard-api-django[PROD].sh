#!/bin/bash
source /var/www/cargo-lift-api-django/venv/Scripts/activate
exec python3 /var/www/cargo-lift-api-django/mysatnusa/manage.py runserver 192.168.88.62:40002
