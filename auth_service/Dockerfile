FROM python:3.11-slim
# Задаем рабочую директорию
WORKDIR /code
# Устанавливаем системные зависимости для сборки пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
# Копируем файлы конфигурации зависимостей
COPY pyproject.toml ./
# Устанавливаем менеджер пакетов pip и зависимости проекта
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Копируем исходный код приложения
COPY ./app ./app
# Открываем порты
EXPOSE 8000