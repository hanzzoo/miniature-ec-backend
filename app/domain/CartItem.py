from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CartItem(Base):
    __tablename__ = "cartItem"

    instance = Column(String, primary_key=True, index=True)
    product_id = Column(String, primary_key=True, index=True)
    quantity = Column(Integer, index=True)
    added_at = Column(String, index=True)
