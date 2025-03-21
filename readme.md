# Сваггер
Сваггер api:


```
http://localhost:8000/docs
```


# Запуск проекта для локальной разработки


1. При необходимости установить Poetry ```pip install poetry```

2. Запустить виртуальное окружение ```poetry shell```

3. Установить зависимости ```poetry install```

4. Добавьте файл .env и заполните его как в примере .example.env:

5. Запуск Minio```docker compose -f docker-compose.minio.yml up -d```

6. Запуск fastapi ```uvicorn --factory app.main:create_app --host localhost --port 8000```