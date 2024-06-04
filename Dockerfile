# Użyj obrazu bazowego Pythona
FROM python:3-slim

# Ustaw katalog roboczy na /app
WORKDIR /app

# Skopiuj plik requirements.txt do kontenera
COPY requirements.txt requirements.txt

# Zainstaluj zależności aplikacji
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę plików aplikacji do kontenera
COPY . .
COPY . /app/

# Otwórz port 5000, na którym działa aplikacja Flask
EXPOSE 5000

# Uruchom Gunicorn do obsługi aplikacji Flask
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]