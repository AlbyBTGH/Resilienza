# Classi/ClasseUtenti/Classe_t_funzionalita/Repository_t_funzionalita.py
from sqlalchemy.exc import SQLAlchemyError
from Classi.ClasseDB.db_connection import engine
from sqlalchemy.orm import sessionmaker
import logging
from Classi.ClasseUtenti.Classe_t_funzionalita.Domain_t_funzionalita import TFunzionalita
from Classi.ClasseUtenti.Classe_t_funzionalitaUtenti.Domain_t_funzionalitaUtente import TFunzionalitaUtente
from Classi.ClasseUtenti.Classe_t_ruolo.Domain_t_ruolo import TRuolo # Import the Role model
import json

class TFunzionalitaRepository:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def create_table_if_not_exists(self):
        """Creates the t_funzionalita table if it doesn't already exist."""
        session = self.Session()
        try:
            # Create the t_funzionalita table if it doesn't exist
            TFunzionalita.__table__.create(bind=engine, checkfirst=True)
            logging.info("Table 't_funzionalita' created or already exists.")
        except SQLAlchemyError as e:
            logging.error(f"Error creating table 't_funzionalita': {str(e)}")
            raise
        finally:
            session.close()

    def get_all(self):
        session = self.Session()
        try:
            results = session.query(TFunzionalita).order_by(TFunzionalita.ordinatore).all()
            return [{'id': result.id, 'fkPadre': result.fkPadre, 'titolo': result.titolo,
                     'label': result.label, 'icon': result.icon, 'link': result.link,
                     'ordinatore': result.ordinatore, 'target': result.target,
                     'dataCancellazione': result.dataCancellazione,
                     'fkMenuPrincipale': result.fkMenuPrincipale} for result in results]
        except Exception as e:
            session.rollback()
            return {'Error': str(e)}, 500
        finally:
            session.close()

    def get_by_id(self, funzionalita_id):
        session = self.Session()
        try:
            result = session.query(TFunzionalita).filter_by(id=funzionalita_id, dataCancellazione=None).first()
            if not result:
                return {'Error': 'Funzionalità non trovata'}, 404
            
            return {
                'id': result.id, 
                'menuPrincipale': result.menuPrincipale, 
                'fkPadre': result.fkPadre, 
                'titolo': result.titolo,
                'label': result.label, 
                'icon': result.icon, 
                'link': result.link,
                'ordinatore': result.ordinatore, 
                'target': result.target,
                'dataCancellazione': result.dataCancellazione,
                'fkMenuPrincipale': result.fkMenuPrincipale
            }
        except Exception as e:
            session.rollback()
            logging.error(f"Error in get_by_id: {str(e)}")
            return {'Error': str(e)}, 500
        finally:
            session.close()

    def get_all_by_menu_iniziale(self, fkMenuPrincipale):
        session = self.Session()
        try:
            results = session.query(TFunzionalita).filter_by(
                fkMenuPrincipale=fkMenuPrincipale,
                dataCancellazione=None
            ).order_by(TFunzionalita.ordinatore).all()
            return [{'id': result.id, 'fkPadre': result.fkPadre, 'titolo': result.titolo,
                     'label': result.label, 'icon': result.icon, 'link': result.link,
                     'ordinatore': result.ordinatore, 'target': result.target,
                     'dataCancellazione': result.dataCancellazione,
                     'fkMenuPrincipale': result.fkMenuPrincipale} for result in results]
        except Exception as e:
            session.rollback()
            return {'Error': str(e)}, 500
        finally:
            session.close()

    def get_by_padre(self, fkPadre):
        session = self.Session()
        try:
            results = session.query(TFunzionalita).filter_by(
                fkPadre=fkPadre,
                dataCancellazione=None
            ).order_by(TFunzionalita.ordinatore).all()
            return [{'id': result.id, 'fkPadre': result.fkPadre, 'titolo': result.titolo,
                     'label': result.label, 'icon': result.icon, 'link': result.link,
                     'ordinatore': result.ordinatore, 'target': result.target,
                     'dataCancellazione': result.dataCancellazione,
                     'fkMenuPrincipale': result.fkMenuPrincipale} for result in results]
        except Exception as e:
            session.rollback()
            return {'Error': str(e)}, 500
        finally:
            session.close()

    def can_access(self, user_role_id, page_link):
        session = self.Session()
        try:
            # Find the functionality based on the link (the requested page)
            funzionalita = session.query(TFunzionalita).filter_by(link=page_link, dataCancellazione=None).first()
            if not funzionalita:
                return False, False # Functionality does not exist or is deleted

            # Check if there is a specific permission for this role and functionality
            funzionalita_utente = session.query(TFunzionalitaUtente).filter(
                TFunzionalitaUtente.fkIdRuolo == user_role_id, # Corrected to fkIdRuolo
                TFunzionalitaUtente.fkFunzionalita == funzionalita.id
            ).first()

            if not funzionalita_utente:
                return False, False

            if funzionalita_utente.permessi == True: # True for 1, False for 0
                return True, True
            else:
                return True, False

        except Exception as e:
            session.rollback()
            return False, False
        finally:
            session.close()

    def get_funzionalita_by_role_and_menu(self, ruolo_id, app_id):
        session = self.Session()
        try:
            # Query to get the functionalities the user can see
            # Filtering by role, main menu, and non-deleted items
            funzionalita = session.query(TFunzionalita).\
                join(TFunzionalitaUtente, TFunzionalita.id == TFunzionalitaUtente.fkFunzionalita).\
                filter(
                    TFunzionalitaUtente.fkIdRuolo == ruolo_id, # Corrected to fkIdRuolo
                    TFunzionalita.fkMenuPrincipale == app_id,
                    TFunzionalita.dataCancellazione.is_(None)
                ).\
                order_by(TFunzionalita.ordinatore).all()
            
            return funzionalita
        except Exception as e:
            session.rollback()
            logging.error(f"Error in get_funzionalita_by_role_and_menu: {str(e)}")
            raise e
        finally:
            session.close()
