from typing import List
from redis import asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException
from api.schemas import CreateProduct, Product, DeleteProductResponse
from db.session import get_db
from db.dals import ProductDal

product_router = APIRouter()


@product_router.get('/products', response_model=List[Product])
async def get_products(db: aioredis.Redis = Depends(get_db)) -> List[Product]:
    product_dal = ProductDal(db)
    products = await product_dal.get_all_products()
    if products is not None:
        return products
    else:
        raise HTTPException(
            status_code=404, detail=f"No products found"
        )


@product_router.post('/products', response_model=Product)
async def create_products(product: CreateProduct, db: aioredis.Redis = Depends(get_db)) -> Product:
    product_dal = ProductDal(db)
    product = await product_dal.create_product(product.code, product.name, product.price, product.quantity)
    if product is not None:
        return product
    else:
        raise HTTPException(status_code=503, detail=f"Database error")


@product_router.get('/product', response_model=Product)
async def get_product_by_code(code: str, db: aioredis.Redis = Depends(get_db)) -> Product:
    product_dal = ProductDal(db)
    product = await product_dal.get_product_by_code(code)
    if product is not None:
        return product
    else:
        raise HTTPException(status_code=404, detail=f"The product with this code was not found")


@product_router.delete('/product', response_model=DeleteProductResponse)
async def delete_product_by_id(code: str, db: aioredis.Redis = Depends(get_db)) -> DeleteProductResponse:
    product_dal = ProductDal(db)
    code = await product_dal.delete_product(code)
    if code is not None:
        return DeleteProductResponse(code=code)
    else:
        raise HTTPException(status_code=404, detail=f"The product with this code was not found")
