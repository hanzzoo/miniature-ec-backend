from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
import os

from app.repository.ProductRepository import ProductRepository
from app.schemas import ProductResponse
# from app.schemas import ProductResponse as ProductsSchema

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://user:user_password@db:3306/my_database")
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI(title="Miniature EC Backend", version="1.0.0")


from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

@app.get("/")
async def root():
    return {"message": "Hello from miniature-ec-backend!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/products", tags=["products"])
async def get_all_products(db: AsyncSession = Depends(get_db)):
    async with db.begin():
        repo = ProductRepository(db)
        result = await repo.get_all_products()
        return [ProductResponse.model_validate(product) for product in result]
