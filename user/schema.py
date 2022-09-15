from typing import Optional,List
from database import Base
from pydantic import BaseModel


class User(BaseModel):
    name : str
    email : str
    password : str 

class ShowUser(BaseModel): #Response model
    name : str
    email : str
    class Config():
        orm_mode=True
