import datetime

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = Column(String, primary_key=True, index=True)
    user_name = Column(String, index=True)
    user_email = Column(String, primary_key=True, index=True)
    user_password = Column(String, index=True)
    created_at = Column(String, default=datetime.datetime.now, index=True)

    def __init__(
        self,
        user_id: str,
        user_name: str,
        user_email: str,
        user_password: str,
        created_at: datetime.datetime,
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.user_password = user_password
        self.created_at = created_at
