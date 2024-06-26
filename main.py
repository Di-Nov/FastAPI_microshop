from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from api.v1.routers_v1 import routers_v1
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Менеджер для создания таблиц перед запуском приложения.
    Выполнения каких-то действий после закрытия прилодения (После yieald)"""
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=routers_v1, prefix=settings.api_v1_prefix)


def run_app():
    return uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    run_app()
