from scraper.match import get_match_data
from scraper.match_list import get_match_list


def test_match_data_structure():
    data = get_match_data(445133)  # match qui marche bien
    assert "team_1" in data
    assert "team_2" in data
    assert "games" in data
    assert isinstance(data["games"], dict)
    assert len(data["games"]) >= 1


def test_match_list_size():
    results = get_match_list(size=3)
    assert isinstance(results, dict)
    assert len(results) == 3
    for match_id, match_data in results.items():
        assert "teams" in match_data
        assert "team_1" in match_data["teams"]
        assert "team_2" in match_data["teams"]
