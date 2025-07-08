import orjson
from uuid import uuid4, UUID
from app.models import OrderStatus, OrderResponse
from redis.asyncio import Redis as AsyncRedis
from redis import Redis as SyncRedis
from app.config import config

class OrderStorage:
    def __init__(
            self,
            redis_url: str,
            async_redis: AsyncRedis = None,
            sync_redis: SyncRedis = None
    ) -> None:
        self._redis = async_redis or AsyncRedis.from_url(redis_url)
        self._sync_redis = sync_redis or SyncRedis.from_url(redis_url)
        self._key_prefix = "order:"

    def _get_key(self, order_id: UUID) -> str:
        """Генерирует ключ для хранения заказа в Redis"""
        return f"{self._key_prefix}{str(order_id)}"

    async def create_order(
            self,
            provider: str,
            storage_gb: int
    ) -> OrderResponse:
        """Создает новый заказ и сохраняет в Redis"""
        order = OrderResponse(
            order_id=uuid4(),
            status=OrderStatus.PENDING
        )
        key = self._get_key(order.order_id) # Генерация ключа
        await self._redis.set( # Сохранение заказа в Redis
            key,
            orjson.dumps({
                "order_id": str(order.order_id),
                "provider": provider,
                "storage_gb": storage_gb,
                "status": order.status.value
            }),
            ex=86400  # Срок хранения 1 день
        )
        return order

    async def get_order(
            self,
            order_id: UUID
    ) -> OrderResponse | None:
        """Получение заказа по ID из Redis"""

        key = self._get_key(order_id) # Генерация ключа
        data = await self._redis.get(key) # Получение данных по ключу

        if not data: # Проверка на существование заказа
            return None

        order_data = orjson.loads(data) # Десериализация данных заказа
        return OrderResponse(**order_data) # Распаковка в модель OrderResponse

    def update_status(
            self,
            order_id: UUID,
            status: OrderStatus
    ) -> None:
        """
        Обновляет статус заказа в Redis
        :raise ValueError: если заказ не найден
        :return None: если статус успешно обновлен
        """

        key = self._get_key(order_id) # Генерация ключа
        order_data = self._sync_redis.get(key) # Получение данных по ключу

        if not order_data: # Проверка на существование заказа
            raise ValueError(f"Order with ID {order_id} does not exist.")

        data = orjson.loads(order_data)
        data["status"] = status.value # Обновление статуса заказа
        self._sync_redis.set(key, orjson.dumps(data)) # Сохранение обновленных данных в Redis

# Создание экземпляра OrderStorage для использования в приложении
order_storage = OrderStorage(
    redis_url=config.redis.url,
)
