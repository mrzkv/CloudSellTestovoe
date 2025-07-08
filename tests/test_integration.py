import pytest
import httpx
import asyncio
from uuid import UUID

BASE_URL = "http://localhost:8000"



@pytest.mark.asyncio
async def test_get_pricing_plans():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/pricing-plans", params={"min_storage": 100})
        assert response.status_code == 200
        plans = response.json()
        assert isinstance(plans, list)
        assert len(plans) > 0
        for plan in plans:
            assert plan["storage_gb"] >= 100
            assert plan["price_per_gb"] > 0
            assert plan["provider"] in ["A", "B"]


@pytest.mark.asyncio
async def test_create_and_get_order():
    async with httpx.AsyncClient() as client:
        # Create order
        create_data = {
            "provider": "A",
            "storage_gb": 100
        }
        response1 = await client.post(f"{BASE_URL}/orders", json=create_data)
        assert response1.status_code == 200
        order = response1.json()
        assert "order_id" in order
        assert order["status"] == "pending"



@pytest.mark.asyncio
async def test_get_non_existent_order():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/orders/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_invalid_pricing_plan():
    async with httpx.AsyncClient() as client:
        create_data = {
            "provider": "A",
            "storage_gb": 142  # Non-existent plan size
        }
        response = await client.post(f"{BASE_URL}/orders", json=create_data)
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_negative_min_storage():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/pricing-plans", params={"min_storage": -100})
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_invalid_provider():
    async with httpx.AsyncClient() as client:
        create_data = {
            "provider": "C",  # Invalid provider
            "storage_gb": 100
        }
        response = await client.post(f"{BASE_URL}/orders", json=create_data)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_zero_storage():
    async with httpx.AsyncClient() as client:
        create_data = {
            "provider": "A",
            "storage_gb": 0  # Invalid storage size
        }
        response = await client.post(f"{BASE_URL}/orders", json=create_data)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_invalid_order_id_format():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/orders/not-a-uuid")
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_missing_required_fields():
    async with httpx.AsyncClient() as client:
        # Missing provider
        response = await client.post(f"{BASE_URL}/orders", json={"storage_gb": 100})
        assert response.status_code == 422

        # Missing storage_gb
        response = await client.post(f"{BASE_URL}/orders", json={"provider": "A"})
        assert response.status_code == 422

        # Empty body
        response = await client.post(f"{BASE_URL}/orders", json={})
        assert response.status_code == 422