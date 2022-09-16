from typing import Optional,List
from database import Base
from pydantic import BaseModel
from user.schema import ShowUser

class AddressBase(BaseModel):
    address_detail: str
    lat: float
    long: float
    user: int


class Address(AddressBase):
    class Config():
        orm_mode = True


class ShowAddress(BaseModel):
    address_detail: str
    lat: float
    long: float
    id: int

    class Config():
        orm_mode = True
