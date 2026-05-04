FROM python:3.15.0a8-slim

RUN addgroup app && adduser -S -G app app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libaio1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER app

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]