FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Делаем скрипт исполняемым
RUN chmod +x entrypoint.sh

EXPOSE 8000

# Используем entrypoint.sh для запуска
ENTRYPOINT ["./entrypoint.sh"]
