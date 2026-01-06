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
