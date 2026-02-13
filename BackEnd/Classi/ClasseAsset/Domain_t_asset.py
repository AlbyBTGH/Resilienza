# Classi/ClasseAsset/Domain_t_asset.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base

class TAsset(Base):
    __tablename__ = 'asset'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    descr = Column('DESCR', String(255), nullable=False)
    id_cliente = Column('ID_CLIENTE', Integer, ForeignKey('cliente.ID', ondelete='CASCADE'), nullable=False)
    
    # Valori RID
    r_val = Column('R_VAL', Integer, default=0)
    i_val = Column('I_VAL', Integer, default=0)
    d_val = Column('D_VAL', Integer, default=0)
    
    # V_SCORE è una colonna virtuale gestita lato DB
    v_score = Column('V_SCORE', Integer, server_default=text('0'), nullable=True)
    
    classe_asset = Column('CLASSE_ASSET', String(100))
    id_driver = Column('ID_DRIVER', Integer, ForeignKey('driver.ID', ondelete='SET NULL'))
    stato = Column('STATO', String(50), default='DA_MAPPARE')
    
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    modificato_da = Column('MODIFICATO_DA', String(100))

    # Relazioni
    # Assumi che esistano le classi TCliente e TDriver
    driver = relationship("TDriver", backref="assets")

    def __repr__(self):
        return f"<TAsset(id={self.id}, descr='{self.descr}', v_score={self.v_score})>"