import datetime
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

class LoginSchema(BaseModel):
    user_email: str
    user_password: str

class LoginRequest(BaseModel):
    user: LoginSchema

class AuthorizeUserSchema(BaseModel):
  user_id: str | None
  user_name: str | None
class AuthorizeUserSchemaWrapper(BaseModel):
  user: AuthorizeUserSchema

class LoginResponse(BaseModel):
    user: AuthorizeUserSchema
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


class PostPurchaseRequest(BaseModel):
    payment_method: str
    products: List[ProductSchema]
    expected_shipping_date: datetime.datetime


class PostPurchaseResponse(BaseModel):
    ordered_products: List[ProductSchema]
    order_completion_date: datetime.datetime
    expected_shipping_date: datetime.datetime
