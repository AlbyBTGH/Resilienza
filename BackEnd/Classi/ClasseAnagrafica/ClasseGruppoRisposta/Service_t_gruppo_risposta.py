# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseGruppoRisposta/Service_t_gruppo_risposta.py

import logging
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Repository_t_gruppo_risposta import Repository_t_gruppo_risposta
from datetime import datetime

class Service_t_gruppo_risposta:
    """
    Fornisce la logica di business per la gestione dei gruppi di risposta.
    """
    def __init__(self):
        """
        Inizializza il repository dei gruppi di risposta.
        """
        self.repository = Repository_t_gruppo_risposta()

    def create_table_if_not_exists(self):
        """
        Crea la tabella 'gruppo_risposta' se non esiste.
        """
        self.repository.create_table_if_not_exists()

    def get_all_gruppi_risposta(self):
        """
        Recupera tutti i gruppi di risposta.
        La gestione degli errori è delegata al Repository (che esegue il 'raise') 
        e al Controller (che gestisce lo status 500).
        """
        # CORREZIONE: Rimosso il try-except che mascherava l'errore
        gruppi = self.repository.get_all()
        logging.info(f"Recuperati {len(gruppi)} gruppi di risposta.")
        return gruppi

    def get_gruppo_risposta_by_id(self, gruppo_id: int):
        """
        Recupera un gruppo di risposta per ID.
        """
        try:
            gruppo = self.repository.get_by_id(gruppo_id)
            return gruppo
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero del gruppo di risposta con ID {gruppo_id}: {str(e)}")
            return None # Scelta di ritornare None in caso di errore di lettura

    def create_gruppo_risposta(self, descr: str, creato_da: str):
        """
        Crea un nuovo gruppo di risposta.
        """
        try:
            if not descr:
                return {"error": "La descrizione è obbligatoria."}, 400

            existing_gruppo = self.repository.get_by_descr(descr)
            if existing_gruppo:
                return {"error": "Un gruppo di risposta con questa descrizione esiste già."}, 409 # Conflict

            new_gruppo = self.repository.create(descr, creato_da)
            logging.info(f"Nuovo gruppo di risposta creato con successo (ID: {new_gruppo['id']}).")
            return new_gruppo, 201 # Created

        except Exception as e:
            logging.error(f"Errore nel servizio durante la creazione del gruppo di risposta: {str(e)}")
            return {"error": f"Errore durante la creazione del gruppo di risposta: {str(e)}"}, 500 # Internal Server Error

    def update_gruppo_risposta(self, gruppo_id: int, descr: str, modificato_da: str = 'system'):
        """
        Aggiorna un gruppo di risposta esistente.
        """
        try:
            existing_gruppo = self.repository.get_by_id(gruppo_id)
            if not existing_gruppo:
                return {"error": "Gruppo di risposta non trovato."}, 404 # Not Found
            
            if not descr:
                return {"error": "La descrizione è obbligatoria."}, 400

            # Verifica unicità della descrizione
            duplicate_gruppo = self.repository.get_by_descr_excluding_self(descr, gruppo_id)
            if duplicate_gruppo:
                return {"error": "Un altro gruppo di risposta con questa descrizione esiste già."}, 409 # Conflict

            updated_gruppo = self.repository.update(gruppo_id, descr, modificato_da)
            logging.info(f"Gruppo di risposta con ID {gruppo_id} aggiornato con successo.")
            return updated_gruppo, 200 # OK

        except Exception as e:
            logging.error(f"Errore nel servizio durante l'aggiornamento del gruppo di risposta con ID {gruppo_id}: {str(e)}")
            return {"error": f"Errore durante l'aggiornamento del gruppo di risposta: {str(e)}"}, 500 # Internal Server Error

    def delete_gruppo_risposta(self, gruppo_id: int):
        """
        Elimina fisicamente un gruppo di risposta dal database.
        """
        try:
            success = self.repository.delete(gruppo_id)
            if success:
                logging.info(f"Gruppo di risposta con ID {gruppo_id} eliminato fisicamente con successo.")
                return {"message": "Gruppo di risposta eliminato con successo."}, 200 # OK
            else:
                logging.warning(f"Tentativo di eliminare gruppo di risposta con ID {gruppo_id} non trovato.")
                return {"error": "Gruppo di risposta non trovato."}, 404 # Not Found
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'eliminazione del gruppo di risposta con ID {gruppo_id}: {str(e)}")
            return {"error": f"Errore durante la cancellazione del gruppo di risposta: {str(e)}"}, 500 # Internal Server Error

    def check_gruppi_risposta_exist(self, gruppi_risposta_ids: list[int]) -> bool:
        """
        Controlla se tutti gli ID di gruppo di risposta forniti esistono nel database.
        """
        try:
            return self.repository.check_gruppi_risposta_exist(gruppi_risposta_ids)
        except Exception as e:
            logging.error(f"Errore nel servizio durante la verifica dell'esistenza dei gruppi di risposta: {str(e)}")
            # Ritorna False se c'è un errore di database.
            return False