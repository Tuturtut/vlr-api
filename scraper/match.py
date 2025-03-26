from bs4 import BeautifulSoup
from scraper.utils import fetch_soup, safe_text, clean_nested_span
from scraper.config import BASE_URL



def get_match_data(match_id):
    soup = fetch_soup(f"{BASE_URL}/{match_id}")
    team1_name, team2_name = extract_team_names(soup)
    team1_score, team2_score = extract_global_score(soup)
    games = extract_games(soup)

    return format_match_json(match_id, team1_name, team2_name, team1_score, team2_score, games)


def extract_team_names(soup):
    team1 = soup.find("div", class_="match-header-link-name mod-1")
    team2 = soup.find("div", class_="match-header-link-name mod-2")

    team1_name = team1.find("div", class_="wf-title-med").text.strip() if team1 else "Équipe 1"
    team2_name = team2.find("div", class_="wf-title-med").text.strip() if team2 else "Équipe 2"

    return team1_name, team2_name


def extract_global_score(soup):
    team1_score = team2_score = "0"
    score_div = soup.find("div", class_="match-header-vs-score")

    if score_div:
        score_spans = score_div.find_all("span")
        score_spans = [s for s in score_spans if s.get("class") != ["match-header-vs-score-colon"]]

        if len(score_spans) == 2:
            team1_score = score_spans[0].text.strip()
            team2_score = score_spans[1].text.strip()

    return team1_score, team2_score


from scraper.utils import clean_nested_span

def extract_games(soup):
    maps = soup.find_all("div", class_="vm-stats-game")
    games = []
    for i, game in enumerate(maps, start=1):
        map_name = "TBD"
        map_duration = "0"
        scores = game.find_all("div", class_="score")
        map_div = game.find("div", class_="map")

        if map_div and map_div.div and map_div.div.span:
            map_name = clean_nested_span(map_div.div.span)
            duration_div = map_div.find("div", class_="map-duration")
            if duration_div:
                map_duration = duration_div.text.strip()
                if map_duration == "-":
                    map_duration = "0"

        if len(scores) >= 2:
            team1_score = scores[0].text.strip()
            team2_score = scores[1].text.strip()
            games.append({
                "game": i,
                "map_name": map_name,
                "map_duration": map_duration,
                "team_1_score": team1_score,
                "team_2_score": team2_score
            })

    return games


def format_match_json(match_id, team1_name, team2_name, team1_score, team2_score, games):
    return {
        "match_id": match_id,
        "team_1": team1_name,
        "team_2": team2_name,
        "team_1_score": team1_score,
        "team_2_score": team2_score,
        "score_named_with_dash": f"{team1_name} {team1_score} - {team2_score} {team2_name}",
        "score_with_dash": f"{team1_score} - {team2_score}",
        "score_named_with_colon": f"{team1_name} {team1_score} : {team2_score} {team2_name}",
        "score_with_colon": f"{team1_score} : {team2_score}",
        "games": {f"game_{g['game']}": g for g in games}
    }
