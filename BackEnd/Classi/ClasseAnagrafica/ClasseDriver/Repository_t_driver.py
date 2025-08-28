# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDriver/Repository_t_driver.py

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAnagrafica.ClasseDriver.Domain_t_driver import TDriver
from Classi.ClasseAnagrafica.ClasseCategoria.Domain_t_categoria import TCategoria # Necessario per le query con join
import logging
from datetime import datetime

class Repository_t_driver:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        """Crea la tabella 'driver' se non esiste."""
        session = self.Session()
        try:
            TDriver.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'driver' creata o gi� esistente (secondo il modello TDriver).")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'driver': {str(e)}")
            raise
        finally:
            session.close()

    def get_all(self, id_categoria_filter: int = None):
        """Recupera tutti i driver con i dettagli della categoria associata."""
        session = self.Session()
        try:
            query = session.query(TDriver, TCategoria).join(TCategoria)
            if id_categoria_filter is not None:
                query = query.filter(TDriver.id_categoria == id_categoria_filter)

            drivers = query.all()
            
            result = []
            for driver_obj, categoria_obj in drivers:
                result.append({
                    'id': driver_obj.id,
                    'descr': driver_obj.descr,
                    'id_categoria': driver_obj.id_categoria,
                    'categoria_descr': categoria_obj.descr, # Descrizione della categoria
                    'data_ultima_modifica': driver_obj.data_ultima_modifica.isoformat() if driver_obj.data_ultima_modifica else None,
                    'modificato_da': driver_obj.modificato_da
                })
            logging.info(f"Recuperati {len(result)} driver.")
            return result
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero di tutti i driver: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_id(self, driver_id: int):
        """Recupera un driver tramite ID con i dettagli della categoria."""
        session = self.Session()
        try:
            driver = session.query(TDriver, TCategoria).join(TCategoria).filter(TDriver.id == driver_id).first()
            if driver:
                driver_obj, categoria_obj = driver
                return {
                    'id': driver_obj.id,
                    'descr': driver_obj.descr,
                    'id_categoria': driver_obj.id_categoria,
                    'categoria_descr': categoria_obj.descr,
                    'data_ultima_modifica': driver_obj.data_ultima_modifica.isoformat() if driver_obj.data_ultima_modifica else None,
                    'modificato_da': driver_obj.modificato_da
                }
            return None
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero driver {driver_id}: {str(e)}")
            raise
        finally:
            session.close()

    def create(self, descr: str, id_categoria: int, creato_da: str = 'system'):
        """Crea un nuovo driver nel database."""
        session = self.Session()
        try:
            new_driver = TDriver(
                descr=descr,
                id_categoria=id_categoria,
                modificato_da=creato_da,
                data_ultima_modifica=datetime.now()
            )
            session.add(new_driver)
            session.commit()
            session.refresh(new_driver)
            logging.info(f"Driver '{new_driver.descr}' creato con successo (ID: {new_driver.id}).")
            return {
                'id': new_driver.id,
                'descr': new_driver.descr,
                'id_categoria': new_driver.id_categoria,
                'data_ultima_modifica': new_driver.data_ultima_modifica.isoformat() if new_driver.data_ultima_modifica else None,
                'modificato_da': new_driver.modificato_da
            }
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nella creazione del driver: {str(e)}")
            raise
        finally:
            session.close()

    def update(self, driver_id: int, descr: str, id_categoria: int, modificato_da: str = 'system'):
        """Aggiorna un driver esistente nel database."""
        session = self.Session()
        try:
            driver = session.query(TDriver).filter_by(id=driver_id).first()
            if driver:
                driver.descr = descr
                driver.id_categoria = id_categoria
                driver.data_ultima_modifica = datetime.now()
                driver.modificato_da = modificato_da
                session.commit()
                session.refresh(driver)
                logging.info(f"Driver {driver_id} aggiornato.")
                return {
                    'id': driver.id,
                    'descr': driver.descr,
                    'id_categoria': driver.id_categoria,
                    'data_ultima_modifica': driver.data_ultima_modifica.isoformat() if driver.data_ultima_modifica else None,
                    'modificato_da': driver.modificato_da
                }
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'aggiornamento del driver {driver_id}: {str(e)}")
            raise
        finally:
            session.close()

    def delete(self, driver_id: int):
        """Elimina fisicamente un driver dal database."""
        session = self.Session()
        try:
            driver = session.query(TDriver).filter_by(id=driver_id).first()
            if driver:
                session.delete(driver)
                session.commit()
                logging.info(f"Driver {driver_id} eliminato fisicamente.")
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'eliminazione del driver {driver_id}: {str(e)}")
            raise
        finally:
            session.close()
