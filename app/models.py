from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from enum import Enum

class Provider(str, Enum):
    A = "A"
    B = "B"

class PricingPlan(BaseModel):
    provider: Provider
    storage_gb: int = Field(gt=0, description="Объем хранилища в GB")
    price_per_gb: float = Field(gt=0, description="Цена за GB в месяц")

    @property
    def total_price(self) -> float:
        return self.storage_gb * self.price_per_gb


class OrderCreate(BaseModel):
    provider: Provider
    storage_gb: int = Field(gt=0, description="Объем хранилища в GB")

class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETE = "complete"

class OrderResponse(BaseModel):
    order_id: UUID
    status: OrderStatus