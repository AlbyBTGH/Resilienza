# Classi/ClasseAnagrafica/ClasseProgetto/Repository_t_progetto.py
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

    def create_table_if_not_exists(self):
        session = self.Session()
        try:
            TProgetto.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'PROGETTO' creata o gia esistente (secondo il modello TProgetto).")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'PROGETTO': {str(e)}")
            raise
        finally:
            session.close()

    def get_all(self):
        session = self.Session()
        try:
            # Carica in modo anticipato la relazione con la tabella ambito
            progetti_db = session.query(TProgetto).options(
                joinedload(TProgetto.ambito),
                joinedload(TProgetto.stato_progetto)
            ).all()
            return progetti_db
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nel repository durante il recupero di tutti i progetti: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_id(self, progetto_id: int):
        session = self.Session()
        try:
            progetto = session.query(TProgetto).options(
                joinedload(TProgetto.ambito),
                joinedload(TProgetto.stato_progetto)
            ).filter_by(id=progetto_id).first()
            return progetto
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nel repository durante il recupero del progetto {progetto_id}: {str(e)}")
            raise
        finally:
            session.close()

    def create(self, descr, dt_inizio, dt_fine, id_stato, id_ambito, ref_cliente, modificato_da):
        session = self.Session()
        try:
            new_progetto = TProgetto(
                descr=descr,
                dt_inizio=dt_inizio,
                dt_fine=dt_fine,
                id_stato=id_stato,
                id_ambito=id_ambito,
                ref_cliente=ref_cliente,
                modificato_da=modificato_da
            )
            session.add(new_progetto)
            session.commit()
            session.refresh(new_progetto)
            return new_progetto
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nella creazione del progetto: {str(e)}")
            raise
        finally:
            session.close()

    def update(self, progetto_id: int, descr, dt_inizio, dt_fine, id_stato, id_ambito, ref_cliente, modificato_da):
        session = self.Session()
        try:
            progetto = session.query(TProgetto).filter_by(id=progetto_id).first()
            if progetto:
                progetto.descr = descr
                progetto.dt_inizio = dt_inizio
                progetto.dt_fine = dt_fine
                progetto.id_stato = id_stato
                progetto.id_ambito = id_ambito
                progetto.ref_cliente = ref_cliente
                progetto.modificato_da = modificato_da
                session.commit()
                session.refresh(progetto)

                # Carica le relazioni per evitare il Lazy Loading dopo la chiusura della sessione
                progetto = session.query(TProgetto).options(
                    joinedload(TProgetto.ambito),
                    joinedload(TProgetto.stato_progetto)
                ).filter_by(id=progetto_id).first()

                logging.info(f"Progetto {progetto_id} aggiornato.")
                return progetto
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'aggiornamento del progetto {progetto_id}: {str(e)}")
            raise
        finally:
            session.close()

    def delete(self, progetto_id: int):
        session = self.Session()
        try:
            progetto = session.query(TProgetto).filter_by(id=progetto_id).first()
            if progetto:
                session.delete(progetto)
                session.commit()
                logging.info(f"Progetto {progetto_id} eliminato fisicamente.")
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'eliminazione del progetto {progetto_id}: {str(e)}")
            raise
        finally:
            session.close()