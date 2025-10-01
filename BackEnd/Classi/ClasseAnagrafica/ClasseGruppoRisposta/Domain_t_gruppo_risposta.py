# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseGruppoRisposta/Domain_t_gruppo_risposta.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from datetime import datetime
from Classi.ClasseAnagrafica.ClasseRisposta.Domain_t_risposta import gruppo_risposta_risposta

class TGruppoRisposta(Base):
    """
    Modello SQLAlchemy per la tabella 'gruppo_risposta'.
    Rappresenta un gruppo di risposte.
    """
    __tablename__ = 'gruppo_risposta'

    id = Column('ID_GRUPPO_RISPOSTA', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR_GRUPPO_RISPOSTA', String(100), nullable=False)
    modificato_da = Column('MODIFICATO_DA', String(100), nullable=True)
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)

    # Relazione molti-a-molti: un TGruppoRisposta ha molte risposte.
    # Usa la tabella di associazione 'gruppo_risposta_risposta' come ponte.
    risposte = relationship("TRisposta", secondary=gruppo_risposta_risposta, back_populates="gruppi_risposta")

    def __repr__(self):
        return f"<TGruppoRisposta(id={self.id}, descr='{self.descr}')>"