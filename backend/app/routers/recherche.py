from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_ # Pour les conditions OR dans la requête

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/recherche",
    tags=["Recherche"],
)

@router.get("/maisons-et-chambres/", response_model=List[Union[schemas.MaisonResponse, schemas.ChambreResponse]])
def search_maisons_et_chambres(
    db: Session = Depends(get_db),
    # Paramètres de recherche communs
    localisation: Optional[str] = Query(None, description="Rechercher par ville ou adresse partielle de la maison."),
    prix_min: Optional[float] = Query(None, description="Prix minimum par mois."),
    prix_max: Optional[float] = Query(None, description="Prix maximum par mois."),
    type_bien: Optional[str] = Query(None, description="Filtrer par type de bien ('maison' ou 'chambre')."),
    disponible: Optional[bool] = Query(True, description="Filtrer par disponibilité (True par défaut)."),
    # Paramètres spécifiques aux chambres
    nombre_lits_min: Optional[int] = Query(None, description="Nombre minimum de lits pour une chambre."),
    salle_de_bain_privee: Optional[bool] = Query(None, description="Indique si la chambre a une salle de bain privée."),
    # Paramètres spécifiques aux maisons
    nombre_chambres_maison_min: Optional[int] = Query(None, description="Nombre minimum de chambres pour une maison."),
    # Pagination
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=200),
):
    """
    Recherche des maisons ou des chambres en fonction de divers critères.

    - **localisation**: Filtre par ville ou adresse partielle.
    - **prix_min / prix_max**: Fourchette de prix mensuel.
    - **type_bien**: Spécifie si la recherche porte sur des 'maisons' ou des 'chambres'.
    - **disponible**: Filtre par disponibilité (par défaut True).
    - **nombre_lits_min**: (Pour les chambres) Nombre minimum de lits.
    - **salle_de_bain_privee**: (Pour les chambres) Indique si la salle de bain est privée.
    - **nombre_chambres_maison_min**: (Pour les maisons) Nombre minimum de chambres.
    """
    results = []

    # Construire la requête pour les maisons
    if type_bien is None or type_bien.lower() == 'maison':
        query_maisons = db.query(models.Maison)

        if localisation:
            query_maisons = query_maisons.filter(
                or_(
                    models.Maison.ville.ilike(f"%{localisation}%"),
                    models.Maison.adresse.ilike(f"%{localisation}%")
                )
            )
        if prix_min is not None:
            query_maisons = query_maisons.filter(models.Maison.prix_mensuel >= prix_min)
        if prix_max is not None:
            query_maisons = query_maisons.filter(models.Maison.prix_mensuel <= prix_max)
        if disponible is not None:
            query_maisons = query_maisons.filter(models.Maison.disponible == disponible)
        if nombre_chambres_maison_min is not None:
            query_maisons = query_maisons.filter(models.Maison.nombre_chambres >= nombre_chambres_maison_min)

        maisons = query_maisons.offset(skip).limit(limit).all()
        results.extend(maisons)

    # Construire la requête pour les chambres
    if type_bien is None or type_bien.lower() == 'chambre':
        query_chambres = db.query(models.Chambre)

        if localisation:
            # Pour les chambres, nous devons joindre la table Maison pour filtrer par localisation
            query_chambres = query_chambres.join(models.Maison).filter(
                or_(
                    models.Maison.ville.ilike(f"%{localisation}%"),
                    models.Maison.adresse.ilike(f"%{localisation}%")
                )
            )
        if prix_min is not None:
            query_chambres = query_chambres.filter(models.Chambre.prix_mensuel >= prix_min)
        if prix_max is not None:
            query_chambres = query_chambres.filter(models.Chambre.prix_mensuel <= prix_max)
        if disponible is not None:
            query_chambres = query_chambres.filter(models.Chambre.disponible == disponible)
        if nombre_lits_min is not None:
            query_chambres = query_chambres.filter(models.Chambre.nombre_lits >= nombre_lits_min)
        if salle_de_bain_privee is not None:
            query_chambres = query_chambres.filter(models.Chambre.salle_de_bain_privee == salle_de_bain_privee)

        chambres = query_chambres.offset(skip).limit(limit).all()
        results.extend(chambres)

    return results