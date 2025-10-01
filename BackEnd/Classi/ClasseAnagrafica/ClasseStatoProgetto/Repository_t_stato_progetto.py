# Classi/ClasseAnagrafica/ClasseStatoProgetto/Repository_t_stato_progetto.py
# -*- coding: utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from .Domain_t_stato_progetto import TStatoProgetto

class Repository_t_stato_progetto:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        try:
            TStatoProgetto.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'STATI_PROGETTO' creata o gia esistente.")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'STATI_PROGETTO': {str(e)}")
            raise

    def get_all(self):
        session = self.Session()
        try:
            stati_db = session.query(TStatoProgetto).all()
            return stati_db
        except SQLAlchemyError as e:
            logging.error(f"Errore nel repository durante il recupero degli stati progetto: {str(e)}")
            return []
        finally:
            session.close()
