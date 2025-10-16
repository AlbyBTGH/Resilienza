# Classi/ClasseAnagrafica/ClasseProgetto/Domain_t_progetto.py
# -*- coding: utf-8 -*-\r
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from datetime import datetime
from Classi.ClasseAnagrafica.ClasseAmbito.Domain_t_ambito import TAmbito
from Classi.ClasseAnagrafica.ClasseStatoProgetto.Domain_t_stato_progetto import TStatoProgetto 
# *** AGGIUNTA CRITICA: Importazione del modello Cliente ***
from Classi.ClasseAnagrafica.ClasseCliente.Domain_t_cliente import TCliente 

class TProgetto(Base):
    __tablename__ = 'PROGETTO'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR', String(200), nullable=False)
    dt_inizio = Column('DT_INIZIO', Date)
    dt_fine = Column('DT_FINE', Date)
    id_stato = Column('ID_STATO', Integer, ForeignKey('STATI_PROGETTO.ID'))
    id_ambito = Column('ID_AMBITO', Integer, ForeignKey('ambito.ID'))
    
    # *** NUOVO CAMPO CLIENTE (Foreign Key) ***
    # La tabella 'cliente' deve avere un ID intero come chiave primaria
    id_cliente = Column('ID_CLIENTE', Integer, ForeignKey('cliente.ID'), nullable=False)
    
    # Mantenuto per non omettere codice precedente, ma non più utilizzato per le query
    ref_cliente = Column('REF_CLIENTE', String(200))
    
    modificato_da = Column('MODIFICATO_DA', String(100))
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', String(100), default=datetime.now)

    # Relazione con la tabella TAmbito
    ambito = relationship("TAmbito", back_populates="progetti") 
    # Relazione con la tabella TStatoProgetto
    stato_progetto = relationship("TStatoProgetto", back_populates="progetti") 
    
    # *** RELAZIONE CRITICA: Nuova relazione con TCliente ***
    # Permette di accedere a progetto.cliente.ragione_sociale
    cliente = relationship("TCliente", back_populates="progetti") 

    def __repr__(self):
        return f"<TProgetto(id={self.id}, descr='{self.descr}', id_cliente={self.id_cliente})>"