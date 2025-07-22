import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Purchase(Base):
    __tablename__ = "purchase"

    purchase_id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    total_amount = Column(Integer, index=True)
    purchased_at = Column(DateTime, default=datetime.datetime.now)

    def __init__(
        self,
        purchase_id: str,
        user_id: str,
        total_amount: int,
        purchased_at: datetime.datetime,
    ):
        self.purchase_id = purchase_id
        self.user_id = user_id
        self.total_amount = total_amount
        self.purchased_at = purchased_at
