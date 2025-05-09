from fastapi import FastAPI
from app.routes import match_routes  # fichier à venir

app = FastAPI()

app.include_router(match_routes.router)