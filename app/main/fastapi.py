import os
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from dotenv import load_dotenv
from fastapi import FastAPI

from app.main.di import InfraProvider, UseCaseProvider
from app.presentation.fastapi.root import root_router


def init_routers(app: FastAPI):
    app.include_router(root_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    load_dotenv()
    print(os.getenv("MINIO_URL"))
    app = FastAPI(lifespan=lifespan)
    init_routers(app)
    container = make_async_container(FastapiProvider(), InfraProvider(), UseCaseProvider())
    setup_dishka(container=container, app=app)
    return app
