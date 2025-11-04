# File: Classi/ClasseRisposteCliente/Domain_risposta_cliente.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, DateTime, ForeignKey, text, String
from sqlalchemy.orm import relationship
from Classi.ClasseDB.db_connection import Base # Assumendo questo path
from datetime import datetime

class RispostaCliente(Base):
    """
    Modello ORM per la tabella 'risposta_cliente' con i campi di tracciabilità richiesti.
    """
    __tablename__ = 'risposta_cliente'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    
    # Collega alla specifica associazione Domanda-Progetto-Questionario (senza UNIQUE)
    id_progetto_questionario_domanda = Column('ID_PROGETTO_QUESTIONARIO_DOMANDA', Integer, 
                                               ForeignKey('progetto_questionario_domanda.ID'), 
                                               nullable=False)
    
    # Collega all'ID della risposta selezionata
    id_risposta = Column('ID_RISPOSTA', Integer, 
                           ForeignKey('risposta.ID_RISPOSTA'), 
                           nullable=False) 
                           
    # Campo di creazione (popolato solo all'INSERT)
    data_compilazione = Column('DATA_COMPILAZIONE', DateTime, 
                               server_default=text('CURRENT_TIMESTAMP'), nullable=True) 

    # CAMPI DI TRACCIABILITÀ (come da DDL finale)
    modificato_da = Column('MODIFICATO_DA', String(100), nullable=True)
    data_ultima_modifica = Column('DATA_ULTIMA_MODIFICA', DateTime, 
                                 server_default=text('CURRENT_TIMESTAMP'), 
                                 onupdate=text('CURRENT_TIMESTAMP'), # SQLAlchemy gestisce l'aggiornamento
                                 nullable=True) 

    def __init__(self, id_progetto_questionario_domanda, id_risposta, modificato_da):
        self.id_progetto_questionario_domanda = id_progetto_questionario_domanda
        self.id_risposta = id_risposta
        self.modificato_da = modificato_da 
        
    def __repr__(self):
        return (f"<RispostaCliente(id={self.id}, id_pqd={self.id_progetto_questionario_domanda}, "
                f"modificato_da={self.modificato_da})>")