from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Chemin vers la base SQLite (fichier local)
DATABASE_URL = "sqlite:///./matches.db"

# Création de l'"engine" de connexion à la base
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Permet de créer une session pour accéder à la base
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base pour déclarer les modèles de tables
Base = declarative_base()
