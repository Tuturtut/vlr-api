from database import Base, engine
from models import Match

# Crée la table si elle n'existe pas encore
Base.metadata.create_all(bind=engine)
