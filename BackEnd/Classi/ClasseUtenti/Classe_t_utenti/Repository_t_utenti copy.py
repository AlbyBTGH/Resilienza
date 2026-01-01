# Classi/ClasseUtenti/Classe_t_utenti/Repository_t_utenti.py
from sqlalchemy.orm import sessionmaker
from Classi.ClasseDB.db_connection import engine
from sqlalchemy.exc import SQLAlchemyError
import logging
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from Classi.ClasseUtenti.Classe_t_utenti.Domain_t_utenti import TUtenti
from Classi.ClasseUtenti.Classe_t_ruolo.Domain_t_ruolo import TRuolo # Importa il modello TRuolo
from sqlalchemy.sql import func
from datetime import datetime

class Repository_t_utenti:
    def __init__(self):
        self.SessionLocal = sessionmaker(bind=engine)

    def create_table_if_not_exists(self):
        """Crea la tabella t_utenti se non esiste già."""
        session = self.SessionLocal()
        try:
            TUtenti.__table__.create(bind=engine, checkfirst=True)
            logging.info("Tabella 't_utenti' creata o già esistente.")
        except SQLAlchemyError as e:
            logging.error(f"Errore durante la creazione della tabella 't_utenti': {str(e)}")
            raise
        finally:
            session.close()

    def create_default_admin_user(self):
        session = self.SessionLocal()
        try:
            # Recupera il ruolo 'Admin' usando DESCR, come definito in Domain_t_ruolo.py
            admin_role = session.query(TRuolo).filter_by(DESCR='Admin').first()
            if not admin_role:
                logging.error("DEBUG: create_default_admin_user - Ruolo 'Admin' non trovato. Impossibile creare utente admin di default.")
                return None

            # Verifica se esiste già un utente admin di default
            admin_user = session.query(TUtenti).filter_by(email='admin@example.com').first()
            if not admin_user:
                hashed_password = generate_password_hash("password", method='pbkdf2:sha256')
                new_admin = TUtenti(
                    public_id=str(uuid.uuid4()),
                    username='admin',
                    nome='Admin',
                    cognome='User',
                    # Assegna a fkIdRuolo, come definito in Domain_t_utenti.py
                    fkIdRuolo=admin_role.ID,
                    attivo=True,
                    email='admin@example.com',
                    password=hashed_password,
                    data_creazione=func.now(),
                    ultimo_accesso=func.now()
                )
                session.add(new_admin)
                session.commit()
                logging.info("DEBUG: create_default_admin_user - Utente 'admin@example.com' predefinito creato con successo.")
                return new_admin # Restituisci l'utente appena creato
            else:
                logging.info("DEBUG: create_default_admin_user - Utente 'admin@example.com' predefinito già esistente.")
                return admin_user # Restituisci l'utente esistente
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"ERRORE: create_default_admin_user - Errore durante la creazione dell'utente admin predefinito: {e}")
            raise
        finally:
            session.close()

    def get_user_by_email(self, email):
        session = self.SessionLocal()
        try:
            print(f"DEBUG: get_user_by_email - Cercando utente con email: {email}")
            user = session.query(TUtenti).filter_by(email=email).first()
            if user:
                print(f"DEBUG: get_user_by_email - Trovato utente: {user.email}, ID: {user.id}")
            else:
                print(f"DEBUG: get_user_by_email - Nessun utente trovato per email: {email}")
            return user
        except Exception as e:
            logging.error(f"ERRORE: get_user_by_email - Errore nel recupero utente per email '{email}': {e}")
            raise
        finally:
            session.close()

    def get_user_by_public_id(self, public_id):
        session = self.SessionLocal()
        try:
            print(f"DEBUG: get_user_by_public_id - Cercando utente con public_id: {public_id}")
            user = session.query(TUtenti).filter_by(public_id=public_id).first()
            if user:
                print(f"DEBUG: get_user_by_public_id - Trovato utente: {user.email}, ID: {user.id}")
            else:
                print(f"DEBUG: get_user_by_public_id - Nessun utente trovato per public_id: {public_id}")
            return user
        except Exception as e:
            logging.error(f"ERRORE: get_user_by_public_id - Errore nel recupero utente per public_id '{public_id}': {e}")
            raise
        finally:
            session.close()

    def create_user(self, email, password, nome, cognome, fkIdRuolo):
        session = self.SessionLocal()
        try:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            print(f"DEBUG: create_user - Creazione nuovo utente: {email}, Ruolo ID: {fkIdRuolo}")
            new_user = TUtenti(
                public_id=str(uuid.uuid4()),
                username=email,
                nome=nome,
                cognome=cognome,
                fkIdRuolo=fkIdRuolo,
                attivo=True,
                email=email,
                password=hashed_password,
                data_creazione=func.now(),
                ultimo_accesso=func.now()
            )
            session.add(new_user)
            session.commit()
            logging.info(f"DEBUG: create_user - Utente '{email}' creato con successo.")
            return new_user
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"ERRORE: create_user - Errore durante la creazione dell'utente '{email}': {e}")
            return None
        finally:
            session.close()

    def update_user_last_access(self, user):
        session = self.SessionLocal()
        try:
            print(f"DEBUG: update_user_last_access - Aggiornando ultimo accesso per utente: {user.email}")
            user_in_session = session.merge(user) # Assicurati che l'oggetto user sia nella sessione corrente
            user_in_session.ultimo_accesso = func.now()
            session.commit()
            print(f"DEBUG: update_user_last_access - Ultimo accesso aggiornato per utente: {user.email}")
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(f"ERRORE: update_user_last_access - Errore durante l'aggiornamento dell'ultimo accesso per l'utente '{user.email}': {e}")
        finally:
            session.close()

    def change_password(self, public_id, old_password, new_password):
        session = self.SessionLocal()
        try:
            print(f"DEBUG: change_password - Tentativo cambio password per public_id: {public_id}")
            user = session.query(TUtenti).filter_by(public_id=public_id).first()
            if user and check_password_hash(user.password, old_password):
                user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                session.commit()
                logging.info(f"DEBUG: change_password - Password utente '{user.email}' cambiata con successo.")
                return True
            print(f"DEBUG: change_password - Cambio password fallito per public_id: {public_id} (utente non trovato o password vecchia errata).")
            return False
        except Exception as e:
            session.rollback()
            logging.error(f"ERRORE: change_password - Errore durante il cambio password per l'utente '{public_id}': {e}")
            return False
        finally:
            session.close()
