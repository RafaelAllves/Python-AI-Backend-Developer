from httpx import AsyncClient
import pytest
import asyncio
from uuid import UUID
from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductUpdate
from tests.factories import product_data, products_data
from store.usecases.product import product_usecase


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mongo_client():
    return db_client.get()


@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    yield
    collection_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collection_names:
        if collection_name.startswith("system"):
            continue

        await mongo_client.get_database()[collection_name].delete_many({})


@pytest.fixture
def product_in():
    return ProductIn(**product_data(), id=product_id)


@pytest.fixture
def product_id() -> UUID:
    return UUID("6efbed42-d78e-4dc4-a4d1-725316279401")


@pytest.fixture
async def product_inserted(product_in):
    return await product_usecase.create(body=product_in)


@pytest.fixture
def products_in():
    return [ProductIn(**product) for product in products_data()]


@pytest.fixture
async def products_inserted(products_in):
    return [await product_usecase.create(body=product_in) for product_in in products_in]


@pytest.fixture
def product_up(product_id):
    return ProductUpdate(**product_data(), id=product_id)


@pytest.fixture
def client() -> AsyncClient:
    from store.main import app

    return AsyncClient(app=app, base_url="http://test")


@pytest.fixture
def products_url() -> str:
    return "/products/"
