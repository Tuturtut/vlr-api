from fastapi import APIRouter
from app.controllers.match_controller import fetch_live_matches

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/match/{match_id}")
def get_match_from_id(match_id: int):
    return fetch_live_matches(match_id) 
