from pydantic import BaseModel
from typing import Optional


class ProductResponse(BaseModel):
    product_id: str
    name: Optional[str] = None
    category_id: Optional[str] = None
    price: Optional[str] = None
    description: Optional[str] = None
    specs: Optional[str] = None

    class Config:
        from_attributes = True
