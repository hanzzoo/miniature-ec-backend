from pydantic import BaseModel, ConfigDict
from typing import Any, List, Optional


class ProductResponse(BaseModel):
    product_id: str
    name: Optional[str] = None
    category_id: Optional[str] = None
    price: Optional[str] = None
    description: Optional[str] = None
    specs: Optional[str] = None

    class Config:
        from_attributes = True

class CartProductRequest(BaseModel):
    product_id: str
    quantity: int

class UpdateToCartRequest(BaseModel):
    products: List[CartProductRequest]

class CartItemSchema(BaseModel):
    product_id: str
    quantity: int
    added_at: str

    model_config = ConfigDict(from_attributes=True)

class GetCartItemResponse(BaseModel):
    products: List[CartItemSchema] |  List[Any]