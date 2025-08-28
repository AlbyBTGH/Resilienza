# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseGruppoRisposta/Domain_t_gruppo_risposta.py

from sqlalchemy import Column, Integer, String, DateTime
from Classi.ClasseDB.db_connection import Base
from datetime import datetime

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

    def __repr__(self):
        return f"<TGruppoRisposta(id={self.id}, descr='{self.descr}')>"