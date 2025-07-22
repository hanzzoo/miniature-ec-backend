import datetime
import os
from typing import Any, AsyncGenerator

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.repository.CartItemRepository import CartItemRepository
from app.repository.CartRepository import CartRepository
from app.repository.ProductRepository import ProductRepository
from app.repository.PurchaseRepository import PurchaseRepository
from app.repository.UserRepository import UserRepository
from app.schemas import (
    AuthorizeUserSchema,
    CartItemSchema,
    GetCartItemResponse,
    GetProductResponse,
    GetProductsResponse,
    LoginRequest,
    LoginResponse,
    ProductSchema,
    RegisterRequest,
    RegisterResponse,
    UpdateToCartRequest,
)
from app.useCase.PurchaseUseCase import PurchaseUseCase

# from app.schemas import PostPurchaseRequest


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+aiomysql://user:user_password@db:3306/my_database?charset=utf8mb4",
)
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = FastAPI(title="Miniature EC Backend", version="1.0.0")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_jwt_token(user_id: str) -> tuple[str, str]:
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    payload: dict[str, Any] = {"user_id": user_id, "exp": expire}
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)  # type: ignore
    return token, expire.isoformat()


def decode_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)  # type: ignore
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/")
async def root():
    return {"message": "Hello from miniature-ec-backend!"}


@app.post("/register", tags=["user_register"], response_model=RegisterResponse)
async def register(user: RegisterRequest, db: AsyncSession = Depends(get_db)):
    try:
        async with db.begin():
            user_repo = UserRepository(db)
            user_id = await user_repo.register_user(
                user_name=user.user.user_name,
                user_email=user.user.user_email,
                user_password=user.user.user_password,
            )
            if not user_id:
                return
            token, expire = create_jwt_token(user_id=user_id)
            return RegisterResponse(user_id=user_id, token=token, expire=expire)
    except Exception:
        raise


@app.post("/login", tags=["login"], response_model=LoginResponse)
async def login(
    user: LoginRequest, db: AsyncSession = Depends(get_db)
) -> LoginResponse:
    try:
        async with db.begin():
            user_repo = UserRepository(db)
            is_password, auth_user = await user_repo.authorize_user(
                user_email=user.user.user_email, user_password=user.user.user_password
            )
            auth_user_id = auth_user.user.user_id
            auth_user_name = auth_user.user.user_name
            if not is_password or not auth_user_id or not auth_user_name:
                raise HTTPException(status_code=401, detail="Not found user")
            token, expire = create_jwt_token(user_id=auth_user_id)
            return LoginResponse(
                user=AuthorizeUserSchema(
                    user_id=auth_user_id, user_name=auth_user_name
                ),
                token=token,
                expire=expire,
            )
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/products", tags=["products"], response_model=GetProductsResponse)
async def get_all_products(db: AsyncSession = Depends(get_db)) -> GetProductsResponse:
    try:
        async with db.begin():
            repo = ProductRepository(db)
            result = await repo.get_all_products()
            products_schema = [
                ProductSchema.model_validate(product) for product in result
            ]
            return GetProductsResponse(products=products_schema)
    except Exception as e:
        print(f"Error occurred while fetching all products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    "/products/{product_id}",
    tags=["products_detail"],
    response_model=GetProductResponse,
)
async def get_product_by_id(
    product_id: str, db: AsyncSession = Depends(get_db)
) -> GetProductResponse:
    try:
        async with db.begin():
            repo = ProductRepository(db)
            result = await repo.get_product_by_id(product_id)
            if not result:
                raise HTTPException(status_code=404, detail="Product not found")

            products_schema = ProductSchema.model_validate(result)
            return GetProductResponse(product=products_schema)
    except Exception as e:
        print(f"Error occurred while fetching product by ID {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/cart/update", tags=["update_to_cart"])
async def update_to_cart(
    request: UpdateToCartRequest,
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
) -> None:
    try:
        async with db.begin():
            cart_repo = CartRepository(db)
            user_id = decode_jwt_token(authorization.replace("Bearer ", ""))
            instance = await cart_repo.create_cart(user_id)

            cart_item_repo = CartItemRepository(db)
            for product in request.products:
                await cart_item_repo.update_product_to_cart(
                    instance, product.product_id, product.quantity
                )
            # TODO: レスポンスに added_product: {'product_name': quantity}[]を返す

    except Exception as e:
        print(f"Error occurred while Add to Cart: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/cart/items", tags=["get_cart_items"], response_model=GetCartItemResponse)
async def get_cart_items(
    db: AsyncSession = Depends(get_db), authorization: str = Header(None)
) -> GetCartItemResponse:
    try:
        async with db.begin():
            cart_repo = CartRepository(db)
            user_id = decode_jwt_token(authorization.replace("Bearer ", ""))
            instance = await cart_repo.get_instance(user_id)
            if not instance:
                return GetCartItemResponse(products=[])

            cart_items_repo = CartItemRepository(db)
            cart_items = await cart_items_repo.get_cart_items(instance)
            cart_item_schemas = [
                CartItemSchema.model_validate(item) for item in cart_items
            ]

            return GetCartItemResponse(products=cart_item_schemas)
    except Exception as e:
        print(f"Error occurred while get to cartItems: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/purchase", tags=["purchase"])
async def purchase(
    db: AsyncSession = Depends(get_db), authorization: str = Header(None)
):
    try:
        async with db.begin():
            user_id = decode_jwt_token(authorization.replace("Bearer ", ""))

            cart_repo = CartRepository(db)
            instance = await cart_repo.get_instance(user_id)
            if not instance:
                return

            cart_items_repo = CartItemRepository(db)
            cart_items = await cart_items_repo.get_cart_items(instance)
            cart_item_schemas = [
                CartItemSchema.model_validate(item) for item in cart_items
            ]

            products_repo = ProductRepository(db)
            result = await products_repo.get_all_products()
            products_schema = [
                ProductSchema.model_validate(product) for product in result
            ]

            total_amount = await PurchaseUseCase.calc_total_price(
                cart_items=cart_item_schemas, products=products_schema
            )

            purchase_repo = PurchaseRepository(db)
            purchase_id = await purchase_repo.order(user_id, total_amount)
            print(f"purchase_id: {purchase_id}")
    except Exception as e:
        print(f"Order Failed: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
