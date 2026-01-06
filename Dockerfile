FROM python:3.11-slim

# Ustawienia Pythona
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Katalog roboczy
WORKDIR /app

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie requirements i instalacja pakietów Pythona
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie całego kodu
COPY . .

# Folder na static files
RUN mkdir -p /app/staticfiles

# Start kontenera – wszystko w jednej linii bez \
CMD ["sh", "-c", "echo '=== START CONTAINER ===' && pwd && ls -la && echo '=== RUNNING MIGRATIONS ===' && export DJANGO_SETTINGS_MODULE=kino_project.settings && python manage.py migrate --noinput && echo '=== MIGRATIONS DONE ===' && python manage.py collectstatic --noinput && echo '=== STARTING GUNICORN ===' && exec gunicorn kino_project.wsgi:application --bind 0.0.0.0:$PORT --workers 1"]
