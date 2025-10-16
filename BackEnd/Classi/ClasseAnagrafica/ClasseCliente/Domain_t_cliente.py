# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseCliente/Domain_t_cliente.py

from sqlalchemy import Column, Integer, String, DateTime
from Classi.ClasseDB.db_connection import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class TCliente(Base):
    """
    Modello SQLAlchemy per la tabella 'cliente'.
    Rappresenta un cliente con i dati anagrafici.
    """
    __tablename__ = 'cliente'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    ragione_sociale = Column('RAGIONE_SOCIALE', String(255), nullable=False)
    partita_iva = Column('PARTITA_IVA', String(11), nullable=True, unique=True)
    indirizzo = Column('INDIRIZZO', String(255), nullable=True)
    citta = Column('CITTA', String(100), nullable=True)
    provincia = Column('PROVINCIA', String(2), nullable=True)
    cap = Column('CAP', String(5), nullable=True)
    email = Column('EMAIL', String(255), nullable=True)
    telefono = Column('TELEFONO', String(50), nullable=True)
    
    # Campi di tracciamento
    modificato_da = Column('MODIFICATO_DA', String(100), nullable=True)
    # Default e onupdate gestiti dal database per le timestamp, ma definito qui per consistenza
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)

    # Relazione con Progetto (un cliente ha molti progetti, back_populates 'cliente' in TProgetto)
    progetti = relationship("TProgetto", back_populates="cliente")

    def __repr__(self):
        return f"<TCliente(id={self.id}, ragione_sociale='{self.ragione_sociale}')>"

    def to_dict(self):
        """Converte l'oggetto in un dizionario per la serializzazione JSON."""
        return {
            'id': self.id,
            'ragione_sociale': self.ragione_sociale,
            'partita_iva': self.partita_iva,
            'indirizzo': self.indirizzo,
            'citta': self.citta,
            'provincia': self.provincia,
            'cap': self.cap,
            'email': self.email,
            'telefono': self.telefono,
            'modificato_da': self.modificato_da,
            'data_ultima_modifica': self.data_ultima_modifica.isoformat() if self.data_ultima_modifica else None
        }