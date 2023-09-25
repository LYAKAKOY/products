import json
import uuid
from typing import List
from redis import asyncio as aioredis
from fastapi import APIRouter, Depends
from db.models import Product
from db.session import get_db

product_router = APIRouter()


@product_router.get('/products')
async def get_products(db: aioredis.Redis = Depends(get_db)) -> List[Product]:
    all_keys = await db.keys('*')
    items = await db.mget(*all_keys)
    products = []
    for item in items:
        json_data = json.loads(item)
        products.append(Product(**json_data))
    return products


@product_router.post('/products')
async def create_products(item: Product, db: aioredis.Redis = Depends(get_db)) -> bool:
    return await db.set(str(uuid.uuid4()), item.model_dump_json())
