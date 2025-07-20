import datetime
import uuid
# from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.User import User

class UserRepository:
  def __init__(self, db: AsyncSession) -> None:
    self.db = db
    self.user_id = ''

  async def register_user(self) -> str | None:
    try:
      user_id = uuid.uuid4().hex
      created_at = datetime.datetime.now(datetime.timezone.utc)
      token = 'test_token'

      user = User(user_id, created_at, token)
      self.db.add(user)

      await self.db.flush()

      self.user_id = user_id
      return user_id
    except Exception as e:
      print(f"Can not register user, {e}")
      RuntimeError("Can not register user")