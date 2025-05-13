from fastapi import APIRouter
from app.controllers.match_controller import fetch_match_from_id, get_matchs

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/match/{match_id}")
def get_match_from_id(match_id: int):
    """
    Fetch match details from the database or scrape if not found.
    """
    return fetch_match_from_id(match_id) 

@router.get("/")
def get_match_list(size: int = 10, status: str = "ended"):
    """
    Returns a list of matches from the database
    """
    return get_matchs(size=size, status=status)