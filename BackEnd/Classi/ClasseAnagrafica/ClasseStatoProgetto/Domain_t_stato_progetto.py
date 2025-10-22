# Classi/ClasseAnagrafica/ClasseStatoProgetto/Domain_t_stato_progetto.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship 
from Classi.ClasseDB.db_connection import Base
from datetime import datetime

class TStatoProgetto(Base):
    __tablename__ = 'stati_progetto'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR', String(255), nullable=False)
    nota = Column('NOTA', Text, nullable=True)
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, default=datetime.now, onupdate=datetime.now)
    modificato_da = Column('MODIFICATO_DA', String(100))

    # Relazione inversa corretta
    progetti = relationship("TProgetto", back_populates="stato_progetto")

    def __repr__(self):
        return f"<TStatoProgetto(id={self.id}, descrizione='{self.descr}')>"
