from fastapi import HTTPException
from pydantic import BaseModel, field_validator


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        from_attributes = True


class ShowProduct(TunedModel):
    name: str
    price: float
    quantity: int


class Product(BaseModel):
    name: str
    price: float
    quantity: int

    @field_validator('price')
    @classmethod
    def check_price(cls, value):
        if value < 0:
            raise HTTPException(
                status_code=400, detail="Сумма должна быть выше или равна нулю"
            )
        return value

    @field_validator('quantity')
    @classmethod
    def check_quantity(cls, value):
        if value <= 0:
            raise HTTPException(
                status_code=400, detail="Количество товара должно быть больше нуля"
            )
        return value