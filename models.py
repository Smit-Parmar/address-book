from enum import unique
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey,Float
from sqlalchemy.orm import relationship

class Address(Base):

    __tablename__='addresses'
    id = Column(Integer,primary_key=True, index=True)
    address_detail=Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    lat= Column(Float)
    long= Column(Float)
    user = relationship("User", back_populates="addresses")

class User(Base):

    __tablename__='users'
    id = Column(Integer,primary_key=True, index=True)
    name=Column(String)
    email= Column(String,unique=True)
    password= Column(String)

    addresses = relationship('Address', back_populates="user")