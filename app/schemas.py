from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class UserSchema(BaseModel):
    user_name: str
    user_email: str
    user_password: str

class RegisterRequest(BaseModel):
    user: UserSchema

class RegisterResponse(BaseModel):
    user_id: str
    token: str
    expire: str

class ProductSchema(BaseModel):
    product_id: str
    name: Optional[str] = None
    category_id: Optional[str] = None
    price: Optional[str] = None
    description: Optional[str] = None
    specs: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class GetProductsResponse(BaseModel):
    products: List[ProductSchema]

class GetProductResponse(BaseModel):
    product: ProductSchema

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
    products: List[CartItemSchema]