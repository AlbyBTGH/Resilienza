# Classi/ClasseAnagrafica/ClasseProgetto/Domain_t_progetto.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Classi.ClasseDB.db_connection import Base
from Classi.ClasseAnagrafica.ClasseAmbito.Domain_t_ambito import TAmbito
from Classi.ClasseAnagrafica.ClasseStatoProgetto.Domain_t_stato_progetto import TStatoProgetto
from Classi.ClasseAnagrafica.ClasseCliente.Domain_t_cliente import TCliente
from Classi.ClasseProgettoQuestionario.Domain_progetto_questionario import ProgettoQuestionario

class TProgetto(Base):
    __tablename__ = 'progetto'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR', String(200), nullable=False)
    dt_inizio = Column('DT_INIZIO', Date)
    dt_fine = Column('DT_FINE', Date)
    id_stato = Column('ID_STATO', Integer, ForeignKey('stati_progetto.ID'), nullable=True)
    id_ambito = Column('ID_AMBITO', Integer, ForeignKey('ambito.ID'), nullable=True)
    id_cliente = Column('ID_CLIENTE', Integer, ForeignKey('cliente.ID'), nullable=False)
    ref_cliente = Column('REF_CLIENTE', String(200))
    modificato_da = Column('MODIFICATO_DA', String(100))
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, default=datetime.now, onupdate=datetime.now)

    # Relazioni
    ambito = relationship("TAmbito", back_populates="progetti")
    stato_progetto = relationship("TStatoProgetto", back_populates="progetti")
    cliente = relationship("TCliente", back_populates="progetti")

    # Relazione uno-a-molti con ProgettoQuestionario
    questionari_assoc = relationship(
        "ProgettoQuestionario",
        back_populates="progetto",
        cascade="all, delete-orphan"
    )

    # 🧩 Property per accedere ai questionari direttamente
    @property
    def questionari(self):
        """Restituisce la lista di questionari associati al progetto."""
        return [assoc.questionario for assoc in self.questionari_assoc]

    def __repr__(self):
        return f"<TProgetto(id={self.id}, descr='{self.descr}', id_cliente={self.id_cliente})>"