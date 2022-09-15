from fastapi import APIRouter,HTTPException,status,Depends
from . import schema
import models
from sqlalchemy.orm import Session
from database import get_db
import pandas as pd

router = APIRouter(
    prefix="/address",
    tags=['Address']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schema.Address,db: Session = Depends(get_db)):
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

@router.get('/{id}',status_code=status.HTTP_200_OK,response_model=schema.ShowBlog)
def get_perticuler_blog(id,db: Session = Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"blog not found")
    return blog

#https://kanoki.org/2019/02/14/how-to-find-distance-between-two-points-based-on-latitude-and-longitude-using-python-and-sql/
#https://www.geeksforgeeks.org/sqlalchemy-orm-conversion-to-pandas-dataframe/