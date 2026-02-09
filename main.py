import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.common.postgres import database
from src.prompts.route import prompts_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


app.include_router(prompts_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")