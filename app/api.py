from fastapi import FastAPI, BackgroundTasks, Query, HTTPException
from app.models import PricingPlan, OrderResponse, OrderCreate, Provider
from app.clients import ProviderClientA, ProviderClientB
from app.tasks import process_order
from app.storage import order_storage
from typing import Annotated
import asyncio
from uuid import UUID

app = FastAPI(
    title="API сравнения цен облачного хранилища",
    description="API для сравнения тарифных планов облачного хранилища от разных провайдеров.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Тарифные планы",
            "description": "Эндпоинты для получения и сравнения тарифных планов от разных провайдеров."
        }
    ]
)


@app.get(
    path="/pricing-plans",
    summary="Получить доступные тарифные планы",
    description="Эндпоинт для получения доступных тарифных планов от разных провайдеров с фильтрацией по минимальному объему хранилища.",
    tags=["Тарифные планы"]
)
async def get_pricing_plans(
        min_storage: Annotated[int, Query(gt=0, description="Минимальный объем хранилища в ГБ")]
) -> list[PricingPlan]:
    plans_a, plans_b = await asyncio.gather( # Gather для параллельного выполнения запросов к провайдерам
        ProviderClientA.get_plans(min_storage=min_storage), # Получаем планы от провайдера A
        ProviderClientB.get_plans(min_storage=min_storage) # Получаем планы от провайдера B
    )
    plans: list[PricingPlan] = plans_a + plans_b # Собираем все планы от обоих провайдеров
    return sorted(plans, key=lambda x: x.total_price) # Сортируем по цене за хранилище


@app.post(
    path="/orders",
    summary="Создать новый заказ",
    description="Создание нового заказа с фоновой обработкой.",
    tags=["Тарифные планы"]
)
async def create_order(
        order_data: OrderCreate,
        background_tasks: BackgroundTasks,
) -> OrderResponse:
    # Получаем клиент провайдера
    provider_client = {
        Provider.A: ProviderClientA,
        Provider.B: ProviderClientB
    }.get(order_data.provider)

    # Проверяем существование тарифного плана
    plans = await provider_client.get_plans(min_storage=order_data.storage_gb)

    if not any(p.storage_gb == order_data.storage_gb for p in plans):
        raise HTTPException(
            status_code=400,
            detail=f"Pricing plan not found for {order_data.storage_gb}GB at provider {order_data.provider}"
        )

    # Создаем заказ, если тарифный план найден
    order: OrderResponse = await order_storage.create_order(order_data.provider, order_data.storage_gb)
    background_tasks.add_task(process_order, order.order_id)
    return order

@app.get(
    path="/orders/{order_id}",
    summary="Получить статус заказа",
    description="Получение статуса существующего заказа по его ID.",
    tags=["Тарифные планы"],
)
async def get_order_status(
        order_id: UUID
) -> OrderResponse | None:
    order: OrderResponse = await order_storage.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="not_found")
    return order