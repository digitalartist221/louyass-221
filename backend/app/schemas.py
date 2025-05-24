from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    nom_utilisateur: Optional[str] = None
    telephone: Optional[str] = None
    cni: Optional[str] = None
    role: str # proprietaire | locataire

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    cree_le: datetime

    class Config:
        from_attributes = True

# --- House Schemas ---
class MaisonBase(BaseModel):
    adresse: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None

class MaisonCreate(MaisonBase):
    proprietaire_id: int

class MaisonResponse(MaisonBase):
    id: int
    proprietaire_id: int
    cree_le: datetime

    class Config:
        from_attributes = True

# --- Room Schemas ---
class ChambreBase(BaseModel):
    maison_id: int
    titre: str
    description: Optional[str] = None
    taille: Optional[str] = None # ex: 12m²
    type: str # simple | appartement | maison
    meublee: bool
    salle_de_bain: bool
    prix: float
    disponible: bool = True

class ChambreCreate(ChambreBase):
    pass

class ChambreResponse(ChambreBase):
    id: int
    cree_le: datetime

    class Config:
        from_attributes = True

# --- Contract Schemas ---
class ContratBase(BaseModel):
    locataire_id: int
    chambre_id: int
    date_debut: date
    date_fin: date
    montant_caution: float
    mois_caution: int # <= 3
    description: Optional[str] = None
    mode_paiement: str # virement | cash | mobile money
    periodicite: str # journalier | hebdomadaire | mensuel
    statut: str # actif | resilié

class ContratCreate(ContratBase):
    pass

class ContratResponse(ContratBase):
    id: int
    cree_le: datetime

    class Config:
        from_attributes = True

# --- Payment Schemas ---
class PaiementBase(BaseModel):
    contrat_id: int
    montant: float
    statut: str # payé | impayé
    date_echeance: date
    date_paiement: Optional[datetime] = None

class PaiementCreate(PaiementBase):
    pass

class PaiementResponse(PaiementBase):
    id: int
    cree_le: datetime

    class Config:
        from_attributes = True

# --- Appointment Schemas ---
class RendezVousBase(BaseModel):
    locataire_id: int
    chambre_id: int
    date_heure: datetime
    statut: str # en_attente | confirmé | annulé

class RendezVousCreate(RendezVousBase):
    pass

class RendezVousResponse(RendezVousBase):
    id: int
    cree_le: datetime

    class Config:
        from_attributes = True

# --- Media Schemas ---
class MediaBase(BaseModel):
    chambre_id: int
    url: str
    type: str # photo | video
    description: Optional[str] = None

class MediaCreate(MediaBase):
    pass

class MediaResponse(MediaBase):
    id: int
    cree_le: datetime

    class Config:
        from_attributes = True

# --- Problem Schemas ---
class ProblemeBase(BaseModel):
    contrat_id: int
    signale_par: int # utilisateur_id
    description: str
    type: str # plomberie | electricite | autre
    responsable: str # locataire | proprietaire
    resolu: bool = False

class ProblemeCreate(ProblemeBase):
    pass

class ProblemeResponse(ProblemeBase):
    id: int
    cree_le: datetime

    class Config:
        from_attributes = True

# --- Authentication Schemas (Added to resolve ImportError) ---
class Token(BaseModel):
    """
    Schema for the authentication token returned after successful login.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for the data contained within the authentication token.
    Typically used to store the username or user ID.
    """
    username: Optional[str] = None # You might want to use EmailStr or an int ID here depending on your token content
