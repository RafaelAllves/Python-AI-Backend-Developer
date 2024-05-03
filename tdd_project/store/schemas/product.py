from decimal import Decimal
from pydantic import Field
from store.schemas.base import BaseSchemaMixin, OutSchema
from bson import Decimal128
from typing import Annotated
from pydantic import AfterValidator


class ProductBase(BaseSchemaMixin):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: Decimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase, BaseSchemaMixin):
    pass


class ProductOut(ProductIn, OutSchema):
    pass


def convert_decimal_128(v):
    return Decimal128(str(v))


Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]
