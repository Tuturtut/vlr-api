from datetime import datetime
from bs4 import BeautifulSoup
from datetime import datetime
from scraper.utils import fetch_soup, clean_nested_span, safe_text, format_scores
from scraper.config import BASE_URL, MATCH_LIST_URL



def get_match_list(size=None, type="results"):
    url = f"{MATCH_LIST_URL}/{type}"
    soup = fetch_soup(url)

    match_cards = soup.find_all("div", class_="wf-card")
    matches = []

    for card in match_cards:
        parsed = parse_match_card(card)
        for match in parsed:
            matches.append(match)
            if size and len(matches) >= size:
                break
        if size and len(matches) >= size:
            break

    matches = sorted(matches, key=lambda m: m["match_id"], reverse=True)
    return {match["match_id"]: match for match in matches}



def extract_match_cards(soup, size=None):
    match_cards = soup.find_all("div", class_="wf-card")
    return match_cards[:size] if size else match_cards


def parse_match_card(match_card):
    matches = []

    prev_sibling = match_card.find_previous_sibling("div", class_="wf-label mod-large")
    if not prev_sibling or not prev_sibling.text:
        return []

    dt_text = clean_nested_span(prev_sibling)
    try:
        match_date = datetime.strptime(dt_text, "%a, %B %d, %Y")
    except ValueError:
        match_date = None

    for link in match_card.find_all("a", class_="match-item"):
        match_id = int(link["href"].split("/")[1])

        teams = link.find_all("div", class_="match-item-vs-team-name")
        if len(teams) < 2:
            continue

        team1 = safe_text(teams[0])
        team2 = safe_text(teams[1])

        score_divs = link.find_all("div", class_="match-item-vs-team-score")
        if len(score_divs) >= 2:
            t1_score = safe_text(score_divs[0])
            t2_score = safe_text(score_divs[1])
        else:
            t1_score = t2_score = "TBD"

        if t1_score == "–" and t2_score == "–":
            t1_score = t2_score = "TBD"

        time_div = link.find("div", class_="match-item-time")
        try:
            time_obj = datetime.strptime(time_div.text.strip(), "%I:%M %p") if time_div else None
            match_dt = match_date.replace(hour=time_obj.hour, minute=time_obj.minute) if match_date and time_obj else None
        except:
            match_dt = match_date

        matches.append({
            "match_id": match_id,
            "match_date": match_dt.isoformat() if match_dt else None,
            "teams": {
                "team_1": {"name": team1, "score": t1_score},
                "team_2": {"name": team2, "score": t2_score},
            },
            "formatted_scores": format_scores(team1, t1_score, t2_score, team2)
        })

    return matches
