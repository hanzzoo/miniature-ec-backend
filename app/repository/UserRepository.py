import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.User import User

class UserRepository:
  def __init__(self, db: AsyncSession) -> None:
    self.db = db

  async def register_user(self) -> str | None:
    try:
      user_id = uuid.uuid4().hex
      created_at = datetime.datetime.now(datetime.timezone.utc)

      user = User(user_id, created_at)
      self.db.add(user)

      await self.db.flush()

      return user_id
    except Exception as e:
      print(f"Can not register user, {e}")
      RuntimeError("Can not register user")