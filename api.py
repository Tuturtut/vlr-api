import scraper
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API Valorant Live Scores"}

@app.get("/match/{match_id}")
def get_match_score(match_id: int):
    """
    Route pour récupérer le détail des scores d'un match spécifique.
    """
    return scraper.get_match_score(match_id)