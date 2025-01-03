# Dockerfile

FROM python:3.12-slim

WORKDIR /app
COPY . /app

# Installa dipendenze
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
