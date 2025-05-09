from app.services.vlr_scraper.match_list import get_match_list
from app.services.vlr_scraper.match import get_match_data as scrape_match_data
from database import SessionLocal
from app.db.models import MatchDetails

def fetch_match_from_id(match_id: int):
    db = SessionLocal()
    match = db.query(MatchDetails).filter(MatchDetails.match_id == match_id).first()

    if not match:
        try:
            print(f"⏳ Scraping match {match_id}...")
            details = scrape_match_data(match_id)
            print(f"✅ Scraping terminé.")
            match = MatchDetails(
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
            db.add(match)
            db.commit()
        except Exception as e:
            db.close()
            return {"error": f"Scraping échoué pour match {match_id}: {str(e)}"}
    else:
        print(f"✅ Match {match_id} trouvé en base de données.")
        
    result = {
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
    db.close()
    return result