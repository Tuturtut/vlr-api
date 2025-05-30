from bs4 import BeautifulSoup


def safe_text(element, default="TBD"):
    """
    Retourne le texte proprement d'un élément BeautifulSoup ou une valeur par défaut.
    """
    return element.text.strip() if element else default


def clean_nested_span(span):
    """
    Supprime un span enfant dans un autre span.
    """
    nested = span.find("span")
    if nested:
        nested.decompose()
    return span.text.strip()


def fetch_soup(url):
    """
    Effectue une requête HTTP et retourne le BeautifulSoup de la page.
    """
    import requests
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    print(f"➡️ Requete vers {url}")
    return BeautifulSoup(response.text, "html.parser")


def format_scores(team1, score1, score2, team2):
    """
    Retourne les noms et scores des équipes de manières formatés
    """
    return {
        "score_named_with_dash": f"{team1} {score1} - {score2} {team2}",
        "score_with_dash": f"{score1} - {score2}",
        "score_named_with_colon": f"{team1} {score1} : {score2} {team2}",
        "score_with_colon": f"{score1} : {score2}"
    }