import uuid
from xml.dom.minidom import Entity


class Product(Entity):
    id: uuid.UUID
    name: str
    category_id: uuid.UUID
    price: int
    description: str
    specs: dict[str, str]