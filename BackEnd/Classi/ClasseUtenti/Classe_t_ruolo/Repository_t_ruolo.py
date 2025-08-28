# Classi/ClasseUtenti/Classe_t_ruolo/Repository_t_ruolo.py
# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseUtenti.Classe_t_ruolo.Domain_t_ruolo import TRuolo
from werkzeug.exceptions import NotFound
import logging
import uuid

class Repository_t_ruolo:

    def __init__(self) -> None:
        self.SessionLocal = sessionmaker(bind=engine)

    def create_table_if_not_exists(self):
        """Crea la tabella t_ruolo se non esiste gi."""
        session = self.SessionLocal()
        try:
            TRuolo.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 't_ruolo' creata o gi esistente.")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 't_ruolo': {str(e)}")
            raise
        finally:
            session.close()

    def create(self, desc_ruolo):
        session = self.SessionLocal()
        try:
            new_ruolo = TRuolo(public_id=str(uuid.uuid4()), DESCR=desc_ruolo)
            session.add(new_ruolo)
            session.commit()
            session.refresh(new_ruolo)
            logging.info(f"DEBUG: create - Ruolo '{desc_ruolo}' creato con successo. ID: {new_ruolo.ID}")
            return new_ruolo
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"ERRORE: create - Error creating ruolo '{desc_ruolo}': {e}")
            return None
        finally:
            session.close()

    def get_by_id(self, id_ruolo):
        session = self.SessionLocal()
        try:
            print(f"DEBUG: get_by_id - Cercando ruolo con ID: {id_ruolo}")
            ruolo = session.query(TRuolo).filter_by(ID=id_ruolo).first()
            if ruolo:
                print(f"DEBUG: get_by_id - Trovato ruolo: {ruolo.DESCR}, ID: {ruolo.ID}")
            else:
                print(f"DEBUG: get_by_id - Nessun ruolo trovato per ID: {id_ruolo}")
            return ruolo
        finally:
            session.close()

    def get_by_public_id(self, public_id):
        session = self.SessionLocal()
        try:
            print(f"DEBUG: get_by_public_id - Cercando ruolo con public_id: {public_id}")
            ruolo = session.query(TRuolo).filter_by(public_id=public_id).first()
            if ruolo:
                print(f"DEBUG: get_by_public_id - Trovato ruolo: {ruolo.DESCR}, public_id: {ruolo.public_id}")
            else:
                print(f"DEBUG: get_by_public_id - Nessun ruolo trovato per public_id: {public_id}")
            return {'ID': ruolo.ID, 'public_id': ruolo.public_id, 'DESCR': ruolo.DESCR} if ruolo else None
        finally:
            session.close()

    def get_all(self):
        session = self.SessionLocal()
        try:
            print("DEBUG: get_all - Recuperando tutti i ruoli.")
            ruoli = session.query(TRuolo).all()
            print(f"DEBUG: get_all - Trovati {len(ruoli)} ruoli.")
            return [{'ID': r.ID, 'public_id': r.public_id, 'DESCR': r.DESCR} for r in ruoli]
        finally:
            session.close()

    def get_by_description(self, description):
        """
        Recupera un ruolo dal database tramite la sua descrizione.
        """
        session = self.SessionLocal()
        try:
            print(f"DEBUG: get_by_description - Cercando ruolo con descrizione: '{description}'")
            ruolo = session.query(TRuolo).filter_by(DESCR=description).first()
            if ruolo:
                print(f"DEBUG: get_by_description - Trovato ruolo: {ruolo.DESCR}, ID: {ruolo.ID}")
            else:
                print(f"DEBUG: get_by_description - Nessun ruolo trovato per descrizione: '{description}'")
            return ruolo # Restituisce l'oggetto TRuolo o None
        except SQLAlchemyError as e:
            logging.error(f"ERRORE: get_by_description - Errore durante la ricerca ruolo per descrizione '{description}': {e}")
            return None
        finally:
            session.close()

    def update(self, public_id, desc_ruolo):
        session = self.SessionLocal()
        try:
            print(f"DEBUG: update - Aggiornando ruolo con public_id: {public_id}, nuova DESCR: {desc_ruolo}")
            ruolo = session.query(TRuolo).filter_by(public_id=public_id).first()
            if ruolo:
                ruolo.DESCR = desc_ruolo
                session.commit()
                logging.info(f"DEBUG: update - Ruolo con public_id {public_id} aggiornato con successo.")
                return {'ID': ruolo.ID, 'public_id': ruolo.public_id, 'DESCR': ruolo.DESCR}, 200
            else:
                print(f"DEBUG: update - Nessun ruolo trovato per public_id: {public_id}")
                return {'Error': f'No match found for this public_id: {public_id}'}, 404
        except Exception as e:
            session.rollback()
            logging.error(f"ERRORE: update - Error updating ruolo with public_id {public_id}: {e}")
            return {'Error': str(e)}, 500
        finally:
            session.close()

    def delete(self, public_id):
        session = self.SessionLocal()
        try:
            print(f"DEBUG: delete - Eliminando ruolo con public_id: {public_id}")
            ruolo = session.query(TRuolo).filter_by(public_id=public_id).first()
            if ruolo:
                session.delete(ruolo)
                session.commit()
                logging.info(f"DEBUG: delete - Ruolo con public_id {public_id} eliminato con successo.")
                return {'message': f'Ruolo with public_id {public_id} deleted successfully'}, 200
            else:
                print(f"DEBUG: delete - Nessun ruolo trovato per public_id: {public_id}")
                return {'Error': f'No match found for this public_id: {public_id}'}, 404
        except Exception as e:
            session.rollback()
            logging.error(f"ERRORE: delete - Error deleting ruolo with public_id {public_id}: {e}")
            return {'Error': str(e)}, 500
        finally:
            session.close()
