# Classi/ClasseAnagrafica/ClasseProgetto/Service_t_progetto.py
# -*- coding: utf-8 -*-
import logging
from Classi.ClasseAnagrafica.ClasseProgetto.Repository_t_progetto import Repository_t_progetto
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from Classi.ClasseAnagrafica.ClasseProgetto.Domain_t_progetto import TProgetto

class Service_t_progetto:
    def __init__(self):
        self.repository = Repository_t_progetto()

    def create_table_if_not_exists(self):
        self.repository.create_table_if_not_exists()
    
    # Metodo helper per convertire un oggetto TProgetto in un dizionario serializzabile
    def _to_dict(self, progetto: TProgetto):
        if progetto is None:
            return None
        return {
            'id': progetto.id,
            'descr': progetto.descr,
            'dt_inizio': progetto.dt_inizio.isoformat() if isinstance(progetto.dt_inizio, date) else progetto.dt_inizio,
            'dt_fine': progetto.dt_fine.isoformat() if isinstance(progetto.dt_fine, date) else progetto.dt_fine,
            'id_stato': progetto.id_stato,
            'stato_descr': progetto.stato_progetto.descr if progetto.stato_progetto else 'N/A', # AGGIUNTO
            'id_ambito': progetto.id_ambito,
            # AGGIORNATO: Aggiunto un controllo esplicito per evitare l'errore se l'ambito non esiste
            'ambito_descr': progetto.ambito.descrizione if progetto.ambito else 'N/A',
            'ref_cliente': progetto.ref_cliente,
            'modificato_da': progetto.modificato_da,
            'data_ultima_modifica': progetto.data_ultima_modifica.isoformat() if isinstance(progetto.data_ultima_modifica, datetime) else progetto.data_ultima_modifica,
        }

    def get_all_progetti(self):
        try:
            progetti = self.repository.get_all()
            logging.info(f"Recuperati {len(progetti)} progetti.")
            # CORRETTO: Converti ogni oggetto TProgetto in un dizionario prima di restituirlo
            return [self._to_dict(p) for p in progetti]
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero di tutti i progetti: {str(e)}")
            return []

    def get_progetto_by_id(self, progetto_id: int):
        try:
            progetto = self.repository.get_by_id(progetto_id)
            if progetto:
                logging.info(f"Recuperato progetto con ID: {progetto_id}")
                return self._to_dict(progetto)
            else:
                logging.warning(f"Progetto con ID: {progetto_id} non trovato.")
            return None
        except Exception as e:
            logging.error(f"Errore nel servizio durante il recupero del progetto con ID {progetto_id}: {str(e)}")
            return None

    def create_progetto(self, descr, dt_inizio, dt_fine, id_stato, id_ambito, ref_cliente, modificato_da):
        try:
            new_progetto = self.repository.create(descr, dt_inizio, dt_fine, id_stato, id_ambito, ref_cliente, modificato_da)
            if new_progetto:
                logging.info(f"Progetto '{new_progetto.descr}' creato con successo con ID: {new_progetto.id}")
                return self._to_dict(new_progetto), 201
            return {"error": "Progetto non creato."}, 500
        except IntegrityError:
            logging.error(f"Violazione di integrità: ID_AMBITO {id_ambito} non esistente.")
            return {"error": "L'ambito selezionato non esiste."}, 409
        except Exception as e:
            logging.error(f"Errore nel servizio durante la creazione del progetto: {str(e)}")
            return {"error": f"Errore durante la creazione del progetto: {str(e)}"}, 500

    def update_progetto(self, progetto_id: int, descr, dt_inizio, dt_fine, id_stato, id_ambito, ref_cliente, modificato_da):
        try:
            updated_progetto = self.repository.update(progetto_id, descr, dt_inizio, dt_fine, id_stato, id_ambito, ref_cliente, modificato_da)
            if updated_progetto:
                logging.info(f"Progetto con ID {progetto_id} aggiornato con successo.")
                return self._to_dict(updated_progetto), 200
            else:
                logging.warning(f"Tentativo di aggiornare progetto con ID {progetto_id} non trovato.")
                return {"error": "Progetto non trovato."}, 404
        except IntegrityError:
            logging.error(f"Violazione di integrità: ID_AMBITO {id_ambito} non esistente.")
            return {"error": "L'ambito selezionato non esiste."}, 409
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'aggiornamento del progetto con ID {progetto_id}: {str(e)}")
            return {"error": f"Errore durante l'aggiornamento del progetto: {str(e)}"}, 500

    def delete_progetto(self, progetto_id: int):
        try:
            success = self.repository.delete(progetto_id)
            if success:
                logging.info(f"Progetto con ID {progetto_id} eliminato fisicamente con successo.")
                return {"message": "Progetto eliminato con successo."}, 200
            else:
                logging.warning(f"Tentativo di eliminare progetto con ID {progetto_id} non trovato.")
                return {"error": "Progetto non trovato."}, 404
        except Exception as e:
            logging.error(f"Errore nel servizio durante l'eliminazione del progetto con ID {progetto_id}: {str(e)}")
            return {"error": f"Errore durante l'eliminazione del progetto: {str(e)}"}, 500