from typing import List
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
async def test_controller_create_should_return_error(client, products_url):
    invalid_product_data = {
        "name": "",
        "quantity": -1,
        "price": "invalid",
        "status": "not a boolean",
    }

    response = await client.post(products_url, json=invalid_product_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


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


@pytest.mark.asyncio
@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


@pytest.mark.asyncio
async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    product = await product_inserted
    response = await client.patch(
        f"{products_url}{product.id}", json={"price": "7.500"}
    )

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product.id),
        "name": "Iphone 14 Pro Max",
        "quantity": 10,
        "price": "7.500",
        "status": True,
    }


@pytest.mark.asyncio
async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    product = await product_inserted
    response = await client.delete(f"{products_url}{product.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.delete(
        f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }
