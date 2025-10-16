# -*- coding: utf-8 -*-
import logging
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from Classi.ClasseAnagrafica.ClasseProgetto.Repository_t_progetto import Repository_t_progetto
from Classi.ClasseAnagrafica.ClasseProgetto.Domain_t_progetto import TProgetto


class Service_t_progetto:
    def __init__(self):
        self.repository = Repository_t_progetto()

    # ===============================
    # 🔹 Funzione di utilità per il mapping
    # ===============================
    def _to_dict(self, progetto: TProgetto):
        if progetto is None:
            return None

        cliente_descr = 'N/A'
        if progetto.cliente and hasattr(progetto.cliente, 'ragione_sociale'):
            cliente_descr = progetto.cliente.ragione_sociale

        return {
            'id': progetto.id,
            'descr': progetto.descr,
            'dt_inizio': progetto.dt_inizio.isoformat() if isinstance(progetto.dt_inizio, date) else progetto.dt_inizio,
            'dt_fine': progetto.dt_fine.isoformat() if isinstance(progetto.dt_fine, date) else progetto.dt_fine,
            'id_stato': progetto.id_stato,
            'stato_descr': progetto.stato_progetto.descr if progetto.stato_progetto else 'N/A',
            'id_ambito': progetto.id_ambito,
            'ambito_descr': progetto.ambito.descrizione if progetto.ambito else 'N/A',
            'id_cliente': progetto.id_cliente,
            'cliente_descr': cliente_descr,
            'ref_cliente': progetto.ref_cliente,
            'modificato_da': progetto.modificato_da,
            'data_ultima_modifica': (
                progetto.data_ultima_modifica.isoformat() if progetto.data_ultima_modifica else None
            ),
        }

    # ===============================
    # 🔹 GET: Tutti i progetti
    # ===============================
    def get_all_progetti(self):
        try:
            progetti_db = self.repository.get_all()
            return [self._to_dict(p) for p in progetti_db]
        except Exception as e:
            logging.error(f"Errore nel servizio get_all_progetti: {str(e)}")
            raise

    # ===============================
    # 🔹 GET: Progetto singolo per ID
    # ===============================
    def get_progetto_by_id(self, progetto_id):
        """
        Restituisce i dettagli di un singolo progetto tramite ID.
        """
        try:
            progetto = self.repository.get_by_id(progetto_id)
            if not progetto:
                return {"error": "Progetto non trovato."}, 404
            return self._to_dict(progetto), 200
        except Exception as e:
            logging.error(f"Errore nel servizio get_progetto_by_id({progetto_id}): {str(e)}")
            return {"error": "Errore interno del server"}, 500

    # ===============================
    # 🔹 POST: Creazione nuovo progetto
    # ===============================
    def create_progetto(self, descr, dt_inizio, dt_fine, id_stato, id_ambito, id_cliente, ref_cliente, creato_da):
        try:
            # Conversione date da stringa a oggetto date
            if dt_inizio and isinstance(dt_inizio, str):
                dt_inizio = datetime.strptime(dt_inizio, "%Y-%m-%d").date()
            if dt_fine and isinstance(dt_fine, str):
                dt_fine = datetime.strptime(dt_fine, "%Y-%m-%d").date()

            nuovo = self.repository.create(
                descr, dt_inizio, dt_fine, id_stato, id_ambito, id_cliente, ref_cliente, creato_da
            )
            logging.info(f"Progetto {nuovo.id} creato con successo.")
            return self._to_dict(nuovo), 201

        except IntegrityError:
            return {"error": "Violazione di integrità su Ambito, Stato o Cliente."}, 409
        except Exception as e:
            logging.error(f"Errore create_progetto: {str(e)}")
            return {"error": str(e)}, 500

    # ===============================
    # 🔹 PUT: Aggiornamento progetto
    # ===============================
    def update_progetto(self, progetto_id, descr, dt_inizio, dt_fine, id_stato, id_ambito, id_cliente, ref_cliente, modificato_da):
        try:
            if dt_inizio and isinstance(dt_inizio, str):
                dt_inizio = datetime.strptime(dt_inizio, "%Y-%m-%d").date()
            if dt_fine and isinstance(dt_fine, str):
                dt_fine = datetime.strptime(dt_fine, "%Y-%m-%d").date()

            updated = self.repository.update(
                progetto_id, descr, dt_inizio, dt_fine, id_stato, id_ambito, id_cliente, ref_cliente, modificato_da
            )
            if updated:
                return self._to_dict(updated), 200
            return {"error": "Progetto non trovato."}, 404

        except IntegrityError:
            return {"error": "Violazione di integrità su Ambito, Stato o Cliente."}, 409
        except Exception as e:
            logging.error(f"Errore update_progetto: {str(e)}")
            return {"error": str(e)}, 500

    # ===============================
    # 🔹 DELETE: Eliminazione progetto
    # ===============================
    def delete_progetto(self, progetto_id):
        try:
            success = self.repository.delete(progetto_id)
            if success:
                return {"message": "Progetto eliminato."}, 200
            return {"error": "Progetto non trovato."}, 404
        except Exception as e:
            logging.error(f"Errore delete_progetto: {str(e)}")
            return {"error": str(e)}, 500