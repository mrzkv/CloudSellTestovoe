# Тестовое задание cloudsell.ru
---
## Инструкция по запуску проекта:  

### Подготовка окружения:
~~~
pip install uv
uv venv
source venv/bin/activate # On linux
source venv/Scripts/activate # On windows
uv sync --group tests
~~~


### Запуск с помощью docker-compose:
~~~
docker compose -f docker/docker-compose.redis.yaml up -d
docker compose -f docker/docker-compose.app.yaml up -d
~~~

### Запуск в prod режиме с помощью docker (Нужно вставить хост Redis в .env):
~~~
docker build -t myapp:prod -f docker/Dockerfile.prod .
docker run -d -p 8000:8000 --name myapp_prod myapp:prod
~~~
### Запуск в dev режиме с помощью docker (Нужно вставить хост Redis в .env):
~~~
docker build -t myapp:dev -f docker/Dockerfile.dev .
docker run -d -p 8000:8000 --name myapp_dev myapp:dev
~~~

### Запуск интеграционных тестов:
~~~
bash tests/run_integration_tests.sh # On linux
tests\run_integration_tests.bat # On windows
~~~

### Костыль для работы с Redis в тестах:  
Из-за условия использования BackgroundTasks в FastAPI, пришлось использовать синхронные методы для работы с Redis.

### Структура проекта:
~~~
.
├── app # Основное приложение
│   ├── api.py
│   ├── clients.py
│   ├── config.py
│   ├── __init__.py
│   ├── models.py
│   ├── storage.py
│   └── tasks.py
├── data # Данные эмулируемых провайдеров
│   ├── provider_a.json
│   └── provider_b.json
├── docker # Docker файлы и конфигурации
│   ├── docker-compose.app.yaml
│   ├── docker-compose.redis.yaml
│   ├── Dockerfile.dev
│   └── Dockerfile.prod
├── LICENSE
├── pyproject.toml
├── README.md
└── tests # Тесты
    ├── __init__.py
    ├── run_integration_tests.sh
    └── test_integration.py

~~~