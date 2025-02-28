import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

URL = "https://www.vlr.gg"
MATCH_LIST_URL = URL + "/matches"


def get_live_scores(size=None):
    """
    Récupère les scores des matchs en direct sur la page des matchs.
    """
    response = requests.get(MATCH_LIST_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    matches = soup.find_all("a", class_="match-item")

    if size is not None:
        matches = matches[:size]

    results = []
    for match in matches:
        teams = match.find_all("div", class_="match-item-vs-team-name")
        scores = match.find_all("div", class_="match-item-vs-team-score")

        if teams and scores:
            results.append([
                teams[0].text.strip(),
                teams[1].text.strip(),
                f"{scores[0].text.strip()} - {scores[1].text.strip()}"
            ])

    return results


def get_match_score(match_id):
    """
    Récupère les scores détaillés d'un match spécifique.
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
    results = []
    i = 1
    for index, game in enumerate(maps):
        
        scores = game.find_all("div", class_="score")
        if len(scores) >= 2:
            team1_score = scores[0].text.strip()
            team2_score = scores[1].text.strip()
            results.append([f"Manche {i}", team1_score, team2_score])
            i += 1

    return [["Score", team1_name, team2_name]] + results  # Ajoute un en-tête à l'affichage


def display_scores(scores):
    """
    Affiche les scores sous forme de tableau.
    """
    if scores and len(scores) > 1:  # Vérifier que les résultats ne sont pas vides
        table = tabulate(scores, headers="firstrow", tablefmt="grid")
        print(table)
    else:
        print("Aucun score trouvé.")


# Exécuter l'affichage si on lance ce fichier directement
if __name__ == "__main__":
    print("\nDétails du match :")
    display_scores(get_match_score(449012))
