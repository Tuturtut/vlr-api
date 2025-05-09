from fastapi import FastAPI
from app.routes import match_routes

app = FastAPI()

app.include_router(match_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Valorant Live Scores API!"}