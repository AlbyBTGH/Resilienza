# -*- coding: utf-8 -*-
# Classi/ClasseProgettoAnalista/Domain_progetto_analisti.py 

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base # Percorso della tua Base Class
from datetime import datetime

# Funzione helper per la conversione datetime
def to_iso(dt):
    """Converte un oggetto datetime in stringa ISO 8601, gestendo i valori None."""
    return dt.isoformat() if dt else None

class TProgettoAnalisti(Base):
    """
    Modello SQLAlchemy per la tabella di associazione 'PROGETTO_ANALISTI'.
    """
    __tablename__ = 'PROGETTO_ANALISTI'
    
    # Colonne mappate in MAIUSCOLO
    ID = Column('ID', Integer, primary_key=True, autoincrement=True)
    
    # Chiavi Esterne
    ID_PROGETTO = Column('ID_PROGETTO', Integer, ForeignKey('progetto.ID'), nullable=False)
    ID_UTENTE = Column('ID_UTENTE', Integer, ForeignKey('t_utenti.id'), nullable=False) 
    
    # Colonne aggiuntive per la gestione logica
    DATA_ASSOCIAZIONE = Column('DATA_ASSOCIAZIONE', DateTime, default=datetime.now)
    DATA_FINE_ASSOCIAZIONE = Column('DATA_FINE_ASSOCIAZIONE', DateTime, nullable=True)

    # Relazioni (Association Object Pattern)
    # L'argomento della relationship deve essere il nome della classe, non il path
    progetto_ref = relationship("TProgetto", back_populates="analisti_associazioni")
    analista_ref = relationship("TUtenti", back_populates="progetti_associazioni")
    
    def to_dict(self):
        """Restituisce la rappresentazione in dizionario."""
        return {
            'id': self.ID,
            'id_progetto': self.ID_PROGETTO,
            'id_utente': self.ID_UTENTE,
            'data_associazione': to_iso(self.DATA_ASSOCIAZIONE),
            'data_fine_associazione': to_iso(self.DATA_FINE_ASSOCIAZIONE),
        }