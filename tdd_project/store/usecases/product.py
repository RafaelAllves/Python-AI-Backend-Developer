from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from store.db.mongo import db_client
from store.schemas.product import ProductIn, ProductOut


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product = await self.collection.insert_one(body.model_dump())
        return product

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        return ProductOut(**result)


product_usecase = ProductUsecase()
