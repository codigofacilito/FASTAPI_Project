from fastapi import FastAPI
from fastapi import APIRouter

from .database import User
from .database import Movie
from .database import UserReview

from .routers import user_router
from .routers import review_router

from .database import database as connection

app = FastAPI(title='Movies Review CF', 
            description='En este proyecto seremos capaces de reseñar peliculas.', 
            version='0.1')

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(user_router)
api_v1.include_router(review_router)

app.include_router(api_v1)

@app.on_event("startup")
async def startup():
    if connection.is_closed():
        connection.connect()
    
    connection.create_tables([User, Movie, UserReview])

@app.on_event("shutdown")
async def startup():
    if not connection.is_closed():
        connection.close()

