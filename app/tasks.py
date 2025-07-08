import time

from app.storage import order_storage
from app.models import OrderStatus
from uuid import UUID


def process_order(order_id: UUID) -> None:
    time.sleep(1) # Имитация длительной обработки заказа
    order_storage.update_status(order_id, OrderStatus.COMPLETE)
