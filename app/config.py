# Можно использовать pydantic для валидации, но с датаклассами будет быстрее и проще для конфигурации.
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

@dataclass(frozen=True)
class RedisConfig:
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: int = int(os.getenv("REDIS_PORT", "6379"))
    password: str | None = os.getenv("REDIS_PASSWORD")
    db: int = int(os.getenv("REDIS_DB", "0"))
    ssl: bool = os.getenv("REDIS_SSL", "false").lower() == "true"
    @property
    def url(self) -> str:
        """Генерирует URL для подключения к Redis"""
        return f"redis://{self.host}:{self.port}/{self.db}" + (f"?ssl={self.ssl}" if self.ssl else "")

@dataclass(frozen=True)
class AppConfig:
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

@dataclass(frozen=True)
class ProviderConfig:
    provider_a_data_file: str = os.getenv("PROVIDER_A_DATA_FILE", "data/provider_a.json")
    provider_b_data_file: str = os.getenv("PROVIDER_B_DATA_FILE", "data/provider_b.json")

@dataclass(frozen=True)
class Config:
    redis: RedisConfig = RedisConfig()
    app: AppConfig = AppConfig()
    providers: ProviderConfig = ProviderConfig()


# Глобальный экземпляр конфига
config = Config()