# BackEnd/Classi/ClasseAnagrafica/ClasseAmbito/Domain_t_ambito.py
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from datetime import datetime # AGGIUNTO: Importa la classe datetime

class TAmbito(Base):
    __tablename__ = 'ambito' # CAMBIATO: ora si riferisce alla tua tabella 'ambito'

    id = Column('ID', Integer, primary_key=True, autoincrement=True) # CAMBIATO: Mappato a 'ID'
    codice = Column('ACRONIMO', String(50), unique=True, nullable=False) # CAMBIATO: Mappato a 'ACRONIMO'
    descrizione = Column('DESCR', String(255), nullable=False) # CAMBIATO: Mappato a 'DESCR'
    # Rimosso: dataCancellazione
    note = Column('NOTE', Text, nullable=True) # AGGIUNTO: Mappato a 'NOTE'
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, default=datetime.now, onupdate=datetime.now, nullable=True) # AGGIUNTO
    modificato_da = Column('MODIFICATO_DA', String(100), nullable=True) # AGGIUNTO

    # NUOVO: Relazione uno-a-molti: un Ambito ha molti Progetti.
    # Il parametro "TProgetto" è il nome della classe del modello progetto.
    # back_populates="ambito" indica che sul lato TProgetto l'attributo si chiama 'ambito'.
    progetti = relationship("TProgetto", back_populates="ambito")

    def __repr__(self):
        return f"<TAmbito(id={self.id}, acronimo='{self.codice}', descrizione='{self.descrizione}')>"

