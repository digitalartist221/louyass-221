# app/models.py

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # Pour l'horodatage automatique

from .database import Base # Assurez-vous que Base est importé depuis .database

# ... (Vos autres modèles comme User, Maison, Chambre, Contrat, Paiement, RendezVous, Media, Probleme) ...

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    expediteur_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destinataire_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contenu = Column(String, nullable=False)
    date_envoi = Column(DateTime(timezone=True), server_default=func.now()) # Horodatage automatique
    lu = Column(Boolean, default=False) # Pour marquer le message comme lu

    # Relations : un message a un expéditeur et un destinataire
    expediteur = relationship("User", foreign_keys=[expediteur_id], back_populates="messages_envoyes")
    destinataire = relationship("User", foreign_keys=[destinataire_id], back_populates="messages_recus")

# Mettre à jour le modèle User pour inclure les relations de message
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    prenom = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="locataire") # "locataire", "bailleur", "admin"
    is_active = Column(Boolean, default=True)

    maisons = relationship("Maison", back_populates="proprietaire")
    chambres = relationship("Chambre", back_populates="proprietaire") # Les chambres peuvent être propriétés par un bailleur
    contrats_locataire = relationship("Contrat", foreign_keys="[Contrat.locataire_id]", back_populates="locataire")
    contrats_bailleur = relationship("Contrat", foreign_keys="[Contrat.bailleur_id]", back_populates="bailleur") # Si vous avez un champ bailleur_id dans Contrat
    rendez_vous_locataire = relationship("RendezVous", foreign_keys="[RendezVous.locataire_id]", back_populates="locataire")
    problemes_signales = relationship("Probleme", foreign_keys="[Probleme.signale_par]", back_populates="signaleur")

    # NOUVELLES RELATIONS POUR LES MESSAGES
    messages_envoyes = relationship("Message", foreign_keys=[Message.expediteur_id], back_populates="expediteur")
    messages_recus = relationship("Message", foreign_keys=[Message.destinataire_id], back_populates="destinataire")