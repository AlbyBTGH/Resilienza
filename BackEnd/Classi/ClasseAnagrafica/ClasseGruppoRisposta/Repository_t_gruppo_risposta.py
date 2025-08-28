# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseGruppoRisposta/Repository_t_gruppo_risposta.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Domain_t_gruppo_risposta import TGruppoRisposta
import logging
from datetime import datetime

class Repository_t_gruppo_risposta:
    """
    Gestisce le operazioni di accesso ai dati per la tabella 'gruppo_risposta'.
    """
    def __init__(self):
        """
        Inizializza la sessione per le operazioni sul database.
        """
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        """
        Crea la tabella 'gruppo_risposta' se non esiste.
        """
        session = self.Session()
        try:
            TGruppoRisposta.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'gruppo_risposta' creata o gi� esistente (secondo il modello TGruppoRisposta).")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'gruppo_risposta': {str(e)}")
            raise
        finally:
            session.close()

    def get_all(self):
        """
        Recupera tutti i gruppi di risposta e li restituisce come lista di dizionari.
        """
        session = self.Session()
        try:
            gruppi_db = session.query(TGruppoRisposta).all()
            gruppi_data = []
            for gruppo in gruppi_db:
                gruppi_data.append({
                    'id': gruppo.id,
                    'descr': gruppo.descr,
                    'data_ultima_modifica': gruppo.data_ultima_modifica.isoformat() if gruppo.data_ultima_modifica else None,
                    'modificato_da': gruppo.modificato_da
                })
            logging.info(f"Recuperati {len(gruppi_data)} gruppi di risposta (come dizionari).")
            return gruppi_data
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero di tutti i gruppi di risposta: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_id(self, gruppo_id: int):
        """
        Recupera un gruppo di risposta tramite ID e lo restituisce come dizionario.
        """
        session = self.Session()
        try:
            gruppo = session.query(TGruppoRisposta).filter_by(id=gruppo_id).first()
            if gruppo:
                return {
                    'id': gruppo.id,
                    'descr': gruppo.descr,
                    'data_ultima_modifica': gruppo.data_ultima_modifica.isoformat() if gruppo.data_ultima_modifica else None,
                    'modificato_da': gruppo.modificato_da
                }
            return None
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero gruppo di risposta {gruppo_id}: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_descr(self, descr: str):
        """
        Recupera un gruppo di risposta tramite descrizione.
        """
        session = self.Session()
        try:
            return session.query(TGruppoRisposta).filter_by(descr=descr).first()
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero gruppo di risposta per descrizione {descr}: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_descr_excluding_self(self, descr: str, exclude_id: int):
        """
        Recupera un gruppo di risposta tramite descrizione, escludendo un ID specifico.
        """
        session = self.Session()
        try:
            return session.query(TGruppoRisposta).filter(TGruppoRisposta.descr == descr, TGruppoRisposta.id != exclude_id).first()
        except SQLAlchemyError as e:
            session.rollback() # Aggiunto rollback in caso di errore
            logging.error(f"Errore nel recupero gruppo di risposta per descrizione {descr} (escludendo {exclude_id}): {str(e)}")
            raise
        finally:
            session.close()

    def create(self, descr: str, creato_da: str = 'system'):
        """
        Crea un nuovo gruppo di risposta nel database.
        """
        session = self.Session()
        try:
            new_gruppo = TGruppoRisposta(
                descr=descr,
                modificato_da=creato_da,
                data_ultima_modifica=datetime.now()
            )
            session.add(new_gruppo)
            session.commit()
            session.refresh(new_gruppo)
            logging.info(f"Gruppo di risposta '{new_gruppo.descr}' creato con successo (ID: {new_gruppo.id}).")
            return {
                'id': new_gruppo.id,
                'descr': new_gruppo.descr,
                'data_ultima_modifica': new_gruppo.data_ultima_modifica.isoformat() if new_gruppo.data_ultima_modifica else None,
                'modificato_da': new_gruppo.modificato_da
            }
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nella creazione del gruppo di risposta: {str(e)}")
            raise
        finally:
            session.close()

    def update(self, gruppo_id: int, descr: str, modificato_da: str = 'system'):
        """
        Aggiorna un gruppo di risposta esistente nel database.
        """
        session = self.Session()
        try:
            gruppo = session.query(TGruppoRisposta).filter_by(id=gruppo_id).first()
            if gruppo:
                gruppo.descr = descr
                gruppo.data_ultima_modifica = datetime.now()
                gruppo.modificato_da = modificato_da
                session.commit()
                session.refresh(gruppo)
                logging.info(f"Gruppo di risposta {gruppo_id} aggiornato.")
                return {
                    'id': gruppo.id,
                    'descr': gruppo.descr,
                    'data_ultima_modifica': gruppo.data_ultima_modifica.isoformat() if gruppo.data_ultima_modifica else None,
                    'modificato_da': gruppo.modificato_da
                }
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'aggiornamento del gruppo di risposta {gruppo_id}: {str(e)}")
            raise
        finally:
            session.close()

    def delete(self, gruppo_id: int):
        """
        Elimina fisicamente un gruppo di risposta dal database.
        """
        session = self.Session()
        try:
            gruppo = session.query(TGruppoRisposta).filter_by(id=gruppo_id).first()
            if gruppo:
                session.delete(gruppo)
                session.commit()
                logging.info(f"Gruppo di risposta {gruppo_id} eliminato fisicamente.")
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'eliminazione del gruppo di risposta {gruppo_id}: {str(e)}")
            raise
        finally:
            session.close()
