from fastapi import APIRouter,HTTPException,status,Depends
from . import schema
import models
from sqlalchemy.orm import Session
from database import get_db,engine
import pandas as pd
from typing import List

from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
  print(lon1, lat1, lon2, lat2,end=" ")
  # convert decimal degrees to radians
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  # haversine formula
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a))
  r = 6371 # Radius of earth in kilometers. Use 3956 for miles
  print(c*r)
  return c * r


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

@router.get('/{user_id}',status_code=status.HTTP_200_OK,response_model=List[schema.ShowAddress])
def get_address_by_range(user_id,lat:float,long:float,distance:int,db: Session = Depends(get_db)):
    address = db.query(models.Address).join(models.User).filter(models.User.id == user_id)
    df = pd.read_sql_query(
    sql = address.statement,
    con = engine
    )
    
    current_lat_long=(long,lat)
    def row_hsign(row):
        return haversine(*current_lat_long,row['long'],row['lat'])

    df["distance"]=df.apply(row_hsign,axis=1)
    df=df.loc[df['distance'] <distance]
    address_ids = df["id"].tolist()
    address = db.query(models.Address).filter(models.Address.id.in_ (address_ids)).all()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No address found")

    return address

#https://kanoki.org/2019/02/14/how-to-find-distance-between-two-points-based-on-latitude-and-longitude-using-python-and-sql/
#https://www.geeksforgeeks.org/sqlalchemy-orm-conversion-to-pandas-dataframe/