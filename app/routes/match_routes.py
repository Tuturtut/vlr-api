from fastapi import APIRouter
from app.controllers.match_controller import delete_match_from_id, fetch_match_from_id, get_matchs

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/match/{match_id}")
def get_match_from_id(match_id: int):
    """
    Fetch match details from the database or scrape if not found.
    """
    return fetch_match_from_id(match_id) 

@router.get("/")
def get_match_list(size: int = 10, status: str = None):
    """
    Returns a list of matches from the database
    """
    return get_matchs(size=size, status=status)

@router.get("/live")
def get_live_matches():
    """
    Returns a list of live matches from the database
    """
    return get_matchs(status="live")

@router.delete("/match/{match_id}")
def delete_match(match_id: int):
    """
    Delete a match from the database
    """
    return delete_match_from_id(match_id)