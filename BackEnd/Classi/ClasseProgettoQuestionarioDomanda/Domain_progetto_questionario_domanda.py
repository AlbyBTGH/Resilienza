# Classi\ClasseProgettoQuestionarioDomanda\Domain_progetto_questionario_domanda.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class ProgettoQuestionarioDomanda(Base):
    __tablename__ = 'progetto_questionario_domanda'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    id_progetto_questionario = Column('ID_PROGETTO_QUESTIONARIO', Integer, ForeignKey('progetto_questionario.ID'), nullable=False)
    id_domanda = Column('ID_DOMANDA', Integer, ForeignKey('domande.ID'), nullable=False)
    id_gruppo_risposta = Column('ID_GRUPPO_RISPOSTA', Integer, ForeignKey('gruppo_risposta.ID_GRUPPO_RISPOSTA'))

    progetto_questionario = relationship("ProgettoQuestionario", back_populates="domande_assoc")

    def __repr__(self):
        return f"<ProgettoQuestionarioDomanda(id={self.id}, id_domanda={self.id_domanda})>"