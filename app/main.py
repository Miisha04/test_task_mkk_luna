import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from .database import engine, Base
from .routers import organization

from .security import verify_api_key

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Organizations",
    lifespan=lifespan
)

app.include_router(
    router=organization.router,
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[Depends(verify_api_key)]
)