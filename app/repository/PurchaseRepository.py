import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.Purchase import Purchase

class PurchaseRepository:
    def __init__(self, db: AsyncSession) -> None:
       self.db = db
    
    async def order(self, user_id: str) -> str:
       purchase_id = uuid.uuid4().hex
       purchased_at = datetime.datetime.now(datetime.timezone.utc)

       purchase = Purchase(purchase_id=purchase_id, user_id=user_id, purchased_at=purchased_at)
       self.db.add(purchase)
       
       await self.db.flush()
       return purchase_id