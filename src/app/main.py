from typing import Annotated

import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from routers.address import address_router
from routers.auth import auth_router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
app.include_router(address_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
