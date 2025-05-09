from fastapi import APIRouter
from app.controllers.match_controller import fetch_match_from_id

router = APIRouter(prefix="/matches", tags=["matches"])

@router.get("/match/{match_id}")
def get_match_from_id(match_id: int):
    return fetch_match_from_id(match_id) 