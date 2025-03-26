import scraper
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import scraper.match, scraper.match_list
from contextlib import asynccontextmanager
import asyncio
from background import update_matches_periodically
from database import SessionLocal
from models import Match, MatchDetails


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tâche de fond lancée au démarrage
    task = asyncio.create_task(update_matches_periodically())
    yield
    # Optionnel : à la fermeture (si tu veux arrêter la tâche proprement)
    task.cancel()

app = FastAPI(lifespan=lifespan)

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
    db = SessionLocal()
    match = db.query(MatchDetails).filter(MatchDetails.match_id == match_id).first()
    db.close()

    if not match:
        return {"error": "Match non trouvé en base. Tu dois l’ajouter d’abord."}

    return {
        "match_id": match.match_id,
        "team_1": match.team_1,
        "team_2": match.team_2,
        "team_1_score": match.team_1_score,
        "team_2_score": match.team_2_score,
        "score_named_with_dash": match.score_named_with_dash,
        "score_with_dash": match.score_with_dash,
        "score_named_with_colon": match.score_named_with_colon,
        "score_with_colon": match.score_with_colon,
        "games": match.games
    }

@app.get("/matchs/results")
def get_match_results(limit: int = None):
    """
    Retourne les derniers matchs enregistrés en base, triés par date décroissante.
    """
    db = SessionLocal()
    matches = db.query(Match).order_by(Match.match_date.desc()).limit(limit).all()
    db.close()

    return [
        {
            "match_id": m.match_id,
            "match_date": m.match_date,
            "team_1": {
                "name": m.team_1,
                "score": m.team_1_score
            },
            "team_2": {
                "name": m.team_2,
                "score": m.team_2_score
            },
            "formatted_score": m.formatted
        }
        for m in matches
    ]

@app.get("/matchs/schedule")
def get_match_schedule(size: int = None):
    return scraper.match_list.get_match_list(size=size, type="schedule")