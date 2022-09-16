from typing import Optional,List
from database import Base
from pydantic import BaseModel,Field
from user.schema import ShowUser

class AddressBase(BaseModel):
    address_detail: str= Field(..., description="Enter address detail like city , state, landmark etc", max_length=250)
    lat: float = Field(...,gt=-90,lt=90,description="Enter latitude of address")
    long: float = Field(...,gt=-180,lt=180,description="Enter latitude of address")
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
