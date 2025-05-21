import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.controllers.match_controller import update_live_matches_periodically
from app.db.init_db import init_db
from app.routes import match_routes

init_db()
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(update_live_matches_periodically())
    yield
    

app = FastAPI(lifespan=lifespan)
app.include_router(match_routes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Valorant Live Scores API!"}