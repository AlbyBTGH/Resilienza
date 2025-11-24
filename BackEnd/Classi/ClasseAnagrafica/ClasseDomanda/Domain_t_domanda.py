# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDomanda/Domain_t_domanda.py

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base # Assicurati che Base sia importabile da qui
from Classi.ClasseAnagrafica.ClasseDriver.Domain_t_driver import TDriver # Importa TDriver
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Domain_t_gruppo_risposta import TGruppoRisposta 
from datetime import datetime

class TDomanda(Base):
    """
    Modello SQLAlchemy per la tabella 'domande'.
    Rappresenta una domanda associata a un driver specifico.
    """
    __tablename__ = 'domande'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR', Text, nullable=False)
    id_driver = Column('ID_DRIVER', Integer, ForeignKey('driver.ID'), nullable=False)
    # NUOVA CHIAVE ESTERNA
    id_gruppo_risposta = Column(
        'ID_GRUPPO_RISPOSTA', 
        Integer, 
        ForeignKey('gruppo_risposta.ID_GRUPPO_RISPOSTA'), 
        nullable=True # O nullable=False se l'associazione è obbligatoria
    )
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)
    modificato_da = Column('MODIFICATO_DA', String(100), nullable=True)

    # Definizione della relazione con TDriver
    # 🚀 FIX CRITICO: Forzatura della chiave esterna per risolvere N/D
    driver_rel = relationship('TDriver', backref='domande', foreign_keys=[id_driver])

    # NUOVA RELAZIONE con TGruppoRisposta
    gruppo_risposta_rel = relationship(
        'TGruppoRisposta', 
        backref='domande', 
        foreign_keys=[id_gruppo_risposta]
    )

    def __repr__(self):
        return f"<TDomanda(id={self.id}, descr='{self.descr}', id_driver={self.id_driver})>"