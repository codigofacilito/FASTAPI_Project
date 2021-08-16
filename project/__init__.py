from fastapi import FastAPI
from fastapi import APIRouter

from fastapi import status
from fastapi import Depends
from fastapi import HTTPException

from .database import User
from .database import Movie
from .database import UserReview

from fastapi.security import OAuth2PasswordRequestForm

from .routers import user_router
from .routers import review_router

from .common import create_access_token

from .database import database as connection

app = FastAPI(title='Movies Review CF', 
            description='En este proyecto seremos capaces de reseñar peliculas.', 
            version='0.1')

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(review_router)

app.include_router(api_v1)

@app.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) 

    return {
        'access_token': create_access_token(user.id, user.username),
        'token_type': 'bearer'
    } 


@app.on_event("startup")
async def startup():
    if connection.is_closed():
        connection.connect()
    
    connection.create_tables([User, Movie, UserReview])


@app.on_event("shutdown")
async def startup():
    if not connection.is_closed():
        connection.close()

