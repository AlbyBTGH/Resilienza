# Classi/ClasseQuestionario/Domain_t_questionario.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Table
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
from datetime import datetime

# Definizione della tabella di unione per la relazione molti-a-molti
t_questionario_domande = Table(
    'domande_questionario',
    Base.metadata,
    Column('id_questionario', Integer, ForeignKey('questionario.id')),
    Column('id_domanda', Integer, ForeignKey('domande.ID')) 
)

class TQuestionario(Base):
    __tablename__ = 'questionario'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    descr = Column('descr', String(255), nullable=False)
    data_creazione = Column('data_creazione', TIMESTAMP, default=datetime.now)
    creato_da = Column('creato_da', String(100))
    data_ultima_modifica = Column('data_ultima_modifica', TIMESTAMP, onupdate=datetime.now)
    modificato_da = Column('modificato_da', String(100))

    # Relazione molti-a-molti con la tabella TDomanda tramite la tabella di unione
    domande = relationship('TDomanda', secondary=t_questionario_domande, backref='questionari', lazy='subquery')