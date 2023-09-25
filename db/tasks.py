from typing import List
import redis


def get_all_keys() -> List[str]:
    db = redis.from_url(
        'redis://redis:6379',
        encoding='utf-8',
        decode_responses=True
    )
    all_keys = db.keys('*')
    db.close()
    return all_keys
