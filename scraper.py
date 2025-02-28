import requests
from bs4 import BeautifulSoup
import json  # Importer json pour la sortie formatée

URL = "https://www.vlr.gg"
MATCH_LIST_URL = URL + "/matches"


def get_match_score(match_id):
    """
    Récupère les scores détaillés d'un match spécifique et retourne un JSON.
    """
    match_url = f"{URL}/{match_id}"
    response = requests.get(match_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    # Récupération des noms des équipes
    team1 = soup.find("div", class_="match-header-link-name mod-1")
    team2 = soup.find("div", class_="match-header-link-name mod-2")

    team1_name = team1.find("div", class_="wf-title-med").text.strip() if team1 else "Équipe 1"
    team2_name = team2.find("div", class_="wf-title-med").text.strip() if team2 else "Équipe 2"

    # Récupération des scores par manche
    maps = soup.find_all("div", class_="vm-stats-game")
    games = []
    
    for index, game in enumerate(maps):
        scores = game.find_all("div", class_="score")
        if len(scores) >= 2:
            team1_score = scores[0].text.strip()
            team2_score = scores[1].text.strip()
            games.append({
                "game": index + 1,
                "team_1_score": team1_score,
                "team_2_score": team2_score
            })

    # Format JSON
    match_data = {
        "match_id": match_id,
        "team_1": team1_name,
        "team_2": team2_name,
        "games": games
    }

    return match_data  # Retourne directement un dictionnaire


# Exécuter le script et afficher en JSON
if __name__ == "__main__":
    match_id = 449012
    match_scores = get_match_score(match_id)

    # Affichage formaté en JSON
    print(json.dumps(match_scores, indent=4, ensure_ascii=False))
