
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.CartItem import CartItem
from app.domain.Cart import Cart
from app.domain.Products import Products

class CartItemRepository:
    def __init__(self, db: AsyncSession) -> None:
      self.db = db
    
    async def _validate_product_id(self, product_id: str) -> None:
      if not product_id:
        raise ValueError("Product ID cannot be empty")
      try:
        query = select(Products).where(Products.product_id == product_id)
        result = await self.db.execute(query)
        if not result.scalars().one_or_none():
          raise ValueError(f"Product with ID {product_id} does not exist")
      except Exception as e:
        print(f"Error occurred while validating product ID {product_id}: {e}")
        raise ValueError("Internal Server Error during product validation")
    
    async def _validate_cart_instance(self, instance: str):
        if not instance:
            raise ValueError("Cart instance ID cannot be empty")
        try:
            query = select(Cart).where(Cart.instance == instance)
            result = await self.db.execute(query)
            cart = result.scalars().one_or_none()
            if not cart:
                raise ValueError(f"Cart instance {instance} does not exist")
        except Exception as e:
            print(f"Error occurred while validating cart instance {instance}: {e}")
            raise ValueError("Internal Server Error during cart instance validation")


    async def update_product_to_cart(self, instance: str, product_id: str, quantity: int) -> None:
      try:
        await self._validate_product_id(product_id)
        await self._validate_cart_instance(instance)

        query = select(CartItem).where(
            CartItem.instance == instance,
            CartItem.product_id == product_id
        )
        result = await self.db.execute(query)
        cart_item = result.scalars().one_or_none()

        if quantity == 0:
            if cart_item:
                await self.db.delete(cart_item)
            return

        added_at = datetime.datetime.now(datetime.timezone.utc)
        if cart_item:
          setattr(cart_item, "quantity", quantity)
          setattr(cart_item, "added_at", added_at)
        else:
          cart_item = CartItem(
              instance=instance,
              product_id=product_id,
              quantity=quantity,
              added_at=added_at
          )
          self.db.add(cart_item)
        
        await self.db.flush()
      except Exception as e:
        print(f"Error occurred while adding product to cart: {e}")
        raise