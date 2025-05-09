from fastapi import APIRouter
from app.controllers.match_controller import fetch_match_from_id, fetch_match_results

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/match/{match_id}")
def get_match_from_id(match_id: int):
    return fetch_match_from_id(match_id) 

@router.get("/results")
def get_match_results(limit: int = None):
    """
    Retourne les derniers matchs enregistrés en base, triés par date décroissante.
    """
    return fetch_match_results(limit)