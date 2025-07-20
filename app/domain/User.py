import datetime
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True, index=True)
    created_at = Column(String, default=datetime.datetime.now, index=True)

    def __init__(self, user_id: str, created_at: datetime.datetime):
        self.user_id = user_id
        self.created_at = created_at