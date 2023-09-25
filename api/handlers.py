import json
from typing import List
from redis import asyncio as aioredis
from fastapi import APIRouter, Depends
from api.schemas import Product, ShowProduct
from db.session import get_db

product_router = APIRouter()


@product_router.get('/products')
async def get_products(db: aioredis.Redis = Depends(get_db)) -> List[ShowProduct]:
    all_keys = await db.keys('*')
    items = await db.mget(*all_keys)
    products = []
    for item in items:
        json_data = json.loads(item)
        products.append(ShowProduct(**json_data))
    return products


@product_router.post('/products')
async def create_products(item: Product, db: aioredis.Redis = Depends(get_db)) -> bool:
    return await db.set(item.code, item.model_dump_json())


@product_router.get('/product')
async def get_product_by_code(code: str, db: aioredis.Redis = Depends(get_db)) -> ShowProduct:
    item = await db.get(code)
    json_data = json.loads(item)
    return ShowProduct(**json_data)


@product_router.delete('/product')
async def delete_product_by_id(code: str, db: aioredis.Redis = Depends(get_db)) -> bool:
    return await db.delete(code)
