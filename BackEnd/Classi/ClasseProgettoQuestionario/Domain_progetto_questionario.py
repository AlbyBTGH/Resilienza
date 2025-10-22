# Classi/ClasseProgettoQuestionario/Domain_progetto_questionario.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Classi.ClasseDB.db_connection import Base

class ProgettoQuestionario(Base):
    __tablename__ = 'progetto_questionario'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    id_progetto = Column('ID_PROGETTO', Integer, ForeignKey('progetto.ID'), nullable=False)
    id_questionario = Column('ID_QUESTIONARIO', Integer, ForeignKey('questionario.ID'), nullable=False)
    data_associazione = Column('DATA_ASSOCIAZIONE', DateTime, default=datetime.now)

    progetto = relationship('TProgetto', back_populates='questionari_assoc')
    questionario = relationship('TQuestionario', back_populates='progetti_assoc')

    # 🔹 Relazione con ProgettoQuestionarioDomanda (solo stringa)
    domande_assoc = relationship(
        "ProgettoQuestionarioDomanda",
        back_populates="progetto_questionario",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<ProgettoQuestionario(progetto={self.id_progetto}, questionario={self.id_questionario})>"