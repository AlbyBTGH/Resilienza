# Classi/Classe_dati_caricamento/Domain_t_dati_caricamento.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..ClasseDB.db_connection import Base

class TDatiCaricamento(Base):
    __tablename__ = 't_dati_caricamento'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    DESCRIZIONE = Column(String(255))
    DATA_CARICAMENTO = Column(DateTime, default=datetime.now)
    UTENTE = Column(String(100))
    NUMERO_RECORD = Column(Integer)
    STATO = Column(String(50)) # 'successo', 'fallito', 'parziale'

    def __init__(self, descrizione, utente, numero_record, stato):
        self.DESCRIZIONE = descrizione
        self.UTENTE = utente
        self.NUMERO_RECORD = numero_record
        self.STATO = stato