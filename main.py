import uvicorn
from fastapi import FastAPI

from api.v1.routers_v1 import  routers_v1

app = FastAPI()
app.include_router(routers_v1)

def run_app():
    return uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    run_app()
