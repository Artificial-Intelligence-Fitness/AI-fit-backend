# Базовый образ Python
FROM python:3.9-slim

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Сборка статических файлов
RUN python manage.py collectstatic --noinput

# Команда для запуска сервера
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]