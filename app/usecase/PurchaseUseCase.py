from app.schemas import CartItemSchema, ProductSchema

class PurchaseUseCase:
    @classmethod
    async def calc_total_price(cls, cart_items: list[CartItemSchema], products: list[ProductSchema]) -> int:
        total = 0
        # product_idでProductSchemaを検索し、price×quantityを合算
        product_map = {p.product_id: p for p in products}
        for item in cart_items:
            product = product_map.get(item.product_id)
            print(f"product: {product}, price: {getattr(product, 'price', None)}, type: {type(getattr(product, 'price', None))}")
            if not product or product.price is None:
                continue
            total += int(product.price) * item.quantity
        return total