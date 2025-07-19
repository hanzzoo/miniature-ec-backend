
from app.domain.Products import Products
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class ProductRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    async def get_all_products(self) -> list[Products]:
      try:
        query = select(Products)
        result = await self.db.execute(query)
        return list(result.scalars().all())
      except Exception as e:
        print(f"Error occurred while fetching all products: {e}")
        return []

    async def get_product_by_id(self, product_id: str) -> Products | None:
      try:
        query = select(Products).where(Products.product_id == product_id)
        result = await self.db.execute(query)
        return result.scalars().one_or_none()
      except Exception as e:
        print(f"Error occurred while fetching product by ID {product_id}: {e}")
        return None