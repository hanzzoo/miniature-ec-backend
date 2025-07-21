from app.repository.ProductRepository import ProductRepository
from app.schemas import CartItemSchema, ProductSchema

class PurchaseUseCase:
    @classmethod
    async def calc_total_price(cls, cart_items:list[CartItemSchema], products_repo: ProductRepository) -> int:
        total = 0
        for item in cart_items:
            product_id = item.product_id
            product = await products_repo.get_product_by_id(product_id)
            if not product:
                return 0
            product_schema = ProductSchema.model_validate(product)
            if not product_schema:
                return 0
            price = product_schema.price
            if not price:
                return 0

            total += int(price) * item.quantity
            return total
        return 0