
import uuid
import datetime
from app.domain.Cart import Cart
from sqlalchemy.ext.asyncio import AsyncSession

class CartRepository:
  def __init__(self, db: AsyncSession) -> None:
    self.db = db
    
  async def create_cart(self, user_id: str) -> str:
    #TODO: user_idからカートのインスタンスを検索し既存のCartがあれば、そちらに保存
    # (user_idはログインユーザーであれば、DB / 未ログインユーザーであればセッションIDとなる)
    #TODO: ログインユーザーであれば、UserRepositoryにバリデーションメソッドを追加し、そちらで判定処理
    try:
      instance = uuid.uuid4().hex
      created_at = datetime.datetime.now(datetime.timezone.utc)
      cart = Cart(instance=instance, user_id=user_id, created_at=created_at)
      self.db.add(cart)

      await self.db.flush()

      return instance
    except Exception as e:
       print(f"Error occurred while adding product to cart: {e}")
       raise RuntimeError("Internal Server Error while creating cart")