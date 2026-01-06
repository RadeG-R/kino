FROM python:3.11-slim

# Ustawienia Pythona
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Katalog roboczy
WORKDIR /app

# Instalacja zależności systemowych (libpq-dev i gcc potrzebne do psycopg2, gdybyś kiedyś przeszedł na Postgres)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie requirements i instalacja pakietów Pythona
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie całego kodu
COPY . .

# Utworzenie folderu na static (żeby nie było błędów)
RUN mkdir -p /app/staticfiles

# WAŻNE: Migracje i collectstatic przy starcie kontenera
# Używamy /tmp na bazę, bo jest writable
CMD python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    exec gunicorn kino_project.wsgi:application --bind 0.0.0.0:$PORT --workers 1
