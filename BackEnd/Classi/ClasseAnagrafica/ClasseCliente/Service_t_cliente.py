# -*- coding: utf-8 -*-
# Classi/ClasseAnagrafica/ClasseCliente/Service_t_cliente.py

import logging
from Classi.ClasseAnagrafica.ClasseCliente.Repository_t_cliente import Repository_t_cliente
from Classi.ClasseAnagrafica.ClasseCliente.Domain_t_cliente import TCliente
from sqlalchemy.exc import IntegrityError
from datetime import date, datetime

class Service_t_cliente:
    """
    Fornisce la logica di business per la gestione dell'anagrafica clienti.
    """
    def __init__(self):
        """Inizializza il repository dei clienti."""
        self.repository = Repository_t_cliente()
        logging.basicConfig(level=logging.INFO)

    def create_table_if_not_exists(self):
        """Crea la tabella 'cliente' se non esiste (utile all'avvio)."""
        self.repository.create_table_if_not_exists()
    
    def _to_dict(self, cliente: TCliente) -> dict | None:
        """Metodo helper per convertire un oggetto TCliente in un dizionario serializzabile."""
        if cliente is None:
            return None
        
        # Usa il metodo to_dict definito nel Domain
        return cliente.to_dict()

    def get_all_clienti(self) -> tuple[list[dict], int]:
        """Recupera tutti i clienti e li converte in dizionari."""
        try:
            clienti = self.repository.get_all()
            clienti_dict = [self._to_dict(c) for c in clienti]
            return clienti_dict, 200
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero di tutti i clienti: {str(e)}")
            return {"error": "Errore interno del server durante il recupero dei clienti."}, 500

    def get_cliente_by_id(self, cliente_id: int) -> tuple[dict | None, int]:
        """Recupera un cliente tramite ID e lo converte in dizionario."""
        try:
            cliente = self.repository.get_by_id(cliente_id)
            if cliente:
                return self._to_dict(cliente), 200
            else:
                return {"error": "Cliente non trovato."}, 404
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero del cliente {cliente_id}: {str(e)}")
            return {"error": f"Errore durante il recupero del cliente: {str(e)}"}, 500

    def create_cliente(self, ragione_sociale: str, partita_iva: str | None, indirizzo: str | None, 
                       citta: str | None, provincia: str | None, cap: str | None, 
                       email: str | None, telefono: str | None, creato_da: str) -> tuple[dict, int]:
        """Crea un nuovo cliente nel database."""
        if not ragione_sociale:
            return {"error": "ragione sociale obbligatoria."}, 400

        nuovo_cliente = TCliente(
            ragione_sociale=ragione_sociale,
            partita_iva=partita_iva,
            indirizzo=indirizzo,
            citta=citta,
            provincia=provincia,
            cap=cap,
            email=email,
            telefono=telefono,
            modificato_da=creato_da
        )
        try:
            cliente_salvato = self.repository.create(nuovo_cliente)
            logging.info(f"Cliente '{ragione_sociale}' creato con successo.")
            return self._to_dict(cliente_salvato), 201  # Created
        except IntegrityError as e:
            logging.error(f"Violazione di integrita durante la creazione del cliente: {str(e)}")
            return {"error": "Errore di integrita: Partita IVA o altri campi unici duplicati."}, 409
        except Exception as e:
            logging.error(f"Errore nel servizio durante la creazione del cliente: {str(e)}")
            return {"error": f"Errore durante la creazione del cliente: {str(e)}"}, 500

    def update_cliente(self, cliente_id: int, ragione_sociale: str, partita_iva: str | None, indirizzo: str | None, 
                       citta: str | None, provincia: str | None, cap: str | None, 
                       email: str | None, telefono: str | None, modificato_da: str) -> tuple[dict, int]:
        """Aggiorna un cliente esistente nel database."""
        if not ragione_sociale:
            return {"error": "ragione sociale obbligatoria."}, 400

        data = {
            'ragione_sociale': ragione_sociale,
            'partita_iva': partita_iva,
            'indirizzo': indirizzo,
            'citta': citta,
            'provincia': provincia,
            'cap': cap,
            'email': email,
            'telefono': telefono,
            'modificato_da': modificato_da,
            'data_ultima_modifica': datetime.now()
        }
        
        try:
            cliente_aggiornato = self.repository.update(cliente_id, data)
            if cliente_aggiornato:
                logging.info(f"Cliente con ID {cliente_id} aggiornato con successo.")
                return self._to_dict(cliente_aggiornato), 200 # OK
            else:
                logging.warning(f"Tentativo di aggiornare cliente con ID {cliente_id} non trovato.")
                return {"error": "Cliente non trovato."}, 404 # Not Found
        except IntegrityError as e:
            logging.error(f"Violazione di integrita durante l'aggiornamento del cliente {cliente_id}: {str(e)}")
            return {"error": "Errore di integrita: Partita IVA o altri campi unici duplicati."}, 409
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'aggiornamento del cliente {cliente_id}: {str(e)}")
            return {"error": f"Errore durante l'aggiornamento del cliente: {str(e)}"}, 500

    def delete_cliente(self, cliente_id: int) -> tuple[dict, int]:
        """Elimina fisicamente un cliente dal database."""
        try:
            success = self.repository.delete(cliente_id)
            if success:
                logging.info(f"Cliente con ID {cliente_id} eliminato fisicamente con successo.")
                return {"message": "Cliente eliminato con successo."}, 200 # OK
            else:
                logging.warning(f"Tentativo di eliminare cliente con ID {cliente_id} non trovato.")
                return {"error": "Cliente non trovato."}, 404 # Not Found
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'eliminazione del cliente con ID {cliente_id}: {str(e)}")
            return {"error": f"Errore durante la cancellazione del cliente: {str(e)}"}, 500 # Internal Server Error