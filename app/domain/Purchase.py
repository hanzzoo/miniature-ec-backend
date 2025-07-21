import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Purchase(Base):
    __tablename__ = "purchase"

    purchase_id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    purchased_at = Column(DateTime, default=datetime.datetime.now)