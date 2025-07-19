
from app.domain.Products import Products
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all_products(self):
        query = select(Products)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_product_by_id(self, product_id: str) -> Products | None:
        query = select(Products).where(Products.product_id == product_id)
        result = await self.db.execute(query)
        return result.scalars().one_or_none()