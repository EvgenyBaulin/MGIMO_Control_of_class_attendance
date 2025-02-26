# Используем базовый образ Python
FROM python:3.10-slim

# Отключаем генерацию pyc-файлов и включаем "буферизацию" через stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаём рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем зависимости для psycopg2 и другие системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*


# Копируем requirements.txt
COPY backend/requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY backend/ /app/

# Пробрасываем порт
EXPOSE 8000
