import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.Cart import Cart


class CartRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_instance(self, user_id: str) -> str | None:
        try:
            query = select(Cart).where(Cart.user_id == user_id)
            result = await self.db.execute(query)
            cart = result.scalars().one_or_none()
            if cart:
                return str(cart.instance)
            else:
                return None
        except Exception as e:
            raise ValueError(f"not found cart instance, {e}")

    async def create_cart(self, user_id: str) -> str:
        try:
            has_created_instance = await self.get_instance(user_id)

            if has_created_instance:
                return has_created_instance
            instance = uuid.uuid4().hex
            created_at = datetime.datetime.now(datetime.timezone.utc)
            cart = Cart(instance=instance, user_id=user_id, created_at=created_at)
            self.db.add(cart)

            await self.db.flush()

            return instance
        except Exception as e:
            print(f"Error occurred while adding product to cart: {e}")
            raise RuntimeError("Internal Server Error while creating cart")
