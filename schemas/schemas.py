from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True


class MaterialBase(BaseModel):
    name: str


class MaterialCreate(MaterialBase):
    pass


class MaterialRead(MaterialBase):
    id: int

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None


class MaterialUpdate(BaseModel):
    name: Optional[str] = None
    product_id: Optional[int] = None