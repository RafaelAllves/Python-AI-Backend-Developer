import pytest
from store.schemas.product import ProductOut
from store.usecases.product import product_usecase


@pytest.mark.asyncio
async def test_usecases_create_should_return_success(product_in):
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"


@pytest.mark.asyncio
async def test_usecases_get_should_return_success(product_inserted):
    product = await product_inserted
    result = await product_usecase.get(id=product.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 Pro Max"
