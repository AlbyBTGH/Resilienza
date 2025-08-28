# Classi/ClasseUtenti/Classe_t_ruolo/Domain_t_ruolo.py
from sqlalchemy import Column, String, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TRuolo(Base):
    __tablename__ = 't_ruolo'

    ID = Column(Integer, autoincrement=True, primary_key=True)
    public_id = Column(String(255), nullable=True, unique=True)
    DESCR = Column(String(50), nullable=True)

    funzionalita_utenti_rel = relationship(
        "TFunzionalitaUtente",
        back_populates="ruolo_rel",
        primaryjoin="TRuolo.ID == TFunzionalitaUtente.fkIdRuolo" # <-- CORREZIONE QUI: da fkRuolo a fkIdRuolo
    )

    utenti_rel = relationship(
        "TUtenti",
        back_populates="ruolo_rel", 
        primaryjoin="TRuolo.ID == TUtenti.fkIdRuolo"
    )

    def __repr__(self):
        return f"<TRuolo(ID={self.ID}, DESCR='{self.DESCR}')>"
