from datetime import datetime
from app.services.vlr_scraper.match_list import get_match_list
from app.services.vlr_scraper.match import get_match_data as scrape_match_data
from app.db.database import SessionLocal
from app.db.models import Match

def fetch_match_from_id(match_id: int):
    db = SessionLocal()
    match = db.query(Match).filter(Match.match_id == match_id).first()

    if not match:
        try:
            details = scrape_match_data(match_id)
            print(f"✅ Scraping terminé.")
            match = Match(
                match_id=match_id,
                team_1=details["team_1"],
                team_2=details["team_2"],
                team_1_score=details["team_1_score"],
                team_2_score=details["team_2_score"],
                score_named_with_dash=details["score_named_with_dash"],
                score_with_dash=details["score_with_dash"],
                score_named_with_colon=details["score_named_with_colon"],
                score_with_colon=details["score_with_colon"],
                games=details["games"],
                status=details.get("status", "planned"),  # optionnel
                updated_at=datetime.now()
            )
            db.add(match)
            db.commit()
            db.refresh(match)
        except Exception as e:
            db.close()
            return {"error": f"Scraping échoué pour match {match_id}: {str(e)}"}
    else:
        print(f"✅ Match {match_id} trouvé en base de données.")

    result = {
        str(match.match_id): {
            "match_id": match.match_id,
            "team_1": match.team_1,
            "team_2": match.team_2,
            "team_1_score": match.team_1_score,
            "team_2_score": match.team_2_score,
            "score_named_with_dash": match.score_named_with_dash,
            "score_with_dash": match.score_with_dash,
            "score_named_with_colon": match.score_named_with_colon,
            "score_with_colon": match.score_with_colon,
            "games": match.games,
            "status": match.status,
            "updated_at": str(match.updated_at)
        }
    }

    db.close()
    return result


def get_matchs(size: int = 10, status: str = "results"):
    """
    Returns a list of matches from the database
    """
    db = SessionLocal()
    matches = db.query(Match).order_by(Match.match_id.desc()).limit(size).all()
    db.close()

    if not matches:
        return {"error": "Aucun match trouvé en base de données."}
    else:
        print(f"✅ {len(matches)} matchs trouvés en base de données.")
        return {match.match_id: match for match in matches}