import datetime
import uuid
import bcrypt
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.User import User
from app.schemas import AuthorizeUserSchema
from app.schemas import AuthorizeUserSchemaWrapper
class UserRepository:
  def __init__(self, db: AsyncSession) -> None:
    self.db = db

  async def register_user(self,user_name: str, user_email: str, user_password: str) -> str | None:
    if not user_name or not user_email or not user_password:
      raise ValueError('user_name or user_email or user_password is empty value')
    try:
      user_id = uuid.uuid4().hex
      created_at = datetime.datetime.now(datetime.timezone.utc)
      hashed_user_password = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt())

      user = User(user_id, user_name, user_email, hashed_user_password.decode(), created_at)
      self.db.add(user)

      await self.db.flush()

      return user_id
    except Exception as e:
      print(f"Can not register user, {e}")
      RuntimeError("Can not register user")

  async def authorize_user(self,user_email: str, user_password: str) -> tuple[bool, AuthorizeUserSchemaWrapper]:
    if not user_email or not user_password:
      raise ValueError('user_id or user_email or user_password is empty value')
    
    try:
      query = select(User).where(User.user_email == user_email) # type: ignore
      result = await self.db.execute(query)
      user = result.scalars().one_or_none()
      if not user:
        return False, AuthorizeUserSchemaWrapper(user=AuthorizeUserSchema(user_id=None, user_name=None))
      is_password = bcrypt.checkpw(user_password.encode(), user.user_password.encode())
      return is_password, AuthorizeUserSchemaWrapper(user=AuthorizeUserSchema(user_id=str(user.user_id), user_name=str(user.user_name)))
    except Exception as e:
      print(f"Can not authorize user, {e}")
      return False, AuthorizeUserSchemaWrapper(user=AuthorizeUserSchema(user_id=None, user_name=None))