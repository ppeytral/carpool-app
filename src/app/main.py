from typing import Annotated

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from routers.address import address_router
from routers.auth import auth_router
from routers.car import car_router
from routers.car_make import car_make_router
from routers.car_model import car_model_router
from routers.school import school_router
from routers.student import student_router
from routers.user import user_router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

origins = [
    "http://localhost:46585",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(address_router)
app.include_router(auth_router)
app.include_router(car_make_router)
app.include_router(car_model_router)
app.include_router(student_router)
app.include_router(car_router)
app.include_router(user_router)
app.include_router(school_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
