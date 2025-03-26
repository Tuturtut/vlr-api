from sqlalchemy import Column, Integer, String, JSON
from database import Base

class Match(Base):
    __tablename__ = "matches"

    match_id = Column(Integer, primary_key=True, index=True)
    match_date = Column(String)
    team_1 = Column(String)
    team_1_score = Column(String)
    team_2 = Column(String)
    team_2_score = Column(String)
    formatted = Column(String)  # exemple : "Team A 13 - 11 Team B"

class MatchDetails(Base):
    __tablename__ = "match_details"

    match_id = Column(Integer, primary_key=True, index=True)
    team_1 = Column(String)
    team_2 = Column(String)
    team_1_score = Column(String)
    team_2_score = Column(String)
    score_named_with_dash = Column(String)
    score_with_dash = Column(String)
    score_named_with_colon = Column(String)
    score_with_colon = Column(String)
    games = Column(JSON)  # stockage direct du dictionnaire des games