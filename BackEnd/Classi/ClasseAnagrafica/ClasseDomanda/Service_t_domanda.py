# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDomanda/Service_t_domanda.py

import logging
from Classi.ClasseAnagrafica.ClasseDomanda.Repository_t_domanda import Repository_t_domanda
from Classi.ClasseAnagrafica.ClasseDriver.Repository_t_driver import Repository_t_driver # Per verificare l'esistenza del driver
from datetime import datetime

class Service_t_domanda:
    """
    Fornisce la logica di business per la gestione delle domande.
    """
    def __init__(self):
        """
        Inizializza il repository delle domande e il repository dei driver per le validazioni.
        """
        self.repository = Repository_t_domanda()
        self.driver_repository = Repository_t_driver() # Per la verifica del driver

    def create_table_if_not_exists(self):
        """
        Crea la tabella 'domande' se non esiste.
        """
        self.repository.create_table_if_not_exists()

    def get_all_domande(self, id_driver_filter: int = None):
        """
        Recupera tutte le domande, con opzione di filtro per ID del driver.
        """
        try:
            domande = self.repository.get_all(id_driver_filter)
            logging.info(f"Recuperate {len(domande)} domande.")
            return domande
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero di tutte le domande: {str(e)}")
            return []

    def get_domanda_by_id(self, domanda_id: int):
        """
        Recupera una domanda tramite ID.
        """
        try:
            domanda = self.repository.get_by_id(domanda_id)
            if domanda:
                logging.info(f"Recuperata domanda con ID: {domanda_id}")
            else:
                logging.warning(f"Domanda con ID: {domanda_id} non trovata.")
            return domanda
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero della domanda con ID {domanda_id}: {str(e)}")
            return None

    def create_domanda(self, descr: str, id_driver: int, creato_da: str = 'system'):
        """
        Crea una nuova domanda nel database.
        Valida l'esistenza del driver associato.
        """
        try:
            if not descr:
                return {"error": "La descrizione è obbligatoria."}, 400

            # Verifica che il driver esista
            driver_exists = self.driver_repository.get_by_id(id_driver)
            if not driver_exists:
                logging.warning(f"Tentativo di creare domanda con ID driver {id_driver} non esistente.")
                return {"error": "Driver specificato non esistente."}, 400

            new_domanda = self.repository.create(descr, id_driver, creato_da)
            logging.info(f"Nuova domanda creata con successo (ID: {new_domanda['id']}).")
            return new_domanda, 201

        except Exception as e:
            logging.error(f"Errore nel servizio durante la creazione della domanda: {str(e)}")
            return {"error": f"Errore durante la creazione della domanda: {str(e)}"}, 500

    def update_domanda(self, domanda_id: int, descr: str, id_driver: int, modificato_da: str = 'system'):
        """
        Aggiorna una domanda esistente nel database.
        Valida l'esistenza della domanda e del driver associato.
        """
        try:
            if not descr:
                return {"error": "La descrizione è obbligatoria."}, 400

            # Verifica che la domanda esista
            existing_domanda = self.repository.get_by_id(domanda_id)
            if not existing_domanda:
                logging.warning(f"Tentativo di aggiornare domanda con ID {domanda_id} non trovata.")
                return {"error": "Domanda non trovata."}, 404

            # Verifica che il driver esista
            driver_exists = self.driver_repository.get_by_id(id_driver)
            if not driver_exists:
                logging.warning(f"Tentativo di aggiornare domanda con ID driver {id_driver} non esistente.")
                return {"error": "Driver specificato non esistente."}, 400

            updated_domanda = self.repository.update(domanda_id, descr, id_driver, modificato_da)
            logging.info(f"Domanda con ID {domanda_id} aggiornata con successo.")
            return updated_domanda, 200

        except Exception as e:
            logging.error(f"Errore nel servizio durante l'aggiornamento della domanda con ID {domanda_id}: {str(e)}")
            return {"error": f"Errore durante l'aggiornamento della domanda: {str(e)}"}, 500

    def delete_domanda(self, domanda_id: int):
        """
        Elimina fisicamente una domanda dal database.
        """
        try:
            success = self.repository.delete(domanda_id)
            if success:
                logging.info(f"Domanda con ID {domanda_id} eliminata fisicamente con successo.")
                return {"message": "Domanda eliminata con successo."}, 200
            else:
                logging.warning(f"Tentativo di eliminare domanda con ID {domanda_id} non trovata.")
                return {"error": "Domanda non trovata."}, 404
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'eliminazione della domanda con ID {domanda_id}: {str(e)}")
            return {"error": f"Errore durante la cancellazione della domanda: {str(e)}"}, 500

    def save_domanda_from_bulk(self, id_driver, descr, modificato_da):
        """
        Salva una domanda nel database da un'operazione di caricamento massivo.
        """
        try:
            domanda = TDomanda(
                id_driver=id_driver,
                descr=descr,
                data_inserimento=datetime.now(),
                modificato_da=modificato_da
            )
            return self.repo.add_domanda(domanda)
        except Exception as e:
            raise e