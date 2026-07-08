FROM python:3.11-slim

# Instalacja podstawowych narzędzi systemowych
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Kopiowanie i instalacja zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie reszty kodu aplikacji
COPY . .

# Flask domyślnie nasłuchuje na porcie 5000
EXPOSE 5000

# Użycie gunicorn z klasą workerów eventlet (wymagane dla Socket.io w Botinderze)
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "run:app"]