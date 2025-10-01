# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseRisposta/Domain_t_risposta.py

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric, Table
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from datetime import datetime

# Definizione della tabella di associazione
gruppo_risposta_risposta = Table(
    'gruppo_risposta_risposta',
    Base.metadata,
    Column('ID_GRUPPO_RISPOSTA', Integer, ForeignKey('gruppo_risposta.ID_GRUPPO_RISPOSTA')),
    Column('ID_RISPOSTA', Integer, ForeignKey('risposta.ID_RISPOSTA'))
)

class TRisposta(Base):
    """
    Modello SQLAlchemy per la tabella 'risposta'.
    Rappresenta una singola risposta che può appartenere a più gruppi.
    """
    __tablename__ = 'risposta'

    id = Column('ID_RISPOSTA', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR_RISPOSTA', Text, nullable=False)
    modificato_da = Column('MODIFICATO_DA', String(100), nullable=True)
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)
    peso = Column('PESO', Numeric(10, 2), default=0.0, nullable=True)

    # Relazione molti-a-molti: una Risposta può avere molti Gruppi
    gruppi_risposta = relationship("TGruppoRisposta", secondary=gruppo_risposta_risposta, back_populates="risposte")

    def __repr__(self):
        return f"<TRisposta(id={self.id}, descr='{self.descr}', peso='{self.peso}')>"