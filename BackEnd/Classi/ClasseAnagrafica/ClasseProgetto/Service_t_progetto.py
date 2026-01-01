# -*- coding: utf-8 -*-
import logging
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from Classi.ClasseAnagrafica.ClasseProgetto.Repository_t_progetto import Repository_t_progetto
from Classi.ClasseAnagrafica.ClasseProgetto.Domain_t_progetto import TProgetto
from Classi.ClasseProgettoAnalista.Domain_progetto_analisti import TProgettoAnalisti

class Service_t_progetto:
    def __init__(self):
        self.repository = Repository_t_progetto()

    # NUOVO METODO HELPER PER MAPPARE L'ASSOCIAZIONE ANALISTA
    def _to_analista_association_dict(self, associazione: TProgettoAnalisti):
        """Mappa un oggetto TProgettoAnalisti in un dizionario serializzabile."""
        if not associazione:
            return None
        
        analista = associazione.analista_ref # Ottiene l'oggetto TUtenti
        
        return {
            'id_analista': associazione.ID_UTENTE,
            'nome_cognome_analista': f"{analista.nome} {analista.cognome}" if analista else 'Analista Sconosciuto',
            'data_associazione': associazione.DATA_ASSOCIAZIONE.isoformat() if associazione.DATA_ASSOCIAZIONE else None,
            'data_fine_associazione': associazione.DATA_FINE_ASSOCIAZIONE.isoformat() if associazione.DATA_FINE_ASSOCIAZIONE else None,
            'attivo': associazione.DATA_FINE_ASSOCIAZIONE is None
        }

    # ===============================
    # 🔹 Funzione di utilità per il mapping
    # ===============================
    def _to_dict(self, progetto: TProgetto):
        if progetto is None:
            return None

        cliente_descr = 'N/A'
        if progetto.cliente and hasattr(progetto.cliente, 'ragione_sociale'):
            cliente_descr = progetto.cliente.ragione_sociale

        # --- ⭐ NUOVA LOGICA ANALISTI ---
        associazioni_mapped = []
        analisti_correnti = []
        analisti_ids_attivi = []

        # Estrazione e mapping dei dati
        if hasattr(progetto, 'analisti_associazioni') and progetto.analisti_associazioni is not None:
            # 1. Mappa tutte le associazioni (attive e non)
            associazioni_mapped = [
                self._to_analista_association_dict(assoc) 
                for assoc in progetto.analisti_associazioni
            ]
            
            # 2. Filtra solo le associazioni ATTIVE
            analisti_correnti = [
                assoc for assoc in associazioni_mapped if assoc.get('attivo', False)
            ]
            
            # 3. Estrai solo gli ID degli analisti attivi
            analisti_ids_attivi = [a['id_analista'] for a in analisti_correnti]

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
            'analisti_associazioni': associazioni_mapped,
            'analisti_correnti': analisti_correnti,
            'analisti_ids_attivi': analisti_ids_attivi
        }

    # ===============================
    # GET: Tutti i progetti
    # ===============================
    def get_all_progetti(self):
        try:
            progetti_db = self.repository.get_all()
            return [self._to_dict(p) for p in progetti_db]
        except Exception as e:
            logging.error(f"Errore nel servizio get_all_progetti: {str(e)}")
            raise

    # ===============================
    # GET: Progetto singolo per ID
    # ===============================
    def get_progetto_by_id(self, progetto_id): # <-- Probabilmente questa è la riga 96, o 97 è subito dopo
        try:
            progetto_orm = self.repository.get_by_id(progetto_id)
            
            if not progetto_orm: # <-- Tutti i blocchi 'if', 'for', 'try', 'def' necessitano di indentazione successiva
                return {"error": "Progetto non trovato."}, 404
            
            progetto_data = self._to_dict(progetto_orm) 
            
            # ... Logica di filtraggio analisti ...
            analisti_attivi_ids = []
            if hasattr(progetto_orm, 'analisti_associazioni') and progetto_orm.analisti_associazioni:
                for assoc in progetto_orm.analisti_associazioni:
                    if assoc.DATA_FINE_ASSOCIAZIONE is None: 
                        analisti_attivi_ids.append(assoc.ID_UTENTE)
                        
            progetto_data['analisti_attivi_ids'] = analisti_attivi_ids 
            
            return progetto_data, 200
            
        except Exception as e:
            # Assicurati che 'logging.error' sia indentato correttamente qui
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
        
    # ===============================
    # FUNZIONE CHIAMATA DAL CONTROLLER
    # ===============================
    def sync_analisti_progetto(self, progetto_id: int, analisti_ids: list, modificato_da: str):
        try:
            # 1. Verifica esistenza progetto (consigliato prima di operare sul DB)
            if not self.repository.get_by_id(progetto_id):
                return {"error": "Progetto non trovato."}, 404
                
            # 2. Chiama il Repository per eseguire l'operazione transazionale
            # Il Repository deve avere un metodo con lo stesso nome, o un nome simile
            self.repository.sincronizza_analisti_progetto(progetto_id, analisti_ids, modificato_da)
            
            logging.info(f"Sincronizzazione analisti per Progetto ID {progetto_id} completata.")
            return {"message": "Associazioni analisti sincronizzate con successo."}, 200
            
        except Exception as e:
            logging.error(f"Errore Service sync_analisti_progetto per Progetto ID {progetto_id}: {str(e)}")
            return {"error": f"Errore interno del server durante la sincronizzazione: {str(e)}"}, 500