from fastapi import APIRouter,HTTPException,status,Depends
from . import schema
import models
from sqlalchemy.orm import Session
from database import get_db,engine
import pandas as pd
from typing import List
from .formula import haversine,get_dataframe


router = APIRouter(
    prefix="/address",
    tags=['Address']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schema.Address,db: Session = Depends(get_db)):
    '''
    user will add address along with latitude and longitude coordinates
    '''
    user=db.query(models.User).filter(models.User.id == request.user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {request.user} not found")

    new_address = models.Address(address_detail=request.address_detail, lat=request.lat,long=request.long,user_id=request.user)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int,db: Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == id)

    if not address.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Address with id {id} not found")

    address.delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id:int,request:schema.Address, db:Session = Depends(get_db)):
    address = db.query(models.Address).filter(models.Address.id == id)

    if not address.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Address with id {id} not found")

    address.update({"address_detail":request.address_detail, "lat":request.lat,"long":request.long,"user_id":request.user},synchronize_session=False)
    db.commit()
    return 'updated'

@router.get('/{user_id}',status_code=status.HTTP_200_OK,response_model=List[schema.ShowAddress])
def get_address_by_range(user_id,lat:float,long:float,distance:int,db: Session = Depends(get_db)):
    address = db.query(models.Address).join(models.User).filter(models.User.id == user_id)
    if not address.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No address found")

    address_ids=get_dataframe(address,long,lat,distance)
    address = db.query(models.Address).filter(models.Address.id.in_ (address_ids)).all()
    

    return address
