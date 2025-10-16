# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseGruppoRisposta/Domain_t_gruppo_risposta.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from datetime import datetime
# Importazione necessaria per la relazione molti-a-molti (non toccare)
from Classi.ClasseAnagrafica.ClasseRisposta.Domain_t_risposta import gruppo_risposta_risposta 

# Funzione helper per la conversione datetime
def to_iso(dt):
    """Converte un oggetto datetime in stringa ISO 8601, gestendo i valori None."""
    return dt.isoformat() if dt else None

class TGruppoRisposta(Base):
    """
    Modello SQLAlchemy per la tabella 'gruppo_risposta'.
    """
    __tablename__ = 'gruppo_risposta'

    id = Column('ID_GRUPPO_RISPOSTA', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR_GRUPPO_RISPOSTA', String(100), nullable=False)
    modificato_da = Column('MODIFICATO_DA', String(100), nullable=True)
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)

    # Relazione molti-a-molti: un TGruppoRisposta ha molte risposte.
    risposte = relationship("TRisposta", secondary=gruppo_risposta_risposta, back_populates="gruppi_risposta")

    def to_dict(self):
        """
        Restituisce la rappresentazione in dizionario escludendo le relazioni 
        e convertendo i tipi datetime in stringhe.
        """
        return {
            'id': self.id,
            'descr': self.descr,
            'modificato_da': self.modificato_da,
            # Conversione esplicita di datetime in stringa (CORREZIONE CHIAVE)
            'data_ultima_modifica': to_iso(self.data_ultima_modifica),
        }

    def __repr__(self):
        return f"<TGruppoRisposta(id={self.id}, descr='{self.descr}')>"