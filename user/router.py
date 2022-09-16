from fastapi import APIRouter,HTTPException,status
from . import schema
import models
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,status
from database import get_db
from .hashing import Hash


router= APIRouter(
    prefix="/user",
    tags=['User']
)

####################################### User ##################################

@router.post('/',status_code=201,response_model=schema.ShowUser)
def create(request:schema.User , db: Session = Depends(get_db)):

    new_user= models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=schema.ShowUser)
def show(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user