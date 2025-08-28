# Classi/ClasseUtenti/Classe_t_funzionalitaUtenti/Domain_t_funzionalitaUtente.py
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

# Non importare TFunzionalita e TRuolo direttamente qui per evitare importazioni circolari.
# Usa stringhe nelle relationship().

class TFunzionalitaUtente(Base):
    __tablename__ = 't_funzionalita_utente' # Ensure table name is correct

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Corrected column name from fkRuolo to fkIdRuolo as per your CREATE TABLE
    fkIdRuolo = Column(Integer, ForeignKey('t_ruolo.ID'), nullable=True) 
    fkFunzionalita = Column(Integer, ForeignKey('t_funzionalita.id'), nullable=True)
    permessi = Column(Boolean, default=False) # Or the correct type for permissions

    # Relationships - using strings to avoid circular imports
    ruolo_rel = relationship("TRuolo", back_populates="funzionalita_utenti_rel")
    funzionalita_rel = relationship("TFunzionalita", back_populates="funzionalita_utente_rel")

    def __repr__(self):
        return f"<TFunzionalitaUtente(id={self.id}, fkIdRuolo={self.fkIdRuolo}, fkFunzionalita={self.fkFunzionalita})>"

