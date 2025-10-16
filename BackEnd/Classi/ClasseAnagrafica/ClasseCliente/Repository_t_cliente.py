# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseCliente/Repository_t_cliente.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAnagrafica.ClasseCliente.Domain_t_cliente import TCliente
import logging

class Repository_t_cliente:
    """
    Gestisce le operazioni di accesso ai dati (CRUD) per la tabella 'cliente'.
    """
    def __init__(self):
        """Inizializza la sessione per le operazioni sul database."""
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        """Crea la tabella 'cliente' se non esiste."""
        session = self.Session()
        try:
            # Creazione esplicita della tabella
            TCliente.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'cliente' creata o gia esistente.")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'cliente': {str(e)}")
            raise
        finally:
            session.close()

    def get_by_id(self, cliente_id: int) -> TCliente | None:
        """Recupera un cliente tramite ID."""
        session = self.Session()
        try:
            cliente = session.query(TCliente).filter(TCliente.id == cliente_id).first()
            return cliente
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero del cliente con ID {cliente_id}: {str(e)}")
            raise
        finally:
            session.close()

    def get_all(self) -> list[TCliente]:
        """Recupera tutti i clienti."""
        session = self.Session()
        try:
            clienti = session.query(TCliente).all()
            return clienti
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero di tutti i clienti: {str(e)}")
            raise
        finally:
            session.close()

    # *NOTA: Per l'integrazione con Progetto, per ora bastano i metodi di lettura e creazione della tabella.*
    # I metodi CRUD completi (create, update, delete) andrebbero aggiunti per la gestione completa dell'anagrafica.
