# Classi/ClasseAnagrafica/ClasseProgetto/Domain_t_progetto.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from datetime import datetime
from Classi.ClasseAnagrafica.ClasseAmbito.Domain_t_ambito import TAmbito
from Classi.ClasseAnagrafica.ClasseStatoProgetto.Domain_t_stato_progetto import TStatoProgetto # Importazione aggiunta

class TProgetto(Base):
    __tablename__ = 'PROGETTO'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR', String(200), nullable=False)
    dt_inizio = Column('DT_INIZIO', Date)
    dt_fine = Column('DT_FINE', Date)
    id_stato = Column('ID_STATO', Integer, ForeignKey('STATI_PROGETTO.ID'))
    id_ambito = Column('ID_AMBITO', Integer, ForeignKey('ambito.ID'))
    ref_cliente = Column('REF_CLIENTE', String(200))
    modificato_da = Column('MODIFICATO_DA', String(100))
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', String(100), default=datetime.now)

    # Relazione con la tabella TAmbito
    ambito = relationship("TAmbito")
    # Aggiungi qui la relazione con TStatoProgetto
    stato_progetto = relationship("TStatoProgetto")
    
    def __repr__(self):
        return f"<TProgetto(id={self.id}, descrizione='{self.descr}', stato_id='{self.id_stato}', ambito_id='{self.id_ambito}')>"