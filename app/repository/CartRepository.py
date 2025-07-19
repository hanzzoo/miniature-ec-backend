
import uuid
import datetime
from app.domain.Cart import Cart
from app.domain.Products import Products
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class CartRepository:
  def __init__(self, db: AsyncSession) -> None:
    self.db = db

  async def _validate_product_id(self, product_id: str) -> None:
    if not product_id:
      raise ValueError("Product ID cannot be empty")
    try:
      # Assuming Products is a valid SQLAlchemy model
      query = select(Products).where(Products.product_id == product_id)
      result = await self.db.execute(query)
      if not result.scalars().one_or_none():
        raise ValueError(f"Product with ID {product_id} does not exist")
    except Exception as e:
      print(f"Error occurred while validating product ID {product_id}: {e}")
      raise ValueError("Internal Server Error during product validation")
    
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

  # FIXME: CartItemRepositoryに移動する
  async def add_product_to_cart(self, product_id: str, user_id: str) -> None:
    if not product_id:
      raise ValueError("Product ID cannot be empty")
    try:
      await self._validate_product_id(product_id)

      #TODO: CartItemsを保存
      #TODO: 複数商品を追加する場合は、CartItemのquantityを加算する

    except ValueError as error:
      print(f"Validation error: {error}")
      raise error
    except Exception as e:
      print(f"Error occurred while adding product to cart: {e}")
      raise ValueError("Internal Server Error while adding product to cart")