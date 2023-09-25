from fastapi import FastAPI, APIRouter
from api.handlers import product_router

app = FastAPI()

main_router = APIRouter()
main_router.include_router(product_router, prefix='', tags=['products'])
app.include_router(main_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
