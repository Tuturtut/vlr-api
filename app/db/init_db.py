from app.db.database import Base, engine
from app.db.models import Match

# Crée la table si elle n'existe pas encore
def init_db():
    """
    Initialise la base de données en créant les tables nécessaires.
    """
    Base.metadata.create_all(bind=engine)
