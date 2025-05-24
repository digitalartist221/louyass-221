# app/routers/maisons.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/maisons",  # Le préfixe de l'URL sera /maisons
    tags=["Maisons"],   # Tag pour la documentation Swagger UI
)

# Placez ici vos opérations CRUD (create_maison, read_maisons, etc.)
# en utilisant les schémas et modèles appropriés.
# ... (code des fonctions create, read, update, delete pour les maisons)