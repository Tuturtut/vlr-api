from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Chemin vers la base SQLite (fichier local)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'matches.db')}"


# Création de l'"engine" de connexion à la base
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Permet de créer une session pour accéder à la base
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base pour déclarer les modèles de tables
Base = declarative_base()
