from sqlalchemy import Column, Integer, String, JSON, DateTime
from app.db.database import Base
from datetime import datetime

class Match(Base):
    __tablename__ = "match"

    match_id = Column(Integer, primary_key=True, index=True)
    team_1 = Column(String)
    team_2 = Column(String)
    team_1_score = Column(Integer)
    team_2_score = Column(Integer)
    score_named_with_dash = Column(String)
    score_with_dash = Column(String)
    score_named_with_colon = Column(String)
    score_with_colon = Column(String)
    games = Column(JSON)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(String, default="planned")