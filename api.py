import scraper
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import scraper.match, scraper.match_list

app = FastAPI()

# Configuration du CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplace "*" par ["http://127.0.0.1:5500"] pour plus de sécurité
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API Valorant Live Scores"}

@app.get("/match/{match_id}")
def get_match_data(match_id: int):
    """
    Route pour récupérer le détail des données d'un match spécifique.
    """
    return scraper.match.get_match_data(match_id)

@app.get("/matchs/results")
def get_match_results(size: int = None):
    """
    Route pour récupérer la liste des matchs passés
    """
    return scraper.match_list.get_match_list(size=size)

@app.get("/matchs/schedule")
def get_match_schedule(size: int = None):
    return scraper.match_list.get_match_list(size=size, type="schedule")


