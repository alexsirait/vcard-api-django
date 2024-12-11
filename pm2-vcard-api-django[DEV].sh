#!/bin/bash
source /var/lib/jenkins/workspace/cargo-lift-api-django/venv/Scripts/activate
exec python3 /var/lib/jenkins/workspace/cargo-lift-api-django/mysatnusa/manage.py runserver 192.168.88.60:40002
