# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDriver/Domain_t_driver.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from Classi.ClasseAnagrafica.ClasseCategoria.Domain_t_categoria import TCategoria # Importa TCategoria
from datetime import datetime

class TDriver(Base):
    __tablename__ = 'driver'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR', String(255), nullable=False)
    id_categoria = Column('ID_CATEGORIA', Integer, ForeignKey('categoria.ID'), nullable=False)
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)
    modificato_da = Column('MODIFICATO_DA', String(100), nullable=True)

    # Definizione della relazione con TCategoria
    # 'categoria' sar� un attributo su TDriver per accedere ai dettagli della categoria associata
    categoria = relationship('TCategoria', backref='drivers')

    def __repr__(self):
        return f"<TDriver(id={self.id}, descr='{self.descr}', id_categoria={self.id_categoria})>"

