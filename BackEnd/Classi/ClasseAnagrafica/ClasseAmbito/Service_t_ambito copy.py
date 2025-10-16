# BackEnd/Classi/ClasseAnagrafica/ClasseAmbito/Service_t_ambito.py
import logging
from Classi.ClasseAnagrafica.ClasseAmbito.Repository_t_ambito import Repository_t_ambito # CORRETTO: rimosso 'BackEnd.'
from datetime import datetime # Importa datetime per i campi data

class Service_t_ambito:
    def __init__(self):
        self.repository = Repository_t_ambito()

    def create_table_if_not_exists(self):
        """Crea la tabella 'ambito' se non esiste."""
        self.repository.create_table_if_not_exists()

    def get_all_ambiti(self):
        """Recupera tutti gli ambiti."""
        try:
            ambiti = self.repository.get_all()
            logging.info(f"Recuperati {len(ambiti)} ambiti.")
            return ambiti
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero di tutti gli ambiti: {str(e)}")
            return []

    def get_ambito_by_id(self, ambito_id: int):
        """Recupera un ambito tramite ID."""
        try:
            ambito = self.repository.get_by_id(ambito_id)
            if ambito:
                logging.info(f"Recuperato ambito con ID: {ambito_id}")
            else:
                logging.warning(f"Ambito con ID: {ambito_id} non trovato.")
            return ambito
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero dell'ambito con ID {ambito_id}: {str(e)}")
            return None

    def create_ambito(self, codice: str, descrizione: str, note: str = None, modificato_da: str = None):
        """Crea un nuovo ambito, verificando l'unicità del codice."""
        try:
            existing_ambito = self.repository.get_by_codice(codice)
            if existing_ambito:
                logging.warning(f"Tentativo di creare ambito con codice duplicato: {codice}")
                return {"error": "Codice ambito già esistente."}, 409 # Conflict
            
            new_ambito = self.repository.create(codice, descrizione, note, modificato_da)
            logging.info(f"Ambito '{codice}' creato con successo.")
            return new_ambito, 201 # Created
        except Exception as e:
            logging.error(f"Errore nel servizio durante la creazione dell'ambito '{codice}': {str(e)}")
            return {"error": f"Errore durante la creazione dell'ambito: {str(e)}"}, 500 # Internal Server Error

    def update_ambito(self, ambito_id: int, descrizione: str, note: str = None, modificato_da: str = None):
        """Aggiorna la descrizione e le note di un ambito esistente."""
        try:
            ambito = self.repository.get_by_id(ambito_id)
            if not ambito:
                logging.warning(f"Tentativo di aggiornare ambito con ID {ambito_id} non trovato.")
                return {"error": "Ambito non trovato."}, 404 # Not Found
            
            updated_ambito = self.repository.update(ambito_id, descrizione, note, modificato_da)
            logging.info(f"Ambito con ID {ambito_id} aggiornato con successo.")
            return updated_ambito, 200 # OK
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'aggiornamento dell'ambito con ID {ambito_id}: {str(e)}")
            return {"error": f"Errore durante l'aggiornamento dell'ambito: {str(e)}"}, 500 # Internal Server Error

    def delete_ambito(self, ambito_id: int):
        """Elimina fisicamente un ambito dal database."""
        try:
            success = self.repository.delete(ambito_id)
            if success:
                logging.info(f"Ambito con ID {ambito_id} eliminato fisicamente con successo.")
                return {"message": "Ambito eliminato con successo."}, 200 # OK
            else:
                logging.warning(f"Tentativo di eliminare ambito con ID {ambito_id} non trovato.")
                return {"error": "Ambito non trovato."}, 404 # Not Found
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'eliminazione dell'ambito con ID {ambito_id}: {str(e)}")
            return {"error": f"Errore durante la cancellazione dell'ambito: {str(e)}"}, 500 # Internal Server Error

