# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDomanda/Domain_t_domanda.py

from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base # Assicurati che Base sia importabile da qui
from Classi.ClasseAnagrafica.ClasseDriver.Domain_t_driver import TDriver # Importa TDriver
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
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)
    modificato_da = Column('MODIFICATO_DA', String(100), nullable=True)

    # Definizione della relazione con TDriver
    # 'driver_rel' sarà un attributo su TDomanda per accedere ai dettagli del driver associato
    # backref='domande' creerà un attributo 'domande' su TDriver per accedere alle domande associate
    driver_rel = relationship('TDriver', backref='domande')

    def __repr__(self):
        """
        Rappresentazione stringa dell'oggetto TDomanda.
        """
        return f"<TDomanda(id={self.id}, descr='{self.descr[:30]}...', id_driver={self.id_driver})>"