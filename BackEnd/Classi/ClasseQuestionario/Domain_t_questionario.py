# Classi/ClasseQuestionario/Domain_t_questionario.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from Classi.ClasseDB.db_connection import Base
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
from Classi.ClasseProgettoQuestionario.Domain_progetto_questionario import ProgettoQuestionario

# Tabella di unione per la relazione molti-a-molti domande–questionario
t_questionario_domande = Table(
    'domande_questionario',
    Base.metadata,
    Column('id_questionario', Integer, ForeignKey('questionario.ID')),
    Column('id_domanda', Integer, ForeignKey('domande.ID'))
)

class TQuestionario(Base):
    __tablename__ = 'questionario'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR', String(255), nullable=False)
    data_creazione = Column('DATA_CREAZIONE', TIMESTAMP, default=datetime.now)
    creato_da = Column('CREATO_DA', String(100))
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', TIMESTAMP, onupdate=datetime.now)
    modificato_da = Column('MODIFICATO_DA', String(100))

    # Relazione con domande
    domande = relationship(
        'TDomanda',
        secondary=t_questionario_domande,
        backref='questionari',
        lazy='subquery'
    )

    # 🔗 Relazione uno-a-molti con ProgettoQuestionario
    progetti_assoc = relationship(
        "ProgettoQuestionario",
        back_populates="questionario",
        cascade="all, delete-orphan"
    )

    # 🧩 Property per accedere direttamente ai progetti associati
    @property
    def progetti(self):
        """Restituisce la lista dei progetti associati al questionario."""
        return [assoc.progetto for assoc in self.progetti_assoc]

    def __repr__(self):
        return f"<TQuestionario(id={self.id}, descr='{self.descr}')>"