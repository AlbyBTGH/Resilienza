# Classi/ClasseAnagrafica/ClasseAmbito/Repository_t_ambito.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from Classi.ClasseAnagrafica.ClasseAmbito.Domain_t_ambito import TAmbito
import logging
from datetime import datetime

class Repository_t_ambito:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session

    def create_table_if_not_exists(self):
        session = self.Session()
        try:
            TAmbito.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 'ambito' creata o già esistente (secondo il modello TAmbito).")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 'ambito': {str(e)}")
            raise
        finally:
            session.close()

    def get_all(self):
        """Recupera tutti gli ambiti e li restituisce come lista di dizionari."""
        session = self.Session()
        try:
            ambiti_db = session.query(TAmbito).all()
            ambiti_data = []
            for ambito in ambiti_db:
                ambiti_data.append({
                    'id': ambito.id,
                    'codice': ambito.codice,
                    'descrizione': ambito.descrizione,
                    'note': ambito.note,
                    'data_ultima_modifica': ambito.data_ultima_modifica.isoformat() if ambito.data_ultima_modifica else None,
                    'modificato_da': ambito.modificato_da
                })
            logging.info(f"Recuperati {len(ambiti_data)} ambiti (come dizionari).")
            return ambiti_data # Restituisce una lista di dizionari
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero di tutti gli ambiti: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_id(self, ambito_id: int):
        """Recupera un ambito tramite ID e lo restituisce come dizionario."""
        session = self.Session()
        try:
            ambito = session.query(TAmbito).filter_by(id=ambito_id).first()
            if ambito:
                return {
                    'id': ambito.id,
                    'codice': ambito.codice,
                    'descrizione': ambito.descrizione,
                    'note': ambito.note,
                    'data_ultima_modifica': ambito.data_ultima_modifica.isoformat() if ambito.data_ultima_modifica else None,
                    'modificato_da': ambito.modificato_da
                }
            return None
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero ambito {ambito_id}: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_codice(self, codice: str):
        """Recupera un ambito tramite codice."""
        session = self.Session()
        try:
            return session.query(TAmbito).filter_by(codice=codice).first()
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero ambito per codice {codice}: {str(e)}")
            raise
        finally:
            session.close()

    def get_by_codice_excluding_self(self, codice: str, exclude_id: int):
        """Recupera un ambito tramite codice, escludendo un ID specifico."""
        session = self.Session()
        try:
            return session.query(TAmbito).filter(TAmbito.codice == codice, TAmbito.id != exclude_id).first()
        except SQLAlchemyError as e:
            logging.error(f"Errore nel recupero ambito per codice {codice} (escludendo {exclude_id}): {str(e)}")
            raise
        finally:
            session.close()

    def create(self, codice: str, descrizione: str, note: str = None, creato_da: str = 'system'):
        """Crea un nuovo ambito nel database."""
        session = self.Session()
        try:
            new_ambito = TAmbito(
                codice=codice,
                descrizione=descrizione,
                note=note,
                modificato_da=creato_da,
                data_ultima_modifica=datetime.now()
            )
            session.add(new_ambito)
            session.commit()
            session.refresh(new_ambito)
            logging.info(f"Ambito '{new_ambito.codice}' creato con successo (ID: {new_ambito.id}).")
            return {
                'id': new_ambito.id,
                'codice': new_ambito.codice,
                'descrizione': new_ambito.descrizione,
                'note': new_ambito.note,
                'data_ultima_modifica': new_ambito.data_ultima_modifica.isoformat() if new_ambito.data_ultima_modifica else None,
                'modificato_da': new_ambito.modificato_da
            }
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nella creazione dell'ambito: {str(e)}")
            raise
        finally:
            session.close()

    def update(self, ambito_id: int, descrizione: str, note: str = None, modificato_da: str = 'system'):
        """Aggiorna un ambito esistente nel database."""
        session = self.Session()
        try:
            ambito = session.query(TAmbito).filter_by(id=ambito_id).first()
            if ambito:
                ambito.descrizione = descrizione
                ambito.note = note
                ambito.data_ultima_modifica = datetime.now()
                ambito.modificato_da = modificato_da
                session.commit()
                session.refresh(ambito)
                logging.info(f"Ambito {ambito_id} aggiornato.")
                return {
                    'id': ambito.id,
                    'codice': ambito.codice,
                    'descrizione': ambito.descrizione,
                    'note': ambito.note,
                    'data_ultima_modifica': ambito.data_ultima_modifica.isoformat() if ambito.data_ultima_modifica else None,
                    'modificato_da': ambito.modificato_da
                }
            return None
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'aggiornamento dell'ambito {ambito_id}: {str(e)}")
            raise
        finally:
            session.close()

    def delete(self, ambito_id: int):
        """Elimina fisicamente un ambito dal database."""
        session = self.Session()
        try:
            ambito = session.query(TAmbito).filter_by(id=ambito_id).first()
            if ambito:
                session.delete(ambito)
                session.commit()
                logging.info(f"Ambito {ambito_id} eliminato fisicamente.")
                return True
            return False
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore nell'eliminazione dell'ambito {ambito_id}: {str(e)}")
            raise
        finally:
            session.close()