# File: Classi/ClassePunteggi/Domain_progetto_questionario_punteggio.py
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, DateTime, ForeignKey, text, Numeric
# Assumendo che Base sia importato dal tuo file di connessione al database
from Classi.ClasseDB.db_connection import Base 

class ProgettoQuestionarioPunteggio(Base):
    """
    Modello ORM per la tabella 'progetto_questionario_punteggio'.
    """
    __tablename__ = 'progetto_questionario_punteggio'

    id = Column('ID', Integer, primary_key=True, autoincrement=True)
    
    # Chiavi Esterne (collegate alle rispettive tabelle)
    id_progetto = Column('ID_PROGETTO', Integer, ForeignKey('progetto.ID'), nullable=False)
    id_questionario = Column('ID_QUESTIONARIO', Integer, ForeignKey('questionario.ID'), nullable=False)
    id_cliente = Column('ID_CLIENTE', Integer, ForeignKey('cliente.ID'), nullable=False)
    id_progetto_questionario = Column('ID_PROGETTO_QUESTIONARIO', Integer, 
                                        ForeignKey('progetto_questionario.ID'), nullable=False)
    id_categoria = Column('ID_CATEGORIA', Integer, ForeignKey('categoria.ID'), nullable=False)
    
    # Campo Dati (il risultato del calcolo)
    peso_totale = Column('PESO_TOTALE', Numeric(10, 2), nullable=False)
    
    # Campo Data di Chiusura
    data_chiusura = Column('DATA_CHIUSURA', DateTime, 
                           server_default=text('CURRENT_TIMESTAMP'), nullable=True)

    def __repr__(self):
        return (f"<PQP(id={self.id}, "
                f"pq_id={self.id_progetto_questionario}, "
                f"cat_id={self.id_categoria}, "
                f"peso={self.peso_totale})>")