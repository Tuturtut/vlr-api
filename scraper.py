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

    score_div = soup.find("div", class_="match-header-vs-score")

    if score_div:
        score_spans = score_div.find_all("span")
        for item in score_spans:
            if item.get("class") == ["match-header-vs-score-colon"]:
                score_spans.remove(item)

        if len(score_spans) == 2:
            team1_score = score_spans[0].text.strip()
            team2_score = score_spans[1].text.strip()
            print(f"Score global: {team1_score} - {team2_score}")
        else:
            print("Impossible de récupérer le score global.")
    else:
        print("Le score global n'a pas été trouvé.")


    team1_name = team1.find("div", class_="wf-title-med").text.strip() if team1 else "Équipe 1"
    team2_name = team2.find("div", class_="wf-title-med").text.strip() if team2 else "Équipe 2"

    # Récupération des scores par manche
    maps = soup.find_all("div", class_="vm-stats-game")  # Récupérer tous les blocs de maps
    games = {}
    i = 1
    for index, game in enumerate(maps):
        scores = game.find_all("div", class_="score")

        if len(scores) >= 2:
            team1_game_score = scores[0].text.strip()
            team2_game_score = scores[1].text.strip()
            games[f"game_{i}"] = {
                "game": i,
                "team_1_score": team1_game_score,
                "team_2_score": team2_game_score
            }

            i += 1

    # Format JSON
    match_data = {
        "match_id": match_id,
        "team_1": team1_name,
        "team_2": team2_name,
        "team_1_score": team1_score,
        "team_2_score": team2_score,
        "score_named_with_dash": f"{team1_name} {team1_score} - {team2_score} {team2_name}",
        "score_with_dash": f"{team1_score} - {team2_score}",
        "score_named_with_colon": f"{team1_name} {team1_score} : {team2_score} {team2_name}",
        "score_with_colon": f"{team1_score} : {team2_score}",
        "games": games,
    }


    return match_data  # Retourne directement un dictionnaire


def get_match_results(size=None):
    """
    Récupère les résultats des matchs terminés sous forme d'un objet JSON, avec la date complète.
    """
    match_results_url = MATCH_LIST_URL + "/results"
    response = requests.get(match_results_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    matches = {}

    # Récupérer tous les blocs de date des matchs
    date_blocks = soup.find_all("div", class_="wf-label mod-large")  # Contient la date complète
    match_cards = soup.find_all("div", class_="wf-card")  # Contient les matchs
    match_cards = match_cards[:size] if size else match_cards

    current_date = "Date inconnue"

    for match_card in match_cards:
        # Vérifier si un bloc date précède le match et l'assigner
        prev_sibling = match_card.find_previous_sibling("div", class_="wf-label mod-large")
        if prev_sibling:
            current_date = prev_sibling.text.strip()

        # Récupérer l'ID du match
        match_link = match_card.find("a", class_="match-item")
        if not match_link:
            continue  # Passer si aucun lien trouvé

        match_id = match_link["href"].split("/")[1]  # Extraire l'ID du match

        # Récupérer les équipes
        teams = match_card.find_all("div", class_="match-item-vs-team-name")
        if len(teams) < 2:
            continue

        team_1 = teams[0].text.strip()
        team_2 = teams[1].text.strip()

        # Récupérer le score
        score_divs = match_card.find_all("div", class_="match-item-vs-team-score")
        if score_divs and len(score_divs) >= 2:
            team_1_score = score_divs[0].text.strip()
            team_2_score = score_divs[1].text.strip()
        else:
            team_1_score = team_2_score = "N/A"

        # Ajouter au dictionnaire de résultats
        matches[match_id] = {
            "match_id": match_id,
            "match_date": current_date,  # Ajout de la date correcte
            "teams": {
                "team_1": {
                    "name": team_1,
                    "score": team_1_score
                },
                "team_2": {
                    "name": team_2,
                    "score": team_2_score
                }
            },
            "formatted_scores": {
                "score_named_with_dash": f"{team_1} {team_1_score} - {team_2_score} {team_2}",
                "score_with_dash": f"{team_1_score} - {team_2_score}",
                "score_named_with_colon": f"{team_1} {team_1_score} : {team_2_score} {team_2}",
                "score_with_colon": f"{team_1_score} : {team_2_score}"
            }
        }

    return matches

# Exécuter le script et afficher en JSON
if __name__ == "__main__":
    print(get_match_results())
