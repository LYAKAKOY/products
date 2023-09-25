from typing import Generator
from redis import asyncio as aioredis


async def get_db() -> Generator:
    redis = aioredis.from_url(
        'redis://redis:6379',
        encoding='utf-8',
        decode_responses=True
    )
    try:
        yield await redis
    finally:
        await redis.close()
