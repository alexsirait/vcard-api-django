#!/bin/bash

PORT="40004"
HOST="192.168.88.60"
APP_NAME="vcard-api-django"

# Definisikan variabel
DJANGO_DIR="/var/lib/jenkins/workspace/$APP_NAME/mysatnusa"
VENV_DIR="/var/lib/jenkins/workspace/$APP_NAME/venv"
WORKERS=9  # Jumlah workers untuk 4 CPU Core
THREADS=2  # Jumlah thread per worker
MAX_REQUESTS=1000  # Batas permintaan per worker
MAX_REQUESTS_JITTER=100  # Jitter untuk permintaan
TIMEOUT=30  # Waktu timeout dalam detik

# Aktivasi virtual environment
source "$VENV_DIR/Scripts/activate"

# Jalankan server menggunakan gunicorn dalam daemon mode
exec gunicorn \
    --workers=$WORKERS \
    --threads=$THREADS \
    --max-requests=$MAX_REQUESTS \
    --max-requests-jitter=$MAX_REQUESTS_JITTER \
    --timeout=$TIMEOUT \
    --bind "$HOST:$PORT" \
    --chdir "$DJANGO_DIR" \
    mysatnusa.wsgi:application \
