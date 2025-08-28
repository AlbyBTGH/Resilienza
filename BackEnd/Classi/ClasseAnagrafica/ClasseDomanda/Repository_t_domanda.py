# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDomanda/Repository_t_domanda.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine # Assicurati che engine sia importabile da qui
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda
from Classi.ClasseAnagrafica.ClasseDriver.Domain_t_driver import TDriver # Necessario per le query con join
import logging
from datetime import datetime

class Repository_t_domanda:
    """
    Gestisce le operazioni di accesso ai dati per la tabella 'domande'.
    """
    def __init__(self):
        """
        Inizializza la sessione per le operazioni sul database.
        """
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        """
        Crea la tabella 'domande' se non esiste.
        """
        session = self.Session()
        try:
            TDomanda.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'domande' creata o già esistente (secondo il modello TDomanda).")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'domande': {str(e)}")
            raise
        finally:
            session.close()

    def get_all(self, id_driver_filter: int = None):
        """
        Recupera tutte le domande con i dettagli del driver associato.
        Supporta il filtro opzionale per id_driver.
        """
        session = self.Session()
        try:
            # Esegue un join tra TDomanda e TDriver per ottenere la descrizione del driver
            query = session.query(TDomanda, TDriver).join(TDriver)
            if id_driver_filter is not None:
                query = query.filter(TDomanda.id_driver == id_driver_filter)

            domande = query.all()
            
            result = []
            for domanda_obj, driver_obj in domande:
                result.append({
                    'id': domanda_obj.id,
                    'descr': domanda_obj.descr,
                    'id_driver': domanda_obj.id_driver,
                    'driver_descr': driver_obj.descr, # Descrizione del driver
                    'data_ultima_modifica': domanda_obj.data_ultima_modifica.isoformat() if domanda_obj.data_ultima_modifica else None,
                    'modificato_da': domanda_obj.modificato_da
                })
            logging.info(f"Recuperate {len(result)} domande.")
            return result
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero di tutte le domande: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_id(self, domanda_id: int):
        """
        Recupera una domanda tramite ID con i dettagli del driver.
        """
        session = self.Session()
        try:
            domanda = session.query(TDomanda, TDriver).join(TDriver).filter(TDomanda.id == domanda_id).first()
            if domanda:
                domanda_obj, driver_obj = domanda
                return {
                    'id': domanda_obj.id,
                    'descr': domanda_obj.descr,
                    'id_driver': domanda_obj.id_driver,
                    'driver_descr': driver_obj.descr,
                    'data_ultima_modifica': domanda_obj.data_ultima_modifica.isoformat() if domanda_obj.data_ultima_modifica else None,
                    'modificato_da': domanda_obj.modificato_da
                }
            return None
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero domanda {domanda_id}: {str(e)}")
            raise
        finally:
            session.close()

    def create(self, descr: str, id_driver: int, creato_da: str = 'system'):
        """
        Crea una nuova domanda nel database.
        """
        session = self.Session()
        try:
            new_domanda = TDomanda(
                descr=descr,
                id_driver=id_driver,
                modificato_da=creato_da,
                data_ultima_modifica=datetime.now()
            )
            session.add(new_domanda)
            session.commit()
            session.refresh(new_domanda)
            logging.info(f"Domanda '{new_domanda.descr[:30]}...' creata con successo (ID: {new_domanda.id}).")
            return {
                'id': new_domanda.id,
                'descr': new_domanda.descr,
                'id_driver': new_domanda.id_driver,
                'data_ultima_modifica': new_domanda.data_ultima_modifica.isoformat() if new_domanda.data_ultima_modifica else None,
                'modificato_da': new_domanda.modificato_da
            }
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nella creazione della domanda: {str(e)}")
            raise
        finally:
            session.close()

    def update(self, domanda_id: int, descr: str, id_driver: int, modificato_da: str = 'system'):
        """
        Aggiorna una domanda esistente nel database.
        """
        session = self.Session()
        try:
            domanda = session.query(TDomanda).filter_by(id=domanda_id).first()
            if domanda:
                domanda.descr = descr
                domanda.id_driver = id_driver
                domanda.data_ultima_modifica = datetime.now()
                domanda.modificato_da = modificato_da
                session.commit()
                session.refresh(domanda)
                logging.info(f"Domanda {domanda_id} aggiornata.")
                return {
                    'id': domanda.id,
                    'descr': domanda.descr,
                    'id_driver': domanda.id_driver,
                    'data_ultima_modifica': domanda.data_ultima_modifica.isoformat() if domanda.data_ultima_modifica else None,
                    'modificato_da': domanda.modificato_da
                }
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'aggiornamento della domanda {domanda_id}: {str(e)}")
            raise
        finally:
            session.close()

    def delete(self, domanda_id: int):
        """
        Elimina fisicamente una domanda dal database.
        """
        session = self.Session()
        try:
            domanda = session.query(TDomanda).filter_by(id=domanda_id).first()
            if domanda:
                session.delete(domanda)
                session.commit()
                logging.info(f"Domanda {domanda_id} eliminata fisicamente.")
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'eliminazione della domanda {domanda_id}: {str(e)}")
            raise
        finally:
            session.close()

