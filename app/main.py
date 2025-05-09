from fastapi import FastAPI
from app.db.init_db import init_db
from app.routes import match_routes

init_db()

app = FastAPI()
app.include_router(match_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Valorant Live Scores API!"}