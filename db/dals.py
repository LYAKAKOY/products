import json
from typing import List
from redis import asyncio as aioredis
from api.schemas import Product


class ProductDal:
    __slots__ = ['db_session', ]

    def __init__(self, db_session: aioredis.Redis):
        self.db_session = db_session

    async def create_product(self, code: str, name: str, price: float, quantity: int) -> Product | None:
        product = Product(code=code, name=name, price=price, quantity=quantity)
        result = await self.db_session.set(product.code, product.model_dump_json())
        if result:
            return product
        return

    async def delete_product(self, code: str) -> str | None:
        result = await self.db_session.delete(code)
        if result:
            return code
        return

    async def get_product_by_code(self, code: str) -> Product | None:
        product = await self.db_session.get(code)
        if product:
            json_data = json.loads(product)
            return Product(**json_data)
        return

    async def get_all_products(self) -> List[Product] | None:
        all_keys = await self.db_session.keys('*')
        if all_keys:
            products = await self.db_session.mget(*all_keys)
            products_list = []
            for product in products:
                json_data = json.loads(product)
                products_list.append(Product(**json_data))
            return products_list
        return
