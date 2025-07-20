from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class UserInfo(Base):
    __tablename__ = "userInfo"

    user_id = Column(String, primary_key=True, index=True)
    user_name = Column(String)
    user_email = Column(String, unique=True, index=True)