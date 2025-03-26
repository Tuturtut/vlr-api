import asyncio
from scraper.match_list import get_match_list
from database import SessionLocal
from models import Match, MatchDetails
from scraper.match import get_match_data

async def update_matches_periodically():
    while True:
        print("🔄 Mise à jour des matchs...")
        data = get_match_list(size=10)  # Récupère les 10 derniers matchs

        db = SessionLocal()
        try:
            for match_id, match in data.items():
                exists = db.query(Match).filter(Match.match_id == match_id).first()
                if not exists:
                    m = Match(
                        match_id=match_id,
                        match_date=match["match_date"],
                        team_1=match["teams"]["team_1"]["name"],
                        team_1_score=match["teams"]["team_1"]["score"],
                        team_2=match["teams"]["team_2"]["name"],
                        team_2_score=match["teams"]["team_2"]["score"],
                        formatted=match["formatted_scores"]["score_named_with_dash"]
                    )
                    db.add(m)
            db.commit()
        finally:
            db.close()

        await asyncio.sleep(30)  # attends 30 secondes avant de recommencer




def store_match_details(match_id):
    db = SessionLocal()
    try:
        exists = db.query(MatchDetails).filter(MatchDetails.match_id == match_id).first()
        if not exists:
            details = get_match_data(match_id)
            m = MatchDetails(
                match_id=match_id,
                team_1=details["team_1"],
                team_2=details["team_2"],
                team_1_score=details["team_1_score"],
                team_2_score=details["team_2_score"],
                score_named_with_dash=details["score_named_with_dash"],
                score_with_dash=details["score_with_dash"],
                score_named_with_colon=details["score_named_with_colon"],
                score_with_colon=details["score_with_colon"],
                games=details["games"]
            )
            db.add(m)
            db.commit()
    finally:
        db.close()
