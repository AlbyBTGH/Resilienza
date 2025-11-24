# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseDomanda/Service_t_domanda.py

import logging
from Classi.ClasseAnagrafica.ClasseDomanda.Repository_t_domanda import Repository_t_domanda
from Classi.ClasseAnagrafica.ClasseDriver.Repository_t_driver import Repository_t_driver # Per verificare l'esistenza del driver
from Classi.ClasseAnagrafica.ClasseGruppoRisposta.Repository_t_gruppo_risposta import Repository_t_gruppo_risposta 
from datetime import datetime
# Import TDomanda per il metodo save_domanda_from_bulk
from Classi.ClasseAnagrafica.ClasseDomanda.Domain_t_domanda import TDomanda 

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
        self.gruppo_risposta_repository = Repository_t_gruppo_risposta() 

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

    # Firma corretta: 5 argomenti totali (self + 4 espliciti)
    def create_domanda(self, descr: str, id_driver: int, id_gruppo_risposta: int = None, creato_da: str = 'system'):
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
            
            # LOGICA DI VALIDAZIONE GRUPPO RISPOSTA (corretta)
            if id_gruppo_risposta is not None and id_gruppo_risposta != 0:
                gruppo_risposta_exists = self.gruppo_risposta_repository.get_by_id(id_gruppo_risposta)
                if not gruppo_risposta_exists:
                    return {"error": "Gruppo Risposta specificato non esistente."}, 400

            # Chiama il Repository con i 4 campi necessari
            new_domanda_result = self.repository.create(descr, id_driver, creato_da, id_gruppo_risposta) 
            
            # 💡 CORREZIONE: Estrae il dizionario in caso il Repository restituisca una tupla (dizionario, stato)
            if isinstance(new_domanda_result, tuple) and len(new_domanda_result) > 0:
                new_domanda = new_domanda_result[0]
            else:
                new_domanda = new_domanda_result
            
            # Logging più sicuro per evitare l'errore se l'ID non è presente
            domanda_id_log = new_domanda.get('id', 'N/D') if isinstance(new_domanda, dict) else 'N/D'
            logging.info(f"Nuova domanda creata con successo (ID: {domanda_id_log}).")
            
            # Ritorna il dizionario creato e lo stato HTTP 201
            return new_domanda, 201

        except Exception as e:
            logging.error(f"Errore nel servizio durante la creazione della domanda: {str(e)}")
            return {"error": f"Errore durante la creazione della domanda: {str(e)}"}, 500

    # Firma corretta: 6 argomenti totali (self + 5 espliciti)
    def update_domanda(self, domanda_id: int, descr: str, id_driver: int, id_gruppo_risposta: int = None, modificato_da: str = 'system'):
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
            
            # LOGICA DI VALIDAZIONE GRUPPO RISPOSTA (corretta)
            if id_gruppo_risposta is not None and id_gruppo_risposta != 0:
                gruppo_risposta_exists = self.gruppo_risposta_repository.get_by_id(id_gruppo_risposta)
                if not gruppo_risposta_exists:
                    return {"error": "Gruppo Risposta specificato non esistente."}, 400

        
            # Chiama il Repository con i 5 campi necessari
            updated_domanda = self.repository.update(domanda_id, descr, id_driver, id_gruppo_risposta, modificato_da) 
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

    # Metodo ausiliario: TDomanda importato in cima per farlo funzionare
    def save_domanda_from_bulk(self, id_driver, descr, modificato_da):
        """
        Salva una domanda nel database da un'operazione di caricamento massivo.
        Questo metodo è obsoleto o richiede una revisione per usare il repository.
        """
        try:
            # Assumendo che self.repository abbia un metodo add_domanda
            domanda = TDomanda(
                id_driver=id_driver,
                descr=descr,
                modificato_da=modificato_da
            )
            # Ho corretto la variabile da self.repo a self.repository, assumendo l'errore.
            # Se la tua classe TDomanda non accetta questo formato, dovrai usare il metodo create del repository.
            return self.repository.add_domanda(domanda) 
        except Exception as e:
            raise e