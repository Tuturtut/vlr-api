import scraper
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
def get_match_score(match_id: int):
    """
    Route pour récupérer le détail des scores d'un match spécifique.
    """
    return scraper.get_match_score(match_id)

