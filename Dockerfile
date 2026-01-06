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

# Kopiowanie requirements i instalacja pakietów
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie całego kodu (w tym db.sqlite3)
COPY . .

# Folder na static files
RUN mkdir -p /app/staticfiles

# Collectstatic i start Gunicorna
CMD ["sh", "-c", "python manage.py collectstatic --noinput --clear && exec gunicorn kino_project.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120"]
