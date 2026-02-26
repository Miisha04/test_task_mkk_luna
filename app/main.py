import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Organizations",
    lifespan=lifespan
)


if __name__ == "__main__":
    
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )

    