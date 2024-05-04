import pytest
from tests.factories import product_data
from fastapi import status


@pytest.mark.asyncio
async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()

    del content["created_at"]
    del content["updated_at"]
    del content["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


@pytest.mark.asyncio
async def test_controller_get_should_return_success(
    client, products_url, product_inserted
):
    product = await product_inserted
    response = await client.get(f"{products_url}{product.id}")

    content = response.json()

    del content["created_at"]
    del content["updated_at"]
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product.id),
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


@pytest.mark.asyncio
async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }
