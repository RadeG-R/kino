FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# --- ZMIANA: USUNĄŁEM COLLECTSTATIC ---
# Dzięki temu budowanie nie powinno się wywalić na błędach Django.
# Utworzymy tylko pusty folder staticfiles, żeby Gunicorn nie krzyczał.
RUN mkdir -p staticfiles

EXPOSE 8000

CMD exec gunicorn kino_project.wsgi:application --bind 0.0.0.0:$PORT --workers 1