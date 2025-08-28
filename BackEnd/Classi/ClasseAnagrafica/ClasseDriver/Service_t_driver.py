# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDriver/Service_t_driver.py

import logging
from Classi.ClasseAnagrafica.ClasseDriver.Repository_t_driver import Repository_t_driver
from Classi.ClasseAnagrafica.ClasseCategoria.Repository_t_categoria import Repository_t_categoria # Per verificare l'esistenza della categoria
from datetime import datetime

class Service_t_driver:
    def __init__(self):
        self.repository = Repository_t_driver()
        self.categoria_repository = Repository_t_categoria() # Per la verifica della categoria

    def create_table_if_not_exists(self):
        """Crea la tabella 'driver' se non esiste."""
        self.repository.create_table_if_not_exists()

    def get_all_drivers(self, id_categoria_filter: int = None):
        """Recupera tutti i driver."""
        try:
            drivers = self.repository.get_all(id_categoria_filter)
            logging.info(f"Recuperati {len(drivers)} driver.")
            return drivers
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero di tutti i driver: {str(e)}")
            return []

    def get_driver_by_id(self, driver_id: int):
        """Recupera un driver tramite ID."""
        try:
            driver = self.repository.get_by_id(driver_id)
            if driver:
                logging.info(f"Recuperato driver con ID: {driver_id}")
            else:
                logging.warning(f"Driver con ID: {driver_id} non trovato.")
            return driver
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero del driver con ID {driver_id}: {str(e)}")
            return None

    def create_driver(self, descr: str, id_categoria: int, creato_da: str = 'system'):
        """Crea un nuovo driver nel database."""
        try:
            if not descr:
                return {"error": "Descrizione è obbligatoria."}, 400

            categoria_exists = self.categoria_repository.get_by_id(id_categoria)
            if not categoria_exists:
                logging.warning(f"Tentativo di creare driver con ID categoria {id_categoria} non esistente.")
                return {"error": "Categoria specificata non esistente."}, 400

            new_driver = self.repository.create(descr, id_categoria, creato_da)
            logging.info(f"Nuovo driver creato con successo (ID: {new_driver['id']}).")
            return new_driver, 201

        except Exception as e:
            logging.error(f"Errore nel servizio durante la creazione del driver: {str(e)}")
            return {"error": f"Errore durante la creazione del driver: {str(e)}"}, 500

    def update_driver(self, driver_id: int, descr: str, id_categoria: int, modificato_da: str = 'system'):
        """Aggiorna un driver esistente nel database."""
        try:
            if not descr:
                return {"error": "Descrizione è obbligatoria."}, 400

            existing_driver = self.repository.get_by_id(driver_id)
            if not existing_driver:
                logging.warning(f"Tentativo di aggiornare driver con ID {driver_id} non trovato.")
                return {"error": "Driver non trovato."}, 404

            categoria_exists = self.categoria_repository.get_by_id(id_categoria)
            if not categoria_exists:
                logging.warning(f"Tentativo di aggiornare driver con ID categoria {id_categoria} non esistente.")
                return {"error": "Categoria specificata non esistente."}, 400

            updated_driver = self.repository.update(driver_id, descr, id_categoria, modificato_da)
            logging.info(f"Driver con ID {driver_id} aggiornato con successo.")
            return updated_driver, 200

        except Exception as e:
            logging.error(f"Errore nel servizio durante l'aggiornamento del driver con ID {driver_id}: {str(e)}")
            return {"error": f"Errore durante l'aggiornamento del driver: {str(e)}"}, 500

    def delete_driver(self, driver_id: int):
        """Elimina fisicamente un driver dal database."""
        try:
            success = self.repository.delete(driver_id)
            if success:
                logging.info(f"Driver con ID {driver_id} eliminato fisicamente con successo.")
                return {"message": "Driver eliminato con successo."}, 200
            else:
                logging.warning(f"Tentativo di eliminare driver con ID {driver_id} non trovato.")
                return {"error": "Driver non trovato."}, 404
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'eliminazione del driver con ID {driver_id}: {str(e)}")
            return {"error": f"Errore durante la cancellazione del driver: {str(e)}"}, 500

