from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import get_setting
from app.modules.dashboard.router import router as dashboard_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


settings = get_setting()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(dashboard_router)
