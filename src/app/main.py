import uvicorn
from fastapi import FastAPI
from routers.address import address_router

app = FastAPI()
app.include_router(address_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
