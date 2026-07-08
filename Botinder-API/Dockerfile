FROM python:3.11-slim

WORKDIR /app

# Kopiowanie i instalacja zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu
COPY . .

# FastAPI nasłuchuje na porcie 8000
EXPOSE 8000

# Uruchomienie aplikacji za pomocą uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]