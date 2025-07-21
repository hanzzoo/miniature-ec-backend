import datetime
import uuid
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.User import User

class UserRepository:
  def __init__(self, db: AsyncSession) -> None:
    self.db = db

  async def register_user(self,user_name: str, user_email: str, user_password: str) -> str | None:
    if not user_name or not user_email or not user_password:
      raise ValueError('user_name or user_email or user_password is empty value')
    try:
      user_id = uuid.uuid4().hex
      created_at = datetime.datetime.now(datetime.timezone.utc)
      hashed_user_password = bcrypt.hashpw(user_email.encode(), bcrypt.gensalt())

      #TODO - 検証：# 検証時　bcrypt.checkpw(plain_password.encode(), hashed_from_db.encode())

      user = User(user_id, user_name, user_email, hashed_user_password.decode(), created_at)
      self.db.add(user)

      await self.db.flush()

      return user_id
    except Exception as e:
      print(f"Can not register user, {e}")
      RuntimeError("Can not register user")