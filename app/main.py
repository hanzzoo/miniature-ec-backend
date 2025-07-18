from fastapi import FastAPI, Depends, HTTPException
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

@app.get("/products", tags=["products"], response_model=dict[str, list[ProductResponse]])
async def get_all_products(db: AsyncSession = Depends(get_db)) -> dict[str, list[ProductResponse]]:
    try:
        async with db.begin():
            repo = ProductRepository(db)
            result = await repo.get_all_products()
            json_data = [ProductResponse.model_validate(product) for product in result]
            return {"products": json_data}
    except Exception as e:
        print(f"Error occurred while fetching all products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/products/{product_id}", tags=["products_detail"], response_model=dict[str, ProductResponse])
async def get_product_by_id(product_id: str, db: AsyncSession = Depends(get_db)) -> dict[str, ProductResponse]:
    try:
        async with db.begin():
            repo = ProductRepository(db)
            product = await repo.get_product_by_id(product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            json_data = ProductResponse.model_validate(product)
            return {"product": json_data}
    except Exception as e:
        print(f"Error occurred while fetching product by ID {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")