# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAnagrafica.ClasseProgetto.Domain_t_progetto import TProgetto
import logging
from datetime import datetime 
from Classi.ClasseProgettoAnalista.Domain_progetto_analisti import TProgettoAnalisti 

class Repository_t_progetto:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    # ====================================================================
    # NUOVO METODO HELPER PER LA SINCRONIZZAZIONE ANALISTI
    # (Logica centralizzata per la cancellazione logica o creazione)
    # ====================================================================
    def _sync_analisti_associazioni(self, session, progetto: TProgetto, nuovi_analisti_ids: list[int], modificato_da: str):
        """
        Sincronizza le associazioni degli analisti:
        1. Disattiva le associazioni esistenti che non sono nella nuova lista.
        2. Attiva o crea le associazioni richieste.
        """
        
        # Converte i nuovi ID in interi e li mette in un set per operazioni veloci
        nuovi_analisti_ids = {int(id) for id in nuovi_analisti_ids if id is not None}
        
        # Set di ID attuali ATTIVI
        analisti_attuali_ids = {assoc.ID_UTENTE for assoc in progetto.analisti_associazioni if assoc.DATA_FINE_ASSOCIAZIONE is None}
        
        # 1. Disattiva (Logica Delete): Analisti esistenti NON nella nuova lista
        analisti_da_rimuovere = analisti_attuali_ids.difference(nuovi_analisti_ids)
        
        for assoc in progetto.analisti_associazioni:
            # Se l'analista è da rimuovere e l'associazione è ancora attiva
            if assoc.ID_UTENTE in analisti_da_rimuovere and assoc.DATA_FINE_ASSOCIAZIONE is None:
                # Imposta la data di fine associazione (cancellazione logica)
                assoc.DATA_FINE_ASSOCIAZIONE = datetime.now()
                logging.info(f"Analista ID {assoc.ID_UTENTE} rimosso logicamente dal Progetto ID {progetto.id}.")

        # 2. Attiva o Crea: Analisti nella nuova lista che non sono attivi
        analisti_da_aggiungere_o_riattivare = nuovi_analisti_ids.difference(analisti_attuali_ids)
        
        for analista_id in analisti_da_aggiungere_o_riattivare:
            # Cerca se esiste un'associazione precedente (per riattivare)
            associazione_esistente = next(
                (assoc for assoc in progetto.analisti_associazioni if assoc.ID_UTENTE == analista_id), 
                None
            )
            
            if associazione_esistente:
                # Riattivazione: resetta la data di fine
                associazione_esistente.DATA_FINE_ASSOCIAZIONE = None
                associazione_esistente.DATA_ASSOCIAZIONE = datetime.now() 
                logging.info(f"Analista ID {analista_id} riattivato per il Progetto ID {progetto.id}.")
            else:
                # Nuova Associazione: Crea un nuovo oggetto TProgettoAnalisti
                nuova_associazione = TProgettoAnalisti(
                    ID_UTENTE=analista_id,
                    DATA_ASSOCIAZIONE=datetime.now(),
                    DATA_FINE_ASSOCIAZIONE=None
                )
                # Aggiunge il nuovo oggetto alla collezione della relazione
                progetto.analisti_associazioni.append(nuova_associazione)
                logging.info(f"Nuova associazione Analista ID {analista_id} a Progetto ID {progetto.id} creata.")


    # ===============================
    # 🔹 Recupera tutti i progetti
    # ===============================
    def get_all(self):
        session = self.Session()
        try:
            progetti = session.query(TProgetto).options(
                joinedload(TProgetto.ambito),
                joinedload(TProgetto.stato_progetto),
                joinedload(TProgetto.cliente),
                joinedload(TProgetto.analisti_associazioni).joinedload(TProgettoAnalisti.analista_ref)
            ).all()
            return progetti
        except SQLAlchemyError as e:
            logging.error(f"Errore get_all(): {str(e)}")
            raise
        finally:
            session.close()

    # ===============================
    # 🔹 Recupera un progetto per ID
    # ===============================
    def get_by_id(self, progetto_id):
        session = self.Session()
        try:
            progetto = session.query(TProgetto).options(
                joinedload(TProgetto.ambito),
                joinedload(TProgetto.stato_progetto),
                joinedload(TProgetto.cliente),
                joinedload(TProgetto.analisti_associazioni).joinedload(TProgettoAnalisti.analista_ref)
            ).filter_by(id=progetto_id).first()
            return progetto
        except SQLAlchemyError as e:
            logging.error(f"Errore get_by_id({progetto_id}): {str(e)}")
            raise
        finally:
            session.close()

    # ===============================
    # 🔹 Crea un nuovo progetto
    # ===============================
    def create(self, descr, dt_inizio, dt_fine, id_stato, id_ambito, id_cliente, ref_cliente, creato_da):
        session = self.Session()
        try:
            nuovo = TProgetto(
                descr=descr,
                dt_inizio=dt_inizio,
                dt_fine=dt_fine,
                id_stato=id_stato,
                id_ambito=id_ambito,
                id_cliente=id_cliente,
                ref_cliente=ref_cliente,
                modificato_da=creato_da,
            )
            session.add(nuovo)
            session.commit()
            session.refresh(nuovo)

            # Ricarico l’oggetto con le relazioni caricate
            progetto_caricato = session.query(TProgetto).options(
                joinedload(TProgetto.ambito),
                joinedload(TProgetto.stato_progetto),
                joinedload(TProgetto.cliente),
                joinedload(TProgetto.analisti_associazioni).joinedload(TProgettoAnalisti.analista_ref)
            ).filter_by(id=nuovo.id).first()

            logging.info(f"Progetto {progetto_caricato.id} creato nel repository.")
            return progetto_caricato
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore create(): {str(e)}")
            raise
        finally:
            session.close()

    # ===============================
    # 🔹 Aggiorna un progetto esistente
    # ===============================
    def update(self, progetto_id, descr, dt_inizio, dt_fine, id_stato, id_ambito, id_cliente, ref_cliente, modificato_da):
        session = self.Session()
        try:
            progetto = session.query(TProgetto).filter_by(id=progetto_id).first()
            if not progetto:
                logging.warning(f"Tentativo di aggiornare progetto inesistente (ID: {progetto_id})")
                return None

            progetto.descr = descr
            progetto.dt_inizio = dt_inizio
            progetto.dt_fine = dt_fine
            progetto.id_stato = id_stato
            progetto.id_ambito = id_ambito
            progetto.id_cliente = id_cliente
            progetto.ref_cliente = ref_cliente
            progetto.modificato_da = modificato_da

            session.commit()

            progetto_caricato = session.query(TProgetto).options(
                joinedload(TProgetto.ambito),
                joinedload(TProgetto.stato_progetto),
                joinedload(TProgetto.cliente),
                joinedload(TProgetto.analisti_associazioni).joinedload(TProgettoAnalisti.analista_ref)
            ).filter_by(id=progetto_id).first()

            logging.info(f"Progetto {progetto_id} aggiornato con successo.")
            return progetto_caricato
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore update({progetto_id}): {str(e)}")
            raise
        finally:
            session.close()

    # ===============================
    # NUOVO METODO: Sincronizza Analisti (Per la Modal)
    # ===============================
    def sincronizza_analisti_progetto(self, progetto_id: int, analisti_ids: list[int], modificato_da: str) -> TProgetto | None:
        """
        Metodo dedicato per l'aggiunta/rimozione logica degli analisti 
        dal progetto, chiamato dalla nuova Modal.
        """
        session = self.Session()
        try:
            # Carica il progetto con le sue associazioni analista attuali e passate
            progetto = session.query(TProgetto).options(
                joinedload(TProgetto.analisti_associazioni)
            ).filter_by(id=progetto_id).first()

            if not progetto:
                logging.warning(f"Tentativo di sincronizzare analisti su progetto inesistente (ID: {progetto_id})")
                return None

            # Sincronizza solo la relazione analisti
            self._sync_analisti_associazioni(session, progetto, analisti_ids, modificato_da)
            
            # Aggiorna il campo di modifica sul progetto principale
            progetto.modificato_da = modificato_da
            progetto.data_ultima_modifica = datetime.now() 

            session.commit()
            
            # Ricarica l'oggetto con tutte le relazioni per il ritorno
            progetto_caricato = self.get_by_id(progetto_id)
            
            logging.info(f"Analisti sincronizzati per il Progetto {progetto_id}.")
            return progetto_caricato

        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore sync_analisti({progetto_id}): {str(e)}")
            raise
        finally:
            session.close()


    # ===============================
    # 🔹 Elimina un progetto
    # ===============================
    def delete(self, progetto_id):
        session = self.Session()
        try:
            # La clausola cascade="all, delete-orphan" sui Domain gestirà l'eliminazione 
            # delle righe in PROGETTO_ANALISTI associate a questo progetto.
            progetto = session.query(TProgetto).filter_by(id=progetto_id).first()
            if not progetto:
                logging.warning(f"Tentativo di eliminare progetto inesistente (ID: {progetto_id})")
                return False

            session.delete(progetto)
            session.commit()
            logging.info(f"Progetto {progetto_id} eliminato con successo.")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore delete({progetto_id}): {str(e)}")
            raise
        finally:
            session.close()