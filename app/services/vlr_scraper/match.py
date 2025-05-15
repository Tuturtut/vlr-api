from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from app.services.vlr_scraper.utils import fetch_soup, safe_text, clean_nested_span
from app.services.vlr_scraper.config import BASE_URL
from app.services.vlr_scraper.utils import clean_nested_span
import re

def get_match_data(match_id):
    soup = fetch_soup(f"{BASE_URL}/{match_id}")
    team1_name, team2_name = extract_team_names(soup)
    team1_score, team2_score = extract_match_score(soup)
    games = extract_map_scores(soup)

    status = extract_match_status(soup)
    seconds_until_match = extract_seconds_until_match(soup)
    scheduled_time = extract_scheduled_datetime(soup)

    return format_match_json(match_id, team1_name, team2_name, team1_score, team2_score, games, status, seconds_until_match, scheduled_time)


def extract_team_names(soup):
    team1 = soup.find("div", class_="match-header-link-name mod-1")
    team2 = soup.find("div", class_="match-header-link-name mod-2")

    team1_name = (
        team1.find("div", class_="wf-title-med").text.strip()
        if team1 and team1.find("div", class_="wf-title-med")
        else "Équipe 1"
    )

    team2_name = (
        team2.find("div", class_="wf-title-med").text.strip()
        if team2 and team2.find("div", class_="wf-title-med")
        else "Équipe 2"
    )

    return team1_name, team2_name


def extract_match_score(soup):
    team1_score = team2_score = 0
    score_div = soup.find("div", class_="match-header-vs-score")

    if score_div:
        score_spans = score_div.find_all("span")
        score_spans = [s for s in score_spans if s.get("class") != ["match-header-vs-score-colon"]]

        if len(score_spans) == 2:
            try: 
                team1_score = int(score_spans[0].text.strip())
                team2_score = int(score_spans[1].text.strip())
            except ValueError:
                team1_score = team2_score = 0
    return team1_score, team2_score


def extract_map_scores(soup):
    maps = soup.find_all("div", class_="vm-stats-game")
    games = []
    game_index = 1
    for i, game in enumerate(maps, start=1):
        map_name = "TBD"
        map_duration_td = timedelta(0)
        scores = game.find_all("div", class_="score")
        map_div = game.find("div", class_="map")

        if map_div and map_div.div and map_div.div.span:
            map_name = clean_nested_span(map_div.div.span)
            duration_div = map_div.find("div", class_="map-duration")
            if duration_div:
                raw_duration = duration_div.text.strip()
                if raw_duration != "-":
                    map_duration_td = parse_map_duration(raw_duration)

        if len(scores) >= 2:
            team1_score = scores[0].text.strip()
            team2_score = scores[1].text.strip()
            if team1_score.isdigit() and team2_score.isdigit():
                team1_score = int(team1_score)
                team2_score = int(team2_score)
                is_overtime = team1_score > 13 or team2_score > 13
                games.append({
                    "game": game_index,
                    "map_name": map_name,
                    "map_duration": str(map_duration_td),
                    "map_duration_seconds": int(map_duration_td.total_seconds()),
                    "team_1_score": team1_score,
                    "team_2_score": team2_score,
                    "is_overtime": is_overtime,
                })
                game_index += 1

    return games

def parse_map_duration(duration_str):
    try:
        minutes, seconds = map(int, duration_str.strip().split(":"))
        return timedelta(minutes=minutes, seconds=seconds)
    except Exception:
        return timedelta(0)

def extract_match_status(soup):
    status_div = soup.find("span", class_="match-header-vs-note mod-live")
    if status_div:
        return "live"

    status_div = soup.find("span", class_="match-header-vs-note mod-upcoming")
    if status_div and parse_countdown(status_div.text.strip()):
        return "planned"

    return "ended"

def extract_seconds_until_match(soup):
    status_div = soup.find("span", class_="match-header-vs-note mod-upcoming")
    if not status_div:
        return None
    parsed = parse_countdown(status_div.text.strip())
    if parsed:
        days, hours, minutes = parsed
        return days * 86400 + hours * 3600 + minutes * 60
    return None

def extract_scheduled_datetime(soup):
    status_div = soup.find("span", class_="match-header-vs-note mod-upcoming")
    if not status_div:
        return None
    parsed = parse_countdown(status_div.text.strip())
    if parsed:
        days, hours, minutes = parsed
        return (datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)).isoformat() + "Z"
    return None

def parse_countdown(status_text):
    match = re.match(r"^(?:(\d+)d\s*)?(?:(\d+)h\s*)?(?:(\d+)m)?$", status_text.lower())
    if not match:
        return None
    days = int(match.group(1) or 0)
    hours = int(match.group(2) or 0)
    minutes = int(match.group(3) or 0)
    return days, hours, minutes

def format_match_json(match_id, team1_name, team2_name, team1_score, team2_score, games, status, seconds_until_match=None, scheduled_time=None):
    data = {
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
        "status": status,
        "seconds_until_match": seconds_until_match,
        "scheduled_time": scheduled_time,
    }    

    return data
