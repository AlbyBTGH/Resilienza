# Classi/ClasseUtenti/Classe_t_utenti/Domain_t_utenti.py
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from Classi.ClasseUtenti.Classe_t_ruolo.Domain_t_ruolo import TRuolo
from sqlalchemy.sql import func

class TUtenti(Base):
    __tablename__ = 't_utenti'

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(255), nullable=True)
    username = Column(String(50), nullable=False)
    nome = Column(String(50), nullable=False)
    cognome = Column(String(50), nullable=False)
    fkIdRuolo = Column(Integer, ForeignKey('t_ruolo.ID'), nullable=False)
    attivo = Column(TINYINT(1), default=None)
    data_creazione = Column(DateTime, nullable=True, default=func.now())
    ultimo_accesso = Column(DateTime, nullable=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    token = Column(String(512), default=None)
    expires = Column(DateTime, default=None)

    # Relationship with TRuolo
    ruolo_rel = relationship('TRuolo', back_populates="utenti_rel")

    def __repr__(self):
        return f"<TUtenti(id={self.id}, username='{self.username}', fkIdRuolo={self.fkIdRuolo})>"