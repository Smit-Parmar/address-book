from fastapi import FastAPI
import models
import database
from user.router import router as user_router
from address.router import router as address_router
app= FastAPI()
models.Base.metadata.create_all(database.engine)

app.include_router(user_router)
app.include_router(address_router)
