# Classi/Classe_menu_principale/Repository_t_menu_principale.py
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from Classi.Classe_menu_principale.Domain_t_menu_principale import TMenuPrincipale
import json
import logging
from sqlalchemy.exc import SQLAlchemyError # Import SQLAlchemyError

class Repository_t_menu_principale: # Changed class name to Repository_t_menu_principale for consistency
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.Session = Session # Store the Session factory, not an active session

    def get_menu_principale(self):
        session = self.Session() # Get a new session for each operation
        try:
            results = session.query(TMenuPrincipale).order_by(TMenuPrincipale.ordinatore).all()
            return [
                {
                    'id': result.id,
                    'titolo': result.titolo,
                    'label': result.label,
                    'icon': result.icon,
                    'link': result.link,
                    'ordinatore': result.ordinatore,
                    'foto': result.foto,
                    'target': result.target,
                    'dataCancellazione': result.dataCancellazione
                }
                for result in results
            ]
        except SQLAlchemyError as e: # Catch specific SQLAlchemy errors
            session.rollback()
            logging.error(f"Errore in get_menu_principale: {str(e)}")
            return [] # Return an empty list on error
        except Exception as e: # Catch any other unexpected errors
            session.rollback()
            logging.error(f"Errore generico in get_menu_principale: {str(e)}")
            return [] # Return an empty list on error
        finally:
            session.close() # Ensure the session is closed

    def get_by_id(self, id):
        session = self.Session()
        try:
            result = session.query(TMenuPrincipale).filter_by(id=id).first()
            if not result:
                return None # Return None if not found, let service handle 404

            return {
                'id': result.id,
                'titolo': result.titolo,
                'label': result.label,
                'icon': result.icon,
                'link': result.link,
                'ordinatore': result.ordinatore,
                'foto': result.foto,
                'target': result.target,
                'dataCancellazione': result.dataCancellazione
            }
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore in get_by_id: {str(e)}")
            raise e # Re-raise for service to handle
        finally:
            session.close()

    def get_by_title(self, title):
        session = self.Session()
        try:
            result = session.query(TMenuPrincipale).filter_by(titolo=title, dataCancellazione=None).first()
            if not result:
                return None
            return result
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"Errore in get_by_title: {str(e)}")
            raise e
        finally:
            session.close()
