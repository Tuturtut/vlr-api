import requests
from bs4 import BeautifulSoup
from tabulate import tabulate  # Pour afficher un tableau

URL = "https://www.vlr.gg/matches"

def get_live_scores():
    try: 
        response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        print("ERREUR")
    matches = soup.find_all("a", class_="match-item")  # Vérifie la classe exacte en inspectant le site

    results = []
    for match in matches:
        teams = match.find_all("div", class_="match-item-vs-team-name")
        scores = match.find_all("div", class_="match-item-vs-team-score")  # Vérifie la classe exacte

        if teams and scores:
            results.append([  # Liste au lieu d'un dictionnaire
                teams[0].text.strip(),
                teams[1].text.strip(),
                f"{scores[0].text.strip()} - {scores[1].text.strip()}"
            ])

    return results

def display_scores():
    scores = get_live_scores()
    if scores:
        table = tabulate(scores, headers=["Équipe 1", "Équipe 2", "Score"], tablefmt="grid")
        print(table)
    else:
        print("Aucun match en direct trouvé.")

# Exécuter l'affichage si on lance ce fichier directement
if __name__ == "__main__":
    display_scores()