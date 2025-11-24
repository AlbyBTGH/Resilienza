# File: Classi/ClasseCorrettive/Domain_correttiva.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, DateTime, ForeignKey, text, String, Date, Enum, Boolean, Text
from Classi.ClasseDB.db_connection import Base 
from datetime import datetime

class Correttiva(Base):
    """
    Modello ORM per la tabella 'CORRETTIVA'.
    """
    __tablename__ = 'CORRETTIVA'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    
    # Chiave esterna che lega alla domanda istanziata
    id_progetto_questionario_domanda = Column('ID_PROGETTO_QUESTIONARIO_DOMANDA', Integer, 
                                               ForeignKey('progetto_questionario_domanda.ID'), 
                                               nullable=False)
    
    descrizione_correttiva = Column('DESCRIZIONE_CORRETTIVA', Text, nullable=False)
    responsabile = Column('RESPONSABILE', String(100), nullable=True)
    data_inserimento = Column('DATA_INSERIMENTO', DateTime, server_default=text('CURRENT_TIMESTAMP')) 
    
    data_scadenza = Column('DATA_SCADENZA', Date, nullable=False)
    data_effettiva_intervento = Column('DATA_EFFETTIVA_INTERVENTO', Date, nullable=True)
    
    stato = Column('STATO', Enum('Aperta', 'In Corso', 'Completata', 'Pending', 'Annullata'), 
                    nullable=False, default='Aperta')
    
    costo = Column('COSTO', Boolean, default=False) 
    note = Column('NOTE', Text, nullable=True)

    # CAMPI DI TRACCIABILITÀ
    modificato_da = Column('MODIFICATO_DA', String(100), nullable=True)
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, 
                                 server_default=text('CURRENT_TIMESTAMP'), 
                                 onupdate=text('CURRENT_TIMESTAMP'), 
                                 nullable=True) 
    
    def __init__(self, id_pqd, descrizione, responsabile, data_scadenza, costo, nome_utente_autore, 
                 data_effettiva_intervento=None, stato='Aperta', note=None): 
        self.id_progetto_questionario_domanda = id_pqd
        self.descrizione_correttiva = descrizione
        self.responsabile = responsabile
        self.data_scadenza = data_scadenza
        self.costo = costo
        self.modificato_da = nome_utente_autore 
        self.data_effettiva_intervento = data_effettiva_intervento
        self.stato = stato
        self.note = note

    def __repr__(self):
        return f"<Correttiva(id={self.id}, id_pqd={self.id_progetto_questionario_domanda}, stato={self.stato})>"