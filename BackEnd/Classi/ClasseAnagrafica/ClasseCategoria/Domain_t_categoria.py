# Classi/ClasseAnagrafica/ClasseCategoria/Domain_t_categoria.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base
from Classi.ClasseAnagrafica.ClasseAmbito.Domain_t_ambito import TAmbito
from datetime import datetime

class TCategoria(Base):
    __tablename__ = 'categoria'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR', String(255), nullable=False)
    tipo_categoria = Column('TIPO_CATEGORIA', String(100), nullable=True) # Aggiunto: TIPO_CATEGORIA
    id_ambito = Column('ID_AMBITO', Integer, ForeignKey('ambito.ID'), nullable=False)
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)
    modificato_da = Column('MODIFICATO_DA', String(100), nullable=True)

    ambito = relationship('TAmbito', backref='categorie')

    def __repr__(self):
        return f"<TCategoria(id={self.id}, descr='{self.descr}', tipo_categoria='{self.tipo_categoria}')>"
