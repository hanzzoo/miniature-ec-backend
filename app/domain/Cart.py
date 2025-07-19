import datetime
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Cart(Base):
    __tablename__ = "cart"

    instance = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    created_at = Column(String, default=datetime.datetime.now, index=True)