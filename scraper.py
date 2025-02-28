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


def get_match_results():
    match_results_url = MATCH_LIST_URL + "/results"
    response = requests.get(match_results_url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    matches = []
    
    # Récupérer tous les blocs de match
    match_list = soup.find_all("div", class_="wf-card")  # Chaque carte représente un match

    for match in match_list:
        # Récupérer l'ID du match
        match_link = match.find("a", class_="match-item")  # Lien vers la page du match
        if not match_link:
            continue  # Passer si aucun lien trouvé

        match_id = match_link["href"].split("/")[1]  # Extraire l'ID du match

        # Récupérer les équipes
        teams = match.find_all("div", class_="match-item-vs-team-name")
        if len(teams) < 2:
            continue

        team_1 = teams[0].text.strip()
        team_2 = teams[1].text.strip()

        # Récupérer le score
        score_div = match.find("div", class_="match-item-vs-score")
        if score_div:
            score_spans = score_div.find_all("span")
            if len(score_spans) >= 2:
                team_1_score = score_spans[0].text.strip()
                team_2_score = score_spans[1].text.strip()
            else:
                team_1_score = team_2_score = "N/A"
        else:
            team_1_score = team_2_score = "N/A"

        # Récupérer la date du match (si disponible)
        date_div = match.find("div", class_="match-item-time")
        match_date = date_div.text.strip() if date_div else "Date inconnue"

        # Ajouter au tableau de résultats
        matches.append({
            "match_id": match_id,
            "team_1": team_1,
            "team_2": team_2,
            "team_1_score": team_1_score,
            "team_2_score": team_2_score,
            "score_named_with_dash": f"{team_1} {team_1_score} - {team_2_score} {team_2}",
            "score_with_dash": f"{team_1_score} - {team_2_score}",
            "score_named_with_colon": f"{team_1} {team_1_score} : {team_2_score} {team_2}",
            "score_with_colon": f"{team_1_score} : {team_2_score}",
            "match_date": match_date
        })

    return matches

# Exécuter le script et afficher en JSON
if __name__ == "__main__":
    print(get_match_results())
