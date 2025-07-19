from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
import os

from app.repository.ProductRepository import ProductRepository
from app.schemas import ProductResponse

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://user:user_password@db:3306/my_database?charset=utf8mb4")
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

@app.get("/products", tags=["products"], response_model=list[ProductResponse])
async def get_all_products(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    async with db.begin():
        repo = ProductRepository(db)
        result = await repo.get_all_products()
        json_data = [ProductResponse.model_validate(product).model_dump() for product in result]
        return JSONResponse(
            content={ "products": json_data },
            media_type="application/json; charset=utf-8"
        )
