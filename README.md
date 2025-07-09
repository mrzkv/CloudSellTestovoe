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


### Примеры запросов:
**Получаение плана тарифов:**
![Примеры запросов](https://github.com/mrzkv/CloudSellTestovoe/blob/main/docs/pricing_plan200.png?raw=true)
**Получение пустого плана тарифов из-за слишком высокого кол-ва гигабайт:**
![Примеры запросов](https://github.com/mrzkv/CloudSellTestovoe/blob/main/docs/pricing_plan200empty.png?raw=true)
**Получение плана тарифов с ошибкой 422 из-за некорректного формата запроса:**
![Примеры запросов](https://github.com/mrzkv/CloudSellTestovoe/blob/main/docs/pricing_plan422.png?raw=true)

**Не найденный план у провайдера:**
![Примеры запросов](https://github.com/mrzkv/CloudSellTestovoe/blob/main/docs/create_order400.png?raw=true)
**Корректный запрос на создание заказа:**
![Примеры запросов](https://github.com/mrzkv/CloudSellTestovoe/blob/main/docs/create_order200.png?raw=true)

**Корректный запрос на получение заказа:**
![Примеры запросов](https://github.com/mrzkv/CloudSellTestovoe/blob/main/docs/get_order200.png?raw=true)
**Через 1 минуту получение созданного заказа:**
![Примеры запросов](https://github.com/mrzkv/CloudSellTestovoe/blob/main/docs/get_order200complete.png?raw=true)
**404 при неверном UUID заказа:**
![Примеры запросов](https://github.com/mrzkv/CloudSellTestovoe/blob/main/docs/get_order404.png?raw=true)

### Содержимое JSON файлов провайдеров:
~~~json
[
    {
        "provider": "A",
        "storage_gb": 25,
        "price_per_gb": 0.03
    },
    {
        "provider": "A",
        "storage_gb": 100,
        "price_per_gb": 0.025
    },
    {
        "provider": "A",
        "storage_gb": 200,
        "price_per_gb": 0.02
    },
    {
        "provider": "A",
        "storage_gb": 500,
        "price_per_gb": 0.015
    },
    {
        "provider": "A",
        "storage_gb": 1000,
        "price_per_gb": 0.012
    }
]
~~~
~~~json
[
    {
        "provider": "B",
        "storage_gb": 100,
        "price_per_gb": 0.02
    },
    {
        "provider": "B",
        "storage_gb": 200,
        "price_per_gb": 0.017
    },
    {
        "provider": "B",
        "storage_gb": 300,
        "price_per_gb": 0.014
    },
    {
        "provider": "B",
        "storage_gb": 500,
        "price_per_gb": 0.012
    },
    {
        "provider": "B",
        "storage_gb": 1000,
        "price_per_gb": 0.01
    }
]
~~~