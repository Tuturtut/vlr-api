from datetime import datetime, timedelta

def get_match_status(start_time: datetime, has_score: bool) -> str:
    """
    Détermine le statut d'un match en fonction de son heure de début et de la présence d'un score.
    """
    now = datetime.now()
    if has_score:
        return "end"
    elif start_time <= now <= start_time + timedelta(hours=3):
        return "live"
    else:
        return "planned"
