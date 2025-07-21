from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Products(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String, index=True)
    category_id = Column(String, index=True)
    price = Column(Integer, index=True)
    description = Column(String, index=True)
    specs = Column(String, index=True)
