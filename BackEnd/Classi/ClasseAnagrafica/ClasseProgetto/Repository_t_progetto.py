# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAnagrafica.ClasseProgetto.Domain_t_progetto import TProgetto
import logging


class Repository_t_progetto:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    # ===============================
    # 🔹 Recupera tutti i progetti
    # ===============================
    def get_all(self):
        session = self.Session()
        try:
            progetti = session.query(TProgetto).options(
                joinedload(TProgetto.ambito),
                joinedload(TProgetto.stato_progetto),
                joinedload(TProgetto.cliente)
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
                joinedload(TProgetto.cliente)
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
                joinedload(TProgetto.cliente)
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
                joinedload(TProgetto.cliente)
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
    # 🔹 Elimina un progetto
    # ===============================
    def delete(self, progetto_id):
        session = self.Session()
        try:
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