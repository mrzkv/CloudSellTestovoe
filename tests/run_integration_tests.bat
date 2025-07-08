@echo off

:: Start the services with test environment
docker compose -f docker/docker-compose.redis.yaml up -d
docker compose -f docker/docker-compose.app.yaml up -d

echo Waiting for services to start...
timeout /t 5 /nobreak >nul

:: Run the tests
pytest tests/test_integration.py -v

:: Clean up
docker compose -f docker/docker-compose.app.yaml down
docker compose -f docker/docker-compose.redis.yaml down